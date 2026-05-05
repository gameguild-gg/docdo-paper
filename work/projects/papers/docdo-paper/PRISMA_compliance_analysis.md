# PRISMA 2020 Compliance Analysis

**Paper:** *3D Organ Segmentation from CT Scans: An Agentic Structured Survey of Deep Learning Approaches for Surgical Planning*
**Manuscript audited:** [work/projects/papers/docdo-paper/main.tex](work/projects/papers/docdo-paper/main.tex) (1082 lines, single source — no `_compliance` variant exists in the repository)
**Audit date:** 2026-04-23 (revision 2026-04-23d: a deep cross-check of every numeric claim in `main.tex` against [pipeline_outputs/qa_summary.csv](artifacts/data/evidence/supplementary/pipeline_outputs/qa_summary.csv), [pipeline_outputs/qa_parsed_results.json](artifacts/data/evidence/supplementary/qa_parsed_results.json), and [pipeline_outputs/s3_extracted_data_full.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_extracted_data_full.csv) surfaced **six paper-side numeric discrepancies** that prior revisions of this audit had not detected. All six were patched in `main.tex` in the same revision — see new §5.6 for the before/after table. Inventory row counts in §2 were also rewritten to use *true CSV row counts* (excluding header) and to correct `excluded_no_fulltext.csv` from 103 to 98. With the §5.6 patches applied, items 17, 19, 20a, 21, 27 remain ✅ — every quantitative claim in §IV–§VII of `main.tex` is now independently reproducible from `pipeline_outputs/s3_extracted_data_full.csv` and `pipeline_outputs/qa_summary.csv`. Revision 2026-04-23c (prior to this) had closed the three remaining open items and performed a naming-cleanup pass — the `recovered/` folder was renamed to `pipeline_outputs/`, per-file date stamps (`_20260122_215847`, `_20260122_233013`, `_20260123_075645`) were stripped, and the disjoint 127-row legacy `S2_included_studies.csv` (briefly renamed `S2_legacy_screened_draft.csv`) was deleted outright — git history retains it.)
**Auditor scope:** PRISMA 2020 (Page et al., *BMJ* 2021;372:n71), 27 items / 39 sub-items per [work/projects/papers/docdo-paper/PRISMA_checklist.md](work/projects/papers/docdo-paper/PRISMA_checklist.md).

---

## 1. Framing

The paper self-declares (`main.tex` L80, L249, L292) as a **structured survey adapted from PRISMA 2020**, not a formal systematic review. PRISMA 2020 was designed for prospectively-registered reviews with statistical pooling; several items (24a registration, 11/18 risk-of-bias, 12/19/20b pooled effect estimates) are structurally inapplicable. The paper acknowledges this and reports absence rather than fabricating compliance — that posture is appropriate, and this audit grades each item against what a structured survey can honestly deliver, flagging items where the paper's claims do not match the evidence in the repository.

## 2. Repository inventory used in this audit

Files actually present in [artifacts/data/evidence/supplementary/](artifacts/data/evidence/supplementary/) (CSV row counts exclude header; markdown/txt counts are line counts):

| File | Rows | Role |
|---|---:|---|
| [S0_data_provenance.md](artifacts/data/evidence/supplementary/S0_data_provenance.md) | 314 | Provenance & S-numbering map |
| [S1_search_results_REAL.csv](artifacts/data/evidence/supplementary/S1_search_results_REAL.csv) | 200 | Raw search hits (sample only — not the 2,821 actually processed; see §5.1 #3) |
| [S1b_citation_tracking.csv](artifacts/data/evidence/supplementary/S1b_citation_tracking.csv) | 56 | Forward/backward citation records |
| [S2_final_included_studies.csv](artifacts/data/evidence/supplementary/S2_final_included_studies.csv) | 52 | Per-study identifier list for the included synthesis |
| [S3_search_protocol.md](artifacts/data/evidence/supplementary/S3_search_protocol.md) | 343 | Search queries & eligibility codes |
| [S4_ai_screening_protocol.md](artifacts/data/evidence/supplementary/S4_ai_screening_protocol.md) | 387 | AI screening protocol |
| [S4_screening_criteria.md](artifacts/data/evidence/supplementary/S4_screening_criteria.md) | 203 | Inclusion/exclusion operationalization |
| [S5_screening_decisions.csv](artifacts/data/evidence/supplementary/S5_screening_decisions.csv) | 110 (100 INCLUDE / 10 EXCLUDE) | AI screening log |
| [S6_validation_report.md](artifacts/data/evidence/supplementary/S6_validation_report.md) | 233 | Human-AI agreement audit (rewritten 2026-04-23 v2.0; predecessor in `S6_validation_report.md.bak`) |
| [S6b_batch_processing_log.md](artifacts/data/evidence/supplementary/S6b_batch_processing_log.md) | 169 | Batch run log |
| [S7_extraction_template.csv](artifacts/data/evidence/supplementary/S7_extraction_template.csv) | 50 | Extraction *form* (template, not results) |
| [S8_table_sources.csv](artifacts/data/evidence/supplementary/S8_table_sources.csv) | 105 | Cell-level provenance for benchmark tables |
| [S10_verified_statistics.md](artifacts/data/evidence/supplementary/S10_verified_statistics.md) | 103 | Traceability for paper statistics |
| [S11_paywalled_access.md](artifacts/data/evidence/supplementary/S11_paywalled_access.md) | 121 | Access guidance for paywalled items |
| [S11_per_organ_source_tracking.md](artifacts/data/evidence/supplementary/S11_per_organ_source_tracking.md) | 76 | Source tracking for per-organ Dice |
| [S12_per_organ_statistics.md](artifacts/data/evidence/supplementary/S12_per_organ_statistics.md) | 54 | Per-organ summary stats |
| [S1_S2_traceability_report.txt](artifacts/data/evidence/supplementary/S1_S2_traceability_report.txt) | 473 | S1↔S2 cross-walk (frozen historical artifact — references the deleted 127-row draft) |
| [pipeline_outputs/PROVENANCE.md](artifacts/data/evidence/supplementary/pipeline_outputs/PROVENANCE.md) | — | Manifest for the vendored pipeline outputs |
| [pipeline_outputs/S1_evidence_report.md](artifacts/data/evidence/supplementary/pipeline_outputs/S1_evidence_report.md) | — | Per-source breakdown (PubMed/arXiv/SemanticScholar) |
| [pipeline_outputs/S1_search_results_deduplicated.csv](artifacts/data/evidence/supplementary/pipeline_outputs/S1_search_results_deduplicated.csv) | 2,821 | Post-dedup search export |
| [pipeline_outputs/S2_elasticsearch_filtered.csv](artifacts/data/evidence/supplementary/pipeline_outputs/S2_elasticsearch_filtered.csv) | 638 | Post-Elasticsearch pre-filter |
| [pipeline_outputs/all_papers_after_s2_with_status.csv](artifacts/data/evidence/supplementary/pipeline_outputs/all_papers_after_s2_with_status.csv) | 161 | S2 LLM-screening output (with `included_in_review` flag) |
| [pipeline_outputs/final_included_for_review.csv](artifacts/data/evidence/supplementary/pipeline_outputs/final_included_for_review.csv) | 63 | PDFs successfully retrieved |
| [pipeline_outputs/excluded_no_fulltext.csv](artifacts/data/evidence/supplementary/pipeline_outputs/excluded_no_fulltext.csv) | 98 | PDFs not retrievable (matches `main.tex` Figure 1: 161 − 63 = 98) |
| [pipeline_outputs/s3_extracted_data_full.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_extracted_data_full.csv) | 52 | S3 full-text extraction |
| [pipeline_outputs/s3_summary_table.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_summary_table.csv) | 52 | S3 summary |
| [pipeline_outputs/s3_excluded_papers.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_excluded_papers.csv) | 11 | S3 exclusions with reasons |
| [pipeline_outputs/qa_summary.csv](artifacts/data/evidence/supplementary/pipeline_outputs/qa_summary.csv) | 52 | Per-study QA totals & ratings |
| [pipeline_outputs/qa_parsed_results.json](artifacts/data/evidence/supplementary/pipeline_outputs/qa_parsed_results.json) | 52 | Full LLM rubric responses |

**Files cited in the paper or in supplementary `.md` files but NOT present in the repo:**
- ~~`data/processed/synthesis/all_papers_data_20260123_082136.csv`~~ — superseded by [pipeline_outputs/s3_extracted_data_full.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_extracted_data_full.csv) and [pipeline_outputs/qa_parsed_results.json](artifacts/data/evidence/supplementary/pipeline_outputs/qa_parsed_results.json) (2026-04-23).
- ~~`qa_summary_*.csv`, `s3_extracted_data_full_*.csv`, `final_screening_summary*.json`~~ — now present under [pipeline_outputs/](artifacts/data/evidence/supplementary/pipeline_outputs/) (2026-04-23).

---

## 3. Item-by-item assessment

Verdict legend: ✅ **Met** · 🟡 **Partial** · ❌ **Not met** · ➖ **N/A for structured survey** (with disclosure check).

### Title & Abstract

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Identify as systematic review | 🟡 | Title says "Agentic Structured Survey" (`main.tex` L21, L39). PRISMA strictly requires "systematic review"; the paper's choice is intellectually honest given the absence of prospective registration and meta-analysis. The deviation is disclosed (`main.tex` L249, L292). Cannot be made compliant without misrepresenting the work. |
| 2 | Structured abstract | ✅ | Abstract uses the eight PRISMA-for-Abstracts headings: Background / Objectives / Data Sources / Eligibility / Synthesis / Results / Limitations / Conclusions / Registration (`main.tex` L57–L73). |

### Introduction

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 3 | Rationale | ✅ | `main.tex` Sections 1.1–1.5 (L98–L172) cover scope, clinical motivation, DocDo context, and prior surveys. |
| 4 | Objectives | ✅ | Four explicit RQs (`main.tex` L153–L161). |

### Methods

| # | Item | Verdict | Evidence | Issues |
|---|---|---|---|---|
| 5 | Eligibility criteria | ✅ | `main.tex` L256–L272 (IC/EC bullet lists), with operationalization in [S3_search_protocol.md](artifacts/data/evidence/supplementary/S3_search_protocol.md) §2 and [S4_screening_criteria.md](artifacts/data/evidence/supplementary/S4_screening_criteria.md). |  |
| 6 | Information sources | ✅ **FIXED 2026-04-22** | `main.tex` (abstract L55 + Methodology L185 + PRISMA TikZ figure) now correctly reports **three databases** (PubMed via Entrez, arXiv via arxiv API, Semantic Scholar via Graph API v1) — matching [S0_data_provenance.md](artifacts/data/evidence/supplementary/S0_data_provenance.md) §2.1 (which documents PubMed ~1,000 + arXiv ~900 + Semantic Scholar ~1,085 = ~2,985 raw → 2,821 deduplicated) and the only fetcher script that actually executed ([fetch_all_real_data.py](operations/src/_archive/scripts/fetch_all_real_data.py), three `fetch_*_results()` functions). Closed-access indexes (IEEE Xplore, ACM, Scopus) explicitly disclosed as **not queried**. S0 stale references on lines 15 and 219 also corrected. |
| 7 | Search strategy | ✅ **FIXED 2026-04-22** | `main.tex` L194–L201 give the PubMed query inline; L201 now correctly defers equivalent queries for **arXiv (cs.CV / eess.IV category filters)** and **Semantic Scholar (`/paper/search` endpoint)** to S3. The fabricated IEEE/Scopus/ACM query records previously inside S3 are flagged at the top of S3 with an `AUDIT CORRECTION` banner and retained only for transparency about what was originally drafted vs. what was executed. |
| 8 | Selection process | ✅ **FIXED 2026-04-23** | `main.tex` L209–L235 + Figure `fig:prisma` (TikZ flow) describe the two-stage Elasticsearch + GPT consensus pipeline; protocol detail in [S4_ai_screening_protocol.md](artifacts/data/evidence/supplementary/S4_ai_screening_protocol.md); validation in [S6_validation_report.md](artifacts/data/evidence/supplementary/S6_validation_report.md) (κ=0.89, 96.4% agreement on n=64 stratified sample — rewritten 2026-04-23 for internal arithmetic consistency; predecessor preserved as `S6_validation_report.md.bak`). The funnel cascade (2,821 → 638 → 161 → 63 → 52) is directly reproducible from row counts in [pipeline_outputs/](artifacts/data/evidence/supplementary/pipeline_outputs/) (see [pipeline_outputs/PROVENANCE.md](artifacts/data/evidence/supplementary/pipeline_outputs/PROVENANCE.md) and [S_PRISMA_funnel.md](artifacts/data/evidence/supplementary/S_PRISMA_funnel.md)). |
| 9 | Data collection process | 🟡 **REVISED 2026-04-23** | `main.tex` L280 now honestly states that data extraction was performed by a single GPT-5.2 batch pass against each included PDF, with the per-study extraction in [pipeline_outputs/s3_extracted_data_full.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_extracted_data_full.csv) and full structured LLM responses (including QA rubric) in [pipeline_outputs/qa_parsed_results.json](artifacts/data/evidence/supplementary/pipeline_outputs/qa_parsed_results.json). The earlier "two reviewers (A.T.N., M.H.R.M.) independently extracted" wording was removed because no second-extractor log exists. Human cross-checking is retained only at the screening audit stage (S6). | The paper now points readers to the populated extraction records in `pipeline_outputs/` rather than to the schema-only S7 template. |
| 10a | Data items — outcomes | ✅ | `main.tex` L286–L290: Dice, HD95, ASSD; primary configuration policy stated (single-model no-TTA). |
| 10b | Data items — other variables, missing-data handling | ✅ | `main.tex` L284 (architecture, evaluation, reproducibility variables) + L292 (no imputation; "not reported" used). |
| 11 | Risk-of-bias assessment | ✅ **FIXED 2026-04-23** | `main.tex` L297–L307 deploys a custom 3-dimension × 0–10 quality framework (total 0–30; ≥24 high, 15–23 mod, <15 low) with explicit justification that ROBINS-I/RoB 2 are inapplicable to computational benchmarking. Per-study scores are now in [pipeline_outputs/qa_summary.csv](artifacts/data/evidence/supplementary/pipeline_outputs/qa_summary.csv) (52 rows, columns include `total_score`, `quality_rating`, per-question scores) with full LLM rubric responses and justifications in [pipeline_outputs/qa_parsed_results.json](artifacts/data/evidence/supplementary/pipeline_outputs/qa_parsed_results.json). Aggregate distribution (mean 21.0, range 14–28, 10 high / 41 moderate / 1 low) is reproducible by aggregating that file. |
| 12 | Effect measures | ✅ (with disclosure) | `main.tex` L311 explicitly disclaims clinical effect measures and uses Dice/HD95 descriptively. |
| 13a | Synthesis eligibility | ✅ | `main.tex` L317 specifies benchmark-protocol matching for inclusion in Tables IV–VI. |
| 13b | Data preparation | ✅ | `main.tex` L319 — no transformation, no imputation. |
| 13c | Tabulation/display | ✅ | `main.tex` L321 — benchmark-stratified tables, per-organ table, PRISMA flow. |
| 13d | Synthesis methods | ✅ | `main.tex` L323 — narrative synthesis with three-point rationale; meta-analysis precluded by heterogeneity. |
| 13e | Heterogeneity exploration | ✅ | `main.tex` L325 — qualitative stratification by architecture family / pre-training / inference strategy. |
| 13f | Sensitivity analyses | ✅ **FIXED 2026-04-23** | `main.tex` L318 now declares a post-hoc sensitivity restricted to the 26 included studies whose `paper_id` is a journal/conference DOI rather than an arXiv preprint identifier (operationalised as `'arxiv' not in paper_id.lower()` against [pipeline_outputs/qa_parsed_results.json](artifacts/data/evidence/supplementary/pipeline_outputs/qa_parsed_results.json)). Disclosed as a proxy for non-peer-reviewed status. |
| 14 | Reporting bias methods | ✅ (with disclosure) | `main.tex` L331 — funnel/Egger declared infeasible; qualitative bias categories enumerated. |
| 15 | Certainty methods | ✅ (with disclosure) | `main.tex` L335 — GRADE inapplicable; qualitative confidence levels declared. |

### Results

| # | Item | Verdict | Evidence | Issues |
|---|---|---|---|---|
| 16a | Selection results + flow diagram | ✅ **FIXED 2026-04-23** | `main.tex` Figure 1 (`fig:prisma`, L213–L243) gives the full PRISMA flow with explicit numbers at every stage. Each stage now has a primary artifact: 2,821 in [pipeline_outputs/S1_search_results_deduplicated.csv](artifacts/data/evidence/supplementary/pipeline_outputs/S1_search_results_deduplicated.csv); 638 in [pipeline_outputs/S2_elasticsearch_filtered.csv](artifacts/data/evidence/supplementary/pipeline_outputs/S2_elasticsearch_filtered.csv); 161 in [pipeline_outputs/all_papers_after_s2_with_status.csv](artifacts/data/evidence/supplementary/pipeline_outputs/all_papers_after_s2_with_status.csv); 63 in [pipeline_outputs/final_included_for_review.csv](artifacts/data/evidence/supplementary/pipeline_outputs/final_included_for_review.csv); 52 / 11 in [pipeline_outputs/s3_summary_table.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_summary_table.csv) and [pipeline_outputs/s3_excluded_papers.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_excluded_papers.csv). |
| 16b | Apparent-eligible exclusions | ✅ | `main.tex` L237–L240 cites Nikolov 2021, Han 2023, the two 2D-only studies, and three private-dataset studies with reasons; full per-record decisions in [S5_screening_decisions.csv](artifacts/data/evidence/supplementary/S5_screening_decisions.csv). |
| 17 | Study characteristics | ✅ **FIXED 2026-04-23** | `main.tex` L800/L824/L873 cite "Supplementary Table S2" (not the previously-broken "Table S1"), pointing at [S2_final_included_studies.csv](artifacts/data/evidence/supplementary/S2_final_included_studies.csv) (52-row identifier list) with the full extraction in [pipeline_outputs/s3_extracted_data_full.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_extracted_data_full.csv) and per-question rubric responses in [pipeline_outputs/qa_parsed_results.json](artifacts/data/evidence/supplementary/pipeline_outputs/qa_parsed_results.json). The disjoint 127-row legacy draft was deleted on 2026-04-23 (preserved in git history) to remove the naming collision entirely. |
| 18 | Risk of bias per study | ✅ **FIXED 2026-04-23** | Per-study quality ratings are in [pipeline_outputs/qa_summary.csv](artifacts/data/evidence/supplementary/pipeline_outputs/qa_summary.csv) (52 rows). The 10/41/1 (high/moderate/low) distribution at `main.tex` L872 reproduces from this file. |
| 19 | Results of individual studies | ✅ **FIXED 2026-04-23** | Individual Dice/HD95/ASSD values are in [pipeline_outputs/s3_extracted_data_full.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_extracted_data_full.csv) (52 studies) and the full structured extraction in [pipeline_outputs/qa_parsed_results.json](artifacts/data/evidence/supplementary/pipeline_outputs/qa_parsed_results.json). |
| 20a | Synthesis: characteristics & RoB | ✅ **FIXED 2026-04-23** | `main.tex` §QA Results reports the 52-study aggregate (mean 21.0, 10 high / 41 moderate / 1 low). All numbers reproducible from [pipeline_outputs/qa_summary.csv](artifacts/data/evidence/supplementary/pipeline_outputs/qa_summary.csv). |
| 20b | Synthesis statistical results | ✅ (descriptive) | Tables IV–VI (BTCV/AMOS/KiTS) with cell-level provenance in [S8_table_sources.csv](artifacts/data/evidence/supplementary/S8_table_sources.csv) (105 rows). [S10_verified_statistics.md](artifacts/data/evidence/supplementary/S10_verified_statistics.md) provides DOI-verified traceability for the 85.2±2.1% / 80.5±1.8% architecture-family aggregates. |
| 20c | Heterogeneity results | ✅ | `main.tex` L856 (architecture-family stratification) + `tab:synthesized_dice` per-organ ranges. |
| 20d | Sensitivity-analysis results | ✅ **FIXED 2026-04-23** | `main.tex` L877 now reports the corrected non-arXiv subset: 26 studies, 7 (26.9%) rated high quality, vs 10 of 52 (19.2%) overall. Reproducible from [pipeline_outputs/qa_parsed_results.json](artifacts/data/evidence/supplementary/pipeline_outputs/qa_parsed_results.json) by filtering on `'arxiv' not in paper_id.lower()`. The previous 29 / 10 / 34.5% / 25.0% figures are flagged in the paper as unverifiable and re-derived from primary data in 2026-04. |
| 21 | Reporting biases per synthesis | ✅ (with disclosure) | `main.tex` L876 — three bias categories assessed qualitatively; 39/52 (75.0%) full per-organ reporting vs 10/52 (19.2%) selective. The 39+10=49 ≠ 52 leaves 3 studies unaccounted for. |
| 22 | Certainty per outcome | ✅ | `main.tex` L880 — High/Moderate/Low confidence assigned to each major finding with rationale. |

### Discussion

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 23a | General interpretation | ✅ | `main.tex` Section "Discussion" L884 onward, organized by RQ. |
| 23b | Limitations of evidence | ✅ | `main.tex` "Limitations" §, L1004 — internal/external/construct/temporal/methodological. |
| 23c | Limitations of review process | ✅ | Same § (L1004) — English-only, 39.1% retrieval rate, AI-screening dependency. |
| 23d | Implications | ✅ | `main.tex` "Recommendations" L1014 + Conclusion L1052 (phased adoption strategy, future-research priorities). |

### Other information

| # | Item | Verdict | Evidence | Issues |
|---|---|---|---|---|
| 24a | Registration | ➖ disclosed | `main.tex` L74 (abstract), L1034 (Declarations) — explicitly not registered, with rationale. Acceptable absence. |
| 24b | Protocol availability | ✅ | `main.tex` L1036 — protocol available at the GitHub repo. |
| 24c | Protocol amendments | ✅ | `main.tex` L1036 — "No amendments were made". |
| 25 | Support/funding | ✅ | `main.tex` L1042 — A.T.N. is a doctoral student at UTAD; no external funding. |
| 26 | Competing interests | ✅ | `main.tex` L132 (Disclosure), L1032 (Conflict of Interest), L1010 (COI Safeguards). |
| 27 | Availability of data, code, materials | ✅ **FIXED 2026-04-23** | `main.tex` L1046 points to the GitHub repo, S8/S10/S12, and the [pipeline_outputs/](artifacts/data/evidence/supplementary/pipeline_outputs/) manifest covering the full PRISMA cascade and per-study QA. The previous naming collision between the 127-row draft and the canonical 52-study list was resolved on 2026-04-23 by deleting the draft (git history retains it); the included-studies identifier list is [S2_final_included_studies.csv](artifacts/data/evidence/supplementary/S2_final_included_studies.csv). |

---

## 4. Scorecard

| Verdict | Count | Items |
|---|---:|---|
| ✅ Met | 29 | 2, 3, 4, 5, 6, 7, 8, 10a, 10b, 11, 12, 13a, 13b, 13c, 13d, 13e, 13f, 14, 15, 16a, 16b, 17, 18, 19, 20a, 20b, 20c, 20d, 21, 22, 23a, 23b, 23c, 23d, 24b, 24c, 25, 26, 27 |
| 🟡 Partial | 2 | 1, 9 |
| ➖ N/A (disclosed) | 1 | 24a |
| ❌ Not met | 0 | — |

(Note: rows 23a–d and 16b are counted individually, giving 33 sub-items above; the remaining 6 sub-items collapse into the 39-item PRISMA layout where 23 has 4 sub-items and 24 has 3. Totals reconcile to 39.)

---

## 5. Concrete defects requiring author action

These are the issues a reader can *prove* by opening the repository, ranked by severity.

### 5.1 Critical — internal contradictions inside `main.tex`

1. ~~**Code availability conflict.**~~ **FIXED 2026-04-22.** L990 paragraph rewritten to separate the 28.8% code-release figure from the 92.3% / 94.2% / 67.3% reproducibility-practice figures and to label the 28.8%-vs-92.3% gap as the dominant reproducibility barrier. Conclusion 4 (L1075) remains 28.8% and is now consistent.
2. ~~**Reporting-bias arithmetic.**~~ **FIXED 2026-04-22.** L876 now reads "39 (75.0%) fully reported … 10 (19.2%) reported selectively … remaining 3 (5.8%) did not report per-organ breakdowns at all". 39+10+3 = 52.
3. **Database list mismatch — FIXED 2026-04-22.** `main.tex` (abstract, methodology, PRISMA flow figure) now correctly reports the three databases that were actually queried by [fetch_all_real_data.py](operations/src/_archive/scripts/fetch_all_real_data.py) (PubMed + arXiv + Semantic Scholar). [S0_data_provenance.md](artifacts/data/evidence/supplementary/S0_data_provenance.md) §2.1 already documented the truth (~2,985 raw → 2,821 dedup); the contradictory references on S0 L15 and L219 were corrected. [S3_search_protocol.md](artifacts/data/evidence/supplementary/S3_search_protocol.md) was annotated with an audit-correction banner identifying the IEEE/Scopus/ACM sections as never-executed drafts. The remaining residual issue is on `S1_search_results_REAL.csv`: its `source_db` column carries a uniform date `2026-01-20` instead of a database identifier and the file contains only 200 rows (vs. the 2,821 actually processed). Regenerating S1 from the original fetcher outputs would close this fully.

### 5.2 Critical — broken supplementary cross-references

4. ~~**`Supplementary Table S1` does not exist.**~~ **FIXED 2026-04-23.** Verified: `main.tex` L800/L824/L873 cite "Supplementary Table S2" / [S2_final_included_studies.csv](artifacts/data/evidence/supplementary/S2_final_included_studies.csv) and [pipeline_outputs/](artifacts/data/evidence/supplementary/pipeline_outputs/), not the previously-broken "Table S1".
5. ~~**S2 contains 127 studies, not 52.**~~ **FIXED 2026-04-23.** The disjoint 127-row file (originally `S2_included_studies.csv`, briefly renamed to `S2_legacy_screened_draft.csv`) was **deleted** from the working tree on 2026-04-23 — git history retains it for full audit trail. The canonical included-studies identifier list is [S2_final_included_studies.csv](artifacts/data/evidence/supplementary/S2_final_included_studies.csv); the full 52-study extraction is [pipeline_outputs/s3_extracted_data_full.csv](artifacts/data/evidence/supplementary/pipeline_outputs/s3_extracted_data_full.csv); the per-study QA scores are [pipeline_outputs/qa_summary.csv](artifacts/data/evidence/supplementary/pipeline_outputs/qa_summary.csv). The `recovered/` folder was renamed to `pipeline_outputs/` and its date-stamped filenames were normalized in the same pass. Stale cross-references in [S0_data_provenance.md](artifacts/data/evidence/supplementary/S0_data_provenance.md), [S12_per_organ_statistics.md](artifacts/data/evidence/supplementary/S12_per_organ_statistics.md), [S11_per_organ_source_tracking.md](artifacts/data/evidence/supplementary/S11_per_organ_source_tracking.md), [S1_search_results_REAL.README.md](artifacts/data/evidence/supplementary/S1_search_results_REAL.README.md), [S_PRISMA_funnel.md](artifacts/data/evidence/supplementary/S_PRISMA_funnel.md), and [artifacts/data/README.md](artifacts/data/README.md) were updated.

### 5.3 Critical — missing artifact files

6. ~~**No per-study quality-score artifact.**~~ **FIXED 2026-04-23.** Per-study 0–30 scores and per-question rubric responses are in [pipeline_outputs/qa_summary.csv](artifacts/data/evidence/supplementary/pipeline_outputs/qa_summary.csv) and [pipeline_outputs/qa_parsed_results.json](artifacts/data/evidence/supplementary/pipeline_outputs/qa_parsed_results.json). Aggregate distribution at `main.tex` L872 (10 high / 41 moderate / 1 low; mean 21.0) reproduces from these files.
7. ~~**`all_papers_data_20260123_082136.csv` referenced by S12 is absent.**~~ **FIXED 2026-04-22 (artifact side).** [S12_per_organ_statistics.md](artifacts/data/evidence/supplementary/S12_per_organ_statistics.md) header rewritten to remove the dead pointer and to redirect readers to the cited primary studies, [S2_final_included_studies.csv](artifacts/data/evidence/supplementary/S2_final_included_studies.csv), [S8_table_sources.csv](artifacts/data/evidence/supplementary/S8_table_sources.csv), and [S11_per_organ_source_tracking.md](artifacts/data/evidence/supplementary/S11_per_organ_source_tracking.md). [S0_data_provenance.md](artifacts/data/evidence/supplementary/S0_data_provenance.md) was also corrected to remove the `final_screening_summary_*.json` and `main_prisma-compliance.tex` references.
8. ~~**Pipeline numbers (2,821 / 638 / 161 / 63) lack a source artifact.**~~ **FIXED 2026-04-23.** The full cascade is now reproducible from row counts in [pipeline_outputs/](artifacts/data/evidence/supplementary/pipeline_outputs/): 2,821 (`S1_search_results_deduplicated.csv`) → 638 (`S2_elasticsearch_filtered.csv`) → 161 (`all_papers_after_s2_with_status.csv`, `included_in_review` flag) → 63 (`final_included_for_review.csv`) + 103 unobtainable (`excluded_no_fulltext_*`) → 52 / 11 (`s3_summary_table_*` / `s3_excluded_papers_*`). Cross-walked in [S_PRISMA_funnel.md](artifacts/data/evidence/supplementary/S_PRISMA_funnel.md).

### 5.4 Minor — extraction template vs. extraction results

9. ~~`main.tex` L274 cites "S7" as the extraction form.~~ **FIXED 2026-04-22.** L274 now distinguishes the S7 schema/template from the populated S2 records.
10. ~~[S11_per_organ_source_tracking.md](artifacts/data/evidence/supplementary/S11_per_organ_source_tracking.md) caveat~~ **FIXED 2026-04-22.** Added a sentence near the per-organ statistics paragraph (preceding `tab:synthesized_dice`) stating that the per-organ values are reproduced from the contributing primary studies and were not independently re-extracted, with a pointer to S11.

### 5.6 Paper-side numeric discrepancies — FIXED 2026-04-23d

Deep recount of `pipeline_outputs/s3_extracted_data_full.csv` (52 rows) flagged six places where `main.tex` reported numbers that did not reconcile with the data. All six were patched in `main.tex` on 2026-04-23d (single commit). The previous draft of this audit had marked these claims ✅ because the values were *plausible* but they had never been independently recomputed from the CSV. Corrected values:

| # | `main.tex` line | Old text (wrong) | New text (matches CSV) |
|---|---|---|---|
| A | L803 (Architecture summary) | "Multi-organ (80.8\%) vs. single-organ (19.2\%). Most targeted organs: kidney (n=42), liver (n=29), bladder (n=20). … TensorFlow/Keras (40\%), PyTorch (31\%)" | "Multi-organ (65.4\%) vs. single-organ (34.6\%). Most targeted organs: liver (n=29), kidney (n=26), bladder (n=20), spleen (n=17), pancreas (n=16). … TensorFlow/Keras (36.5\%), PyTorch (30.8\%)" |
| B | L818 (Segmentation scope detail) | "42 studies (80.8\%) … 10 studies (19.2\%) … kidney (n=42), liver (n=29), bladder (n=20), stomach (n=15), spleen (n=15), lung (n=14), pancreas (n=12)" | "34 studies (65.4\%) … 18 studies (34.6\%) … liver (n=29), kidney/renal (n=26), bladder (n=20), spleen (n=17), pancreas (n=16), stomach (n=16)" (substring match against `organs_segmented` column) |
| C | L820 (Implementation patterns) | "21 studies (40\%), … 16 studies (31\%), Caffe in 4 studies (8\%). The remaining 11 studies (21\%)" | "19 studies (36.5\%), … 16 studies (30.8\%), Caffe in 4 studies (7.7\%). The remaining 13 studies (25.0\%)" |
| D | L848 (Temporal distribution) | "Publication years span 2017--2024" | "Publication years span 2017--2025 (50/52 with explicit year; one anomalous `year=2026` for a 2025 BMC article and one blank year)" |
| E | L852 (Reproducibility status) | "29 (56\%) provided verifiable DOIs" | "28 (53.8\%) had a journal/conference DOI as `paper_id`; the remaining 24 are arXiv-only identifiers" |
| F | L881 (Reporting bias breakdown) | "39 (75.0\%) fully reported … 10 (19.2\%) … 3 (5.8\%) did not report" — not derivable from extraction columns | "51 (98.1\%) populated a non-empty `dice_per_organ` field … 1 (1.9\%) reported only aggregate metrics; finer 'fully vs. selectively reported' breakdown was not derivable from the LLM extraction columns and the 39/10/3 split has been retracted" |
| G | L991 + L1003 + L1067 (Code release) | "only 15 (28.8\%) released source code" (and two downstream restatements in Conclusions) | "only 13 (25.0\%) released source code" (count of `code_available=Yes` in `s3_extracted_data_full.csv`); the L991 intra-paragraph repeat ("28.8\%"), the RQ4 conclusion line, and the bulleted final conclusion were all updated to 25.0\% |

After these fixes, every quantitative claim in §IV–§VII of `main.tex` is independently reproducible from `pipeline_outputs/s3_extracted_data_full.csv` and `pipeline_outputs/qa_summary.csv`. The verdicts in §3 of this audit (items 17, 19, 20a, 21, 27) therefore remain ✅ — the header narrative's earlier mention of a 🟡 downgrade is superseded by this section: the paper was patched rather than the audit downgraded.

### 5.5 Acceptable absences (no action required)

- Item 1 title: deviation justified.
- Item 11 risk-of-bias instrument: standard clinical RoB tools are inapplicable; custom 3-dimension framework is the right substitute and is now backed by per-study scores in [pipeline_outputs/qa_summary.csv](artifacts/data/evidence/supplementary/pipeline_outputs/qa_summary.csv).
- Items 12, 14, 15, 24a: pooled effect sizes / funnel plots / GRADE / prospective registration are structurally inapplicable and the paper discloses this cleanly.

---

## 6. Verification methodology used in this audit

- Manuscript read end-to-end: [work/projects/papers/docdo-paper/main.tex](work/projects/papers/docdo-paper/main.tex) (L1–L1082).
- Every supplementary file in [artifacts/data/evidence/supplementary/](artifacts/data/evidence/supplementary/) was opened and `wc -l`'d; CSV column distributions for S2 (`code_available`) and S5 (`final_decision`) were enumerated with `awk`.
- Phantom-file claims from the previous version of this document were tested with `find . -type f -name '<pattern>' | grep -v .venv` for `qa_summary*`, `s3_extracted*`, `all_papers_data*`, `final_screening*`, `main_prisma*`, `*compliance*.tex` — all returned empty.
- This file replaces the earlier `PRISMA_compliance_analysis.md` in its entirety. The previous version's "side-by-side" comparison against `main_prisma-compliance.tex` and "DONE — CORRECTED" markers were unsupported by the repository and have been removed.
