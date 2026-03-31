# S9: Analysis Scripts - Verification and Reproducibility

This directory contains Python scripts for verifying the methodology and reproducing the analyses in the survey.

## Contents

1. `verify_screening.py` - Verify AI screening consensus calculations
2. `compute_statistics.py` - Compute descriptive statistics from extracted data
3. `reproduce_figures.py` - Reproduce figures from the paper
4. `validate_citations.py` - Validate citation counts and cross-references
5. `requirements.txt` - Python dependencies

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run verification
python verify_screening.py --input ../S5_screening_decisions.csv
python compute_statistics.py --input ../S2_included_studies.csv
python validate_citations.py --input ../S8_table_sources.csv
```

## Requirements

- Python 3.8+
- pandas >= 1.5.0
- numpy >= 1.21.0
- scipy >= 1.9.0
- matplotlib >= 3.5.0

## Contact

For questions about the analysis scripts, contact [corresponding author].
