#!/usr/bin/env python3
"""
Process S3 batch results: create final CSV, generate synthesis tables.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import Counter

# Paths
RESULTS_FILE = Path("d:/repositories/game-guild/docdo-paper/data/processed/s3_fulltext_screening/batch/s3_parsed_results.json")
OUTPUT_DIR = Path("d:/repositories/game-guild/docdo-paper/data/processed/s3_fulltext_screening")

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Load results
    with open(RESULTS_FILE) as f:
        results = json.load(f)
    
    print(f"Loaded {len(results)} results")
    
    # Separate included/excluded
    included = [r for r in results if r.get('screening_decision') == 'INCLUDE']
    excluded = [r for r in results if r.get('screening_decision') == 'EXCLUDE']
    
    print(f"INCLUDED: {len(included)}")
    print(f"EXCLUDED: {len(excluded)}")
    
    # Extract data from included papers
    extracted_data = []
    for r in included:
        data = r.get('extracted_data', {}) or {}
        data['paper_id'] = r.get('paper_id', '')
        data['screening_confidence'] = r.get('confidence', 0)
        data['screening_notes'] = r.get('screening_notes', '')
        extracted_data.append(data)
    
    # Create DataFrame
    df = pd.DataFrame(extracted_data)
    
    # Save full extracted data
    full_csv = OUTPUT_DIR / f"s3_extracted_data_full_{timestamp}.csv"
    df.to_csv(full_csv, index=False)
    print(f"\nSaved: {full_csv}")
    
    # Create summary table for paper
    summary_cols = ['paper_id', 'title', 'authors', 'year', 'venue', 'architecture', 
                   'organs_segmented', 'multi_organ', 'best_dice', 'datasets']
    
    df_summary = df[[c for c in summary_cols if c in df.columns]].copy()
    summary_csv = OUTPUT_DIR / f"s3_summary_table_{timestamp}.csv"
    df_summary.to_csv(summary_csv, index=False)
    print(f"Saved: {summary_csv}")
    
    # Save excluded papers
    excluded_data = [{
        'paper_id': r.get('paper_id', ''),
        'screening_decision': r.get('screening_decision', ''),
        'exclusion_reason': r.get('exclusion_reason', ''),
        'screening_notes': r.get('screening_notes', '')
    } for r in excluded]
    
    df_excluded = pd.DataFrame(excluded_data)
    excluded_csv = OUTPUT_DIR / f"s3_excluded_papers_{timestamp}.csv"
    df_excluded.to_csv(excluded_csv, index=False)
    print(f"Saved: {excluded_csv}")
    
    # Generate statistics
    print("\n" + "="*60)
    print("DATA EXTRACTION SUMMARY")
    print("="*60)
    
    # Architecture distribution
    if 'architecture' in df.columns:
        archs = df['architecture'].dropna().value_counts()
        print("\n📊 Architectures:")
        for arch, count in archs.head(10).items():
            print(f"   {arch}: {count}")
    
    # Organs distribution
    if 'organs_segmented' in df.columns:
        all_organs = []
        for organs in df['organs_segmented'].dropna():
            try:
                if isinstance(organs, str):
                    organ_list = eval(organs)
                else:
                    organ_list = organs
                all_organs.extend([str(o).lower().strip() for o in organ_list])
            except:
                pass
        
        organ_counts = Counter(all_organs)
        print("\n🫀 Organs Segmented (top 15):")
        for organ, count in organ_counts.most_common(15):
            print(f"   {organ}: {count}")
    
    # Year distribution
    if 'year' in df.columns:
        years = df['year'].dropna().astype(int).value_counts().sort_index()
        print("\n📅 Publication Years:")
        for year, count in years.items():
            print(f"   {year}: {count}")
    
    # Multi-organ stats
    if 'multi_organ' in df.columns:
        multi = df['multi_organ'].sum()
        print(f"\n🔢 Multi-organ segmentation: {multi}/{len(df)} ({100*multi/len(df):.1f}%)")
    
    # Dice scores
    if 'best_dice' in df.columns:
        dice_values = pd.to_numeric(df['best_dice'], errors='coerce').dropna()
        if len(dice_values) > 0:
            # Normalize to 0-1 if percentages
            if dice_values.max() > 1:
                dice_values = dice_values / 100
            print(f"\n🎯 Best Dice Scores:")
            print(f"   Mean: {dice_values.mean():.3f}")
            print(f"   Median: {dice_values.median():.3f}")
            print(f"   Range: {dice_values.min():.3f} - {dice_values.max():.3f}")
    
    # Frameworks
    if 'framework' in df.columns:
        frameworks = df['framework'].dropna().value_counts()
        print("\n🛠️ Frameworks:")
        for fw, count in frameworks.head(5).items():
            print(f"   {fw}: {count}")
    
    # Exclusion reasons
    print("\n❌ Exclusion Reasons:")
    for reason, count in Counter(r.get('exclusion_reason', 'Unknown') for r in excluded).most_common():
        print(f"   {reason}: {count}")
    
    # Final PRISMA numbers
    print("\n" + "="*60)
    print("FINAL PRISMA FLOW")
    print("="*60)
    print(f"""
Records identified (Scopus + Semantic Scholar): 2,821
                    ↓
After ES filter (embeddings): 638
                    ↓
After AI screening (S2 - 3-model consensus): 161
                    ↓
Full-text retrieved: 63
                    ↓
After S3 full-text screening: {len(included)}
                    ↓
Studies included in synthesis: {len(included)}
""")
    
    # Create LaTeX table
    latex_table = OUTPUT_DIR / f"latex_summary_table_{timestamp}.tex"
    
    # Select key columns for LaTeX
    latex_cols = ['authors', 'year', 'architecture', 'organs_segmented', 'best_dice']
    df_latex = df[[c for c in latex_cols if c in df.columns]].copy()
    
    # Truncate long values
    if 'organs_segmented' in df_latex.columns:
        df_latex['organs_segmented'] = df_latex['organs_segmented'].apply(
            lambda x: str(x)[:50] + '...' if len(str(x)) > 50 else str(x)
        )
    if 'authors' in df_latex.columns:
        df_latex['authors'] = df_latex['authors'].apply(
            lambda x: str(x)[:30] if pd.notna(x) else ''
        )
    
    df_latex.to_latex(latex_table, index=False, escape=True)
    print(f"\nSaved LaTeX table: {latex_table}")
    
    return len(included), len(excluded)

if __name__ == "__main__":
    main()
