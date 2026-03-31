# CLI Reference

The `docdo` CLI wraps the review pipeline. Install with `pip install -e ".[dev]"`.

## Commands

| Command | What it does |
|---------|-------------|
| `fetch-pubmed` | Search PubMed and save results as CSV |
| `fetch-pdfs` | Download PDFs for included papers (arXiv + Unpaywall) |
| `fetch-oa` | Download open-access PDFs from a paywalled list |
| `deduplicate` | Remove duplicates by DOI and fuzzy title matching |
| `screen` | Screen papers one-by-one with GPT (small batches) |
| `screen-batch` | Submit screening to OpenAI Batch API (large batches) |
| `check-batch` | Check status of a batch job |
| `download-batch` | Download completed batch results |
| `compile` | 3-model consensus vote across strict/nano/gpt52 runs |
| `verify-dois` | Spot-check that DOIs resolve correctly |
| `verify-traceability` | Confirm S2 included papers trace back to S1 searches |
| `stats` | Compute descriptive statistics, optionally export LaTeX tables |

## Environment Variables

- `OPENAI_API_KEY` — required for screening commands
- `OPENAI_MODEL` — override default model (optional)

## Source

Implemented in [operations/src/docdo/cli.py](../src/docdo/cli.py) using [Click](https://click.palletsprojects.com/).
