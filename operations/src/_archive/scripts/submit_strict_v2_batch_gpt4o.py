#!/usr/bin/env python3
"""
Submit an additional STRICT-V2 validation batch using a stronger model.

Purpose:
- Keep the current strict batches running.
- Submit a second batch with *stricter* inclusion rules (agentic, no UNCERTAIN)
  using a stronger model (gpt-4o) for cross-validation.

Strict-v2 additions (beyond IC1-IC5 + EC1-EC6):
- Requires explicit evidence of quantitative evaluation on public benchmarks
  (dataset name and/or standard metrics such as Dice/HD95/NSD).

Input:
- data/processed/S2_elasticsearch_filtered.csv (638 papers)

Output:
- data/processed/batches_esfiltered_strictv2_gpt4o/*
"""

import csv
import json
import os
import argparse
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, cast

from dotenv import load_dotenv
from openai import OpenAI

# Load .env from repo root
REPO_ROOT = Path(__file__).parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

INPUT_FILE = REPO_ROOT / "data" / "processed" / "S2_elasticsearch_filtered.csv"
OUT_DIR = REPO_ROOT / "data" / "processed" / "batches_esfiltered_strictv2_gpt4o"
MANIFEST_PATH = OUT_DIR / "strictv2_manifest.json"

MODEL = "gpt-4o"
TEMPERATURE = 0.0
NUM_RUNS = 1  # validation batch; keep cost controlled while tightening rules

# gpt-4o has an enqueued-token limit; submit in smaller batches to avoid
# "token_limit_exceeded" at enqueue time.
DEFAULT_BATCH_SIZE = 80


def _is_token_limit_exceeded(batch_obj: Any) -> bool:
    errs = getattr(batch_obj, "errors", None)
    data = getattr(errs, "data", None) if errs is not None else None
    if not data:
        return False
    for e in data:
        if getattr(e, "code", None) == "token_limit_exceeded":
            return True
    return False

# STRICT-V2 prompt
SCREENING_PROMPT_V2 = """You are screening papers for a systematic review on "3D Organ Segmentation from CT Scans using Deep Learning".

## STRICT DECISION PROTOCOL: NO "UNCERTAIN".
Return ONLY INCLUDE or EXCLUDE.
If any criterion is missing or unclear -> EXCLUDE.

## REQUIRED INCLUSION CRITERIA (ALL must be clearly satisfied):

IC1 - Deep Learning Method:
- Uses neural networks (CNN, Transformer, U-Net, encoder-decoder, attention).

IC2 - 3D Volumetric Segmentation:
- Must clearly be 3D/volumetric (3D conv, volumetric network, 3D U-Net/V-Net/nnU-Net, etc.).

IC3 - CT Modality:
- Must clearly involve CT / computed tomography.

IC4 - Anatomical Organ Segmentation:
- Must segment organs (e.g., liver, kidney, spleen, pancreas, lung, heart, multi-organ, organs-at-risk).
- NOT tumors-only/vessels-only/bones-only/muscle-only/airway-only.

IC5 - Original Research:
- Must present an original method/approach/network/model/algorithm/architecture OR a substantive benchmark study.
- NOT review/survey/editorial/dataset-only.

IC6 - Quantitative Public Benchmark Evidence (STRICT-V2):
- Must clearly report quantitative segmentation evaluation AND indicate a public benchmark dataset and/or standard metrics.
- Accept if the abstract/title explicitly mentions any of:
  - A public dataset name: BTCV, MSD, AMOS, KiTS, CHAOS, LiTS, Synapse, TotalSegmentator
  - OR standard metrics: Dice/DSC, HD95/Hausdorff, NSD/ASSD
  - OR phrases like: "public dataset", "benchmark", "challenge", "MICCAI" (when tied to evaluation).
- If metrics/dataset are not clearly stated in title/abstract -> EXCLUDE.

## EXCLUSION TRIGGERS (ANY one excludes):
- EC1: Detection/classification only
- EC2: Non-CT modalities exclusively
- EC3: Non-organ targets exclusively
- EC4: 2D-only without volumetric context
- EC5: Non-deep learning
- EC6: Review/survey/dataset-only

---
TITLE: {title}
ABSTRACT: {abstract}
---

Return ONLY valid JSON:
{{"decision":"INCLUDE"|"EXCLUDE","confidence":70-95,"rationale":"One sentence","criteria_met":["IC1",...],"criteria_failed":["EC1"|"IC6",...]}}
"""


def _paper_id(paper: Mapping[str, str]) -> str:
    return (paper.get("doi") or paper.get("id") or paper.get("title", "")[:50] or "unknown").strip()


def main() -> None:
    ap = argparse.ArgumentParser(description="Submit STRICT-V2 validation batches (gpt-4o)")
    ap.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Number of papers per batch (smaller reduces enqueued-token risk)",
    )
    ap.add_argument(
        "--start",
        type=int,
        default=1,
        help="1-based paper index to start from (e.g., 81 to submit papers 81+)",
    )
    ap.add_argument(
        "--max-parts",
        type=int,
        default=0,
        help="Max number of parts to submit this run (0 = no limit)",
    )
    args = ap.parse_args()

    batch_size = int(args.batch_size)
    if batch_size <= 0:
        raise SystemExit("--batch-size must be > 0")
    start_1based = int(args.start)
    if start_1based <= 0:
        raise SystemExit("--start must be >= 1")
    max_parts = int(args.max_parts)
    if max_parts < 0:
        raise SystemExit("--max-parts must be >= 0")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY not set")

    if not INPUT_FILE.exists():
        raise SystemExit(f"Missing input file: {INPUT_FILE}")

    client = OpenAI(api_key=api_key)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    manifest: dict[str, Any] = {}
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            manifest = {}

    manifest.setdefault("model", MODEL)
    manifest.setdefault("protocol", "strict-v2 (adds IC6 public benchmark evidence)")
    manifest.setdefault("input_file", str(INPUT_FILE))
    manifest.setdefault("parts", [])

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        papers = list(csv.DictReader(f))

    if not papers:
        raise SystemExit("No papers found in input")

    batches: list[dict[str, Any]] = []
    batch_ids: list[str] = []

    start_idx = start_1based - 1
    if start_idx >= len(papers):
        raise SystemExit(f"--start {start_1based} is beyond total papers ({len(papers)})")

    parts_submitted = 0

    for batch_index, start in enumerate(range(start_idx, len(papers), batch_size), start=1):
        if max_parts and parts_submitted >= max_parts:
            break

        end = min(start + batch_size, len(papers))
        subset = papers[start:end]

        # Build requests (1 run)
        requests: list[dict[str, Any]] = []
        for paper in subset:
            pid = _paper_id(paper)
            title = paper.get("title", "")
            abstract = paper.get("abstract_snippet", "") or paper.get("abstract", "")

            prompt = SCREENING_PROMPT_V2.format(
                title=title or "No title",
                abstract=abstract or "No abstract available",
            )

            requests.append(
                {
                    "custom_id": f"{pid}__strictv2",
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a systematic review screening assistant. Always respond with valid JSON only.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": TEMPERATURE,
                        "max_tokens": 280,
                    },
                }
            )

        jsonl_path = OUT_DIR / f"strictv2_gpt4o_{ts}_part{batch_index:02d}_input.jsonl"
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for req in requests:
                f.write(json.dumps(req) + "\n")

        try:
            with open(jsonl_path, "rb") as f:
                file_obj = client.files.create(file=f, purpose="batch")

            batch = client.batches.create(
                input_file_id=file_obj.id,
                endpoint="/v1/chat/completions",
                completion_window="24h",
                metadata={
                    "description": f"S2 ES-filtered STRICT-V2 validation | {MODEL} | part {batch_index} | {len(subset)} reqs",
                    "source": "S2_elasticsearch_filtered.csv",
                    "protocol": "strict-v2 (adds IC6 public benchmark evidence)",
                    "part": str(batch_index),
                    "range": f"{start+1}-{end}",
                },
            )
        except Exception as e:
            print(f"\n❌ Failed submitting STRICT-V2 part {batch_index} ({start+1}-{end}): {e}")
            print("Stopping early; writing progress for submitted parts (if any).")
            break

        # If we immediately hit the enqueued-token limit, this batch will fail fast.
        # Stop submitting further parts; rerun later after in-progress batches complete.
        try:
            refreshed = client.batches.retrieve(batch.id)
            if getattr(refreshed, "status", "") == "failed" and _is_token_limit_exceeded(refreshed):
                print(
                    f"\n⚠️  Batch {batch.id} failed immediately due to gpt-4o enqueued token limit. "
                    "Do not submit more parts yet; rerun later."
                )
                break
        except Exception:
            pass

        part_info: dict[str, Any] = {
            "submitted_at": datetime.now().isoformat(),
            "model": MODEL,
            "temperature": TEMPERATURE,
            "num_runs": NUM_RUNS,
            "part": batch_index,
            "range": [start + 1, end],
            "requests": len(requests),
            "input_file": str(INPUT_FILE),
            "jsonl": str(jsonl_path),
            "uploaded_file_id": file_obj.id,
            "batch_id": batch.id,
        }

        info_path = OUT_DIR / f"strictv2_gpt4o_{ts}_part{batch_index:02d}_info.json"
        info_path.write_text(json.dumps(part_info, indent=2), encoding="utf-8")

        # Append to cumulative manifest (so multiple runs build a complete list)
        try:
            existing_parts_any = manifest.get("parts")
            parts_list: list[dict[str, Any]] = (
                cast(list[dict[str, Any]], existing_parts_any) if isinstance(existing_parts_any, list) else []
            )
            parts_list.append(part_info)
            manifest["parts"] = parts_list
            manifest["last_updated_at"] = datetime.now().isoformat()
            MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        except Exception:
            pass

        batches.append(part_info)
        batch_ids.append(batch.id)
        parts_submitted += 1

        print(f"Submitted STRICT-V2 part {batch_index}: {start+1}-{end} ({len(requests)} reqs)")
        print(f"  Batch ID: {batch.id}")

    progress: dict[str, Any] = {
        "submitted_at": datetime.now().isoformat(),
        "model": MODEL,
        "temperature": TEMPERATURE,
        "num_runs": NUM_RUNS,
        "batch_size": batch_size,
        "start_1based": start_1based,
        "max_parts": max_parts,
        "total_papers": len(papers),
        "total_requests": len(papers) * NUM_RUNS,
        "input_file": str(INPUT_FILE),
        "batch_ids": batch_ids,
        "parts": batches,
    }

    progress_path = OUT_DIR / f"strictv2_gpt4o_{ts}_submission_progress.json"
    progress_path.write_text(json.dumps(progress, indent=2), encoding="utf-8")

    print("\nSubmitted STRICT-V2 validation batches")
    print(f"  Model: {MODEL}")
    print(f"  Total requests: {len(papers) * NUM_RUNS}")
    print(f"  Parts: {len(batch_ids)}")
    print(f"  Progress: {progress_path}")


if __name__ == "__main__":
    main()
