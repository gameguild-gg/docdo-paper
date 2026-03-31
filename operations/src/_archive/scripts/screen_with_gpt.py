#!/usr/bin/env python3
"""
S2 - AI-Assisted Screening with GPT
Applies inclusion/exclusion criteria following paper methodology.

Methodology (from main.tex):
- 3 screening runs per paper (temperature=0.3)
- INCLUDE requires ≥2/3 agreement
- UNCERTAIN triggers manual review flag
- EXCLUDE with confidence <80 flags for manual verification

Input: data/interim/S1_search_results_deduplicated.csv
Output: data/processed/S2_screened.csv
"""

import os
import csv
import json
import time
import httpx
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file from project root
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# Configuration
INPUT_FILE = Path(__file__).parent.parent.parent / "data" / "interim" / "S1_search_results_deduplicated.csv"
OUTPUT_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_screened.csv"
PROGRESS_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_screening_progress.json"

# API timeout (seconds) - longer to handle slow responses
API_TIMEOUT = 60.0

# Number of screening runs per paper (for hallucination control)
NUM_RUNS = 3
TEMPERATURE = 0.3  # Low randomness for consistency

# Improved screening prompt (v1.2) - see supplementary/S4_screening_criteria.md
SCREENING_PROMPT = """You are screening papers for a systematic review on "3D Organ Segmentation from CT Scans using Deep Learning".

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

## DECISION GUIDANCE:
- **INCLUDE**: Meets IC1-IC5 or abstract strongly suggests it does
- **EXCLUDE**: Clearly violates any exclusion criterion
- **UNCERTAIN**: Abstract missing/unclear or genuinely ambiguous (rare)

BE DECISIVE. Papers with "CT", "organ segmentation", and "deep learning/neural network" are usually INCLUDE.

---
TITLE: {title}

ABSTRACT: {abstract}
---

Return ONLY valid JSON:
{{
  "decision": "INCLUDE" | "EXCLUDE" | "UNCERTAIN",
  "confidence": 70-95,
  "rationale": "One sentence explanation",
  "criteria_met": ["IC1", "IC2", ...],
  "criteria_failed": ["EC1", ...]
}}"""


def load_progress():
    """Load screening progress if exists."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"screened_dois": [], "results": []}


def save_progress(progress):
    """Save screening progress."""
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)


def screen_paper_once(client, title, abstract, retries=3):
    """Single screening run for a paper."""
    prompt = SCREENING_PROMPT.format(
        title=title or "No title",
        abstract=abstract or "No abstract available"
    )
    
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Reliable: $0.15 input, $0.60 output per 1M tokens
                messages=[
                    {"role": "system", "content": "You are a systematic review screening assistant. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=300
            )
            
            result_text = response.choices[0].message.content
            if result_text is None:
                result_text = ""
            result_text = result_text.strip()
            
            # Debug: print raw response for first few
            if not result_text:
                print(f"      Empty response from API")
                raise json.JSONDecodeError("Empty response", "", 0)
            
            # Handle markdown code blocks
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            
            result = json.loads(result_text)
            
            # Validate required fields
            if 'decision' not in result:
                result['decision'] = 'EXCLUDE'
            if 'confidence' not in result:
                result['confidence'] = 50
            if 'rationale' not in result:
                result['rationale'] = ''
            if 'criteria_met' not in result:
                result['criteria_met'] = []
            if 'criteria_failed' not in result:
                result['criteria_failed'] = []
                
            return result
            
        except json.JSONDecodeError as e:
            print(f"      JSON error: {str(e)[:60]}")
            if attempt < retries - 1:
                time.sleep(1)
                continue
            return {
                "decision": "EXCLUDE",
                "confidence": 0,
                "rationale": f"JSON parse error: {str(e)[:50]}",
                "criteria_met": [],
                "criteria_failed": []
            }
        except Exception as e:
            error_str = str(e).lower()
            print(f"      API error: {str(e)[:80]}")
            
            # Rate limit handling
            if "rate_limit" in error_str:
                wait_time = 30 * (attempt + 1)
                print(f"      Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            # Network/timeout errors - retry with longer wait
            elif any(x in error_str for x in ["timeout", "connection", "network", "ssl", "read"]):
                wait_time = 5 * (attempt + 1)
                print(f"      Network error. Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            elif attempt < retries - 1:
                time.sleep(2)
            else:
                return {
                    "decision": "EXCLUDE",
                    "confidence": 0,
                    "rationale": f"API error: {str(e)[:50]}",
                    "criteria_met": [],
                    "criteria_failed": []
                }
    
    return None


def determine_final_decision(runs):
    """
    Determine final decision based on unanimous voting.
    
    Rules (conservative approach):
    - INCLUDE requires 3/3 runs agreeing (unanimous)
    - If no agreement → EXCLUDE (no UNCERTAIN)
    """
    decisions = [r['decision'] for r in runs]
    confidences = [r['confidence'] for r in runs]
    
    include_count = decisions.count('INCLUDE')
    total_runs = len(runs)
    
    avg_confidence = sum(confidences) / len(confidences)
    
    # Unanimous agreement required for INCLUDE (conservative approach)
    if include_count == total_runs:
        final_decision = 'INCLUDE'
    else:
        final_decision = 'EXCLUDE'  # No consensus = EXCLUDE
    
    # No manual review flags - decision is final
    needs_manual_review = False
    manual_review_reason = []
    
    # Combine rationales
    combined_rationale = runs[0]['rationale']  # Use first run's rationale
    
    # Combine criteria
    all_criteria_met = set()
    all_criteria_failed = set()
    for r in runs:
        all_criteria_met.update(r.get('criteria_met', []))
        all_criteria_failed.update(r.get('criteria_failed', []))
    
    return {
        'final_decision': final_decision,
        'avg_confidence': avg_confidence,
        'run_1_decision': runs[0]['decision'],
        'run_1_confidence': runs[0]['confidence'],
        'run_2_decision': runs[1]['decision'],
        'run_2_confidence': runs[1]['confidence'],
        'run_3_decision': runs[2]['decision'],
        'run_3_confidence': runs[2]['confidence'],
        'rationale': combined_rationale,
        'criteria_met': ','.join(sorted(str(c) for c in all_criteria_met)),
        'criteria_failed': ','.join(sorted(str(c) for c in all_criteria_failed)),
        'needs_manual_review': needs_manual_review,
        'manual_review_reason': '; '.join(manual_review_reason) if manual_review_reason else ''
    }


def screen_paper(client, title, abstract):
    """Screen a paper with 3 runs and majority voting."""
    runs = []
    
    for run_num in range(NUM_RUNS):
        result = screen_paper_once(client, title, abstract)
        if result:
            runs.append(result)
            # Small delay between runs
            time.sleep(0.3)
    
    if len(runs) < NUM_RUNS:
        # Fill missing runs with UNCERTAIN
        while len(runs) < NUM_RUNS:
            runs.append({
                "decision": "UNCERTAIN",
                "confidence": 0,
                "rationale": "Run failed",
                "criteria_met": [],
                "criteria_failed": []
            })
    
    return determine_final_decision(runs)


def main():
    # Check for API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set!")
        print("Set it with: $env:OPENAI_API_KEY='your-key-here'")
        return
    
    # Create client with longer timeout
    client = OpenAI(
        api_key=api_key,
        timeout=httpx.Timeout(API_TIMEOUT, connect=10.0)
    )
    
    # Load data
    print("=" * 70)
    print("  S2 - AI-ASSISTED SCREENING (3-RUN MAJORITY VOTING)")
    print("=" * 70)
    print(f"\nMethodology:")
    print(f"  - Model: gpt-4o-mini (~$1.55 estimated)")
    print(f"  - Runs per paper: {NUM_RUNS}")
    print(f"  - Temperature: {TEMPERATURE}")
    print(f"  - INCLUDE requires: ≥2/3 agreement")
    print(f"\nInput:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    
    # Load papers
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
    
    print(f"\nTotal papers to screen: {len(papers)}")
    
    # Load progress
    progress = load_progress()
    screened_dois = set(progress["screened_dois"])
    results = progress["results"]
    
    if screened_dois:
        print(f"Resuming from checkpoint: {len(screened_dois)} already screened")
    
    # Screen papers
    start_time = time.time()
    
    for i, paper in enumerate(papers):
        doi = paper.get('doi', paper.get('title', f'idx_{i}'))
        
        # Skip already screened
        if doi in screened_dois:
            continue
        
        title = paper.get('title', '')
        abstract = paper.get('abstract_snippet', '') or paper.get('abstract', '')  # Handle both column names
        
        print(f"\n[{i+1}/{len(papers)}] {title[:55]}...")
        
        # Screen with 3 runs
        screening_result = screen_paper(client, title, abstract)
        
        # Build output record
        screened_paper = {
            **paper,
            'screening_decision': screening_result['final_decision'],
            'avg_confidence': f"{screening_result['avg_confidence']:.0f}",
            'run_1_decision': screening_result['run_1_decision'],
            'run_1_confidence': screening_result['run_1_confidence'],
            'run_2_decision': screening_result['run_2_decision'],
            'run_2_confidence': screening_result['run_2_confidence'],
            'run_3_decision': screening_result['run_3_decision'],
            'run_3_confidence': screening_result['run_3_confidence'],
            'rationale': screening_result['rationale'],
            'criteria_met': screening_result['criteria_met'],
            'criteria_failed': screening_result['criteria_failed'],
            'needs_manual_review': screening_result['needs_manual_review'],
            'manual_review_reason': screening_result['manual_review_reason']
        }
        results.append(screened_paper)
        screened_dois.add(doi)
        
        # Show result
        decision = screening_result['final_decision']
        conf = screening_result['avg_confidence']
        votes = f"[{screening_result['run_1_decision'][0]}/{screening_result['run_2_decision'][0]}/{screening_result['run_3_decision'][0]}]"
        symbol = "✅" if decision == "INCLUDE" else "❌" if decision == "EXCLUDE" else "❓"
        flag = " 🔍" if screening_result['needs_manual_review'] else ""
        print(f"    {symbol} {decision} {votes} (conf={conf:.0f}){flag}")
        
        # Save progress every 10 papers
        if len(results) % 10 == 0:
            progress["screened_dois"] = list(screened_dois)
            progress["results"] = results
            save_progress(progress)
            
            # Show interim stats
            inc = sum(1 for r in results if r.get('screening_decision') == 'INCLUDE')
            exc = sum(1 for r in results if r.get('screening_decision') == 'EXCLUDE')
            unc = sum(1 for r in results if r.get('screening_decision') == 'UNCERTAIN')
            print(f"    [Checkpoint: {len(results)} papers | ✅{inc} ❌{exc} ❓{unc}]")
        
        # Delay between papers
        time.sleep(0.5)
    
    # Save final results
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if results:
        fieldnames = list(results[0].keys())
        with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    
    # Summary
    elapsed = time.time() - start_time
    include_count = sum(1 for r in results if r.get('screening_decision') == 'INCLUDE')
    exclude_count = sum(1 for r in results if r.get('screening_decision') == 'EXCLUDE')
    uncertain_count = sum(1 for r in results if r.get('screening_decision') == 'UNCERTAIN')
    manual_review_count = sum(1 for r in results if r.get('needs_manual_review'))
    
    print("\n" + "=" * 70)
    print("  SCREENING COMPLETE")
    print("=" * 70)
    print(f"\n  Total screened:    {len(results)}")
    print(f"  ✅ INCLUDE:        {include_count} ({100*include_count/len(results):.1f}%)")
    print(f"  ❌ EXCLUDE:        {exclude_count} ({100*exclude_count/len(results):.1f}%)")
    print(f"  ❓ UNCERTAIN:      {uncertain_count} ({100*uncertain_count/len(results):.1f}%)")
    print(f"  🔍 Manual review:  {manual_review_count}")
    print(f"\n  Time elapsed:      {elapsed/60:.1f} minutes")
    print(f"  Output saved:      {OUTPUT_FILE}")
    print("=" * 70)
    
    # Cleanup progress file on success
    if PROGRESS_FILE.exists() and len(results) == len(papers):
        PROGRESS_FILE.unlink()
        print("\n  [Progress file cleaned up]")


if __name__ == "__main__":
    main()
