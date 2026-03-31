#!/usr/bin/env python3
"""
S2 - AI-Assisted Screening with GPT (PARALLEL MODE)
Sends multiple concurrent requests for faster processing.

Speed comparison:
- Sequential: ~2 sec/paper = ~1.5 hours
- Parallel (50 concurrent): ~10-15 minutes

Uses asyncio for concurrent API calls.
"""

import os
import csv
import json
import time
import asyncio
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load .env file from project root
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# Configuration
INPUT_FILE = Path(__file__).parent.parent.parent / "data" / "interim" / "S1_search_results_deduplicated.csv"
OUTPUT_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_screened.csv"
PROGRESS_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_screening_progress.json"

# Parallel settings
MAX_CONCURRENT = 50  # Concurrent requests (adjust based on rate limits)
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

# Screening parameters
NUM_RUNS = 3
TEMPERATURE = 0.3

# Screening prompt
SCREENING_PROMPT = """You are screening papers for a systematic review on "3D Organ Segmentation from CT Scans using Deep Learning".

INCLUSION CRITERIA (ALL must be met):
1. Uses deep learning (CNN, Transformer, U-Net, etc.) - NOT traditional ML or rule-based
2. Performs 3D volumetric segmentation - NOT 2D slice-by-slice only
3. Uses CT imaging modality - NOT MRI, ultrasound, X-ray only
4. Segments anatomical organs (liver, kidney, lung, heart, spleen, pancreas, etc.) - NOT tumors/lesions only, NOT bones/vessels only
5. Published 2015-2024
6. Original research with methodology - NOT review papers, NOT datasets-only papers

EXCLUSION CRITERIA (ANY excludes):
- Detection/classification without segmentation
- 2D-only methods
- Non-CT modalities exclusively  
- Non-organ targets (tumors, vessels, bones only)
- Survey/review papers without novel methodology

PAPER TO SCREEN:
Title: {title}
Abstract: {abstract}

Respond with JSON only:
{{"decision": "INCLUDE" or "EXCLUDE", "confidence": 0-100, "rationale": "brief reason", "criteria_met": ["list"], "criteria_failed": ["list"]}}"""


async def screen_paper_once(client, semaphore, paper_id, title, abstract, run_num):
    """Single async screening request."""
    prompt = SCREENING_PROMPT.format(
        title=title or "No title",
        abstract=abstract or "No abstract available"
    )
    
    async with semaphore:
        for attempt in range(RETRY_ATTEMPTS):
            try:
                response = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a systematic review screening assistant. Always respond with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=TEMPERATURE,
                    max_tokens=300
                )
                
                result_text = response.choices[0].message.content or ""
                result_text = result_text.strip()
                
                # Handle markdown code blocks
                if result_text.startswith("```"):
                    result_text = result_text.split("```")[1]
                    if result_text.startswith("json"):
                        result_text = result_text[4:]
                    result_text = result_text.strip()
                
                result = json.loads(result_text)
                
                return {
                    "paper_id": paper_id,
                    "run": run_num,
                    "decision": result.get("decision", "UNCERTAIN"),
                    "confidence": result.get("confidence", 50),
                    "rationale": result.get("rationale", ""),
                    "criteria_met": result.get("criteria_met", []),
                    "criteria_failed": result.get("criteria_failed", [])
                }
                
            except json.JSONDecodeError:
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY)
                    continue
                return {
                    "paper_id": paper_id,
                    "run": run_num,
                    "decision": "UNCERTAIN",
                    "confidence": 0,
                    "rationale": "JSON parse error"
                }
            except Exception as e:
                error_str = str(e).lower()
                if "rate" in error_str:
                    wait = 10 * (attempt + 1)
                    print(f"    Rate limit hit, waiting {wait}s...")
                    await asyncio.sleep(wait)
                elif attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    return {
                        "paper_id": paper_id,
                        "run": run_num,
                        "decision": "UNCERTAIN",
                        "confidence": 0,
                        "rationale": f"API error: {str(e)[:50]}"
                    }
    
    return {
        "paper_id": paper_id,
        "run": run_num,
        "decision": "UNCERTAIN",
        "confidence": 0,
        "rationale": "Max retries exceeded"
    }


async def screen_paper_batch(client, semaphore, papers, progress_callback=None):
    """Screen a batch of papers with 3 runs each."""
    tasks = []
    
    for paper in papers:
        paper_id = paper.get('doi') or paper.get('id') or paper.get('title', '')[:50]
        title = paper.get('title', '')
        abstract = paper.get('abstract_snippet', '') or paper.get('abstract', '')
        
        for run_num in range(1, NUM_RUNS + 1):
            task = screen_paper_once(client, semaphore, paper_id, title, abstract, run_num)
            tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle any exceptions
    processed_results = []
    for r in results:
        if isinstance(r, Exception):
            processed_results.append({
                "paper_id": "unknown",
                "run": 0,
                "decision": "UNCERTAIN",
                "confidence": 0,
                "rationale": f"Exception: {str(r)[:50]}"
            })
        else:
            processed_results.append(r)
    
    return processed_results


def aggregate_results(results, papers):
    """Aggregate 3-run results into final decisions."""
    # Group by paper_id
    by_paper = {}
    for r in results:
        pid = r.get("paper_id", "")
        if pid not in by_paper:
            by_paper[pid] = []
        by_paper[pid].append(r)
    
    # Create final rows
    final_results = []
    for paper in papers:
        paper_id = paper.get('doi') or paper.get('id') or paper.get('title', '')[:50]
        runs = by_paper.get(paper_id, [])
        
        # Sort by run number
        runs = sorted(runs, key=lambda x: x.get('run', 0))
        
        # Count decisions
        include_count = sum(1 for r in runs if r.get('decision') == 'INCLUDE')
        exclude_count = sum(1 for r in runs if r.get('decision') == 'EXCLUDE')
        
        # Unanimous voting: INCLUDE only if ALL runs agree, otherwise EXCLUDE
        if include_count == len(runs):
            final_decision = 'INCLUDE'
        else:
            final_decision = 'EXCLUDE'  # No consensus = EXCLUDE (conservative)
        
        # Average confidence
        confidences = [r.get('confidence', 50) for r in runs if r.get('confidence', 0) > 0]
        avg_conf = sum(confidences) / len(confidences) if confidences else 50
        
        # Build vote string
        votes = ''.join(r.get('decision', 'E')[0] for r in runs[:3])
        
        # Get rationales
        rationales = [r.get('rationale', '') for r in runs if r.get('rationale')]
        combined_rationale = rationales[0] if rationales else ''
        
        # Criteria
        criteria_met = []
        criteria_failed = []
        for r in runs:
            criteria_met.extend(r.get('criteria_met', []))
            criteria_failed.extend(r.get('criteria_failed', []))
        
        row = {
            **paper,
            'screening_decision': final_decision,
            'avg_confidence': round(avg_conf, 1),
            'run_1_decision': runs[0].get('decision', '') if len(runs) > 0 else '',
            'run_1_confidence': runs[0].get('confidence', '') if len(runs) > 0 else '',
            'run_2_decision': runs[1].get('decision', '') if len(runs) > 1 else '',
            'run_2_confidence': runs[1].get('confidence', '') if len(runs) > 1 else '',
            'run_3_decision': runs[2].get('decision', '') if len(runs) > 2 else '',
            'run_3_confidence': runs[2].get('confidence', '') if len(runs) > 2 else '',
            'votes': votes,
            'rationale': combined_rationale,
            'criteria_met': ', '.join(set(criteria_met))[:200],
            'criteria_failed': ', '.join(set(criteria_failed))[:200],
            'needs_manual_review': final_decision == 'UNCERTAIN' or avg_conf < 70
        }
        final_results.append(row)
    
    return final_results


async def main_async():
    # Check API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set!")
        return
    
    client = AsyncOpenAI(api_key=api_key)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    
    # Load papers
    print("=" * 70)
    print("  S2 - AI-ASSISTED SCREENING (PARALLEL MODE)")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  - Model: gpt-4o-mini")
    print(f"  - Concurrent requests: {MAX_CONCURRENT}")
    print(f"  - Runs per paper: {NUM_RUNS}")
    print(f"  - Temperature: {TEMPERATURE}")
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
    
    total_papers = len(papers)
    total_requests = total_papers * NUM_RUNS
    print(f"\nTotal papers: {total_papers}")
    print(f"Total API requests: {total_requests}")
    print(f"Estimated time: {total_requests / MAX_CONCURRENT * 1.5 / 60:.1f} minutes")
    print(f"Estimated cost: ~${total_requests * 0.0002:.2f}")
    
    # Process in chunks to show progress
    CHUNK_SIZE = 100
    all_results = []
    
    start_time = time.time()
    
    for i in range(0, total_papers, CHUNK_SIZE):
        chunk = papers[i:i + CHUNK_SIZE]
        chunk_num = i // CHUNK_SIZE + 1
        total_chunks = (total_papers + CHUNK_SIZE - 1) // CHUNK_SIZE
        
        print(f"\n[Chunk {chunk_num}/{total_chunks}] Processing papers {i+1}-{min(i+CHUNK_SIZE, total_papers)}...")
        
        chunk_start = time.time()
        results = await screen_paper_batch(client, semaphore, chunk)
        chunk_time = time.time() - chunk_start
        
        all_results.extend(results)
        
        # Quick stats
        chunk_decisions = {}
        for r in results:
            d = r.get('decision', 'UNCERTAIN')
            chunk_decisions[d] = chunk_decisions.get(d, 0) + 1
        
        elapsed = time.time() - start_time
        rate = (i + len(chunk)) / elapsed if elapsed > 0 else 0
        remaining = (total_papers - i - len(chunk)) / rate if rate > 0 else 0
        
        print(f"  ✓ {len(chunk)} papers in {chunk_time:.1f}s | "
              f"I:{chunk_decisions.get('INCLUDE', 0)//3} E:{chunk_decisions.get('EXCLUDE', 0)//3} U:{chunk_decisions.get('UNCERTAIN', 0)//3}")
        print(f"  Progress: {i + len(chunk)}/{total_papers} | ETA: {remaining/60:.1f} min")
    
    # Aggregate results
    print(f"\nAggregating results...")
    final_results = aggregate_results(all_results, papers)
    
    # Count final decisions
    include_count = sum(1 for r in final_results if r['screening_decision'] == 'INCLUDE')
    exclude_count = sum(1 for r in final_results if r['screening_decision'] == 'EXCLUDE')
    uncertain_count = sum(1 for r in final_results if r['screening_decision'] == 'UNCERTAIN')
    
    # Save results
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = [
        'id', 'database', 'search_date', 'title', 'authors', 'year', 'journal_conference', 'doi', 'abstract_snippet',
        'screening_decision', 'avg_confidence', 'votes',
        'run_1_decision', 'run_1_confidence',
        'run_2_decision', 'run_2_confidence',
        'run_3_decision', 'run_3_confidence',
        'rationale', 'criteria_met', 'criteria_failed', 'needs_manual_review'
    ]
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(final_results)
    
    total_time = time.time() - start_time
    
    print(f"\n{'=' * 70}")
    print(f"  SCREENING COMPLETE")
    print(f"{'=' * 70}")
    print(f"\nTime: {total_time/60:.1f} minutes")
    print(f"\nResults:")
    print(f"  ✅ INCLUDE:   {include_count} ({100*include_count/total_papers:.1f}%)")
    print(f"  ❌ EXCLUDE:   {exclude_count} ({100*exclude_count/total_papers:.1f}%)")
    print(f"  ❓ UNCERTAIN: {uncertain_count} ({100*uncertain_count/total_papers:.1f}%)")
    print(f"\nOutput: {OUTPUT_FILE}")
    
    # Save progress too
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({
            "completed_at": datetime.now().isoformat(),
            "total_papers": total_papers,
            "include": include_count,
            "exclude": exclude_count,
            "uncertain": uncertain_count,
            "time_seconds": total_time
        }, f, indent=2)


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
