"""
verify_screening.py - Verify AI screening consensus calculations

This script validates the consensus voting logic used in the AI-assisted
screening protocol. It reads the screening decisions and verifies that
the consensus calculations are correct.

Usage:
    python verify_screening.py --input ../S5_screening_decisions.csv
"""

import argparse
import pandas as pd
import numpy as np
from collections import Counter


def load_screening_data(filepath: str) -> pd.DataFrame:
    """Load screening decisions from CSV file."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} screening records from {filepath}")
    return df


def verify_consensus(row: pd.Series) -> dict:
    """Verify consensus calculation for a single record."""
    decisions = [row['run1_decision'], row['run2_decision'], row['run3_decision']]
    counts = Counter(decisions)
    
    # Calculate expected consensus
    if counts['INCLUDE'] >= 2:
        expected_decision = 'INCLUDE'
    elif counts['EXCLUDE'] >= 2:
        expected_decision = 'EXCLUDE'
    else:
        expected_decision = 'UNCERTAIN'
    
    # Determine expected consensus type
    if decisions[0] == decisions[1] == decisions[2]:
        expected_type = 'unanimous'
    else:
        expected_type = 'majority'
    
    # Compare with recorded values
    decision_match = (expected_decision == row['consensus_decision'])
    type_match = (expected_type == row['consensus_type'])
    
    return {
        'record_id': row['record_id'],
        'expected_decision': expected_decision,
        'recorded_decision': row['consensus_decision'],
        'decision_match': decision_match,
        'expected_type': expected_type,
        'recorded_type': row['consensus_type'],
        'type_match': type_match,
        'votes': dict(counts)
    }


def compute_kappa(decisions_ai: list, decisions_human: list) -> float:
    """
    Compute Cohen's Kappa coefficient.
    
    Args:
        decisions_ai: List of AI decisions (INCLUDE/EXCLUDE)
        decisions_human: List of human decisions (INCLUDE/EXCLUDE)
    
    Returns:
        Cohen's Kappa coefficient
    """
    assert len(decisions_ai) == len(decisions_human)
    n = len(decisions_ai)
    
    # Build confusion matrix
    tp = sum(1 for a, h in zip(decisions_ai, decisions_human) 
             if a == 'INCLUDE' and h == 'INCLUDE')
    tn = sum(1 for a, h in zip(decisions_ai, decisions_human) 
             if a == 'EXCLUDE' and h == 'EXCLUDE')
    fp = sum(1 for a, h in zip(decisions_ai, decisions_human) 
             if a == 'INCLUDE' and h == 'EXCLUDE')
    fn = sum(1 for a, h in zip(decisions_ai, decisions_human) 
             if a == 'EXCLUDE' and h == 'INCLUDE')
    
    # Observed agreement
    po = (tp + tn) / n
    
    # Expected agreement
    pe = ((tp + fp) * (tp + fn) + (tn + fn) * (tn + fp)) / (n * n)
    
    # Cohen's Kappa
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    
    return kappa


def verify_all_consensus(df: pd.DataFrame) -> dict:
    """Verify consensus for all records."""
    results = []
    for _, row in df.iterrows():
        result = verify_consensus(row)
        results.append(result)
    
    # Summarize results
    decision_matches = sum(r['decision_match'] for r in results)
    type_matches = sum(r['type_match'] for r in results)
    total = len(results)
    
    summary = {
        'total_records': total,
        'decision_accuracy': decision_matches / total,
        'type_accuracy': type_matches / total,
        'mismatches': [r for r in results if not r['decision_match'] or not r['type_match']]
    }
    
    return summary


def print_summary(summary: dict):
    """Print verification summary."""
    print("\n" + "="*60)
    print("SCREENING VERIFICATION SUMMARY")
    print("="*60)
    print(f"Total records verified: {summary['total_records']}")
    print(f"Decision accuracy: {summary['decision_accuracy']:.2%}")
    print(f"Consensus type accuracy: {summary['type_accuracy']:.2%}")
    
    if summary['mismatches']:
        print(f"\nMismatches found: {len(summary['mismatches'])}")
        for m in summary['mismatches']:
            print(f"  Record {m['record_id']}: "
                  f"expected {m['expected_decision']}/{m['expected_type']}, "
                  f"got {m['recorded_decision']}/{m['recorded_type']}")
    else:
        print("\n✓ All consensus calculations verified successfully!")


def main():
    parser = argparse.ArgumentParser(
        description='Verify AI screening consensus calculations'
    )
    parser.add_argument(
        '--input', '-i',
        default='../S5_screening_decisions.csv',
        help='Path to screening decisions CSV file'
    )
    args = parser.parse_args()
    
    # Load data
    df = load_screening_data(args.input)
    
    # Verify consensus calculations
    summary = verify_all_consensus(df)
    
    # Print results
    print_summary(summary)
    
    # Compute agreement statistics
    print("\n" + "="*60)
    print("AGREEMENT STATISTICS")
    print("="*60)
    
    include_count = (df['consensus_decision'] == 'INCLUDE').sum()
    exclude_count = (df['consensus_decision'] == 'EXCLUDE').sum()
    unanimous_count = (df['consensus_type'] == 'unanimous').sum()
    majority_count = (df['consensus_type'] == 'majority').sum()
    
    print(f"INCLUDE decisions: {include_count} ({include_count/len(df):.1%})")
    print(f"EXCLUDE decisions: {exclude_count} ({exclude_count/len(df):.1%})")
    print(f"Unanimous consensus: {unanimous_count} ({unanimous_count/len(df):.1%})")
    print(f"Majority consensus: {majority_count} ({majority_count/len(df):.1%})")


if __name__ == '__main__':
    main()
