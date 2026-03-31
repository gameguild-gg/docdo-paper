#!/usr/bin/env python3
"""
Sample papers for human validation (10-20% of included papers).
Creates a spreadsheet for manual review.
"""

import csv
import json
import random
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
FINAL_RESULTS_DIR = REPO_ROOT / "data" / "processed" / "final_results"
OUT_DIR = REPO_ROOT / "data" / "processed" / "validation"

SAMPLE_RATE = 0.15  # 15% sample
RANDOM_SEED = 42


def find_latest_included_file():
    files = sorted(FINAL_RESULTS_DIR.glob("final_included_papers_*.csv"), reverse=True)
    if not files:
        raise SystemExit(f"No final_included_papers_*.csv found in {FINAL_RESULTS_DIR}")
    return files[0]


def find_latest_results_file():
    files = sorted(FINAL_RESULTS_DIR.glob("final_screening_results_*.csv"), reverse=True)
    if not files:
        raise SystemExit(f"No final_screening_results_*.csv found in {FINAL_RESULTS_DIR}")
    return files[0]


def main():
    random.seed(RANDOM_SEED)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load all results for context
    results_file = find_latest_results_file()
    all_results = {}
    with open(results_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_results[row['paper_id']] = row
    
    # Load included papers
    included_file = find_latest_included_file()
    included_papers = []
    with open(included_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            included_papers.append(row)
    
    total = len(included_papers)
    sample_size = max(10, int(total * SAMPLE_RATE))  # At least 10
    
    print(f"Total included papers: {total}")
    print(f"Sample size ({SAMPLE_RATE*100:.0f}%): {sample_size}")
    
    # Random sample
    sample = random.sample(included_papers, sample_size)
    
    # Create validation spreadsheet
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    val_path = OUT_DIR / f"validation_sample_{timestamp}.csv"
    
    with open(val_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "paper_id", 
            "title", 
            "abstract_snippet",
            "strict_decision",
            "nano_decision", 
            "gpt52_decision",
            "final_decision",
            "human_decision",  # To be filled by reviewer
            "human_notes"      # To be filled by reviewer
        ])
        
        for paper in sample:
            pid = paper['paper_id']
            result = all_results.get(pid, {})
            writer.writerow([
                pid,
                paper.get('title', ''),
                paper.get('abstract_snippet', '')[:1000],
                result.get('strict_decision', ''),
                result.get('nano_decision', ''),
                result.get('gpt52_decision', ''),
                result.get('final_decision', ''),
                '',  # human_decision - to be filled
                ''   # human_notes - to be filled
            ])
    
    print(f"\nWrote: {val_path.name}")
    
    # Also create a summary
    summary = {
        "timestamp": timestamp,
        "total_included": total,
        "sample_size": sample_size,
        "sample_rate": SAMPLE_RATE,
        "random_seed": RANDOM_SEED,
        "papers": [p['paper_id'] for p in sample]
    }
    summary_path = OUT_DIR / f"validation_sample_{timestamp}_info.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(f"Wrote: {summary_path.name}")
    
    print(f"\n✅ Validation sample created!")
    print(f"   Review the {sample_size} papers in: {val_path.name}")
    print(f"   Fill in 'human_decision' (INCLUDE/EXCLUDE) and 'human_notes'")


if __name__ == "__main__":
    main()
