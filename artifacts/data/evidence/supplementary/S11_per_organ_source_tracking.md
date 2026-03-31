# S11: Per-Organ Performance Source Tracking

This document tracks the source of per-organ Dice scores cited in the main paper.

## IMPORTANT: Data Verification Status

⚠️ **Note**: Per-organ Dice scores in this document are cited directly from the original papers. They were NOT independently extracted/verified through our S2 data extraction process. Readers should verify these values against the original publications.

## Cited Per-Organ Performance Values

### Kakeya et al. (2018) - 3D U-JAPA-Net
- **Source**: \cite{kakeya2018ujapa}
- **DOI**: Check references.bib
- **Reported values**:
  - Liver: 97.1%
  - Kidney: 98.4%
  - Pancreas: 86.1%
- **Verification status**: ⚠️ Values from original paper, not in S2 extraction

### Amjad et al. (2022) - nnU-Net variants
- **Source**: \cite{amjad2022general}
- **DOI**: Check references.bib
- **Reported values**:
  - Liver: 97.0%
  - Spleen: 97.0%
- **Verification status**: ⚠️ Values from original paper, not in S2 extraction

### Gibson et al. (2018) - DenseVNet
- **Source**: \cite{gibson2018densevnet}
- **Study ID**: S015 (in S2_included_studies.csv)
- **Verified overall Dice**: 90.7% (from S2 extraction)
- **Per-organ values from paper**:
  - Liver: ~96.0%
  - Spleen: ~96.0%
- **Verification status**: ✓ Overall Dice verified; per-organ values from original paper

## Table VI (tab:synthesized_dice) - Per-Organ Ranges

The per-organ ranges in Table VI are representative values derived from:
1. Top performer citations above
2. General literature ranges

| Organ | Range | Source |
|-------|-------|--------|
| Liver | 89-97% | Kakeya, Amjad, Gibson papers |
| Kidney | 78-98% | Kakeya paper, literature |
| Spleen | 84-97% | Amjad, Gibson papers |
| Pancreas | 72-86% | Kakeya paper, literature |

## BTCV Benchmark Verified Data (Table V)

These values ARE verified from S8_table_sources.csv:

| Method | Dice | HD95 | DOI | Verified |
|--------|------|------|-----|----------|
| nnU-Net | 82.3% | 21.4mm | 10.1038/s41592-020-01008-z | ✓ |
| MedNeXt | 86.2% | 12.1mm | 10.1007/978-3-031-43901-8_39 | ✓ |
| STU-Net | 87.1% | 9.8mm | 10.48550/arXiv.2304.06716 | ✓ |
| UNETR | 78.7% | 29.1mm | 10.1109/WACV51458.2022.00181 | ✓ |
| Swin UNETR | 82.4% | 18.3mm | 10.1007/978-3-031-08999-2_22 | ✓ |
| nnFormer | 86.9% | 14.2mm | 10.48550/arXiv.2109.03201 | ✓ |
| MedSAM | 85.7% | 8.1mm | 10.1038/s41467-024-44824-z | ✓ |

## Architecture Family Statistics

### Verified (from S8, BTCV benchmark):
- **Auto-configured CNN**: 85.2±2.1% (n=3: nnU-Net, MedNeXt, STU-Net)
- **Transformer**: 80.5±1.8% (n=2: UNETR, Swin UNETR)

### Not Verified (removed from paper):
- Classic CNN (76.2±1.8%) - No source extraction
- Hybrid (78.9±1.6%) - No BTCV benchmark data

---
Generated: 2026-01-28
Purpose: Transparent documentation of data sources and verification status
