# Task B8: Pool Widening Funnel

## Harvest Results
- **Total Harvested (B8 lanes):** 7,436
- **Deduped New (vs Corpus):** 6,764
- **DSL Passers (Title-only):** 6
- **S2 Screened-in (Unanimous INCLUDE):** 26
- **Acquired PDFs:** 13

## Lane Breakdown (Acquisition)
- **OpenAlex Locations:** 6
- **PMC (PoW):** 7
- **arXiv/Others:** 0

## Final Yield
- **New Unique PDFs in expansion/:** 13
- **Verification:** `python3 -c "import os, hashlib; from pathlib import Path; p = Path('/Users/tolstenko/projects/docdo-paper-research/artifacts/data/evidence/pdfs/expansion'); hashes = set(); [hashes.add(hashlib.sha256(f.read_bytes()).hexdigest()) for f in p.glob('*.pdf') if f.stat().st_size > 10000]; print(len(hashes))"` -> 13
