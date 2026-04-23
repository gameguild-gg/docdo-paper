# PRISMA Screening Funnel — Provenance

**Last updated:** 2026-04-23
**Status:** Verified against the screening pipeline's primary outputs
in [`pipeline_outputs/`](pipeline_outputs/) in this directory. PDFs of the 52
included studies are in `data/final_included_papers/`.

## 1. Funnel (verified)

| Stage | N | Authoritative artifact in `pipeline_outputs/` |
|------:|---|----------------------------------------|
| Records identified across PubMed (997) + arXiv (904) + Semantic Scholar (1,084) | **2,985** raw | `S1_evidence_report.md` (per-source breakdown) |
| Deduplication by DOI + normalised title | **2,821** | `S1_search_results_deduplicated.csv` (2,821 rows; produced by `operations/src/_archive/scripts/deduplicate_s1.py`) |
| Boolean Elasticsearch filter (English analyzer; 3D / volumetric / segmentation / CT terms) | **638** | `S2_elasticsearch_filtered.csv` (638 rows) |
| S2 LLM screening (GPT-4o-mini, 3-vote unanimous-INCLUDE rule) | **161** included | `all_papers_after_s2_with_status.csv` (161 rows; column `included_in_review`) |
| Full-text retrieval (PDF acquisition for the 161; subset where PDF could be obtained) | **63** | `final_included_for_review.csv` (63 rows); 103 unobtainable in `excluded_no_fulltext.csv` |
| S3 full-text screening (GPT-5.2 batch) | **52 included / 11 excluded** | `s3_extracted_data_full.csv` (52 rows), `s3_summary_table.csv` (52 rows), `s3_excluded_papers.csv` (11 rows with explicit exclusion reasons) |

Authoritative included-studies table:
[`S2_final_included_studies.csv`](S2_final_included_studies.csv)
(52 rows; rebuilt from the on-disk PDFs by
`operations/src/_archive/scripts/build_s2_final_included.py`).

## 2. Quality Assessment (verified)

GPT-5.2 batch applied a 15-question rubric (5 questions × 3 dimensions,
each scored 0–2; total 0–30; rubric in
`operations/src/_archive/scripts/step2_quality_assessment_batch.py`).
Per-study scores in `pipeline_outputs/qa_summary.csv` and
full LLM responses in `pipeline_outputs/qa_parsed_results.json`.

Aggregate (n = 52):

| Statistic | Value |
|-----------|-------|
| Mean total score | 21.0 / 30 |
| Range | 14 – 28 |
| High quality (total ≥ 24) | **10 (19.2 %)** |
| Medium quality (15 – 23) | **41 (78.8 %)** |
| Low quality (< 15) | **1 (1.9 %)** |

These are the numbers cited in §Quality Assessment Results of the
paper.

## 3. Reproducibility

Re-running the pipeline from scratch will not reproduce the exact
counts because the public APIs (PubMed, arXiv, Semantic Scholar)
return different result sets over time and the LLMs are not
deterministic. To audit the *current* paper's claims, use the
artifacts under `pipeline_outputs/` directly.

Pipeline scripts (in `operations/src/_archive/scripts/`):
1. `fetch_all_real_data.py` — query PubMed / arXiv / Semantic Scholar.
2. `deduplicate_s1.py` — DOI + normalised title dedup.
3. `elasticsearch/filter_with_elasticsearch.py` — boolean filter.
4. S2 GPT-4o-mini 3-vote screening pipeline.
5. `step2_quality_assessment_batch.py` — S3 full-text + QA via GPT-5.2 batch.
6. `step1_copy_included_papers.py` — copy 52 included PDFs.
7. `build_s2_final_included.py` — rebuild `S2_final_included_studies.csv` from the PDF directory.
