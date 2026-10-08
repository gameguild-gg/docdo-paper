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

## v2.3 — wave-8 shadow/expansion screen merge (2026-10-08)

- Source: 857 previously-unscreened shadow/expansion PDFs, S3-screened + QA'd on lane
  `omo/vision` (OmniRoute), 0 terminal failures (network-retry hardened passes).
- Raw audit file: `wave8_screening_raw.json` (857 records, verbatim runner output).
- Results: 209 INCLUDE (all with QA) / 648 EXCLUDE. After dedup vs corpus v2.2
  (30 preprint-vs-published / arXiv-version / supplement-DOI manifestations dropped,
  15 duplicate excludes dropped): **+179 net-new studies** — corpus 254 → **433**
  (method 405, framework 13, benchmark 15).
- Row deltas: s3v2_extracted_data_full 354→1,166 (both decisions, historical semantics);
  s3v2_excluded_papers 100→733; qa_v2_parsed_results 348→557; qa_v2_summary 348→557;
  s3v2_summary_table 242→405 (method-INCLUDE only); S3v2_acquisition_log 843→1,700
  (route `wave8-shadow-expansion`); reconciliation 52→83 (30 dup-manifestation rows +
  1 human-adjudication flag `10.1016_j.eclinm.2024.102772`: C1 INCLUDE 0.6 vs wave-8 EXCLUDE, wave-8 retained).
- QA rubric mapping: wave-8 D1-D5/M1-M5/C1-C5 mapped to Q1-Q15; total_score recovered
  from nested quality_assessment where models ignored the top-level instruction;
  band cutoffs calibrated on the 240 legacy scores (>=24 High, <=14 Low reproduce v2.2's 60/26).
- Synthesis regenerated with one uniform architecture classifier (v2.2's ad-hoc pass
  not row-reproducible; noted in-file).
