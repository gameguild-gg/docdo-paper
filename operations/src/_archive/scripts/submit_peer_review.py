#!/usr/bin/env python3
"""
Submit Peer Review Batch (Non-interactive)
==========================================
Submits the prepared peer review batch to OpenAI.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from openai import OpenAI

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs): return False

REPO_ROOT = Path(__file__).parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

OUTPUT_DIR = REPO_ROOT / "data/processed/peer_review"


def main():
    print("=" * 70)
    print("Submit Peer Review Batch")
    print("=" * 70)
    
    # Find the most recent batch file
    batch_files = list(OUTPUT_DIR.glob("peer_review_batch_*.jsonl"))
    
    if not batch_files:
        print("❌ No batch file found. Run peer_review_batch.py first.")
        return None
    
    # Use most recent
    batch_file = max(batch_files, key=lambda p: p.stat().st_mtime)
    
    # Count requests
    with open(batch_file, 'r') as f:
        num_requests = sum(1 for line in f if line.strip())
    
    print(f"\nBatch file: {batch_file.name}")
    print(f"Requests: {num_requests}")
    
    # Submit to OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    print(f"\nUploading batch file...")
    with open(batch_file, 'rb') as f:
        uploaded = client.files.create(file=f, purpose="batch")
    print(f"File uploaded: {uploaded.id}")
    
    print(f"\nSubmitting batch...")
    batch = client.batches.create(
        input_file_id=uploaded.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": f"Peer Review - {num_requests} papers reviewing our systematic review",
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
        }
    )
    
    print(f"\n{'='*70}")
    print(f"BATCH SUBMITTED")
    print(f"{'='*70}")
    print(f"Batch ID:     {batch.id}")
    print(f"Status:       {batch.status}")
    print(f"Reviewers:    {num_requests}")
    print(f"Estimated completion: 12-24 hours")
    
    # Save batch info
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_info = {
        "batch_id": batch.id,
        "timestamp": timestamp,
        "num_reviewers": num_requests,
        "status": batch.status,
        "batch_file": str(batch_file)
    }
    
    info_file = OUTPUT_DIR / f"submitted_batch_info_{timestamp}.json"
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(batch_info, f, indent=2)
    
    # Create/update status check script
    check_script_content = f'''#!/usr/bin/env python3
"""Check status and download results for peer review batch."""
import os
from openai import OpenAI
from pathlib import Path
import json
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

BATCH_ID = "{batch.id}"
OUTPUT_DIR = Path(r"{OUTPUT_DIR}")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
batch = client.batches.retrieve(BATCH_ID)

print("=" * 60)
print("PEER REVIEW BATCH STATUS")
print("=" * 60)
print(f"Batch ID: {{batch.id}}")
print(f"Status: {{batch.status}}")
print(f"Created: {{batch.created_at}}")
print(f"Completed: {{batch.request_counts.completed}}/{{batch.request_counts.total}}")
print(f"Failed: {{batch.request_counts.failed}}")

if batch.status == "completed":
    print("\\n[OK] Batch completed! Downloading results...")
    content = client.files.content(batch.output_file_id)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"peer_reviews_results_{{timestamp}}.jsonl"
    output_file.write_bytes(content.content)
    print(f"Results saved to: {{output_file}}")
    print("\\nNext: Run compile_peer_reviews.py to generate the report")
    
elif batch.status == "failed":
    print("\\n[FAILED] Batch failed!")
    if batch.errors:
        print(f"Errors: {{batch.errors}}")
        
elif batch.status == "in_progress":
    progress = batch.request_counts.completed / batch.request_counts.total * 100
    print(f"\\n[PROGRESS] {{progress:.1f}}%")
    print("Run this script again later to check status.")
    
else:
    print(f"\\n[STATUS] Current status: {{batch.status}}")
    print("Run this script again later to check status.")
'''
    
    check_file = OUTPUT_DIR / "check_peer_review_status.py"
    with open(check_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(check_script_content)
    
    print(f"\nTo check status, run:")
    print(f"   python {check_file.relative_to(REPO_ROOT)}")
    print(f"\nAfter completion, compile report with:")
    print(f"   python supplementary/scripts/compile_peer_reviews.py")
    
    return batch.id


if __name__ == "__main__":
    main()
