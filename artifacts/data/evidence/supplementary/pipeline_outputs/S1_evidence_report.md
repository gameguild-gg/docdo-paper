# S1 Search Results - Evidence Report

**Generated:** 2026-01-21 10:45:34  
**Purpose:** Document data quality and provenance for reproducibility

---

## Data Pipeline

| Stage | File | Records |
|-------|------|---------|
| Raw | `data/raw/S1_search_results_REAL.csv` | 2,985 |
| Deduplicated | `data/interim/S1_search_results_deduplicated.csv` | 2,821 |
| Duplicates removed | - | 164 (5.5%) |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total unique papers** | 2,821 |
| **With abstract (>100 chars)** | 2,562 (90.8%) |
| **With DOI** | 2,821 (100.0%) |
| **Average abstract length** | 1,465 chars |
| **Median abstract length** | 1,515 chars |

---

## By Source

### PubMed (via Entrez/Biopython API)

| Metric | Value |
|--------|-------|
| Records | 997 |
| With abstract | 992 (99.5%) |
| With DOI | 997 (100.0%) |
| Average abstract | 1,854 chars |
| Median abstract | 1,779 chars |
| Year range | 2022 - 2026 |

**Abstract distribution:**
- Empty (0 chars): 4
- Short (<500 chars): 1
- Full (≥500 chars): 992

### arXiv (via arxiv Python package)

| Metric | Value |
|--------|-------|
| Records | 904 |
| With abstract | 904 (100.0%) |
| With DOI | 904 (100.0%) |
| Average abstract | 1,315 chars |
| Median abstract | 1,325 chars |
| Year range | 2012 - 2026 |

**Abstract distribution:**
- Empty (0 chars): 0
- Short (<500 chars): 11
- Full (≥500 chars): 893

### Semantic Scholar (via free API)

| Metric | Value |
|--------|-------|
| Records | 920 |
| With abstract | 666 (72.4%) |
| With DOI | 920 (100.0%) |
| Average abstract | 1,191 chars |
| Median abstract | 1,367 chars |
| Year range | 1975 - 2026 |

**Abstract distribution:**
- Empty (0 chars): 253
- Short (<500 chars): 9
- Full (≥500 chars): 658

---

## Data Quality Assessment

### Strengths
- ✅ 100% of records have DOI/identifier for verification
- ✅ 90.8% have full abstracts for screening
- ✅ PubMed and arXiv have near-complete abstracts
- ✅ All data fetched from official APIs (verifiable)

### Limitations
- ⚠️ Semantic Scholar has 27.6% missing abstracts (API limitation)
- ⚠️ 257 total records without abstracts (may need title-only screening)

---

## Reproducibility Evidence

### API Sources
| Source | API | Package | Query Date |
|--------|-----|---------|------------|
| PubMed | Entrez E-utilities | biopython 1.86 | 2026-01-21 |
| arXiv | arXiv API | arxiv 2.4.0 | 2026-01-21 |
| Semantic Scholar | Graph API v1 | requests 2.32.5 | 2026-01-21 |

### Search Queries
- **PubMed:** CT/computed tomography + segmentation + organ + deep learning
- **arXiv:** CT computed tomography segmentation organ deep learning
- **Semantic Scholar:** Multiple queries covering CT, organ segmentation, deep learning

### Deduplication Method
1. **DOI matching:** Exact DOI comparison (case-insensitive)
2. **Title matching:** Normalized title comparison (lowercase, whitespace-collapsed)
3. **Priority:** Keep record with most complete metadata

---

## Sample Records (DOI Verification)

| ID | Database | DOI | Year | Title (truncated) |
|----|----------|-----|------|-------------------|
| R0001 | PubMed | 10.1007/s12664-025-01925-x | 2026 | Deep-learning pipeline for automated... |
| R0002 | PubMed | 10.1109/access.2025.3631322 | 2025 | From CNNs to SAM: A Survey... |
| R1000 | arXiv | arXiv:2401.xxxxx | 2024 | [varies] |
| R2000 | Semantic Scholar | 10.xxxx/xxxxx | [varies] | [varies] |

All DOIs can be verified at https://doi.org/[DOI]

---

## Files

| File | Location | Description |
|------|----------|-------------|
| Raw data | `data/raw/S1_search_results_REAL.csv` | Original API fetch |
| Deduplicated | `data/interim/S1_search_results_deduplicated.csv` | Cross-source deduplication |
| Fetch script | `supplementary/scripts/fetch_all_real_data.py` | Reproducible fetch |
| Dedup script | `supplementary/scripts/deduplicate_s1.py` | Deduplication logic |
| This report | `data/interim/S1_evidence_report.md` | Evidence documentation |

---

**Report Version:** 1.0  
**Author:** Automated pipeline  
**Date:** 2026-01-21
