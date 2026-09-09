# S2v2 Seed Recall Oracle — Task 6 (paper-coverage-gap-update)

**Generated:** 2026-09-08
**Binding spec:** `.omo/plans/paper-coverage-gap-update.md` Task 6 (recall oracle).
**Input artifacts:** `interim/S1v2_search_results_deduplicated.csv` (8,161 rows),
`pipeline_outputs/S2v2_elasticsearch_filtered.csv` (901 rows = 464 standard + 437 bypass).

Each seed reaches exactly one of INCLUDE / excluded-with-logged-reason /
not-indexed — **except MONAI Deploy, recorded BLOCKED** (query-layer failure
whose sanctioned remedy cannot recover it; see row 4). Seeds marked
*in screening pool* have satisfied the identification and pre-filter stages;
their INCLUDE/EXCLUDE decision belongs to the S2v2 3-vote screening run,
which is currently blocked on the missing `OPENAI_API_KEY` (see
`S2v2_screening_log.md`).

## Seed table (12 rows)

| # | Seed | Status | Evidence |
|---|------|--------|----------|
| 1 | MONAI | in screening pool (R5017, bypass lane) | arXiv:2211.02701 "MONAI: An open-source framework for deep learning in healthcare" (Cardoso et al. 2022 — the MONAI framework paper), `framework_candidate=true`. The title variant "MONAI: Medical Open Network for AI" is NOT indexed: PubMed exact-title 0 hits, arXiv 0 hits (2026-09-08). **Plan's pinned id arXiv:2011.08506 is WRONG** — verified to resolve to an unrelated physics paper ("Coupled spin-1/2 antiferromagnetic chain Cs2LiRuCl6..."); do not use it for inbox naming. |
| 2 | Auto3DSeg | **not-indexed** | No canonical peer-reviewed paper exists. Zero-hit log: PubMed `"Auto3DSeg: A Large-Scale Benchmark and Comprehensive Evaluation of 3D Medical Image Segmentation"[ti]` = 0; PubMed `Auto3DSeg[tiab]` = 9 hits, ALL application papers (none canonical — verified 2026-09-08); arXiv `ti:"Auto3DSeg"` = 3 hits, all applications; arXiv `abs:"Medical Open Network for AI"`-class title probes = 0. Semantic Scholar lane blocked (control probe HTTP 429 at both spaced retries, 2026-09-08 — storm context in `S1v2_evidence_report.md`). The citable artifact is Project-MONAI Auto3DSeg technical documentation (tutorials/Zenodo). **Plan's pinned id arXiv:2209.13545 is WRONG** — resolves to "The Proximal Map of the Weighted Mean Absolute Error"; do not use it. Bib coverage: Task 9 @techreport (plan-sanctioned path, NV-Segment-CT precedent). |
| 3 | MONAI Label | in screening pool (R4847, bypass lane) | arXiv:2203.12362 "MONAI Label: A framework for AI-assisted Interactive Labeling of 3D Medical Images", `framework_candidate=true`. **Plan's pinned id arXiv:2203.12345 is WRONG** — resolves to "Surface Patches with Rounded Corners"; the correct id is 2203.12362 (verified by direct arXiv id_list fetch + title match). |
| 4 | MONAI Deploy | **BLOCKED** (query-layer; 1 fix loop executed) | The canonical citable paper EXISTS and is PubMed-indexed: Gupta et al. 2024, "Current State of Community-Driven Radiological AI Deployment in Medical Imaging", JMIR AI 3:e55833, PMID 39653370, DOI 10.2196/55833 (verified by DOI lookup 2026-09-08; official MONAI Deploy citation per project-monai.github.io/deploy.html). It is unreachable by the sanctioned remedy: its tiab does NOT contain "MONAI Deploy" (PubMed `"MONAI Deploy"[tiab]` = 0), so no tool-name term matches; it matches only family-B's broad vocabulary arm (20,929 PubMed matches), whose 1,000-record fetch window is date-descending and 2026-dominated (B-PUB-001: 997/999 rows from 2026; B-PUB-002 re-fetch: same window behavior; the 2024 PMID sits outside every observed 1,000-window under both default and pub_date sort). No minimal yaml term addition can surface a 2024 record behind ~20k newer matches — recovery requires a fetcher-level window fix (explicit sort or deeper pagination in `fetch_pubmed_v2`, Task-3 code, outside Task-6's amendable surface). Recommended interim: cite via Task 9 bib (DOI above) and flag the fetcher fix for orchestrator sanction. arXiv: not present (title probes 0). |
| 5 | VISTA-3D | in screening pool (R5809, bypass lane) | arXiv:2406.05285 — **pinned id VERIFIED CORRECT**, but the title is "VISTA3D: A Unified Segmentation Foundation Model For 3D Medical Imaging" (unhyphenated). The hyphenated family-B term "VISTA-3D" could not match it in any fielded index (root cause of the original miss). Fixed by the Task-6 query-layer fix loop: `queries_v2.yaml` revision r1 adds the exact token VISTA3D to family B (query ids B-*-002); re-fetched via B-ARX-002; ES whitelist synced (`FRAMEWORK_TOOL_NAMES` += "VISTA3D"); tool-name anatomy-check guard added so framework tool papers reach the bypass lane. `framework_candidate=true`. |
| 6 | NV-Segment-CT | **not-indexed** | Zero-hit log (2026-09-08): PubMed `"NV-Segment-CT"[tiab] OR "NV Segment CT"[tiab]` = 0; arXiv `all:"NV-Segment-CT"` = 0; Semantic Scholar blocked (control probe 429, both retry rounds — recorded as evidence context per plan scoping; the S2 zero-hit is therefore unverified, not contradicted). Consistent with the plan's pre-declaration: NV-Segment-CT is industry technical documentation that PubMed/arXiv/S2 do not index; bib coverage via Task 9 @techreport satisfies the success criterion without S2 inclusion. |
| 7 | nnInteractive | in screening pool (R4964, bypass lane) | arXiv:2503.08373 "nnInteractive: Redefining 3D Promptable Segmentation", `framework_candidate=true`. Originally dropped by the pre-filter's method-paper anatomy checks ("Bone/skeletal only" — abstract mentions spine/vertebrae targets, no organ-list term); restored by the Task-6 tool-name anatomy-check guard. |
| 8 | MedSAM | excluded-with-logged-reason (pre-filter, recall stage) | Canonical "Segment Anything in Medical Images" IS identified — in dedup as the Google Scholar row R0155 (title-exact; GS hits process normally per plan scoping) — but fails the recall DSL on the GS snippet: the two-sentence snippet carries no IC1 deep-learning anchor term (machine reason: recall miss, IC1). The arXiv copy (2304.12306, verified) is additionally buried below the relevance window of both C-ARX samples (893-row stable parse; not in any top-100 page of either -001/-002 fetch; informational retrieval limitation). Reason code: IC1 retrieval anchor. |
| 9 | SAM-Med3D | excluded-with-logged-reason (pinned-template scope) | Canonical arXiv:2310.15161 "SAM-Med3D: Towards General-purpose Segmentation Models for Volumetric Medical Images" is indexed (arXiv `ti:"SAM-Med3D"` rank 1; S2 total=3365 with canonical in top-3, confirmed via a storm-window slip-through on 2026-09-08) but is structurally unreachable by family C's pinned conjunction template: the canonical abstract contains ZERO family-F anatomy/CT tokens (verified token-by-token: no liver/kidney/.../CT), so `(family-C terms) AND (segmentation) AND (F anatomy)` cannot match it. One fix loop executed (C-ARX-002 resample; query text unchanged) — confirmed the 893-row parse is stable and the miss is template-inherent, not API flakiness. No minimal term addition legitimately surfaces an abstract with no anatomy anchor (the anchor IS the review's CT-organ scope). Reason code: IC3/IC4 retrieval anchor (family F). Flagged for Limitations (Task 9/11): general-purpose foundation models that omit CT/organ terms in the abstract are invisible to the pinned template. |
| 10 | U-Mamba | in screening pool (R6519, standard lane) | arXiv:2401.04722 "U-Mamba: Enhancing Long-range Dependency for Biomedical Image Segmentation" (correct canonical id established at execution; retrieved via D-ARX + D-GS lanes). Passes the standard 4-block DSL; `framework_candidate=false` — will be screened against IC1-IC6. |
| 11 | SegVol | excluded-with-logged-reason (pre-filter, recall stage) | Canonical arXiv:2311.13385 "SegVol: Universal and Interactive Volumetric Medical Image Segmentation" in dedup (R5832); fails the recall DSL's IC4 arm — the abstract names no organ-list term (speaks of "universal/volumetric" coverage; has3d ✓, hasCT ✓, hasOrgan ✗). Reason code: IC4 retrieval anchor. |
| 12 | clDice | excluded-with-logged-reason (criteria-consistent) | Canonical arXiv:2003.07311 / CVPR 2021 "clDice — A Novel Topology-Preserving Loss Function for Tubular Structure Segmentation" in dedup (R4522, retrieved via family A arXiv lane). Fails the recall DSL on BOTH IC3 (no CT/modality claim in title+abstract) and IC4/EC3 (tubular structures = vessels, an explicitly non-organ target class). This exclusion is semantically consistent with the review's method-paper criteria, though it removes a plan-listed family-A term from the screening pool; flagged for Limitations (Task 9/11). |

## Status summary

- In screening pool (awaiting the S2v2 3-vote run): 5 (MONAI, MONAI Label, VISTA-3D, nnInteractive, U-Mamba)
- Excluded-with-logged-reason: 4 (MedSAM, SAM-Med3D, SegVol, clDice)
- Not-indexed (zero-hit evidence + context): 2 (Auto3DSeg, NV-Segment-CT)
- BLOCKED: 1 (MONAI Deploy — query-layer window failure; PMID 39653370 / DOI 10.2196/55833 for Task 9 bib)

Zero silent losses: every absence above carries either a zero-hit query log
(PubMed/arXiv executed queries inline; S2 storm context recorded) or a
machine-derivable pipeline reason tied to a criterion code.

## Query-layer fix loop executed (revision r1, 2026-09-08)

1. `queries_v2.yaml`: family B += exact token `VISTA3D` (all four databases; ids → B-PUB-002 / B-ARX-002 / B-S2-002 / B-GS-002); family C arXiv id → C-ARX-002 (query text unchanged — API parse-flakiness resample). Validator green.
2. Targeted re-fetch via package fetchers (no EBSCO re-fire): B-PUB-002 = 999 rows, B-ARX-002 = 1,000 rows, C-ARX-002 = 893 rows, B-GS-002 = 10 rows (blocked: MaxTriesExceeded — informational), B-S2-002 = 0 rows (HTTP 500 — storm persists). Provenance rows appended to `raw/v2/_provenance.csv`.
3. `docdo fetch-v2 --concat` → `_combined.csv` 13,546 rows; `docdo deduplicate` → 8,161 rows; `v2_filter_and_funnel.py` re-run → `S2v2_elasticsearch_filtered.csv` 901 rows (464 standard + 437 bypass), checker green.
4. ES whitelist sync: `FRAMEWORK_TOOL_NAMES` += "VISTA3D" (same spelling defect as the yaml); `apply_exclusion_filters` now skips the EC3/strict-organ checks for **tool-name** framework matches only (definitionally framework papers; vocabulary-only matches remain under the method-paper anatomy criteria — pinned Task-3 behavior preserved). Tests: `operations/tests/test_fetch_v2.py` 41 passed (3 new lock-ins).

## arXiv id verification (plan-pinned ids, checked at execution)

| Plan id | Claimed seed | Actual content | Correct id |
|---------|--------------|----------------|------------|
| 2011.08506 | MONAI | Coupled spin-1/2 antiferromagnetic chain (physics) — WRONG | 2211.02701 (framework paper) |
| 2209.13545 | Auto3DSeg | The Proximal Map of the Weighted MAE — WRONG | none (technical documentation) |
| 2203.12345 | MONAI Label | Surface Patches with Rounded Corners — WRONG | 2203.12362 |
| 2406.05285 | VISTA-3D | VISTA3D: A Unified Segmentation Foundation Model — CORRECT | 2406.05285 (title unhyphenated) |
