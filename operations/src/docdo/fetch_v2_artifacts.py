"""Immutable raw-CSV artifact store + derived combined CSV for the v2 fetcher.

Immutability carve-out (pinned): per-DB+query CSVs (<QUERY_ID>.csv) are the
immutable fetched artifacts; _combined.csv is DERIVED and regenerable on
demand — it is the sole input to the dedup stage (``docdo deduplicate``
takes a single csv path). Underscore-prefixed files (_combined.csv,
_provenance.csv) are never concat inputs, so the glob cannot self-include.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

COMBINED_FILENAME = "_combined.csv"
PROVENANCE_FILENAME = "_provenance.csv"

CSV_FIELDS = [
    "id", "database", "search_date", "title", "authors",
    "year", "journal_conference", "doi", "abstract_snippet",
]
PROVENANCE_FIELDS = [
    "query_id", "database", "family", "search_date", "record_count", "status",
]


def write_raw_csv(path: Path | str, rows: list[dict[str, Any]]) -> Path:
    """Write one raw CSV with the exact v1 schema; refuses to overwrite."""
    path = Path(path)
    if path.exists():
        raise FileExistsError(f"raw CSV already exists (immutable): {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for i, row in enumerate(rows, 1):
            out = {f: str(row.get(f, "") or "") for f in CSV_FIELDS}
            out["id"] = f"R{i:04d}"  # per-file ids; dedup renumbers after concat
            writer.writerow(out)
    return path


def append_provenance(
    raw_dir: Path | str,
    *,
    query_id: str,
    database: str,
    family: str,
    search_date: str,
    record_count: int,
    status: str,
) -> None:
    path = Path(raw_dir) / PROVENANCE_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=PROVENANCE_FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(
            {
                "query_id": query_id,
                "database": database,
                "family": family,
                "search_date": search_date,
                "record_count": record_count,
                "status": status,
            }
        )


def read_provenance(raw_dir: Path | str) -> list[dict[str, str]]:
    path = Path(raw_dir) / PROVENANCE_FILENAME
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def row_count(path: Path | str) -> int:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return sum(1 for _ in csv.DictReader(fh))


_DB_TOKEN_LABELS = {"PUB": "PubMed", "ARX": "arXiv", "S2": "Semantic Scholar",
                    "GS": "Google Scholar"}


def _db_label_for(stem: str) -> str:
    parts = stem.split("-")
    return _DB_TOKEN_LABELS.get(parts[1], parts[1]) if len(parts) > 1 else stem


def concat_raw(raw_dir: Path | str) -> Path:
    """Deterministically concatenate per-DB+query CSVs into _combined.csv.

    Stable sort by (database label, query_id), in-file row order preserved.
    """
    raw_dir = Path(raw_dir)
    combined = raw_dir / COMBINED_FILENAME
    inputs = sorted(
        (p for p in raw_dir.glob("*.csv") if not p.name.startswith("_")),
        key=lambda p: (_db_label_for(p.stem), p.stem),
    )
    all_rows: list[dict[str, str]] = []
    for path in inputs:
        with path.open(newline="", encoding="utf-8") as fh:
            all_rows.extend(csv.DictReader(fh))
    combined.parent.mkdir(parents=True, exist_ok=True)
    with combined.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)
    return combined
