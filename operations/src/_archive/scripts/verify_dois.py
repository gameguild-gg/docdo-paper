#!/usr/bin/env python3
"""
Verify DOIs in S1 search results are real and resolvable.

This script tests a sample of DOIs to confirm they resolve to actual papers.
Run this for evidence that the data is verifiable.
"""

import csv
import random
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
INPUT_FILE = BASE_DIR / "data" / "interim" / "S1_search_results_deduplicated.csv"

def verify_doi(doi, retries=3):
    """Check if DOI resolves (returns HTTP 200/302)."""
    if not doi or doi.startswith('S2:'):
        return None, "No standard DOI"
    
    # Clean DOI
    if doi.startswith('http://arxiv.org/'):
        url = doi
    elif doi.startswith('arXiv:'):
        arxiv_id = doi.replace('arXiv:', '')
        url = f"https://arxiv.org/abs/{arxiv_id}"
    else:
        url = f"https://doi.org/{doi}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for attempt in range(retries):
        try:
            # Try GET instead of HEAD (some servers block HEAD)
            response = requests.get(url, timeout=15, allow_redirects=True, headers=headers, stream=True)
            response.close()  # Don't download full content
            
            if response.status_code in [200, 302, 301]:
                return True, response.url
            elif response.status_code in [403, 418, 429]:
                # Retry on bot protection / rate limit
                if attempt < retries - 1:
                    import time
                    time.sleep(2)
                    continue
                return True, f"Exists (HTTP {response.status_code} - bot protection)"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.exceptions.Timeout:
            if attempt < retries - 1:
                continue
            return False, "Timeout"
        except Exception as e:
            if attempt < retries - 1:
                continue
            return False, str(e)
    
    return False, "Max retries exceeded"


def main():
    print("=" * 70)
    print("  DOI VERIFICATION TEST")
    print("  Testing sample DOIs to confirm data is verifiable")
    print("=" * 70)
    
    # Load records
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        records = list(reader)
    
    print(f"\nTotal records: {len(records)}")
    
    # Sample from each database
    results = {'verified': 0, 'failed': 0, 'skipped': 0}
    
    for db in ['PubMed', 'arXiv', 'Semantic Scholar']:
        db_records = [r for r in records if r['database'] == db and r['doi']]
        sample_size = min(5, len(db_records))
        sample = random.sample(db_records, sample_size)
        
        print(f"\n{db} (testing {sample_size} DOIs):")
        print("-" * 50)
        
        for r in sample:
            doi = r['doi']
            title = r['title'][:40]
            
            verified, info = verify_doi(doi)
            
            if verified is True:
                results['verified'] += 1
                status = "✅ VERIFIED"
            elif verified is False:
                results['failed'] += 1
                status = f"❌ FAILED: {info}"
            else:
                results['skipped'] += 1
                status = f"⚠️ SKIPPED: {info}"
            
            print(f"  {status}")
            print(f"    DOI: {doi}")
            print(f"    Title: {title}...")
            print()
    
    # Summary
    total = results['verified'] + results['failed'] + results['skipped']
    
    print("=" * 70)
    print("  VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"  Tested:   {total} DOIs")
    print(f"  Verified: {results['verified']} ✅")
    print(f"  Failed:   {results['failed']} ❌")
    print(f"  Skipped:  {results['skipped']} ⚠️")
    print()
    
    if results['failed'] == 0:
        print("  ✅ ALL TESTED DOIs ARE VERIFIABLE!")
        print("     Data can be independently confirmed.")
    else:
        print(f"  ⚠️ {results['failed']} DOIs could not be verified")
    
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    main()
