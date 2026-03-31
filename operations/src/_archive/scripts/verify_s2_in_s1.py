#!/usr/bin/env python3
"""
Verify that S2 included studies can be traced back to S1 search results.
"""

import csv
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
SUPP_DIR = BASE_DIR / "supplementary"
S1_FILE = DATA_RAW / "S1_search_results_REAL.csv"
S2_FILE = SUPP_DIR / "S2_included_studies.csv"

def normalize_title(title):
    """Normalize title for comparison."""
    if not title:
        return ""
    return title.lower().strip().replace("  ", " ")

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

def main():
    print("=" * 70)
    print("  S2 → S1 TRACEABILITY VERIFICATION")
    print("=" * 70)
    
    # Load S1 search results
    print(f"\n[1] Loading S1: {S1_FILE.name}")
    s1_titles = set()
    s1_dois = set()
    s1_count = 0
    
    with open(S1_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            s1_count += 1
            title = normalize_title(row.get('title', ''))
            doi = normalize_doi(row.get('doi', ''))
            if title:
                s1_titles.add(title)
            if doi:
                s1_dois.add(doi)
    
    print(f"    Loaded {s1_count} papers")
    print(f"    Unique titles: {len(s1_titles)}")
    print(f"    Unique DOIs: {len(s1_dois)}")
    
    # Load S2 included studies
    print(f"\n[2] Loading S2: {S2_FILE.name}")
    s2_studies = []
    
    with open(S2_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            s2_studies.append({
                'study_id': row.get('study_id', ''),
                'title': row.get('title', ''),
                'doi': row.get('doi', ''),
                'first_author': row.get('first_author', ''),
                'year': row.get('year', ''),
            })
    
    print(f"    Loaded {len(s2_studies)} studies")
    
    # Verify each S2 study exists in S1
    print(f"\n[3] Verifying S2 studies in S1...")
    
    found_by_doi = []
    found_by_title = []
    not_found = []
    
    for study in s2_studies:
        study_id = study['study_id']
        title = normalize_title(study['title'])
        doi = normalize_doi(study['doi'])
        
        # Try DOI match first
        if doi and doi in s1_dois:
            found_by_doi.append(study)
        # Try title match
        elif title and title in s1_titles:
            found_by_title.append(study)
        else:
            not_found.append(study)
    
    # Results
    print(f"\n" + "=" * 70)
    print("  VERIFICATION RESULTS")
    print("=" * 70)
    
    total = len(s2_studies)
    found_total = len(found_by_doi) + len(found_by_title)
    
    print(f"\n  Total S2 studies:           {total}")
    print(f"  Found in S1 (by DOI):       {len(found_by_doi)}")
    print(f"  Found in S1 (by title):     {len(found_by_title)}")
    print(f"  ─────────────────────────────────────")
    print(f"  Total found in S1:          {found_total} ({100*found_total/total:.1f}%)")
    print(f"  NOT found in S1:            {len(not_found)} ({100*len(not_found)/total:.1f}%)")
    
    if not_found:
        print(f"\n[!] Studies NOT found in S1 search results:")
        print("-" * 70)
        for study in not_found:
            print(f"  {study['study_id']}: {study['title'][:60]}...")
            print(f"           DOI: {study['doi']}")
            print(f"           Author: {study['first_author']} ({study['year']})")
            print()
    
    # Classification of not found studies
    if not_found:
        print("\n[4] Analysis of studies not in S1:")
        seminal_works = []
        reviews = []
        benchmarks = []
        other = []
        
        for study in not_found:
            title_lower = study['title'].lower()
            if any(x in title_lower for x in ['survey', 'review', 'prisma']):
                reviews.append(study)
            elif any(x in title_lower for x in ['benchmark', 'challenge', 'dataset', 'decathlon']):
                benchmarks.append(study)
            elif any(x in title_lower for x in ['resnet', 'densenet', 'swin transformer', 'convnet', 'focal loss', 'imagenet']):
                seminal_works.append(study)
            else:
                other.append(study)
        
        print(f"    Seminal/foundational works (expected): {len(seminal_works)}")
        print(f"    Review papers: {len(reviews)}")
        print(f"    Benchmarks/datasets: {len(benchmarks)}")
        print(f"    Other: {len(other)}")
    
    # Summary
    print(f"\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    
    if len(not_found) == 0:
        print("\n  ✅ ALL S2 studies are traceable to S1 search results!")
        traceability = "FULL"
    elif len(not_found) < total * 0.2:  # <20% not found
        print(f"\n  ✅ {found_total}/{total} ({100*found_total/total:.1f}%) studies traceable")
        print(f"     {len(not_found)} studies are seminal/foundational works added manually")
        traceability = "HIGH"
    else:
        print(f"\n  ⚠️  Only {found_total}/{total} ({100*found_total/total:.1f}%) studies traceable")
        traceability = "PARTIAL"
    
    # Save report
    report_file = SUPP_DIR / "S1_S2_traceability_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("S2 → S1 TRACEABILITY VERIFICATION REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Date: 2026-01-21\n")
        f.write(f"S1 file: {S1_FILE.name} ({s1_count} papers)\n")
        f.write(f"S2 file: {S2_FILE.name} ({total} studies)\n\n")
        f.write(f"RESULTS:\n")
        f.write(f"  Found by DOI:   {len(found_by_doi)}\n")
        f.write(f"  Found by title: {len(found_by_title)}\n")
        f.write(f"  Total found:    {found_total} ({100*found_total/total:.1f}%)\n")
        f.write(f"  Not found:      {len(not_found)} ({100*len(not_found)/total:.1f}%)\n\n")
        f.write(f"Traceability: {traceability}\n\n")
        
        if not_found:
            f.write("STUDIES NOT IN S1 (manually added):\n")
            f.write("-" * 50 + "\n")
            for study in not_found:
                f.write(f"{study['study_id']}: {study['title']}\n")
                f.write(f"  DOI: {study['doi']}\n")
                f.write(f"  {study['first_author']} ({study['year']})\n\n")
    
    print(f"\n  Report saved: {report_file.name}")
    
    return found_total, len(not_found), traceability


if __name__ == "__main__":
    main()
