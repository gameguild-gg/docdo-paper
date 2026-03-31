#!/usr/bin/env python3
"""
Step 1: Copy the 52 included papers to a dedicated folder.
"""

import json
import shutil
from pathlib import Path

# Paths
RESULTS_FILE = Path("d:/repositories/game-guild/docdo-paper/data/processed/s3_fulltext_screening/batch/s3_parsed_results.json")
PDF_DIR = Path("d:/repositories/game-guild/docdo-paper/data/pdfs")
OUTPUT_DIR = Path("d:/repositories/game-guild/docdo-paper/data/final_included_papers")

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load results
    with open(RESULTS_FILE) as f:
        results = json.load(f)
    
    # Get included papers
    included = [r for r in results if r.get('screening_decision') == 'INCLUDE']
    print(f"Found {len(included)} included papers")
    
    # Copy PDFs
    copied = 0
    not_found = []
    
    for r in included:
        paper_id = r.get('paper_id', '')
        
        # Find the PDF file
        pdf_file = PDF_DIR / f"{paper_id}.pdf"
        
        if pdf_file.exists():
            dest = OUTPUT_DIR / f"{paper_id}.pdf"
            shutil.copy2(pdf_file, dest)
            copied += 1
            print(f"  ✓ {paper_id}")
        else:
            not_found.append(paper_id)
            print(f"  ✗ NOT FOUND: {paper_id}")
    
    print(f"\n{'='*60}")
    print(f"Copied: {copied}/{len(included)} papers")
    print(f"Destination: {OUTPUT_DIR}")
    
    if not_found:
        print(f"\nNot found ({len(not_found)}):")
        for p in not_found:
            print(f"  - {p}")
    
    return copied

if __name__ == "__main__":
    main()
