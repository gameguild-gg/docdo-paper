"""Deduplication of S1 search results across databases."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from . import config
from .io import read_csv, write_csv


def normalize_title(title: str) -> str:
    """Lowercase, collapse whitespace, strip punctuation."""
    if not title:
        return ""
    t = title.lower().strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^\w\s]", "", t)
    return t


def normalize_doi(doi: str) -> str:
    """Strip common prefixes and lowercase."""
    if not doi:
        return ""
    d = doi.lower().strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:", "doi.org/"):
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d


def completeness_score(row: dict[str, Any]) -> int:
    """Score a record's metadata completeness (higher = more complete)."""
    score = 0
    abstract_key = "abstract_snippet" if "abstract_snippet" in row else "abstract"
    if row.get("doi"):
        score += 3
    if row.get(abstract_key) and len(str(row[abstract_key])) > 100:
        score += 2
    if row.get("authors"):
        score += 1
    if row.get("year"):
        score += 1
    if row.get("journal_conference"):
        score += 1
    return score


def deduplicate(
    input_path: Path | None = None,
    output_path: Path | None = None,
) -> tuple[int, int]:
    """Run DOI + title deduplication on S1 search results.

    Parameters
    ----------
    input_path : Path | None
        CSV of raw search results. Defaults to ``config.S1_RAW``.
    output_path : Path | None
        Where to write deduplicated CSV. Defaults to ``config.S1_DEDUP``.

    Returns
    -------
    (kept, removed) : tuple[int, int]
    """
    input_path = input_path or config.S1_RAW
    output_path = output_path or config.S1_DEDUP
    output_path.parent.mkdir(parents=True, exist_ok=True)

    records = read_csv(input_path)
    if not records:
        print("  No records to deduplicate.")
        return 0, 0

    # Build indexes
    doi_idx: dict[str, list[int]] = defaultdict(list)
    title_idx: dict[str, list[int]] = defaultdict(list)
    for i, row in enumerate(records):
        d = normalize_doi(row.get("doi", ""))
        t = normalize_title(row.get("title", ""))
        if d:
            doi_idx[d].append(i)
        if t:
            title_idx[t].append(i)

    to_remove: set[int] = set()

    # DOI dups
    for indices in doi_idx.values():
        if len(indices) > 1:
            best = max(indices, key=lambda i: completeness_score(records[i]))
            to_remove.update(i for i in indices if i != best)

    # Title dups (skip already-removed)
    for indices in title_idx.values():
        remaining = [i for i in indices if i not in to_remove]
        if len(remaining) > 1:
            best = max(remaining, key=lambda i: completeness_score(records[i]))
            to_remove.update(i for i in remaining if i != best)

    unique = [r for i, r in enumerate(records) if i not in to_remove]

    # Renumber
    for i, row in enumerate(unique, 1):
        row["id"] = f"R{i:04d}"

    write_csv(output_path, unique)

    kept = len(unique)
    removed = len(to_remove)
    print(f"  Dedup: {len(records)} → {kept} ({removed} duplicates removed)")
    return kept, removed
