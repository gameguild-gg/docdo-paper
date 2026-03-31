```markdown
# TODO.md — Final Reconciled Revision Plan (from 3 independent aggregations of 52 peer reviews)
Manuscript: **“3D Organ Segmentation from CT Scans”** (currently framed inconsistently as *systematic review* vs *AI-assisted/agentic structured survey*).

## How to read this TODO
- **Severity**: Critical / Major / Minor (publication-blocking vs substantial vs polish).
- **Confidence**: High / Medium / Low (agreement across all 3 runs).
- **Paper IDs**: listed **only when consistently cited across runs** (to avoid propagating run-specific noise).

---

## P0 — Publication-blocking (do first)

### M01 — Resolve article type and align PRISMA + claims
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.13300; 10.1002_mp.13438; 10.1002_mp.14386; 10.1002_mp.15507; 10.1109_ACCESS.2020.3024277; 10.1109_SPS.2019.8882073; arXiv_1809.04430; http___arxiv.org_abs_2309.13872v1
- **Problem:** Methods (AI-heavy screening + incomplete retrieval) do not support “systematic review” strength claims; scope reads abdomen-centric but claims broad CT organ segmentation.
- **Action items:**
  1. Choose **one** framing and implement consistently across title/abstract/methods/conclusions:
     - **Option A (AI-assisted structured/scoping survey):** keep PRISMA-*informed* reporting but **remove systematic-review-level completeness claims**.
     - **Option B (true systematic review):** upgrade methods per M02–M04 + Q03 and keep “systematic review” framing.
  2. Align scope statements (abdomen vs whole-body; surgery vs RT) and ensure tables/figures match the chosen scope.

---

### M02 — Fix screening validity (AI-only screening; “no consensus = exclude”)
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.12480; 10.1002_mp.13300; 10.1002_mp.13438; 10.1002_mp.13950; 10.1002_mp.14386; 10.1002_mp.14422; 10.1002_mp.15507; 10.1016_j.compmedimag.2018.03.001; 10.1016_j.imu.2020.100357; 10.1109_ACCESS.2020.3024277; 10.1109_SPS.2019.8882073; arXiv_1704.06382; arXiv_1809.04430; http___arxiv.org_abs_2302.00162v4; http___arxiv.org_abs_2309.13872v1
- **Problem:** LLM-only screening without human adjudication is viewed as non-standard and likely to cause false exclusions; “no consensus = exclude” is especially problematic.
- **Action items:**
  1. Replace rule with **“no consensus → human adjudication”** (and document it).
  2. Add **dual human screening** at least for:
     - all “uncertain/no-consensus” records, and
     - a **random stratified audit sample** of the remaining records.
  3. Report screening reliability: human–human and/or human–AI agreement; estimate **false exclusion risk** (recall/sensitivity).
  4. Release screening artifacts: prompts, model/version, dates, decision logs (supplement/repository).

---

### M03 — Address full-text retrieval rate and availability bias (63/161; 39.1%)
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.12480; 10.1002_mp.13300; 10.1002_mp.13438; 10.1002_mp.13950; 10.1002_mp.14386; 10.1002_mp.14422; 10.1002_mp.15507; 10.1016_j.compmedimag.2018.03.001; 10.1038_s41598-020-63285-0; 10.1038_s41598-022-07848-3; 10.1109_ACCESS.2020.3024277; 10.1109_SPS.2019.8882073; http___arxiv.org_abs_2309.13872v1
- **Problem:** Excluding studies due to PDF access creates strong availability/open-access bias; PRISMA flow needs clearer categories.
- **Action items:**
  1. Improve retrieval (institutional access, interlibrary loan, author contact).
  2. In PRISMA, separate **“eligible but inaccessible”** from “excluded for eligibility.”
  3. State explicitly whether **all included 52** had full text; if not, restrict quantitative extraction to full-text-only.
  4. Add sensitivity analysis: conclusions with/without inaccessible studies (or an “abstract-only evidence tier” clearly labeled).

---

### Q01 — Rebuild quantitative synthesis (Table VI) to avoid invalid cross-dataset ranking
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.12480; 10.1002_mp.13300; 10.1002_mp.13438; 10.1002_mp.13950; 10.1002_mp.14386; 10.1002_mp.14422; 10.1002_mp.15507; 10.1016_j.compmedimag.2018.03.001; 10.1016_j.imu.2020.100357; 10.1109_ACCESS.2020.3024277; 10.1109_SPS.2019.8882073; arXiv_1809.04430; http___arxiv.org_abs_2001.09647v1; http___arxiv.org_abs_2208.13271v1; http___arxiv.org_abs_2309.13872v1
- **Problem:** Current synthesis mixes datasets/tasks/splits/label sets and sources (“orig.” vs secondary), encouraging misleading “league table” conclusions.
- **Action items:**
  1. Replace Table VI with **dataset-/task-stratified tables** (e.g., BTCV, AMOS, FLARE, KiTS, MSD *by task*, TotalSegmentator, etc.).
  2. For each result row, add mandatory metadata:
     - dataset version + label set, split (official test vs CV), preprocessing/spacing, inference regime (whole/patch/cascade), TTA/ensemble, and **source type** (paper vs leaderboard vs re-implementation).
  3. Remove cross-dataset ranking language; label as **“reported results (non-comparable across datasets)”** unless harmonized.
  4. Where pooling is attempted, restrict to homogeneous strata and report study counts + dispersion/uncertainty.

---

### C01 — Recalibrate “deployment-ready” claims with explicit criteria and evidence tiers
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.12480; 10.1002_mp.13300; 10.1002_mp.13438; 10.1002_mp.14422; 10.1002_mp.15507; arXiv_1809.04430; arXiv_2406.13674
- **Problem:** Readiness is inferred mainly from mean Dice; reviewers want explicit operational criteria, external validation, QA/uncertainty, failure modes, and downstream endpoints.
- **Action items:**
  1. Define a **deployment-readiness rubric** (minimum evidence tiers), e.g.:
     - Tier 0: benchmark-only
     - Tier 1: external validation (multi-site/protocol)
     - Tier 2: workflow endpoints (editing time/acceptability)
     - Tier 3: downstream clinical endpoints (e.g., DVH/FLR/measurement reliability)
     - Tier 4: safety/QA (uncertainty, failure detection, missing-organ/hallucination)
  2. Map each “recommended” method/tool to tiers with citations.
  3. Rewrite conclusions to match the achieved tier(s); avoid Dice-only readiness statements.

---

### F01 — Correct factual/citation errors and make numeric claims reproducible
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1016_j.imu.2020.100357; 10.1002_mp.13950; 10.1002_mp.14422; 10.1109_TMI.2018.2806309; http___arxiv.org_abs_1909.06684v1; http___arxiv.org_abs_2208.13271v1; http___arxiv.org_abs_2302.00162v4
- **Problem:** Dataset facts/label sets and attributions are inconsistent (KiTS/MSD/BTCV/TotalSegmentator; “orig.” vs secondary; augmentation claims; “peer-reviewed” vs preprints; 52 vs 127 count mismatch).
- **Action items:**
  1. Create a **versioned dataset fact sheet** (labels, splits, tasks) and reference it consistently.
  2. Audit every numeric claim in abstract/tables: add explicit citation + where it appears (table/figure/leaderboard) + protocol context.
  3. Fix dataset-specific issues repeatedly flagged:
     - **MSD**: report **per task**, not as one dataset number.
     - **KiTS**: separate kidney vs tumor metrics; correct dataset description.
     - **BTCV/“13 organs”**: clarify that “13 organs” differs across datasets/label sets.
     - **TotalSegmentator**: specify version and organ count consistently.
  4. Remove or correct unverified universal statements (e.g., augmentation ranges, “universal mirroring”).

---

## P1 — High-impact completeness (major content gaps)

### T01 — Expand taxonomy beyond architecture families
- **Severity:** Major  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.12480; 10.1002_mp.13300; 10.1002_mp.13438; 10.1002_mp.13950; 10.1002_mp.14386; 10.1007_978-3-030-00937-3_49; 10.1016_j.compmedimag.2018.03.001; http___arxiv.org_abs_1909.07480v2; http___arxiv.org_abs_2302.00162v4
- **Problem:** CNN/Transformer/Hybrid/Foundation is too coarse for deployment guidance.
- **Action items:**
  1. Keep architecture taxonomy but add orthogonal axes:
     - input dimensionality (2D/2.5D/3D), inference regime (whole/patch/cascade), supervision regime, target type (parenchymal/hollow/vascular/OAR/lesion), modality/protocol (SECT/DECT; phase), QA/uncertainty, ensemble vs single, continual learning.
  2. Add a supplementary **Included Studies Master Table** mapping each included paper to these axes.

---

### D01 — Add (or explicitly scope out) radiotherapy (RT) OAR segmentation + endpoints
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.13300; 10.1002_mp.14386; 10.1002_mp.15507; 10.1088_1361-6560_aaf11c; 10.1186_s13014-022-01985-9; arXiv_1809.04430
- **Problem:** RT is a major CT deployment domain; missing OAR datasets, acceptability/editing time, DICOM-RT context, and dosimetric endpoints.
- **Action items:**
  1. Add a dedicated RT section (HN/pelvis/thorax as appropriate to scope).
  2. Include RT-relevant metrics (surface/tolerance-based) and downstream endpoints (DVH/plan impact) where available.
  3. If RT is out-of-scope, state this explicitly and remove/limit RT-adjacent readiness claims.

---

### D02 — Add thorax/lung and thoracic OAR benchmarks
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1109_ACCESS.2020.3024277; 10.1109_ICIEAM48468.2020.9111950; 10.1109_SPS.2019.8882073; arXiv_1908.00360
- **Problem:** Abdomen-centric coverage omits major thoracic segmentation settings and small tubular organs (e.g., esophagus/trachea).
- **Action items:**
  1. Add thoracic benchmarks/challenges and typical failure modes (small/tubular structures).
  2. Stratify evaluation discussion for tubular organs (surface metrics, localization/cascades).

---

### D03 — Add DECT/spectral CT (PMI/VMI/iodine maps) and protocol-driven domain shift
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.13950; 10.1038_s41598-019-40584-9; http___arxiv.org_abs_1710.05379v1
- **Problem:** DECT/spectral CT is absent; HU “consistency” claims are oversimplified.
- **Action items:**
  1. Add DECT/spectral subsection: inputs (low/high kV, VMI/iodine maps), fusion strategies (early/feature/late), robustness implications.
  2. Treat protocol/energy as a first-class domain-shift axis in taxonomy and synthesis.

---

### D04 — Include 2D/2.5D multi-view fusion (or justify exclusion)
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.12480; 10.1002_mp.13438
- **Problem:** Excluding 2D-only approaches misses clinically practical 2.5D/multi-view fusion under memory/anisotropy constraints.
- **Action items:**
  1. Define “in-scope” as **3D-context** segmentation (including 2.5D/multi-view fusion with explicit 3D fusion/voting).
  2. Add a subsection comparing 2.5D vs 3D under deployment constraints (VRAM, anisotropy).
  3. If still excluded, explicitly limit deployment claims accordingly.

---

### D05 — Add cascades/coarse-to-fine and memory-efficient pipelines
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1016_j.compmedimag.2018.03.001; arXiv_1704.06382; http___arxiv.org_abs_1909.07480v2; 10.1109_WRCSARA57040.2022.9903976
- **Problem:** Missing two-stage localization→segmentation pipelines and practical memory-efficient strategies; reviewers want error-propagation discussion.
- **Action items:**
  1. Add section on cascades/ROI localization, candidate-region recall vs precision, and failure propagation.
  2. Integrate compute constraints (patching, tiling, overlap) into taxonomy and evidence tables.

---

### L01 — Add weak/partial/semi/self/interactive supervision and annotation-cost axis
- **Severity:** Critical  
- **Confidence:** High  
- **Consistently cited IDs:** http___arxiv.org_abs_2105.14314v3; http___arxiv.org_abs_2203.01934v1; http___arxiv.org_abs_2009.09571v4; http___arxiv.org_abs_2309.09730; 10.1088_1361-6560_ab6f99
- **Problem:** Review discusses annotation trade-offs but undercovers weak/partial labels, semi/self-supervision, and interactive refinement.
- **Action items:**
  1. Add supervision-regime taxonomy and synthesize evidence by regime (full vs partial vs weak vs semi/self vs interactive).
  2. Include missing-label learning strategies (masked losses) and pseudo-label failure modes.
  3. Where available, extract annotation time/effort and “time-to-correct” endpoints.

---

### Q02 — Expand evaluation beyond mean Dice (surface tolerances, failures, QA/uncertainty)
- **Severity:** Major  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.12480; 10.1002_mp.13300; 10.1002_mp.13438; 10.1002_mp.14422; 10.1002_mp.15507; arXiv_2406.13674; http___arxiv.org_abs_2309.13872v1
- **Problem:** Dice-centric evaluation misses clinically relevant errors and safety failures; NSD tolerances treated too generically.
- **Action items:**
  1. Add “metrics-for-deployment” section:
     - organ-wise performance + dispersion/outliers,
     - surface metrics (HD95/ASSD/NSD) with **organ/application-specific tolerances**,
     - laterality swaps, topology/connectivity issues (esp. tubular structures),
     - uncertainty/calibration and QA triggers.
  2. Avoid universal tolerance claims; cite application-specific tolerance frameworks where used.

---

### Q03 — Replace coarse quality rubric with segmentation-specific risk-of-bias / evidence grading
- **Severity:** Major  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.12480; 10.1002_mp.13300; 10.1002_mp.13438; 10.1002_mp.13950; 10.1002_mp.14386; 10.1002_mp.14422; 10.1002_mp.15507; 10.1186_s41747-024-00507-4; 10.3389_fonc.2018.00215
- **Problem:** Current 4-binary QA is too coarse; not used in synthesis; no per-study reporting or sensitivity analyses.
- **Action items:**
  1. Implement a segmentation-tailored RoB tool (adapt CLAIM/TRIPOD-AI/QUADAS-2 concepts):
     - split integrity/leakage, annotation protocol & interobserver variability, label definition clarity, external validation, post-processing tuned on test, uncertainty reporting, reproducibility artifacts.
  2. Publish per-study RoB table and use it to grade certainty and run sensitivity analyses.

---

## P2 — Strengthening credibility, robustness, and reporting

### E01 — Standardize compute/efficiency reporting (runtime, VRAM, hardware, inference regime)
- **Severity:** Major  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1016_j.compmedimag.2018.03.001; 10.1109_WRCSARA57040.2022.9903976; http___arxiv.org_abs_1909.07480v2
- **Action items:**
  1. Add an efficiency extraction table: hardware, VRAM peak, patch size/spacing, throughput, end-to-end latency (incl. pre/post), cascade/TTA/ensemble conditions.
  2. Remove unconditioned runtime claims if not supported.

---

### COI01 — Strengthen COI mitigation and transparency (DocDo affiliation)
- **Severity:** Major  
- **Confidence:** High  
- **Consistently cited IDs:** 10.1002_mp.12480; 10.1002_mp.13300; 10.1002_mp.14386; 10.1109_ACCESS.2020.3024277; http___arxiv.org_abs_2302.00162v4
- **Action items:**
  1. Add independent audit of screening/extraction (or audited subset) by non-affiliated reviewer(s).
  2. Provide evidence-to-recommendation mapping table separating evidence synthesis from engineering/product perspective.
  3. Release full artifacts (search strings, logs, extraction sheets) in a DOI-stamped repository.

---

## Conflicts / partial agreement items (include with caution)

### M04 — Public-benchmark-only vs inclusion of private clinical studies
- **Severity:** Critical  
- **Confidence:** Medium (agreement on *problem*, differing preferred remedy)
- **Consistently cited IDs:** 10.1002_mp.13950; 10.1002_mp.14422; 10.1002_mp.15507
- **Issue:** Benchmark-only inclusion improves comparability but undermines “deployment readiness” evidence.
- **Recommended resolution (balanced):**
  - Maintain **two evidence streams**:
    1) benchmark-comparable evidence (public datasets/leaderboards), and  
    2) clinical/private-cohort evidence (external validation, workflow endpoints), graded separately with stricter RoB.

### D06 — Post-surgical anatomy / missing organs / hallucination (RAOS)
- **Severity:** Critical  
- **Confidence:** Medium (present in runs 1 & 3; run 2 includes it but less structurally)
- **Consistently cited IDs:** arXiv_2406.13674
- **Action items:**
  - Add safety subsection on missing-organ/resection scenarios; propose presence/absence metrics and QA/abstention logic.
  - Clearly state that Dice alone cannot detect hallucinated organs.

### R01 — Robustness evaluation taxonomy (corruptions/adversarial augmentation) and “degradation” effect sizes
- **Severity:** Major  
- **Confidence:** Medium (runs 2–3 explicit; run 1 partially via safety/robustness)
- **Consistently cited IDs:** http___arxiv.org_abs_2302.13172v1
- **Action items:**
  - Define “degradation” precisely (absolute vs relative drop; organs; conditions).
  - Add corruption/protocol/anatomy shift stratification; avoid unsupported percentage claims.

### S08/D07 — Boundary-aware / shape priors / level-set hybrids
- **Severity:** Major  
- **Confidence:** Medium (strong in runs 2–3; present in run 1)
- **Consistently cited IDs:** http___arxiv.org_abs_2210.04285v1; 10.1109_cvidliccea56201.2022.9823971
- **Action items:**
  - Add a boundary/shape-prior subsection and connect it to surface metrics and small-structure performance.

### S11/D08 — Ensembles and calibration
- **Severity:** Major  
- **Confidence:** Medium (runs 1–3 include; emphasis varies)
- **Consistently cited IDs:** http___arxiv.org_abs_2001.09647v1; http___arxiv.org_abs_2309.13872v1
- **Action items:**
  - Add ensemble strategies (trainable/non-trainable), calibration, and reporting standards.

### S10/D06 — Continual learning / partial-label conflict
- **Severity:** Major  
- **Confidence:** Medium (runs 2–3; run 1 includes as critical but narrower)
- **Consistently cited IDs:** http___arxiv.org_abs_2302.00162v4
- **Action items:**
  - Add continual learning axis: catastrophic forgetting, background-label conflict, evaluation protocols.

### D05/S12 — Hollow organs (bowel/colon/duodenum)
- **Severity:** Major  
- **Confidence:** Medium (runs 1–3 include; details vary)
- **Consistently cited IDs:** 10.1002_mp.14386; 10.1038_s41598-020-63285-0; http___arxiv.org_abs_2309.13872v1
- **Action items:**
  - Add hollow-organ subsection; emphasize label ambiguity/topology and realistic performance expectations.

---

## Final ordered checklist (authors can paste into issue tracker)

### P0 (Critical)
- [ ] **M01** Decide review type (systematic vs AI-assisted survey) and align title/claims/PRISMA usage. *(High)*
- [ ] **M02** Replace “no consensus = exclude” with human adjudication; add dual human screening or validated audit; publish logs. *(High)*
- [ ] **M03** Fix availability bias: improve retrieval; PRISMA “eligible but inaccessible”; sensitivity analysis. *(High)*
- [ ] **Q01** Redesign quantitative synthesis into dataset-/task-stratified tables with protocol metadata; remove cross-dataset ranking. *(High)*
- [ ] **C01** Replace Dice-only “deployment-ready” claims with explicit rubric + evidence tiers; rewrite conclusions. *(High)*
- [ ] **F01** Audit and correct dataset facts, label sets, counts, and numeric attributions; create dataset fact sheet. *(High)*

### P1 (Major/Critical)
- [ ] **T01** Expand taxonomy to multi-axis (pipeline, supervision, modality/protocol, target type, QA). *(High)*
- [ ] **D01** Add RT OAR section + endpoints (or explicitly scope out and adjust claims). *(High)*
- [ ] **D02** Add thorax/lung/thoracic OAR coverage. *(High)*
- [ ] **D03** Add DECT/spectral CT coverage and protocol-driven domain shift. *(High)*
- [ ] **D04** Add 2D/2.5D multi-view fusion discussion (or justify exclusion). *(High)*
- [ ] **D05** Add cascades/coarse-to-fine and memory-efficient pipelines. *(High)*
- [ ] **L01** Add weak/partial/semi/self/interactive supervision + annotation-cost synthesis. *(High)*
- [ ] **Q02** Expand metrics beyond Dice (surface tolerances, failures, QA/uncertainty). *(High)*

### P2 (Major; credibility/polish)
- [ ] **Q03** Implement segmentation-specific risk-of-bias tool; publish per-study table; sensitivity analyses. *(High)*
- [ ] **E01** Standardize compute reporting (VRAM/runtime/hardware; inference regime). *(High)*
- [ ] **COI01** Add COI safeguards: independent audit + evidence-to-recommendation mapping + public artifacts. *(High)*
- [ ] **(Optional, Medium confidence)** Add RAOS/missing-organ hallucination safety evaluation; robustness taxonomy; boundary/shape priors; ensembles; continual learning; hollow organs. *(Medium)*

---
```