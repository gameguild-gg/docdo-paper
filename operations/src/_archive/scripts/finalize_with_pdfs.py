#!/usr/bin/env python3
"""
Create final included papers list with only papers that have PDFs.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
PDF_DIR = Path("data/pdfs")
WITH_PDFS = Path("data/processed/pdf_fetching/papers_with_pdfs_ready.csv")
WITHOUT_PDFS = Path("data/processed/pdf_fetching/papers_to_fetch_manually.csv")
OUTPUT_DIR = Path("data/processed/final_results")

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Load data
    df_with = pd.read_csv(WITH_PDFS)
    df_without = pd.read_csv(WITHOUT_PDFS)
    
    print(f"Papers WITH PDFs: {len(df_with)}")
    print(f"Papers WITHOUT PDFs: {len(df_without)}")
    
    # Add status columns
    df_with['pdf_status'] = 'available'
    df_with['included_in_review'] = True
    
    df_without['pdf_status'] = 'not_available'
    df_without['included_in_review'] = False
    df_without['exclusion_reason'] = 'Full-text not publicly available'
    df_without['exclusion_stage'] = 'S3_fulltext_retrieval'
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save final included (with PDFs only)
    output_included = OUTPUT_DIR / f"final_included_for_review_{timestamp}.csv"
    df_with.to_csv(output_included, index=False)
    print(f"\nSaved: {output_included}")
    
    # Save excluded (no PDFs)
    output_excluded = OUTPUT_DIR / f"excluded_no_fulltext_{timestamp}.csv"
    df_without.to_csv(output_excluded, index=False)
    print(f"Saved: {output_excluded}")
    
    # Combined file with all papers and their status
    df_all = pd.concat([df_with, df_without], ignore_index=True)
    output_all = OUTPUT_DIR / f"all_papers_after_s2_with_status_{timestamp}.csv"
    df_all.to_csv(output_all, index=False)
    print(f"Saved: {output_all}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total after AI screening (S2):  161")
    print(f"Full-text retrieved:            {len(df_with)}")
    print(f"Full-text not available:        {len(df_without)}")
    print(f"Final for full-text review:     {len(df_with)}")
    print("="*60)
    
    return len(df_with), len(df_without)

if __name__ == "__main__":
    main()
