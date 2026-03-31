# Getting Started

## Prerequisites

- Python ≥ 3.10
- Git

## Setup

```bash
git clone https://github.com/game-guild/docdo-paper-research.git
cd docdo-paper-research
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -e ".[dev]"
```

Check it works:

```bash
docdo --help
pytest operations/tests/ -v
```

## Day-to-day commands

```bash
# Fetch papers from PubMed
docdo fetch-pubmed --max-results 500

# Deduplicate search results
docdo deduplicate -i artifacts/data/evidence/raw/search_results.csv

# Screen papers (small batch, interactive)
docdo screen -i deduplicated.csv -o screened.csv --limit 20

# Screen papers (large batch via OpenAI Batch API)
docdo screen-batch -i deduplicated.csv --output-dir artifacts/data/evidence/processed/

# Download PDFs for included papers
docdo fetch-pdfs -i included.csv

# Compute statistics
docdo stats -i included.csv --latex-dir tables/

# Run tests
pytest operations/tests/ -v --cov=docdo
```

## Where things live

- **Search exports** → `artifacts/data/evidence/`
- **PDFs** → `artifacts/data/evidence/pdfs/`
- **BibTeX** → `scholar/bib/`
- **Python code** → `operations/src/docdo/`
- **Tests** → `operations/tests/`
- **LaTeX paper** → separate repo: [docdo-paper](https://github.com/game-guild/docdo-paper)
