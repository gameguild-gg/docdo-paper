# S2v2 Screening Log — Task 6 (paper-coverage-gap-update)

**Status: EXECUTED 2026-09-09.** 3-vote unanimous-INCLUDE screening over all
1,101 pool records completed on the user-directed LiteLLM proxy
(`deepseek-ai/DeepSeek-V4-Flash-0731`). Zero vote failures, zero silent skips.

> **Provider switch annotation (2026-09-09, user-directed):** screening votes
> moved from OpenAI direct (gpt-4o-mini, v1 era; v2 plan) to the user's
> LiteLLM proxy at `https://llm.gameguild.gg/v1` serving
> `deepseek-ai/DeepSeek-V4-Flash-0731` — mini-class equivalent, cheaper tier.
> ZAI GLM was evaluated for this stage and rejected as too heavy for the
> ~3.3k reasoning-model calls required. The proxy WAF 403-blocks the OpenAI
> SDK's default `User-Agent: OpenAI/Python ...`; fixed by
> `default_headers={"User-Agent": "docdo/1.0", "Accept-Encoding": "identity"}`
> on every client construction in `operations/src/docdo/openai_utils.py`
> (the Accept-Encoding override additionally works around a local
> brotli-1.1.0/httpx2-2.12 decoder incompatibility).

## 1. Run configuration (verified at execution)

| Parameter | Value |
|-----------|-------|
| Vote model (all 3 votes + compile assert) | `deepseek-ai/DeepSeek-V4-Flash-0731` |
| Base URL | user LiteLLM proxy (`.env` OPENAI_BASE_URL, gitignored) |
| Votes per record | 3 (temperature 0.3, independent runs) |
| max_tokens per vote | 2048 (`VOTE_MAX_TOKENS`, screening.py) — the model emits `reasoning_content` BEFORE `content` and reasoning tokens count against max_tokens; the v1-era 300 cap truncated completions to `'{"'` (verified in pilot: finish_reason=length at 300, clean stop at 512+) |
| Decision rule | unanimous-INCLUDE (`determine_final_decision` / compile equivalent — unchanged from v1) |
| Lane routing | `framework_candidate=true` → F1-F3/FEC1-FEC3 (Framework/Software, v2 prompt in screening.py); `false` → IC1-IC5 + EC1-EC6 |
| Vote parser | reads `message.content` only; `reasoning_content` is a separate response field (vLLM backend) and never contaminates the JSON vote |
| Concurrency | 2 workers (proxy degrades/tarpits above ~12 concurrent; verified empirically) |

## 2. Run execution

- Driver: `operations/src/_archive/scripts/s2v2_screen_run.py` (package
  machinery: `screening.screen_paper_once` per vote + `determine_final_decision`;
  vote-granular JSONL checkpoint at
  `evidence/processed/batches_v2/s2v2_votes_checkpoint.jsonl`, resume-safe).
- Votes cast: **3,303** (1,101 × 3). Error votes: **0** (chat()-level retry
  with rate-limit backoff absorbed every transient; driver-level retry never
  engaged).
- Wall time: **≈ 501 min (8.35 h)** at the 2-worker cap, including one
  mid-run network blip absorbed by backoff. Includes a 165 s / 24-vote
  first chunk at 12 workers before the concurrency cap was applied.
- Model-drift check: driver header (run4.log) pins
  `model=deepseek-ai/DeepSeek-V4-Flash-0731`; compile-time assert over all
  checkpoint records reports `models=['deepseek-ai/DeepSeek-V4-Flash-0731']`.
  No vote used any other model.

## 3. Results (from `pipeline_outputs/all_papers_after_s2v2_with_status.csv`)

| Lane | INCLUDE | EXCLUDE | Total |
|------|---------|---------|-------|
| standard (framework_candidate=false) | 274 | 367 | 641 |
| bypass (framework_candidate=true) | 14 | 446 | 460 |
| **Total** | **288** | **813** | **1,101** |

Per-vote pattern distribution (I=INCLUDE, E=EXCLUDE):

| Pattern | Count | Outcome |
|---------|-------|---------|
| III | 288 | INCLUDE (unanimous) |
| EEE | 735 | EXCLUDE (unanimous) |
| EEI | 17 | EXCLUDE (no consensus) |
| EIE | 11 | EXCLUDE (no consensus) |
| EII | 11 | EXCLUDE (no consensus) |
| IEE | 14 | EXCLUDE (no consensus) |
| IEI | 14 | EXCLUDE (no consensus) |
| IIE | 11 | EXCLUDE (no consensus) |

Mixed patterns (any): 78 → all EXCLUDE per the unanimous rule.

## 4. Output schema

`all_papers_after_s2v2_with_status.csv` mirrors v1
`all_papers_after_s2_with_status.csv` (paper_id, title, path, pdf_status,
included_in_review, abstract_snippet, exclusion_reason, exclusion_stage) and
appends per-vote provenance columns (framework_candidate, final_decision,
avg_confidence, run_1..3 decision/confidence, criteria_met, criteria_failed,
vote_pattern, vote_model). `path`/`pdf_status` are empty — Task 7 (acquisition)
owns them.

## 5. Resume procedure (superseded — executed)

1. ~~v2 two-lane prompt amendment~~ — done r2 (§4 of the previous stub).
2. ~~Batch path~~ — NOT used: the LiteLLM proxy does not expose the OpenAI
   Batch API; the synchronous chat path via `s2v2_screen_run.py` was used
   instead (same package functions, same unanimous rule).
3. ~~Outputs~~ — `all_papers_after_s2v2_with_status.csv` written (this file
   replaces the blocked stub).
4. ~~Model-drift check~~ — §2 above.
5. ~~Post-run QA~~ — §6 below.

## 6. Post-run QA (executed 2026-09-09)

- 10 random INCLUDE re-check against v2 criteria (agent, criterion-coded,
  fixed seed 20260909): **10/10 agreement** (3 weak-but-criteria-consistent:
  a Framework-stratum tooling paper under F1-F3; a µCT application study
  whose DL lung-lobe segmentation satisfies IC1-IC4; an nnU-Net OAR
  auto-segmentation clinical study — IC4 explicitly admits organs-at-risk).
- Seed-recall oracle: 12/12 terminal states complete — see
  `S2v2_seed_recall.md` §"S2v2 run terminal states". Pool seeds: 3 INCLUDE
  (MONAI Label, nnInteractive, U-Mamba), 3 excluded-with-reason (MONAI
  FEC3; MONAI Deploy FEC1/FEC2/FEC3; VISTA3D split vote IEI + FEC1).
- `python3 -m pytest operations/tests/ -q`: **199 passed** (196 baseline +
  3 new: UA-header construction test, vote-budget tests for the sync and
  batch paths).

## 7. Wall time

Total ≈ 8.35 h vote collection (3,303 votes, 2-worker cap, proxy-latency
bound) + compile/QA. Prior Task-6 pipeline work (seed oracle, fix loops,
funnel rebuild) documented in `S2v2_seed_recall.md` and
`.omo/evidence/task-6-paper-coverage-gap-update.md`.
