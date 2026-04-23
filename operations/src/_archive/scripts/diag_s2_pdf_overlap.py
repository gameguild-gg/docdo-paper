"""Quick disjoint-set diagnostic for S2 DOIs vs PDF corpus DOIs."""
from pathlib import Path
import csv

REPO = Path(__file__).resolve().parents[4]
S2 = REPO / "artifacts/data/evidence/supplementary/S2_included_studies.csv"
PDF_DIR = REPO / "data/final_included_papers"

with S2.open(newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))
header, data = rows[0], rows[1:]
doi_idx = header.index("doi")
s2_dois = {(r[doi_idx] or "").strip().lower() for r in data}
s2_dois.discard("")

pdf_dois = {p.stem.replace("_", "/", 1).lower() for p in PDF_DIR.glob("*.pdf")}

print(f"S2 unique DOIs: {len(s2_dois)}")
print(f"PDF unique DOIs: {len(pdf_dois)}")
print(f"Intersection: {len(s2_dois & pdf_dois)}")
print("--- intersection items:")
for d in sorted(s2_dois & pdf_dois):
    print(" ", d)
print("--- 5 sample PDF DOIs not in S2:")
for d in sorted(pdf_dois - s2_dois)[:5]:
    print(" ", d)
print("--- 5 sample S2 DOIs not in PDFs:")
for d in sorted(s2_dois - pdf_dois)[:5]:
    print(" ", d)
