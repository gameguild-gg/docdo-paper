"""Roll back the misleading `included_in_synthesis` column on S2.

The legacy S2_included_studies.csv contains 127 rows from an earlier
pipeline pass whose DOIs do not overlap with the 52 PDFs actually
synthesized in the paper (only 1/52 DOIs match). Marking 126 of 127
rows as `included_in_synthesis=no` would falsely imply the 52 are a
subset of these 127. They are disjoint corpora.

This script removes the column.
"""
from __future__ import annotations
import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
S2 = REPO / "artifacts/data/evidence/supplementary/S2_included_studies.csv"


def main() -> None:
    with S2.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header = rows[0]
    if "included_in_synthesis" not in header:
        print("Column not present; nothing to do.")
        return
    idx = header.index("included_in_synthesis")
    new_rows = [r[:idx] + r[idx + 1:] for r in rows]
    with S2.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(new_rows)
    print(f"Removed column 'included_in_synthesis' (was at index {idx}).")


if __name__ == "__main__":
    main()
