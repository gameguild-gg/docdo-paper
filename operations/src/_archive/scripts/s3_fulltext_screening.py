#!/usr/bin/env python3
"""
S3 Full-Text Screening and Data Extraction using GPT-4o.
Reads PDFs, extracts text, and applies inclusion/exclusion criteria + data extraction.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from openai import OpenAI
import time
import os

# Load .env
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs): return False

REPO_ROOT = Path(__file__).parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

# Paths
PDF_DIR = Path("data/pdfs")
INCLUDED_FILE = Path("data/processed/final_results/final_included_for_review_20260122_215847.csv")
OUTPUT_DIR = Path("data/processed/s3_fulltext_screening")

# S3 Inclusion/Exclusion Criteria (full-text level)
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

# Data Extraction Schema
DATA_EXTRACTION_SCHEMA = {
    "paper_id": "string - identifier from filename",
    "title": "string - paper title",
    "authors": "string - first author et al.",
    "year": "integer - publication year",
    "venue": "string - journal/conference name",
    
    # Method
    "architecture": "string - main architecture (U-Net, V-Net, nnU-Net, Transformer, etc.)",
    "architecture_details": "string - specific variant or modifications",
    "is_3d": "boolean - true if 3D convolutions used",
    "loss_function": "string - loss function(s) used",
    "preprocessing": "string - preprocessing steps",
    "postprocessing": "string - postprocessing steps if any",
    
    # Dataset
    "datasets": "list - dataset names used",
    "dataset_size": "string - number of CT scans/patients",
    "organs_segmented": "list - which organs (liver, kidney, spleen, pancreas, etc.)",
    "multi_organ": "boolean - segments multiple organs",
    
    # Results
    "best_dice": "float - best reported Dice score (0-1 or %)",
    "dice_per_organ": "dict - Dice scores per organ if reported",
    "other_metrics": "dict - other metrics (IoU, Hausdorff, etc.)",
    "comparison_methods": "list - methods compared against",
    
    # Technical
    "framework": "string - PyTorch, TensorFlow, etc.",
    "gpu_used": "string - GPU model if mentioned",
    "training_time": "string - training time if mentioned",
    "inference_time": "string - inference time if mentioned",
    "code_available": "boolean - is code publicly available",
    "code_url": "string - URL to code if available",
    
    # Limitations
    "limitations": "string - stated limitations",
    "future_work": "string - suggested future work"
}

def extract_pdf_text(pdf_path: Path, max_pages: int = 30) -> str:
    """Extract text from PDF using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            text += page.get_text()
        doc.close()
        return text[:50000]  # Limit to ~50k chars
    except Exception as e:
        return f"ERROR extracting PDF: {e}"

def screen_and_extract(client: OpenAI, paper_id: str, pdf_text: str) -> dict:
    """Use GPT-4o to screen paper and extract data."""
    
    prompt = f"""You are reviewing a scientific paper for a systematic review on "3D Organ Segmentation from CT Scans using Deep Learning".

{S3_CRITERIA}

## Your Task

1. **SCREEN**: Determine if this paper should be INCLUDED or EXCLUDED based on the criteria above.
2. **EXTRACT**: If INCLUDED, extract the data according to the schema below.

## Data Extraction Schema (extract if INCLUDED):
{json.dumps(DATA_EXTRACTION_SCHEMA, indent=2)}

## Paper Content:
{pdf_text}

## Response Format (JSON):
{{
    "screening_decision": "INCLUDE" or "EXCLUDE",
    "exclusion_reason": "reason if EXCLUDE, null if INCLUDE",
    "confidence": 0.0-1.0,
    "screening_notes": "brief justification",
    "extracted_data": {{ ... data if INCLUDE, null if EXCLUDE }}
}}

Respond ONLY with valid JSON.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=4000,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        result['paper_id'] = paper_id
        return result
        
    except Exception as e:
        return {
            "paper_id": paper_id,
            "screening_decision": "ERROR",
            "error": str(e)
        }

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load papers to screen
    df = pd.read_csv(INCLUDED_FILE)
    print(f"Papers to screen: {len(df)}")
    
    # Get PDF files
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    print(f"PDF files available: {len(pdf_files)}")
    
    # Initialize OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Check for existing progress
    progress_file = OUTPUT_DIR / "screening_progress.json"
    if progress_file.exists():
        with open(progress_file) as f:
            results = json.load(f)
        processed_ids = {r['paper_id'] for r in results}
        print(f"Resuming from {len(results)} completed")
    else:
        results = []
        processed_ids = set()
    
    # Process each PDF
    for i, pdf_path in enumerate(pdf_files):
        paper_id = pdf_path.stem
        
        if paper_id in processed_ids:
            continue
        
        print(f"\n[{i+1}/{len(pdf_files)}] Processing: {paper_id}")
        
        # Extract text
        pdf_text = extract_pdf_text(pdf_path)
        if pdf_text.startswith("ERROR"):
            print(f"  ⚠️ {pdf_text}")
            results.append({
                "paper_id": paper_id,
                "screening_decision": "ERROR",
                "error": pdf_text
            })
            continue
        
        print(f"  Extracted {len(pdf_text)} chars")
        
        # Screen and extract
        result = screen_and_extract(client, paper_id, pdf_text)
        results.append(result)
        
        decision = result.get('screening_decision', 'ERROR')
        print(f"  Decision: {decision}")
        
        # Save progress after each paper
        with open(progress_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Rate limiting
        time.sleep(3)  # Increased delay to avoid rate limiting
    
    # Final summary
    print("\n" + "="*60)
    print("SCREENING COMPLETE")
    print("="*60)
    
    included = [r for r in results if r.get('screening_decision') == 'INCLUDE']
    excluded = [r for r in results if r.get('screening_decision') == 'EXCLUDE']
    errors = [r for r in results if r.get('screening_decision') == 'ERROR']
    
    print(f"INCLUDED: {len(included)}")
    print(f"EXCLUDED: {len(excluded)}")
    print(f"ERRORS: {len(errors)}")
    
    # Save final results
    final_file = OUTPUT_DIR / f"s3_screening_results_{timestamp}.json"
    with open(final_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {final_file}")
    
    # Extract included data to CSV
    if included:
        extracted_data = []
        for r in included:
            data = r.get('extracted_data', {}) or {}
            data['paper_id'] = r['paper_id']
            data['confidence'] = r.get('confidence')
            extracted_data.append(data)
        
        df_extracted = pd.DataFrame(extracted_data)
        extracted_file = OUTPUT_DIR / f"extracted_data_{timestamp}.csv"
        df_extracted.to_csv(extracted_file, index=False)
        print(f"Saved: {extracted_file}")
    
    # Exclusion reasons summary
    if excluded:
        reasons = {}
        for r in excluded:
            reason = r.get('exclusion_reason', 'Unknown')
            reasons[reason] = reasons.get(reason, 0) + 1
        
        print("\nExclusion reasons:")
        for reason, count in sorted(reasons.items(), key=lambda x: -x[1]):
            print(f"  - {reason}: {count}")

if __name__ == "__main__":
    main()
