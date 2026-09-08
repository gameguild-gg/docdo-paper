"""Multi-query v2 fetcher orchestration (Task 3): loads queries_v2.yaml,
executes every query per database, and writes ONE immutable raw CSV per
database+query into artifacts/data/evidence/raw/v2/ with the exact v1 column
schema (see fetch_v2_artifacts / fetch_v2_fetchers / fetch_v2_parsers).

queries_v2.yaml contract: each query is a LIST of AND-blocks; the executed
string is " AND ".join(blocks). Family B is a single top-level disjunction
block. PubMed keeps Entrez wildcards; arXiv/S2/GS blocks arrive pre-expanded
and pass through as-is.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from . import config
from .fetch_v2_artifacts import append_provenance, row_count, write_raw_csv
from .fetch_v2_fetchers import (
    ARXIV_MAX,
    ARXIV_PAGE,
    GS_MAX_RESULTS,
    GS_RESULTS_PER_PAGE,
    PUBMED_BATCH,
    PUBMED_MAX,
    S2_PAGE,
    S2_PER_QUERY_LIMIT,
    fetch_arxiv_v2,
    fetch_ebsco,
    fetch_google_scholar_v2,
    fetch_pubmed_v2,
    fetch_semantic_scholar_v2,
    render_ebsco_queries,
)

QUERIES_V2_YAML = config.REPO_ROOT / "operations/src/_archive/scripts/queries_v2.yaml"
RAW_V2_DIR = config.RAW_DIR / "v2"

DATABASES = ("pubmed", "arxiv", "semantic_scholar", "google_scholar")

FETCHERS: dict[str, Callable[..., tuple[list[dict[str, str]], str]]] = {
    "pubmed": fetch_pubmed_v2,
    "arxiv": fetch_arxiv_v2,
    "semantic_scholar": fetch_semantic_scholar_v2,
    "google_scholar": fetch_google_scholar_v2,
}


class QueriesFileError(Exception):
    """queries_v2.yaml is unreadable, unparseable, or violates the block contract."""


@dataclass(frozen=True)
class V2Query:
    family: str
    database: str
    query_id: str
    blocks: tuple[str, ...]

    @property
    def executed(self) -> str:
        return " AND ".join(self.blocks)


def load_queries(path: str | Path | None = None) -> dict[str, Any]:
    path = Path(path) if path else QUERIES_V2_YAML
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise QueriesFileError(f"cannot read queries yaml at {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("executed_families"), dict):
        raise QueriesFileError(f"{path}: missing executed_families mapping")
    for family, fam_def in data["executed_families"].items():
        queries = fam_def.get("queries") if isinstance(fam_def, dict) else None
        if not isinstance(queries, dict):
            raise QueriesFileError(f"family {family}: missing queries mapping")
        missing = [db for db in DATABASES if db not in queries]
        if missing:
            raise QueriesFileError(f"family {family}: missing database blocks {missing}")
        for db, q in queries.items():
            blocks = q.get("blocks") if isinstance(q, dict) else None
            valid = (
                isinstance(q.get("query_id"), str)
                and q["query_id"]
                and isinstance(blocks, list)
                and blocks
                and all(isinstance(b, str) and b.strip() for b in blocks)
            )
            if not valid:
                raise QueriesFileError(
                    f"family {family}/{db}: query_id and non-empty string blocks required"
                )
    return data


def build_queries(data: dict[str, Any]) -> list[V2Query]:
    queries: list[V2Query] = []
    for family, fam_def in data["executed_families"].items():
        for db in DATABASES:
            q = fam_def["queries"][db]
            queries.append(
                V2Query(
                    family=family,
                    database=db,
                    query_id=q["query_id"],
                    blocks=tuple(b.strip() for b in q["blocks"]),
                )
            )
    return queries


def estimate_api_calls(q: V2Query) -> int:
    """Offline per-query estimate: 1 esearch + efetch batches (PubMed),
    result pages (arXiv/S2), or 10-result GS pages."""
    if q.database == "pubmed":
        return 1 + math.ceil(PUBMED_MAX / PUBMED_BATCH)
    if q.database == "arxiv":
        return math.ceil(ARXIV_MAX / ARXIV_PAGE)
    if q.database == "semantic_scholar":
        return math.ceil(S2_PER_QUERY_LIMIT / S2_PAGE)
    return math.ceil(GS_MAX_RESULTS / GS_RESULTS_PER_PAGE)


def dry_run(
    path: str | Path | None = None,
) -> tuple[list[tuple[str, str, int]], dict[str, tuple[str, str]]]:
    """Offline plan: per-query estimated API calls + rendered EBSCO strings."""
    data = load_queries(path)
    plan = [
        (q.query_id, q.database, estimate_api_calls(q)) for q in build_queries(data)
    ]
    ebsco = {
        family: (entry["query_id"], entry["query"])
        for family, entry in render_ebsco_queries(data).items()
    }
    return plan, ebsco


def run_all(
    queries_path: str | Path | None = None,
    output_dir: str | Path | None = None,
) -> dict[str, dict[str, Any]]:
    """Execute every query per database; write one immutable CSV per query.

    Existing CSVs are never overwritten (skipped-existing provenance row).
    Failures degrade to a status string — one bad lane never stops the run.
    """
    data = load_queries(queries_path)
    out_dir = Path(output_dir) if output_dir else RAW_V2_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    date_start = str(data.get("date_range", {}).get("start", "2015-01-01"))
    search_date = datetime.now().strftime("%Y-%m-%d")
    summary: dict[str, dict[str, Any]] = {}

    for q in build_queries(data):
        csv_path = out_dir / f"{q.query_id}.csv"
        if csv_path.exists():
            _log(out_dir, q, search_date, row_count(csv_path), "skipped-existing", summary)
            continue
        fetch = FETCHERS[q.database]
        try:
            if q.database == "google_scholar":
                rows, status = fetch(q.executed)
            else:
                rows, status = fetch(q.executed, date_start=date_start)
        except Exception as exc:
            rows, status = [], f"error: {exc}"
        write_raw_csv(csv_path, rows)
        _log(out_dir, q, search_date, len(rows), status, summary)

    _run_ebsco_lane(data, out_dir, search_date, summary)
    return summary


def _log(
    out_dir: Path,
    q: V2Query,
    search_date: str,
    count: int,
    status: str,
    summary: dict[str, dict[str, Any]],
) -> None:
    append_provenance(
        out_dir,
        query_id=q.query_id,
        database=q.database,
        family=q.family,
        search_date=search_date,
        record_count=count,
        status=status,
    )
    summary[q.query_id] = {"records": count, "status": status}


def _run_ebsco_lane(
    data: dict[str, Any],
    out_dir: Path,
    search_date: str,
    summary: dict[str, dict[str, Any]],
) -> None:
    rendered, statuses = fetch_ebsco(data, attempt_live=True)
    for family in sorted(rendered):
        entry = rendered[family]
        print(f"EBSCO render {entry['query_id']}: {entry['query'][:100]}")
        status = statuses[entry["query_id"]]
        append_provenance(
            out_dir,
            query_id=entry["query_id"],
            database="ebsco",
            family=family,
            search_date=search_date,
            record_count=0,
            status=status,
        )
        summary[entry["query_id"]] = {"records": 0, "status": status}
