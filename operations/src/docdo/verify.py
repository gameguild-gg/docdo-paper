"""DOI verification and S2 → S1 traceability checking."""

from __future__ import annotations

import csv
import random
import time
from pathlib import Path
from typing import Any

from . import config
from .dedup import normalize_doi, normalize_title
from .io import read_csv


# ---------------------------------------------------------------------------
# DOI resolution
# ---------------------------------------------------------------------------

def verify_doi(doi: str, *, retries: int = 3) -> tuple[bool | None, str]:
    """Check whether a DOI / arXiv ID resolves.

    Returns ``(resolved, info_string)``.
    ``None`` means the identifier type is unsupported.
    """
    import requests  # lazy to keep startup fast

    if not doi or doi.startswith("S2:"):
        return None, "No standard DOI"

    if doi.startswith("http://arxiv.org/"):
        url = doi
    elif doi.startswith("arXiv:"):
        url = f"https://arxiv.org/abs/{doi.replace('arXiv:', '')}"
    else:
        url = f"https://doi.org/{doi}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    for attempt in range(retries):
        try:
            resp = requests.get(
                url, timeout=15, allow_redirects=True, headers=headers, stream=True
            )
            resp.close()
            if resp.status_code in (200, 301, 302):
                return True, resp.url
            if resp.status_code in (403, 418, 429):
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                return True, f"Exists (HTTP {resp.status_code} – bot protection)"
            return False, f"HTTP {resp.status_code}"
        except requests.exceptions.Timeout:
            if attempt < retries - 1:
                continue
            return False, "Timeout"
        except Exception as exc:
            if attempt < retries - 1:
                continue
            return False, str(exc)

    return False, "Max retries exceeded"


def verify_doi_sample(
    input_csv: Path | None = None,
    *,
    per_db: int = 5,
) -> dict[str, int]:
    """Verify a random sample of DOIs from each database.

    Returns counts ``{verified, failed, skipped}``.
    """
    input_csv = input_csv or config.S1_DEDUP
    records = read_csv(input_csv)

    results: dict[str, int] = {"verified": 0, "failed": 0, "skipped": 0}

    databases = {r.get("database", "Unknown") for r in records}
    for db in sorted(databases):
        db_rows = [r for r in records if r.get("database") == db and r.get("doi")]
        sample = random.sample(db_rows, min(per_db, len(db_rows)))
        for r in sample:
            ok, info = verify_doi(r["doi"])
            if ok is True:
                results["verified"] += 1
            elif ok is False:
                results["failed"] += 1
            else:
                results["skipped"] += 1

    return results


# ---------------------------------------------------------------------------
# S2 → S1 traceability
# ---------------------------------------------------------------------------

def verify_traceability(
    s1_path: Path | None = None,
    s2_path: Path | None = None,
    *,
    report_path: Path | None = None,
) -> tuple[int, int, str]:
    """Verify all S2 studies can be traced to S1 search results.

    Returns ``(found_count, not_found_count, traceability_level)``.
    """
    s1_path = s1_path or config.S1_RAW
    s2_path = s2_path or config.SUPPLEMENTARY_DIR / "S2_final_included_studies.csv"

    # Build S1 indexes
    s1_records = read_csv(s1_path)
    s1_titles = {normalize_title(r.get("title", "")) for r in s1_records}
    s1_dois = {normalize_doi(r.get("doi", "")) for r in s1_records}
    s1_titles.discard("")
    s1_dois.discard("")

    # Load S2
    s2 = read_csv(s2_path)

    found_doi: list[dict] = []
    found_title: list[dict] = []
    not_found: list[dict] = []

    for study in s2:
        doi = normalize_doi(study.get("doi", ""))
        title = normalize_title(study.get("title", ""))
        if doi and doi in s1_dois:
            found_doi.append(study)
        elif title and title in s1_titles:
            found_title.append(study)
        else:
            not_found.append(study)

    total = len(s2)
    found_total = len(found_doi) + len(found_title)

    if not not_found:
        level = "FULL"
    elif len(not_found) < total * 0.2:
        level = "HIGH"
    else:
        level = "PARTIAL"

    # Write report
    if report_path is None:
        report_path = config.SUPPLEMENTARY_DIR / "S1_S2_traceability_report.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("S2 → S1 TRACEABILITY VERIFICATION REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"S1 file: {s1_path.name} ({len(s1_records)} papers)\n")
        f.write(f"S2 file: {s2_path.name} ({total} studies)\n\n")
        f.write("RESULTS:\n")
        f.write(f"  Found by DOI:   {len(found_doi)}\n")
        f.write(f"  Found by title: {len(found_title)}\n")
        f.write(f"  Total found:    {found_total} ({100 * found_total / total:.1f}%)\n")
        f.write(f"  Not found:      {len(not_found)} ({100 * len(not_found) / total:.1f}%)\n\n")
        f.write(f"Traceability: {level}\n\n")

        if not_found:
            f.write("STUDIES NOT IN S1 (manually added):\n")
            f.write("-" * 50 + "\n")
            for s in not_found:
                f.write(f"{s.get('study_id', '')}: {s.get('title', '')}\n")
                f.write(f"  DOI: {s.get('doi', '')}\n")
                f.write(f"  {s.get('first_author', '')} ({s.get('year', '')})\n\n")

    print(f"  Traceability: {found_total}/{total} ({level})")
    return found_total, len(not_found), level
