#!/usr/bin/env python3
"""
Deduplicate S1 search results across databases.

Input:  data/raw/S1_search_results_REAL.csv
Output: data/interim/S1_search_results_deduplicated.csv

Deduplication strategy:
1. Exact DOI match (highest priority)
2. Normalized title match (case-insensitive, whitespace-normalized)

When duplicates found, keep the record with most complete metadata.
"""

import csv
import re
from pathlib import Path
from collections import defaultdict

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
INPUT_FILE = BASE_DIR / "data" / "raw" / "S1_search_results_REAL.csv"
OUTPUT_FILE = BASE_DIR / "data" / "interim" / "S1_search_results_deduplicated.csv"


def normalize_title(title):
    """Normalize title for comparison."""
    if not title:
        return ""
    # Lowercase, collapse whitespace, remove punctuation
    title = title.lower().strip()
    title = re.sub(r'\s+', ' ', title)
    title = re.sub(r'[^\w\s]', '', title)
    return title


def normalize_doi(doi):
    """Normalize DOI for comparison."""
    if not doi:
        return ""
    doi = doi.lower().strip()
    # Remove common prefixes
    for prefix in ["https://doi.org/", "http://doi.org/", "doi:", "doi.org/"]:
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
    return doi


def completeness_score(row):
    """Score record completeness (higher = more complete)."""
    score = 0
    if row.get('doi'):
        score += 3
    if row.get('abstract_snippet') and len(row['abstract_snippet']) > 100:
        score += 2
    if row.get('authors'):
        score += 1
    if row.get('year'):
        score += 1
    if row.get('journal_conference'):
        score += 1
    return score


def main():
    print("=" * 70)
    print("  S1 DEDUPLICATION")
    print("  Input:  data/raw/S1_search_results_REAL.csv")
    print("  Output: data/interim/S1_search_results_deduplicated.csv")
    print("=" * 70)
    
    # Load all records
    print(f"\n[1] Loading {INPUT_FILE.name}...")
    records = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            records.append(row)
    
    print(f"    Loaded {len(records)} records")
    
    # Count by database
    db_counts = defaultdict(int)
    for r in records:
        db_counts[r.get('database', 'Unknown')] += 1
    
    print("\n    By database (before dedup):")
    for db, count in sorted(db_counts.items()):
        print(f"      {db}: {count}")
    
    # Build indexes
    print(f"\n[2] Building deduplication indexes...")
    
    doi_index = defaultdict(list)  # doi -> list of record indices
    title_index = defaultdict(list)  # normalized_title -> list of record indices
    
    for i, row in enumerate(records):
        doi = normalize_doi(row.get('doi', ''))
        title = normalize_title(row.get('title', ''))
        
        if doi:
            doi_index[doi].append(i)
        if title:
            title_index[title].append(i)
    
    # Find duplicates
    print(f"\n[3] Finding duplicates...")
    
    to_remove = set()
    doi_dups = 0
    title_dups = 0
    
    # DOI-based deduplication
    for doi, indices in doi_index.items():
        if len(indices) > 1:
            # Keep the most complete record
            best_idx = max(indices, key=lambda i: completeness_score(records[i]))
            for idx in indices:
                if idx != best_idx:
                    to_remove.add(idx)
                    doi_dups += 1
    
    # Title-based deduplication (for records without DOI matches)
    for title, indices in title_index.items():
        if len(indices) > 1:
            # Filter out already-removed records
            remaining = [i for i in indices if i not in to_remove]
            if len(remaining) > 1:
                # Keep the most complete record
                best_idx = max(remaining, key=lambda i: completeness_score(records[i]))
                for idx in remaining:
                    if idx != best_idx:
                        to_remove.add(idx)
                        title_dups += 1
    
    print(f"    DOI duplicates: {doi_dups}")
    print(f"    Title duplicates: {title_dups}")
    print(f"    Total to remove: {len(to_remove)}")
    
    # Filter and renumber
    print(f"\n[4] Writing deduplicated file...")
    
    unique_records = [r for i, r in enumerate(records) if i not in to_remove]
    
    # Renumber IDs
    for i, row in enumerate(unique_records, 1):
        row['id'] = f"R{i:04d}"
    
    # Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_records)
    
    # Final stats
    db_counts_after = defaultdict(int)
    for r in unique_records:
        db_counts_after[r.get('database', 'Unknown')] += 1
    
    print(f"\n" + "=" * 70)
    print("  DEDUPLICATION RESULTS")
    print("=" * 70)
    print(f"\n  Before: {len(records)} records")
    print(f"  After:  {len(unique_records)} unique records")
    print(f"  Removed: {len(to_remove)} duplicates ({100*len(to_remove)/len(records):.1f}%)")
    
    print("\n  By database (after dedup):")
    for db in sorted(db_counts.keys()):
        before = db_counts[db]
        after = db_counts_after.get(db, 0)
        removed = before - after
        print(f"    {db}: {before} → {after} (-{removed})")
    
    print(f"\n  Output: {OUTPUT_FILE}")
    print("=" * 70)
    
    return len(unique_records), len(to_remove)


if __name__ == "__main__":
    main()
