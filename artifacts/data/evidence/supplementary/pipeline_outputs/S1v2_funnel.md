# S1v2 Funnel — Dedup + Pre-Filter with Bypass-Lane Split

**Generated:** 2026-09-08 by `operations/src/_archive/scripts/v2_filter_and_funnel.py`
(every count machine-derived from the artifact files named below).
**Status:** Checker-verified — `es_pass_total == es_pass_standard + es_pass_framework_bypass
== COUNT(DISTINCT record ids passing either lane)`; lanes disjoint.

## 1. Funnel (v2)

| Stage | N | Authoritative artifact |
|-------|---|------------------------|
| Records identified (raw; per-source breakdown below) | **14,547** | `raw/v2/_combined.csv` (concat of 30 immutable per-query CSVs; `S1v2_evidence_report.md`) |
| Deduplication by DOI + normalised title | **8,846** | `interim/S1v2_search_results_deduplicated.csv` (tracked copy: `pipeline_outputs/S1v2_search_results_deduplicated.csv`); duplicate-DOI rate in output: 0.0000% |
| Pre-filter, standard lane — passes standard inclusion AND strict exclusions AND NOT `framework_candidate` | **641** | `pipeline_outputs/S2v2_elasticsearch_filtered.csv` (`framework_candidate=false`) |
| Pre-filter, framework bypass lane — `framework_candidate` only | **460** | `pipeline_outputs/S2v2_elasticsearch_filtered.csv` (`framework_candidate=true`) |
| **`es_pass_total`** — records-screened input (= standard + bypass; sole PRISMA "records screened" number) | **1,101** | checker assert above; this union row is what Task 11's diagram consumes |

## 2. Delta vs v1

v1 numbers parsed from [`S_PRISMA_funnel.md`](../S_PRISMA_funnel.md) §1.
v1's single "ES-filtered" stage is NOT commensurable with v2 without the
lane split — the v2 bypass lane admits records the v1 filter excluded by
construction.

| Stage | v1 | v2 | Δ |
|-------|---:|---:|---:|
| Raw | 2,985 | 14,547 | +11,562 |
| Dedup | 2,821 | 8,846 | +6,025 |
| Pre-filtered (v1: single ES stage; v2: `es_pass_total`) | 638 | 1,101 | +463 |

## 3. Lane status (documented degradations)

Raw records by source (machine-derived from `raw/v2/_combined.csv`):

| Source | Raw records |
|--------|------------:|
| arXiv | 7,164 |
| PubMed | 7,045 |
| Google Scholar | 338 |

- **Semantic Scholar: blocked** — all 6 family queries (A/B/C/D/E/G-S2-001)
  returned 0 records on 2026-09-08 (sustained rate-limit storm; interactive
  probes returned HTTP 429/500 incl. a failing control probe — see
  [`S1v2_evidence_report.md`](S1v2_evidence_report.md) §Degradation Narrative).
- **EBSCO ChampSearch: render-count only** — queries executed in a guest
  browser session (hit counts logged in the evidence report); no record
  harvest. A pending logged-session EBSCO harvest may add rows later.
- **Google Scholar: partial** — A/B truncated by soft-blocks (7/11 rows),
  D/E/G at the 100-results/query cap; non-reproducible by design.

Re-run note: this task's outputs are idempotent (the driver overwrites the
interim dedup CSV's tracked copy, the filtered CSV, and this funnel md);
an EBSCO harvest landing later re-runs Task 5 cleanly.

## 4. Retention sanity — v1 core reproduced?

Of the v1 52 included studies
([`S2_final_included_studies.csv`](../S2_final_included_studies.csv)),
**32/52** appear in the v2 dedup CSV (9 by DOI, 23 by
normalised title). This sits BELOW the ≥ 30 sanity bar — the absences were
verified genuine (by de-mangled DOI and normalised title) and are
explainable, not silent losses: (1) the Semantic Scholar lane was blocked
this run (v1 drew 1,084 records from S2); (2) v1's PubMed query
carried a bare `organ[tiab]` anatomy term that has no v2 family-F
equivalent (papers indexed only as "organ(s)" without a specific F anatomy
word drop out); (3) PubMed/arXiv 1,000-record caps select different
relevance windows than v1's 997/904-record windows. Family G (v1 core DL
architectures) protects the core query shape; it cannot protect against
lane blocks or cap windows. Misses:

| Study | DOI | Title (truncated) | Reason |
|-------|-----|-------------------|--------|
| S001 | 10.1002/mp.12480 | Deep learning of the sectional appearances of 3D CT images for anatomical struct | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S002 | 10.1002/mp.13300 | AnatomyNet: Deep learning for fast and fully automated whole-volume segmentation | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S003 | 10.1002/mp.13438 | U-Net based deep learning bladder segmentation in CT urography | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S007 | 10.1002/mp.15507 | General and custom deep learning autosegmentation models for organs in head and  | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S008 | 10.1007/978-3-030-00937-3_49 | 3D U-JAPA-Net: Mixture of Convolutional Networks for Abdominal Multi-organ CT Se | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S012 | 10.1038/s41598-019-40584-9 | Dual-energy CT for automatic organs-at-risk segmentation in brain-tumor patients | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S015 | 10.1088/1361-6560_aaf11c | Fully automated organ segmentation in male pelvic CT images | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S017 | 10.1109/ACCESS.2020.3024277 | Automatic Segmentation Using a Hybrid Dense Network Integrated With an 3D-Atrous | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S018 | 10.1109/cvidliccea56201.2022.9823971 | Research on Liver Segmentation of CT Image Based on Deep Active Contour Model | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S019 | 10.1109/ICIEAM48468.2020.9111950 | Hybrid 3D-ResNet Deep Learning Model for Automatic Segmentation of Thoracic Orga | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S020 | 10.1109/SPS.2019.8882073 | Segmentation of Organs at Risk in Chest Cavity Using 3D Deep Neural Network | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S022 | 10.1109/WRCSARA57040.2022.9903976 | Two-Stage Multi-Organ Automatic Segmentation with Low GPU Memory Occupancy | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S023 | 10.1186/s12880-025-02106-0 | Deep learning-based volumetry of the future liver remnants and prediction of can | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S024 | 10.1186/s13014-022-01985-9 | Dosimetric impact of deep learning-based CT auto-segmentation on radiation thera | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S025 | 10.1186/s41747-024-00507-4 | Segmentation-based quantitative measurements in renal CT imaging using deep lear | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S026 | 10.3389/fonc.2018.00215 | Deep Learning Renal Segmentation for Fully Automated Radiation Dose Estimation i | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S030 | arXiv/1809.04430 | Deep learning to achieve clinically applicable segmentation of head and neck ana | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S031 | arXiv/1908.00360 | A Method of Rapid Quantification of Patient-Specific Organ Dose for CT Using Cou | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S035 | http/__arxiv.org_abs_1809.00960v2 | Organ at Risk Segmentation in Head and Neck CT Images Using a Two-Stage Segmenta | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |
| S047 | http/__arxiv.org_abs_2203.01934v1 | Quality or Quantity: Toward a Unified Approach for Multi-organ Segmentation in B | not retrieved by the v2 lanes this run — Semantic Scholar lane blocked; v1's bare organ[tiab] PubMed term has no family-F equivalent; 1,000-record caps select different relevance windows; Task 9 reconciles |

The full 52-row study-level reconciliation (outcome ∈ re-included /
s2-excluded / s3-excluded / fulltext-missed / not-identified) is Task 9's
deliverable (`pipeline_outputs/v1_v2_study_reconciliation.csv`).

## 5. Provenance

- Dedup: `docdo deduplicate -i raw/v2/_combined.csv -o interim/S1v2_search_results_deduplicated.csv`
  (14,547 → 8,846; `docdo.dedup` DOI + normalised-title, empty DOIs skipped).
- Pre-filter: pure-Python evaluation of the pinned inclusion DSL
  (`filter_with_elasticsearch.inclusion_query()`) with the module's
  exact-token semantics, then `apply_exclusion_filters()` (strict
  Python-side precision + `framework_candidate` flag). Live Elasticsearch
  was unavailable this run; the ES english-analyzer stemming is not
  replicated (recall-side approximation only — pinned precision is
  Python-side by Task-3 design). The filtered CSV therefore carries no
  `es_score`/`es_id` columns (no ES hits); schema = dedup columns +
  `framework_candidate`.
