# S3v2 Synthesis — Architecture Strata, Supervision, Multi-Axis Taxonomy, Per-Organ Dice

**v2.1 (2026-09-30):** regenerated after the glm-5.3-flash re-screen of 149 additional full texts
(OA re-fetch + user-sanctioned shadow-library acquisition). All counts machine-derived from
`s3v2_extracted_data_full.csv` (333 rows), `s3v2_summary_table.csv` (224 method-INCLUDE rows),
`qa_v2_summary.csv`, and `v1_v2_study_reconciliation.csv`. The prior 186/121-based version is superseded.

## Funnel recap (full-text stage)

- Obtained distinct papers: **333** (186 original + 82 OA re-fetch + 75 shadow-library; 149 re-screened by glm-5.3-flash after dedup of supplementary payloads)
- Full-text INCLUDE: **236** (method 224, framework 9, benchmark 3)
- Full-text EXCLUDE: **97** (method 87 incl. 4 unusable PDFs, benchmark 7, framework 2, review 1)
- Retrieval: 333/1,035 unique S2-includes = **32.2%**; 515 paywalled routed to librarian hand-off

## Architecture-family strata (method INCLUDE, n=224)

- **CNN**: 205/224
- **Hybrid**: 16/224
- **Transformer**: 1/224
- **Foundation**: 2/224
- U-Net family: 160/224 (71.4%)

## Framework stratum (INCLUDE, n=9) — qualitative template

| paper_id | components | license | benchmark_reproduction | release_version |
|---|---|---|---|---|
| 10.1101_2021.03.17.435903 | CERR platform extension; pre/post-processing configurations  | Open-source, GNU GPL | No quantitative benchmark results reported; framew | Not specified; prepr |
| 10.48550_arxiv.2211.02701 | MONAI Core modules: monai.data (datasets, readers/writers),  | Apache-2.0 License | Provides tools for benchmarking and performance op | No specific version  |
| 10.48550_arxiv.2406.05285 | Automatic branch (promptable class embedding) and interactiv | Not explicitly state | Benchmarked on 14 datasets with 127 classes, compa | Not specified; code  |
| 10.48550_arxiv.2503.08373 | UNet-based architecture (ResEnc-L from nnU-Net) with early p | Not explicitly state | Benchmarked on RadioActive benchmark, expert scrib | No specific version  |
| 10.1001_jamanetworkopen.2020.27426 | InnerEye end-to-end pipeline (Figure 3): hospital image acqu | Code license not sta | No versioned benchmark reproduction; external vali | Not stated in paper |
| 10.1007_978-3-031-17027-0_2 | DeepEdit model (automatic, semi-automatic, and refinement mo | Not stated in paper  | Reproduces baseline comparisons: nnU-Net on PROSTA | MONAI Core 0.8.1; MO |
| 10.1007_s10278-025-01716-y | Segment Model CT (SMCT) for Couinaud segments on CT; Segment | Not explicitly state | External evaluation on LiTS test set applied direc | Not explicitly state |
| 10.1016_j.media.2024.103207 | MONAI Label Server (REST API, DICOMWeb: WADO-RS/STOW-RS/QIDO | Apache-2.0 | Evaluated on MSD Spleen (41 CT volumes, 4-stage ac | 0.3.0 |
| 10.21203_rs.3.rs-9480032_v1 | Containerized models on shared mhubai/base image; unified ap | Article: CC BY 4.0;  | Yes: side-by-side evaluation of 3 lung segmentatio | No explicit version  |

Framework papers are EXCLUDED from the quantitative table (plan task-8 contract).

## Supervision regime (method INCLUDE)

- fully(implicit): 217
- semi: 5
- self: 2

## Multi-axis taxonomy (method INCLUDE)

- **Input dimensionality**: true-3D 184 / not-3D 40
- **Anatomical scope**: multi-organ 90 / single-organ 134
- **Code availability**: 41/224 report code
- **Best-Dice reported**: 212/224

## Year distribution (method INCLUDE)

- 2016: 1
- 2017: 7
- 2018: 16
- 2019: 32
- 2020: 43
- 2021: 27
- 2022: 27
- 2023: 21
- 2024: 16
- 2025: 26
- 2026: 8

## Per-organ Dice (methods papers only, aggregated from dice_per_organ)

| Organ | n (values) | Mean | Range |
|---|---|---|---|
| liver | 100 | 89.8% | 8.0-98.7% |
| kidney | 92 | 88.5% | 50.2-99.5% |
| pancreas | 40 | 76.4% | 23.9-96.0% |
| lung | 33 | 95.0% | 62.0-99.8% |
| spleen | 26 | 89.2% | 33.0-98.8% |
| bladder | 26 | 84.6% | 65.9-97.0% |
| heart | 22 | 93.0% | 86.0-96.6% |
| stomach | 19 | 87.3% | 67.0-97.0% |
| esophagus | 17 | 74.3% | 50.3-85.2% |
| prostate | 8 | 81.5% | 49.5-97.8% |

Cross-study aggregation over heterogeneous datasets/protocols; descriptive dispersion only (v1 convention).

## Quality assessment (method INCLUDE, scored n=222 of 224)

- 15-question rubric (v1-identical): mean **20.5/30**, median **21/30**, range 6-30
- High (>=24): 56 (25.2%) | Medium: 142 (64.0%) | Low: 24 (10.8%)
- Scorer tiers: v1 GPT-4o/GPT-5.2; v2 batch-1 deepseek-v4-flash (mean 20.3, n=116); v2 batch-2 glm-5.3-flash (mean 20.7, n=107). Rubric identical across all waves.

## v1-to-v2 study reconciliation (52 v1 studies)

- fulltext-missed: 26
- re-included: 20
- not-identified: 5
- s3-excluded: 1

The fetch + re-screen waves recovered 15 additional v1 studies (re-included 5 -> 20; not-identified 15 -> 5).
