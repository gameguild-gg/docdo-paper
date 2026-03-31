#!/usr/bin/env python3
"""
Monitor batch progress and auto-submit remaining papers when quota frees up.

Current status:
- Batches 1-2 (papers 1-1000): in_progress with gpt-4o-mini
- Remaining (papers 1001-2821): waiting for quota

This script monitors and auto-resubmits.
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

INPUT_FILE = Path(__file__).parent.parent.parent / "data" / "interim" / "S1_search_results_deduplicated.csv"
BATCH_DIR = Path(__file__).parent.parent.parent / "data" / "processed" / "batches"
PROGRESS_FILE = BATCH_DIR / "submission_progress.json"

MODEL = "gpt-4o-mini"
NUM_RUNS = 3
TEMPERATURE = 0.3
BATCH_SIZE = 500

# Improved screening prompt (v1.2) - see supplementary/S4_screening_criteria.md
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


def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"submitted_papers": 0, "batch_ids": [], "completed_batch_ids": []}


def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


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
                "messages": [
                    {"role": "system", "content": "You are a systematic review screening assistant. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": TEMPERATURE,
                "max_tokens": 300
            }
        }
        requests.append(request)
    return requests


def submit_batch(client, papers, batch_num):
    """Submit a batch of papers."""
    all_requests = []
    for run_num in range(1, NUM_RUNS + 1):
        all_requests.extend(create_batch_requests(papers, run_num))
    
    batch_file = BATCH_DIR / f"batch_{batch_num:03d}_input.jsonl"
    with open(batch_file, 'w', encoding='utf-8') as f:
        for req in all_requests:
            f.write(json.dumps(req) + '\n')
    
    with open(batch_file, 'rb') as f:
        file_obj = client.files.create(file=f, purpose="batch")
    
    batch = client.batches.create(
        input_file_id=file_obj.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": f"S2 Screening Batch {batch_num}"}
    )
    
    return batch.id


def get_active_batches(client):
    """Get batches that are in_progress or validating."""
    batches = client.batches.list(limit=20)
    active = []
    for b in batches.data:
        if b.status in ['in_progress', 'validating']:
            active.append({
                'id': b.id,
                'status': b.status,
                'completed': b.request_counts.completed,
                'total': b.request_counts.total
            })
    return active


def main():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        all_papers = list(csv.DictReader(f))
    
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    progress = load_progress()
    
    # Already have batches 1-2 in progress (papers 0-999)
    if progress["submitted_papers"] == 0:
        progress["submitted_papers"] = 1000
        progress["batch_ids"] = [
            'batch_6970eb31099c8190b1add0e6d9bf9d84',
            'batch_6970ead762008190a8507b50ce284070'
        ]
        save_progress(progress)
    
    print("=" * 70)
    print("  BATCH MONITOR & AUTO-SUBMIT")
    print("=" * 70)
    print(f"\nTotal papers: {len(all_papers)}")
    print(f"Already submitted: {progress['submitted_papers']}")
    print(f"Remaining: {len(all_papers) - progress['submitted_papers']}")
    
    CHECK_INTERVAL = 60  # seconds
    batch_counter = len(progress["batch_ids"]) + 1
    
    while progress["submitted_papers"] < len(all_papers):
        # Check active batches
        active = get_active_batches(client)
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Active batches: {len(active)}")
        for b in active:
            pct = 100 * b['completed'] / b['total'] if b['total'] else 0
            print(f"  {b['id'][:25]}... | {b['status']} | {b['completed']}/{b['total']} ({pct:.0f}%)")
        
        # Check if any completed
        active_ids = {b['id'] for b in active}
        newly_completed = [bid for bid in progress["batch_ids"] 
                          if bid not in active_ids and bid not in progress.get("completed_batch_ids", [])]
        
        if newly_completed:
            print(f"\n✅ Completed: {newly_completed}")
            progress.setdefault("completed_batch_ids", []).extend(newly_completed)
            save_progress(progress)
        
        # Try to submit more if we have room
        if len(active) < 2 and progress["submitted_papers"] < len(all_papers):
            start_idx = progress["submitted_papers"]
            end_idx = min(start_idx + BATCH_SIZE, len(all_papers))
            batch_papers = all_papers[start_idx:end_idx]
            
            print(f"\n📤 Submitting batch {batch_counter}: papers {start_idx+1}-{end_idx}...")
            
            try:
                batch_id = submit_batch(client, batch_papers, batch_counter)
                print(f"  ✅ Submitted: {batch_id}")
                
                progress["submitted_papers"] = end_idx
                progress["batch_ids"].append(batch_id)
                save_progress(progress)
                batch_counter += 1
                
            except Exception as e:
                if "token limit" in str(e).lower():
                    print(f"  ⏳ Token limit - waiting for batches to complete...")
                else:
                    print(f"  ❌ Error: {e}")
        
        # Summary
        print(f"\nProgress: {progress['submitted_papers']}/{len(all_papers)} papers submitted")
        
        if progress["submitted_papers"] >= len(all_papers) and not active:
            print("\n🎉 All batches submitted and completed!")
            break
        
        print(f"Next check in {CHECK_INTERVAL}s... (Ctrl+C to stop)")
        time.sleep(CHECK_INTERVAL)
    
    print("\n✅ All papers submitted!")


if __name__ == "__main__":
    main()
