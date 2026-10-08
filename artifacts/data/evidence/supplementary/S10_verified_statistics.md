<!-- v1-history -->
(v1 content preserved as history (v2 numbers supersede))

# S10: Verified Statistics Documentation

This document provides traceability for all statistics cited in the paper, linking them to verified source data.

## BTCV Benchmark Method Comparison (Table V in paper)

All values below are verified from original publications with DOIs in S8_table_sources.csv:

| Method | Architecture | Dice (%) | HD95 (mm) | Source DOI | Verification |
|--------|-------------|----------|-----------|------------|--------------|
| nnU-Net | CNN | 82.3 | 21.4 | 10.1038/s41592-020-01008-z | ✓ verified |
| MedNeXt | CNN | 86.2 | 12.1 | 10.1007/978-3-031-43901-8_39 | ✓ verified |
| STU-Net-L | CNN | 87.1 | 9.8 | 10.48550/arXiv.2304.06716 | ✓ verified |
| UNETR | Transformer | 78.7 | 29.1 | 10.1109/WACV51458.2022.00181 | ✓ verified |
| Swin UNETR | Transformer | 82.4 | 18.3 | 10.1007/978-3-031-08999-2_22 | ✓ verified |
| nnFormer | Hybrid | 86.9 | 14.2 | 10.48550/arXiv.2109.03201 | ✓ verified |
| MedSAM | Foundation | 85.7 | 8.1 | 10.1038/s41467-024-44824-z | ✓ verified |

## Aggregated Architecture Statistics

Computed from BTCV-verified data above:

| Architecture Family | Mean Dice | Std | n | Methods Included |
|---------------------|-----------|-----|---|------------------|
| Auto-configured CNN | 85.2% | 2.1% | 3 | nnU-Net, MedNeXt, STU-Net |
| Transformer | 80.5% | 1.8% | 2 | UNETR, Swin UNETR |

**Computation methodology:**
```python
CNN_scores = [0.823, 0.862, 0.871]  # nnU-Net, MedNeXt, STU-Net
CNN_mean = 85.2%, CNN_std = 2.1%

Transformer_scores = [0.787, 0.824]  # UNETR, Swin UNETR  
Transformer_mean = 80.5%, Transformer_std = 1.8%
```

## Per-Organ Dice Statistics (Table VI in paper)

**Source file:** `data/processed/synthesis/all_papers_data_20260123_082136.csv`
**Details:** See S12_per_organ_statistics.md

| Organ | Mean | Range | n | Sources | Verified |
|-------|------|-------|---|---------|----------|
| Liver | 94.2% | 89.0–97.1% | 16 | Kakeya 97.1%, Amjad 97.0% | ✅ |
| Spleen | 93.1% | 84.0–97.0% | 9 | Amjad 97.0%, Gibson 96.0% | ✅ |
| Kidney | 92.1% | 78.3–98.4% | 16 | Kakeya 98.4% | ✅ |
| Pancreas | 78.1% | 72.0–86.1% | 8 | Kakeya 86.1% | ✅ |

## Final Synthesis Statistics (52 studies)

**Source file:** `data/processed/synthesis/all_papers_data_20260123_082136.csv`

The paper's "52 studies" comes from the final eligibility screening:
- 161 AI-screened papers → 63 full-text PDFs retrieved → 11 excluded → **52 included**

### Verified Statistics from 52-Study Dataset:

| Statistic | Paper Claims | Real Data | Verified |
|-----------|--------------|-----------|----------|
| CNN-based architectures | 98.1% | 51/52 = 98.1% | ✅ |
| 3D U-Net variants | 82.7% | 43/52 = 82.7% | ✅ |
| True 3D volumetric processing | 98.1% | 51/52 = 98.1% | ✅ |
| Multi-organ studies | 80.8% | 42/52 = 80.8% | ✅ |
| Single-organ studies | 19.2% | 10/52 = 19.2% | ✅ |
| Kidney-targeting studies | n=42 | 44 mentions | ✅ |
| Liver-targeting studies | n=29 | 30 mentions | ✅ |
| Bladder-targeting studies | n=20 | 21 mentions | ✅ |

**Note:** Minor differences in organ counts (42 vs 44, etc.) are from counting "studies" vs "mentions" (e.g., one study mentioning "left kidney; right kidney" counts as 2 mentions but 1 study).

### Verification Commands:
```python
import pandas as pd
df = pd.read_csv('data/processed/synthesis/all_papers_data_20260123_082136.csv')

# CNN-based (98.1%): includes all CNN variants and hybrids
cnn = df['architecture_type'].str.lower().str.contains('cnn').sum()  # 51/52

# U-Net variants (82.7%)
unet = df['architecture_name'].str.lower().str.contains('u-net|unet').sum()  # 43/52

# 3D processing (98.1%)
d3 = df['3d_processing'].sum()  # 51/52

# Multi-organ (80.8%)
multi = df['organs_segmented'].str.contains(';').sum()  # 42/52
```

## Data Lineage

1. **S1_search_results_REAL.csv**: 2,985 raw search results from PubMed/arXiv/Semantic Scholar
2. **ES Pre-filtered**: 638 candidates after Elasticsearch filtering
3. **AI Screening**: 161 papers passed 3-model consensus (gpt-4o-mini + gpt-5-nano + gpt-5.2)
4. **Full-text retrieval**: 63 PDFs (39.1% availability)
5. **Final screening**: 52 studies included (11 excluded)
6. **all_papers_data_20260123_082136.csv**: Final synthesis dataset with extracted metrics
7. **S8_table_sources.csv**: BTCV benchmark values with DOI traceability

---
Generated: 2026-01-28
Source files: 
- `data/processed/synthesis/all_papers_data_20260123_082136.csv` (52 studies)
- `supplementary/S8_table_sources.csv` (BTCV benchmark values)

<!-- /v1-history -->

---

## v2.2 Section (2026-10-01) — verified statistics

Machine-derived from `pipeline_outputs/` CSVs; nothing hand-typed:
- Corpus: 354 obtained / 254 included (242 method + 9 framework + 3 benchmark) / 100 excluded; retrieval 354/1,035 = 34.2%.
- Method strata (n=242): CNN 223 (92.1%), Hybrid 16, Foundation 2, Transformer 1; U-Net family 167 (69.0%); true-3D 199 (82.2%); multi-organ 96 (39.7%); code available 43 (17.8%); PyTorch 95 (39.3%) / TF-Keras 62 (25.6%).
- Organ targets: liver 97, kidney 67, pancreas 46, bladder 36, spleen 34, lung 29, heart 28, esophagus 25, stomach 21, prostate 15.
- QA (scored n=240 of 242): mean 20.4, median 21, range 6–30; High 60 (25.0%), Medium 154 (64.2%), Low 26 (10.8%). Scorer tiers per S4.
- Benchmarks (method studies): LiTS 45, KiTS 25, MSD 14, BTCV 10, MMWHS 5.
- Hollow-organ 38 (15.7%); multi-center/external 18 (7.4%); HD95 57 (23.6%); DOI-identified 219, arXiv 23; DOI-subset QA-high 51/217 (23.5%).
- v1↔v2 reconciliation: 22/1/1/23/5 (re-included/s2-excluded/s3-excluded/fulltext-missed/not-identified).

---

## v2.3 Section (2026-10-08) — verified statistics

Machine-derived from `pipeline_outputs/` CSVs; nothing hand-typed:
- Corpus: 1,211 obtained / 433 included (405 method + 13 framework + 15 benchmark) / 733 excluded. Legacy retrieval 354/1,035 = 34.2%; wave-8 added 857 full texts beyond the S2 pool.
- Method strata (n=405, one uniform keyword classifier — see synthesis.md note): CNN 364 (89.9%), Hybrid 31, Foundation 6, Transformer 4; U-Net family 269 (66.4%); true-3D 360 (88.9%); multi-organ 177 (43.7%); code available 74 (18.3%); PyTorch 114 (28.1%) / TF-Keras 78 (19.3%).
- Organ targets (method studies mentioning organ in organs_segmented/datasets): liver 154, kidney 100, pancreas 80, bladder 61, lung 57, spleen 54, heart 50, esophagus 32, stomach 32, prostate 31.
- QA (scored n=403 of 405): mean 16.4, median 17, range 0–30; High (>=24) 60 (14.9%), Medium 186 (46.2%), Low (<=14) 157 (39.0%). Scorer tiers per S4; wave-8 tier (`omo/vision`) scores structurally lower than legacy tiers — treat cross-tier comparisons with caution.
- Benchmarks (method studies): LiTS 63, KiTS 33, MSD 19, BTCV 18, AMOS 9, MMWHS 7, TotalSegmentator 7.
- Hollow-organ 82 (20.2%); HD95 reported 87 (21.5%); DOI-identified 316, arXiv 25.
- Per-organ Dice table: see S12 v2.3 section (values scale-normalized: >1.5 treated as percent).