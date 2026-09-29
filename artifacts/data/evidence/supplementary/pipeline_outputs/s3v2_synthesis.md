# S3v2 Synthesis — Architecture Strata, Supervision, Multi-Axis Taxonomy, Per-Organ Dice

Generated programmatically from `s3v2_extracted_data_full.csv` (186 rows = 186 obtained distinct PDFs),
`s3v2_summary_table.csv` (116 method-INCLUDE rows), `qa_v2_summary.csv`, and `v1_v2_study_reconciliation.csv`.
No statistic in this file is hand-typed; re-derive with the counts below audited against the CSVs.

## Funnel recap (full-text stage)

- Obtained distinct papers: **186**
- Full-text INCLUDE: **121** (method 116, framework 5)
- Full-text EXCLUDE: **65** (method 55, benchmark 7, framework 2, review 1)

## Architecture-family strata (method INCLUDE, n=116)

Classification regex over `architecture` + `architecture_details`; extends the v1 CNN/Transformer/Hybrid
strata (content.tex 742-780) with Foundation and Framework strata. "Foundation" = SAM/foundation-model
derived architectures; the Framework stratum is tracked separately below.

- **CNN**: 106/116
- **Hybrid**: 8/116
- **Transformer**: 0/116
- **Foundation**: 2/116
- **Neuro-symbolic**: 1/116 (Graph-ResNet classification head on nnU-Net backbone, arXiv:2012.04701) — counted inside CNN stratum above

## Framework stratum (INCLUDE, n=5) — qualitative template

| paper_id | components | license | benchmark_reproduction | release_version |
|---|---|---|---|---|
| 10.1101_2021.03.17.435903 | CERR platform extension; pre/post-processing configurations  | Open-source, GNU GPL | No quantitative benchmark results reported; framew | Not specified; prepr |
| 10.48550_arxiv.2203.12362 | Client-server architecture with GUI integrations (3D Slicer, | Apache-2.0 | Evaluated on Spleen MSD dataset (41 CT volumes) wi | 0.3.0 (as of submiss |
| 10.48550_arxiv.2211.02701 | MONAI Core modules: monai.data (datasets, readers/writers),  | Apache-2.0 License | Provides tools for benchmarking and performance op | No specific version  |
| 10.48550_arxiv.2406.05285 | Automatic branch (promptable class embedding) and interactiv | Not explicitly state | Benchmarked on 14 datasets with 127 classes, compa | Not specified; code  |
| 10.48550_arxiv.2503.08373 | UNet-based architecture (ResEnc-L from nnU-Net) with early p | Not explicitly state | Benchmarked on RadioActive benchmark, expert scrib | No specific version  |

Framework papers are EXCLUDED from the quantitative table (plan task-8 contract).

## Supervision regime (method INCLUDE)

- fully(implicit): 114
- semi: 2

## Multi-axis taxonomy (method INCLUDE)

- **Input dimensionality**: true-3D 100 / not-3D 16
- **Anatomical scope**: multi-organ 51 / single-organ 65
- **Code availability**: 23/116 report code
- **Best-Dice reported**: 110/116

## Year distribution (method INCLUDE)

- 2017: 3
- 2018: 5
- 2019: 18
- 2020: 18
- 2021: 10
- 2022: 18
- 2023: 18
- 2024: 8
- 2025: 15
- 2026: 3

## Per-organ Dice (methods papers only, aggregated from dice_per_organ)

| Organ | n (values) | Mean | Range |
|---|---|---|---|
| kidney | 46 | 90.2% | 63.2-99.5% |
| liver | 33 | 91.8% | 64.1-98.7% |
| bladder | 13 | 87.1% | 71.9-97.0% |
| lung | 12 | 94.7% | 67.0-99.2% |
| heart | 9 | 94.3% | 89.0-96.6% |
| spleen | 9 | 93.0% | 85.3-98.8% |
| pancreas | 9 | 75.2% | 23.9-86.5% |
| prostate | 7 | 82.1% | 49.5-97.8% |
| stomach | 7 | 86.3% | 67.0-92.5% |
| esophagus | 4 | 80.6% | 74.3-85.2% |

Cross-study aggregation over heterogeneous datasets/protocols; descriptive dispersion only (v1 convention).

## Quality assessment (method INCLUDE)

- 15-question rubric (v1-identical), n=116: mean **20.3/30**, median **21/30**

## v1-to-v2 study reconciliation (52 v1 studies)

- fulltext-missed: 30
- not-identified: 15
- re-included: 5
- s3-excluded: 1
- s2-excluded: 1

Per-study rows with reasons: `v1_v2_study_reconciliation.csv`. The 15 not-identified are absent from the
v2 dedup CSV by DOI and normalized title (search-template recall gap documented in Task-6 evidence);
30 fulltext-missed are v2-identified (mostly S2v2 INCLUDE) whose full text was paywalled/hand-off;
5 re-included passed v2 full-text screening again.
