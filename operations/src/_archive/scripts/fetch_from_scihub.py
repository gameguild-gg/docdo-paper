#!/usr/bin/env python3
"""
Download PDFs from Sci-Hub for paywalled papers.
"""

import csv
import re
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
PDF_DIR = REPO_ROOT / "data" / "pdfs"
PAYWALL_FILE = REPO_ROOT / "data" / "processed" / "pdf_fetching" / "papers_to_fetch_manually.csv"
OUT_DIR = REPO_ROOT / "data" / "processed" / "pdf_fetching"

SCIHUB_MIRROR = "https://www.sci-hub.ru"
DELAY = 2  # seconds between requests to be nice


def get_pdf_url_from_scihub(doi):
    """Fetch Sci-Hub page and extract PDF URL."""
    url = f"{SCIHUB_MIRROR}/{doi}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Pattern for sci-hub.ru: look for object data or download href with PDF path
        patterns = [
            r'<object[^>]+data\s*=\s*["\']([^"\']+\.pdf[^"\']*)["\']',  # <object data="/storage/.../file.pdf">
            r'href\s*=\s*["\']([^"\']+/download/[^"\']+\.pdf)["\']',     # download link
            r'fetch\(["\']([^"\']+\.pdf)["\']',                          # fetch('/storage/.../file.pdf')
            r'<embed[^>]+src=["\']([^"\']+\.pdf[^"\']*)["\']',
            r'<iframe[^>]+src=["\']([^"\']+\.pdf[^"\']*)["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                pdf_url = match.group(1)
                # Remove fragment
                if '#' in pdf_url:
                    pdf_url = pdf_url.split('#')[0]
                # Fix relative URLs
                if pdf_url.startswith('//'):
                    pdf_url = 'https:' + pdf_url
                elif pdf_url.startswith('/'):
                    pdf_url = SCIHUB_MIRROR + pdf_url
                elif not pdf_url.startswith('http'):
                    pdf_url = SCIHUB_MIRROR + '/' + pdf_url
                return pdf_url, None
        
        # Check if paper not found
        if 'article not found' in html.lower() or 'не найдена' in html.lower():
            return None, "not_found"
        
        return None, "no_pdf_link"
        
    except urllib.error.HTTPError as e:
        return None, f"http_{e.code}"
    except Exception as e:
        return None, str(e)[:50]


def download_pdf(url, dest_path):
    """Download PDF from URL."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=60) as response:
            content = response.read()
        
        # Verify it's a PDF
        if not content.startswith(b'%PDF'):
            return False, "not_a_pdf"
        
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(content)
        return True, f"{len(content)//1024}KB"
        
    except Exception as e:
        return False, str(e)[:50]


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load papers to fetch
    papers = []
    with open(PAYWALL_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['paper_id'].startswith('10.'):  # Only DOIs
                papers.append(row)
    
    print(f"Papers with DOIs to fetch: {len(papers)}")
    print(f"Using mirror: {SCIHUB_MIRROR}")
    print(f"Delay between requests: {DELAY}s")
    print()
    
    results = {"success": [], "not_found": [], "failed": []}
    
    for i, paper in enumerate(papers):
        doi = paper['paper_id']
        title = paper.get('title', '')[:40]
        
        # Check if already exists
        safe_name = re.sub(r'[^\w\-.]', '_', doi)[:80]
        dest_path = PDF_DIR / f"{safe_name}.pdf"
        
        if dest_path.exists():
            print(f"[{i+1}/{len(papers)}] ⏭️  {doi[:40]} (exists)")
            results["success"].append({"doi": doi, "status": "exists"})
            continue
        
        print(f"[{i+1}/{len(papers)}] 🔍 {doi[:40]}...", end=" ", flush=True)
        
        # Get PDF URL from Sci-Hub
        pdf_url, err = get_pdf_url_from_scihub(doi)
        
        if not pdf_url:
            print(f"❌ {err}")
            if err == "not_found":
                results["not_found"].append({"doi": doi})
            else:
                results["failed"].append({"doi": doi, "reason": err})
            time.sleep(1)
            continue
        
        # Download PDF
        success, msg = download_pdf(pdf_url, dest_path)
        
        if success:
            print(f"✅ ({msg})")
            results["success"].append({"doi": doi, "size": msg})
        else:
            print(f"❌ {msg}")
            results["failed"].append({"doi": doi, "reason": msg})
        
        time.sleep(DELAY)
    
    # Summary
    print("\n" + "=" * 60)
    print("SCI-HUB DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"✅ Downloaded: {len([r for r in results['success'] if r.get('size')])}")
    print(f"⏭️  Already existed: {len([r for r in results['success'] if r.get('status') == 'exists'])}")
    print(f"🚫 Not on Sci-Hub: {len(results['not_found'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    import json
    results_path = OUT_DIR / f"scihub_results_{timestamp}.json"
    results_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(f"\nWrote: {results_path.name}")


if __name__ == "__main__":
    main()
