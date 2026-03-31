"""
compute_statistics.py - Compute descriptive statistics from extracted data

This script computes summary statistics from the included studies data
and generates tables for the survey paper.

Usage:
    python compute_statistics.py --input ../S2_included_studies.csv
"""

import argparse
import pandas as pd
import numpy as np
from collections import Counter


def load_studies_data(filepath: str) -> pd.DataFrame:
    """Load included studies from CSV file."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} included studies from {filepath}")
    return df


def compute_year_distribution(df: pd.DataFrame) -> dict:
    """Compute distribution of studies by year."""
    year_counts = df['year'].value_counts().sort_index()
    return year_counts.to_dict()


def compute_architecture_distribution(df: pd.DataFrame) -> dict:
    """Compute distribution of studies by architecture type."""
    arch_counts = df['architecture_type'].value_counts()
    return arch_counts.to_dict()


def compute_study_type_distribution(df: pd.DataFrame) -> dict:
    """Compute distribution by study type."""
    type_counts = df['study_type'].value_counts()
    return type_counts.to_dict()


def compute_performance_statistics(df: pd.DataFrame) -> dict:
    """Compute performance metric statistics."""
    # Filter to method papers with reported Dice
    methods_df = df[df['study_type'] == 'method'].copy()
    methods_df['dice_reported'] = pd.to_numeric(
        methods_df['dice_reported'], errors='coerce'
    )
    methods_df['hd95_reported'] = pd.to_numeric(
        methods_df['hd95_reported'], errors='coerce'
    )
    
    dice_values = methods_df['dice_reported'].dropna()
    hd95_values = methods_df['hd95_reported'].dropna()
    
    stats = {
        'dice': {
            'count': len(dice_values),
            'mean': dice_values.mean(),
            'std': dice_values.std(),
            'min': dice_values.min(),
            'max': dice_values.max(),
            'median': dice_values.median()
        },
        'hd95': {
            'count': len(hd95_values),
            'mean': hd95_values.mean(),
            'std': hd95_values.std(),
            'min': hd95_values.min(),
            'max': hd95_values.max(),
            'median': hd95_values.median()
        }
    }
    
    return stats


def compute_organ_statistics(df: pd.DataFrame) -> dict:
    """Compute statistics about organ coverage."""
    organ_lists = df['organ_focus'].dropna()
    
    # Count individual organs
    all_organs = []
    for organs in organ_lists:
        if pd.notna(organs):
            all_organs.extend([o.strip() for o in str(organs).split(';')])
    
    organ_counts = Counter(all_organs)
    
    return {
        'unique_organs': len(organ_counts),
        'top_organs': organ_counts.most_common(10),
        'multi_organ_studies': sum(1 for o in organ_lists if ';' in str(o))
    }


def compute_code_availability(df: pd.DataFrame) -> dict:
    """Compute code availability statistics."""
    methods_df = df[df['study_type'] == 'method']
    
    code_available = (methods_df['code_available'] == 'yes').sum()
    total_methods = len(methods_df)
    
    return {
        'code_available': code_available,
        'total_methods': total_methods,
        'availability_rate': code_available / total_methods if total_methods > 0 else 0
    }


def print_statistics(stats: dict):
    """Print all statistics."""
    print("\n" + "="*60)
    print("INCLUDED STUDIES STATISTICS")
    print("="*60)
    
    print("\n--- Year Distribution ---")
    for year, count in sorted(stats['years'].items()):
        print(f"  {year}: {count}")
    
    print("\n--- Architecture Distribution ---")
    for arch, count in stats['architectures'].items():
        print(f"  {arch}: {count}")
    
    print("\n--- Study Type Distribution ---")
    for stype, count in stats['study_types'].items():
        print(f"  {stype}: {count}")
    
    print("\n--- Performance Statistics ---")
    dice = stats['performance']['dice']
    print(f"  Dice Score (n={dice['count']}):")
    print(f"    Mean ± Std: {dice['mean']:.3f} ± {dice['std']:.3f}")
    print(f"    Range: [{dice['min']:.3f}, {dice['max']:.3f}]")
    print(f"    Median: {dice['median']:.3f}")
    
    hd95 = stats['performance']['hd95']
    print(f"  HD95 (n={hd95['count']}):")
    print(f"    Mean ± Std: {hd95['mean']:.2f} ± {hd95['std']:.2f} mm")
    print(f"    Range: [{hd95['min']:.2f}, {hd95['max']:.2f}] mm")
    print(f"    Median: {hd95['median']:.2f} mm")
    
    print("\n--- Organ Statistics ---")
    print(f"  Unique organs studied: {stats['organs']['unique_organs']}")
    print(f"  Multi-organ studies: {stats['organs']['multi_organ_studies']}")
    print("  Top 10 organs:")
    for organ, count in stats['organs']['top_organs']:
        print(f"    {organ}: {count}")
    
    print("\n--- Code Availability ---")
    code = stats['code_availability']
    print(f"  Methods with code: {code['code_available']}/{code['total_methods']} "
          f"({code['availability_rate']:.1%})")


def export_latex_tables(stats: dict, output_dir: str):
    """Export statistics as LaTeX tables."""
    
    # Year distribution table
    latex_years = "\\begin{tabular}{lr}\n\\toprule\nYear & Count \\\\\n\\midrule\n"
    for year, count in sorted(stats['years'].items()):
        latex_years += f"{year} & {count} \\\\\n"
    latex_years += "\\bottomrule\n\\end{tabular}"
    
    with open(f"{output_dir}/year_distribution.tex", 'w') as f:
        f.write(latex_years)
    
    print(f"\nLaTeX tables exported to {output_dir}/")


def main():
    parser = argparse.ArgumentParser(
        description='Compute descriptive statistics from included studies'
    )
    parser.add_argument(
        '--input', '-i',
        default='../S2_included_studies.csv',
        help='Path to included studies CSV file'
    )
    parser.add_argument(
        '--output', '-o',
        default='./output',
        help='Output directory for tables'
    )
    args = parser.parse_args()
    
    # Load data
    df = load_studies_data(args.input)
    
    # Compute all statistics
    stats = {
        'years': compute_year_distribution(df),
        'architectures': compute_architecture_distribution(df),
        'study_types': compute_study_type_distribution(df),
        'performance': compute_performance_statistics(df),
        'organs': compute_organ_statistics(df),
        'code_availability': compute_code_availability(df)
    }
    
    # Print results
    print_statistics(stats)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total included studies: {len(df)}")
    print(f"Year range: {min(stats['years'].keys())}-{max(stats['years'].keys())}")
    print(f"Architecture families: {len(stats['architectures'])}")


if __name__ == '__main__':
    main()
