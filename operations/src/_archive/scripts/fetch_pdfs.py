#!/usr/bin/env python3
"""
Fetch PDFs for included papers.
Attempts to download from:
1. arXiv (direct PDF)
2. DOI via Unpaywall API (open access)
3. PubMed Central
"""

import csv
import json
import os
import re
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO_ROOT = Path(__file__).parent.parent.parent
FINAL_RESULTS_DIR = REPO_ROOT / "data" / "processed" / "final_results"
PDF_DIR = REPO_ROOT / "data" / "pdfs"
OUT_DIR = REPO_ROOT / "data" / "processed" / "pdf_fetching"

# Your email for Unpaywall API (required)
EMAIL = "your-email@example.com"  # Change this!

MAX_WORKERS = 3  # Parallel downloads
DELAY_BETWEEN_REQUESTS = 1  # seconds


def find_latest_included_file():
    files = sorted(FINAL_RESULTS_DIR.glob("final_included_papers_*.csv"), reverse=True)
    if not files:
        raise SystemExit(f"No final_included_papers_*.csv found in {FINAL_RESULTS_DIR}")
    return files[0]


def extract_arxiv_id(paper_id):
    """Extract arXiv ID from paper_id."""
    # Patterns: http://arxiv.org/abs/1234.5678v1, arXiv:1234.5678
    patterns = [
        r'arxiv\.org/abs/(\d+\.\d+)(v\d+)?',
        r'arXiv:(\d+\.\d+)',
        r'^(\d{4}\.\d{4,5})(v\d+)?$'
    ]
    for pattern in patterns:
        match = re.search(pattern, paper_id, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_doi(paper_id):
    """Extract DOI from paper_id."""
    if paper_id.startswith('10.'):
        return paper_id
    match = re.search(r'(10\.\d{4,}/[^\s]+)', paper_id)
    if match:
        return match.group(1)
    return None


def download_file(url, dest_path, timeout=30):
    """Download a file from URL."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Academic Research Bot)'
        })
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            
            # Check if it's actually a PDF
            if not content.startswith(b'%PDF'):
                return False, "Not a PDF"
            
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_bytes(content)
            return True, "OK"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)[:50]


def fetch_from_arxiv(arxiv_id, dest_path):
    """Fetch PDF from arXiv."""
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    return download_file(url, dest_path)


def fetch_from_unpaywall(doi, dest_path):
    """Fetch open-access PDF via Unpaywall API."""
    try:
        api_url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
        req = urllib.request.Request(api_url, headers={
            'User-Agent': 'Mozilla/5.0 (Academic Research Bot)'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # Try best OA location first
        best_oa = data.get('best_oa_location')
        if best_oa and best_oa.get('url_for_pdf'):
            pdf_url = best_oa['url_for_pdf']
            return download_file(pdf_url, dest_path)
        
        # Try other OA locations
        for loc in data.get('oa_locations', []):
            if loc.get('url_for_pdf'):
                success, msg = download_file(loc['url_for_pdf'], dest_path)
                if success:
                    return success, msg
        
        return False, "No OA PDF found"
    except Exception as e:
        return False, str(e)[:50]


def fetch_paper(paper_id, title):
    """Try to fetch PDF for a paper."""
    # Create safe filename
    safe_name = re.sub(r'[^\w\-.]', '_', paper_id)[:100]
    dest_path = PDF_DIR / f"{safe_name}.pdf"
    
    if dest_path.exists():
        return paper_id, "already_exists", str(dest_path)
    
    # Try arXiv first
    arxiv_id = extract_arxiv_id(paper_id)
    if arxiv_id:
        success, msg = fetch_from_arxiv(arxiv_id, dest_path)
        if success:
            return paper_id, "arxiv", str(dest_path)
    
    # Try DOI via Unpaywall
    doi = extract_doi(paper_id)
    if doi:
        time.sleep(DELAY_BETWEEN_REQUESTS)  # Rate limiting
        success, msg = fetch_from_unpaywall(doi, dest_path)
        if success:
            return paper_id, "unpaywall", str(dest_path)
        return paper_id, f"failed: {msg}", None
    
    return paper_id, "no_identifier", None


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load included papers
    included_file = find_latest_included_file()
    papers = []
    with open(included_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)
    
    print(f"Total papers to fetch: {len(papers)}")
    print(f"Output directory: {PDF_DIR}")
    print()
    
    results = {
        "success": [],
        "already_exists": [],
        "failed": [],
        "no_identifier": []
    }
    
    # Fetch PDFs
    for i, paper in enumerate(papers):
        paper_id = paper['paper_id']
        title = paper.get('title', '')[:50]
        
        pid, status, path = fetch_paper(paper_id, title)
        
        if status == "arxiv" or status == "unpaywall":
            results["success"].append({"id": pid, "source": status, "path": path})
            print(f"[{i+1}/{len(papers)}] ✅ {pid[:50]} ({status})")
        elif status == "already_exists":
            results["already_exists"].append({"id": pid, "path": path})
            print(f"[{i+1}/{len(papers)}] ⏭️  {pid[:50]} (exists)")
        elif status == "no_identifier":
            results["no_identifier"].append({"id": pid})
            print(f"[{i+1}/{len(papers)}] ⚠️  {pid[:50]} (no DOI/arXiv)")
        else:
            results["failed"].append({"id": pid, "reason": status})
            print(f"[{i+1}/{len(papers)}] ❌ {pid[:50]} ({status})")
        
        time.sleep(0.5)  # Be nice to servers
    
    # Summary
    print("\n" + "=" * 60)
    print("PDF FETCHING SUMMARY")
    print("=" * 60)
    print(f"✅ Downloaded: {len(results['success'])}")
    print(f"⏭️  Already existed: {len(results['already_exists'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⚠️  No identifier: {len(results['no_identifier'])}")
    print(f"\nTotal available: {len(results['success']) + len(results['already_exists'])}/{len(papers)}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = OUT_DIR / f"pdf_fetch_results_{timestamp}.json"
    results_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(f"\nWrote: {results_path.name}")
    
    # Create paywalled list for manual access
    if results['failed'] or results['no_identifier']:
        paywall_path = OUT_DIR / f"paywalled_papers_{timestamp}.csv"
        with open(paywall_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["paper_id", "status", "notes"])
            for item in results['failed']:
                writer.writerow([item['id'], 'failed', item.get('reason', '')])
            for item in results['no_identifier']:
                writer.writerow([item['id'], 'no_identifier', 'Need manual lookup'])
        print(f"Wrote: {paywall_path.name}")


if __name__ == "__main__":
    main()
