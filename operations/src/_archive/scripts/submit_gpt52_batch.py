#!/usr/bin/env python3
"""
Submit gpt-5.2 batch for final validation of disagreement papers.

Purpose:
- Run high-quality model (gpt-5.2) on papers where nano and strict disagreed
- This is Option C Step 2: validate the 274 disagreements

Input: data/processed/comparisons/papers_for_gpt52_*.csv (from compare_nano_vs_strict.py)
Output: data/processed/batches_gpt52/
"""

# Workaround for Python 3.14 Windows platform.platform() hang
import platform
platform.platform = lambda: platform.system()

import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

REPO_ROOT = Path(__file__).parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

COMPARISONS_DIR = REPO_ROOT / "data" / "processed" / "comparisons"
OUT_DIR = REPO_ROOT / "data" / "processed" / "batches_gpt52"

MODEL = "gpt-5.2"
NUM_RUNS = 1  # Single run for tiebreaker

# Same prompt as STRICT/NANO for fair comparison
SCREENING_PROMPT = """You are screening papers for a systematic review on "3D Organ Segmentation from CT Scans using Deep Learning".

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

## EXCLUSION TRIGGERS (ANY one excludes):
- EC1: Detection/classification only
- EC2: Non-CT modalities exclusively
- EC3: Non-organ targets exclusively
- EC4: 2D-only without volumetric context
- EC5: Non-deep learning
- EC6: Review/survey/dataset-only

BE DECISIVE. Papers with clear "CT", "organ segmentation", and "deep learning" -> INCLUDE.
Any ambiguity -> EXCLUDE.

---
TITLE: {title}
ABSTRACT: {abstract}
---

Return ONLY valid JSON:
{{"decision": "INCLUDE" | "EXCLUDE", "confidence": 70-95, "rationale": "One sentence", "criteria_met": ["IC1",...], "criteria_failed": ["EC1",...]}}"""


def find_latest_papers_file():
    """Find the most recent papers_for_gpt52_*.csv file."""
    files = sorted(COMPARISONS_DIR.glob("papers_for_gpt52_*.csv"), reverse=True)
    if not files:
        raise SystemExit(f"No papers_for_gpt52_*.csv found in {COMPARISONS_DIR}")
    return files[0]


def load_papers(input_file):
    papers = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)
    return papers


def create_batch_requests(papers, run_number=1):
    requests = []
    for paper in papers:
        paper_id = paper.get('paper_id', '') or paper.get('doi') or paper.get('id') or paper.get('title', '')[:50]
        title = paper.get('title', '')
        abstract = paper.get('abstract_snippet', '') or paper.get('abstract', '')
        
        prompt = SCREENING_PROMPT.format(
            title=title or "No title",
            abstract=abstract or "No abstract available"
        )
        
        request = {
            "custom_id": f"{paper_id}__run{run_number}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0,  # gpt-5.2 supports temperature
                "max_completion_tokens": 300
            }
        }
        requests.append(request)
    return requests


def main():
    # Check for --input flag or find latest
    input_file = None
    for i, arg in enumerate(sys.argv):
        if arg == "--input" and i + 1 < len(sys.argv):
            input_file = Path(sys.argv[i + 1])
            if not input_file.is_absolute():
                input_file = COMPARISONS_DIR / input_file
            break
    
    if input_file is None:
        input_file = find_latest_papers_file()
    
    if not input_file.exists():
        raise SystemExit(f"Input file not found: {input_file}")
    
    client = OpenAI()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    papers = load_papers(input_file)
    total_papers = len(papers)
    
    print(f"Input file: {input_file.name}")
    print(f"Total papers for gpt-5.2: {total_papers}")
    print(f"Model: {MODEL}")
    print(f"Runs per paper: {NUM_RUNS}")
    print(f"Total requests: {total_papers * NUM_RUNS}")
    
    # Estimate cost: ~2000 input tokens, ~200 output tokens per request
    # gpt-5.2: $0.875/1M input, $7.00/1M output (batch tier)
    input_tokens = total_papers * NUM_RUNS * 2000
    output_tokens = total_papers * NUM_RUNS * 200
    est_cost = (input_tokens / 1_000_000 * 0.875) + (output_tokens / 1_000_000 * 7.00)
    print(f"\nEstimated cost: ~${est_cost:.2f}")
    
    # Create batch requests
    all_requests = []
    for run in range(1, NUM_RUNS + 1):
        all_requests.extend(create_batch_requests(papers, run))
    
    print(f"\nCreated {len(all_requests)} requests")
    
    # Write JSONL file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_file = OUT_DIR / f"batch_gpt52_{timestamp}.jsonl"
    
    with open(batch_file, 'w', encoding='utf-8') as f:
        for req in all_requests:
            f.write(json.dumps(req) + '\n')
    
    print(f"Created batch file: {batch_file.name}")
    
    # Upload and submit
    confirm = input("\nSubmit batch to OpenAI? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled")
        return
    
    print("Uploading...")
    with open(batch_file, 'rb') as f:
        uploaded = client.files.create(file=f, purpose="batch")
    print(f"Uploaded: {uploaded.id}")
    
    print("Submitting batch...")
    batch = client.batches.create(
        input_file_id=uploaded.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "model": MODEL,
            "papers": str(total_papers),
            "runs": str(NUM_RUNS),
            "strategy": "Option C - gpt-5.2 final validation",
            "description": f"gpt-5.2 validation of {total_papers} disagreement papers from nano vs strict"
        }
    )
    
    # Save batch info
    info = {
        "batch_id": batch.id,
        "input_file": input_file.name,
        "model": MODEL,
        "papers": total_papers,
        "runs": NUM_RUNS,
        "total_requests": len(all_requests),
        "status": batch.status,
        "created_at": datetime.now().isoformat()
    }
    info_path = OUT_DIR / f"batch_info_{batch.id}.json"
    info_path.write_text(json.dumps(info, indent=2), encoding="utf-8")
    
    print(f"\n✅ Batch submitted successfully!")
    print(f"   ID: {batch.id}")
    print(f"   Status: {batch.status}")
    print(f"   Requests: {batch.request_counts.total if batch.request_counts else 'pending'}")
    print(f"\nNext steps:")
    print(f"  1. Monitor: python check_batch_status.py")
    print(f"  2. When done: python compare_final_results.py")


if __name__ == "__main__":
    main()
