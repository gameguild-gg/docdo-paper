#!/usr/bin/env python3
"""
Submit gpt-5-nano batch for Option C validation strategy.

Purpose:
- Run cheapest model (gpt-5-nano) on all 638 ES-filtered papers
- Compare with gpt-4o-mini STRICT results
- Identify disagreements for gpt-5.2 final validation

Input: data/processed/S2_elasticsearch_filtered.csv (638 papers)
Output: data/processed/batches_nano/
"""

# Workaround for Python 3.14 Windows platform.platform() hang
import platform
platform.platform = lambda: platform.system()

import csv
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

REPO_ROOT = Path(__file__).parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

INPUT_FILE = REPO_ROOT / "data" / "processed" / "S2_elasticsearch_filtered.csv"
OUT_DIR = REPO_ROOT / "data" / "processed" / "batches_nano"

MODEL = "gpt-5-nano"
# Note: gpt-5-nano does NOT support temperature parameter (only default=1 allowed)
NUM_RUNS = 3  # Same as STRICT for consistency

# Same prompt as STRICT (gpt-4o-mini) for fair comparison
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


def load_papers():
    papers = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)
    return papers


def create_batch_requests(papers, run_number):
    requests = []
    for paper in papers:
        paper_id = paper.get('doi') or paper.get('id') or paper.get('title', '')[:50]
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
                "max_completion_tokens": 300
            }
        }
        requests.append(request)
    return requests


def main():
    client = OpenAI()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    papers = load_papers()
    total_papers = len(papers)
    print(f"Total ES-filtered papers: {total_papers}")
    print(f"Model: {MODEL}")
    print(f"Runs per paper: {NUM_RUNS}")
    print(f"Total requests: {total_papers * NUM_RUNS}")
    print(f"\nEstimated cost: ~$0.18 (3.83M input + 0.38M output tokens)")
    
    # Create batch requests for all runs
    all_requests = []
    for run in range(1, NUM_RUNS + 1):
        all_requests.extend(create_batch_requests(papers, run))
    
    print(f"\nCreated {len(all_requests)} requests")
    
    # Write JSONL file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_file = OUT_DIR / f"batch_nano_{timestamp}.jsonl"
    
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
    
    try:
        batch = client.batches.create(
            input_file_id=uploaded.id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
                "model": MODEL,
                "papers": str(total_papers),
                "runs": str(NUM_RUNS),
                "strategy": "Option C - nano pre-filter",
                "description": f"gpt-5-nano screening of {total_papers} ES-filtered papers"
            }
        )
        print(f"\n✅ Batch submitted successfully!")
        print(f"   ID: {batch.id}")
        print(f"   Status: {batch.status}")
        print(f"   Requests: {batch.request_counts.total}")
        
        # Save batch info
        info_file = OUT_DIR / f"batch_info_{batch.id}.json"
        with open(info_file, 'w') as f:
            json.dump({
                "batch_id": batch.id,
                "model": MODEL,
                "total_papers": total_papers,
                "num_runs": NUM_RUNS,
                "total_requests": len(all_requests),
                "submitted_at": timestamp,
                "strategy": "Option C - nano pre-filter"
            }, f, indent=2)
        
        print(f"\nNext steps:")
        print(f"  1. Monitor: python check_batch_status.py")
        print(f"  2. When done: python compare_nano_vs_strict.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
