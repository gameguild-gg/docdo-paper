# PRISMA 2020 Compliance Analysis — Current State of main.tex

**Paper:** _3D Organ Segmentation from CT Scans: An Agentic Structured Survey of Deep Learning Approaches for Surgical Planning_

**Original Analysis Date:** March 13, 2026
**Last Compliance Update:** March 15, 2026
**Current Audit Date:** April 20, 2026
**Last Fix Applied:** April 20, 2026 — S-numbering reconciled, quality distribution corrected (10/41/1), code availability corrected (13/52 = 25.0%)

**Context:** This analysis now reflects the **current state of `main.tex`**, which has incorporated the vast majority of PRISMA improvements that were previously only in `main_prisma-compliance.tex`. The prior two-column comparison (main.tex vs compliance.tex) is superseded by this single-column assessment of the merged paper.

**Important context:** This paper is a **structured survey**, not a formal systematic review. It was not prospectively registered, does not perform meta-analysis, and honestly acknowledges this throughout. PRISMA 2020 was designed for systematic reviews and meta-analyses. Some items are structurally impossible to fully meet for a structured survey, and forcing compliance would be dishonest. This analysis is transparent about that.

---

## Summary Scorecard

|                  | main.tex (March 2026) | main.tex (April 20, 2026 — after fixes) |
|------------------|-----------------------|------------------------------------------|
| Fully Met        | 15                    | **29**                                   |
| Partially Met    | 14                    | **10**                                   |
| Not Met          | 10                    | **0**                                    |
| **Total**        | **39**                | **39**                                   |

_All 10 items previously "Not Met" have been resolved — either incorporated into main.tex or correctly classified as Partially Met due to structural constraints. No items remain at Not Met. Three data-accuracy issues (S-numbering, quality distribution, code availability) were corrected in this session._

---

## PRISMA Item-by-Item Assessment — Current main.tex

### TITLE

| # | Requirement | Current main.tex | Analysis |
|---|-------------|-----------------|----------|
| 1 | Identify as systematic review | **Partially Met** | Uses "Agentic Structured Survey." Correct and honest — the paper is not a systematic review and should not claim to be one. **Permanently Partially Met without misrepresentation.** |

### ABSTRACT

| # | Requirement | Current main.tex | Analysis |
|---|-------------|-----------------|----------|
| 2 | PRISMA for Abstracts structured format | **Fully Met** | Abstract now has all required PRISMA headings: Background, Objectives, Data Sources, Eligibility, Synthesis, Results, Limitations, Conclusions, Registration. Content reorganized from existing paper material. |

### INTRODUCTION

| # | Requirement | Current main.tex | Analysis |
|---|-------------|-----------------|----------|
| 3 | Rationale | **Fully Met** | Thorough rationale across Sections 1, 1.2, 1.3, 1.5. |
| 4 | Objectives | **Fully Met** | Four explicit RQs (RQ1–RQ4). |

### METHODS

| # | Requirement | Current main.tex | Analysis |
|---|-------------|-----------------|----------|
| 5 | Eligibility criteria | **Fully Met** | Explicit inclusion and exclusion criteria lists in §2.3. |
| 6 | Information sources | **Fully Met** | Five databases named with date range (Nov 15, 2025–Jan 10, 2026). |
| 7 | Search strategy | **Partially Met** | PubMed query shown inline as "illustrative example." Complete queries for all five databases deferred to Supplementary S3. Four of five database queries remain outside the paper body. To upgrade: add all five queries inline or in an appendix table. |
| 8 | Selection process | **Fully Met** | Two-stage selection (Elasticsearch + AI consensus) described in detail with assessor count, independence, and automation tools. |
| 9 | Data collection process | **Fully Met** | Two named reviewers (A.T.N., M.H.R.M.); "Study authors were not contacted for missing or unclear data; extraction relied solely on published information." Standardized form referenced (Supplementary S7). |
| 10a | Data items — outcomes | **Fully Met** | "All compatible results were sought for each outcome domain." Explicitly states "the single-model result without TTA was recorded as the primary outcome." |
| 10b | Data items — other variables | **Fully Met** | Fields not reported recorded as "not reported." "No imputation of missing values was performed." |
| 11 | Risk of bias assessment | **Fully Met** | Two named reviewers; standard tools' inapplicability justified; custom three-dimension numerical framework described; declaration sentence present: "This three-dimension numerical framework constitutes the study-level quality assessment instrument used in this review, applied in place of standard risk-of-bias tools (ROBINS-I, Cochrane RoB 2) that are designed for clinical study designs not applicable to computational benchmarking." |
| 12 | Effect measures | **Fully Met** | Dedicated "Effect Measures" subsection explains why Dice/HD95 replace traditional effect measures with explicit justification. |
| 13a | Synthesis — eligibility | **Fully Met** | Explicit criteria for benchmark inclusion (e.g., "BTCV: standard 30-train/20-test split with 13 organs"). |
| 13b | Synthesis — data preparation | **Fully Met** | "Performance values were extracted as reported in original publications without conversion or transformation." "No summary statistics were imputed or estimated from figures." |
| 13c | Synthesis — display | **Fully Met** | Explicitly justifies absence of forest plots: "heterogeneity in evaluation protocols, preprocessing pipelines, and training configurations across studies precluded meaningful statistical pooling." |
| 13d | Synthesis — rationale | **Fully Met** | Three numbered reasons for narrative synthesis. |
| 13e | Synthesis — heterogeneity exploration | **Fully Met** | Stratification approach described; explicitly states "No formal subgroup analysis or meta-regression was conducted due to the absence of pooled effect estimates." |
| 13f | Sensitivity analyses | **Fully Met** | "one post-hoc sensitivity analysis (not pre-specified in the review protocol)." Honest framing. |
| 14 | Reporting bias assessment | **Fully Met** | Dedicated "Reporting Bias Assessment" subsection. Explains why funnel plots/Egger's test were not feasible. Three qualitative bias sources identified. |
| 15 | Certainty assessment | **Fully Met** | Dedicated "Certainty Assessment" subsection. States GRADE not applied and why; qualitative alternative described. |

### RESULTS

| # | Requirement | Current main.tex | Analysis |
|---|-------------|-----------------|----------|
| 16a | Study selection — flow | **Fully Met** | PRISMA 2020 flow diagram (Figure 1) with numbers at every stage. |
| 16b | Excluded studies cited | **Partially Met** | Names Nikolov et al. and Han et al. with individual justifications; also names two category-level exclusions (2D-only: n=2; private datasets: n=3). References S5 for complete list: "Complete full-text screening decisions with individual exclusion reasons for all assessed studies are provided in Supplementary S5 (S5_screening_decisions.csv)." The S5 reference was the identified fix — it is applied. Still Partially Met because PRISMA asks to cite each excluded study; category-level counts and supplementary reference satisfy the spirit but not the letter. |
| 17 | Study characteristics | **Partially Met** | ✅ **S-numbering fixed (April 20, 2026):** All three references now consistently say "Supplementary Table S2" (`S2_included_studies.csv`, 52 studies). `S1_search_results_REAL.csv` contains raw search results and is explicitly documented as not directly cited. Remains Partially Met because S2 captures screening-phase metadata and may require augmentation with synthesis-phase characteristics for full PRISMA Item 17 compliance. |
| 18 | Risk of bias in studies | **Partially Met** | ✅ **Numbers corrected (April 20, 2026):** Updated from 13/38/1 to **10 (19.2%) high / 41 (78.8%) moderate / 1 (1.9%) low** (thresholds: High ≥24, Moderate 16–23, Low ≤15; total 0–30). Source: prior audit of `qa_summary_20260123_075645.csv` (not in repo; generated by QA pipeline). Code availability also corrected to 25.0% (13/52) — see Item 27 note. Per-study ratings in Supplementary Table S2 (reference now consistent). |
| 19 | Individual study results | **Partially Met** | ✅ **S-reference fixed.** Per-study data in "Supplementary Table S2" (consistent across paper). Precision measures absent from inline tables; 35/52 (67.3%) reported SDs or CIs; 16/52 (30.8%) reported formal CIs. Most ML papers don't report CIs for Dice — honest source-literature limitation. |
| 20a | Synthesis — characteristics + RoB | **Partially Met** | Corrected quality distribution among contributing studies (26 studies): **high 19% / moderate 81%** — matches the audit correction. But presentation is aggregate, not per-synthesis-table. |
| 20b | Statistical results | **Fully Met** | Explicit clarification: "These aggregate statistics (85.2±2.1% and 80.5±1.8%) are arithmetic means ± standard deviations computed from reported values across contributing studies, not pooled meta-analytic estimates." |
| 20c | Heterogeneity results | **Partially Met** | Dedicated "Heterogeneity Investigation Results" subsection with stratification findings (4.7-pt CNN/Transformer gap, pre-training effects, organ complexity spread). Correctly states no formal subgroup analysis or meta-regression. Structural limit: no pooled estimates → formal heterogeneity statistics do not exist. **Permanently Partially Met.** |
| 20d | Sensitivity analysis results | **Partially Met** | Fabricated 84.8±2.3% figure removed. Now reports directional consistency and quality-subset statistic (34.5% high quality in DOI subset vs 25.0% overall). No verifiable mean Dice for the 29-study subset (only 7/29 have numeric overall_dice in synthesis CSV). Partially Met — honest maximum given the data. |
| 21 | Reporting biases | **Fully Met** | Dedicated "Reporting Bias Results" subsection. Three bias sources identified. ⚠️ NOTE: The paper now states "39 of 52 studies (75.0%) fully reported per-organ results" (up from a previously stated 32/52 = 61.5%). Neither figure has a dedicated field in repository data — treat as an estimate from the original extraction review. |
| 22 | Certainty of evidence | **Fully Met** | "Certainty of Evidence" subsection with high/moderate/low confidence by finding category. Appropriate qualitative approach when GRADE doesn't apply. |

### DISCUSSION

| # | Requirement | Current main.tex | Analysis |
|---|-------------|-----------------|----------|
| 23a | General interpretation | **Fully Met** | Thorough discussion addressing all four RQs. |
| 23b | Limitations of evidence | **Fully Met** | Detailed limitations section covering internal, external, construct, temporal, and methodological validity. |
| 23c | Limitations of review processes | **Fully Met** | English-only search, publication bias, availability bias, and other process limitations stated. |
| 23d | Implications | **Fully Met** | Phased adoption strategy and future research priorities stated. |

### OTHER INFORMATION

| # | Requirement | Current main.tex | Analysis |
|---|-------------|-----------------|----------|
| 24a | Registration | **Partially Met** | Declarations section: "This review was not prospectively registered in PROSPERO or other systematic review registries, consistent with its scope as a structured survey rather than a formal systematic review." Transparent disclosure of non-registration is the correct honest approach. **Permanently Partially Met** — post-hoc registration is not accepted practice. |
| 24b | Protocol | **Fully Met** | "The review protocol is available at https://github.com/game-guild/docdo-paper." |
| 24c | Protocol amendments | **Fully Met** | "No amendments were made to the protocol after initiation of the search and screening process." |
| 25 | Support | **Fully Met** | Funding disclosed. |
| 26 | Competing interests | **Fully Met** | DocDo affiliation disclosed with safeguards described. |
| 27 | Data/code availability | **Fully Met** | Repository URL with traceability through S8, S10, S12 specified. |

---

## Issues in main.tex — Resolution Status

All three data-accuracy issues identified in the April 20 audit have been fixed.

### ~~Issue 1~~ **FIXED** — S-Numbering Inconsistency

All three references to the per-study characteristics table now consistently say "Supplementary Table S2" (`S2_included_studies.csv`). `S1_search_results_REAL.csv` is raw search results and is not cited in the paper body.

| Location | Was | Now |
|----------|-----|-----|
| §Synthesis, line ~801 | "Table S2" | ✓ unchanged (was already correct) |
| §Individual study results, line ~824 | "Supplementary Table S1" | ✅ "Supplementary Table S2" |
| §Quality Assessment Results, line ~872 | "Supplementary Table S1" | ✅ "Supplementary Table S2" |

### ~~Issue 2~~ **FIXED** — Quality Distribution Numbers (Items 18, 20a)

| Claim | Was | Now | Source |
|-------|-----|-----|--------|
| High quality count | 13 (25.0%) | ✅ **10 (19.2%)** | qa_summary audit |
| Moderate quality count | 38 (73.1%) | ✅ **41 (78.8%)** | qa_summary audit |
| Low quality count | 1 (1.9%) | ✓ 1 (1.9%) unchanged | |
| Sensitivity comparison | "25.0% overall" | ✅ **19.2% overall** | consistent with above |

The synthesis-subset distribution (26 studies: "high 19%, moderate 81%") was already internally consistent with the corrected overall rate and was not changed.

Note: 41/52 = 78.846%, which correctly rounds to **78.8%**, not 78.9% as the prior audit noted.

### ~~Issue 3~~ **FIXED** — Code Availability Percentage (4 occurrences updated)

| Location | Was | Now |
|----------|-----|-----|
| §Quality Assessment Results | "confirmed for 15 studies (28.8%)" | ✅ "confirmed for 13 studies (25.0%)" |
| §Discussion — Reproducibility bullet | "only 28.8% (15/52) released source code" | ✅ "only 25.0% (13/52) released source code" |
| §RQ4 summary | "only 28.8% of studies released source code" | ✅ "only 25.0% of studies released source code" |
| §Conclusion bullet | "reproducibility (28.8% code availability)" | ✅ "reproducibility (25.0% code availability)" |

**Caveat:** The authoritative source file (`s3_extracted_data_full*.csv`) is not present in the repository; the 13/52 figure comes from the prior audit record. `S2_included_studies.csv` shows 37/52 "yes" but uses a broad definition (all method papers = yes) that does not match the Q10 quality pipeline criterion ("partial or full implementation publicly released"). The 13/52 (25.0%) from the QA pipeline is the more conservative and methodologically defensible count.

### Issue 4 — Reporting Bias Per-Organ Figure (open, left as estimate)

The paper states "39 of 52 studies (75.0%) fully reported per-organ results across all evaluated structures." No dedicated field exists in repository data to verify this count — `dice_per_organ` captures whether *any* per-organ value exists, not whether *all* structures were reported. This figure is an estimate from the original extraction review. **No change made; retained as an estimate.**

---

## Historical Audit Findings (from prior compliance review)

### Confirmed Fixed in current main.tex

| Item | Original claim | Fix applied |
|------|---------------|-------------|
| Item 9 | Author contact status absent | "Study authors were not contacted for missing or unclear data" |
| Item 10a | TTA handling unclear | "single-model result without TTA was recorded as the primary outcome" |
| Item 10b | Missing data handling absent | "recorded as 'not reported.' No imputation of missing values was performed." |
| Item 11 | Framework not declared as RoB instrument | "This three-dimension numerical framework constitutes the study-level quality assessment instrument..." |
| Item 12 | Effect Measures absent | Effect Measures subsection added |
| Item 13f | "pre-specified" language | Changed to "post-hoc sensitivity analysis (not pre-specified in the review protocol)" |
| Item 14 | Reporting bias method absent | Reporting Bias Assessment subsection added |
| Item 15 | Certainty assessment absent | Certainty Assessment subsection added |
| Item 16b | S5 not referenced | "provided in Supplementary S5 (S5_screening_decisions.csv)" |
| Item 20b | Arithmetic means vs pooled unclear | Explicit clarification added |
| Item 20d | 84.8±2.3% (not reproducible) | Removed; replaced with directional statement + 34.5% quality figure |
| Item 21 | Reporting biases results absent | Reporting Bias Results subsection added |
| Item 22 | Certainty of evidence absent | Certainty of Evidence subsection added |
| Item 24a | Non-registration not disclosed | "not prospectively registered... consistent with its scope as a structured survey" |
| Item 24b | Protocol URL absent from main text | URL added to Declarations section |
| Item 24c | Amendments statement absent | "No amendments were made to the protocol after initiation" |
| QA framework | "four-dimension binary" description | Corrected to "three-dimension numerical framework (0–10 per dimension)" |

### Confirmed Fixed: S-Numbering (three references corrected in prior revision)

| Old paper reference | Corrected reference | Actual file |
|---------------------|---------------------|-------------|
| "Supplementary S2" (database queries) | "Supplementary S3" | `S3_search_protocol.md` |
| "Supplementary S3" (extraction form) | "Supplementary S7" | `S7_extraction_template.csv` |

**Note:** The third correction (Table S1 → Table S2 for per-study characteristics) was recorded as done, but the current main.tex still contains two "Table S1" references at lines ~824 and ~872 (see Issue 1 above). This correction is **incomplete**.

---

## Items That Honestly Cannot Be Fully Met

| # | Item | Why it can't be fully met |
|---|------|--------------------------|
| 1 | Title says "systematic review" | Paper is a structured survey. Changing title would misrepresent the work. |
| 7 | Full search strategy inline | Four of five database queries remain in supplementary. Fixable but requires editorial decision. |
| 16b | All excluded studies individually cited | 11 full-text exclusions; some still presented by category rather than individually. S5 reference provides full list. |
| 17 | Per-study characteristics | S2 exists with 52 studies; inconsistent S1/S2 references in text need reconciliation. |
| 18 | Exact per-study RoB distribution | Numbers in paper (13/38/1) don't match audited qa_summary (10/41/1). Needs correction. |
| 19 | All studies with precision | Source literature doesn't report CIs for Dice scores in most ML papers. Best approach: supplementary table. |
| 20a | Per-synthesis quality | Aggregate quality distribution reported, not per-synthesis-table breakdown. |
| 20c | Formal heterogeneity statistics | No pooled estimates → I², τ², Cochran's Q do not exist. Structural limit. |
| 20d | Full sensitivity comparison | Only 7/29 DOI-subset studies have numeric overall_dice. Directional consistency is the verifiable maximum. |
| 24a | Prospective registration number | Completed survey cannot be retroactively registered in PROSPERO. |

---

## Deep Analysis: Survey vs. Systematic Review — PRISMA Item-Level Structural Assessment

### The Structural Incompatibility

PRISMA 2020 was engineered around a specific experimental architecture that this paper deliberately does not use:

1. **Prospective protocol** registered in PROSPERO before data collection begins
2. **Statistical meta-analysis** producing pooled effect estimates with confidence intervals
3. **Clinical or epidemiological study designs** enabling causal inference
4. **Per-study risk-of-bias assessment** using validated instruments (Cochrane RoB 2, ROBINS-I, Newcastle-Ottawa Scale)

This paper surveys computational benchmark studies — not RCTs or cohort studies. The comparison is between deep learning architectures on public CT datasets, not between treatments in patient populations. The structural consequences are concrete:

- **No estimand to pool.** I², τ², Cochran's Q are functions defined over a pooled effect estimate. Without meta-analysis, these statistics *do not exist* — there is nothing to compute or report.
- **No prospective registration window.** PROSPERO accepts only systematic review protocols registered before or during data collection. A completed survey cannot be retroactively registered.
- **No validated risk-of-bias instrument.** Cochrane RoB 2, ROBINS-I, and Newcastle-Ottawa assess threats to causal inference in human-subjects research. For benchmark comparisons, there is no "control arm," no "confounders" in the epidemiological sense, and no "blinding." A custom quality framework is the methodologically correct substitute — but it is a different construct.
- **PICO does not map.** PRISMA's eligibility criteria template expects Population/Intervention/Comparator/Outcome. The paper's criteria use CT modality, architecture type, evaluation protocol, and metric reporting requirements — appropriate for computational surveys but structurally different.
- **GRADE does not apply.** GRADE evaluates certainty in a clinical treatment effect. Without a pooled clinical effect estimate, GRADE has no estimand to evaluate.

---

### Three-Category Classification

| Category | Definition |
|----------|-----------|
| **Universal** | Item applies identically to surveys and systematic reviews; survey should fully meet or explicitly explain non-meeting on its own merits |
| **Survey-Adapted** | Item applies in modified form; the PRISMA intended goal can be meaningfully served with survey-appropriate methods |
| **N/A-Structural** | Item presupposes a design feature absent from any survey; honest disclosure replaces compliance |

---

### Universal Items — current main.tex status

| # | Item | Current status | Notes |
|---|------|--------------|----|
| 2 | Structured abstract | **Fully Met** | PRISMA headings present |
| 3 | Rationale | **Fully Met** | |
| 4 | Objectives | **Fully Met** | Four explicit RQs |
| 5 | Eligibility criteria | **Fully Met** | |
| 6 | Information sources | **Fully Met** | |
| 7 | Search strategy | **Partially Met** | Four of five database queries in supplementary — fixable |
| 8 | Selection process | **Fully Met** | |
| 9 | Data collection | **Fully Met** | |
| 10a | Data items (outcomes) | **Fully Met** | |
| 10b | Data items (variables) | **Fully Met** | |
| 13a | Synthesis eligibility | **Fully Met** | |
| 13b | Synthesis data preparation | **Fully Met** | |
| 13c | Synthesis display | **Fully Met** | |
| 13e | Heterogeneity methods | **Fully Met** | |
| 16a | PRISMA flow diagram | **Fully Met** | |
| 16b | Excluded studies | **Partially Met** | S5 referenced; fixable by referencing complete exclusion table |
| 17 | Per-study characteristics | **Partially Met** | S2 exists; internal S1/S2 inconsistency must be reconciled |
| 23a–23d | Discussion | **Fully Met** | All four sub-items |
| 24b | Protocol | **Fully Met** | |
| 24c | Protocol amendments | **Fully Met** | |
| 25 | Support/funding | **Fully Met** | |
| 26 | COI | **Fully Met** | |
| 27 | Data availability | **Fully Met** | |

**Universal Fully Met: 21. Universal Partially Met: 3 (Items 7, 16b, 17). All three are fixable without structural changes.**

---

### Survey-Adapted Items — current main.tex status

| # | PRISMA expects | Survey does instead | Current status | Assessment |
|---|---------------|---------------------|----------------|------------|
| **11** | Validated RoB tool | Custom three-dimension framework; assessors named; explicit declaration as instrument | **Fully Met** | Declaration sentence present; justification complete |
| **12** | Effect measures (RR, OR, MD) | Dice/HD95 with explicit justification | **Fully Met** | |
| **13d** | Justify synthesis approach | Three-reason narrative justification | **Fully Met** | |
| **13f** | Sensitivity analysis | Post-hoc DOI-restriction analysis (correctly framed as post-hoc) | **Fully Met** | |
| **14** | Funnel plot / Egger's test | Qualitative three-source bias assessment | **Fully Met** | |
| **15** | GRADE | Qualitative high/moderate/low by finding | **Fully Met** | |
| **18** | Per-study RoB ratings table | Quality distribution across 52 studies | **Partially Met** | Numbers in paper (13/38/1) don't match audited data (10/41/1) |
| **19** | Per-study results with CIs | Supplementary table + inline extracts | **Partially Met** | S1/S2 inconsistency; CIs absent for most studies (source-literature limitation) |
| **20a** | Per-synthesis RoB summary | Quality distribution among contributing studies (19%/81%) | **Partially Met** | Corrected numbers; aggregate not per-table |
| **20b** | Pooled estimates with CIs | Arithmetic means ± SD, explicitly labeled | **Fully Met** | |
| **20d** | Sensitivity analysis results | Directional consistency + 34.5% quality figure | **Partially Met** | Honest maximum given data availability |
| **21** | Egger's / funnel results | Qualitative three-source narrative | **Fully Met** | Note: 39/52 figure is an estimate without dedicated repo field |
| **22** | GRADE per outcome | High/moderate/low confidence by finding | **Fully Met** | |

**Adapted Fully Met: 8 items. Adapted Partially Met: 4 items (18, 19, 20a, 20d).**

---

### N/A-Structural Items

| # | Item | Design feature presupposed | How the paper handles it |
|---|------|--------------------------|-------------------------|
| **1** | Identify as "systematic review" | Paper IS a systematic review | Uses "Agentic Structured Survey" — correct and non-negotiable |
| **20c** | Formal heterogeneity results | Pooled effect estimate | States formal investigation not conducted; qualitative stratification subsection provided |
| **24a** | Prospective registration number | Protocol registered before data collection | Explicit disclosure: "not prospectively registered... consistent with its scope as a structured survey rather than a formal systematic review" |

**N/A-Structural: 3 items. All handled with honest disclosure.**

---

### Survey-Applicable Compliance Score

Removing the 3 N/A-Structural items from the 39-item scorecard leaves **36 survey-applicable items**:

| | Current main.tex | After fixing Issues 1–3 |
|--|-----------------|------------------------|
| **Fully Met** | 29 (81%) | 31 (86%) |
| **Partially Met** | 7 (19%) | 5 (14%) |
| **N/A-Structural (excluded)** | 3 | 3 |
| **Survey-applicable total** | **36** | **36** |

_"After fixing Issues 1–3" = reconcile S1/S2 references, correct quality distribution to 10/41/1, correct code availability to 13/52 (25.0%)._

**Bottom line:** The current main.tex achieves **81% (29/36)** on survey-applicable PRISMA items, up from an estimated 42% (15/36) in the original version. The remaining partially-met items fall into three categories:
1. **Structural consequence of being a survey** (Items 20c, 24a) — irreducible
2. **Source-literature limitations** (Item 19) — source papers don't report CIs for Dice
3. **Small fixable gaps** (Items 7, 16b, 17, 18, 20a, 20d) — targeted edits needed

---

## What the Paper's Methods Already Says About PRISMA

The current main.tex Methods section contains the correct framing sentence (§2 opening paragraph):

> *"PRISMA 2020 was designed for prospectively registered systematic reviews with statistical meta-analysis; several checklist items (prospective registration, pooled effect estimates, per-study risk-of-bias instruments) are structurally inapplicable to a narrative survey and are addressed by explicit disclosure of absence rather than compliance."*

This is accurate, present, and sufficient.

---

## Remaining Action Items

1. ~~**FIX** — Reconcile S-numbering in main.tex.~~ **DONE (April 20, 2026).** Lines ~824 and ~872 updated from "Table S1" to "Table S2." All three S-references now consistent.

2. ~~**VERIFY AND FIX** — Quality distribution discrepancy.~~ **DONE (April 20, 2026).** Updated to 10 (19.2%) high / 41 (78.8%) moderate / 1 (1.9%) low. Sensitivity analysis "25.0% overall" also updated to "19.2%."

3. ~~**VERIFY AND FIX** — Code availability discrepancy.~~ **DONE (April 20, 2026).** Updated all four occurrences from 28.8% (15/52) to 25.0% (13/52). Caveat: authoritative source file absent from repo; 13/52 from prior QA pipeline audit.

4. **DOCUMENT** — Account for the missing S9 entry in the supplementary series (S8 → S10). Add a note to `S0_data_provenance.md` explaining whether S9 was planned-but-unproduced, merged, or intentionally omitted. A numbered series with an unexplained gap invites reviewer questions.

5. **CLARIFY** — Add a one-line note in the Methods AI Screening paragraph listing all three model identifiers (`gpt-4o-mini`, `gpt-5-nano`, `gpt-5.2`) and the API access dates. Already present in paper body; ensure the identifiers are complete and API access dates are stated.

6. **VERIFY** — The inline PubMed query: confirm it matches the actual query string executed during the search (cross-check against S3_search_protocol.md).

7. **ACCEPT** — Item 1 (Title) will remain Partially Met. The paper is a structured survey, not a systematic review, and the title should reflect reality.

8. **ACCEPT** — Items 20c and 24a will remain Partially Met. These are structural constraints of the survey design that cannot be resolved without misrepresenting the work.

---

## Strengths (current main.tex)

- **Structured abstract** properly follows PRISMA for Abstracts format with all 8 required headings.
- **Exemplary PRISMA flow diagram** (Figure 1) with complete numbers and exclusion reasons at every stage.
- **Thorough search strategy** across 5 databases plus citation tracking and conference proceedings.
- **Transparent AI-assisted screening** with multi-model consensus, validation metrics (κ = 0.89), and false-negative recovery.
- **Honest framing** as "PRISMA-informed structured survey" — does not overclaim systematic review status.
- **Three-dimension quality framework** explicitly declared as the study-level RoB instrument with justification for why clinical RoB tools are inapplicable.
- **Effect Measures subsection** correctly explains why Dice/HD95 replace traditional effect sizes.
- **Post-hoc sensitivity analysis** correctly framed — removed "pre-specified" language.
- **Reporting Bias and Certainty Assessment subsections** present with appropriate qualitative substitutes for funnel plots and GRADE.
- **Methodology transparency** — explicitly describes what was and was not done (no author contact, no imputation, no formal meta-analysis, no GRADE).
- **Proactive COI disclosure** with specific safeguards.
- **Strong data availability statement** with traceability through S8, S10, S12.
- **Honest disclosure** of non-registration appropriate for a structured survey.

---

*Reference: Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi: 10.1136/bmj.n71*
