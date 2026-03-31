#!/usr/bin/env python3
"""Compare strict vs strict-v2 screening outcomes.

Strict (main):
- Model: gpt-4o-mini
- 3 runs per paper
- Final decision: INCLUDE only if all 3 runs are INCLUDE; otherwise EXCLUDE.

Strict-v2 (validation):
- Model: gpt-4o
- 1 run per paper
- Adds IC6 (public benchmark / metrics evidence)

This script:
1) Loads batch IDs from progress JSONs (or CLI overrides)
2) Downloads batch output JSONL via OpenAI Batch API (with local caching)
3) Parses model JSON responses
4) Aggregates strict 3-run decisions to a final decision
5) Compares strict final vs strict-v2 decision
6) Writes comparison CSVs + a small summary JSON

Usage:
  python supplementary/scripts/compare_strict_vs_strictv2.py
  python supplementary/scripts/compare_strict_vs_strictv2.py --wait --poll-seconds 60
  python supplementary/scripts/compare_strict_vs_strictv2.py --strict-batch-ids <id1> <id2> --strictv2-batch-id <id3>
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform as _platform
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, cast

try:
    from dotenv import load_dotenv  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    def load_dotenv(*_args: object, **_kwargs: object) -> bool:  # type: ignore
        return False

from openai import OpenAI

# Workaround: On some Windows/Python builds, platform.platform() can hang due to
# WMI queries (seen on Python 3.14). The OpenAI SDK calls platform.platform()
# when constructing default headers. Override it with a fast implementation.
try:  # pragma: no cover
    _platform.platform = lambda *args, **kwargs: _platform.system()  # type: ignore
except Exception:
    pass

REPO_ROOT = Path(__file__).parent.parent.parent
# Optional: if python-dotenv is not installed, user can still run by setting
# OPENAI_API_KEY in the environment.
load_dotenv(REPO_ROOT / ".env")

S2_FILE = REPO_ROOT / "data" / "processed" / "S2_elasticsearch_filtered.csv"
STRICT_PROGRESS = REPO_ROOT / "data" / "processed" / "batches_esfiltered" / "esfilter_submission_progress.json"
STRICTV2_DIR = REPO_ROOT / "data" / "processed" / "batches_esfiltered_strictv2_gpt4o"
STRICTV2_MANIFEST = STRICTV2_DIR / "strictv2_manifest.json"

DOWNLOAD_DIR = REPO_ROOT / "data" / "processed" / "batch_downloads"
OUT_DIR = REPO_ROOT / "data" / "processed" / "comparisons"

STRICT_EXPECTED_RUNS = 3


@dataclass(frozen=True)
class PaperMeta:
    pid: str
    id: str
    doi: str
    title: str
    year: str
    database: str
    journal_conference: str


@dataclass
class RunDecision:
    decision: str  # INCLUDE/EXCLUDE
    confidence: float
    rationale: str
    parse_error: str = ""


def _paper_id_from_row(row: Dict[str, str]) -> str:
    return (row.get("doi") or row.get("id") or row.get("title", "")[:50] or "unknown").strip()


def _load_paper_meta() -> Dict[str, PaperMeta]:
    if not S2_FILE.exists():
        raise SystemExit(f"Missing input file: {S2_FILE}")

    out: Dict[str, PaperMeta] = {}
    with open(S2_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = _paper_id_from_row(row)
            out[pid] = PaperMeta(
                pid=pid,
                id=row.get("id", ""),
                doi=row.get("doi", ""),
                title=row.get("title", ""),
                year=row.get("year", ""),
                database=row.get("database", ""),
                journal_conference=row.get("journal_conference", ""),
            )
    return out


def _load_strict_batch_ids(progress_path: Path) -> List[str]:
    if not progress_path.exists():
        raise SystemExit(f"Missing strict progress file: {progress_path}")

    data = json.loads(progress_path.read_text(encoding="utf-8"))
    batch_ids_any: Any = data.get("batch_ids")
    if not isinstance(batch_ids_any, list) or not batch_ids_any:
        raise SystemExit(f"No strict batch_ids found in: {progress_path}")

    batch_ids_list = cast(List[Any], batch_ids_any)
    out: List[str] = []
    for item in batch_ids_list:
        s = str(item).strip()
        if s:
            out.append(s)
    return out


def _load_latest_strictv2_batch_id(strictv2_dir: Path) -> str:
    if not strictv2_dir.exists():
        raise SystemExit(f"Missing strict-v2 directory: {strictv2_dir}")

    infos = sorted(strictv2_dir.glob("*_info.json"))
    if not infos:
        raise SystemExit(f"No strict-v2 info json found in: {strictv2_dir}")

    # Filenames include timestamp; lexicographic sort is fine.
    info_path = infos[-1]
    info = json.loads(info_path.read_text(encoding="utf-8"))
    batch_id = str(info.get("batch_id", "")).strip()
    if not batch_id:
        raise SystemExit(f"No batch_id in: {info_path}")
    return batch_id


def _load_latest_strictv2_batch_ids(strictv2_dir: Path) -> List[str]:
    """Prefer submission_progress.json (multi-part); fall back to latest *_info.json."""
    if not strictv2_dir.exists():
        raise SystemExit(f"Missing strict-v2 directory: {strictv2_dir}")

    # Preferred: cumulative manifest across multiple submission runs
    if STRICTV2_MANIFEST.exists():
        try:
            manifest = json.loads(STRICTV2_MANIFEST.read_text(encoding="utf-8"))
            parts_any: Any = manifest.get("parts")
            if isinstance(parts_any, list) and parts_any:
                parts_list = cast(List[Any], parts_any)
                ids: List[str] = []
                for p in parts_list:
                    if isinstance(p, dict):
                        pd = cast(Dict[str, Any], p)
                        bid = str(pd.get("batch_id", "")).strip()
                        if bid:
                            ids.append(bid)
                if ids:
                    # preserve order, de-dupe
                    seen: set[str] = set()
                    out: List[str] = []
                    for bid in ids:
                        if bid not in seen:
                            seen.add(bid)
                            out.append(bid)
                    return out
        except Exception:
            pass

    progresses = sorted(strictv2_dir.glob("*_submission_progress.json"))
    if progresses:
        progress_path = progresses[-1]
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        batch_ids_raw: Any = progress.get("batch_ids")
        if isinstance(batch_ids_raw, list) and batch_ids_raw:
            batch_ids_list = cast(List[Any], batch_ids_raw)
            batch_ids: List[str] = []
            for item in batch_ids_list:
                s = str(item).strip()
                if s:
                    batch_ids.append(s)
            if batch_ids:
                return batch_ids

    # Fallback: single-batch strictv2
    return [_load_latest_strictv2_batch_id(strictv2_dir)]


def _strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        # split on fences and take the first fenced block content
        parts = t.split("```")
        if len(parts) >= 2:
            t = parts[1]
        t = t.strip()
        if t.lower().startswith("json"):
            t = t[4:].strip()
    return t


_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse_model_json(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Return (parsed_json, error). Tries to be robust to minor formatting."""
    c = _strip_code_fences(content)

    try:
        return json.loads(c), ""
    except Exception:
        match = _JSON_OBJECT_RE.search(c)
        if match:
            try:
                return json.loads(match.group(0)), ""
            except Exception as e:
                return None, f"json_extract_parse_error: {e}"
        return None, "json_parse_error"


def _extract_chat_content(result_line: Dict[str, Any]) -> Tuple[Optional[str], str]:
    response_any: Any = result_line.get("response")
    response: Dict[str, Any] = cast(Dict[str, Any], response_any) if isinstance(response_any, dict) else {}
    status_code = response.get("status_code")

    if status_code == 200:
        body_any: Any = response.get("body")
        body: Dict[str, Any] = cast(Dict[str, Any], body_any) if isinstance(body_any, dict) else {}
        choices_any: Any = body.get("choices")
        choices: List[Any] = cast(List[Any], choices_any) if isinstance(choices_any, list) else []
        if choices:
            first: Any = choices[0] if choices else {}
            first_d: Dict[str, Any] = cast(Dict[str, Any], first) if isinstance(first, dict) else {}
            msg_any = first_d.get("message")
            msg: Dict[str, Any] = cast(Dict[str, Any], msg_any) if isinstance(msg_any, dict) else {}
            content_any = msg.get("content")
            return (str(content_any) if content_any is not None else ""), ""
        return None, "missing_choices"

    # Non-200
    err_any: Any = result_line.get("error")
    err: Dict[str, Any] = cast(Dict[str, Any], err_any) if isinstance(err_any, dict) else {}
    msg_any: Any = err.get("message")
    err_msg = str(msg_any) if msg_any is not None else f"status_code={status_code}"
    return None, f"api_error: {err_msg}"


def _download_batch_output(
    client: OpenAI,
    batch_id: str,
    *,
    wait: bool,
    poll_seconds: int,
    wait_max_seconds: int,
) -> Path:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DOWNLOAD_DIR / f"{batch_id}_output.jsonl"

    if out_path.exists():
        return out_path

    started = time.time()
    while True:
        batch = client.batches.retrieve(batch_id)
        status = getattr(batch, "status", "")

        if status == "completed":
            output_file_id = getattr(batch, "output_file_id", None)
            if not output_file_id:
                raise SystemExit(f"Batch {batch_id} completed but has no output_file_id")

            content = client.files.content(output_file_id)
            out_path.write_text(content.text, encoding="utf-8")
            return out_path

        if status in {"failed", "expired", "cancelled", "cancelling"}:
            raise SystemExit(f"Batch {batch_id} is in terminal state: {status}")

        if not wait:
            raise SystemExit(f"Batch {batch_id} not completed yet (status={status}). Re-run with --wait.")

        if wait_max_seconds > 0 and (time.time() - started) > wait_max_seconds:
            raise SystemExit(
                f"Timed out waiting for batch {batch_id} (status={status}). "
                f"Increase --wait-max-seconds or re-run later."
            )

        time.sleep(max(5, poll_seconds))


def _iter_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _parse_strict_outputs(paths: List[Path]) -> Dict[str, Dict[int, RunDecision]]:
    """Return pid -> run_num -> RunDecision."""
    decisions: Dict[str, Dict[int, RunDecision]] = {}

    for path in paths:
        for result in _iter_jsonl(path):
            custom_id = str(result.get("custom_id", ""))
            if "__run" not in custom_id:
                continue

            pid, run_part = custom_id.rsplit("__run", 1)
            try:
                run_num = int(run_part)
            except ValueError:
                continue

            content, err = _extract_chat_content(result)
            if not pid:
                continue

            decisions.setdefault(pid, {})

            if err:
                decisions[pid][run_num] = RunDecision(decision="EXCLUDE", confidence=0.0, rationale=err, parse_error=err)
                continue

            parsed, parse_err = _parse_model_json(content or "")
            if not parsed:
                decisions[pid][run_num] = RunDecision(
                    decision="EXCLUDE",
                    confidence=0.0,
                    rationale="parse_error",
                    parse_error=parse_err or "parse_error",
                )
                continue

            decision = str(parsed.get("decision", "EXCLUDE")).strip().upper()
            if decision not in {"INCLUDE", "EXCLUDE"}:
                decision = "EXCLUDE"

            conf = parsed.get("confidence", 0)
            try:
                conf_f = float(conf)
            except Exception:
                conf_f = 0.0

            decisions[pid][run_num] = RunDecision(
                decision=decision,
                confidence=conf_f,
                rationale=str(parsed.get("rationale", "")).strip(),
                parse_error=parse_err,
            )

    return decisions


def _parse_strictv2_outputs(path: Path) -> Dict[str, RunDecision]:
    """Return pid -> RunDecision."""
    decisions: Dict[str, RunDecision] = {}

    for result in _iter_jsonl(path):
        custom_id = str(result.get("custom_id", ""))
        if not custom_id.endswith("__strictv2"):
            continue

        pid = custom_id[: -len("__strictv2")]
        content, err = _extract_chat_content(result)

        if err:
            decisions[pid] = RunDecision(decision="EXCLUDE", confidence=0.0, rationale=err, parse_error=err)
            continue

        parsed, parse_err = _parse_model_json(content or "")
        if not parsed:
            decisions[pid] = RunDecision(decision="EXCLUDE", confidence=0.0, rationale="parse_error", parse_error=parse_err)
            continue

        decision = str(parsed.get("decision", "EXCLUDE")).strip().upper()
        if decision not in {"INCLUDE", "EXCLUDE"}:
            decision = "EXCLUDE"

        conf = parsed.get("confidence", 0)
        try:
            conf_f = float(conf)
        except Exception:
            conf_f = 0.0

        decisions[pid] = RunDecision(
            decision=decision,
            confidence=conf_f,
            rationale=str(parsed.get("rationale", "")).strip(),
            parse_error=parse_err,
        )

    return decisions


def _parse_strictv2_outputs_many(paths: List[Path]) -> Dict[str, RunDecision]:
    merged: Dict[str, RunDecision] = {}
    for p in paths:
        part = _parse_strictv2_outputs(p)
        for k, v in part.items():
            merged[k] = v
    return merged


def _strict_final(runs: Dict[int, RunDecision]) -> Tuple[str, float, str]:
    """Return (final_decision, avg_conf, vote_string)."""
    if not runs:
        return "EXCLUDE", 0.0, "no_runs"

    votes: List[str] = []
    confs: List[float] = []
    for i in range(1, STRICT_EXPECTED_RUNS + 1):
        r = runs.get(i)
        if not r:
            votes.append("MISSING")
            confs.append(0.0)
        else:
            votes.append(r.decision)
            confs.append(r.confidence)

    avg_conf = sum(confs) / len(confs) if confs else 0.0
    final = "INCLUDE" if all(v == "INCLUDE" for v in votes) else "EXCLUDE"
    return final, avg_conf, "|".join(votes)


def _write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> None:
    ap = argparse.ArgumentParser(description="Compare strict vs strict-v2 batch decisions")
    ap.add_argument("--strict-batch-ids", nargs="*", default=None, help="Override strict batch IDs (space-separated)")
    ap.add_argument("--strictv2-batch-id", default=None, help="Override strict-v2 batch ID (single)")
    ap.add_argument("--strictv2-batch-ids", nargs="*", default=None, help="Override strict-v2 batch IDs (multi-part)")
    ap.add_argument("--wait", action="store_true", help="Wait for batches to complete")
    ap.add_argument("--poll-seconds", type=int, default=60, help="Polling interval when --wait is set")
    ap.add_argument(
        "--wait-max-seconds",
        type=int,
        default=3600,
        help="Max seconds to wait when --wait is set (0 = no limit)",
    )
    ap.add_argument(
        "--status-only",
        action="store_true",
        help="Only print batch statuses and exit (does not download/compare)",
    )
    ap.add_argument(
        "--strict-only",
        action="store_true",
        help="Only aggregate STRICT final decisions (ignores strict-v2 entirely)",
    )
    ap.add_argument(
        "--allow-partial-strictv2",
        action="store_true",
        help="Allow comparison even if strict-v2 coverage is incomplete",
    )
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY not set (set it or add it to .env)")

    client = OpenAI(api_key=api_key)

    paper_meta = _load_paper_meta()

    strict_batch_ids = args.strict_batch_ids if args.strict_batch_ids else _load_strict_batch_ids(STRICT_PROGRESS)
    if args.strictv2_batch_ids:
        strictv2_batch_ids = [b.strip() for b in args.strictv2_batch_ids if b.strip()]
    elif args.strictv2_batch_id:
        strictv2_batch_ids = [args.strictv2_batch_id.strip()]
    else:
        strictv2_batch_ids = _load_latest_strictv2_batch_ids(STRICTV2_DIR)

    print("Strict batch IDs:")
    for bid in strict_batch_ids:
        print(f"  - {bid}")
    print("Strict-v2 batch IDs:")
    for bid in strictv2_batch_ids:
        print(f"  - {bid}")

    if args.status_only:
        print("\nBatch statuses:")
        for bid in strict_batch_ids + strictv2_batch_ids:
            b = client.batches.retrieve(bid)
            status = getattr(b, "status", "")
            rc = getattr(b, "request_counts", None)
            if rc:
                completed = getattr(rc, "completed", 0)
                total = getattr(rc, "total", 0)
                failed = getattr(rc, "failed", 0)
                print(f"  {bid}: {status} ({completed}/{total}, failed={failed})")
            else:
                print(f"  {bid}: {status}")

            if status == "failed":
                errs = getattr(b, "errors", None)
                data = getattr(errs, "data", None) if errs is not None else None
                if data:
                    for e in data:
                        code = getattr(e, "code", "")
                        msg = getattr(e, "message", "")
                        if code or msg:
                            print(f"    - {code}: {msg}")
        return

    if not args.strict_only:
        # Filter out failed strict-v2 batch IDs to avoid hard failures from historical submissions.
        filtered_v2_ids: List[str] = []
        failed_v2_ids: List[str] = []
        for bid in strictv2_batch_ids:
            b = client.batches.retrieve(bid)
            status = getattr(b, "status", "")
            if status == "failed":
                failed_v2_ids.append(bid)
            else:
                filtered_v2_ids.append(bid)

        if failed_v2_ids:
            print("\n⚠️  Ignoring failed strict-v2 batches:")
            for bid in failed_v2_ids:
                print(f"  - {bid}")
            strictv2_batch_ids = filtered_v2_ids

    strict_paths: List[Path] = []
    for bid in strict_batch_ids:
        strict_paths.append(
            _download_batch_output(
                client,
                bid,
                wait=args.wait,
                poll_seconds=args.poll_seconds,
                wait_max_seconds=args.wait_max_seconds,
            )
        )

    strictv2_paths: List[Path] = []
    for bid in strictv2_batch_ids:
        strictv2_paths.append(
            _download_batch_output(
                client,
                bid,
                wait=args.wait,
                poll_seconds=args.poll_seconds,
                wait_max_seconds=args.wait_max_seconds,
            )
        )

    print("Parsing strict outputs...")
    strict_runs = _parse_strict_outputs(strict_paths)

    # STRICT-only reporting
    if args.strict_only:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        OUT_DIR.mkdir(parents=True, exist_ok=True)

        rows: List[Dict[str, Any]] = []
        include_n = 0
        exclude_n = 0
        missing_runs_n = 0

        for pid, meta in sorted(paper_meta.items()):
            runs = strict_runs.get(pid, {})
            final, avg_conf, vote_str = _strict_final(runs)
            if "MISSING" in vote_str or "no_runs" in vote_str:
                missing_runs_n += 1
            if final == "INCLUDE":
                include_n += 1
            else:
                exclude_n += 1

            rows.append(
                {
                    "pid": pid,
                    "doi": meta.doi,
                    "id": meta.id,
                    "title": meta.title,
                    "year": meta.year,
                    "database": meta.database,
                    "journal_conference": meta.journal_conference,
                    "strict_votes": vote_str,
                    "strict_final": final,
                    "strict_avg_confidence": round(avg_conf, 2),
                }
            )

        out_csv = OUT_DIR / f"strict_results_{ts}.csv"
        _write_csv(
            out_csv,
            rows,
            [
                "pid",
                "doi",
                "id",
                "title",
                "year",
                "database",
                "journal_conference",
                "strict_votes",
                "strict_final",
                "strict_avg_confidence",
            ],
        )

        summary = {
            "timestamp": datetime.now().isoformat(),
            "strict_batch_ids": strict_batch_ids,
            "total_papers": len(paper_meta),
            "include": include_n,
            "exclude": exclude_n,
            "missing_or_partial_runs": missing_runs_n,
            "output_csv": str(out_csv),
        }
        summary_path = OUT_DIR / f"strict_results_{ts}_summary.json"
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

        print("\nSTRICT results")
        print(f"  Total:   {len(paper_meta)}")
        print(f"  INCLUDE: {include_n} ({(100*include_n/len(paper_meta)):.1f}%)")
        print(f"  EXCLUDE: {exclude_n} ({(100*exclude_n/len(paper_meta)):.1f}%)")
        print(f"  Output:  {out_csv}")
        print(f"  Summary: {summary_path}")
        return

    print("Parsing strict-v2 outputs...")
    strictv2 = _parse_strictv2_outputs_many(strictv2_paths)

    # Enforce full coverage for comparison unless explicitly allowed.
    missing_v2 = [pid for pid in paper_meta.keys() if pid not in strictv2]
    if missing_v2 and not args.allow_partial_strictv2:
        raise SystemExit(
            f"Strict-v2 coverage incomplete: missing {len(missing_v2)}/{len(paper_meta)} papers. "
            "Re-run with --allow-partial-strictv2 to compare only the completed subset, "
            "or submit remaining strict-v2 batches and re-run."
        )

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows: List[Dict[str, Any]] = []
    disagreements: List[Dict[str, Any]] = []

    agree_include = 0
    agree_exclude = 0
    strict_include_v2_exclude = 0
    strict_exclude_v2_include = 0

    all_pids = set(paper_meta.keys()) | set(strict_runs.keys()) | set(strictv2.keys())

    for pid in sorted(all_pids):
        meta = paper_meta.get(pid)
        runs = strict_runs.get(pid, {})
        strict_final, strict_avg_conf, vote_str = _strict_final(runs)

        v2d = strictv2.get(pid)
        v2_decision = v2d.decision if v2d else "EXCLUDE"
        v2_conf = v2d.confidence if v2d else 0.0

        agree = strict_final == v2_decision
        if agree and strict_final == "INCLUDE":
            agree_include += 1
        elif agree and strict_final == "EXCLUDE":
            agree_exclude += 1
        elif strict_final == "INCLUDE" and v2_decision == "EXCLUDE":
            strict_include_v2_exclude += 1
        elif strict_final == "EXCLUDE" and v2_decision == "INCLUDE":
            strict_exclude_v2_include += 1

        disagreement_type = ""
        if not agree:
            disagreement_type = f"strict={strict_final}; strictv2={v2_decision}"

        row: Dict[str, Any] = {
            "pid": pid,
            "doi": meta.doi if meta else "",
            "id": meta.id if meta else "",
            "title": meta.title if meta else "",
            "year": meta.year if meta else "",
            "database": meta.database if meta else "",
            "journal_conference": meta.journal_conference if meta else "",
            "strict_votes": vote_str,
            "strict_final": strict_final,
            "strict_avg_confidence": round(strict_avg_conf, 2),
            "strictv2_decision": v2_decision,
            "strictv2_confidence": round(v2_conf, 2),
            "agree": "Y" if agree else "N",
            "disagreement_type": disagreement_type,
        }
        rows.append(row)
        if not agree:
            disagreements.append(row)

    comparison_csv = OUT_DIR / f"strict_vs_strictv2_{ts}.csv"
    disagreements_csv = OUT_DIR / f"strict_vs_strictv2_{ts}_disagreements.csv"

    fieldnames = [
        "pid",
        "doi",
        "id",
        "title",
        "year",
        "database",
        "journal_conference",
        "strict_votes",
        "strict_final",
        "strict_avg_confidence",
        "strictv2_decision",
        "strictv2_confidence",
        "agree",
        "disagreement_type",
    ]

    _write_csv(comparison_csv, rows, fieldnames)
    _write_csv(disagreements_csv, disagreements, fieldnames)

    summary: Dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "strict_batch_ids": strict_batch_ids,
        "strictv2_batch_ids": strictv2_batch_ids,
        "total_pids": len(rows),
        "agree_include": agree_include,
        "agree_exclude": agree_exclude,
        "disagree_strict_include_v2_exclude": strict_include_v2_exclude,
        "disagree_strict_exclude_v2_include": strict_exclude_v2_include,
        "disagreements_total": len(disagreements),
    }
    summary_path = OUT_DIR / f"strict_vs_strictv2_{ts}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\nDone")
    print(f"  Comparison CSV: {comparison_csv}")
    print(f"  Disagreements:  {disagreements_csv}")
    print(f"  Summary JSON:   {summary_path}")


if __name__ == "__main__":
    main()
