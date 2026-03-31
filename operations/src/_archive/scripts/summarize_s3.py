#!/usr/bin/env python3
"""Create final S3 screening report and data extraction summary."""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import Counter

# Paths
PROGRESS_FILE = Path("data/processed/s3_fulltext_screening/screening_progress.json")
EXTRACTED_FILE = Path("data/processed/s3_fulltext_screening/extracted_data_20260122_223714.csv")
OUTPUT_DIR = Path("data/processed/s3_fulltext_screening")

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Load progress
    with open(PROGRESS_FILE) as f:
        results = json.load(f)
    
    # Count decisions
    included = [r for r in results if r.get('screening_decision') == 'INCLUDE']
    excluded = [r for r in results if r.get('screening_decision') == 'EXCLUDE']
    errors = [r for r in results if r.get('screening_decision') == 'ERROR']
    
    print("=" * 60)
    print("S3 FULL-TEXT SCREENING SUMMARY")
    print("=" * 60)
    print(f"Total PDFs processed: {len(results)}")
    print(f"INCLUDED: {len(included)}")
    print(f"EXCLUDED: {len(excluded)}")
    print(f"ERRORS (API issues): {len(errors)}")
    print()
    
    # Exclusion reasons
    if excluded:
        reasons = Counter(r.get('exclusion_reason', 'Unknown') for r in excluded)
        print("Exclusion reasons:")
        for reason, count in reasons.most_common():
            print(f"  - {reason}: {count}")
    
    # Load extracted data
    if EXTRACTED_FILE.exists():
        df = pd.read_csv(EXTRACTED_FILE)
        print(f"\nExtracted data for {len(df)} papers")
        
        # Architecture summary
        if 'architecture' in df.columns:
            archs = df['architecture'].dropna().value_counts()
            print("\nArchitectures used:")
            for arch, count in archs.head(10).items():
                print(f"  - {arch}: {count}")
        
        # Organs summary
        if 'organs_segmented' in df.columns:
            all_organs = []
            for organs in df['organs_segmented'].dropna():
                try:
                    organ_list = eval(organs) if isinstance(organs, str) else organs
                    all_organs.extend([o.lower() for o in organ_list])
                except:
                    pass
            organ_counts = Counter(all_organs)
            print("\nOrgans segmented (top 10):")
            for organ, count in organ_counts.most_common(10):
                print(f"  - {organ}: {count}")
        
        # Multi-organ stats
        if 'multi_organ' in df.columns:
            multi = df['multi_organ'].sum()
            print(f"\nMulti-organ segmentation: {multi}/{len(df)} papers")
        
        # Year distribution
        if 'year' in df.columns:
            years = df['year'].dropna().value_counts().sort_index()
            print("\nPublication years:")
            for year, count in years.items():
                print(f"  - {int(year)}: {count}")
    
    # Create final report
    report = f"""# S3 Full-Text Screening Report

Generated: {datetime.now().isoformat()}

## Summary

| Category | Count |
|----------|-------|
| PDFs assessed | 63 |
| Screened successfully | {len(included) + len(excluded)} |
| INCLUDED (for review) | {len(included)} |
| EXCLUDED | {len(excluded)} |
| API Errors (not processed) | {len(errors)} |

## Final PRISMA Numbers

```
Records identified: 2,821
    ↓
After ES filter: 638
    ↓  
After AI screening (S2): 161
    ↓
Full-text available: 63
    ↓
After S3 full-text screening: {len(included)}
```

## S3 Exclusion Reasons

| Reason | Count |
|--------|-------|
"""
    
    if excluded:
        for reason, count in Counter(r.get('exclusion_reason', 'Unknown') for r in excluded).most_common():
            report += f"| {reason} | {count} |\n"
    
    report += f"""

## Papers with API Errors (Need Manual Review)

{len(errors)} papers could not be processed due to API rate limits.
These papers should be reviewed manually or retried later.

## Data Extraction Summary

- Papers with extracted data: {len(df) if EXTRACTED_FILE.exists() else 0}
- Data includes: title, authors, year, venue, architecture, organs, metrics, etc.

## Output Files

1. `extracted_data_20260122_223714.csv` - Extracted data from {len(df) if EXTRACTED_FILE.exists() else 0} papers
2. `screening_progress.json` - Full screening results with decisions

## Next Steps

1. ⏳ Retry {len(errors)} papers with API errors (or review manually)
2. ⏳ Validate extracted data
3. ⏳ Synthesize findings for systematic review
"""
    
    report_file = OUTPUT_DIR / f"S3_screening_report_{timestamp}.md"
    report_file.write_text(report, encoding='utf-8')
    print(f"\nSaved report: {report_file}")
    
    # Save final included list
    included_df = pd.DataFrame([{
        'paper_id': r['paper_id'],
        'decision': r['screening_decision'],
        'confidence': r.get('confidence'),
        'notes': r.get('screening_notes', '')
    } for r in included])
    
    included_file = OUTPUT_DIR / f"final_s3_included_{timestamp}.csv"
    included_df.to_csv(included_file, index=False)
    print(f"Saved: {included_file}")

if __name__ == "__main__":
    main()
