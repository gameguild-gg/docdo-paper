# S9: Analysis Scripts — Verification and Reproducibility

The Python analysis scripts for this survey are maintained in the project source tree.

**Location:** `operations/src/_archive/analysis/`

**Entry point for full documentation:** `operations/src/_archive/analysis/README.md`

## Scripts

| Script | Purpose |
|---|---|
| `verify_screening.py` | Verify AI screening consensus calculations |
| `compute_statistics.py` | Compute descriptive statistics from extracted data |
| `reproduce_figures.py` | Reproduce figures from the paper |
| `validate_citations.py` | Validate citation counts and cross-references |

## Quick Start

```bash
cd operations/src/_archive/analysis/
pip install -r requirements.txt
python verify_screening.py --input ../../../artifacts/data/evidence/supplementary/S5_screening_decisions.csv
python compute_statistics.py --input ../../../artifacts/data/evidence/supplementary/S2_final_included_studies.csv
python validate_citations.py --input ../../../artifacts/data/evidence/supplementary/S8_table_sources.csv
```

## Requirements

- Python 3.8+
- pandas ≥ 1.5.0, numpy ≥ 1.21.0, scipy ≥ 1.9.0, matplotlib ≥ 3.5.0
