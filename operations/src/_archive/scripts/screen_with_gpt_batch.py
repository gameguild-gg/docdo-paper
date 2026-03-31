#!/usr/bin/env python3
"""
S2 - AI-Assisted Screening with GPT (BATCH MODE)
Uses OpenAI Batch API for 50% cost reduction.

Batch API benefits:
- 50% cheaper than synchronous API
- Up to 50,000 requests per batch
- Results within 24 hours (usually much faster)

Workflow:
1. Create batch file (JSONL) with all screening requests
2. Submit batch to OpenAI
3. Poll for completion
4. Download and process results
"""

import os
import csv
import json
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file from project root
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# Configuration
# Use ES-filtered data (638 papers) instead of full 2821
INPUT_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_elasticsearch_filtered.csv"
OUTPUT_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_screened_batch.csv"
BATCH_DIR = Path(__file__).parent.parent.parent / "data" / "processed" / "batches"

# Screening parameters
NUM_RUNS = 3
TEMPERATURE = 0.3
BATCH_SIZE = 500  # Papers per batch file (each paper = 3 requests)

# Screening prompt - strict, no "uncertain" allowed (matches cancel_and_resubmit.py)
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
                "model": "gpt-4o-mini",
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


def write_batch_file(requests, batch_num):
    """Write requests to JSONL file."""
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    batch_file = BATCH_DIR / f"batch_{batch_num:03d}_input.jsonl"
    
    with open(batch_file, 'w', encoding='utf-8') as f:
        for req in requests:
            f.write(json.dumps(req) + '\n')
    
    return batch_file


def submit_batch(client, batch_file, description):
    """Submit batch file to OpenAI."""
    # Upload file
    with open(batch_file, 'rb') as f:
        file_obj = client.files.create(file=f, purpose="batch")
    
    print(f"  Uploaded file: {file_obj.id}")
    
    # Create batch
    batch = client.batches.create(
        input_file_id=file_obj.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": description}
    )
    
    return batch


def wait_for_batch(client, batch_id, check_interval=30):
    """Poll for batch completion."""
    while True:
        batch = client.batches.retrieve(batch_id)
        status = batch.status
        
        completed = batch.request_counts.completed
        total = batch.request_counts.total
        failed = batch.request_counts.failed
        
        print(f"  Status: {status} | Progress: {completed}/{total} | Failed: {failed}", end='\r')
        
        if status == "completed":
            print(f"\n  ✅ Batch completed: {completed}/{total} requests")
            return batch
        elif status == "failed":
            print(f"\n  ❌ Batch failed!")
            return batch
        elif status == "expired":
            print(f"\n  ⏰ Batch expired!")
            return batch
        elif status in ["cancelled", "cancelling"]:
            print(f"\n  🚫 Batch cancelled!")
            return batch
        
        time.sleep(check_interval)


def download_results(client, batch):
    """Download batch results."""
    if not batch.output_file_id:
        print("  No output file available")
        return []
    
    content = client.files.content(batch.output_file_id)
    results = []
    
    for line in content.text.strip().split('\n'):
        if line:
            results.append(json.loads(line))
    
    return results


def parse_batch_results(results):
    """Parse batch results into screening decisions."""
    decisions = {}
    
    for result in results:
        custom_id = result.get('custom_id', '')
        
        # Parse custom_id: "paper_id__runN"
        if '__run' in custom_id:
            paper_id, run_part = custom_id.rsplit('__run', 1)
            run_num = int(run_part)
        else:
            continue
        
        if paper_id not in decisions:
            decisions[paper_id] = {}
        
        # Extract response
        response = result.get('response', {})
        if response.get('status_code') == 200:
            body = response.get('body', {})
            choices = body.get('choices', [])
            if choices:
                content = choices[0].get('message', {}).get('content', '')
                try:
                    # Parse JSON response
                    if content.startswith('```'):
                        content = content.split('```')[1]
                        if content.startswith('json'):
                            content = content[4:]
                        content = content.strip()
                    
                    parsed = json.loads(content)
                    decisions[paper_id][f'run_{run_num}'] = {
                        'decision': parsed.get('decision', 'UNCERTAIN'),
                        'confidence': parsed.get('confidence', 50),
                        'rationale': parsed.get('rationale', ''),
                        'criteria_met': parsed.get('criteria_met', []),
                        'criteria_failed': parsed.get('criteria_failed', [])
                    }
                except json.JSONDecodeError:
                    decisions[paper_id][f'run_{run_num}'] = {
                        'decision': 'UNCERTAIN',
                        'confidence': 0,
                        'rationale': 'JSON parse error'
                    }
        else:
            error = result.get('error', {})
            decisions[paper_id][f'run_{run_num}'] = {
                'decision': 'UNCERTAIN',
                'confidence': 0,
                'rationale': f"API error: {error.get('message', 'unknown')}"
            }
    
    return decisions


def determine_final_decision(runs):
    """Unanimous voting: INCLUDE only if ALL runs agree, otherwise EXCLUDE."""
    include_count = sum(1 for r in runs.values() if r.get('decision') == 'INCLUDE')
    exclude_count = sum(1 for r in runs.values() if r.get('decision') == 'EXCLUDE')
    
    total_runs = len(runs)
    if total_runs == 0:
        return 'EXCLUDE', 0, 'No valid runs'
    
    avg_confidence = sum(r.get('confidence', 50) for r in runs.values()) / total_runs
    
    # Unanimous agreement required for INCLUDE (conservative approach)
    if include_count == total_runs:
        return 'INCLUDE', avg_confidence, f"{include_count}/{total_runs} INCLUDE (unanimous)"
    else:
        return 'EXCLUDE', avg_confidence, f"{include_count}I/{exclude_count}E - no consensus"


def main():
    # Check API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set!")
        return
    
    client = OpenAI(api_key=api_key)
    
    # Load papers
    print("=" * 70)
    print("  S2 - AI-ASSISTED SCREENING (BATCH MODE)")
    print("=" * 70)
    print(f"\nBatch API benefits:")
    print(f"  - 50% cost reduction")
    print(f"  - ~$0.78 estimated (vs ~$1.55 sync)")
    print(f"  - Results within 24h (usually faster)")
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
    
    print(f"\nTotal papers: {len(papers)}")
    print(f"Total requests: {len(papers) * NUM_RUNS} (3 runs per paper)")
    
    # Create all batch requests
    all_requests = []
    for run_num in range(1, NUM_RUNS + 1):
        requests = create_batch_requests(papers, run_num)
        all_requests.extend(requests)
    
    print(f"\nCreating batch files...")
    
    # Split into batches and submit
    batch_ids = []
    for i in range(0, len(all_requests), BATCH_SIZE * NUM_RUNS):
        batch_num = i // (BATCH_SIZE * NUM_RUNS) + 1
        batch_requests = all_requests[i:i + BATCH_SIZE * NUM_RUNS]
        
        batch_file = write_batch_file(batch_requests, batch_num)
        print(f"\nBatch {batch_num}: {len(batch_requests)} requests")
        print(f"  File: {batch_file}")
        
        batch = submit_batch(
            client, 
            batch_file, 
            f"S2 Screening Batch {batch_num} - {len(batch_requests)} requests"
        )
        batch_ids.append(batch.id)
        print(f"  Batch ID: {batch.id}")
    
    # Save batch IDs for recovery
    batch_info_file = BATCH_DIR / "batch_info.json"
    with open(batch_info_file, 'w') as f:
        json.dump({
            "submitted_at": datetime.now().isoformat(),
            "batch_ids": batch_ids,
            "total_papers": len(papers),
            "total_requests": len(all_requests)
        }, f, indent=2)
    
    print(f"\n{'=' * 70}")
    print(f"  BATCHES SUBMITTED")
    print(f"{'=' * 70}")
    print(f"\nBatch IDs saved to: {batch_info_file}")
    print(f"\nTo check status later, run:")
    print(f"  python check_batch_status.py")
    print(f"\nOr wait here for completion...")
    
    # Wait for all batches
    input("\nPress Enter to start monitoring batches (or Ctrl+C to exit)...")
    
    all_results = []
    for i, batch_id in enumerate(batch_ids):
        print(f"\nWaiting for batch {i+1}/{len(batch_ids)} ({batch_id})...")
        batch = wait_for_batch(client, batch_id)
        
        if batch.status == "completed":
            results = download_results(client, batch)
            all_results.extend(results)
            
            # Save intermediate results
            results_file = BATCH_DIR / f"batch_{i+1:03d}_results.jsonl"
            with open(results_file, 'w') as f:
                for r in results:
                    f.write(json.dumps(r) + '\n')
    
    # Process all results
    print(f"\nProcessing {len(all_results)} results...")
    decisions = parse_batch_results(all_results)
    
    # Create final output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    include_count = 0
    exclude_count = 0
    uncertain_count = 0
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'id', 'database', 'title', 'authors', 'year', 'doi', 'abstract_snippet',
            'screening_decision', 'avg_confidence',
            'run_1_decision', 'run_1_confidence',
            'run_2_decision', 'run_2_confidence', 
            'run_3_decision', 'run_3_confidence',
            'rationale', 'needs_manual_review'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for paper in papers:
            paper_id = paper.get('doi') or paper.get('id') or paper.get('title', '')[:50]
            runs = decisions.get(paper_id, {})
            
            final_decision, avg_conf, rationale = determine_final_decision(runs)
            
            if final_decision == 'INCLUDE':
                include_count += 1
            elif final_decision == 'EXCLUDE':
                exclude_count += 1
            else:
                uncertain_count += 1
            
            row = {
                'id': paper.get('id', ''),
                'database': paper.get('database', ''),
                'title': paper.get('title', ''),
                'authors': paper.get('authors', ''),
                'year': paper.get('year', ''),
                'doi': paper.get('doi', ''),
                'abstract_snippet': paper.get('abstract_snippet', ''),
                'screening_decision': final_decision,
                'avg_confidence': round(avg_conf, 1),
                'run_1_decision': runs.get('run_1', {}).get('decision', ''),
                'run_1_confidence': runs.get('run_1', {}).get('confidence', ''),
                'run_2_decision': runs.get('run_2', {}).get('decision', ''),
                'run_2_confidence': runs.get('run_2', {}).get('confidence', ''),
                'run_3_decision': runs.get('run_3', {}).get('decision', ''),
                'run_3_confidence': runs.get('run_3', {}).get('confidence', ''),
                'rationale': rationale,
                'needs_manual_review': final_decision == 'UNCERTAIN' or avg_conf < 70
            }
            writer.writerow(row)
    
    print(f"\n{'=' * 70}")
    print(f"  SCREENING COMPLETE")
    print(f"{'=' * 70}")
    print(f"\nResults:")
    print(f"  ✅ INCLUDE:   {include_count} ({100*include_count/len(papers):.1f}%)")
    print(f"  ❌ EXCLUDE:   {exclude_count} ({100*exclude_count/len(papers):.1f}%)")
    print(f"  ❓ UNCERTAIN: {uncertain_count} ({100*uncertain_count/len(papers):.1f}%)")
    print(f"\nOutput: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
