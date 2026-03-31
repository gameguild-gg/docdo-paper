#!/usr/bin/env python3
"""
Submit S3 Full-Text Screening as a GPT-5.2 Batch.
Processes all 63 PDFs for screening + data extraction.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from openai import OpenAI

# Load environment
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs): return False

REPO_ROOT = Path(__file__).parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

# Paths
PDF_DIR = REPO_ROOT / "data/pdfs"
OUTPUT_DIR = REPO_ROOT / "data/processed/s3_fulltext_screening/batch"

# S3 Criteria and Schema
S3_CRITERIA = """
## S3 Full-Text Screening Criteria

### INCLUDE if ALL of the following:
1. **Deep Learning Focus**: Uses deep learning (CNN, U-Net, Transformer, etc.) as PRIMARY method for segmentation
2. **3D/Volumetric**: Processes 3D CT volumes (not just 2D slices independently)
3. **Organ Segmentation**: Segments anatomical organs (liver, kidney, spleen, pancreas, etc.)
4. **CT Modality**: Uses CT scans (not MRI, ultrasound, or X-ray only)
5. **Evaluation**: Reports quantitative metrics (Dice, IoU, Hausdorff, etc.)
6. **Novel Contribution**: Presents new method, architecture, or significant improvement

### EXCLUDE if ANY of the following:
1. **Review/Survey**: Paper is a literature review without novel method
2. **Non-DL Primary**: Deep learning is not the primary segmentation method
3. **2D Only**: Only processes 2D slices without 3D context
4. **Non-CT**: Focuses on MRI, PET, ultrasound, or other modalities (CT must be primary)
5. **Tumor/Lesion Only**: Only segments tumors/lesions, not organs
6. **No Evaluation**: No quantitative evaluation metrics reported
7. **Application Only**: Only applies existing methods without methodological contribution
"""

DATA_EXTRACTION_SCHEMA = {
    "paper_id": "string - identifier from filename",
    "title": "string - paper title",
    "authors": "string - first author et al.",
    "year": "integer - publication year",
    "venue": "string - journal/conference name",
    "architecture": "string - main architecture (U-Net, V-Net, nnU-Net, Transformer, etc.)",
    "architecture_details": "string - specific variant or modifications",
    "is_3d": "boolean - true if 3D convolutions used",
    "loss_function": "string - loss function(s) used",
    "preprocessing": "string - preprocessing steps",
    "postprocessing": "string - postprocessing steps if any",
    "datasets": "list - dataset names used",
    "dataset_size": "string - number of CT scans/patients",
    "organs_segmented": "list - which organs (liver, kidney, spleen, pancreas, etc.)",
    "multi_organ": "boolean - segments multiple organs",
    "best_dice": "float - best reported Dice score (0-1 or %)",
    "dice_per_organ": "dict - Dice scores per organ if reported",
    "other_metrics": "dict - other metrics (IoU, Hausdorff, etc.)",
    "comparison_methods": "list - methods compared against",
    "framework": "string - PyTorch, TensorFlow, etc.",
    "gpu_used": "string - GPU model if mentioned",
    "training_time": "string - training time if mentioned",
    "inference_time": "string - inference time if mentioned",
    "code_available": "boolean - is code publicly available",
    "code_url": "string - URL to code if available",
    "limitations": "string - stated limitations",
    "future_work": "string - suggested future work"
}

def extract_pdf_text(pdf_path: Path, max_pages: int = 30, max_chars: int = 45000) -> str:
    """Extract text from PDF using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            text += page.get_text()
            if len(text) > max_chars:
                break
        doc.close()
        return text[:max_chars]
    except Exception as e:
        return f"ERROR extracting PDF: {e}"

def create_prompt(paper_id: str, pdf_text: str) -> str:
    """Create the screening prompt."""
    return f"""You are reviewing a scientific paper for a systematic review on "3D Organ Segmentation from CT Scans using Deep Learning".

{S3_CRITERIA}

## Your Task

1. **SCREEN**: Determine if this paper should be INCLUDED or EXCLUDED based on the criteria above.
2. **EXTRACT**: If INCLUDED, extract the data according to the schema below.

## Data Extraction Schema (extract if INCLUDED):
{json.dumps(DATA_EXTRACTION_SCHEMA, indent=2)}

## Paper ID: {paper_id}

## Paper Content:
{pdf_text}

## Response Format (JSON):
{{
    "paper_id": "{paper_id}",
    "screening_decision": "INCLUDE" or "EXCLUDE",
    "exclusion_reason": "reason if EXCLUDE, null if INCLUDE",
    "confidence": 0.0-1.0,
    "screening_notes": "brief justification",
    "extracted_data": {{ ... data if INCLUDE, null if EXCLUDE }}
}}

Respond ONLY with valid JSON."""

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get all PDFs
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDFs to process")
    
    # Create batch requests
    batch_requests = []
    
    for i, pdf_path in enumerate(pdf_files):
        paper_id = pdf_path.stem
        print(f"[{i+1}/{len(pdf_files)}] Extracting: {paper_id}")
        
        pdf_text = extract_pdf_text(pdf_path)
        
        if pdf_text.startswith("ERROR"):
            print(f"  ⚠️ {pdf_text}")
            continue
        
        prompt = create_prompt(paper_id, pdf_text)
        
        request = {
            "custom_id": f"s3_screen_{paper_id}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-5.2",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_completion_tokens": 4000,
                "response_format": {"type": "json_object"}
            }
        }
        batch_requests.append(request)
    
    print(f"\nCreated {len(batch_requests)} batch requests")
    
    # Save batch file
    batch_file = OUTPUT_DIR / f"s3_batch_requests_{timestamp}.jsonl"
    with open(batch_file, 'w', encoding='utf-8') as f:
        for req in batch_requests:
            f.write(json.dumps(req) + '\n')
    
    print(f"Saved: {batch_file}")
    
    # Estimate cost
    total_input_tokens = sum(len(create_prompt(pdf.stem, extract_pdf_text(pdf))[:45000]) // 4 
                            for pdf in pdf_files[:5]) * len(pdf_files) // 5
    total_output_tokens = len(batch_requests) * 1500
    
    input_cost = (total_input_tokens / 1_000_000) * 0.75
    output_cost = (total_output_tokens / 1_000_000) * 3.00
    
    print(f"\n--- Cost Estimate ---")
    print(f"Input tokens: ~{total_input_tokens:,}")
    print(f"Output tokens: ~{total_output_tokens:,}")
    print(f"Input cost: ${input_cost:.2f}")
    print(f"Output cost: ${output_cost:.2f}")
    print(f"Total estimate: ${input_cost + output_cost:.2f}")
    
    # Upload and submit batch
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    print(f"\nUploading batch file...")
    with open(batch_file, 'rb') as f:
        uploaded = client.files.create(file=f, purpose="batch")
    
    print(f"Uploaded: {uploaded.id}")
    
    print(f"Submitting batch...")
    batch = client.batches.create(
        input_file_id=uploaded.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": f"S3 Full-Text Screening - {len(batch_requests)} papers",
            "timestamp": timestamp
        }
    )
    
    print(f"\n{'='*60}")
    print(f"BATCH SUBMITTED SUCCESSFULLY")
    print(f"{'='*60}")
    print(f"Batch ID: {batch.id}")
    print(f"Status: {batch.status}")
    print(f"Papers: {len(batch_requests)}")
    print(f"Estimated cost: ${input_cost + output_cost:.2f}")
    print(f"\nCheck status with:")
    print(f"  python supplementary/scripts/check_batch_status.py {batch.id}")
    
    # Save batch info
    batch_info = {
        "batch_id": batch.id,
        "input_file_id": uploaded.id,
        "timestamp": timestamp,
        "num_papers": len(batch_requests),
        "status": batch.status,
        "estimated_cost": input_cost + output_cost
    }
    
    info_file = OUTPUT_DIR / f"batch_info_{timestamp}.json"
    with open(info_file, 'w') as f:
        json.dump(batch_info, f, indent=2)
    
    print(f"\nSaved batch info: {info_file}")
    
    return batch.id

if __name__ == "__main__":
    main()
