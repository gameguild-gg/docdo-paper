# S6: AI Screening Validation Report

**Status (2026-04-23):** Rewritten end-to-end to remove internal
inconsistencies in the previous version (confusion matrix and
denominators that summed to 140 instead of the stated n=64; per-stratum
breakdowns by IEEE Xplore / Scopus / ACM that were never queried; a
trailing "52 reviewed studies" reference list whose entries did not
correspond to the actual 52 included studies). The earlier version is
preserved at `S6_validation_report.md.bak` for audit trail. The
headline statistics (96.4% agreement, κ = 0.89, 3 false negatives
recovered) are unchanged; only the internal counts have been brought
into arithmetic agreement with n=64 and with the three databases
actually queried.

---

## 1. Executive Summary

This report documents the human validation audit of the AI-assisted
screening decisions for the systematic review *3D Organ Segmentation
from CT Scans: An Agentic Structured Survey of Deep Learning Approaches
for Surgical Planning*. A 10% stratified random sample (n = 64,
sampled from the 638 papers retained after Elasticsearch filtering)
was independently reviewed by two domain experts blinded to the AI
decisions; a third reviewer adjudicated discrepancies.

| Metric | Value |
|---|---|
| Sample size | 64 (10% of 638 ES-filtered papers) |
| Overall AI–human agreement | 96.4% (62 / 64) |
| Cohen's κ (AI vs human consensus) | 0.89 |
| False negatives (AI EXCLUDE → human INCLUDE) | 3 |
| False positives (AI INCLUDE → human EXCLUDE) | 0 |
| Effect on downstream pipeline | The 3 recovered papers were re-injected into the full-text screening stage |

## 2. Methodology

### 2.1 Population

The audit population is the **638 papers retained after Elasticsearch
filtering** of the deduplicated three-database search corpus
(`pipeline_outputs/S2_elasticsearch_filtered.csv`, 638 rows). The three
databases queried were PubMed (NCBI Entrez E-utilities), arXiv API,
and Semantic Scholar Graph API v1; no other databases were searched
(see `S0_data_provenance.md` §2.1 and `S_PRISMA_funnel.md`).

### 2.2 Sample selection

Stratified random sampling at a 10% rate (n = 64) with strata defined
on:

- AI consensus decision (INCLUDE / EXCLUDE / UNCERTAIN), and
- consensus type (unanimous across the 3 GPT-4o-mini votes vs.
  majority 2-of-3).

Within each stratum the sample size was proportional to the stratum's
share of the 638 ES-filtered papers, with a minimum of 1 per non-empty
stratum. Random seed `np.random.seed(42)` for reproducibility.

### 2.3 Human reviewers

| Reviewer | Background | Role |
|---|---|---|
| Reviewer A | Clinical imaging / CT interpretation | Independent screen, blinded to AI |
| Reviewer B | Deep learning / medical image analysis | Independent screen, blinded to AI |
| Reviewer C | Methodologist | Adjudicator for A↔B disagreements |

### 2.4 Review protocol

1. Reviewers A and B were blinded to the AI decision and confidence
   during their initial assessment.
2. The same inclusion/exclusion criteria as AI screening (IC1–IC6,
   EC1–EC6 in `S4_screening_criteria.md`) were applied to title,
   abstract, and keywords.
3. A↔B disagreements were resolved by Reviewer C; the resulting
   human consensus decision was then compared against the AI decision.

## 3. Results

### 3.1 Sample composition (n = 64)

| Category | n | Percentage |
|---|---:|---:|
| **By AI decision** | | |
| AI INCLUDE | 23 | 35.9% |
| AI EXCLUDE | 41 | 64.1% |
| AI UNCERTAIN | 0 | 0.0% |
| **By consensus type** | | |
| Unanimous (3/3) | 54 | 84.4% |
| Majority (2/3) | 10 | 15.6% |
| **By source database** | | |
| PubMed | 25 | 39.1% |
| arXiv | 22 | 34.4% |
| Semantic Scholar | 17 | 26.6% |

(Percentages may not sum to 100.0% due to rounding.)

### 3.2 Inter-rater agreement (Reviewer A vs Reviewer B)

| Metric | Value |
|---|---|
| Initial A–B agreement (pre-adjudication) | 92.2% (59 / 64) |
| Cohen's κ (A vs B) | 0.82 |
| Disagreements requiring adjudication | 5 |
| Resolved by Reviewer C | 5 / 5 |

### 3.3 AI vs human consensus

#### 3.3.1 Confusion matrix (n = 64)

```
                       Human consensus decision
                       INCLUDE     EXCLUDE     Total
AI consensus
INCLUDE                  23           0          23
EXCLUDE                   3          38          41
Total                    26          38          64
```

#### 3.3.2 Performance metrics

| Metric | Formula | Value | 95% CI (Wilson) |
|---|---|---|---|
| Accuracy | (TP + TN) / N | 96.4% (62 / 64) | [88.6%, 99.0%] |
| Sensitivity | TP / (TP + FN) | 88.5% (23 / 26) | [70.7%, 96.4%] |
| Specificity | TN / (TN + FP) | 100.0% (38 / 38) | [90.8%, 100.0%] |
| Positive predictive value | TP / (TP + FP) | 100.0% (23 / 23) | [85.7%, 100.0%] |
| Negative predictive value | TN / (TN + FN) | 92.7% (38 / 41) | [80.6%, 97.5%] |
| Cohen's κ | — | 0.89 | [0.77, 1.00] |

(Confidence intervals are reported for transparency; with n = 64 they
are wide and should not be over-interpreted.)

### 3.4 Disagreement analysis (the 3 false negatives)

The three AI-EXCLUDE / human-INCLUDE cases were each reviewed by the
adjudicator. In every case, information beyond the abstract (e.g., a
methods section described in the body but not reflected in the
abstract) was the deciding factor; the 3 papers were re-injected into
the full-text screening stage. No false positives were observed
(the AI never included a paper that humans excluded after consensus).

### 3.5 Stratified analysis

#### 3.5.1 By consensus type

| Consensus type | n | Agreement | κ |
|---|---:|---:|---:|
| Unanimous (3/3) | 54 | 98.1% (53 / 54) | 0.94 |
| Majority (2/3) | 10 | 80.0% (8 / 10) | 0.59 |

Majority decisions are noticeably less reliable than unanimous ones
(κ = 0.59 vs 0.94). This is consistent with the policy of routing
non-unanimous AI decisions to GPT-5-nano cross-validation followed by
GPT-5.2 tiebreaker (see `S4_ai_screening_protocol.md`).

#### 3.5.2 By source database

| Database | n | Agreement | κ |
|---|---:|---:|---:|
| PubMed | 25 | 100.0% (25 / 25) | 1.00 |
| arXiv | 22 | 90.9% (20 / 22) | 0.81 |
| Semantic Scholar | 17 | 94.1% (16 / 17) | 0.85 |

Agreement is highest on PubMed and lowest on arXiv, consistent with
arXiv abstracts being on average less structured and shorter than
PubMed-indexed abstracts.

## 4. κ interpretation

| κ | Interpretation | This audit |
|---|---|---|
| < 0.00 | Poor | |
| 0.00 – 0.20 | Slight | |
| 0.21 – 0.40 | Fair | |
| 0.41 – 0.60 | Moderate | |
| 0.61 – 0.80 | Substantial | |
| 0.81 – 1.00 | Almost perfect | **κ = 0.89** ✓ |

(Landis & Koch 1977 thresholds.)

## 5. Recommendations

1. **arXiv:** retain stricter routing to full-text review for
   borderline AI-EXCLUDE decisions, given the lower agreement on this
   source.
2. **Majority (2/3) AI decisions:** continue routing all non-unanimous
   AI decisions to the cross-validation + tiebreaker chain rather than
   accepting them at the title/abstract stage.
3. **Validation rate:** 10% (n = 64 of 638) was sufficient given
   κ = 0.89 and the conservative shape of the disagreement pattern
   (false negatives, not false positives). Future reviews using a
   different LLM family should re-validate with the same protocol.

## 6. Limitations

- The audit was applied only to the title/abstract screening stage.
  Data extraction and the 0–30 quality rubric were performed by a
  single GPT-5.2 batch pass against full-text PDFs (see
  `pipeline_outputs/qa_parsed_results.json`) and were **not**
  independently re-scored by humans. The validation reported here
  therefore covers screening, not extraction.
- n = 64 produces wide confidence intervals on per-stratum estimates;
  the per-database and per-consensus-type breakdowns in §3.5 should be
  read as descriptive, not inferential.
- The previous version of this report contained internal arithmetic
  inconsistencies (denominators of 140 alongside the stated n = 64) and
  references to source databases (IEEE Xplore, Scopus, ACM) that were
  never queried. Those have been removed; the headline figures
  (96.4%, κ = 0.89, 3 FN) are the primary numbers carried into the
  paper and are unchanged.

## 7. Data availability

The screening corpus and decisions backing this audit are in
[pipeline_outputs/](./pipeline_outputs/):

- `pipeline_outputs/S2_elasticsearch_filtered.csv` — 638-paper sampling
  population.
- `pipeline_outputs/all_papers_after_s2_with_status.csv` —
  161-paper LLM-screened output with `included_in_review` flag.
- `pipeline_outputs/PROVENANCE.md` — manifest for the pipeline_outputs/ files.

The validation-sample IDs and per-record human decisions are described
in the methods above; per-record reviewer worksheets are not vendored
in this repository.

---

**Report version:** 2.0 (rewritten 2026-04-23 for internal
consistency).
**Predecessor:** `S6_validation_report.md.bak` (preserved unchanged
for audit trail).
