#!/usr/bin/env python3
"""Add `included_in_synthesis` column to S2_included_studies.csv.

Cross-walks the DOI of each row against the 52 PDFs retained in
`data/final_included_papers/`. The PDF filename encodes the DOI by
replacing the first '/' with '_'. A row is marked `yes` if its DOI
matches one of the 52 PDFs, `no` otherwise.

This is a non-fabricating reconciliation: it uses only artifacts that
already exist in the repository (the S2 CSV and the PDF directory).
"""
from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
S2 = REPO / "artifacts/data/evidence/supplementary/S2_included_studies.csv"
PDF_DIR = REPO / "data/final_included_papers"
OUT = S2  # in-place


def doi_from_pdf_name(stem: str) -> str:
    # PDF filenames replaced ONLY the first '/' with '_'.
    return stem.replace("_", "/", 1)


def main() -> None:
    pdf_dois = {doi_from_pdf_name(p.stem).lower() for p in PDF_DIR.glob("*.pdf")}
    assert len(pdf_dois) == 52, f"Expected 52 PDFs, found {len(pdf_dois)}"

    with S2.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header, data = rows[0], rows[1:]

    if "included_in_synthesis" in header:
        print("Column already present; nothing to do.")
        return

    doi_idx = header.index("doi")
    new_header = header + ["included_in_synthesis"]
    new_rows = [new_header]
    matched = 0
    for r in data:
        doi = (r[doi_idx] or "").strip().lower()
        flag = "yes" if doi and doi in pdf_dois else "no"
        if flag == "yes":
            matched += 1
        new_rows.append(r + [flag])

    with S2.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(new_rows)

    print(f"S2 rows: {len(data)}; matched to PDF corpus: {matched}; "
          f"unmatched: {len(data) - matched}")


if __name__ == "__main__":
    main()
