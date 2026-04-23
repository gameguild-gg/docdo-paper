# S12: Per-Organ Dice Score Statistics from 52 Reviewed Studies

**Primary source:** Per-organ Dice values were transcribed from the original primary studies as cited in the Sources column below. The intermediate aggregation file (`data/processed/synthesis/all_papers_data_20260123_082136.csv`) produced during analysis is **not retained in the repository**; the same per-organ values can be regenerated from [pipeline_outputs/s3_extracted_data_full.csv](pipeline_outputs/s3_extracted_data_full.csv) (the 52-study full-text extraction) and [S2_final_included_studies.csv](S2_final_included_studies.csv) (the included-paper identifier list). Cell-level provenance for the BTCV/AMOS/KiTS aggregates is recorded separately in [S8_table_sources.csv](S8_table_sources.csv); per-organ source attribution is in [S11_per_organ_source_tracking.md](S11_per_organ_source_tracking.md), which also documents that the per-organ values were not independently re-extracted from the underlying CT volumes.

## Summary Statistics

| Organ | Mean | Range | n | Sources |
|-------|------|-------|---|---------|
| Liver | 94.2% | 89.0–97.1% | 16 | Kakeya (97.1%), Amjad (97.0%), Gibson (96.0%) |
| Spleen | 93.1% | 84.0–97.0% | 9 | Amjad (97.0%), Gibson (96.0%) |
| Kidney | 92.1% | 78.3–98.4% | 16 | Kakeya (98.4%), nnU-Net variants |
| Pancreas | 78.1% | 72.0–86.1% | 8 | Kakeya (86.1%), Attention U-Net |

## Computation Method

```python
import pandas as pd
df = pd.read_csv('data/processed/synthesis/all_papers_data_20260123_082136.csv')

organs = ['liver_dice', 'kidney_dice', 'spleen_dice', 'pancreas_dice']
for organ in organs:
    values = pd.to_numeric(df[organ], errors='coerce').dropna()
    print(f'{organ}: n={len(values)}, Mean={values.mean():.1f}%, Range={values.min():.1f}–{values.max():.1f}%')
```

## Results (verified 2026-01-28):
```
Liver: n=16, Mean=94.2%, Range=89.0–97.1%
Kidney: n=16, Mean=92.1%, Range=78.3–98.4%
Spleen: n=9, Mean=93.1%, Range=84.0–97.0%
Pancreas: n=8, Mean=78.1%, Range=72.0–86.1%
```

## Top Performer Studies (verified from all_papers_data.csv)

### Kakeya et al. (2018) - 3D U-JAPA-Net
- Liver: 97.1%
- Kidney: 98.4%
- Pancreas: 86.1%
- DOI: MICCAI LNCS proceedings

### Amjad et al. (2022) - nnU-Net variants
- Liver: 97.0%
- Spleen: 97.0%
- Venue: Medical Physics

### Gibson et al. (2018) - DenseVNet
- Liver: 96.0%
- Spleen: 96.0%
- Venue: IEEE TMI

---
Generated: 2026-01-28
Source: data/processed/synthesis/all_papers_data_20260123_082136.csv
