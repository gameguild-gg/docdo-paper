#!/usr/bin/env python3
"""Check single batch status."""
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / ".env")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

BATCH_ID = "batch_6972e053c6108190ac38ab54bd2987ec"

batch = client.batches.retrieve(BATCH_ID)
print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")
print(f"Total: {batch.request_counts.total}")
print(f"Completed: {batch.request_counts.completed}")
print(f"Failed: {batch.request_counts.failed}")

if batch.status == "completed":
    print(f"\nOutput file: {batch.output_file_id}")
