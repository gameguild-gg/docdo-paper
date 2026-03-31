#!/usr/bin/env python3
"""Download S3 batch results."""
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / ".env")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

BATCH_ID = "batch_6972db9744cc819083344e8c564d96b9"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "data/processed/s3_fulltext_screening/batch"

# Get batch info
batch = client.batches.retrieve(BATCH_ID)
print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")
print(f"Total: {batch.request_counts.total}")
print(f"Completed: {batch.request_counts.completed}")
print(f"Failed: {batch.request_counts.failed}")

if batch.status == "completed" and batch.output_file_id:
    print(f"\nDownloading results...")
    
    # Download output file
    content = client.files.content(batch.output_file_id)
    
    output_file = OUTPUT_DIR / "s3_batch_results.jsonl"
    output_file.write_bytes(content.content)
    print(f"Saved: {output_file}")
    
    # Parse results
    results = []
    with open(output_file) as f:
        for line in f:
            results.append(json.loads(line))
    
    print(f"\nParsed {len(results)} results")
    
    # Count decisions
    included = 0
    excluded = 0
    errors = 0
    
    parsed_results = []
    for r in results:
        try:
            response = json.loads(r['response']['body']['choices'][0]['message']['content'])
            parsed_results.append(response)
            if response.get('screening_decision') == 'INCLUDE':
                included += 1
            elif response.get('screening_decision') == 'EXCLUDE':
                excluded += 1
        except:
            errors += 1
    
    print(f"\nINCLUDED: {included}")
    print(f"EXCLUDED: {excluded}")
    print(f"ERRORS: {errors}")
    
    # Save parsed results
    parsed_file = OUTPUT_DIR / "s3_parsed_results.json"
    with open(parsed_file, 'w') as f:
        json.dump(parsed_results, f, indent=2)
    print(f"\nSaved parsed: {parsed_file}")
    
elif batch.status == "failed":
    print(f"\nBatch failed!")
    if batch.errors:
        print(f"Errors: {batch.errors}")
else:
    print(f"\nBatch not yet completed. Status: {batch.status}")
