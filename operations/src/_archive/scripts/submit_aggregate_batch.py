#!/usr/bin/env python3
"""Submit the aggregate reviews batch to OpenAI Batch API."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PEER_REVIEW_DIR = REPO_ROOT / "data" / "processed" / "peer_review"


def find_latest(pattern: str) -> Path:
    candidates = sorted(PEER_REVIEW_DIR.glob(pattern), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise FileNotFoundError(f"No files matching {pattern} in {PEER_REVIEW_DIR}")
    return candidates[-1]


def main() -> int:
    batch_file = find_latest("aggregate_batch_*.jsonl")
    print(f"Submitting batch file: {batch_file.name}")
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Upload
    print("Uploading batch file...")
    with open(batch_file, "rb") as f:
        uploaded = client.files.create(file=f, purpose="batch")
    print(f"Uploaded: {uploaded.id}")
    
    # Submit batch
    print("Submitting batch...")
    batch = client.batches.create(
        input_file_id=uploaded.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": "Aggregate 52 peer reviews into TODO.md (3 runs)"},
    )
    
    print(f"\nBatch submitted!")
    print(f"  Batch ID: {batch.id}")
    print(f"  Status: {batch.status}")
    
    # Save batch info
    info = {
        "batch_id": batch.id,
        "input_file_id": uploaded.id,
        "batch_file": batch_file.name,
        "submitted_at": datetime.now().isoformat(),
        "status": batch.status,
    }
    
    info_file = PEER_REVIEW_DIR / f"aggregate_batch_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    info_file.write_text(json.dumps(info, indent=2), encoding="utf-8")
    print(f"  Info saved: {info_file.name}")
    
    # Write status checker
    check_script = PEER_REVIEW_DIR / "check_aggregate_status.py"
    check_content = f'''#!/usr/bin/env python3
"""Check status and download results for aggregate batch."""
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
OUTPUT_DIR = Path(r"{PEER_REVIEW_DIR}")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
batch = client.batches.retrieve(BATCH_ID)

print("=" * 60)
print("AGGREGATE BATCH STATUS")
print("=" * 60)
print(f"Batch ID: {{batch.id}}")
print(f"Status: {{batch.status}}")
print(f"Completed: {{batch.request_counts.completed}}/{{batch.request_counts.total}}")
print(f"Failed: {{batch.request_counts.failed}}")

if batch.status == "completed":
    print("\\n[OK] Batch completed! Downloading results...")
    content = client.files.content(batch.output_file_id)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"aggregate_results_{{timestamp}}.jsonl"
    output_file.write_bytes(content.content)
    print(f"[SAVED] Results saved to: {{output_file}}")
    print("\\nNext: Run reconcile_aggregate_reviews.py to produce final TODO.md")
    
elif batch.status == "failed":
    print("\\n[FAILED] Batch failed!")
    if batch.errors:
        print(f"Errors: {{batch.errors}}")
        
elif batch.status == "in_progress":
    progress = batch.request_counts.completed / batch.request_counts.total * 100 if batch.request_counts.total > 0 else 0
    print(f"\\n[PROGRESS] {{progress:.1f}}%")
    print("Run this script again later to check status.")
    
else:
    print(f"\\n[STATUS] Current status: {{batch.status}}")
    print("Run this script again later to check status.")
'''
    check_script.write_text(check_content, encoding="utf-8")
    print(f"  Status checker: {check_script.name}")
    
    print(f"\nTo check status later:")
    print(f"  python {check_script}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
