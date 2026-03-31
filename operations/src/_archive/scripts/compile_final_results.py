#!/usr/bin/env python3
"""
Compile final screening results from 3-model consensus (Option C).

Models:
1. STRICT (gpt-4o-mini) - 3 runs, unanimous INCLUDE
2. NANO (gpt-5-nano) - 3 runs, unanimous INCLUDE  
3. GPT-5.2 - 1 run on disagreements only

Final decision logic:
- If nano and strict agree: use that decision
- If they disagree: use gpt-5.2 as tiebreaker

Output: Final INCLUDE/EXCLUDE list for all 638 papers
"""

# Workaround for Python 3.14 Windows platform.platform() hang
import platform
platform.platform = lambda: platform.system()

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

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
GPT52_DIR = REPO_ROOT / "data" / "processed" / "batches_gpt52"
DOWNLOAD_DIR = REPO_ROOT / "data" / "processed" / "batch_downloads"
OUT_DIR = REPO_ROOT / "data" / "processed" / "final_results"


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


def _parse_model_json(content: str):
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


def _extract_chat_content(result_line):
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


def load_paper_meta():
    out = {}
    with open(S2_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = (row.get("doi") or row.get("id") or row.get("title", "")[:50] or "unknown").strip()
            out[pid] = dict(row)
    return out


def load_batch_ids(progress_path):
    data = json.loads(progress_path.read_text(encoding="utf-8"))
    return [str(b).strip() for b in data.get("batch_ids", []) if str(b).strip()]


def load_batch_ids_from_dir(dir_path):
    infos = sorted(dir_path.glob("batch_info_*.json"))
    ids = []
    for info_path in infos:
        info = json.loads(info_path.read_text(encoding="utf-8"))
        bid = str(info.get("batch_id", "")).strip()
        if bid:
            ids.append(bid)
    return ids


def download_batch_output(client, batch_id):
    cache_path = DOWNLOAD_DIR / f"{batch_id}_output.jsonl"
    if cache_path.exists():
        return cache_path
    
    batch = client.batches.retrieve(batch_id)
    if batch.status != "completed":
        raise ValueError(f"Batch {batch_id} not completed: {batch.status}")
    
    if not batch.output_file_id:
        raise ValueError(f"Batch {batch_id} has no output file")
    
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    content = client.files.content(batch.output_file_id)
    cache_path.write_text(content.text, encoding="utf-8")
    print(f"  Downloaded: {cache_path.name}")
    return cache_path


def parse_decisions_from_files(output_files, expected_runs=3):
    """Parse decisions using unanimous voting rule."""
    paper_runs = defaultdict(list)
    
    for fpath in output_files:
        for line in fpath.read_text(encoding="utf-8").strip().split("\n"):
            if not line.strip():
                continue
            result = json.loads(line)
            custom_id = result.get("custom_id", "")
            
            # Extract paper_id and run number
            if "__run" in custom_id:
                paper_id, run_part = custom_id.rsplit("__run", 1)
            else:
                paper_id = custom_id
            
            content, err = _extract_chat_content(result)
            if err:
                paper_runs[paper_id].append(("ERROR", err))
                continue
            
            parsed, perr = _parse_model_json(content)
            if perr:
                paper_runs[paper_id].append(("ERROR", perr))
                continue
            
            decision = str(parsed.get("decision", "")).upper()
            if decision not in ("INCLUDE", "EXCLUDE"):
                decision = "EXCLUDE"  # Default to exclude
            
            paper_runs[paper_id].append((decision, parsed.get("rationale", "")))
    
    # Apply unanimous voting
    final = {}
    for paper_id, runs in paper_runs.items():
        decisions = [r[0] for r in runs if r[0] in ("INCLUDE", "EXCLUDE")]
        
        if not decisions:
            final[paper_id] = "EXCLUDE"
        elif all(d == "INCLUDE" for d in decisions):
            final[paper_id] = "INCLUDE"
        else:
            final[paper_id] = "EXCLUDE"
    
    return final


def parse_single_run_decisions(output_files):
    """Parse decisions for single-run batches (gpt-5.2)."""
    final = {}
    
    for fpath in output_files:
        for line in fpath.read_text(encoding="utf-8").strip().split("\n"):
            if not line.strip():
                continue
            result = json.loads(line)
            custom_id = result.get("custom_id", "")
            
            if "__run" in custom_id:
                paper_id, _ = custom_id.rsplit("__run", 1)
            else:
                paper_id = custom_id
            
            content, err = _extract_chat_content(result)
            if err:
                final[paper_id] = "EXCLUDE"
                continue
            
            parsed, perr = _parse_model_json(content)
            if perr:
                final[paper_id] = "EXCLUDE"
                continue
            
            decision = str(parsed.get("decision", "")).upper()
            if decision not in ("INCLUDE", "EXCLUDE"):
                decision = "EXCLUDE"
            
            final[paper_id] = decision
    
    return final


def main():
    client = OpenAI()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load paper metadata
    papers = load_paper_meta()
    print(f"Loaded {len(papers)} papers from ES-filtered file")
    
    # Load batch IDs
    strict_ids = load_batch_ids(STRICT_PROGRESS)
    nano_ids = load_batch_ids_from_dir(NANO_DIR)
    gpt52_ids = load_batch_ids_from_dir(GPT52_DIR)
    
    print(f"\nBatch IDs:")
    print(f"  STRICT: {len(strict_ids)}")
    print(f"  NANO: {len(nano_ids)}")
    print(f"  GPT-5.2: {len(gpt52_ids)}")
    
    # Download outputs
    print("\nDownloading outputs...")
    strict_files = [download_batch_output(client, bid) for bid in strict_ids]
    nano_files = [download_batch_output(client, bid) for bid in nano_ids]
    gpt52_files = [download_batch_output(client, bid) for bid in gpt52_ids]
    
    # Parse decisions
    print("\nParsing decisions...")
    strict_decisions = parse_decisions_from_files(strict_files, expected_runs=3)
    nano_decisions = parse_decisions_from_files(nano_files, expected_runs=3)
    gpt52_decisions = parse_single_run_decisions(gpt52_files)
    
    print(f"  STRICT: {len(strict_decisions)} papers")
    print(f"  NANO: {len(nano_decisions)} papers")
    print(f"  GPT-5.2: {len(gpt52_decisions)} papers (disagreements only)")
    
    # Compute final decisions
    print("\nComputing final 3-model consensus...")
    
    final_decisions = {}
    stats = {
        "agree_include": 0,
        "agree_exclude": 0,
        "disagree_gpt52_include": 0,
        "disagree_gpt52_exclude": 0,
        "missing": 0
    }
    
    for paper_id in papers:
        strict_d = strict_decisions.get(paper_id, "EXCLUDE")
        nano_d = nano_decisions.get(paper_id, "EXCLUDE")
        
        if strict_d == nano_d:
            # Agreement - use that decision
            final_decisions[paper_id] = strict_d
            if strict_d == "INCLUDE":
                stats["agree_include"] += 1
            else:
                stats["agree_exclude"] += 1
        else:
            # Disagreement - use gpt-5.2 as tiebreaker
            gpt52_d = gpt52_decisions.get(paper_id)
            if gpt52_d:
                final_decisions[paper_id] = gpt52_d
                if gpt52_d == "INCLUDE":
                    stats["disagree_gpt52_include"] += 1
                else:
                    stats["disagree_gpt52_exclude"] += 1
            else:
                # Fallback to EXCLUDE if no gpt-5.2 decision
                final_decisions[paper_id] = "EXCLUDE"
                stats["missing"] += 1
    
    # Count final results
    include_count = sum(1 for d in final_decisions.values() if d == "INCLUDE")
    exclude_count = sum(1 for d in final_decisions.values() if d == "EXCLUDE")
    
    # Print results
    print("\n" + "=" * 60)
    print("FINAL 3-MODEL CONSENSUS RESULTS")
    print("=" * 60)
    print(f"Total papers: {len(final_decisions)}")
    print(f"\n**FINAL INCLUDE: {include_count} ({100*include_count/len(final_decisions):.1f}%)**")
    print(f"**FINAL EXCLUDE: {exclude_count} ({100*exclude_count/len(final_decisions):.1f}%)**")
    
    print(f"\nBreakdown:")
    print(f"  Strict+Nano agree INCLUDE: {stats['agree_include']}")
    print(f"  Strict+Nano agree EXCLUDE: {stats['agree_exclude']}")
    print(f"  Disagreed → GPT-5.2 INCLUDE: {stats['disagree_gpt52_include']}")
    print(f"  Disagreed → GPT-5.2 EXCLUDE: {stats['disagree_gpt52_exclude']}")
    if stats["missing"]:
        print(f"  Missing GPT-5.2 decision: {stats['missing']}")
    
    # Write output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Full results CSV
    csv_path = OUT_DIR / f"final_screening_results_{timestamp}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "title", "abstract_snippet", "strict_decision", "nano_decision", "gpt52_decision", "final_decision"])
        for paper_id, meta in papers.items():
            writer.writerow([
                paper_id,
                meta.get("title", ""),
                meta.get("abstract_snippet", "")[:500],
                strict_decisions.get(paper_id, ""),
                nano_decisions.get(paper_id, ""),
                gpt52_decisions.get(paper_id, ""),
                final_decisions.get(paper_id, "")
            ])
    print(f"\nWrote: {csv_path.name}")
    
    # Include-only CSV
    include_path = OUT_DIR / f"final_included_papers_{timestamp}.csv"
    with open(include_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "title", "abstract_snippet"])
        for paper_id, meta in papers.items():
            if final_decisions.get(paper_id) == "INCLUDE":
                writer.writerow([
                    paper_id,
                    meta.get("title", ""),
                    meta.get("abstract_snippet", "")
                ])
    print(f"Wrote: {include_path.name}")
    
    # Summary JSON
    summary = {
        "timestamp": timestamp,
        "total_papers": len(final_decisions),
        "final_include": include_count,
        "final_exclude": exclude_count,
        "include_pct": round(100 * include_count / len(final_decisions), 1),
        "breakdown": stats,
        "models": {
            "strict": "gpt-4o-mini (3 runs, unanimous)",
            "nano": "gpt-5-nano (3 runs, unanimous)",
            "gpt52": "gpt-5.2 (1 run, tiebreaker)"
        }
    }
    summary_path = OUT_DIR / f"final_screening_summary_{timestamp}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote: {summary_path.name}")
    
    print("\n" + "=" * 60)
    print("SCREENING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
