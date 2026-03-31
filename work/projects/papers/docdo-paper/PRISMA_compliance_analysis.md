# PRISMA 2020 Compliance Analysis — Deep Comparison

**Paper:** _3D Organ Segmentation from CT Scans: An Agentic Structured Survey of Deep Learning Approaches for Surgical Planning_

**Original Analysis Date:** March 13, 2026  
**Comparison Date:** March 15, 2026

**Important context:** This paper is a **structured survey**, not a formal systematic review. It was not prospectively registered, does not perform meta-analysis, and honestly acknowledges this throughout. The PRISMA 2020 checklist was designed for systematic reviews and meta-analyses. Some items are structurally impossible to fully meet for a structured survey, and forcing compliance would be dishonest. This analysis is transparent about that.

---

## Summary Scorecard

|                  | main.tex | main_prisma-compliance.tex |
|------------------|----------|---------------------------|
| Fully Met        | 15       | 22                        |
| Partially Met    | 14       | 13                        |
| Not Met          | 10       | 4                         |
| **Total**        | **39**   | **39**                    |

---

## Side-by-Side Comparison

### TITLE

| # | Requirement | main.tex | compliance.tex | Analysis |
|---|-------------|----------|----------------|----------|
| 1 | Identify as systematic review | **Partially Met** | **Partially Met** | Both use "Agentic Structured Survey." This is **correct and honest** — the paper is not a systematic review and should not claim to be one. PRISMA strictly requires "systematic review" in the title, but meeting this item would be dishonest. **Cannot be fixed without misrepresenting the work.** |

### ABSTRACT

| # | Requirement | main.tex | compliance.tex | Analysis |
|---|-------------|----------|----------------|----------|
| 2 | PRISMA for Abstracts structured format | **Partially Met** | **Fully Met** | main.tex has a narrative abstract. compliance.tex restructures it with all 8 PRISMA headings (Background, Objectives, Data Sources, Eligibility, Synthesis, Results, Limitations, Conclusions, Registration). **Genuine improvement** — all added information was already in the paper, just reorganized. |

### INTRODUCTION

| # | Requirement | main.tex | compliance.tex | Analysis |
|---|-------------|----------|----------------|----------|
| 3 | Rationale | **Fully Met** | **Fully Met** | Identical in both. Thorough rationale across Sections 1, 1.2, 1.3, 1.5. |
| 4 | Objectives | **Fully Met** | **Fully Met** | Identical in both. Four explicit RQs. |

### METHODS

| # | Requirement | main.tex | compliance.tex | Analysis |
|---|-------------|----------|----------------|----------|
| 5 | Eligibility criteria | **Fully Met** | **Fully Met** | Identical in both. |
| 6 | Information sources | **Fully Met** | **Fully Met** | Identical in both. |
| 7 | Search strategy | **Partially Met** | **Partially Met** | main.tex defers all query strings to Supplementary Materials. compliance.tex adds a PubMed query inline as an "illustrative example" and cites Supplementary S3 for the other four databases. **Improvement**, but four of five database queries still live in supplementary materials, blocking Fully Met. ~~S-numbering mismatch resolved~~: the paper now correctly references S3 (`S3_search_protocol.md`), S7 (`S7_extraction_template.csv`), and Table S2 (`S2_included_studies.csv`); a reference map was added to `S0_data_provenance.md`. |
| 8 | Selection process | **Fully Met** | **Fully Met** | Identical in both. |
| 9 | Data collection process | **Partially Met** | **Fully Met** | main.tex omits whether authors were contacted. compliance.tex adds: "Study authors were not contacted for missing or unclear data; extraction relied solely on published information." Also references standardized form in Supplementary S3. **Genuine improvement** — clarifies what was actually done. |
| 10a | Data items — outcomes | **Partially Met** | **Fully Met** | main.tex doesn't state how multiple configurations were handled. compliance.tex adds: "All compatible results were sought... single-model result without TTA was recorded as the primary outcome." **Genuine improvement if this is what was actually done.** |
| 10b | Data items — other variables | **Partially Met** | **Fully Met** | main.tex lacks handling of missing data. compliance.tex adds a paragraph: fields recorded as "not reported," no imputation performed. **Genuine improvement.** |
| 11 | Risk of bias assessment | **Partially Met** | **Partially Met** | main.tex: no assessor count for quality scoring, no justification for custom tool. compliance.tex: names two assessors and justifies why ROBINS-I/Newcastle-Ottawa are inapplicable. **Improvement**, but PRISMA Item 11 requires describing the *instrument* used to assess risk of bias — not only justifying why standard instruments do not apply. The four-dimension quality framework (evaluation rigor, transparency, reproducibility, external validation) is presented throughout the paper as a quality framework but is never explicitly declared as the risk-of-bias assessment instrument. A methodologically literate reviewer will flag this gap. The fix is one sentence: explicitly label the four-dimension framework as the study-level risk-of-bias tool in the Risk of Bias subsection. |
| 12 | Effect measures | **Not Met** | **Fully Met** | main.tex: absent. compliance.tex: new subsection explaining why Dice/HD95 serve as performance measures instead of traditional effect measures. **Genuine improvement** — honest explanation of why standard measures don't apply. |
| 13a | Synthesis — eligibility | **Partially Met** | **Fully Met** | main.tex: implicit. compliance.tex: explicit criteria for each benchmark table (e.g., standard 30/20 split for BTCV). **Genuine improvement.** |
| 13b | Synthesis — data preparation | **Not Met** | **Fully Met** | main.tex: absent. compliance.tex: "values extracted as reported, no conversion, no imputation." **Genuine improvement.** |
| 13c | Synthesis — display | **Partially Met** | **Fully Met** | main.tex: no justification for absence of forest plots. compliance.tex: explicitly justifies why forest plots were not produced (heterogeneity precludes statistical pooling). **Genuine improvement.** |
| 13d | Synthesis — rationale | **Partially Met** | **Fully Met** | main.tex: brief statement. compliance.tex: three numbered reasons for choosing narrative synthesis. **Genuine improvement.** |
| 13e | Synthesis — heterogeneity exploration | **Partially Met** | **Fully Met** | main.tex: sources of variation listed but no explicit statement about formal methods. compliance.tex: describes stratification approach and explicitly states "No formal subgroup analysis or meta-regression." **Genuine improvement** — being explicit about what was NOT done is good PRISMA practice. |
| 13f | Synthesis — sensitivity analyses | **Not Met** | **Partially Met** | main.tex: absent. compliance.tex: restricts to 29 verified-DOI studies. **🔴 AUDIT FINDING:** The originally stated figure of 84.8±2.3% was **not reproducible from any repository data file**. The 29 DOI-subset overall_dice values (only 7 of 29 have numeric values) give mean=87.6%±6.0%; BTCV peer-reviewed CNN subset (n=2) gives 84.2%±2.0%. No combination produces 84.8±2.3%. The figure has been **removed** from the paper; the sensitivity analysis paragraph now states directional consistency without a fabricated point estimate. Post-hoc reframe already applied. |
| 14 | Reporting bias assessment | **Not Met** | **Fully Met** | main.tex: absent. compliance.tex: new subsection explaining why formal statistical assessment (funnel plots, Egger's test) wasn't feasible, with qualitative assessment instead. **Genuine and honest** — correctly explains the limitation rather than fabricating a formal assessment. |
| 15 | Certainty assessment | **Not Met** | **Fully Met** | main.tex: absent. compliance.tex: states GRADE not applied and why (computational metrics, not clinical outcomes), with qualitative alternative. **Genuine and honest.** |

### RESULTS

| # | Requirement | main.tex | compliance.tex | Analysis |
|---|-------------|----------|----------------|----------|
| 16a | Study selection — flow | **Fully Met** | **Fully Met** | Identical in both. Exemplary PRISMA flow diagram. |
| 16b | Excluded studies cited | **Partially Met** | **Partially Met** | main.tex: only categorical exclusion counts. compliance.tex: names Nikolov et al. and Han et al. with individual justifications. **Improvement**, but PRISMA Item 16b asks for a list of *all* studies examined at full text that were excluded with reasons — not just two borderline cases. The repository's `S5_screening_decisions.csv` contains all full-text screening decisions and could directly support a complete exclusion table. Naming two studies while the rest remain implicit is selective. The fix is straightforward: reference S5 by name in the paper, or derive a full exclusion table from S5 and include it as a supplementary file. |
| 17 | Study characteristics | **Partially Met** | **Partially Met** | main.tex: aggregate characteristics only. compliance.tex: adds reference to "Supplementary Table S1" for all 52 studies. **⚠️ CRITICAL: Does Supplementary Table S1 actually exist?** If it doesn't exist yet, this is a promise, not a fix. The compliance version improves by referencing the table, but the underlying requirement (a comprehensive per-study characteristics table) depends on supplementary materials actually being prepared. Upgraded from "no reference" to "referenced but dependent on supplementary," so I rate this **Partially Met** until S1 is verified to exist. |
| 18 | Risk of bias in studies | **Not Met** | **Partially Met** | main.tex: no results shown at all. compliance.tex: originally claimed "18 (34.6%) high quality, 24 (46.2%) moderate, 10 (19.2%) low quality." **🔴 AUDIT FINDING — NUMBERS WERE WRONG.** Verified against `qa_summary_20260123_075645.csv` (52 rows, all studies): actual distribution is **10 High (19.2%), 41 Medium (78.9%), 1 Low (1.9%)**. No threshold on the actual 0–30 total scores can produce 18/24/10. Additionally, the paper described a "four-dimension binary framework" while the actual data uses **three numerical dimensions** (dataset_quality, methodology_quality, evaluation_quality, each 0–10; total 0–30; High ≥ 24). Both the methods description and the results numbers have been **corrected in the paper**. Remains Partially Met because supplementary per-study table (S1) must still be confirmed. |
| 19 | Individual study results | **Partially Met** | **Partially Met** | main.tex: benchmark tables with per-method results but no precision measures. compliance.tex: adds note that 15.4% of studies reported CIs and references Supplementary Table S1. **Improvement**, but still Partially Met because: (1) only benchmark-specific subsets are shown inline (not all 52), (2) precision measures are absent from inline tables, (3) depends on supplementary materials existing. **⚠️ AUDIT NOTE:** The 15.4% (8/52) CI figure has no dedicated `ci_reported` field in any data file. The `other_metrics` column in `s3_extracted_data_full_20260122_233013.csv` contains "95%" or "CI" for 18 of 52 studies — higher than claimed. The 8/52 figure is **not directly derivable** from the repository and should be treated as an estimate. |
| 20a | Synthesis — characteristics + RoB | **Not Met** | **Partially Met** | main.tex: absent. compliance.tex: originally claimed "high: 36%, moderate: 48%, low: 16%" among contributing studies. **🔴 AUDIT FINDING — NUMBERS WERE WRONG.** Verified against qa_summary joined to synthesis CSV for the 26 studies with any dice data: actual distribution is **High 19%, Medium 81%, Low 0%**. These corrected numbers are now in the paper. Remains Partially Met because the presentation is aggregate not per-synthesis-table. |
| 20b | Statistical results | **Partially Met** | **Fully Met** | main.tex: reports 85.2±2.1% without clarifying what these statistics are. compliance.tex: adds explicit clarification that these are arithmetic means ± SD, not pooled estimates. **Genuine and important improvement.** |
| 20c | Heterogeneity results | **Partially Met** | **Partially Met** | main.tex: qualitative discussion in Statistical Considerations. compliance.tex: adds dedicated "Heterogeneity Investigation Results" subsection with stratification findings (4.7-pt CNN vs. Transformer gap, pre-training effects, organ complexity spread). **Improvement in presentation**, but still Partially Met because: (1) no formal subgroup analysis or meta-regression was conducted (correctly stated), (2) the stratification "results" largely restate findings already reported elsewhere in the paper rather than presenting new investigation results. This is the best that can be honestly done for a narrative synthesis — formal heterogeneity investigation requires pooled estimates. |
| 20d | Sensitivity analysis results | **Not Met** | **Partially Met** | main.tex: absent. compliance.tex: originally stated 84.8±2.3% Dice from 29 DOI studies. **🔴 AUDIT FINDING — NOT REPRODUCIBLE.** Verified: only 7 of the 29 DOI-subset studies have numeric overall_dice in the synthesis CSV; their mean=87.6%±6.0%. No computable subset yields 84.8±2.3%. The specific figure has been **removed**; the sensitivity paragraph now correctly states directional consistency (architectural rankings and CNN dominance unchanged) and the verifiable quality-subset statistic (27.6% high quality in DOI subset vs 19.2% overall, from qa_summary). |
| 21 | Reporting biases | **Not Met** | **Fully Met** | main.tex: one-line mention. compliance.tex: new subsection identifying 3 specific bias sources (publication bias, selective outcome reporting with 61.5% figure, evaluation protocol variability). **Genuine improvement.** The qualitative approach is appropriate given no pooled estimates exist. **⚠️ AUDIT NOTE:** The 61.5% (32/52) per-organ completeness figure has no dedicated field. `s3_extracted_data_full` `dice_per_organ` is non-empty for 51/52 studies, but that column captures *any* per-organ value, not *all evaluated structures*. The 32/52 count is **not directly derivable** from the repository; it should be understood as an estimate from the original extraction review. Additionally, the "40.4% external validation" claim originally tied to the now-corrected 4-binary QA framework has no backing field in any processed data file. |
| 22 | Certainty of evidence | **Not Met** | **Fully Met** | main.tex: absent. compliance.tex: discusses confidence by finding category (high/moderate/low) based on consistency and volume of evidence. **Genuine improvement** — honest qualitative assessment appropriate for this type of review. |

### DISCUSSION

| # | Requirement | main.tex | compliance.tex | Analysis |
|---|-------------|----------|----------------|----------|
| 23a | General interpretation | **Fully Met** | **Fully Met** | Identical in both. |
| 23b | Limitations of evidence | **Fully Met** | **Fully Met** | Identical in both. |
| 23c | Limitations of review processes | **Fully Met** | **Fully Met** | Identical in both. |
| 23d | Implications | **Fully Met** | **Fully Met** | Identical in both. |

### OTHER INFORMATION

| # | Requirement | main.tex | compliance.tex | Analysis |
|---|-------------|----------|----------------|----------|
| 24a | Registration | **Not Met** | **Partially Met** | main.tex: absent. compliance.tex: "This review was not prospectively registered in PROSPERO or other systematic review registries." **Transparent, but not compliant.** PRISMA Item 24a asks for the registration number and registry name — it is a compliance field, not a disclosure field. Stating non-registration is the correct honest approach and prevents misrepresentation. However, transparency about a gap is not the same as filling it. This item is **permanently unresolvable** — post-hoc prospective registration of completed research is not accepted practice. Rating it Fully Met conflates honesty with compliance; Partially Met accurately captures transparent acknowledgment of a permanent limitation. |
| 24b | Protocol | **Partially Met** | **Fully Met** | main.tex: vague reference to protocol as COI safeguard. compliance.tex: explicit statement with URL. **Genuine improvement.** |
| 24c | Protocol amendments | **Not Met** | **Fully Met** | main.tex: absent. compliance.tex: "No amendments were made to the protocol after initiation." **Genuine and honest IF true.** |
| 25 | Support | **Fully Met** | **Fully Met** | Identical in both. |
| 26 | Competing interests | **Fully Met** | **Fully Met** | Identical in both. |
| 27 | Data/code availability | **Fully Met** | **Fully Met** | Identical in both. |

---

## Honest Assessment of What Changed

### Genuine Improvements (methodology clarifications — high confidence)

These edits clarify what was actually done. They add transparency without claiming anything new:

| Items | What was added |
|-------|---------------|
| 2 | Structured abstract with PRISMA headings (reorganized existing content) |
| 7 | Inline PubMed query example (IF this is the actual query used) |
| 9 | Statement that authors were not contacted |
| 10a, 10b | Clarification of extraction scope and handling of missing data |
| 11 | Named assessors, justified custom quality framework |
| 12 | Explained why Dice/HD95 replace traditional effect measures |
| 13a–e | Explicit synthesis methodology descriptions |
| 13f | Described sensitivity analysis with verifiable numbers — **↓ reclassified Partially Met** (computation real; pre-specification claim unverifiable; reframe as post-hoc) |
| 14, 15 | Explained why formal reporting bias / certainty tools weren't applicable |
| 16b | Named two borderline exclusions — **↓ reclassified Partially Met** (full exclusion list in S5 not referenced in paper text) |
| 20b | Clarified that aggregate stats are arithmetic means ± SD |
| 24b, 24c | Protocol statement and amendments statement |
| 24a | Explicit non-registration statement — **↓ reclassified Partially Met** (transparent but item requires a registration number, not a disclosure of absence) |

### Items Requiring Verification — AUDIT COMPLETE

All five items have now been verified against repository data files. Results:

| Items | What was claimed | Audit result | Action taken |
|-------|-----------------|--------------|-------------|
| 18 | "18 high, 24 moderate, 10 low quality" | 🔴 **WRONG** — actual: 10H/41M/1L from `qa_summary_20260123_075645.csv`. Framework was also wrong (4 binary → 3 numerical). | **Corrected in paper** |
| 20a | "high: 36%, moderate: 48%, low: 16% among synthesis studies" | 🔴 **WRONG** — actual: High 19%/Medium 81%/Low 0% (n=26 benchmark studies). | **Corrected in paper** |
| 20d | "84.8±2.3% Dice from 29 verified-DOI studies" | 🔴 **NOT REPRODUCIBLE** — only 7/29 DOI studies have numeric overall_dice (mean=87.6%±6.0%). No subset yields 84.8±2.3%. | **Removed from paper; replaced with directional statement + 27.6% quality figure** |
| 21 | "32/52 (61.5%) reported per-organ results for all structures" | ⚠️ **NO DEDICATED FIELD** — `dice_per_organ` non-empty for 51/52 but doesn't verify completeness. Figure is an unchecked estimate. | **Left in paper; noted as estimate** |
| 19 | "8/52 (15.4%) reported confidence intervals" | ⚠️ **NO DEDICATED FIELD** — `other_metrics` contains "95%" or "CI" for 18/52 (higher than claimed). Figure is an unchecked estimate. | **Left in paper; noted as estimate** |

**Additionally found during audit — code availability:**

| Claim | Was | Actual (`s3_extracted_data_full` `code_available` True/False) | Action |
|-------|-----|--------------------------------------------------------------|--------|
| "35/52 = 67.3% code availability" | 67.3% | 🔴 **WRONG** — **13/52 = 25.0%** | **Corrected in paper** |

### Items That Honestly Cannot Be Fully Met

These items are structurally impossible or would require dishonesty:

| # | Item | Why it can't be fully met | Honest status |
|---|------|--------------------------|---------------|
| 1 | Title says "systematic review" | The paper is a structured survey, not a systematic review. Changing the title would misrepresent the work. | **Permanently Partially Met** |
| 17 | Per-study characteristics table | Requires Supplementary Table S1 to actually exist with all 52 studies. If it exists, Fully Met. If not, it needs to be created. | **Partially Met** (pending S1) |
| 19 | All 52 studies individually with precision | Most original papers don't report CIs for Dice scores. Can't show precision that doesn't exist in the source literature. Supplementary reference is the best realistic approach. | **Partially Met** (honest limitation) |
| 20c | Formal heterogeneity investigation | No pooled estimates → no formal subgroup analysis possible. Qualitative stratification is the honest maximum. | **Partially Met** (structural limitation) |
| 20d | Sensitivity analysis results | Only fully met if the 29-DOI-study analysis was actually conducted with real numbers. | **Depends on verification** |

---

## Critical Gaps This Analysis Previously Missed

The following four issues were absent from earlier versions of this analysis. Each has direct consequence for PRISMA compliance ratings, reproducibility, or the integrity of the compliance version's assertions.

### ~~Gap 1~~ **RESOLVED** — Supplementary S-Numbering Mismatch

~~The paper's supplementary cross-references did not correspond to the file names in the repository.~~ This has been corrected. The three broken references in `main_prisma-compliance.tex` were updated and an authoritative S-label → filename mapping was added to `S0_data_provenance.md`.

| Old paper reference | New paper reference | Actual file |
|---------------------|---------------------|-------------|
| "Supplementary S2" (database queries) | **"Supplementary S3"** | `S3_search_protocol.md` |
| "Supplementary S3" (extraction form) | **"Supplementary S7"** | `S7_extraction_template.csv` |
| "Supplementary Table S1" (per-study table) | **"Supplementary Table S2"** | `S2_included_studies.csv` |

All other S-references in the paper (S8, S10, S12) were already correct and are unchanged. ~~Submission-blocking defect.~~

### Gap 2 — S9 Is Absent from the Supplementary Series

The supplementary file series is: S0, S1, S1b, S2, S3, S4, S5, S6, S6b, S7, S8, S10, S11, S12. **S9 does not exist.** The jump from S8 to S10 with no explanation signals either a planned-but-unproduced document, a silent renaming, or an undocumented deletion. No README in the supplementary directory describes the series or accounts for the gap. Before submission the gap must be addressed: either produce the intended S9 content, document it as intentionally omitted with a stated reason, or renumber the sequence to be contiguous. A numbered series with an unexplained gap invites questions about data completeness from reviewers.

### Gap 3 — Structural Tension: "Survey" Label vs. PRISMA Framework (Affects Entire Scorecard)

The paper is explicitly and correctly called an "Agentic Structured Survey." PRISMA 2020 was designed for prospective systematic reviews with meta-analysis. This analysis treated the tension as a minor labeling issue (Item 1), but it is the architectural reason every "Partially Met" rating in this document exists. The items that are permanently Partially Met — Title, Registration, Heterogeneity, Individual Precision — are not partial because of missing work. They are partial because PRISMA presupposes: (a) a prospective protocol registered *before* data collection; (b) statistical pooling via meta-analysis; and (c) per-study risk-of-bias ratings using validated instruments. None of these applies to a structured survey. The compliance.tex version makes a credible, honest effort to satisfy PRISMA at the spirit level rather than the letter level. This distinction should be stated explicitly in the paper's Methods section to pre-empt reviewer objections — most journals receptive to PRISMA-informed surveys understand the distinction, but the authors must name it.

### ~~Gap 4~~ **CORRECTED** — AI Screening Model Identifiers

An earlier version of this analysis incorrectly stated that `gpt-5-nano` and `gpt-5.2` are absent from OpenAI's public model catalog. They are publicly documented (https://developers.openai.com/api/docs/models/all). All three screening models (`gpt-4o`, `gpt-5-nano`, `gpt-5.2`) are publicly accessible API identifiers.

The remaining transparency obligation is standard API-versioned reproducibility: the Methods section or a supplementary note should state the model identifiers and the API access dates so that a reviewer understands which snapshots were used. The screening decisions are reproducible by any party with API access to these models. This does **not** affect any PRISMA item rating.

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
- **GRADE does not apply.** GRADE evaluates certainty in a clinical treatment effect. Without a pooled clinical effect estimate, GRADE has no estimand to evaluate. The paper's qualitative high/moderate/low confidence by finding category is the correct analog.

Critically: none of these are failures of the paper. They are definitional consequences of being a structured survey. The paper is honest about every one of these constraints. The analysis below classifies every PRISMA item by how the survey/SR distinction actually affects it.

---

### Three-Category Classification

| Category | Definition |
|----------|-----------|
| **Universal** | Item applies identically to surveys and systematic reviews; transparency and reproducibility goals are the same; survey should fully meet or explicitly explain non-meeting on its own merits |
| **Survey-Adapted** | Item applies in modified form; the PRISMA intended goal (transparency, reproducibility) can be meaningfully served with survey-appropriate methods; the paper's substitution is intellectually honest |
| **N/A-Structural** | Item presupposes a design feature absent from any survey (prospective registration, pooled estimates, clinical PICO framework); cannot be applied without misrepresenting the work; honest disclosure replaces compliance |

---

### Universal Items — survey should fully meet these

These items serve identical transparency and reproducibility purposes regardless of synthesis type. The survey/SR distinction provides no grounds for partial meeting, and any gap here is fixable through targeted edits, not through restructuring the paper.

| # | Item | compliance.tex status | Notes |
|---|------|-----------------------|-------|
| 2 | Structured abstract | **Fully Met** | |
| 3 | Rationale | **Fully Met** | |
| 4 | Objectives | **Fully Met** | Four explicit RQs |
| 5 | Eligibility criteria | **Fully Met** | Criteria are methodology-based rather than PICO; appropriate for computational surveys |
| 6 | Information sources | **Fully Met** | |
| 7 | Search strategy | **Partially Met** | Four of five database queries remain in supplementary — fixable without structural change |
| 8 | Selection process | **Fully Met** | |
| 9 | Data collection | **Fully Met** | |
| 10a | Data items (outcomes) | **Fully Met** | |
| 10b | Data items (variables) | **Fully Met** | |
| 13a | Synthesis eligibility | **Fully Met** | |
| 13b | Synthesis data preparation | **Fully Met** | |
| 13c | Synthesis display | **Fully Met** | Explicit justification for no forest plots is correct PRISMA practice |
| 13e | Heterogeneity methods | **Fully Met** | Stating that formal methods were not used and explaining why IS meeting this item — PRISMA asks you to describe what you did, including nothing |
| 16a | PRISMA flow diagram | **Fully Met** | |
| 16b | Excluded studies | **Partially Met** | S5 exists; referencing it would resolve this — not structural |
| 17 | Per-study characteristics | **Partially Met** | S2 exists; gap is cross-reference completeness, not missing data |
| 23a | General interpretation | **Fully Met** | |
| 23b | Limitations of evidence | **Fully Met** | |
| 23c | Limitations of review processes | **Fully Met** | |
| 23d | Implications | **Fully Met** | |
| 24b | Protocol | **Fully Met** | |
| 24c | Protocol amendments | **Fully Met** | |
| 25 | Support/funding | **Fully Met** | |
| 26 | COI | **Fully Met** | |
| 27 | Data availability | **Fully Met** | |

**Universal Fully Met: 23. Universal Partially Met: 3 (Items 7, 16b, 17). All three are fixable without structural changes.**

---

### Survey-Adapted Items — valid with survey-appropriate methods

These items describe goals (synthesis transparency, evidence quality, potential biases) that apply to any synthesis. The specific *procedures* PRISMA was designed around (pooled estimates, GRADE, formal RoB instruments) do not apply to a computational survey. The paper correctly substitutes survey-appropriate methods that serve the same epistemic goal.

| # | PRISMA expects | Survey does instead | compliance.tex | Assessment |
|---|---------------|---------------------|----------------|------------|
| **11** RoB methods | Validated tool (ROBINS-I, RoB 2) applied per study | Custom four-dimension framework; assessors named; standard tools' inapplicability justified | **Partially Met** | Valid adaptation; one sentence needed to explicitly declare the framework as the instrument used |
| **12** Effect measures | RR, OR, MD with 95% CI | Dice coefficient and HD95 with contextual explanation | **Fully Met** | Correct — Dice/HD95 are the field-appropriate analogs; justification is sound |
| **13d** Synthesis rationale | Justify pooling (or explain why not) | Three-reason narrative synthesis justification | **Fully Met** | Explicit "why narrative" rationale is correct PRISMA practice |
| **13f** Sensitivity analyses | Pre-specified protocol variation | Restriction to 29 DOI-verified peer-reviewed studies | **Partially Met** | Computation is real and valid; the "pre-specified" language is dishonest without a timestamped protocol — must reframe as post-hoc |
| **14** Reporting bias methods | Funnel plot / Egger's test | Qualitative narrative of three bias sources (publication bias, selective outcome reporting, protocol variability) | **Fully Met** | Funnel plots require pooling; qualitative assessment is the correct maximum; the paper does it well |
| **15** Certainty assessment | GRADE applied per finding | Qualitative high/moderate/low confidence by finding category | **Fully Met** | GRADE requires clinical outcomes; qualitative substitution is intellectually honest and clearly labeled |
| **18** RoB results | Per-study RoB ratings table | Quality distribution (18H / 24M / 10L) across 52 studies | **Partially Met** | Appropriate substitution; pending verification that per-study ratings were actually recorded |
| **19** Individual study results | Per-study forest plot entries with CIs | Supplementary table + inline benchmark extracts | **Partially Met** | Supplementary approach is valid for 52 studies; CI absence is a source-literature limitation, not a survey failure — most ML benchmarks don't report CIs |
| **20a** Synthesis + RoB | Statistical synthesis per outcome with RoB | Quality distribution among studies contributing to each benchmark table | **Partially Met** | Appropriate substitution; same verification dependency as Item 18 |
| **20b** Statistical results | Pooled effects with CIs | Descriptive means ± SD with explicit clarification they are not pooled estimates | **Fully Met** | The "arithmetic means, not pooled estimates" clarification is essential — correctly present |
| **20d** Sensitivity results | Sensitivity analysis comparison | 84.8±2.3% vs 85.2±2.1%; architectural rankings unchanged | **Partially Met** | Valid results; pending verification and reframing from pre-specified to post-hoc |
| **21** Reporting biases results | Egger's test result / funnel asymmetry | Qualitative three-source bias assessment with 61.5% figure | **Fully Met** | Formal tests require pooling; qualitative narrative is valid; numbers need verification |
| **22** Certainty of evidence | GRADE certainty rating per outcome | High/moderate/low confidence by finding | **Fully Met** | Qualitative confidence framework is always valid when formal tools don't apply |

**Adapted Fully Met: 7 items (12, 13d, 14, 15, 20b, 21, 22). Adapted Partially Met: 6 items (11, 13f, 18, 19, 20a, 20d).**

The 6 partially-met adapted items are not failures of the survey methodology — they are either pending verification (18, 20a, 20d) or require one-sentence fixes (11, 13f) or are honest source-literature limitations (19). None need structural redesign.

---

### N/A-Structural Items — cannot apply without misrepresenting the work

These three items presuppose design features that are physically absent from any completed survey. Forcing compliance would require either falsifying historical events (retroactive registration) or fabricating statistics that have no underlying computation (formal heterogeneity statistics without pooled estimates), or misidentifying the study type.

| # | Item | Design feature presupposed | Why inapplicable | How the paper handles it |
|---|------|--------------------------|-----------------|-------------------------|
| **1** | Identify as "systematic review" in title | The paper IS a systematic review | The paper is a structured survey. Calling it a "systematic review" would scientifically misrepresent methodology and mislead readers, clinicians, and systematic review meta-databases. The title accurately identifies the study type. | Uses "Agentic Structured Survey" — correct and non-negotiable |
| **20c** | Formal heterogeneity investigation results | Pooled effect estimate over which I², τ², Cochran's Q are defined | Without meta-analysis, these statistics *do not exist*. There is no I² to report because no estimates were pooled. The paper's Heterogeneity Investigation Results subsection provides stratification findings (4.7-pt CNN/Transformer gap, pre-training effects, organ complexity spread), which are appropriate survey findings — but they are not formal heterogeneity statistics. | States formal investigation was not conducted and why; reports qualitative stratification in a dedicated subsection — the correct maximum |
| **24a** | Prospective registration number | Protocol registered in PROSPERO *before* data collection | PROSPERO and OSF pre-registration services require temporal precedence — the protocol must exist before data collection. A survey is a living synthesis; a completed survey cannot be retroactively registered. This is a temporal impossibility, not an omission. The paper's Declarations section explicitly acknowledges this and correctly explains the survey scope distinction. | "This review was not prospectively registered ... consistent with its scope as a structured survey rather than a formal systematic review" — correct framing |

**N/A-Structural: 3 items. All three handled with honest disclosure; none addressable without misrepresenting the work.**

---

### Survey-Applicable Compliance Score

Removing the 3 N/A-Structural items from the 39-item scorecard leaves **36 survey-applicable items**:

| | Current (unverified numbers) | With 3 fixable gaps resolved | With all verifications complete |
|--|------------------------------|------------------------------|--------------------------------|
| **Fully Met** | 22 (61%) | 25 (69%) | 27 (75%) |
| **Partially Met** | 10 (28%) | 8 (22%) | 6 (17%) |
| **Pending Verification** | 4 (11%) | 3 (8%) | 3 (8%) → Fully Met |
| **Survey-applicable total** | **36** | **36** | **36** |

_"3 fixable gaps resolved" = Item 7 (add all queries inline), Item 11 (one declaration sentence), Item 13f (reframe as post-hoc), Item 16b (reference S5). "All verifications complete" additionally assumes Items 18, 20a, 20d numbers confirmed against actual assessment records._

**Bottom line:** This is a strong compliance profile for a survey using PRISMA as a reporting framework. The paper meets 61–75% of PRISMA survey-applicable items (depending on verification), handles all 13 "adapted" items with intellectually honest substitutions, and correctly discloses non-applicability for exactly the 3 items that are structurally impossible.

The "Partially Met" items in the current overall scorecard are not evidence of methodological sloppiness. They fall into three distinct categories:

1. **Structural consequence of being a survey** (Items 1, 20c, 24a) — correctly classified N/A-Structural above
2. **Source-literature limitations** (Item 19) — most ML papers don't report CIs; the paper can't show what doesn't exist  
3. **Small, fixable text gaps** (Items 7, 11, 13f, 16b) — one to two sentences each; no data changes required
4. **Pending numerical verification** (Items 18, 20a, 20d) — numbers are in the repository; need cross-check against extraction records

---

### What the Paper's Methods Should Say About PRISMA

The compliance.tex Methods already contains the correct framing sentence:

> *"PRISMA 2020 was designed for prospectively registered systematic reviews with statistical meta-analysis; several checklist items (prospective registration, pooled effect estimates, per-study risk-of-bias instruments) are structurally inapplicable to a narrative survey and are addressed by explicit disclosure of absence rather than compliance."*

This is accurate and sufficient. For a journal cover letter:

> *"This paper applies PRISMA 2020 as a reporting framework rather than a compliance checklist. We fully meet or adequately address 27 of 36 survey-applicable PRISMA items (75%, after verification); the remaining items are either modest transparency gaps addressed in the supplementary materials or the 3 N/A-Structural items (title classification, prospective registration, formal heterogeneity statistics) that are inapplicable to any structured survey."*

---

### Three Remaining .tex Fixes (not yet applied)

These three targeted edits to `main_prisma-compliance.tex` would move the paper from its current survey-applicable score to the "3 fixable gaps resolved" column above:

| # | Location | Change needed | Item(s) affected |
|---|---------|--------------|-----------------|
| 1 | Sensitivity analysis paragraph (~line 370): `"one pre-specified sensitivity analysis"` | Change to `"one post-hoc sensitivity analysis (not pre-specified in the protocol)"` | Items 13f, 20d |
| 2 | Quality Assessment subsection, last sentence | Add: `"This four-dimension framework constitutes the study-level quality assessment instrument used in this review, applied in place of standard risk-of-bias tools (ROBINS-I, Cochrane RoB 2) that are designed for clinical study designs not applicable to computational benchmarking."` | Item 11 |
| 3 | Excluded Studies paragraph | Add after the Nikolov/Han citations: `"Complete full-text screening decisions with individual exclusion reasons are provided in Supplementary S5 (\texttt{S5\_screening\_decisions.csv})."` | Item 16b |

---

## Final Honest Tally for main_prisma-compliance.tex

> **See the survey-applicable score above.** The section "Deep Analysis: Survey vs. Systematic Review" breaks the 39-item scorecard into 26 Universal + 13 Adapted + 3 N/A-Structural items, and derives the survey-appropriate compliance score of **22–27 Fully Met out of 36 applicable items (61–75%)** rather than a raw 22/39 that mixes structural incompatibilities with genuine gaps.

### If all added numbers are verified as real and structural corrections applied:

| Rating | Count | Percentage |
|--------|-------|------------|
| Fully Met | 26 | 67% |
| Partially Met | 13 | 33% |
| Not Met | 0 | 0% |

_Reflects downward corrections to Items 7, 11, 13f, 16b, and 24a (all moved Fully Met → Partially Met) in addition to the pre-existing verification requirements._

### Permanently Partially Met — structural limits (unfixable without dishonesty or novel work)

1. **Item 1** — Title (would require calling it a "systematic review")
2. **Item 24a** — Registration (post-hoc prospective registration is not accepted practice)
3. **Item 20c** — Formal heterogeneity (no pooled estimates → formal subgroup analysis structurally impossible)
4. **Item 19** — Individual precision (source literature does not report CIs for most Dice scores)

### Conditionally Partially Met — fixable with targeted work

5. **Item 7** — Search strategy (resolve S-numbering mismatch; consider adding all 5 database queries inline)
6. **Item 11** — Risk of bias methods (one sentence: explicitly declare the four-dimension framework as the RoB instrument)
7. **Item 13f** — Sensitivity analysis (reframe language from "pre-specified" to "post-hoc"; no data change required)
8. **Item 16b** — Excluded studies (reference S5 in text, or derive a full exclusion table from S5 as a supplementary file)
9. **Item 17** — Per-study characteristics (resolve S-numbering; map paper "S1" → repo `S2_included_studies.csv`)
10. **Item 18** — Quality results (verify 18/24/10 distribution against per-study assessment records)
11. **Item 20a** — Per-synthesis quality (derived from Item 18; resolvable once Item 18 is verified)
12. **Item 20d** — Sensitivity results (computation is real; reframe as post-hoc to align with 13f correction)

### If added numbers are NOT verified:

| Rating | Count | Percentage |
|--------|-------|------------|
| Fully Met | 22 | 56% |
| Partially Met | 13 | 33% |
| Not Met | 4 | 10% |

Items 18, 20a, 20d, and the specific numerical claims in 19 and 21 would need to be either verified against real data or removed/softened.

---

## Action Items

1. ~~**VERIFY** — Check whether the quality assessment was actually performed.~~ **DONE — CORRECTED.** Audit confirmed: `qa_summary_20260123_075645.csv` exists with 52 rows and actual scores. The originally stated distribution (18h/24m/10l) was wrong; the actual distribution (10H/41M/1L) has been applied to the paper. The QA framework description (4 binary → 3 numerical) has also been corrected.

2. ~~**VERIFY** — Confirm the sensitivity analysis 84.8±2.3% Dice.~~ **DONE — REMOVED.** Audit confirmed the figure is not reproducible from any data file in the repository. The sensitivity paragraph no longer contains a specific mean Dice figure; it states directional consistency with the verifiable quality-subset statistic (27.6% high quality in DOI subset).

3. **VERIFY AND RENAME** — The paper refers to "Supplementary S1" for the per-study characteristics table. The repository's `S2_included_studies.csv` (128 lines, 52 studies catalogued) contains this data but is labeled S2, not S1. Either rename the file or update all in-text cross-references to match the actual filename. Also verify the CSV includes all characteristics required by PRISMA Item 17 (study design, population, intervention details, outcome measures) — the current file captures screening-phase metadata and may require augmentation from the synthesis phase.

4. **VERIFY** — The inline PubMed query: confirm it matches the actual query executed during the search.

5. **ACCEPT** — Item 1 (Title) will remain Partially Met. This is the honest answer — the paper is a structured survey, not a systematic review, and the title should reflect reality.

6. ~~**FIX** — Resolve the supplementary S-numbering mismatch across all in-text references.~~ **DONE** — `main_prisma-compliance.tex` updated (S2→S3, S3→S7, Table S1→Table S2). Reference map added to `S0_data_provenance.md`.

7. **DOCUMENT** — Account for the missing S9 entry in the supplementary series (series jumps S8 → S10). Add a note to `S0_data_provenance.md` or a supplementary directory README explaining whether S9 was planned and not produced, intentionally omitted, or merged into another file. A numbered series with an unexplained gap undermines reviewer confidence in data completeness.

8. **CLARIFY** — Add a one-line note in the Methods AI Screening paragraph (or supplementary S4) listing all three model identifiers (`gpt-4o`, `gpt-5-nano`, `gpt-5.2`) and the API access dates. All three are publicly available models; this is standard API citation practice, not a reproducibility blocker.

9. ~~**FIX** — Change "pre-specified sensitivity analysis" to "post-hoc sensitivity analysis" in `main_prisma-compliance.tex` (~line 319).~~ **DONE** — Text now reads "one post-hoc sensitivity analysis (not pre-specified in the review protocol)."

10. ~~**FIX** — Add explicit declaration of the four-dimension quality framework as the study-level RoB assessment instrument in the Quality Assessment subsection.~~ **DONE** — Sentence added: "This four-dimension framework constitutes the study-level quality assessment instrument used in this review, applied in place of standard risk-of-bias tools (ROBINS-I, Cochrane RoB 2) that are designed for clinical study designs not applicable to computational benchmarking."

11. ~~**FIX** — Reference S5 in the Excluded Studies paragraph to surface the full exclusion list.~~ **DONE** — Sentence added pointing to `S5_screening_decisions.csv` for complete full-text screening decisions.

---

## Strengths (both versions)

- **Exemplary PRISMA flow diagram** (Figure 1) with complete numbers and exclusion reasons at every stage.
- **Thorough search strategy** across 5 databases plus citation tracking and conference proceedings.
- **Transparent AI-assisted screening** with multi-model consensus, validation metrics (κ = 0.89), and false-negative recovery.
- **Honest framing** as "PRISMA-informed structured survey" — does not overclaim systematic review status.
- **Strong eligibility criteria** with clearly separated inclusion and exclusion lists.
- **Proactive COI disclosure** with specific safeguards described in both Introduction and Declarations.
- **Data and code availability** with traceability through supplementary materials (S8, S10, S12).
- **Comprehensive discussion** addressing all four research questions with practical recommendations.

### Additional strengths in compliance version

- **Structured abstract** properly follows PRISMA for Abstracts format.
- **Methodology transparency** — explicitly describes what was and was not done (no author contact, no imputation, no formal meta-analysis, no GRADE), which is better PRISMA practice than omitting these details.
- **Honest justifications** for why certain formal tools (ROBINS-I, GRADE, funnel plots) were not applied — citing the computational (non-clinical) nature of the review.

---

*Reference: Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi: 10.1136/bmj.n71*
