# S2v2 Screening Log — Task 6 (paper-coverage-gap-update)

**Status: NOT RUN — BLOCKED on missing `OPENAI_API_KEY`.**
**Date of block:** 2026-09-08. No screening votes were cast; no tallies exist.
Nothing in this file is fabricated — every field below is either a verified
configuration fact or an explicit placeholder.

## 1. Blocker

`OPENAI_API_KEY` is absent from the repo-root `.env` (which carries only the
four `DOCDO_*_MODEL` pins), from the shell environment, and from all user
dotfiles/keychains checked (names only; no secrets printed). `docdo.config.openai_api_key()`
raises `EnvironmentError` — verified at execution:

```
DEFAULT_MODEL = gpt-4o-mini
BATCH_MODEL   = gpt-4o-mini
FULLTEXT_MODEL= gpt-4o-mini
TIEBREAKER    = gpt-4o-mini
NUM_RUNS      = 3 | TEMPERATURE = 0.3
OPENAI_API_KEY: MISSING -> OPENAI_API_KEY not set. Export it or add to .env at repo root.
```

Per the task contract ("if missing, STOP and report — do not fabricate"),
the 3-vote screening run was not executed and no model-drift check, vote
tally, or 10-random-INCLUDE re-check can be reported. Resume instructions in §5.

## 2. Screening input (ready)

- Pool: `pipeline_outputs/S2v2_elasticsearch_filtered.csv` — **1,101 records**
  (641 standard lane + 460 framework_candidate bypass lane), post fix-loop r1
  + remediation r2 (seed PMID recovery + relevance-window probe).
  (The task handoff quoted 865 = 466+399; the seed-recall fix loop and
  remediation changed the composition — see `S2v2_seed_recall.md` §fix-loop
  and `S1v2_funnel.md`.)
- Criteria files in force (v2): `S4_ai_screening_protocol.md`,
  `S4_screening_criteria.md` (v2 section), `coding-scheme.md` (v2),
  `labeling-rules.md`.
- Routing rule: `framework_candidate=true` rows are screened against the
  **Framework/Software** study type (qualitative stratum), NOT IC3;
  `framework_candidate=false` rows against IC1-IC6.

## 3. Model configuration (verified, pre-run)

| Slot | Value | Source |
|------|-------|--------|
| DOCDO_MODEL | gpt-4o-mini | `.env` (repo root, gitignored) + `config.py` default |
| DOCDO_BATCH_MODEL | gpt-4o-mini | same |
| DOCDO_FULLTEXT_MODEL | gpt-4o-mini | same |
| DOCDO_TIEBREAKER_MODEL | gpt-4o-mini | same |

All four tiers are mini-class; the tiebreaker participates only as a 4th
audit opinion (unanimous rule is authoritative — `labeling-rules.md`).

## 4. Prompt amendment (APPLIED — remediation r2, 2026-09-08)

`operations/src/docdo/screening.py` now implements the v2 two-lane criteria:

- `SCREENING_PROMPT` carries a `{study_type_instructions}` slot plus a
  lane-aware DECISION RULE (apply F1-F3/FEC1-FEC3 when the study-type block
  is present, IC1-IC5 otherwise).
- `FRAMEWORK_STUDY_TYPE_CRITERIA` (F1 software framework/tool for 3D medical
  segmentation; F2 documented components/architecture; F3 benchmark
  reproduction or versioned release; FEC1-FEC3 exclude triggers;
  qualitative-synthesis-only) is injected for `framework_candidate=true`
  rows — coerced from bool OR CSV "true"/"false" (`_is_framework_candidate`).
- Routing wired through `screen_paper_once` / `screen_paper` /
  `build_screening_batch_requests` / `docdo screen` CLI (per-row flag).
- Tests: `operations/tests/test_screening.py::TestTwoLaneCriteria` (3,
  red-first). v1 archive scripts that format `SCREENING_PROMPT` pass
  `study_type_instructions=""` (v1-equivalent behavior).
- The v1 machinery is unchanged: 3 runs, unanimous-INCLUDE, temperature 0.3,
  JSON schema (`screening.py::screen_paper`, `determine_final_decision`,
  `build_screening_batch_requests`, `unanimous_vote`).

## 5. Resume procedure (once `OPENAI_API_KEY` is present in `.env`)

1. ~~Amend `SCREENING_PROMPT`/batch builder with the v2 two-lane criteria~~ — DONE (r2, §4).
2. Batch path (1,101 x 3 = 3,303 requests, mini tier):
   `docdo screen-batch -i artifacts/data/evidence/supplementary/pipeline_outputs/S2v2_elasticsearch_filtered.csv --output-dir artifacts/data/evidence/processed/batches_v2/`
   then `docdo check-batch <id>` / `docdo download-batch <id>`, votes compiled
   with `screening.unanimous_vote` (unanimous-INCLUDE rule — DO NOT change).
3. Outputs to co-locate in `pipeline_outputs/`: `all_papers_after_s2v2_with_status.csv`
   (schema mirror of v1 `all_papers_after_s2_with_status.csv`) and replace this
   stub with the real log: model ids per stage, per-paper vote tallies,
   unanimous-rule stats, wall time.
4. Model-drift check: grep the log — every model id must be gpt-4o-mini class.
5. Post-run QA: 10 random INCLUDEs re-checked against v2 criteria (agreement >= 9/10).

## 6. Wall time

Not applicable (no run). Elapsed Task-6 pipeline work before the block:
seed-recall audit + fix loop + funnel rebuild (documented in
`S2v2_seed_recall.md` and `.omo/evidence/task-6-paper-coverage-gap-update.md`).
