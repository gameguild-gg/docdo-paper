#!/usr/bin/env python3
"""
Submit batch with alternative model (gpt-3.5-turbo or gpt-4-turbo).
Each model has SEPARATE quota, so you can run batches in parallel!
"""

import os
import csv
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parent.parent.parent / ".env")

INPUT_FILE = Path(__file__).parent.parent.parent / "data" / "interim" / "S1_search_results_deduplicated.csv"
BATCH_DIR = Path(__file__).parent.parent.parent / "data" / "processed" / "batches"

# Change this to try different models
# Batch API pricing (per 1M tokens): gpt-5-nano=$0.025/$0.20, gpt-4.1-nano=$0.05/$0.20, gpt-4o-mini=$0.075/$0.30
MODEL = "gpt-5-nano"  # Cheapest option!
NUM_RUNS = 3
TEMPERATURE = 0.3
BATCH_SIZE = 500  # Papers per batch

# Improved screening prompt (v1.2)
SCREENING_PROMPT = """You are screening papers for a systematic review on "3D Organ Segmentation from CT Scans using Deep Learning".

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

BE DECISIVE. Papers with "CT", "organ segmentation", and "deep learning/neural network" are usually INCLUDE.

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
        
        # Use max_completion_tokens for gpt-5 models, max_tokens for others
        token_param = "max_completion_tokens" if MODEL.startswith("gpt-5") else "max_tokens"
        
        request = {
            "custom_id": f"{paper_id}__run{run_number}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": TEMPERATURE,
                token_param: 300
            }
        }
        requests.append(request)
    return requests


def main():
    client = OpenAI()
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    
    papers = load_papers()
    total_papers = len(papers)
    print(f"Total papers: {total_papers}")
    print(f"Model: {MODEL}")
    
    # Ask which range to submit
    print("\nWhich papers to submit?")
    print("  1. Papers 1-500")
    print("  2. Papers 501-1000") 
    print("  3. Papers 1001-1500")
    print("  4. Papers 1501-2000")
    print("  5. Papers 2001-2500")
    print("  6. Papers 2501-2821")
    print("  7. ALL papers (0-2821)")
    
    choice = input("\nEnter choice (1-7): ").strip()
    
    ranges = {
        "1": (0, 500),
        "2": (500, 1000),
        "3": (1000, 1500),
        "4": (1500, 2000),
        "5": (2000, 2500),
        "6": (2500, total_papers),
        "7": (0, total_papers)
    }
    
    if choice not in ranges:
        print("Invalid choice")
        return
    
    start, end = ranges[choice]
    selected_papers = papers[start:end]
    print(f"\nSubmitting papers {start+1}-{end} ({len(selected_papers)} papers)")
    
    # Create batch requests for all 3 runs
    all_requests = []
    for run in range(1, NUM_RUNS + 1):
        all_requests.extend(create_batch_requests(selected_papers, run))
    
    print(f"Total requests: {len(all_requests)} ({len(selected_papers)} papers × {NUM_RUNS} runs)")
    
    # Write JSONL file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_file = BATCH_DIR / f"batch_{MODEL}_{start}_{end}_{timestamp}.jsonl"
    
    with open(batch_file, 'w', encoding='utf-8') as f:
        for req in all_requests:
            f.write(json.dumps(req) + '\n')
    
    print(f"Created batch file: {batch_file.name}")
    
    # Upload and submit
    confirm = input("\nSubmit batch? (y/n): ").strip().lower()
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
                "papers": f"{start+1}-{end}",
                "description": f"Screening {len(selected_papers)} papers with {MODEL}"
            }
        )
        print(f"\n✅ Batch submitted successfully!")
        print(f"   ID: {batch.id}")
        print(f"   Status: {batch.status}")
        print(f"   Requests: {batch.request_counts.total}")
        
        # Save batch info
        info_file = BATCH_DIR / f"batch_info_{batch.id}.json"
        with open(info_file, 'w') as f:
            json.dump({
                "batch_id": batch.id,
                "model": MODEL,
                "papers_start": start,
                "papers_end": end,
                "total_papers": len(selected_papers),
                "total_requests": len(all_requests),
                "submitted_at": timestamp
            }, f, indent=2)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if "enqueued" in str(e).lower():
            print("\nQuota exceeded for this model. Try a different model or wait.")


if __name__ == "__main__":
    main()
