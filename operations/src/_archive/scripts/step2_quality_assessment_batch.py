#!/usr/bin/env python3
"""
Steps 2-5: Read papers, Quality Assessment, Synthesis, and Write.
Submits a batch to GPT-5.2 to analyze all 52 papers comprehensively.
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
PDF_DIR = REPO_ROOT / "data/final_included_papers"
EXTRACTED_DATA = REPO_ROOT / "data/processed/s3_fulltext_screening/batch/s3_parsed_results.json"
OUTPUT_DIR = REPO_ROOT / "data/processed/quality_assessment"

# Quality Assessment Criteria (adapted from common systematic review tools)
QUALITY_CRITERIA = """
## Quality Assessment Criteria for Deep Learning Medical Image Segmentation Studies

Assess each paper on these criteria (score 0-2 for each: 0=No/Poor, 1=Partial, 2=Yes/Good):

### 1. Dataset Quality (max 10 points)
- Q1: Dataset size adequate (>50 subjects for training)? [0-2]
- Q2: Dataset source clearly described? [0-2]
- Q3: Train/validation/test split methodology clear? [0-2]
- Q4: Ground truth annotation process described? [0-2]
- Q5: External validation on independent dataset? [0-2]

### 2. Methodology Quality (max 10 points)
- Q6: Network architecture fully described? [0-2]
- Q7: Training process reproducible (hyperparameters, optimizer, etc.)? [0-2]
- Q8: Loss function choice justified? [0-2]
- Q9: Pre/post-processing steps clearly described? [0-2]
- Q10: Code/model publicly available? [0-2]

### 3. Evaluation Quality (max 10 points)
- Q11: Multiple evaluation metrics used (Dice + at least one other)? [0-2]
- Q12: Statistical analysis performed (confidence intervals, p-values)? [0-2]
- Q13: Comparison with state-of-the-art methods? [0-2]
- Q14: Per-organ results reported (not just average)? [0-2]
- Q15: Failure cases / limitations discussed? [0-2]

### Risk of Bias Assessment
- Selection bias: Was patient selection clearly defined?
- Performance bias: Were outcomes assessed consistently?
- Reporting bias: Were all relevant outcomes reported?

Total score: /30 (High quality: ≥24, Medium: 15-23, Low: <15)
"""

def extract_pdf_text(pdf_path: Path, max_chars: int = 60000) -> str:
    """Extract text from PDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
            if len(text) > max_chars:
                break
        doc.close()
        return text[:max_chars]
    except Exception as e:
        return f"ERROR: {e}"

def create_analysis_prompt(paper_id: str, pdf_text: str, extracted_data: dict) -> str:
    """Create comprehensive analysis prompt."""
    return f"""You are conducting a systematic review on "3D Organ Segmentation from CT Scans using Deep Learning".

Analyze this paper comprehensively for:
1. Quality Assessment
2. Detailed Data Extraction
3. Key Contributions Summary

{QUALITY_CRITERIA}

## Previously Extracted Data:
{json.dumps(extracted_data, indent=2)}

## Paper ID: {paper_id}

## Full Paper Text:
{pdf_text}

## Required Output (JSON):
{{
    "paper_id": "{paper_id}",
    
    "quality_assessment": {{
        "dataset_quality": {{
            "Q1_dataset_size": {{"score": 0-2, "justification": "..."}},
            "Q2_dataset_source": {{"score": 0-2, "justification": "..."}},
            "Q3_train_test_split": {{"score": 0-2, "justification": "..."}},
            "Q4_ground_truth": {{"score": 0-2, "justification": "..."}},
            "Q5_external_validation": {{"score": 0-2, "justification": "..."}}
        }},
        "methodology_quality": {{
            "Q6_architecture_description": {{"score": 0-2, "justification": "..."}},
            "Q7_reproducibility": {{"score": 0-2, "justification": "..."}},
            "Q8_loss_function": {{"score": 0-2, "justification": "..."}},
            "Q9_preprocessing": {{"score": 0-2, "justification": "..."}},
            "Q10_code_availability": {{"score": 0-2, "justification": "..."}}
        }},
        "evaluation_quality": {{
            "Q11_multiple_metrics": {{"score": 0-2, "justification": "..."}},
            "Q12_statistical_analysis": {{"score": 0-2, "justification": "..."}},
            "Q13_comparison_sota": {{"score": 0-2, "justification": "..."}},
            "Q14_per_organ_results": {{"score": 0-2, "justification": "..."}},
            "Q15_limitations": {{"score": 0-2, "justification": "..."}}
        }},
        "total_score": 0-30,
        "quality_rating": "High/Medium/Low",
        "risk_of_bias": {{
            "selection_bias": "Low/Medium/High - explanation",
            "performance_bias": "Low/Medium/High - explanation", 
            "reporting_bias": "Low/Medium/High - explanation"
        }}
    }},
    
    "detailed_extraction": {{
        "title": "Full paper title",
        "authors": "First Author et al.",
        "year": 2020,
        "venue": "Journal/Conference name",
        "doi": "DOI if available",
        
        "method": {{
            "architecture_name": "e.g., 3D U-Net, V-Net, nnU-Net",
            "architecture_type": "CNN/Transformer/Hybrid",
            "key_innovations": ["list of novel contributions"],
            "3d_processing": true/false,
            "attention_mechanism": true/false,
            "multi_scale": true/false,
            "cascade_stages": 1,
            "loss_functions": ["list of losses"],
            "optimizer": "Adam/SGD/etc",
            "learning_rate": "value or schedule",
            "batch_size": "value",
            "epochs": "value",
            "augmentation": ["list of augmentations"]
        }},
        
        "dataset": {{
            "names": ["dataset names"],
            "total_subjects": "number",
            "train_subjects": "number",
            "val_subjects": "number", 
            "test_subjects": "number",
            "ct_scanner": "manufacturer/model if mentioned",
            "slice_thickness": "value if mentioned",
            "image_size": "dimensions"
        }},
        
        "organs": {{
            "segmented_organs": ["complete list"],
            "num_organs": "number",
            "multi_organ": true/false,
            "challenging_organs": ["organs mentioned as difficult"]
        }},
        
        "results": {{
            "primary_metric": "Dice/IoU/etc",
            "overall_dice": "value (0-1 or %)",
            "dice_per_organ": {{"organ": "dice_value"}},
            "hausdorff_distance": {{"organ": "hd_value"}},
            "inference_time": "value",
            "gpu_memory": "value if mentioned",
            "comparison_results": {{"method": "dice_value"}}
        }},
        
        "implementation": {{
            "framework": "PyTorch/TensorFlow/etc",
            "gpu": "GPU model",
            "training_time": "value",
            "code_url": "URL or null"
        }}
    }},
    
    "contribution_summary": {{
        "main_contribution": "One sentence summary of key contribution",
        "novelty": "What is novel compared to prior work",
        "strengths": ["list of strengths"],
        "weaknesses": ["list of weaknesses"],
        "clinical_applicability": "Assessment of clinical relevance"
    }}
}}

Respond ONLY with valid JSON."""

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load previously extracted data
    with open(EXTRACTED_DATA) as f:
        all_results = json.load(f)
    
    # Filter to included papers
    included = {r['paper_id']: r.get('extracted_data', {}) for r in all_results 
                if r.get('screening_decision') == 'INCLUDE'}
    
    print(f"Found {len(included)} included papers")
    
    # Get PDFs
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDFs")
    
    # Create batch requests
    batch_requests = []
    
    for pdf_path in pdf_files:
        paper_id = pdf_path.stem
        
        if paper_id not in included:
            continue
        
        print(f"Processing: {paper_id}")
        
        pdf_text = extract_pdf_text(pdf_path)
        if pdf_text.startswith("ERROR"):
            print(f"  ⚠️ {pdf_text}")
            continue
        
        extracted_data = included.get(paper_id, {})
        prompt = create_analysis_prompt(paper_id, pdf_text, extracted_data)
        
        request = {
            "custom_id": f"qa_{paper_id}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-5.2",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_completion_tokens": 6000,
                "response_format": {"type": "json_object"}
            }
        }
        batch_requests.append(request)
    
    print(f"\nCreated {len(batch_requests)} batch requests")
    
    # Save batch file
    batch_file = OUTPUT_DIR / f"qa_batch_requests_{timestamp}.jsonl"
    with open(batch_file, 'w', encoding='utf-8') as f:
        for req in batch_requests:
            f.write(json.dumps(req) + '\n')
    
    print(f"Saved: {batch_file}")
    
    # Estimate cost
    est_input = len(batch_requests) * 15000  # ~15k tokens per paper
    est_output = len(batch_requests) * 2000   # ~2k tokens output
    input_cost = (est_input / 1_000_000) * 0.75
    output_cost = (est_output / 1_000_000) * 3.00
    
    print(f"\n--- Cost Estimate ---")
    print(f"Input tokens: ~{est_input:,}")
    print(f"Output tokens: ~{est_output:,}")
    print(f"Estimated cost: ${input_cost + output_cost:.2f}")
    
    # Upload and submit
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
        metadata={"description": f"Quality Assessment + Analysis - {len(batch_requests)} papers"}
    )
    
    print(f"\n{'='*60}")
    print(f"BATCH SUBMITTED")
    print(f"{'='*60}")
    print(f"Batch ID: {batch.id}")
    print(f"Status: {batch.status}")
    print(f"Papers: {len(batch_requests)}")
    
    # Save batch info
    batch_info = {
        "batch_id": batch.id,
        "timestamp": timestamp,
        "num_papers": len(batch_requests),
        "status": batch.status
    }
    
    info_file = OUTPUT_DIR / f"batch_info_{timestamp}.json"
    with open(info_file, 'w') as f:
        json.dump(batch_info, f, indent=2)
    
    # Update check script
    check_script = REPO_ROOT / "supplementary/scripts/check_s3_batch.py"
    check_content = check_script.read_text()
    check_content = check_content.replace(
        'BATCH_ID = "batch_6972db9744cc819083344e8c564d96b9"',
        f'BATCH_ID = "{batch.id}"'
    )
    check_script.write_text(check_content)
    
    print(f"\nCheck status: python supplementary/scripts/check_s3_batch.py")
    
    return batch.id

if __name__ == "__main__":
    main()
