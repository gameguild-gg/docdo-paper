"""Tests for docdo.fetch_v2 / docdo.fetch_v2_fetchers + ES framework whitelist.

Task 3 of .omo/plans/paper-coverage-gap-update.md. Written BEFORE the
implementation (TDD red phase). All network-touching code is mocked — no live
API calls ever run from this suite.
"""

from __future__ import annotations

import csv
import importlib.util
import math
import re
import sys
import types
from pathlib import Path

import pytest
import yaml as pyyaml
from click.testing import CliRunner
from docdo import config
from docdo.cli import main
from docdo.fetch_v2 import (
    QueriesFileError,
    build_queries,
    dry_run,
    estimate_api_calls,
    load_queries,
)
from docdo.fetch_v2_artifacts import (
    CSV_FIELDS,
    append_provenance,
    concat_raw,
    read_provenance,
    write_raw_csv,
)
from docdo.fetch_v2_fetchers import (
    ARXIV_MAX,
    GS_MAX_RESULTS,
    PUBMED_BATCH,
    PUBMED_MAX,
    S2_PAGE,
    S2_PER_QUERY_LIMIT,
    fetch_arxiv_v2,
    fetch_google_scholar_v2,
    fetch_semantic_scholar_v2,
    render_ebsco_queries,
)

QUERIES_YAML = config.REPO_ROOT / "operations/src/_archive/scripts/queries_v2.yaml"
ES_FILTER_PATH = (
    config.REPO_ROOT / "operations/src/_archive/scripts/elasticsearch/filter_with_elasticsearch.py"
)
FIELD_DBS = ("pubmed", "arxiv", "semantic_scholar")
ALL_DBS = FIELD_DBS + ("google_scholar",)
TEMPLATE_FAMILIES = ("A", "C", "D", "E", "G")


@pytest.fixture()
def queries_data() -> dict:
    return load_queries(QUERIES_YAML)


@pytest.fixture(scope="module")
def es_filter():
    """Load the archived ES filter script as a module (elasticsearch lazy-imported)."""
    spec = importlib.util.spec_from_file_location(
        "filter_with_elasticsearch_under_test", ES_FILTER_PATH
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Group 1 — query builder: template conformance + GS plain-string rendering
# ---------------------------------------------------------------------------


class TestQueryBuilder:
    def test_real_yaml_builds_24_queries(self, queries_data):
        queries = build_queries(queries_data)
        assert len(queries) == 24  # 6 executed families x 4 databases
        ids = [q.query_id for q in queries]
        assert len(set(ids)) == 24

    def test_every_database_covered_for_every_family(self, queries_data):
        queries = build_queries(queries_data)
        for family in ("A", "B", "C", "D", "E", "G"):
            dbs = {q.database for q in queries if q.family == family}
            assert dbs == set(ALL_DBS)

    def test_executed_string_is_block_join(self, queries_data):
        for q in build_queries(queries_data):
            assert q.executed == " AND ".join(q.blocks)

    def test_template_families_have_three_and_blocks(self, queries_data):
        for q in build_queries(queries_data):
            if q.family in TEMPLATE_FAMILIES:
                assert len(q.blocks) == 3, (q.query_id, len(q.blocks))
                # middle block is the (segmentation OR "medical imaging") context
                assert "segmentation" in q.blocks[1] and "medical imaging" in q.blocks[1]
            else:
                assert q.family == "B"
                assert len(q.blocks) == 1, (q.query_id, len(q.blocks))

    def test_gs_blocks_are_plain_phrases(self, queries_data):
        for q in build_queries(queries_data):
            if q.database != "google_scholar":
                continue
            low = q.executed.lower()
            assert "ti:" not in low and "abs:" not in low
            assert "[tiab]" not in low and "[title/abstract]" not in low

    def test_gs_family_b_matrix(self, queries_data):
        """Family-B GS: tool names, NO anatomy, NO AND-segmentation."""
        b_gs = next(
            q for q in build_queries(queries_data)
            if q.family == "B" and q.database == "google_scholar"
        )
        joined = b_gs.executed
        for tool in (
            "MONAI", "Auto3DSeg", "MONAI Label", "MONAI Deploy", "VISTA-3D",
            "NV-Segment-CT", "nnInteractive", "NVIDIA Clara", "Holoscan",
        ):
            assert f'"{tool}"' in joined
        low = joined.lower()
        for anatomy in ("liver", "pancreas", "kidney", "spleen", "lung", "abdominal", "thoracic"):
            assert anatomy not in low
        assert not re.search(r"\bAND\s*\(?\s*\"?segmentation", joined, re.IGNORECASE)

    def test_gs_template_families_carry_terms_and_anatomy(self, queries_data):
        """A/C/D/E/G GS blocks: family terms + anatomy phrases present."""
        fam_term = {"A": '"knowledge graph"', "C": '"Segment Anything"', "D": '"Mamba"',
                    "E": '"TotalSegmentator"', "G": '"nnU-Net"'}
        for q in build_queries(queries_data):
            if q.database != "google_scholar" or q.family not in TEMPLATE_FAMILIES:
                continue
            assert fam_term[q.family] in q.executed, q.query_id
            for anatomy in ('"liver"', '"pancreas"', '"computed tomography"'):
                assert anatomy in q.executed, (q.query_id, anatomy)

    def test_pubmed_keeps_wildcards_others_expanded(self, queries_data):
        for q in build_queries(queries_data):
            if q.family != "B":
                continue
            if q.database == "pubmed":
                for stem in ("radiolog*", "tomograph*", "reproducib*"):
                    assert stem in q.executed
            else:
                assert "*" not in q.executed, q.query_id
                assert "reproducibility" in q.executed or "reproducible" in q.executed

    def test_load_queries_rejects_unparseable_yaml(self, tmp_path):
        bad = tmp_path / "corrupt.yaml"
        bad.write_text("{{{ not : valid : yaml\n\t-[", encoding="utf-8")
        with pytest.raises(QueriesFileError):
            load_queries(bad)

    def test_load_queries_rejects_wrong_structure(self, tmp_path):
        bad = tmp_path / "wrong.yaml"
        bad.write_text(pyyaml.safe_dump({"version": "2"}), encoding="utf-8")
        with pytest.raises(QueriesFileError):
            load_queries(bad)

    def test_load_queries_rejects_non_string_blocks(self, tmp_path):
        bad = tmp_path / "blocks.yaml"
        bad.write_text(
            pyyaml.safe_dump(
                {"executed_families": {"A": {"queries": {
                    "pubmed": {"query_id": "A-PUB-001", "blocks": [1, 2]}}}}}
            ),
            encoding="utf-8",
        )
        with pytest.raises(QueriesFileError):
            load_queries(bad)

    def test_estimate_api_calls(self, queries_data):
        est = {q.query_id: estimate_api_calls(q) for q in build_queries(queries_data)}
        assert est["A-PUB-001"] == 1 + math.ceil(PUBMED_MAX / PUBMED_BATCH)
        assert est["A-ARX-001"] == math.ceil(ARXIV_MAX / 100)
        assert est["A-S2-001"] == math.ceil(S2_PER_QUERY_LIMIT / S2_PAGE)
        assert est["A-GS-001"] == math.ceil(GS_MAX_RESULTS / 10)

    def test_dry_run_is_offline(self, monkeypatch):
        def _boom(*args, **kwargs):  # pragma: no cover - must never run
            raise AssertionError("network touched during dry-run")

        import requests
        from Bio import Entrez

        monkeypatch.setattr(requests, "get", _boom)
        monkeypatch.setattr(requests, "post", _boom)
        monkeypatch.setattr(Entrez, "esearch", _boom)

        plan, ebsco = dry_run(QUERIES_YAML)
        assert len(plan) == 24
        for query_id, db, calls in plan:
            assert query_id and db in ALL_DBS and isinstance(calls, int) and calls >= 1
        assert len(ebsco) == 6
        for family, (query_id, rendered) in ebsco.items():
            assert query_id.startswith(f"{family}-EBSCO")
            assert "ti:" not in rendered and "abs:" not in rendered


# ---------------------------------------------------------------------------
# Group 2 — ES framework whitelist: whole-token semantics + bypass audit
# ---------------------------------------------------------------------------

BYPASS_SAMPLES = [
    ("MONAI: An open-source framework for deep learning in healthcare", ""),
    ("auto3dseg automates medical imaging model design", ""),
    ("MONAI Label: intelligent annotation for radiology", ""),
    ("monai deploy packaging of inference pipelines", ""),
    ("VISTA-3D: promptable 3D segmentation without finetuning", ""),
    ("NV-Segment-CT industry technical documentation", ""),
    ("nnInteractive: interactive segmentation revisited", ""),
    ("NVIDIA Clara platform overview", ""),
    ("Holoscan streaming deployment for sensors", ""),
    ("An open-source toolkit for tomographic reconstruction", ""),
    ("DICOM integration in a clinical workflow for radiology departments", ""),
    ("Reproducibility of PACS deployment in medical imaging", ""),
]

NON_BYPASS_SAMPLES = [
    ("VISTAable networks for vision tasks", ""),
    ("SAMPLE-efficient reinforcement learning agents", ""),
    ("A MONAIable approach to nothing", ""),
    ("A toolkit for natural language processing pipelines", ""),
    ("Advances in computed tomography image quality", ""),
    ("Deployment of web services for e-commerce", ""),
    ("The Grand Challenge of machine translation", ""),
    ("Microservice architectures for cloud computing", ""),
    ("PACS: polynomial approximation and curve splines", ""),
    ("Deep learning for CT segmentation of lungs", ""),
    ("A software suite for video streaming", ""),
    ("Random forest classification of iris flowers", ""),
]


class TestEsWhitelist:
    def test_true_positives_bypass(self, es_filter):
        for title, abstract in BYPASS_SAMPLES:
            assert es_filter.is_framework_candidate(title, abstract), title

    def test_no_substring_false_positives(self, es_filter):
        for title, abstract in NON_BYPASS_SAMPLES:
            assert not es_filter.is_framework_candidate(title, abstract), title

    def test_anchor_required_for_vocabulary_lane(self, es_filter):
        # vocabulary without a medical-imaging anchor must NOT bypass
        assert not es_filter.is_framework_candidate(
            "A toolkit for e-commerce deployment", ""
        )
        # anchor without vocabulary must NOT bypass
        assert not es_filter.is_framework_candidate(
            "Novel loss for tomographic reconstruction", ""
        )
        # vocab + anchor does bypass
        assert es_filter.is_framework_candidate(
            "A toolkit for tomographic reconstruction", ""
        )

    def test_match_in_abstract_only(self, es_filter):
        assert es_filter.is_framework_candidate(
            "A deployment study", "we present a software framework for medical imaging"
        )

    def test_whole_token_not_substring(self, es_filter):
        # 'CT' as exact token: inside another word must not serve as anchor
        assert not es_filter.is_framework_candidate(
            "A toolkit for SCATTER plots", ""
        )
        # exact token 'ct' does serve as anchor
        assert es_filter.is_framework_candidate("A toolkit for CT reading", "")

    def test_synthetic_bypass_audit_sample(self, es_filter):
        """20+ record audit: exact expected bypass set, no substring leaks."""
        records = []
        for i, (title, abstract) in enumerate(BYPASS_SAMPLES):
            records.append({"id": f"B{i+1:02d}", "title": title,
                            "abstract_snippet": abstract, "expect": True})
        for i, (title, abstract) in enumerate(NON_BYPASS_SAMPLES):
            records.append({"id": f"N{i+1:02d}", "title": title,
                            "abstract_snippet": abstract, "expect": False})
        assert len(records) >= 20
        flagged = {r["id"] for r in records
                   if es_filter.is_framework_candidate(r["title"], r["abstract_snippet"])}
        expected = {r["id"] for r in records if r["expect"]}
        assert flagged == expected

    def test_bypass_records_carry_flag_and_lanes_disjoint(self, es_filter):
        papers = [
            # passes standard filter, no whitelist terms
            {"id": "std-ok", "title": "3D U-Net for Liver Segmentation from CT Scans",
             "abstract_snippet": "A volumetric 3D CNN approach for abdominal organ "
                                 "segmentation; the network architecture is evaluated "
                                 "on CT volumes of the liver."},
            # framework candidate lacking the 3D/volumetric/CT/segmentation requirement
            {"id": "fw-no3d", "title": "MONAI Deploy for multi-organ inference",
             "abstract_snippet": "A software framework for medical imaging; the model "
                                 "deployment approach targets abdominal imaging units."},
            # framework candidate without any CT mention (skips the CT requirement)
            {"id": "fw-noct", "title": "Holoscan toolkit for radiology workflows",
             "abstract_snippet": "A microservice model for clinical workflow "
                                 "deployment in multi-organ imaging."},
            # fails 3D requirement, not a framework candidate -> excluded
            {"id": "plain-no3d", "title": "Image registration study",
             "abstract_snippet": "A method for aligning abdominal images."},
        ]
        filtered = es_filter.apply_exclusion_filters(papers)
        by_id = {p["id"]: p for p in filtered}
        assert "std-ok" in by_id and "fw-no3d" in by_id and "fw-noct" in by_id
        assert "plain-no3d" not in by_id  # excluded: no 3D/volumetric method
        # bypass records carry the flag
        assert by_id["fw-no3d"].get("framework_candidate") == "true"
        assert by_id["fw-noct"].get("framework_candidate") == "true"
        assert by_id["std-ok"].get("framework_candidate") == "false"
        # lanes disjoint by construction
        bypass_lane = {p["id"] for p in filtered if p.get("framework_candidate") == "true"}
        standard_lane = {p["id"] for p in filtered if p.get("framework_candidate") != "true"}
        assert "fw-no3d" in bypass_lane and "fw-no3d" not in standard_lane
        assert "std-ok" in standard_lane and "std-ok" not in bypass_lane
        assert not (bypass_lane & standard_lane)

    def test_framework_candidate_can_skip_segmentation_requirement(self, es_filter):
        # detection-flavored framework paper: would fail EC1 without the bypass
        papers = [{
            "id": "fw-detect", "title": "MONAI Label deployment for detection tasks",
            "abstract_snippet": "A software framework for medical imaging; a model "
                                "for multi-organ abdominal annotation.",
        }]
        filtered = es_filter.apply_exclusion_filters(papers)
        assert [p["id"] for p in filtered] == ["fw-detect"]
        assert filtered[0].get("framework_candidate") == "true"


# ---------------------------------------------------------------------------
# Group 3 — concat: self-exclusion, idempotence, stable sort
# ---------------------------------------------------------------------------


def _write_query_csv(raw_dir: Path, name: str, db_label: str, titles: list[str]) -> None:
    path = raw_dir / f"{name}.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(CSV_FIELDS)
        for i, title in enumerate(titles, 1):
            writer.writerow([
                f"R{i:04d}", db_label, "2026-09-08", title, "Author A", "2023",
                "Venue", f"10.1/{name}-{i}", "abstract text",
            ])


@pytest.fixture()
def raw_v2_dir(tmp_path: Path) -> Path:
    raw_dir = tmp_path / "raw" / "v2"
    raw_dir.mkdir(parents=True)
    # deliberately unordered mix of databases and query ids
    _write_query_csv(raw_dir, "G-S2-001", "Semantic Scholar", ["S2 first", "S2 second"])
    _write_query_csv(raw_dir, "B-GS-001", "Google Scholar", ["GS only"])
    _write_query_csv(raw_dir, "C-ARX-001", "arXiv", ["arXiv b", "arXiv a"])
    _write_query_csv(raw_dir, "A-PUB-001", "PubMed", ["PubMed 2", "PubMed 1"])
    # derived/metadata files must never be concatenated
    prov = raw_dir / "_provenance.csv"
    with prov.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["query_id", "database", "family", "search_date",
                         "record_count", "status"])
        writer.writerow(["A-PUB-001", "pubmed", "A", "2026-09-08", 2, "ok"])
    # a stale combined file (garbage) that must be excluded from its own input
    (raw_dir / "_combined.csv").write_text("garbage,rows\n1,2\n", encoding="utf-8")
    return raw_dir


class TestConcat:
    def test_concat_sorts_by_database_then_query_id(self, raw_v2_dir):
        combined = concat_raw(raw_v2_dir)
        assert combined == raw_v2_dir / "_combined.csv"
        with combined.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        order = [(r["database"], t) for r, t in
                 zip(rows, ["GS only", "PubMed 2", "PubMed 1", "S2 first", "S2 second",
                            "arXiv b", "arXiv a"])]
        # stable sort by (database label, query_id): Google Scholar < PubMed
        # < Semantic Scholar < arXiv (byte-order on the label)
        assert [r["database"] for r in rows] == [
            "Google Scholar", "PubMed", "PubMed", "Semantic Scholar",
            "Semantic Scholar", "arXiv", "arXiv",
        ]
        assert order[0] == ("Google Scholar", "GS only")
        assert rows[5]["title"] == "arXiv b" and rows[6]["title"] == "arXiv a"
        assert len(rows) == 7

    def test_concat_idempotent_and_self_excluding(self, raw_v2_dir):
        first = concat_raw(raw_v2_dir).read_bytes()
        second = concat_raw(raw_v2_dir).read_bytes()
        assert first == second  # no row doubling, no self-inclusion
        assert b"garbage" not in first  # stale _combined.csv never fed back in
        with (raw_v2_dir / "_combined.csv").open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        assert len(rows) == 7  # 2+1+2+2 per-query rows only, no provenance rows
        assert all(r["title"] != "A-PUB-001" for r in rows)

    def test_concat_preserves_in_file_order(self, raw_v2_dir):
        concat_raw(raw_v2_dir)
        with (raw_v2_dir / "_combined.csv").open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        pubmed_titles = [r["title"] for r in rows if r["database"] == "PubMed"]
        assert pubmed_titles == ["PubMed 2", "PubMed 1"]


# ---------------------------------------------------------------------------
# Group 4 — CSV schema: leading id column, v1 column order, immutability
# ---------------------------------------------------------------------------


class TestCsvSchema:
    def test_fields_match_v1_exactly(self):
        assert CSV_FIELDS == [
            "id", "database", "search_date", "title", "authors",
            "year", "journal_conference", "doi", "abstract_snippet",
        ]

    def test_write_raw_csv_header_and_ids(self, tmp_path):
        out = tmp_path / "A-PUB-001.csv"
        rows = [
            {"database": "PubMed", "title": f"T{i}", "authors": "A",
             "year": "2023", "journal_conference": "V", "doi": f"10.1/{i}",
             "abstract_snippet": "abs", "search_date": "2026-09-08"}
            for i in (1, 2)
        ]
        write_raw_csv(out, rows)
        lines = out.read_text(encoding="utf-8").splitlines()
        assert lines[0] == "id,database,search_date,title,authors,year,journal_conference,doi,abstract_snippet"
        with out.open(newline="", encoding="utf-8") as fh:
            back = list(csv.DictReader(fh))
        assert [r["id"] for r in back] == ["R0001", "R0002"]

    def test_write_raw_csv_immutable(self, tmp_path):
        out = tmp_path / "B-GS-001.csv"
        write_raw_csv(out, [])
        with pytest.raises(FileExistsError):
            write_raw_csv(out, [{"database": "Google Scholar", "title": "x"}])

    def test_provenance_roundtrip(self, tmp_path):
        append_provenance(tmp_path, query_id="A-PUB-001", database="pubmed",
                          family="A", search_date="2026-09-08",
                          record_count=5, status="ok")
        append_provenance(tmp_path, query_id="B-GS-001", database="google_scholar",
                          family="B", search_date="2026-09-08",
                          record_count=0, status="blocked: CAPTCHA")
        rows = read_provenance(tmp_path)
        assert len(rows) == 2
        assert rows[0]["query_id"] == "A-PUB-001" and rows[0]["record_count"] == "5"
        assert rows[1]["status"].startswith("blocked")


# ---------------------------------------------------------------------------
# Group 5 — fetcher contracts (fully mocked network)
# ---------------------------------------------------------------------------


class _FakeResponse:
    def __init__(self, *, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data or {}
        self.text = text

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._json


ARXIV_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2406.05285v1</id>
    <title>VISTA-3D for segmentation</title>
    <summary>An abstract about segmentation.</summary>
    <published>2024-06-01T00:00:00Z</published>
    <author><name>Ann Author</name></author>
    <author><name>Bob Author</name></author>
    <arxiv:doi xmlns:arxiv="http://arxiv.org/schemas/atom">10.1000/test</arxiv:doi>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2011.08506v2</id>
    <title>MONAI framework</title>
    <summary>Another abstract.</summary>
    <published>2020-11-01T00:00:00Z</published>
    <author><name>Cid Author</name></author>
  </entry>
</feed>
"""


class TestFetcherContracts:
    def test_arxiv_uses_params_encoding_with_date_range(self, monkeypatch):
        import docdo.fetch_v2_fetchers as fvf

        captured = {}

        def fake_get(url, params=None, timeout=None):
            captured["url"] = url
            captured["params"] = params
            return _FakeResponse(text=ARXIV_ATOM)

        monkeypatch.setattr(fvf.requests, "get", fake_get)
        query = '(ti:"liver" OR abs:"liver")'
        rows, status = fetch_arxiv_v2(query, date_start="2015-01-01",
                                      date_end="2026-09-08", page_size=100)
        assert status == "ok"
        # params encoding, never string concatenation into the URL
        assert "search_query" not in captured["url"]
        sq = captured["params"]["search_query"]
        assert 'ti:"liver"' in sq
        assert "submittedDate:[201501010000 TO 202609082359]" in sq
        assert len(rows) == 2
        assert rows[0]["database"] == "arXiv"
        assert rows[0]["title"] == "VISTA-3D for segmentation"
        assert rows[0]["doi"] == "10.1000/test"
        assert rows[1]["doi"] == "arXiv:2011.08506"  # no DOI -> arXiv id fallback
        assert rows[0]["authors"].startswith("Ann Author")

    def test_s2_backoff_on_429_then_success(self, monkeypatch):
        import docdo.fetch_v2_fetchers as fvf

        responses = [
            _FakeResponse(status_code=429),
            _FakeResponse(json_data={"data": [{
                "title": "A MONAI paper", "authors": [{"name": "X Y"}],
                "year": 2023, "venue": "MICCAI",
                "externalIds": {"DOI": "10.2/paper"}, "abstract": "abs",
            }], "total": 1}),
        ]
        sleeps = []

        def fake_get(url, params=None, timeout=None):
            return responses.pop(0)

        monkeypatch.setattr(fvf.requests, "get", fake_get)
        monkeypatch.setattr(fvf.time, "sleep", lambda s: sleeps.append(s))
        rows, status = fetch_semantic_scholar_v2("MONAI OR toolkit",
                                                 per_query_limit=100)
        assert status == "ok"
        # 30s progressive 429 backoff first, then the 1s courtesy sleep after success
        assert sleeps == [30, 1]
        assert len(rows) == 1 and rows[0]["doi"] == "10.2/paper"
        assert rows[0]["database"] == "Semantic Scholar"

    def test_s2_year_filter_param(self, monkeypatch):
        import docdo.fetch_v2_fetchers as fvf

        captured = {}

        def fake_get(url, params=None, timeout=None):
            captured["params"] = params
            return _FakeResponse(json_data={"data": [], "total": 0})

        monkeypatch.setattr(fvf.requests, "get", fake_get)
        rows, status = fetch_semantic_scholar_v2("mamba",
                                                 date_start="2015-01-01",
                                                 date_end="2026-09-08")
        assert rows == [] and status == "ok"
        assert captured["params"]["year"] == "2015-2026"

    def test_gs_caps_at_100(self, monkeypatch):
        pubs = [{"bib": {"title": f"Paper {i}", "author": ["A B"],
                         "pub_year": "2023", "venue": "V", "abstract": "abs"}}
                for i in range(150)]

        class FakeScholarly:
            def search_pubs(self, query):
                yield from pubs

        fake_mod = types.ModuleType("scholarly")
        fake_mod.scholarly = FakeScholarly()
        monkeypatch.setitem(sys.modules, "scholarly", fake_mod)
        rows, status = fetch_google_scholar_v2('"MONAI" OR "toolkit"')
        assert status == "ok"
        assert len(rows) == 100  # pinned cap: FIRST 100 results, never more
        assert rows[0]["database"] == "Google Scholar"

    def test_gs_block_recorded_and_continues(self, monkeypatch):
        class FakeScholarly:
            def search_pubs(self, query):
                yield {"bib": {"title": "One", "author": ["A"],
                               "pub_year": "2022", "venue": "", "abstract": ""}}
                raise RuntimeError("CAPTCHA redirect detected")

        fake_mod = types.ModuleType("scholarly")
        fake_mod.scholarly = FakeScholarly()
        monkeypatch.setitem(sys.modules, "scholarly", fake_mod)
        rows, status = fetch_google_scholar_v2('"liver"')
        assert status.startswith("blocked")
        assert len(rows) == 1  # partial results kept, no exception raised

    def test_pubmed_passes_date_range(self, monkeypatch):
        import docdo.fetch_v2_fetchers as fvf
        from Bio import Entrez

        class _Handle:
            def __init__(self, payload):
                self._payload = payload

            def read(self):
                return self._payload

            def close(self):
                pass

        captured = {}

        def fake_esearch(**kwargs):
            captured.update(kwargs)
            return _Handle({"IdList": ["1"], "Count": "1"})

        def fake_efetch(**kwargs):
            return _Handle({"PubmedArticle": [{
                "MedlineCitation": {"PMID": "1", "Article": {
                    "ArticleTitle": "A MONAI paper",
                    "AuthorList": [{"LastName": "Doe", "Initials": "J"}],
                    "Journal": {"Title": "J", "JournalIssue": {"PubDate": {"Year": "2023"}}},
                    "Abstract": {"AbstractText": ["full abstract"]},
                }},
                "PubmedData": {"ArticleIdList": []},
            }]})

        monkeypatch.setattr(Entrez, "esearch", fake_esearch)
        monkeypatch.setattr(Entrez, "efetch", fake_efetch)
        monkeypatch.setattr(Entrez, "read", lambda h: h.read())
        rows, status = fvf.fetch_pubmed_v2("(MONAI[tiab])",
                                           date_start="2015-01-01",
                                           date_end="2026-09-08")
        assert status == "ok" and len(rows) == 1
        assert captured["mindate"] == "2015/01/01"
        assert captured["maxdate"] == "2026/09/08"
        assert captured["datetype"] == "pdat"
        assert captured["term"] == "(MONAI[tiab])"
        assert rows[0]["abstract_snippet"] == "full abstract"  # full, not truncated

    def test_render_ebsco_queries_six_families(self, queries_data):
        rendered = render_ebsco_queries(queries_data)
        assert set(rendered) == {"A", "B", "C", "D", "E", "G"}
        for family, entry in rendered.items():
            assert entry["query_id"] == f"{family}-EBSCO-001"
            assert "ti:" not in entry["query"] and "abs:" not in entry["query"]
            assert " AND " in entry["query"]


# ---------------------------------------------------------------------------
# Group 6 — CLI: dry-run offline, corrupt-yaml exit code, concat flag
# ---------------------------------------------------------------------------


@pytest.fixture()
def runner():
    return CliRunner()


class TestFetchV2CLI:
    def test_help_lists_subcommand(self, runner):
        result = runner.invoke(main, ["fetch-v2", "--help"])
        assert result.exit_code == 0
        assert "--dry-run" in result.output and "--concat" in result.output

    def test_dry_run_prints_estimates_no_network(self, runner, monkeypatch):
        def _boom(*args, **kwargs):  # pragma: no cover
            raise AssertionError("network touched during dry-run")

        import requests
        from Bio import Entrez

        monkeypatch.setattr(requests, "get", _boom)
        monkeypatch.setattr(requests, "post", _boom)
        monkeypatch.setattr(Entrez, "esearch", _boom)

        result = runner.invoke(
            main, ["fetch-v2", "--dry-run", "--queries", str(QUERIES_YAML)]
        )
        assert result.exit_code == 0, result.output
        assert result.output.count("est_calls=") == 24
        assert "A-PUB-001" in result.output
        assert "EBSCO render" in result.output
        assert "no network writes" in result.output

    def test_dry_run_corrupt_yaml_exits_nonzero(self, runner, tmp_path):
        bad = tmp_path / "corrupt.yaml"
        bad.write_text(":\n- [unclosed", encoding="utf-8")
        result = runner.invoke(main, ["fetch-v2", "--dry-run", "--queries", str(bad)])
        assert result.exit_code != 0
        assert "ERROR" in result.output

    def test_concat_flag(self, runner, raw_v2_dir):
        result = runner.invoke(
            main, ["fetch-v2", "--concat", "--output-dir", str(raw_v2_dir)]
        )
        assert result.exit_code == 0, result.output
        assert (raw_v2_dir / "_combined.csv").exists()
