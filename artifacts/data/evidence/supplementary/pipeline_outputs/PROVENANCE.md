# `pipeline_outputs/` — authoritative pipeline outputs

These are the authoritative pipeline outputs for this paper's PRISMA funnel
(S1 search → S2 ES filter → S2 LLM screening → PDF retrieval → S3 full-text →
quality assessment) and are referenced from `main.tex` and
`../S_PRISMA_funnel.md`. Do not edit in place; regenerate from the pipeline
scripts in `operations/src/_archive/scripts/` if updates are needed.

> **Folder rename (2026-04-23):** previously `recovered/`. The contents are
> the canonical pipeline outputs and are not "recovered" in any
> recovery-from-loss sense; the folder was renamed for clarity. Per-file
> date stamps (`_20260122_215847`, `_20260122_233013`, `_20260123_075645`)
> were stripped at the same time; the original timestamps remain visible
> in the git history.

| File | Rows / Notes |
|---|---|
| `S1_evidence_report.md` | per-source breakdown |
| `S1_search_results_deduplicated.csv` | 2,821 |
| `S2_elasticsearch_filtered.csv` | 638 |
| `all_papers_after_s2_with_status.csv` | 161 |
| `final_included_for_review.csv` | 63 (PDFs retrieved) |
| `excluded_no_fulltext.csv` | 103 (no PDF) |
| `s3_extracted_data_full.csv` | 52 |
| `s3_summary_table.csv` | 52 |
| `s3_excluded_papers.csv` | 11 |
| `qa_summary.csv` | 52 (per-study QA) |
| `qa_parsed_results.json` | 52 (full LLM rubric responses) |
