# S3v2: Search Protocol Amendment — Corrected Query Set (v2)

> **PROTOCOL AMENDMENT (2026-09-08).** This document appends a corrected,
> expanded query set (v2) to [S3_search_protocol.md](S3_search_protocol.md),
> following the appended-amendment precedent of the 2026-04-22 audit
> correction (S3 §3 header note). No wording in S3_search_protocol.md is
> altered or superseded silently; the v1 protocol text remains the record of
> what was originally drafted and executed. The machine-readable source of
> truth for the v2 queries is
> [operations/src/_archive/scripts/queries_v2.yaml](../../../../operations/src/_archive/scripts/queries_v2.yaml),
> validated by `validate_queries_v2.py` in the same directory. The v2 search
> will be executed against PubMed, arXiv, Semantic Scholar (API), and Google
> Scholar (supplementary, no-API route) over the date range **2015-01-01 to
> the execution date**, recorded in the S1v2 evidence report.

## A.1 Reason for Amendment (Diagnosis)

Verification of the v1 fetcher source
([operations/src/_archive/scripts/fetch_all_real_data.py:27-41,254-272](../../../../operations/src/_archive/scripts/fetch_all_real_data.py))
confirms that v1 executed only three generic CNN-era query shapes:

- **PubMed** — a single concept-block query (CT AND segmentation AND organs
  AND deep-learning architecture terms; lines 27–34);
- **arXiv** — a single free-text keyword string
  (`"ct computed tomography segmentation organ deep learning"`; line 37),
  with no fielded `ti:`/`abs:` syntax;
- **Semantic Scholar** — five CNN-era relevance queries over generic
  term combinations (lines 266–272).

As a result, entire method families were structurally unfindable by the v1
search: neuro-symbolic / knowledge-guided methods, the MONAI-ecosystem and
related segmentation **frameworks/tooling** (deployment-, PACS/DICOM-, and
workflow-flavored papers that never mention an architecture term in the
v1 sense), and current state-of-the-art lineages (SAM/SAM 2 foundation-model
derivatives, Mamba/state-space models, diffusion-based segmentation,
benchmark/challenge ecosystems). Additionally, the v1 filters and eligibility
rules excluded framework papers by construction — no amount of luck could
surface them. The v2 set below fixes the query layer; the eligibility fix
(study type **Framework/Software**) is recorded in §A.4 and appended to
[S4_screening_criteria.md](S4_screening_criteria.md) and
[coding-scheme.md](../../annotations/coding-scheme.md).

## A.2 v2 Query Families

Six families are **executed** per database (one query per family per
database). Family F is a shared anatomy fragment ANDed into the template
families and is **never executed standalone** — it carries no deep-learning
method anchor, and a standalone F query would flood the raw set with every
anatomy+segmentation record.

| Family | Scope | Role in template |
|--------|-------|------------------|
| **A** | Neuro-symbolic / priors (knowledge-guided, topological, ontology, clDice, …) | executed, template family |
| **B** | Frameworks / tooling (exact tool names OR framework vocabulary) | executed, **not** ANDed with segmentation |
| **C** | Foundation models / SAM lineage (Segment Anything, MedSAM, SegVol, SAT, …) | executed, template family |
| **D** | SOTA architecture families (Mamba, diffusion, AutoML/NAS, SSL, federated, …) | executed, template family |
| **E** | Benchmark / challenge names (TotalSegmentator, AMOS, KiTS, MSD, …) | executed, template family |
| **G** | v1 core DL architectures (deep learning, CNN, U-Net, transformer, …) — reproduces v1's executed PubMed concept block (S3 §3.1) so plain "3D U-Net liver segmentation from CT" abstracts retain an entry point | executed, template family |
| **F** | CT anatomy scope (abdominal, thoracic, multi-organ, liver, kidney, …, computed tomography, CT) | **shared fragment only** (YAML anchor referenced inside A/C/D/E/G) |

The verbatim per-family term lists live in `queries_v2.yaml`
(`executed_families.<X>.terms` and `shared_fragments.family_F_anatomy.terms`)
and are enforced by the validator against the plan's pinned lists.

## A.3 Pinned Conjunction Template (binding)

Fielded `ti`/`abs` syntax per database, AND/OR blocks as in S3 §3.1
(PubMed `[tiab]`; arXiv `ti:`/`abs:`; Semantic Scholar keeps the same boolean
block structure with quoted phrases — its Graph API relevance-search endpoint
has no fielded search; Google Scholar blocks carry the same family terms as
plain quoted phrases, since GS ignores fielded syntax):

- **Families A/C/D/E/G** =
  `(family terms)` AND `(segmentation OR "medical imaging")` AND
  `(family-F anatomy block)`.
- **Family B** =
  `(exact tool names: MONAI, Auto3DSeg, MONAI Label, MONAI Deploy, VISTA-3D,
  NV-Segment-CT, nnInteractive, NVIDIA Clara, Holoscan)` OR
  `((framework vocabulary: open-source framework, medical imaging toolkit,
  software framework, deployment, microservice, inference pipeline, clinical
  workflow, PACS, DICOM, reproducib*, Grand Challenge)` AND
  `("medical imaging" OR radiolog* OR tomograph*))`.
  Family B is explicitly **not** ANDed with `segmentation`, so
  deployment-flavored tooling papers enter the raw set.
- **Family C exact tokens** — the bare tokens "SAM", "SAM2", "SAT" appear
  only as exact-token/phrase forms (`"SAM"[tiab]` as exact token,
  `"Segment Anything"`, `"SAM 2"`, `"Segment Anything with Text"` style),
  never bare substrings.
- Wildcard rendering: PubMed (Entrez) keeps `radiolog*`/`tomograph*`/
  `reproducib*`; arXiv, Semantic Scholar and Google Scholar lack wildcard
  support and expand the stems to explicit word forms (radiology,
  radiological, radiologists; tomography, tomographic; reproducibility,
  reproducible).

## A.4 Amended Eligibility — New Study Type "Framework/Software"

Appended to the eligibility criteria (original IC/EC text for method papers
untouched):

> **Framework/Software (qualitative stratum).** Describes a software
> framework/tool for 3D medical segmentation; documents
> components/architecture; reports benchmark reproduction or versioned
> release; enters qualitative synthesis ONLY (never the quantitative Dice
> table).

Dated v2 sections carrying this criteria set verbatim are appended to
[S4_screening_criteria.md](S4_screening_criteria.md) (screening operational
view) and [coding-scheme.md](../../annotations/coding-scheme.md)
(annotation view).

## A.5 Google Scholar — Supplementary Identification Source

Google Scholar is added as a **supplementary** identification source
(scraped via the `scholarly` wrapper; no official API exists), with the
following recorded limitations:

1. **no API** (access via scraper, subject to CAPTCHA/bot blocking; blocked
   queries are recorded and the run continues — graceful degradation);
2. **non-reproducible result sets** (rankings and coverage drift between
   runs; GS results are informational, never evidence against another
   database's zero-hit status);
3. **100-results/query cap** (first 10 pages per query, pinned);
4. **title-based dedup** (GS records frequently lack DOIs, so dedup matches
   on normalized title only);
5. **no query-level date filtering** (pre-2015 records possible; year
   eligibility enforced downstream at screening).

## A.6 Explicit Diff vs. S3 (v1)

| Aspect | S3 (v1, as executed) | v2 (this amendment) |
|---|---|---|
| Executed databases | PubMed, arXiv, Semantic Scholar (3; per 2026-04-22 audit note) | PubMed, arXiv, Semantic Scholar + Google Scholar (supplementary, no-API) |
| Queries per database | 1 generic concept-block (PubMed), 1 free-text (arXiv), 5 generic relevance strings (S2) | 6 executed families (A, B, C, D, E, G) per database, fielded `ti`/`abs` syntax where the database supports it |
| Anatomy/CT scope | folded into the single query string | family F shared fragment, ANDed into A/C/D/E/G, never standalone |
| Framework/tooling coverage | none (excluded by construction) | family B (exact tool names OR framework vocabulary, not ANDed with segmentation) + Framework/Software study type |
| SOTA/foundation coverage | partial (two small supplements PUB-002/ARXIV-002) | families C (SAM lineage) and D (Mamba/diffusion/NAS/SSL/…) |
| Benchmark/challenge coverage | none | family E |
| v1 core DL coverage | the only coverage | family G reproduces the v1 PubMed concept block (S3 §3.1) inside the v2 template |
| Date range | 2015-01-01 to 2025-09-15/17 (per-query, as executed) | 2015-01-01 to execution date; GS exempt (limitation 5) |
| Validation | none | `validate_queries_v2.py` acceptance matrix + adversarial probe suite (see task-2 evidence) |

## A.7 Amendment Provenance

- Amendment drafted: 2026-09-08 (Task 2, `.omo/plans/paper-coverage-gap-update.md`).
- Query source of truth: `operations/src/_archive/scripts/queries_v2.yaml` (v2, generated 2026-09-08).
- Validator: `operations/src/_archive/scripts/validate_queries_v2.py` (exit 0 on the final yaml; six adversarial probes demonstrated non-zero exits — matrix recorded in `.omo/evidence/task-2-paper-coverage-gap-update.md`).
- Execution of the v2 searches: Task 4 (no searches were run for this amendment).
