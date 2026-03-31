#!/usr/bin/env python3
"""
Quick sample screening for co-author discussion.
Runs synchronously on a small random sample to get immediate results.
"""

import os
import csv
import json
import random
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parent.parent.parent / ".env")

INPUT_FILE = Path(__file__).parent.parent.parent / "data" / "interim" / "S1_search_results_deduplicated.csv"
OUTPUT_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_sample_screening.csv"

SAMPLE_SIZE = 30  # Quick sample for discussion
NUM_RUNS = 3
TEMPERATURE = 0.3

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

BE DECISIVE. Papers with "CT", "organ segmentation", and "deep learning/neural network" are usually INCLUDE.

---
TITLE: {title}
ABSTRACT: {abstract}
---

Return ONLY valid JSON:
{{"decision": "INCLUDE" | "EXCLUDE", "confidence": 70-95, "rationale": "One sentence", "criteria_met": ["IC1",...], "criteria_failed": ["EC1",...]}}"""


def screen_paper_once(client, title, abstract, retries=3):
    """Single screening run with retry."""
    prompt = SCREENING_PROMPT.format(
        title=title or "No title",
        abstract=abstract or "No abstract available"
    )
    
    import time
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a systematic review screening assistant. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=300,
                timeout=30
            )
            
            result_text = response.choices[0].message.content or ""
            result_text = result_text.strip()
            
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            
            return json.loads(result_text)
            
        except Exception as e:
            if attempt < retries - 1:
                print(f"    Retry {attempt+1}...")
                time.sleep(2 * (attempt + 1))
            else:
                return {"decision": "EXCLUDE", "confidence": 0, "rationale": str(e)[:50]}


def screen_paper(client, title, abstract):
    """3-run unanimous voting: INCLUDE only if ALL runs agree, otherwise EXCLUDE."""
    runs = []
    for _ in range(NUM_RUNS):
        result = screen_paper_once(client, title, abstract)
        runs.append(result)
    
    # Count votes
    include = sum(1 for r in runs if r.get('decision') == 'INCLUDE')
    
    # Unanimous agreement required for INCLUDE (conservative approach)
    if include == NUM_RUNS:
        final = 'INCLUDE'
    else:
        final = 'EXCLUDE'  # No consensus = EXCLUDE
    
    avg_conf = sum(r.get('confidence', 50) for r in runs) / len(runs)
    votes = ''.join(r.get('decision', 'E')[0] for r in runs)
    
    return {
        'decision': final,
        'confidence': round(avg_conf, 1),
        'votes': votes,
        'rationale': runs[0].get('rationale', ''),
        'criteria_met': runs[0].get('criteria_met', []),
        'criteria_failed': runs[0].get('criteria_failed', [])
    }


def main():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Load papers
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        all_papers = list(csv.DictReader(f))
    
    # Random sample
    random.seed(42)  # Reproducible
    sample = random.sample(all_papers, min(SAMPLE_SIZE, len(all_papers)))
    
    print("=" * 70)
    print("  SAMPLE SCREENING FOR CO-AUTHOR DISCUSSION")
    print("=" * 70)
    print(f"\nSample size: {len(sample)} papers (random)")
    print(f"Model: gpt-4o-mini | Runs: {NUM_RUNS} | Temperature: {TEMPERATURE}")
    print()
    
    results = []
    include_count = 0
    exclude_count = 0
    uncertain_count = 0
    
    for i, paper in enumerate(sample):
        title = paper.get('title', '')[:60]
        abstract = paper.get('abstract_snippet', '') or paper.get('abstract', '')
        
        print(f"[{i+1}/{len(sample)}] {title}...")
        
        result = screen_paper(client, paper.get('title', ''), abstract)
        
        if result['decision'] == 'INCLUDE':
            include_count += 1
            icon = '✅'
        elif result['decision'] == 'EXCLUDE':
            exclude_count += 1
            icon = '❌'
        else:
            uncertain_count += 1
            icon = '❓'
        
        print(f"    {icon} {result['decision']} [{result['votes']}] (conf={result['confidence']})")
        print(f"    Rationale: {result['rationale'][:80]}...")
        
        results.append({
            **paper,
            'screening_decision': result['decision'],
            'confidence': result['confidence'],
            'votes': result['votes'],
            'rationale': result['rationale'],
            'criteria_met': ', '.join(result.get('criteria_met', [])),
            'criteria_failed': ', '.join(result.get('criteria_failed', []))
        })
    
    # Save results
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = ['title', 'authors', 'year', 'doi', 'abstract_snippet', 
                  'screening_decision', 'confidence', 'votes', 'rationale',
                  'criteria_met', 'criteria_failed']
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    
    # Summary
    print()
    print("=" * 70)
    print("  SAMPLE RESULTS SUMMARY")
    print("=" * 70)
    print(f"\n✅ INCLUDE:   {include_count} ({100*include_count/len(sample):.0f}%)")
    print(f"❌ EXCLUDE:   {exclude_count} ({100*exclude_count/len(sample):.0f}%)")
    print(f"❓ UNCERTAIN: {uncertain_count} ({100*uncertain_count/len(sample):.0f}%)")
    print(f"\nOutput: {OUTPUT_FILE}")
    
    # Show some examples for discussion
    print("\n" + "=" * 70)
    print("  EXAMPLES FOR DISCUSSION")
    print("=" * 70)
    
    includes = [r for r in results if r['screening_decision'] == 'INCLUDE']
    excludes = [r for r in results if r['screening_decision'] == 'EXCLUDE']
    
    if includes:
        print("\n📗 INCLUDED PAPERS:")
        for r in includes[:5]:
            print(f"  • {r['title'][:70]}...")
            print(f"    Year: {r['year']} | Confidence: {r['confidence']} | Criteria met: {r['criteria_met'][:50]}")
    
    if excludes:
        print("\n📕 EXCLUDED PAPERS:")
        for r in excludes[:5]:
            print(f"  • {r['title'][:70]}...")
            print(f"    Reason: {r['rationale'][:60]}")
            print(f"    Failed: {r['criteria_failed'][:50]}")


if __name__ == "__main__":
    main()
