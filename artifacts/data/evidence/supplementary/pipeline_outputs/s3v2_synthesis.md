# S3v2 Synthesis — Architecture Strata, Supervision, Multi-Axis Taxonomy, Per-Organ Dice

**v2.2 (2026-10-01):** regenerated after the second shadow-library wave (+21 PDFs, glm-5.3-flash screened).
All counts machine-derived from `s3v2_extracted_data_full.csv` (354 rows), `s3v2_summary_table.csv`
(242 method-INCLUDE rows), `qa_v2_summary.csv`, and `v1_v2_study_reconciliation.csv`.
The 333/236-based v2.1 version is superseded.

## Funnel recap (full-text stage)

- Obtained distinct papers: **354** (186 original + 82 OA re-fetch + 96 user-sanctioned shadow-library; two re-screen waves)
- Full-text INCLUDE: **254** (method 242, framework 9, benchmark 3)
- Full-text EXCLUDE: **100** (method 90 incl. 4 unusable PDFs, benchmark 7, framework 2, review 1)
- Retrieval: 354/1,035 unique S2-includes = **34.2%**; 501 paywalled routed to librarian hand-off

## Architecture-family strata (method INCLUDE, n=242)

- **CNN**: 223/242
- **Hybrid**: 16/242
- **Transformer**: 1/242
- **Foundation**: 2/242
- U-Net family: 167/242 (69.0%)

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

## Multi-axis taxonomy (method INCLUDE)

- **Input dimensionality**: true-3D 199 / not-3D 43
- **Anatomical scope**: multi-organ 96 / single-organ 146
- **Code availability**: 43/242 report code
- **Per-organ Dice reported**: 233/242

## Year distribution (method INCLUDE)

- 2016: 2
- 2017: 10
- 2018: 18
- 2019: 36
- 2020: 45
- 2021: 31
- 2022: 29
- 2023: 21
- 2024: 16
- 2025: 26
- 2026: 8

## Per-organ Dice (methods papers only, first matching `dice_per_organ` entry per organ per study)

| Organ | studies | Mean | Range |
|---|---|---|---|
| liver | 69 | 93.6% | 64.1-98.7% |
| kidney | 48 | 92.9% | 52.5-99.0% |
| pancreas | 29 | 76.7% | 23.9-94.0% |
| bladder | 25 | 84.8% | 65.9-97.0% |
| spleen | 24 | 91.2% | 57.0-98.8% |
| heart | 22 | 93.4% | 87.0-96.6% |
| lung | 20 | 94.7% | 67.0-99.8% |
| esophagus | 17 | 75.5% | 50.3-85.2% |
| stomach | 17 | 87.1% | 67.0-94.4% |
| prostate | 9 | 82.5% | 49.5-97.8% |

Cross-study aggregation over heterogeneous datasets/protocols; descriptive dispersion only (v1 convention).

## Quality assessment (method INCLUDE, scored n=240 of 242)

- 15-question rubric (v1-identical): mean **20.4/30**, median **21/30**, range 6-30
- High (>=24): 60 (25.0%) | Medium: 154 (64.2%) | Low: 26 (10.8%)
- Scorer tiers: v1 GPT-4o/GPT-5.2; v2 batch-1 mini-class (mean 20.3, n=115); v2 batch-2 glm-5.3-flash (mean 20.5, n=125). Rubric identical across all waves.

## v1-to-v2 study reconciliation (52 v1 studies)

- fulltext-missed: 23
- re-included: 22
- not-identified: 5
- s3-excluded: 1
- s2-excluded: 1

The two fetch + re-screen waves recovered 17 additional v1 studies (re-included 5 -> 22; not-identified 15 -> 5).
