#!/usr/bin/env python3
"""
Monitor batch status and resubmit failed batches when capacity is available.
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

BATCH_DIR = Path(__file__).parent.parent.parent / "data" / "processed" / "batches"
INPUT_FILE = Path(__file__).parent.parent.parent / "data" / "interim" / "S1_search_results_deduplicated.csv"
OUTPUT_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_screened.csv"

# All submitted batch IDs
BATCH_IDS = [
    'batch_6970ead762008190a8507b50ce284070',  # Batch 1: papers 1-500
    'batch_6970eade59348190aaa699dc53bc0a76',  # Batch 2: papers 501-1000 (FAILED - resubmit)
    'batch_6970eb31099c8190b1add0e6d9bf9d84',  # Batch 3: papers 1001-1500
    'batch_6970eb35d3c88190986f71101aa4a7cb',  # Batch 4: papers 1501-2000 (FAILED - resubmit)
    'batch_6970eb3b52d48190af67119ef332b414',  # Batch 5: papers 2001-2500 (FAILED - resubmit)
    'batch_6970eb3e8f808190a74ba756bd43da44',  # Batch 6: papers 2501-2821 (FAILED - resubmit)
]


def check_status(client):
    """Check status of all batches."""
    print("\n" + "=" * 70)
    print(f"  BATCH STATUS - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 70)
    
    total_completed = 0
    total_requests = 0
    in_progress = 0
    completed_batches = []
    failed_batches = []
    
    for i, bid in enumerate(BATCH_IDS, 1):
        try:
            b = client.batches.retrieve(bid)
            status = b.status
            completed = b.request_counts.completed
            total = b.request_counts.total
            
            if status == "completed":
                completed_batches.append(bid)
                total_completed += completed
                total_requests += total
                print(f"  Batch {i}: ✅ COMPLETED  {completed}/{total}")
            elif status == "in_progress":
                in_progress += 1
                total_completed += completed
                total_requests += total
                print(f"  Batch {i}: 🔄 {status:12} {completed}/{total}")
            elif status == "failed":
                failed_batches.append((i, bid))
                print(f"  Batch {i}: ❌ FAILED")
            else:
                print(f"  Batch {i}: ⏳ {status:12}")
                
        except Exception as e:
            print(f"  Batch {i}: ⚠️  Error: {str(e)[:50]}")
    
    print("=" * 70)
    if total_requests > 0:
        print(f"  Progress: {total_completed}/{total_requests} ({100*total_completed/total_requests:.1f}%)")
    print(f"  In Progress: {in_progress} | Completed: {len(completed_batches)} | Failed: {len(failed_batches)}")
    
    return completed_batches, failed_batches, in_progress


def download_results(client, batch_id, batch_num):
    """Download results from completed batch."""
    batch = client.batches.retrieve(batch_id)
    
    if not batch.output_file_id:
        print(f"  No output file for batch {batch_num}")
        return []
    
    content = client.files.content(batch.output_file_id)
    results = []
    
    for line in content.text.strip().split('\n'):
        if line:
            results.append(json.loads(line))
    
    # Save to file
    output_file = BATCH_DIR / f"batch_{batch_num:03d}_results.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r) + '\n')
    
    print(f"  Downloaded {len(results)} results to {output_file.name}")
    return results


def main():
    client = OpenAI()
    
    print("\n" + "=" * 70)
    print("  S2 SCREENING - BATCH MONITOR")
    print("=" * 70)
    print(f"\nMonitoring {len(BATCH_IDS)} batches...")
    print("Press Ctrl+C to exit\n")
    
    downloaded = set()
    
    while True:
        completed, failed, in_progress = check_status(client)
        
        # Download newly completed batches
        for bid in completed:
            if bid not in downloaded:
                batch_num = BATCH_IDS.index(bid) + 1
                print(f"\n  Downloading batch {batch_num}...")
                download_results(client, bid, batch_num)
                downloaded.add(bid)
        
        # Check if all done
        if len(completed) + len(failed) == len(BATCH_IDS):
            if failed:
                print(f"\n⚠️  {len(failed)} batches failed. Need to resubmit when capacity available.")
            else:
                print("\n✅ ALL BATCHES COMPLETED!")
            break
        
        print(f"\n  Next check in 30 seconds...")
        time.sleep(30)
    
    print("\nDone monitoring.")


if __name__ == "__main__":
    main()
