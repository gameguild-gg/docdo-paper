#!/usr/bin/env python3
"""
Cancel existing GPT batches and resubmit with Elasticsearch-filtered data.

This script:
1. Cancels all in-progress batch jobs
2. Submits the 638 ES-filtered papers for screening
3. Uses gpt-4o-mini with 3 runs per paper
"""

import os
import csv
import json
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parent.parent.parent / ".env")

# Use the ES-filtered data (638 papers)
INPUT_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_elasticsearch_filtered.csv"
BATCH_DIR = Path(__file__).parent.parent.parent / "data" / "processed" / "batches_esfiltered"

MODEL = "gpt-4o-mini"
NUM_RUNS = 3
TEMPERATURE = 0.3
BATCH_SIZE = 350  # Smaller batches for 638 papers

# Screening prompt - strict, no "uncertain" allowed
SCREENING_PROMPT = """You are screening papers for a systematic review on "3D Organ Segmentation from CT Scans using Deep Learning".

## STRICT DECISION PROTOCOL: NO "UNCERTAIN" - You must decide INCLUDE or EXCLUDE.

## INCLUSION CRITERIA (ALL must be met):

**IC1 - Deep Learning Method:**
Uses neural networks (CNN, Transformer, U-Net, encoder-decoder, attention mechanisms).
NOT: Traditional ML (SVM, Random Forest), rule-based, classical image processing.

**IC2 - 3D Volumetric Segmentation:**
Processes volumetric data with 3D spatial context (3D conv, 2.5D, or slice-based with 3D post-processing).
NOT: Pure 2D single-slice without any volumetric aggregation.

**IC3 - CT Imaging Modality:**
Uses Computed Tomography (with or without contrast, multi-modal OK if includes CT).
NOT: MRI-only, ultrasound-only, X-ray-only, PET-only.

**IC4 - Anatomical Organ Segmentation:**
Segments organs: liver, kidney, spleen, pancreas, lung, heart, stomach, gallbladder, bladder, prostate, colon, esophagus, adrenal glands.
NOT: Tumors/lesions only, vessels only, bones only, muscles only, airways only.
OK: Organ + tumor together, organs-at-risk for radiotherapy.

**IC5 - Original Research:**
Presents novel method, architecture, training strategy, or benchmark comparison with insights.
NOT: Pure review/survey papers, dataset-only papers, editorials.

## EXCLUSION TRIGGERS (ANY one excludes):
- EC1: Detection/classification only (no spatial segmentation)
- EC2: Non-CT modalities exclusively
- EC3: Non-organ targets exclusively (tumors, vessels, bones, muscles, COVID lesions)
- EC4: 2D-only without volumetric context
- EC5: Non-deep learning methods
- EC6: Review papers without novel methodology

## DECISION RULE:
- If ALL IC1-IC5 are clearly met and NO EC triggers → INCLUDE
- If ANY doubt or missing information → EXCLUDE (conservative approach)
- NO "UNCERTAIN" ALLOWED

---
TITLE: {title}
ABSTRACT: {abstract}
---

Return ONLY valid JSON:
{{"decision": "INCLUDE" | "EXCLUDE", "confidence": 70-95, "rationale": "One sentence", "criteria_met": ["IC1",...], "criteria_failed": ["EC1",...]}}"""


def cancel_all_batches(client):
    """Cancel all in-progress batches."""
    print("\n🛑 Cancelling existing batches...")
    batches = client.batches.list(limit=50)
    cancelled = 0
    
    for batch in batches.data:
        if batch.status in ['in_progress', 'validating', 'finalizing']:
            try:
                client.batches.cancel(batch.id)
                print(f"   Cancelled: {batch.id} (was {batch.status})")
                cancelled += 1
            except Exception as e:
                print(f"   Failed to cancel {batch.id}: {e}")
    
    if cancelled == 0:
        print("   No active batches to cancel.")
    else:
        print(f"   ✅ Cancelled {cancelled} batches")
    
    return cancelled


def create_batch_requests(papers, run_number):
    """Create JSONL batch requests for one screening run."""
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
                "messages": [
                    {"role": "system", "content": "You are a systematic review screening assistant. Always respond with valid JSON only. NEVER respond with 'UNCERTAIN'."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": TEMPERATURE,
                "max_tokens": 300
            }
        }
        requests.append(request)
    
    return requests


def submit_batch(client, papers, batch_num):
    """Submit a batch of papers (3 runs per paper)."""
    all_requests = []
    for run_num in range(1, NUM_RUNS + 1):
        all_requests.extend(create_batch_requests(papers, run_num))
    
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    batch_file = BATCH_DIR / f"esfilter_batch_{batch_num:03d}_input.jsonl"
    
    with open(batch_file, 'w', encoding='utf-8') as f:
        for req in all_requests:
            f.write(json.dumps(req) + '\n')
    
    print(f"   Created batch file: {batch_file.name} ({len(all_requests)} requests)")
    
    with open(batch_file, 'rb') as f:
        file_obj = client.files.create(file=f, purpose="batch")
    
    batch = client.batches.create(
        input_file_id=file_obj.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": f"S2 ES-Filtered Screening Batch {batch_num}"}
    )
    
    return batch.id


def main():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    print("=" * 70)
    print("  CANCEL EXISTING BATCHES & SUBMIT ES-FILTERED DATA")
    print("=" * 70)
    
    # Step 1: Cancel all existing batches
    cancel_all_batches(client)
    time.sleep(2)  # Wait for cancellation to propagate
    
    # Step 2: Load ES-filtered papers
    print(f"\n📂 Loading ES-filtered papers from: {INPUT_FILE.name}")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        papers = list(csv.DictReader(f))
    
    print(f"   Loaded {len(papers)} papers (ES-filtered)")
    
    # Step 3: Submit batches
    print(f"\n📤 Submitting batches ({len(papers)} papers × {NUM_RUNS} runs = {len(papers) * NUM_RUNS} total requests)...")
    
    batch_ids = []
    batch_num = 1
    
    for start_idx in range(0, len(papers), BATCH_SIZE):
        end_idx = min(start_idx + BATCH_SIZE, len(papers))
        batch_papers = papers[start_idx:end_idx]
        
        print(f"\n   Batch {batch_num}: papers {start_idx+1}-{end_idx}")
        
        try:
            batch_id = submit_batch(client, batch_papers, batch_num)
            batch_ids.append(batch_id)
            print(f"   ✅ Submitted: {batch_id}")
            batch_num += 1
        except Exception as e:
            print(f"   ❌ Error: {e}")
            break
    
    # Save progress
    progress_file = BATCH_DIR / "esfilter_submission_progress.json"
    progress = {
        "timestamp": datetime.now().isoformat(),
        "input_file": str(INPUT_FILE),
        "total_papers": len(papers),
        "batch_ids": batch_ids,
        "model": MODEL,
        "num_runs": NUM_RUNS
    }
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)
    
    # Summary
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    print(f"  Total papers: {len(papers)}")
    print(f"  Batches submitted: {len(batch_ids)}")
    print(f"  Total requests: {len(papers) * NUM_RUNS}")
    print(f"  Model: {MODEL}")
    print(f"  Progress saved to: {progress_file.name}")
    print("=" * 70)
    
    print("\n🔍 Check batch status with:")
    print("   openai api batches list")
    print("\nOr run monitor script to watch progress.")


if __name__ == "__main__":
    main()
