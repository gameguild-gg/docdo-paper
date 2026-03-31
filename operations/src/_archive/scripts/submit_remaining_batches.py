#!/usr/bin/env python3
"""
Submit remaining papers using gpt-4o (different rate limit pool).
Papers 0-999 already submitted with gpt-4o-mini.
Papers 1000-2820 will use gpt-4o.
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

# Use gpt-4o for remaining papers (different quota than gpt-4o-mini)
MODEL = "gpt-4o"
NUM_RUNS = 3
TEMPERATURE = 0.3
BATCH_SIZE = 500  # Papers per batch

SCREENING_PROMPT = """You are screening papers for a systematic review on "3D Organ Segmentation from CT Scans using Deep Learning".

INCLUSION CRITERIA (ALL must be met):
1. Uses deep learning (CNN, Transformer, U-Net, etc.) - NOT traditional ML or rule-based
2. Performs 3D volumetric segmentation - NOT 2D slice-by-slice only
3. Uses CT imaging modality - NOT MRI, ultrasound, X-ray only
4. Segments anatomical organs (liver, kidney, lung, heart, spleen, pancreas, etc.) - NOT tumors/lesions only, NOT bones/vessels only
5. Published 2015-2024
6. Original research with methodology - NOT review papers, NOT datasets-only papers

EXCLUSION CRITERIA (ANY excludes):
- Detection/classification without segmentation
- 2D-only methods
- Non-CT modalities exclusively  
- Non-organ targets (tumors, vessels, bones only)
- Survey/review papers without novel methodology

PAPER TO SCREEN:
Title: {title}
Abstract: {abstract}

Respond with JSON only:
{{"decision": "INCLUDE" or "EXCLUDE", "confidence": 0-100, "rationale": "brief reason", "criteria_met": ["list"], "criteria_failed": ["list"]}}"""


def create_batch_requests(papers, run_number, model):
    """Create JSONL batch requests."""
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
                "model": model,
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


def main():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Load all papers
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        all_papers = list(csv.DictReader(f))
    
    # Papers 1000-2820 (remaining after gpt-4o-mini batches)
    START_INDEX = 1000
    papers = all_papers[START_INDEX:]
    
    print(f"=" * 70)
    print(f"  SUBMIT REMAINING BATCHES WITH {MODEL}")
    print(f"=" * 70)
    print(f"\nPapers {START_INDEX}-{START_INDEX + len(papers) - 1}: {len(papers)} papers")
    print(f"Requests: {len(papers) * NUM_RUNS}")
    print(f"Model: {MODEL}")
    
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    
    batch_ids = []
    
    # Process in batches of 500 papers
    for batch_idx, i in enumerate(range(0, len(papers), BATCH_SIZE)):
        batch_papers = papers[i:i + BATCH_SIZE]
        batch_num = batch_idx + 3  # Continue numbering from batch 3
        
        # Create requests for all 3 runs
        all_requests = []
        for run_num in range(1, NUM_RUNS + 1):
            all_requests.extend(create_batch_requests(batch_papers, run_num, MODEL))
        
        # Write batch file
        batch_file = BATCH_DIR / f"batch_{batch_num:03d}_{MODEL}_input.jsonl"
        with open(batch_file, 'w', encoding='utf-8') as f:
            for req in all_requests:
                f.write(json.dumps(req) + '\n')
        
        print(f"\nBatch {batch_num}: {len(batch_papers)} papers ({len(all_requests)} requests)")
        print(f"  File: {batch_file.name}")
        
        # Upload and submit
        try:
            with open(batch_file, 'rb') as f:
                file_obj = client.files.create(file=f, purpose="batch")
            print(f"  Uploaded: {file_obj.id}")
            
            batch = client.batches.create(
                input_file_id=file_obj.id,
                endpoint="/v1/chat/completions",
                completion_window="24h",
                metadata={"description": f"S2 Screening Batch {batch_num} ({MODEL})"}
            )
            batch_ids.append(batch.id)
            print(f"  ✅ Submitted: {batch.id}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            if "token limit" in str(e).lower():
                print(f"\n⚠️  Token limit reached for {MODEL}. Stopping.")
                break
    
    # Save batch info
    info_file = BATCH_DIR / f"batch_info_{MODEL}.json"
    with open(info_file, 'w') as f:
        json.dump({
            "submitted_at": datetime.now().isoformat(),
            "model": MODEL,
            "start_index": START_INDEX,
            "batch_ids": batch_ids
        }, f, indent=2)
    
    print(f"\n{'=' * 70}")
    print(f"  SUBMITTED {len(batch_ids)} BATCHES")
    print(f"{'=' * 70}")
    print(f"\nBatch IDs: {batch_ids}")
    print(f"Info saved to: {info_file}")


if __name__ == "__main__":
    main()
