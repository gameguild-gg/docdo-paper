#!/usr/bin/env python3
"""
Peer Review Batch: Critical Analysis of Our Systematic Review Paper
====================================================================
This script creates a batch job where each of the 52 reviewed papers serves as 
a "reviewer perspective" to critically analyze our systematic review.

Each request sends:
1. Our systematic review paper (main.pdf)
2. One of the 52 reviewed papers
3. A prompt asking for critical academic review from that paper's perspective

Output: 52 critical reviews, one from each paper's perspective.
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
OUR_PAPER_PDF = REPO_ROOT / "main.pdf"
REVIEWED_PAPERS_DIR = REPO_ROOT / "data/final_included_papers"
OUTPUT_DIR = REPO_ROOT / "data/processed/peer_review"

# Extraction limits (reduce prompt size to avoid org-level enqueued token limits)
OUR_PAPER_MAX_CHARS = 60000
REVIEWER_PAPER_MAX_CHARS = 40000

# Model
MODEL_NAME = "gpt-5.2"

# Critical Review Prompt Template
REVIEW_PROMPT_TEMPLATE = """You are an expert academic reviewer in the field of medical image segmentation using deep learning. You have just finished reading the research paper titled "{reviewer_paper_title}" (provided below as REVIEWER_PAPER).

Now, you must CRITICALLY REVIEW and JUDGE the SYSTEMATIC REVIEW paper titled "A Systematic Review of 3D Organ Segmentation from CT Scans Using Deep Learning" (provided below as TARGET_PAPER).

Your review must be from the perspective of someone who has expertise in the methods, datasets, and findings described in your paper (REVIEWER_PAPER). Use your deep knowledge to critically evaluate the systematic review.

================================================================================
REVIEWER_PAPER (Your Research Paper - Use this as your basis for critique):
================================================================================
{reviewer_paper_text}

================================================================================
TARGET_PAPER (Systematic Review to Critique):
================================================================================
{our_paper_text}

================================================================================
CRITICAL REVIEW INSTRUCTIONS:
================================================================================

Provide a comprehensive critical academic review addressing the following aspects:

## 1. ACCURACY OF REPRESENTATION
- Does the systematic review accurately represent your paper's contributions?
- Are there any mischaracterizations or inaccuracies about your methods?
- Is your paper properly cited and contextualized?

## 2. TECHNICAL CRITIQUE
- Are there technical errors or oversimplifications in the review?
- Does the review demonstrate adequate understanding of the methods?
- Are the comparisons between methods fair and accurate?

## 3. COVERAGE COMPLETENESS
- Are important aspects of your research missing from the review?
- Are key limitations or challenges from your domain addressed?
- Is the taxonomy/categorization appropriate?

## 4. METHODOLOGICAL RIGOR
- Is the systematic review methodology sound?
- Are the inclusion/exclusion criteria appropriate?
- Is the quality assessment framework adequate?

## 5. SYNTHESIS QUALITY
- Are the synthesized conclusions well-supported?
- Are there any unsupported generalizations?
- Is the statistical aggregation appropriate?

## 6. STRENGTHS OF THE REVIEW
- What does this systematic review do well?
- What unique contributions does it make?

## 7. WEAKNESSES AND GAPS
- What are the major weaknesses?
- What important topics are missing?
- What would improve the review?

## 8. FACTUAL ERRORS
- List any specific factual errors you identify
- Note any incorrect citations or attributions

## 9. RECOMMENDATIONS
- Specific suggestions for improvement
- Priority rankings (Critical/Major/Minor)

## 10. OVERALL JUDGMENT
- Overall assessment: Accept / Minor Revision / Major Revision / Reject
- Confidence in assessment: High / Medium / Low
- Summary statement (2-3 sentences)

================================================================================
OUTPUT FORMAT (JSON):
================================================================================
{{
    "reviewer_paper_id": "{paper_id}",
    "reviewer_paper_title": "{reviewer_paper_title}",
    
    "accuracy_of_representation": {{
        "is_paper_accurately_represented": true/false,
        "mischaracterizations": ["list any misrepresentations"],
        "properly_cited": true/false,
        "details": "explanation"
    }},
    
    "technical_critique": {{
        "technical_errors": ["list of errors found"],
        "oversimplifications": ["list of oversimplifications"],
        "understanding_adequate": true/false,
        "comparison_fairness": "fair/partial/unfair",
        "details": "explanation"
    }},
    
    "coverage_completeness": {{
        "missing_aspects": ["important aspects from your paper not covered"],
        "domain_challenges_addressed": true/false,
        "taxonomy_appropriate": true/false,
        "details": "explanation"
    }},
    
    "methodological_rigor": {{
        "methodology_sound": true/false,
        "criteria_appropriate": true/false,
        "quality_assessment_adequate": true/false,
        "concerns": ["list of methodological concerns"]
    }},
    
    "synthesis_quality": {{
        "conclusions_supported": true/false,
        "unsupported_generalizations": ["list any"],
        "statistics_appropriate": true/false,
        "details": "explanation"
    }},
    
    "strengths": [
        "strength 1",
        "strength 2"
    ],
    
    "weaknesses": [
        {{"issue": "description", "severity": "Critical/Major/Minor"}},
        {{"issue": "description", "severity": "Critical/Major/Minor"}}
    ],
    
    "factual_errors": [
        {{"error": "description", "location": "where in the paper", "correction": "what should it say"}}
    ],
    
    "recommendations": [
        {{"recommendation": "description", "priority": "Critical/Major/Minor"}}
    ],
    
    "overall_judgment": {{
        "decision": "Accept/Minor Revision/Major Revision/Reject",
        "confidence": "High/Medium/Low",
        "summary": "2-3 sentence overall assessment"
    }},
    
    "scores": {{
        "technical_soundness": 1-5,
        "completeness": 1-5,
        "clarity": 1-5,
        "contribution": 1-5,
        "overall": 1-5
    }}
}}

Respond ONLY with valid JSON. Be critical but fair. Base your critique on your expertise from REVIEWER_PAPER."""


def extract_pdf_text(pdf_path: Path, max_chars: int = 80000) -> str:
    """Extract text from PDF with improved handling."""
    try:
        doc = fitz.open(pdf_path)
        text_parts = []
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            text_parts.append(f"[Page {page_num + 1}]\n{page_text}")
            if sum(len(t) for t in text_parts) > max_chars:
                break
        doc.close()
        full_text = "\n\n".join(text_parts)
        return full_text[:max_chars]
    except Exception as e:
        return f"ERROR: Could not extract text - {e}"


def get_paper_title_from_text(text: str) -> str:
    """Extract approximate title from first part of paper text."""
    lines = text.split('\n')
    for line in lines[:20]:
        line = line.strip()
        if len(line) > 20 and len(line) < 200:
            # Likely a title
            return line
    return "Unknown Title"


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check our paper exists
    if not OUR_PAPER_PDF.exists():
        print(f"ERROR: Our paper PDF not found at {OUR_PAPER_PDF}")
        print("Run: pdflatex main.tex to generate it")
        return None
    
    print("=" * 70)
    print("PEER REVIEW BATCH: Critical Analysis of Our Systematic Review")
    print("=" * 70)
    
    # Extract our paper text
    print(f"\n📄 Extracting our systematic review: {OUR_PAPER_PDF.name}")
    our_paper_text = extract_pdf_text(OUR_PAPER_PDF, max_chars=OUR_PAPER_MAX_CHARS)
    if our_paper_text.startswith("ERROR"):
        print(f"  ❌ {our_paper_text}")
        return None
    print(f"  ✅ Extracted {len(our_paper_text):,} characters")
    
    # Get all reviewed papers
    pdf_files = sorted(REVIEWED_PAPERS_DIR.glob("*.pdf"))
    print(f"\n📚 Found {len(pdf_files)} reviewed papers to use as reviewers")
    
    # Create batch requests
    batch_requests = []
    papers_processed = []

    # Rough token estimation: ~4 chars per token
    # Add a small overhead buffer for prompt scaffolding.
    prompt_overhead_chars = 6000
    total_input_tokens_est = 0
    
    for pdf_path in pdf_files:
        paper_id = pdf_path.stem
        print(f"\n  Processing reviewer: {paper_id}")
        
        # Extract reviewer paper text
        reviewer_text = extract_pdf_text(pdf_path, max_chars=REVIEWER_PAPER_MAX_CHARS)
        if reviewer_text.startswith("ERROR"):
            print(f"    ⚠️ {reviewer_text}")
            continue
        
        # Get approximate title
        reviewer_title = get_paper_title_from_text(reviewer_text)
        
        # Create the review prompt
        prompt = REVIEW_PROMPT_TEMPLATE.format(
            paper_id=paper_id,
            reviewer_paper_title=reviewer_title,
            reviewer_paper_text=reviewer_text,
            our_paper_text=our_paper_text
        )
        
        # Create batch request
        request = {
            "custom_id": f"review_{paper_id}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a critical academic peer reviewer with expertise in medical image segmentation and deep learning. Provide thorough, rigorous, and fair reviews."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "temperature": 0.2,
                "max_completion_tokens": 4000,
                "response_format": {"type": "json_object"}
            }
        }
        batch_requests.append(request)

        total_input_tokens_est += int((len(our_paper_text) + len(reviewer_text) + prompt_overhead_chars) / 4)

        papers_processed.append({
            "paper_id": paper_id,
            "title": reviewer_title[:100],
            "chars_extracted": len(reviewer_text)
        })
        print(f"    ✅ Added as reviewer ({len(reviewer_text):,} chars)")
    
    print(f"\n{'='*70}")
    print(f"BATCH SUMMARY")
    print(f"{'='*70}")
    print(f"Total reviewers: {len(batch_requests)}")
    print(f"Our paper: {len(our_paper_text):,} characters")
    
    # Save batch file
    batch_file = OUTPUT_DIR / f"peer_review_batch_{timestamp}.jsonl"
    with open(batch_file, 'w', encoding='utf-8') as f:
        for req in batch_requests:
            f.write(json.dumps(req) + '\n')
    print(f"\n📁 Batch file saved: {batch_file}")
    
    # Save papers info
    papers_info_file = OUTPUT_DIR / f"reviewer_papers_{timestamp}.json"
    with open(papers_info_file, 'w', encoding='utf-8') as f:
        json.dump(papers_processed, f, indent=2)
    
    # Estimate cost using the same GPT-5.2 assumptions already used elsewhere in this repo.
    # NOTE: This is an estimate only.
    # Input: $0.75 / 1M tokens, Output: $3.00 / 1M tokens
    total_output_tokens_est = len(batch_requests) * 3000
    input_cost = (total_input_tokens_est / 1_000_000) * 0.75
    output_cost = (total_output_tokens_est / 1_000_000) * 3.00
    total_cost = input_cost + output_cost

    print(f"\n{'='*70}")
    print(f"COST ESTIMATE ({MODEL_NAME})")
    print(f"{'='*70}")
    print(f"Input tokens:  ~{total_input_tokens_est:,.0f}")
    print(f"Output tokens: ~{total_output_tokens_est:,.0f}")
    print(f"Input cost:    ${input_cost:.2f}")
    print(f"Output cost:   ${output_cost:.2f}")
    print(f"TOTAL COST:    ${total_cost:.2f}")

    print(f"\nNext: submit with: python supplementary/scripts/submit_peer_review.py")
    return str(batch_file)


if __name__ == "__main__":
    main()
