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

- Pool: `pipeline_outputs/S2v2_elasticsearch_filtered.csv` — **901 records**
  (464 standard lane + 437 framework_candidate bypass lane), post fix-loop.
  (The task handoff quoted 865 = 466+399; the seed-recall fix loop re-fetch
  and the tool-name anatomy guard changed the composition — see
  `S2v2_seed_recall.md` §fix-loop and `S1v2_funnel.md`.)
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

## 4. Required prompt amendment (NOT yet applied — screening never ran)

`operations/src/docdo/screening.py` `SCREENING_PROMPT` still carries the v1
IC1-IC5 text WITHOUT the v2 Framework/Software study-type instructions and
without `framework_candidate` routing. Before the screening run, the prompt
set must be extended per Task-2 v2 criteria so that:

- standard-lane records are prompted with IC1-IC6 + EC triggers (v1 text, unchanged semantics);
- bypass-lane records are prompted with the Framework/Software criteria
  (describes a software framework/tool for 3D medical segmentation;
  documents components/architecture; reports benchmark reproduction or
  versioned release; qualitative-synthesis-only).

The v1 machinery (3 runs, unanimous-INCLUDE, temperature 0.3, JSON schema) is
unchanged and tested (`screening.py::screen_paper`, `determine_final_decision`,
`build_screening_batch_requests`, `unanimous_vote`).

## 5. Resume procedure (once `OPENAI_API_KEY` is present in `.env`)

1. Amend `SCREENING_PROMPT`/batch builder with the v2 two-lane criteria (§4).
2. Batch path (901 x 3 = 2,703 requests, mini tier):
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
