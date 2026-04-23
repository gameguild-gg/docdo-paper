# S1_search_results_REAL.csv — provenance note

**Status:** This CSV is a **200-row retained sample**, not the full
~2,985-record raw search export described in `S_PRISMA_funnel.md`.
The full raw fetch was produced by
`operations/src/_archive/scripts/fetch_all_real_data.py` and was not
committed to the repository.

## Schema

`id, database, search_date, title, authors, year, journal_conference, doi, abstract_snippet`

- `database` carries real source identifiers (`PubMed`, `arXiv`,
  `Semantic Scholar`).
- `search_date` is uniformly `2026-01-20` because it was rewritten at
  retention time (it is not the original query date for each record).
- `id` values are sequential surrogate identifiers assigned at
  retention time, not stable identifiers from the source databases.

## Authoritative provenance

The full 2,821-row deduplicated search export, the 638-row
Elasticsearch-filtered set, the 161-row S2 LLM-screening output, the
63-row full-text manifest, the 52-row S3 included list, and the
11-row S3 excluded list (with reasons) are in `pipeline_outputs/` in this
directory. See `S_PRISMA_funnel.md` for the stage-by-stage map and
`operations/src/_archive/scripts/` for the scripts that produced each
stage. For the included-studies table see
`S2_final_included_studies.csv`.
