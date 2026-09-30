<!-- v1-history -->
(v1 content preserved as history (v2 numbers supersede))

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

<!-- /v1-history -->

---

## v2.2 Section (2026-10-01) — final funnel (second shadow-library wave)

| Stage | N | Artifact |
|-------|---|----------|
| Raw API records (PubMed 7,045 + arXiv 7,164 + Google Scholar 338) | 14,547 | `raw/v2/_combined.csv` |
| OpenAlex identification-lane delta | 264,269 | `interim/S1v2_openalex_delta.csv` |
| Deduplicated records entering pre-filter | **273,115** | dedup CSV + delta |
| Pre-filter pass (1,101 API + 6,269 OpenAlex lane) | **7,370** | `S2v2_elasticsearch_filtered.csv` + `S2v2_openalex_filtered.csv` |
| S2 INCLUDE (unique studies; 288 API + 751 OpenAlex, 4 dual-lane counted once) | **1,035** | `all_papers_after_s2v2_with_status.csv` + lane |
| Not retrieved (501 paywalled hand-off + 180 no accessible route) | 681 | `S3v2_paywalled_librarian_request.csv` |
| Full texts obtained (34.2%) — 186 original + 82 OA re-fetch + 96 user-sanctioned shadow-library (two waves) | **354** | `S3v2_acquisition_log.csv` |
| Full-text EXCLUDE (method 90 incl. 4 unusable PDFs; benchmark 7; framework 2; review 1) | 100 | `s3v2_excluded_papers.csv` |
| **Included (242 method + 9 framework + 3 benchmark)** | **254** | `s3v2_extracted_data_full.csv`, `S2v2_final_included_studies.csv` |
| Method studies with per-organ Dice | 233 | `s3v2_summary_table.csv` |

Screening models: S3 batch 1 (186 papers) mini-class `deepseek-v4-flash-vision-low`; S3 batch 2 (149 papers) `zai/glm-5.3-flash`; S3 batch 3 (21 papers, second shadow wave) `zai/glm-5.3-flash`. v1↔v2 reconciliation (52 v1 studies): **22 re-included / 1 s2-excluded / 1 s3-excluded / 23 fulltext-missed / 5 not-identified** (`v1_v2_study_reconciliation.csv`).
