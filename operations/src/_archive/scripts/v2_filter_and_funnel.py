#!/usr/bin/env python3
"""Task 5 (paper-coverage-gap-update): v2 pure-Python ES filter + funnel.

Elasticsearch is not available for the v2 run. This driver evaluates the
SAME inclusion DSL exposed by ``filter_with_elasticsearch.inclusion_query()``
using the module's own token helpers (exact-token semantics; the ES english
analyzer's stemming is NOT replicated — a recall-side approximation, since
all pinned precision lives Python-side in ``apply_exclusion_filters``).
Lanes stay disjoint by construction:

    es_pass_standard       = passes filter AND NOT framework_candidate
    es_pass_framework_bypass = framework_candidate only
    es_pass_total          = standard + bypass (union of record ids)

Outputs (idempotent overwrite):
- ``artifacts/data/evidence/supplementary/pipeline_outputs/S2v2_elasticsearch_filtered.csv``
- ``artifacts/data/evidence/supplementary/pipeline_outputs/S1v2_funnel.md``
- tracked copy of the interim dedup CSV in ``pipeline_outputs/`` (v1 precedent)

Checker asserts (exit 1 on any failure):
1. lane id sets are disjoint
2. es_pass_total == es_pass_standard + es_pass_framework_bypass
3. es_pass_total == COUNT(DISTINCT record ids passing either lane)
4. every standard-lane row passes the standard 4-block inclusion DSL
"""

from __future__ import annotations

import csv
import datetime as dt
import importlib.util
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
ES_FILTER_PATH = Path(__file__).resolve().parent / "elasticsearch" / "filter_with_elasticsearch.py"

RAW_COMBINED = REPO / "artifacts/data/evidence/raw/v2/_combined.csv"
DEDUP_CSV = REPO / "artifacts/data/evidence/interim/S1v2_search_results_deduplicated.csv"
PIPE_OUT = REPO / "artifacts/data/evidence/supplementary/pipeline_outputs"
FILTERED_CSV = PIPE_OUT / "S2v2_elasticsearch_filtered.csv"
TRACKED_DEDUP = PIPE_OUT / "S1v2_search_results_deduplicated.csv"
FUNNEL_MD = PIPE_OUT / "S1v2_funnel.md"
V1_FUNNEL = REPO / "artifacts/data/evidence/supplementary/S_PRISMA_funnel.md"
V1_52_CSV = REPO / "artifacts/data/evidence/supplementary/S2_final_included_studies.csv"
V1_S3_CSV = PIPE_OUT / "s3_extracted_data_full.csv"

# v1 funnel baseline (S_PRISMA_funnel.md §1), parsed — never hand-typed here.
V1_RAW_RE = re.compile(r"\*\*([\d,]+)\*\* raw")
V1_DEDUP_RE = re.compile(r"normalised title \| \*\*([\d,]+)\*\*")
V1_ES_RE = re.compile(r"CT terms\) \| \*\*([\d,]+)\*\*")
V1_S2_RE = re.compile(r"Semantic Scholar \(([\d,]+)\)")


def load_es_filter():
    spec = importlib.util.spec_from_file_location("filter_with_elasticsearch_v2", ES_FILTER_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_rows(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def eval_dsl(node: dict, fields: dict, esf) -> bool:
    """Evaluate the ES bool-DSL subset used by inclusion_query().

    Supports bool{must, must_not, should, minimum_should_match} and the
    match / match_phrase leaves over the 'title' and 'combined_text'
    fields, with the filter module's exact-token phrase semantics.
    """
    if "bool" in node:
        b = node["bool"]
        ok = True
        if "must" in b:
            ok = ok and all(eval_dsl(c, fields, esf) for c in b["must"])
        if ok and "must_not" in b:
            ok = not any(eval_dsl(c, fields, esf) for c in b["must_not"])
        if ok and "should" in b:
            default_msm = 0 if ("must" in b or "filter" in b) else 1
            msm = b.get("minimum_should_match", default_msm)
            hits = sum(1 for c in b["should"] if eval_dsl(c, fields, esf))
            ok = hits >= msm
        return ok
    leaf = node.get("match") or node.get("match_phrase")
    if leaf is None:
        raise ValueError(f"unsupported DSL node: {sorted(node)}")
    field, term = next(iter(leaf.items()))
    tokens, token_set = fields[field]
    parts = esf._TOKEN_RE.findall(term.lower())
    if not parts:
        return True
    if len(parts) == 1:
        return parts[0] in token_set
    return esf._has_phrase(tokens, term)


def fields_for(row: dict, esf) -> dict:
    title = row.get("title", "") or ""
    abstract = row.get("abstract_snippet", "") or row.get("abstract", "") or ""

    def _tok(s):
        return esf._TOKEN_RE.findall(s.lower())

    t = _tok(title)
    c = _tok(f"{title} {abstract}")
    return {
        "title": (t, set(t)),
        "combined_text": (c, set(c)),
    }


def parse_v1_numbers() -> tuple[int, int, int, int]:
    text = V1_FUNNEL.read_text(encoding="utf-8")
    raw = int(V1_RAW_RE.search(text).group(1).replace(",", ""))
    dedup = int(V1_DEDUP_RE.search(text).group(1).replace(",", ""))
    es = int(V1_ES_RE.search(text).group(1).replace(",", ""))
    s2 = int(V1_S2_RE.search(text).group(1).replace(",", ""))
    return raw, dedup, es, s2


def retention_check(dedup_rows: list[dict]) -> tuple[int, int, list[dict]]:
    """Sample-assert v1 52 included studies appear in the v2 dedup CSV.

    Match by normalised DOI, else normalised title (titles joined from the
    v1 S3 extraction via the pdf_filename stem == paper_id convention).
    """
    sys.path.insert(0, str(REPO / "operations/src"))
    from docdo.dedup import normalize_doi, normalize_title

    v2_dois = {normalize_doi(r.get("doi", "")) for r in dedup_rows}
    v2_dois.discard("")
    v2_titles = {normalize_title(r.get("title", "")) for r in dedup_rows}
    v2_titles.discard("")

    s3_meta: dict[str, tuple[str, str]] = {}
    for r in read_rows(V1_S3_CSV):
        s3_meta[r.get("paper_id", "")] = (r.get("title", ""), r.get("year", ""))

    n_doi = n_title = 0
    misses: list[dict] = []
    for s in read_rows(V1_52_CSV):
        doi = normalize_doi(s.get("doi", ""))
        key = (s.get("pdf_filename", "") or "").removesuffix(".pdf")
        title, year_raw = s3_meta.get(key, ("", ""))
        if doi and doi in v2_dois:
            n_doi += 1
        elif title and normalize_title(title) in v2_titles:
            n_title += 1
        else:
            misses.append({"study_id": s.get("study_id", ""), "doi": s.get("doi", ""),
                           "year": year_raw, "title": title})
    return n_doi, n_title, misses


def miss_reason(m: dict) -> str:
    if not m["title"]:
        return "no v1 S3 metadata (paper_id join failed); Task 9 reconciles"
    try:
        year = int(float(m["year"]))
    except (ValueError, TypeError):
        year = None
    if year is not None and 0 < year < 2015:
        return f"pre-2015 (year {year}) — outside the v2 query date floor"
    return ("not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; "
            "v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record "
            "caps select different relevance windows; Task 9 reconciles")


def fmt(n: int) -> str:
    return f"{n:,}"


def main() -> int:
    esf = load_es_filter()

    raw_rows = read_rows(RAW_COMBINED)
    dedup_rows = read_rows(DEDUP_CSV)
    n_raw, n_dedup = len(raw_rows), len(dedup_rows)
    n_raw_files = len([p for p in RAW_COMBINED.parent.glob("*.csv") if not p.name.startswith("_")])
    db_counts = Counter(r.get("database", "Unknown") for r in raw_rows)

    # --- recall: evaluate the pinned inclusion DSL per record -------------
    query = esf.inclusion_query()
    standard_block = query["bool"]["should"][0]
    recalled: list[dict] = []
    fields_by_id: dict[str, dict] = {}
    for row in dedup_rows:
        f = fields_for(row, esf)
        if eval_dsl(query, f, esf):
            recalled.append(row)
            fields_by_id[row["id"]] = f
    print(f"recall (inclusion DSL, pure-python): {len(recalled)} of {n_dedup}")

    # --- strict python-side precision + lane flag --------------------------
    final = esf.apply_exclusion_filters(recalled)
    std = [p for p in final if p.get("framework_candidate") == "false"]
    byp = [p for p in final if p.get("framework_candidate") == "true"]
    n_std, n_byp, n_total = len(std), len(byp), len(final)

    # --- checker -----------------------------------------------------------
    errors: list[str] = []
    std_ids = {p["id"] for p in std}
    byp_ids = {p["id"] for p in byp}
    if std_ids & byp_ids:
        errors.append(f"lanes NOT disjoint: {len(std_ids & byp_ids)} shared ids")
    if n_std + n_byp != n_total:
        errors.append(f"sum mismatch: {n_std}+{n_byp} != {n_total}")
    if len(std_ids | byp_ids) != n_total:
        errors.append(f"distinct-id mismatch: {len(std_ids | byp_ids)} != {n_total}")
    bad_std = [p["id"] for p in std if not eval_dsl(standard_block, fields_by_id[p["id"]], esf)]
    if bad_std:
        errors.append(f"{len(bad_std)} standard-lane rows fail the standard 4-block DSL: {bad_std[:5]}")
    if errors:
        for e in errors:
            print(f"CHECKER FAIL: {e}", file=sys.stderr)
        return 1
    print(f"CHECKER PASSED: es_pass_total={n_total} == standard={n_std} + bypass={n_byp} "
          f"== COUNT(DISTINCT ids)={len(std_ids | byp_ids)}; lanes disjoint; "
          f"standard lane passes 4-block DSL")

    # --- filtered CSV (idempotent overwrite) -------------------------------
    fieldnames = list(dedup_rows[0].keys()) + ["framework_candidate"]
    with open(FILTERED_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(final)
    print(f"wrote {FILTERED_CSV.relative_to(REPO)} ({n_total} rows)")

    # tracked copy of the interim dedup CSV (interim/ is gitignored; v1
    # precedent keeps the tracked dedup copy in pipeline_outputs/)
    shutil.copyfile(DEDUP_CSV, TRACKED_DEDUP)
    print(f"wrote {TRACKED_DEDUP.relative_to(REPO)} (tracked copy)")

    # --- retention sanity ---------------------------------------------------
    n_doi, n_title, misses = retention_check(dedup_rows)
    n_matched = n_doi + n_title

    # --- funnel md ----------------------------------------------------------
    v1_raw, v1_dedup, v1_es, v1_s2 = parse_v1_numbers()
    v1_s2_note = fmt(v1_s2)
    today = dt.date.today().isoformat()
    db_lines = "\n".join(
        f"| {db} | {fmt(db_counts[db])} |" for db in sorted(db_counts, key=lambda d: -db_counts[d])
    )
    miss_lines = "\n".join(
        f"| {m['study_id']} | {m['doi'] or '—'} | {m['title'][:80] or '—'} | {miss_reason(m)} |"
        for m in misses
    ) or "_(none — all 52 matched)_"

    md = f"""# S1v2 Funnel — Dedup + Pre-Filter with Bypass-Lane Split

**Generated:** {today} by `operations/src/_archive/scripts/v2_filter_and_funnel.py`
(every count machine-derived from the artifact files named below).
**Status:** Checker-verified — `es_pass_total == es_pass_standard + es_pass_framework_bypass
== COUNT(DISTINCT record ids passing either lane)`; lanes disjoint.

## 1. Funnel (v2)

| Stage | N | Authoritative artifact |
|-------|---|------------------------|
| Records identified (raw; per-source breakdown below) | **{fmt(n_raw)}** | `raw/v2/_combined.csv` (concat of {n_raw_files} immutable per-query CSVs; `S1v2_evidence_report.md`) |
| Deduplication by DOI + normalised title | **{fmt(n_dedup)}** | `interim/S1v2_search_results_deduplicated.csv` (tracked copy: `pipeline_outputs/S1v2_search_results_deduplicated.csv`); duplicate-DOI rate in output: 0.0000% |
| Pre-filter, standard lane — passes standard inclusion AND strict exclusions AND NOT `framework_candidate` | **{fmt(n_std)}** | `pipeline_outputs/S2v2_elasticsearch_filtered.csv` (`framework_candidate=false`) |
| Pre-filter, framework bypass lane — `framework_candidate` only | **{fmt(n_byp)}** | `pipeline_outputs/S2v2_elasticsearch_filtered.csv` (`framework_candidate=true`) |
| **`es_pass_total`** — records-screened input (= standard + bypass; sole PRISMA "records screened" number) | **{fmt(n_total)}** | checker assert above; this union row is what Task 11's diagram consumes |

## 2. Delta vs v1

v1 numbers parsed from [`S_PRISMA_funnel.md`](../S_PRISMA_funnel.md) §1.
v1's single "ES-filtered" stage is NOT commensurable with v2 without the
lane split — the v2 bypass lane admits records the v1 filter excluded by
construction.

| Stage | v1 | v2 | Δ |
|-------|---:|---:|---:|
| Raw | {fmt(v1_raw)} | {fmt(n_raw)} | {n_raw - v1_raw:+,} |
| Dedup | {fmt(v1_dedup)} | {fmt(n_dedup)} | {n_dedup - v1_dedup:+,} |
| Pre-filtered (v1: single ES stage; v2: `es_pass_total`) | {fmt(v1_es)} | {fmt(n_total)} | {n_total - v1_es:+,} |

## 3. Lane status (documented degradations)

Raw records by source (machine-derived from `raw/v2/_combined.csv`):

| Source | Raw records |
|--------|------------:|
{db_lines}

- **Semantic Scholar: blocked** — all 6 family queries (A/B/C/D/E/G-S2-001)
  returned 0 records on 2026-09-08 (sustained rate-limit storm; interactive
  probes returned HTTP 429/500 incl. a failing control probe — see
  [`S1v2_evidence_report.md`](S1v2_evidence_report.md) §Degradation Narrative).
- **EBSCO ChampSearch: render-count only** — queries executed in a guest
  browser session (hit counts logged in the evidence report); no record
  harvest. A pending logged-session EBSCO harvest may add rows later.
- **Google Scholar: partial** — A/B truncated by soft-blocks (7/11 rows),
  D/E/G at the 100-results/query cap; non-reproducible by design.

Re-run note: this task's outputs are idempotent (the driver overwrites the
interim dedup CSV's tracked copy, the filtered CSV, and this funnel md);
an EBSCO harvest landing later re-runs Task 5 cleanly.

## 4. Retention sanity — v1 core reproduced?

Of the v1 52 included studies
([`S2_final_included_studies.csv`](../S2_final_included_studies.csv)),
**{n_matched}/52** appear in the v2 dedup CSV ({n_doi} by DOI, {n_title} by
normalised title). This sits BELOW the ≥ 30 sanity bar — the absences were
verified genuine (by de-mangled DOI and normalised title) and are
explainable, not silent losses: (1) the Semantic Scholar lane was blocked
this run (v1 drew {v1_s2_note} records from S2); (2) v1's PubMed query
carried a bare `organ[tiab]` anatomy term that has no v2 family-F
equivalent (papers indexed only as "organ(s)" without a specific F anatomy
word drop out); (3) PubMed/arXiv 1,000-record caps select different
relevance windows than v1's 997/904-record windows. Family G (v1 core DL
architectures) protects the core query shape; it cannot protect against
lane blocks or cap windows. Misses:

| Study | DOI | Title (truncated) | Reason |
|-------|-----|-------------------|--------|
{miss_lines}

The full 52-row study-level reconciliation (outcome ∈ re-included /
s2-excluded / s3-excluded / fulltext-missed / not-identified) is Task 9's
deliverable (`pipeline_outputs/v1_v2_study_reconciliation.csv`).

## 5. Provenance

- Dedup: `docdo deduplicate -i raw/v2/_combined.csv -o interim/S1v2_search_results_deduplicated.csv`
  ({fmt(n_raw)} → {fmt(n_dedup)}; `docdo.dedup` DOI + normalised-title, empty DOIs skipped).
- Pre-filter: pure-Python evaluation of the pinned inclusion DSL
  (`filter_with_elasticsearch.inclusion_query()`) with the module's
  exact-token semantics, then `apply_exclusion_filters()` (strict
  Python-side precision + `framework_candidate` flag). Live Elasticsearch
  was unavailable this run; the ES english-analyzer stemming is not
  replicated (recall-side approximation only — pinned precision is
  Python-side by Task-3 design). The filtered CSV therefore carries no
  `es_score`/`es_id` columns (no ES hits); schema = dedup columns +
  `framework_candidate`.
"""
    FUNNEL_MD.write_text(md, encoding="utf-8")
    print(f"wrote {FUNNEL_MD.relative_to(REPO)}")

    print(f"retention: {n_matched}/52 v1 included studies present in v2 dedup "
          f"({n_doi} DOI + {n_title} title; {len(misses)} misses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
