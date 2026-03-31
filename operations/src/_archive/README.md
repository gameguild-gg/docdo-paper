# Archived Scripts

These scripts have been refactored into the `docdo` Python package
located at `operations/src/docdo/`.

## Migration Map

| Old Script | New Module | CLI Command |
|---|---|---|
| `fetch_pubmed_simple.py` | `docdo.fetch` | `docdo fetch-pubmed` |
| `fetch_pdfs.py` | `docdo.fetch` | `docdo fetch-pdfs` |
| `fetch_pdfs_for_included.py` | `docdo.fetch` | `docdo fetch-pdfs` |
| `fetch_oa_papers.py` | `docdo.fetch` | `docdo fetch-oa` |
| `deduplicate_s1.py` | `docdo.dedup` | `docdo deduplicate` |
| `screen_with_gpt.py` | `docdo.screening` | `docdo screen` |
| `screen_with_gpt_batch.py` | `docdo.screening` | `docdo screen-batch` |
| `submit_s3_batch.py` | `docdo.screening` | `docdo screen-batch` |
| `check_batch_status.py` | `docdo.openai_utils` | `docdo check-batch` |
| `download_s3_batch.py` | `docdo.openai_utils` | `docdo download-batch` |
| `compile_final_results.py` | `docdo.cli` (compile) | `docdo compile` |
| `verify_dois.py` | `docdo.verify` | `docdo verify-dois` |
| `verify_s2_in_s1.py` | `docdo.verify` | `docdo verify-traceability` |
| `compute_statistics.py` | `docdo.analysis` | `docdo stats` |
| `s3_fulltext_screening.py` | `docdo.screening` | (integrated) |
| `citation_verification.py` | `docdo.verify` | (integrated) |

## Utility scripts (preserved as-is)

Other scripts in this archive were one-off utilities for batch management,
comparison, or ad-hoc analysis. Their core patterns have been absorbed into
the library modules above.
