# Operations

The `docdo` Python library and its tests.

```
src/docdo/          # pip-installable library
├── cli.py          # Click CLI (13 subcommands)
├── config.py       # Paths and env vars
├── io.py           # CSV/BibTeX/JSONL loading
├── fetch.py        # PubMed, arXiv, Unpaywall, OA fetching
├── dedup.py        # DOI + fuzzy title deduplication
├── screening.py    # GPT screening prompts, voting
├── openai_utils.py # OpenAI Batch API helpers
├── verify.py       # DOI verification, S2→S1 traceability
└── analysis.py     # Descriptive statistics, LaTeX export
tests/              # 150 pytest tests (~55% coverage)
src/_archive/       # original 57 scripts (kept for reference)
```

## Install

```bash
pip install -e ".[dev]"
```

## CLI

```bash
docdo fetch-pubmed --query "3D organ segmentation" --max-results 200
docdo fetch-pdfs -i included.csv --pdf-dir pdfs/
docdo fetch-oa paywalled.csv --pdf-dir pdfs/
docdo deduplicate -i search_results.csv -o deduplicated.csv
docdo screen -i papers.csv -o screened.csv --limit 50
docdo screen-batch -i papers.csv --output-dir batches/
docdo check-batch <batch_id>
docdo download-batch <batch_id>
docdo compile --strict-dir batches/strict --nano-dir batches/nano
docdo verify-dois -i included.csv --per-db 5
docdo verify-traceability --s1 search.csv --s2 included.csv
docdo stats -i included.csv --latex-dir tables/
```

## Tests

```bash
pytest operations/tests/ -v --cov=docdo
```
