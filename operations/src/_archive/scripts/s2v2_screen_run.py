#!/usr/bin/env python3
"""S2v2 screening run driver (Task 6, paper-coverage-gap-update).

Runs the docdo package screening machinery (screen_paper_once x3 +
determine_final_decision, unanimous-INCLUDE rule) over the 1,101-record
S2v2 pool via the user's LiteTTM proxy (deepseek-ai/DeepSeek-V4-Flash-0731).

Modes:
  run      -- threaded vote collection, JSONL checkpoint per record (resumable)
  compile  -- checkpoint -> all_papers_after_s2v2_with_status.csv + tallies

Failure policy: a vote whose rationale is a machine error marker is retried
(driver-level, on top of chat()'s internal backoff). A record that still has
error votes is written to the checkpoint with status=incomplete and gets NO
final decision -- failures are visible, never silently EXCLUDEd.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "operations" / "src"))

from docdo import config  # noqa: E402
from docdo.screening import determine_final_decision, screen_paper_once  # noqa: E402

POOL_CSV = REPO / "artifacts/data/evidence/supplementary/pipeline_outputs/S2v2_elasticsearch_filtered.csv"
OUT_DIR = REPO / "artifacts/data/evidence/processed/batches_v2"
CHECKPOINT = OUT_DIR / "s2v2_votes_checkpoint.jsonl"
STATUS_CSV = REPO / "artifacts/data/evidence/supplementary/pipeline_outputs/all_papers_after_s2v2_with_status.csv"

WORKERS = 2
VOTE_RETRIES = 4
RETRY_SLEEP = 15.0

ERROR_RATIONALES = {
    "empty_response",
    "json_parse_error",
    "run_failed",
}
ERROR_PREFIXES = ("api_error:", "json_extract_error:")


def is_error_vote(vote: dict) -> bool:
    r = str(vote.get("rationale", ""))
    return r in ERROR_RATIONALES or r.startswith(ERROR_PREFIXES)


def cast_vote(row: dict, run: int) -> dict:
    for attempt in range(1, VOTE_RETRIES + 1):
        v = screen_paper_once(
            row["title"],
            row["abstract_snippet"],
            framework_candidate=row.get("framework_candidate", "false"),
        )
        if not is_error_vote(v):
            return v
        if attempt < VOTE_RETRIES:
            time.sleep(RETRY_SLEEP)
    return v


def load_checkpoint_votes() -> dict[tuple[str, int], dict]:
    done: dict[tuple[str, int], dict] = {}
    if CHECKPOINT.exists():
        for line in CHECKPOINT.read_text().splitlines():
            if line.strip():
                rec = json.loads(line)
                done[(rec["id"], rec["run"])] = rec["vote"]
    return done


def mode_run() -> None:
    config.openai_api_key()
    with open(POOL_CSV, encoding="utf-8") as f:
        pool = list(csv.DictReader(f))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    done = load_checkpoint_votes()
    todo = [
        (row, run)
        for row in pool
        for run in range(1, config.NUM_RUNS + 1)
        if (row["id"], run) not in done
    ]
    print(f"[run] pool={len(pool)} votes_done={len(done)} votes_todo={len(todo)} "
          f"model={config.DEFAULT_MODEL} workers={WORKERS} "
          f"num_runs={config.NUM_RUNS} max_tokens=VOTE_MAX_TOKENS", flush=True)

    t0 = time.time()
    n_err = 0
    ckpt = open(CHECKPOINT, "a", encoding="utf-8")

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(cast_vote, row, run): (row, run) for row, run in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            row, run = futs[fut]
            vote = fut.result()
            ckpt.write(json.dumps(
                {"id": row["id"], "run": run, "vote": vote}, ensure_ascii=False) + "\n")
            if i % 10 == 0 or i == len(todo):
                ckpt.flush()
                el = time.time() - t0
                eta = el / i * (len(todo) - i)
                print(f"  [{i}/{len(todo)}] elapsed={el/60:.1f}m eta={eta/60:.1f}m", flush=True)
            if is_error_vote(vote):
                n_err += 1
                print(f"  ERROR-VOTE {row['id']} run{run}: {vote['rationale']}", flush=True)
    ckpt.close()
    print(f"[run] finished: {len(todo)} votes ({n_err} error votes -- re-run to retry) "
          f"in {(time.time()-t0)/60:.1f}m", flush=True)


def mode_compile() -> None:
    with open(POOL_CSV, encoding="utf-8") as f:
        pool = list(csv.DictReader(f))
    by_id = {r["id"]: r for r in pool}
    votes_by_id: dict[str, dict[int, dict]] = {}
    for line in CHECKPOINT.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        votes_by_id.setdefault(rec["id"], {})[rec["run"]] = rec["vote"]

    complete: dict[str, dict] = {}
    error_records: list[str] = []
    missing: list[str] = []
    for rid in by_id:
        runs = votes_by_id.get(rid, {})
        if len(runs) < config.NUM_RUNS:
            missing.append(rid)
            continue
        votes = [runs[i] for i in range(1, config.NUM_RUNS + 1)]
        if any(is_error_vote(v) or v["decision"] not in ("INCLUDE", "EXCLUDE")
               for v in votes):
            error_records.append(rid)
            continue
        complete[rid] = {"votes": votes, "final": determine_final_decision(votes),
                         "model": config.DEFAULT_MODEL,
                         "framework_candidate": by_id[rid].get("framework_candidate", "false")}
    if error_records or missing:
        print(f"[compile] REFUSING: error_votes={len(error_records)} {error_records[:10]} "
              f"missing_votes={len(missing)} -- re-run 'run' mode", flush=True)
        raise SystemExit(1)

    fieldnames = [
        "paper_id", "title", "path", "pdf_status", "included_in_review",
        "abstract_snippet", "exclusion_reason", "exclusion_stage",
        "framework_candidate", "final_decision", "avg_confidence",
        "run_1_decision", "run_1_confidence",
        "run_2_decision", "run_2_confidence",
        "run_3_decision", "run_3_confidence",
        "criteria_met", "criteria_failed", "vote_pattern", "vote_model",
    ]
    n = 0
    with open(STATUS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for rid, row in by_id.items():
            rec = complete[rid]
            fin = rec["final"]
            votes = rec["votes"]
            pattern = "".join("I" if v["decision"] == "INCLUDE" else "E" for v in votes)
            final = fin["final_decision"]
            w.writerow({
                "paper_id": row.get("doi") or rid,
                "title": row["title"],
                "path": "",
                "pdf_status": "",
                "included_in_review": "True" if final == "INCLUDE" else "False",
                "abstract_snippet": row.get("abstract_snippet", ""),
                "exclusion_reason": fin["criteria_failed"] if final == "EXCLUDE" else "",
                "exclusion_stage": "S2v2" if final == "EXCLUDE" else "",
                "framework_candidate": row.get("framework_candidate", "false"),
                "final_decision": final,
                "avg_confidence": f"{fin['avg_confidence']:.1f}",
                "run_1_decision": votes[0]["decision"],
                "run_1_confidence": votes[0]["confidence"],
                "run_2_decision": votes[1]["decision"],
                "run_2_confidence": votes[1]["confidence"],
                "run_3_decision": votes[2]["decision"],
                "run_3_confidence": votes[2]["confidence"],
                "criteria_met": fin["criteria_met"],
                "criteria_failed": fin["criteria_failed"],
                "vote_pattern": pattern,
                "vote_model": rec["model"],
            })
            n += 1

    models = sorted({r["model"] for r in complete.values()})
    tallies: dict[str, int] = {}
    for rid, rec in complete.items():
        lane = "bypass" if rec["framework_candidate"] == "true" else "standard"
        final = rec["final"]["final_decision"]
        tallies[f"{lane}_{final}"] = tallies.get(f"{lane}_{final}", 0) + 1
    patterns: dict[str, int] = {}
    for rec in complete.values():
        p = "".join("I" if v["decision"] == "INCLUDE" else "E" for v in rec["votes"])
        patterns[p] = patterns.get(p, 0) + 1
    print(f"[compile] {n} rows -> {STATUS_CSV.name}")
    print(f"[compile] models={models}")
    print(f"[compile] tallies={json.dumps(tallies, sort_keys=True)}")
    print(f"[compile] vote_patterns={json.dumps(dict(sorted(patterns.items())), sort_keys=True)}")
    print(f"[compile] generated={datetime.now().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "run":
        mode_run()
    elif mode == "compile":
        mode_compile()
    else:
        raise SystemExit(f"unknown mode: {mode}")
