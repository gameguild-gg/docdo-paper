# S3v2 Synthesis — Architecture Strata, Supervision, Multi-Axis Taxonomy, Per-Organ Dice

**v2.3 (2026-10-08):** regenerated after wave-8 (+857 PDFs, `omo/vision` lane screened, network-retry hardened).
All counts machine-derived from `s3v2_extracted_data_full.csv` (1,166 rows), `s3v2_summary_table.csv`
(405 method-INCLUDE rows), `qa_v2_summary.csv`, and `v1_v2_study_reconciliation.csv`.
The 354/254-based v2.2 version is superseded.

## Funnel recap (full-text stage)

- Obtained distinct papers: **1,211** (186 original + 82 OA re-fetch + 96 shadow v1/v2 + 857 shadow/expansion wave-8)
- Full-text INCLUDE: **433** (method 405, framework 13, benchmark 15)
- Full-text EXCLUDE: **733**
- Acquisition beyond the original 1,035 S2-pool runs through user-sanctioned shadow/expansion harvest waves; 501 paywalled remain routed to librarian hand-off

## Architecture-family strata (method INCLUDE, n=405)

- **CNN**: 364/405
- **Hybrid**: 31/405
- **Transformer**: 4/405
- **Foundation**: 6/405
- U-Net family: 269/405 (66.4%)
- Note: v2.3 applies one explicit keyword classifier (foundation/SAM regex; transformer+CNN-mix -> Hybrid) uniformly to all 405 rows; the v2.2 counts (223/16/1/2) were produced by an ad-hoc pass and are not exactly reproducible, so strata are comparable within v2.3, not row-by-row against v2.2.

## Framework stratum (INCLUDE, n=13) — qualitative template

| paper_id | components | license | benchmark_reproduction | release_version |
|---|---|---|---|---|
| 10.1101_2021.03.17.435903 | CERR platform extension; pre/post-processi | Open-source, GNU GPL (GNU-copyrighted) wit | No quantitative benchmark results reported | Not specified; preprint from 2021. |
| 10.48550_arxiv.2211.02701 | MONAI Core modules: monai.data (datasets,  | Apache-2.0 License | Provides tools for benchmarking and perfor | No specific version number mentioned; pape |
| 10.48550_arxiv.2406.05285 | Automatic branch (promptable class embeddi | Not explicitly stated; code and weights pu | Benchmarked on 14 datasets with 127 classe | Not specified; code and weights available  |
| 10.48550_arxiv.2503.08373 | UNet-based architecture (ResEnc-L from nnU | Not explicitly stated in the paper; public | Benchmarked on RadioActive benchmark, expe | No specific version number mentioned; publ |
| 10.1001_jamanetworkopen.2020.27426 | InnerEye end-to-end pipeline (Figure 3): h | Code license not stated in paper; article  | No versioned benchmark reproduction; exter | Not stated in paper |
| 10.1007_978-3-031-17027-0_2 | DeepEdit model (automatic, semi-automatic, | Not stated in paper (code hosted in Projec | Reproduces baseline comparisons: nnU-Net o | MONAI Core 0.8.1; MONAI Label 0.3.1 |
| 10.1007_s10278-025-01716-y | Segment Model CT (SMCT) for Couinaud segme | Not explicitly stated for code (article is | External evaluation on LiTS test set appli | Not explicitly stated; described as partia |
| 10.1016_j.media.2024.103207 | MONAI Label Server (REST API, DICOMWeb: WA | Apache-2.0 | Evaluated on MSD Spleen (41 CT volumes, 4- | 0.3.0 |
| 10.21203_rs.3.rs-9480032_v1 | Containerized models on shared mhubai/base | Article: CC BY 4.0; software open-source o | Yes: side-by-side evaluation of 3 lung seg | No explicit version number; Docker Hub ima |
| 10.3390_bioengineering13050572 |  |  |  |  |
| 1910.09308v1 | MIScnn (community analog of MONAI / nnInte |  |  |  |
| 2208.05868v2 | nnU-Net |  |  |  |
| 2512.15921v2 | 3D Slicer / OHIF / dcmqi / MONAI ecosystem |  |  |  |

Framework papers are EXCLUDED from the quantitative table (plan task-8 contract).

## Multi-axis taxonomy (method INCLUDE)

- **Input dimensionality**: true-3D 360 / not-3D 45
- **Anatomical scope**: multi-organ 177 / single-organ 228
- **Code availability**: 74/405 report code
- **Per-organ Dice reported**: 301/405

## Year distribution (method INCLUDE)

- 2015: 1
- 2016: 2
- 2017: 14
- 2018: 29
- 2019: 48
- 2020: 59
- 2021: 49
- 2022: 53
- 2023: 35
- 2024: 31
- 2025: 53
- 2026: 31

## Per-organ Dice (methods papers only, first matching `dice_per_organ` entry per organ per study; values scale-normalized: percentages >1.5 divided by 100)

| Organ | studies | Mean | Range |
|---|---|---|---|
| liver | 87 | 93.9% | 64.1-98.7% |
| kidney | 56 | 93.4% | 78.3-99.0% |
| pancreas | 43 | 75.5% | 0.0-94.0% |
| bladder | 39 | 87.4% | 65.9-97.0% |
| spleen | 27 | 91.7% | 57.0-98.8% |
| heart | 28 | 92.9% | 85.0-96.6% |
| lung | 29 | 95.2% | 67.0-99.8% |
| esophagus | 21 | 75.5% | 50.3-85.2% |
| stomach | 21 | 87.9% | 67.0-94.4% |
| prostate | 19 | 85.2% | 49.5-97.8% |

Cross-study aggregation over heterogeneous datasets/protocols; descriptive dispersion only (v1 convention).

## Quality assessment (method INCLUDE, scored n=403 of 405)

- 15-question rubric (v1-identical): mean **16.4/30**, median **17/30**, range 0-30
- High (>=24): 60 (14.9%) | Medium (15-23): 186 (46.2%) | Low (<=14): 157 (39.0%)
- Scorer tiers: v1 GPT-4o/GPT-5.2; v2 batch-1 mini-class; v2 batch-2 glm-5.3-flash; v2.3 wave-8 `omo/vision` (band cutoffs calibrated against v2.2: >=24 High and <=14 Low reproduce 60/26 exactly on the 240 legacy scores).

## v1-to-v2 study reconciliation (52 v1 studies)

- fulltext-missed: 23 / re-included: 22 / not-identified: 5 / s3-excluded: 1 / s2-excluded: 1
- v2.3 additions (see `v1_v2_study_reconciliation.csv`): 30 wave-8 INCLUDE manifestations deduplicated against existing corpus studies (preprint-vs-published, arXiv-version, supplement-base DOI); 1 human-adjudication flag (`10.1016_j.eclinm.2024.102772`: C1 INCLUDE conf 0.6 vs wave-8 EXCLUDE; wave-8 retained).
