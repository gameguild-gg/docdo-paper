#!/usr/bin/env python3
"""Compare gpt-5-nano vs gpt-4o-mini (STRICT) screening outcomes.

This script:
1) Downloads nano batch output
2) Downloads strict batch output (if not cached)
3) Compares decisions
4) Identifies disagreements for gpt-5.2 final batch
5) Creates input file for gpt-5.2 batch (disagreements + nano INCLUDE)

Usage:
  python supplementary/scripts/compare_nano_vs_strict.py
  python supplementary/scripts/compare_nano_vs_strict.py --wait
"""

# Workaround for Python 3.14 Windows platform.platform() hang
import platform
platform.platform = lambda: platform.system()

import argparse
import csv
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*_args, **_kwargs): return False

from openai import OpenAI

REPO_ROOT = Path(__file__).parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

S2_FILE = REPO_ROOT / "data" / "processed" / "S2_elasticsearch_filtered.csv"
STRICT_PROGRESS = REPO_ROOT / "data" / "processed" / "batches_esfiltered" / "esfilter_submission_progress.json"
NANO_DIR = REPO_ROOT / "data" / "processed" / "batches_nano"

DOWNLOAD_DIR = REPO_ROOT / "data" / "processed" / "batch_downloads"
OUT_DIR = REPO_ROOT / "data" / "processed" / "comparisons"

STRICT_EXPECTED_RUNS = 3
NANO_EXPECTED_RUNS = 3


@dataclass
class RunDecision:
    decision: str
    confidence: float
    rationale: str
    parse_error: str = ""


def _paper_id_from_row(row: Dict[str, str]) -> str:
    return (row.get("doi") or row.get("id") or row.get("title", "")[:50] or "unknown").strip()


def _load_paper_meta() -> Dict[str, Dict[str, str]]:
    if not S2_FILE.exists():
        raise SystemExit(f"Missing input file: {S2_FILE}")
    
    out = {}
    with open(S2_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = _paper_id_from_row(row)
            out[pid] = dict(row)
    return out


def _load_batch_ids(progress_path: Path) -> List[str]:
    if not progress_path.exists():
        raise SystemExit(f"Missing progress file: {progress_path}")
    
    data = json.loads(progress_path.read_text(encoding="utf-8"))
    batch_ids = data.get("batch_ids", [])
    return [str(b).strip() for b in batch_ids if str(b).strip()]


def _load_nano_batch_ids() -> List[str]:
    if not NANO_DIR.exists():
        raise SystemExit(f"Missing nano directory: {NANO_DIR}")
    
    infos = sorted(NANO_DIR.glob("batch_info_*.json"))
    if not infos:
        raise SystemExit(f"No nano batch info found in: {NANO_DIR}")
    
    ids = []
    for info_path in infos:
        info = json.loads(info_path.read_text(encoding="utf-8"))
        bid = str(info.get("batch_id", "")).strip()
        if bid:
            ids.append(bid)
    return ids


def _strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        parts = t.split("```")
        if len(parts) >= 2:
            t = parts[1]
        t = t.strip()
        if t.lower().startswith("json"):
            t = t[4:].strip()
    return t


_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse_model_json(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
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
    response = result_line.get("response", {})
    if not isinstance(response, dict):
        response = {}
    
    status_code = response.get("status_code")
    
    if status_code == 200:
        body = response.get("body", {})
        choices = body.get("choices", [])
        if choices and isinstance(choices, list):
            first = choices[0] if choices else {}
            msg = first.get("message", {})
            content = msg.get("content")
            return (str(content) if content is not None else ""), ""
        return None, "missing_choices"
    
    err = result_line.get("error", {})
    err_msg = err.get("message") if isinstance(err, dict) else str(err)
    return None, f"api_error: {err_msg}"


def _download_batch_output(client: OpenAI, batch_id: str, *, wait: bool, poll_seconds: int = 30) -> Path:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DOWNLOAD_DIR / f"{batch_id}_output.jsonl"
    
    if out_path.exists():
        print(f"  Using cached: {out_path.name}")
        return out_path
    
    while True:
        batch = client.batches.retrieve(batch_id)
        status = getattr(batch, "status", "")
        
        if status == "completed":
            output_file_id = getattr(batch, "output_file_id", None)
            if not output_file_id:
                raise SystemExit(f"Batch {batch_id} completed but has no output_file_id")
            
            content = client.files.content(output_file_id)
            out_path.write_text(content.text, encoding="utf-8")
            print(f"  Downloaded: {out_path.name}")
            return out_path
        
        if status in {"failed", "expired", "cancelled", "cancelling"}:
            raise SystemExit(f"Batch {batch_id} is in terminal state: {status}")
        
        if not wait:
            raise SystemExit(f"Batch {batch_id} not completed (status={status}). Re-run with --wait.")
        
        print(f"  Waiting for {batch_id} (status={status})...")
        time.sleep(poll_seconds)


def _parse_batch_outputs(paths: List[Path], expected_runs: int) -> Dict[str, str]:
    """Return pid -> final decision (INCLUDE/EXCLUDE)."""
    decisions: Dict[str, Dict[int, RunDecision]] = {}
    
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                result = json.loads(line)
                
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
                    decisions[pid][run_num] = RunDecision(decision="EXCLUDE", confidence=0.0, rationale="parse_error", parse_error=parse_err)
                    continue
                
                decision = str(parsed.get("decision", "EXCLUDE")).strip().upper()
                if decision not in ("INCLUDE", "EXCLUDE"):
                    decision = "EXCLUDE"
                
                confidence = float(parsed.get("confidence", 0))
                rationale = str(parsed.get("rationale", ""))
                
                decisions[pid][run_num] = RunDecision(decision=decision, confidence=confidence, rationale=rationale)
    
    # Aggregate: unanimous INCLUDE required
    final: Dict[str, str] = {}
    for pid, runs in decisions.items():
        if len(runs) < expected_runs:
            final[pid] = "EXCLUDE"  # Missing runs -> exclude
            continue
        
        all_include = all(r.decision == "INCLUDE" for r in runs.values())
        final[pid] = "INCLUDE" if all_include else "EXCLUDE"
    
    return final


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wait", action="store_true", help="Wait for batches to complete")
    parser.add_argument("--poll-seconds", type=int, default=30)
    args = parser.parse_args()
    
    client = OpenAI()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load paper metadata
    papers = _load_paper_meta()
    print(f"Loaded {len(papers)} papers from ES-filtered file")
    
    # Load batch IDs
    print("\nLoading batch IDs...")
    strict_ids = _load_batch_ids(STRICT_PROGRESS)
    print(f"  STRICT (gpt-4o-mini): {len(strict_ids)} batches")
    
    nano_ids = _load_nano_batch_ids()
    print(f"  NANO (gpt-5-nano): {len(nano_ids)} batches")
    
    # Download outputs
    print("\nDownloading STRICT outputs...")
    strict_paths = []
    for bid in strict_ids:
        path = _download_batch_output(client, bid, wait=args.wait, poll_seconds=args.poll_seconds)
        strict_paths.append(path)
    
    print("\nDownloading NANO outputs...")
    nano_paths = []
    for bid in nano_ids:
        path = _download_batch_output(client, bid, wait=args.wait, poll_seconds=args.poll_seconds)
        nano_paths.append(path)
    
    # Parse decisions
    print("\nParsing decisions...")
    strict_decisions = _parse_batch_outputs(strict_paths, STRICT_EXPECTED_RUNS)
    nano_decisions = _parse_batch_outputs(nano_paths, NANO_EXPECTED_RUNS)
    
    print(f"  STRICT: {len(strict_decisions)} papers")
    print(f"  NANO: {len(nano_decisions)} papers")
    
    # Compare
    print("\nComparing...")
    agree_include = []
    agree_exclude = []
    disagree_strict_inc_nano_exc = []
    disagree_strict_exc_nano_inc = []
    
    for pid in papers:
        strict_dec = strict_decisions.get(pid, "MISSING")
        nano_dec = nano_decisions.get(pid, "MISSING")
        
        if strict_dec == "MISSING" or nano_dec == "MISSING":
            continue
        
        if strict_dec == "INCLUDE" and nano_dec == "INCLUDE":
            agree_include.append(pid)
        elif strict_dec == "EXCLUDE" and nano_dec == "EXCLUDE":
            agree_exclude.append(pid)
        elif strict_dec == "INCLUDE" and nano_dec == "EXCLUDE":
            disagree_strict_inc_nano_exc.append(pid)
        elif strict_dec == "EXCLUDE" and nano_dec == "INCLUDE":
            disagree_strict_exc_nano_inc.append(pid)
    
    # Summary
    total_compared = len(agree_include) + len(agree_exclude) + len(disagree_strict_inc_nano_exc) + len(disagree_strict_exc_nano_inc)
    
    print(f"\n{'='*60}")
    print("COMPARISON RESULTS: STRICT (gpt-4o-mini) vs NANO (gpt-5-nano)")
    print(f"{'='*60}")
    print(f"Total compared: {total_compared}")
    print(f"\nAgreements:")
    print(f"  Both INCLUDE: {len(agree_include)}")
    print(f"  Both EXCLUDE: {len(agree_exclude)}")
    print(f"\nDisagreements:")
    print(f"  STRICT=INCLUDE, NANO=EXCLUDE: {len(disagree_strict_inc_nano_exc)}")
    print(f"  STRICT=EXCLUDE, NANO=INCLUDE: {len(disagree_strict_exc_nano_inc)}")
    
    # Papers for gpt-5.2 (disagreements + nano INCLUDE)
    papers_for_52 = set()
    papers_for_52.update(disagree_strict_inc_nano_exc)
    papers_for_52.update(disagree_strict_exc_nano_inc)
    papers_for_52.update(agree_include)  # Include all INCLUDE papers for validation
    
    print(f"\n{'='*60}")
    print("PAPERS FOR GPT-5.2 FINAL VALIDATION")
    print(f"{'='*60}")
    print(f"Disagreements: {len(disagree_strict_inc_nano_exc) + len(disagree_strict_exc_nano_inc)}")
    print(f"Agree INCLUDE (need validation): {len(agree_include)}")
    print(f"Total for gpt-5.2: {len(papers_for_52)}")
    
    # Estimate cost
    est_input = len(papers_for_52) * 3 * 2000 / 1_000_000  # M tokens
    est_output = len(papers_for_52) * 3 * 200 / 1_000_000
    est_cost = est_input * 0.875 + est_output * 7.00
    print(f"\nEstimated gpt-5.2 cost: ${est_cost:.2f}")
    
    # Write outputs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Full comparison CSV
    comparison_file = OUT_DIR / f"nano_vs_strict_{timestamp}.csv"
    with open(comparison_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "title", "strict_decision", "nano_decision", "agreement"])
        for pid in papers:
            strict_dec = strict_decisions.get(pid, "MISSING")
            nano_dec = nano_decisions.get(pid, "MISSING")
            if strict_dec == "MISSING" or nano_dec == "MISSING":
                continue
            agree = "YES" if strict_dec == nano_dec else "NO"
            title = papers[pid].get("title", "")
            writer.writerow([pid, title, strict_dec, nano_dec, agree])
    print(f"\nWrote: {comparison_file.name}")
    
    # 2. Papers for gpt-5.2 CSV
    papers_52_file = OUT_DIR / f"papers_for_gpt52_{timestamp}.csv"
    with open(papers_52_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "title", "abstract_snippet", "strict_decision", "nano_decision", "reason"])
        for pid in papers_for_52:
            paper = papers.get(pid, {})
            strict_dec = strict_decisions.get(pid, "MISSING")
            nano_dec = nano_decisions.get(pid, "MISSING")
            
            if strict_dec == nano_dec:
                reason = "agree_include_needs_validation"
            else:
                reason = "disagreement"
            
            writer.writerow([
                pid,
                paper.get("title", ""),
                paper.get("abstract_snippet", "") or paper.get("abstract", ""),
                strict_dec,
                nano_dec,
                reason
            ])
    print(f"Wrote: {papers_52_file.name}")
    
    # 3. Summary JSON
    summary = {
        "timestamp": timestamp,
        "models": {
            "strict": "gpt-4o-mini",
            "nano": "gpt-5-nano"
        },
        "total_compared": total_compared,
        "agree_include": len(agree_include),
        "agree_exclude": len(agree_exclude),
        "disagree_strict_inc_nano_exc": len(disagree_strict_inc_nano_exc),
        "disagree_strict_exc_nano_inc": len(disagree_strict_exc_nano_inc),
        "papers_for_gpt52": len(papers_for_52),
        "estimated_gpt52_cost": round(est_cost, 2),
        "output_files": {
            "comparison": comparison_file.name,
            "papers_for_52": papers_52_file.name
        }
    }
    
    summary_file = OUT_DIR / f"nano_vs_strict_{timestamp}_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote: {summary_file.name}")
    
    print(f"\n{'='*60}")
    print("NEXT STEP: Run gpt-5.2 on the selected papers")
    print(f"  python supplementary/scripts/submit_gpt52_batch.py --input {papers_52_file.name}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
