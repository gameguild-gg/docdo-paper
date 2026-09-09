# S2v2 Seed Recall Oracle — Task 6 (paper-coverage-gap-update)

**Generated:** 2026-09-08 (remediation r2 same day)
**Binding spec:** `.omo/plans/paper-coverage-gap-update.md` Task 6 (recall oracle).
**Input artifacts:** `interim/S1v2_search_results_deduplicated.csv` (8,846 rows),
`pipeline_outputs/S2v2_elasticsearch_filtered.csv` (1,101 rows = 641 standard + 460 bypass).

Each seed reaches exactly one of INCLUDE / excluded-with-logged-reason /
not-indexed. Seeds marked *in screening pool* have satisfied the
identification and pre-filter stages; their INCLUDE/EXCLUDE decision belongs
to the S2v2 3-vote screening run, which is currently blocked on the missing
`OPENAI_API_KEY` (see `S2v2_screening_log.md`).

## Seed table (12 rows)

| # | Seed | Status | Evidence |
|---|------|--------|----------|
| 1 | MONAI | in screening pool (R5748, bypass lane) | arXiv:2211.02701 "MONAI: An open-source framework for deep learning in healthcare" (Cardoso et al. 2022 — the MONAI framework paper), `framework_candidate=true`. The title variant "MONAI: Medical Open Network for AI" is NOT indexed: PubMed exact-title 0 hits, arXiv 0 hits (2026-09-08). **Plan's pinned id arXiv:2011.08506 is WRONG** — verified to resolve to an unrelated physics paper ("Coupled spin-1/2 antiferromagnetic chain Cs2LiRuCl6..."); do not use it for inbox naming. |
| 2 | Auto3DSeg | **not-indexed** | No canonical peer-reviewed paper exists. Zero-hit log: PubMed `"Auto3DSeg: A Large-Scale Benchmark and Comprehensive Evaluation of 3D Medical Image Segmentation"[ti]` = 0; PubMed `Auto3DSeg[tiab]` = 9 hits, ALL application papers (none canonical — verified 2026-09-08); arXiv `ti:"Auto3DSeg"` = 3 hits, all applications; arXiv `abs:"Medical Open Network for AI"`-class title probes = 0. Semantic Scholar lane blocked (control probe HTTP 429 at both spaced retries, 2026-09-08 — storm context in `S1v2_evidence_report.md`). The citable artifact is Project-MONAI Auto3DSeg technical documentation (tutorials/Zenodo). **Plan's pinned id arXiv:2209.13545 is WRONG** — resolves to "The Proximal Map of the Weighted Mean Absolute Error"; do not use it. Bib coverage: Task 9 @techreport (plan-sanctioned path, NV-Segment-CT precedent). |
| 3 | MONAI Label | in screening pool (R5579, bypass lane) | arXiv:2203.12362 "MONAI Label: A framework for AI-assisted Interactive Labeling of 3D Medical Images", `framework_candidate=true`. **Plan's pinned id arXiv:2203.12345 is WRONG** — resolves to "Surface Patches with Rounded Corners"; the correct id is 2203.12362 (verified by direct arXiv id_list fetch + title match). |
| 4 | MONAI Deploy | in screening pool (R1754, bypass lane) | arXiv: not present (title probes 0). Originally recorded BLOCKED (query-window failure); **recovered by the r2 PMID-direct remediation**: `fetch_pubmed_by_pmids` efetch of PMID 39653370 → `raw/v2/B-PUB-002-pmid.csv` → dedup R1754, `framework_candidate=true` (abstract contains the MONAI tool token), DOI 10.2196/55833. Root cause was never a query-term defect: PubMed's default esearch id ordering is date-descending under datetype filters, so the 1,000-cap window for family B (20,929 matches) contained only 2026-era records (997/999 in B-PUB-001). The relevance-sort option (`fetch_pubmed_v2(sort=...)`) now exists for supplementary windows; the PMID-direct helper covers known-id recovery. |
| 5 | VISTA-3D | in screening pool (R6540, bypass lane) | arXiv:2406.05285 — **pinned id VERIFIED CORRECT**, but the title is "VISTA3D: A Unified Segmentation Foundation Model For 3D Medical Imaging" (unhyphenated). The hyphenated family-B term "VISTA-3D" could not match it in any fielded index (root cause of the original miss). Fixed by the Task-6 query-layer fix loop: `queries_v2.yaml` revision r1 adds the exact token VISTA3D to family B (query ids B-*-002); re-fetched via B-ARX-002; ES whitelist synced (`FRAMEWORK_TOOL_NAMES` += "VISTA3D"); tool-name anatomy-check guard added so framework tool papers reach the bypass lane. `framework_candidate=true`. |
| 6 | NV-Segment-CT | **not-indexed** | Zero-hit log (2026-09-08): PubMed `"NV-Segment-CT"[tiab] OR "NV Segment CT"[tiab]` = 0; arXiv `all:"NV-Segment-CT"` = 0; Semantic Scholar blocked (control probe 429, both retry rounds — recorded as evidence context per plan scoping; the S2 zero-hit is therefore unverified, not contradicted). Consistent with the plan's pre-declaration: NV-Segment-CT is industry technical documentation that PubMed/arXiv/S2 do not index; bib coverage via Task 9 @techreport satisfies the success criterion without S2 inclusion. |
| 7 | nnInteractive | in screening pool (R5695, bypass lane) | arXiv:2503.08373 "nnInteractive: Redefining 3D Promptable Segmentation", `framework_candidate=true`. Originally dropped by the pre-filter's method-paper anatomy checks ("Bone/skeletal only" — abstract mentions spine/vertebrae targets, no organ-list term); restored by the Task-6 tool-name anatomy-check guard. |
| 8 | MedSAM | excluded-with-logged-reason (pre-filter, recall stage) | Canonical "Segment Anything in Medical Images" IS identified — in dedup as the Google Scholar row R0154 (title-exact; GS hits process normally per plan scoping) — but fails the recall DSL on the GS snippet: the two-sentence snippet carries no IC1 deep-learning anchor term (machine reason: recall miss, IC1). The arXiv copy (2304.12306, verified) is additionally buried below the relevance window of both C-ARX samples (893-row stable parse; not in any top-100 page of either -001/-002 fetch; informational retrieval limitation). Reason code: IC1 retrieval anchor. |
| 9 | SAM-Med3D | excluded-with-logged-reason (pinned-template scope) | Canonical arXiv:2310.15161 "SAM-Med3D: Towards General-purpose Segmentation Models for Volumetric Medical Images" is indexed (arXiv `ti:"SAM-Med3D"` rank 1; S2 total=3365 with canonical in top-3, confirmed via a storm-window slip-through on 2026-09-08) but is structurally unreachable by family C's pinned conjunction template: the canonical abstract contains ZERO family-F anatomy/CT tokens (verified token-by-token: no liver/kidney/.../CT), so `(family-C terms) AND (segmentation) AND (F anatomy)` cannot match it. One fix loop executed (C-ARX-002 resample; query text unchanged) — confirmed the 893-row parse is stable and the miss is template-inherent, not API flakiness. No minimal term addition legitimately surfaces an abstract with no anatomy anchor (the anchor IS the review's CT-organ scope). Reason code: IC3/IC4 retrieval anchor (family F). Flagged for Limitations (Task 9/11): general-purpose foundation models that omit CT/organ terms in the abstract are invisible to the pinned template. |
| 10 | U-Mamba | in screening pool (R7244, standard lane) | arXiv:2401.04722 "U-Mamba: Enhancing Long-range Dependency for Biomedical Image Segmentation" (correct canonical id established at execution; retrieved via D-ARX + D-GS lanes). Passes the standard 4-block DSL; `framework_candidate=false` — will be screened against IC1-IC6. |
| 11 | SegVol | excluded-with-logged-reason (pre-filter, recall stage) | Canonical arXiv:2311.13385 "SegVol: Universal and Interactive Volumetric Medical Image Segmentation" in dedup (R6563); fails the recall DSL's IC4 arm — the abstract names no organ-list term (speaks of "universal/volumetric" coverage; has3d ✓, hasCT ✓, hasOrgan ✗). Reason code: IC4 retrieval anchor. |
| 12 | clDice | excluded-with-logged-reason (criteria-consistent) | Canonical arXiv:2003.07311 / CVPR 2021 "clDice — A Novel Topology-Preserving Loss Function for Tubular Structure Segmentation" in dedup (R5254, retrieved via family A arXiv lane). Fails the recall DSL on BOTH IC3 (no CT/modality claim in title+abstract) and IC4/EC3 (tubular structures = vessels, an explicitly non-organ target class). This exclusion is semantically consistent with the review's method-paper criteria, though it removes a plan-listed family-A term from the screening pool; flagged for Limitations (Task 9/11). |

## Status summary

- In screening pool (awaiting the S2v2 3-vote run): 6 (MONAI, MONAI Label, MONAI Deploy, VISTA-3D, nnInteractive, U-Mamba)
- Excluded-with-logged-reason: 4 (MedSAM, SAM-Med3D, SegVol, clDice)
- Not-indexed (zero-hit evidence + context): 2 (Auto3DSeg, NV-Segment-CT)
- BLOCKED: 0 (MONAI Deploy recovered via r2 PMID-direct fetch)

Zero silent losses: every absence above carries either a zero-hit query log
(PubMed/arXiv executed queries inline; S2 storm context recorded) or a
machine-derivable pipeline reason tied to a criterion code.

## Query-layer fix loop executed (revision r1, 2026-09-08)

1. `queries_v2.yaml`: family B += exact token `VISTA3D` (all four databases; ids → B-PUB-002 / B-ARX-002 / B-S2-002 / B-GS-002); family C arXiv id → C-ARX-002 (query text unchanged — API parse-flakiness resample). Validator green.
2. Targeted re-fetch via package fetchers (no EBSCO re-fire): B-PUB-002 = 999 rows, B-ARX-002 = 1,000 rows, C-ARX-002 = 893 rows, B-GS-002 = 10 rows (blocked: MaxTriesExceeded — informational), B-S2-002 = 0 rows (HTTP 500 — storm persists). Provenance rows appended to `raw/v2/_provenance.csv`.
3. `docdo fetch-v2 --concat` → `_combined.csv` 13,546 rows; `docdo deduplicate` → 8,161 rows; `v2_filter_and_funnel.py` re-run → `S2v2_elasticsearch_filtered.csv` 901 rows (464 standard + 437 bypass), checker green.
4. ES whitelist sync: `FRAMEWORK_TOOL_NAMES` += "VISTA3D" (same spelling defect as the yaml); `apply_exclusion_filters` now skips the EC3/strict-organ checks for **tool-name** framework matches only (definitionally framework papers; vocabulary-only matches remain under the method-paper anatomy criteria — pinned Task-3 behavior preserved). Tests: `operations/tests/test_fetch_v2.py` 41 passed (3 new lock-ins).

## Remediation r2 (2026-09-08, key-free continuation)

1. `fetch_v2_fetchers.py`: `fetch_pubmed_v2(sort=...)` (relevance window option) + `fetch_pubmed_by_pmids()` (direct efetch). Red-first tests; suite 196 green.
2. `B-PUB-002-pmid`: PMID 39653370 fetched directly → 1 row (DOI 10.2196/55833) → dedup R1754, bypass lane (MONAI tool token in abstract). MONAI Deploy: BLOCKED → in screening pool.
3. `G-PUB-002-r`: one relevance-sorted family-G refetch (1,000 rows; year spread 2019-2026 vs the 2026-dominated default window) — **recovered 7 of the 26 v1-missed studies** (abdomen/pelvis U-Net variant, 3D-patch multi-organ, 3D self-attention U-Net, DECT multi-organ, interactive 3D U-Net pancreas, pancreas volumetry DNN, kidney+renal-mass); v1 retention 26/52 → 32/52.
4. Downstream: concat 14,547 → dedup 8,846 → pool **1,101 rows** (641 standard + 460 bypass), checker green.
5. `queries_v2.yaml` revision r2 + `supplementary_queries` section (documented one-shot fetches; validator green unweakened).

## arXiv id verification (plan-pinned ids, checked at execution)

| Plan id | Claimed seed | Actual content | Correct id |
|---------|--------------|----------------|------------|
| 2011.08506 | MONAI | Coupled spin-1/2 antiferromagnetic chain (physics) — WRONG | 2211.02701 (framework paper) |
| 2209.13545 | Auto3DSeg | The Proximal Map of the Weighted MAE — WRONG | none (technical documentation) |
| 2203.12345 | MONAI Label | Surface Patches with Rounded Corners — WRONG | 2203.12362 |
| 2406.05285 | VISTA-3D | VISTA3D: A Unified Segmentation Foundation Model — CORRECT | 2406.05285 (title unhyphenated) |
