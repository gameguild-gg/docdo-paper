#!/usr/bin/env python3
"""
Download PDFs from Open Access publishers (MDPI, Frontiers, BMC).
"""

import csv
import re
import time
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urljoin

PDF_DIR = Path(__file__).parent.parent.parent / "data" / "pdfs"
PAYWALL_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "pdf_fetching" / "papers_to_fetch_manually.csv"


def main():
    papers = []
    with open(PAYWALL_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)

    # Find open access papers
    oa_papers = []
    for p in papers:
        pid = p['paper_id']
        if pid.startswith('10.3390') or pid.startswith('10.3389') or pid.startswith('10.1186'):
            oa_papers.append(p)

    print(f'Found {len(oa_papers)} Open Access papers to try')
    print()

    downloaded = 0
    for i, paper in enumerate(oa_papers, 1):
        doi = paper['paper_id']
        
        safe_name = re.sub(r'[^\w\-.]', '_', doi)[:80] + '.pdf'
        dest_path = PDF_DIR / safe_name
        
        if dest_path.exists():
            print(f'[{i}] SKIP {doi} (exists)')
            downloaded += 1
            continue
        
        print(f'[{i}] Trying {doi}...', end=' ', flush=True)
        
        try:
            # Follow DOI to get landing page
            req = urllib.request.Request(f'https://doi.org/{doi}', headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/pdf,text/html'
            })
            with urllib.request.urlopen(req, timeout=30) as response:
                final_url = response.url
                content_type = response.headers.get('Content-Type', '')
                
                if 'pdf' in content_type.lower():
                    content = response.read()
                    if content.startswith(b'%PDF'):
                        dest_path.write_bytes(content)
                        print(f'OK direct ({len(content)//1024}KB)')
                        downloaded += 1
                        continue
                
                html = response.read().decode('utf-8', errors='ignore')
            
            # Look for PDF link in HTML
            pdf_patterns = [
                r'href=["\']([^"\']+/pdf/[^"\']+\.pdf)["\']',
                r'href=["\']([^"\']+/article/[^"\']+/pdf[^"\']*)["\'?]',
                r'<a[^>]+href=["\']([^"\']+\.pdf)["\'][^>]*>[^<]*PDF',
                r'content=["\']([^"\']+\.pdf)["\']',
            ]
            
            found = False
            for pattern in pdf_patterns:
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    pdf_url = match.group(1)
                    if not pdf_url.startswith('http'):
                        pdf_url = urljoin(final_url, pdf_url)
                    
                    req2 = urllib.request.Request(pdf_url, headers={
                        'User-Agent': 'Mozilla/5.0'
                    })
                    with urllib.request.urlopen(req2, timeout=60) as resp2:
                        content = resp2.read()
                        if content.startswith(b'%PDF'):
                            dest_path.write_bytes(content)
                            print(f'OK ({len(content)//1024}KB)')
                            downloaded += 1
                            found = True
                            break
            
            if not found:
                print('FAIL no PDF link found')
                
        except Exception as e:
            print(f'FAIL {str(e)[:40]}')
        
        time.sleep(1)

    print(f'\nDownloaded: {downloaded}/{len(oa_papers)} OA papers')


if __name__ == "__main__":
    main()
