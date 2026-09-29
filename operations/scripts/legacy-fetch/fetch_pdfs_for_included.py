#!/usr/bin/env python3
"""
Fetch PDFs for the 161 included papers from the final screening.

Strategy:
1. Try Unpaywall API (free, legal access to open-access versions)
2. Try arXiv direct download for arXiv papers
3. Try Semantic Scholar/DOI redirects
4. Generate manual fetch list for paywalled papers

Output:
- data/pdfs/ - Downloaded PDFs
- data/processed/pdf_fetching/fetch_results.csv - Status of each paper
- data/processed/pdf_fetching/papers_to_fetch_manually.csv - Paywalled papers
- data/processed/pdf_fetching/papers_to_fetch_manually.html - Clickable links
"""

import csv
import json
import re
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).parent.parent.parent
FINAL_RESULTS = REPO_ROOT / "data" / "processed" / "final_results"
PDF_DIR = REPO_ROOT / "data" / "pdfs"
OUT_DIR = REPO_ROOT / "data" / "processed" / "pdf_fetching"

UNPAYWALL_EMAIL = "your-email@example.com"  # Replace with your email for Unpaywall API
DELAY = 1.0  # seconds between requests


def find_latest_included_file():
    """Find the most recent final_included_papers_*.csv file."""
    files = sorted(FINAL_RESULTS.glob("final_included_papers_*.csv"), reverse=True)
    if not files:
        raise SystemExit(f"No final_included_papers_*.csv found in {FINAL_RESULTS}")
    return files[0]


def sanitize_filename(paper_id: str) -> str:
    """Convert paper ID to safe filename."""
    # Replace special chars
    safe = paper_id.replace("/", "_").replace(":", "_").replace("?", "_")
    safe = re.sub(r'[<>"|*\\]', "_", safe)
    # Truncate if too long
    if len(safe) > 100:
        safe = safe[:100]
    return safe + ".pdf"


def try_unpaywall(doi: str) -> Tuple[Optional[str], str]:
    """Try to get PDF URL from Unpaywall API."""
    if not doi.startswith("10."):
        return None, "not_a_doi"
    
    url = f"https://api.unpaywall.org/v2/{doi}?email={UNPAYWALL_EMAIL}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (systematic-review-tool)'
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # Check for open access PDF
        if data.get("is_oa"):
            best_loc = data.get("best_oa_location", {})
            pdf_url = best_loc.get("url_for_pdf")
            if pdf_url:
                return pdf_url, "unpaywall_oa"
            
            # Try landing page as fallback
            landing = best_loc.get("url_for_landing_page")
            if landing:
                return landing, "unpaywall_landing"
        
        return None, "unpaywall_not_oa"
        
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, "unpaywall_not_found"
        return None, f"unpaywall_http_{e.code}"
    except Exception as e:
        return None, f"unpaywall_error"


def try_arxiv(paper_id: str) -> Tuple[Optional[str], str]:
    """Try to get PDF from arXiv."""
    # Extract arXiv ID
    arxiv_match = re.search(r'arxiv[:\.]?(\d{4}\.\d{4,5})(v\d+)?', paper_id.lower())
    if not arxiv_match:
        arxiv_match = re.search(r'(\d{4}\.\d{4,5})(v\d+)?', paper_id)
    
    if arxiv_match:
        arxiv_id = arxiv_match.group(1)
        version = arxiv_match.group(2) or ""
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}{version}.pdf"
        return pdf_url, "arxiv"
    
    return None, "not_arxiv"


def try_pmc(doi: str) -> Tuple[Optional[str], str]:
    """Try to find PMC free full text."""
    if not doi.startswith("10."):
        return None, "not_a_doi"
    
    # Use NCBI ID converter
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={doi}&format=json"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (systematic-review-tool)'
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        records = data.get("records", [])
        if records and records[0].get("pmcid"):
            pmcid = records[0]["pmcid"]
            pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"
            return pdf_url, "pmc"
        
        return None, "pmc_not_found"
        
    except Exception as e:
        return None, "pmc_error"


def download_pdf(url: str, dest_path: Path) -> Tuple[bool, str]:
    """Download PDF from URL."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=60) as response:
            content = response.read()
        
        # Verify it's a PDF
        if not content.startswith(b'%PDF'):
            # Maybe HTML redirect
            if b'<html' in content[:1000].lower():
                return False, "html_redirect"
            return False, "not_a_pdf"
        
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(content)
        return True, f"{len(content)//1024}KB"
        
    except urllib.error.HTTPError as e:
        return False, f"http_{e.code}"
    except Exception as e:
        return False, str(e)[:30]


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load included papers
    input_file = find_latest_included_file()
    print(f"Loading papers from: {input_file.name}")
    
    papers = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)
    
    print(f"Total papers to fetch: {len(papers)}")
    
    results = []
    downloaded = 0
    manual_fetch = []
    
    for i, paper in enumerate(papers, 1):
        paper_id = paper.get('paper_id', '')
        title = paper.get('title', '')[:80]
        
        print(f"\n[{i}/{len(papers)}] {paper_id}")
        print(f"  Title: {title}...")
        
        pdf_path = PDF_DIR / sanitize_filename(paper_id)
        
        # Skip if already downloaded
        if pdf_path.exists():
            print(f"  ✓ Already downloaded")
            results.append({
                'paper_id': paper_id,
                'title': title,
                'status': 'already_exists',
                'source': 'cache',
                'path': str(pdf_path.name)
            })
            downloaded += 1
            continue
        
        # Try different sources
        pdf_url = None
        source = None
        
        # 1. Try arXiv first (fastest, most reliable)
        url, src = try_arxiv(paper_id)
        if url:
            pdf_url, source = url, src
            print(f"  → Trying arXiv: {url[:60]}...")
        
        # 2. Try Unpaywall
        if not pdf_url and paper_id.startswith("10."):
            time.sleep(DELAY)
            url, src = try_unpaywall(paper_id)
            if url:
                pdf_url, source = url, src
                print(f"  → Trying Unpaywall ({src}): {url[:60]}...")
        
        # 3. Try PMC
        if not pdf_url and paper_id.startswith("10."):
            time.sleep(DELAY)
            url, src = try_pmc(paper_id)
            if url:
                pdf_url, source = url, src
                print(f"  → Trying PMC: {url[:60]}...")
        
        # Download if we have a URL
        if pdf_url:
            success, msg = download_pdf(pdf_url, pdf_path)
            if success:
                print(f"  ✓ Downloaded ({msg})")
                results.append({
                    'paper_id': paper_id,
                    'title': title,
                    'status': 'downloaded',
                    'source': source,
                    'path': str(pdf_path.name)
                })
                downloaded += 1
                continue
            else:
                print(f"  ✗ Download failed: {msg}")
        
        # Add to manual fetch list
        print(f"  → Need manual fetch")
        manual_fetch.append({
            'paper_id': paper_id,
            'title': paper.get('title', ''),
            'abstract_snippet': paper.get('abstract_snippet', '')[:200]
        })
        results.append({
            'paper_id': paper_id,
            'title': title,
            'status': 'manual_needed',
            'source': 'none',
            'path': ''
        })
        
        time.sleep(DELAY)
    
    # Write results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Full results
    results_path = OUT_DIR / f"fetch_results_{timestamp}.csv"
    with open(results_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['paper_id', 'title', 'status', 'source', 'path'])
        writer.writeheader()
        writer.writerows(results)
    
    # Manual fetch list (CSV)
    manual_csv = OUT_DIR / "papers_to_fetch_manually.csv"
    with open(manual_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['paper_id', 'title', 'abstract_snippet'])
        writer.writeheader()
        writer.writerows(manual_fetch)
    
    # Manual fetch list (HTML with clickable links)
    manual_html = OUT_DIR / "papers_to_fetch_manually.html"
    with open(manual_html, 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Papers to Fetch Manually</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        a { color: #0066cc; }
        .abstract { font-size: 0.9em; color: #666; max-width: 400px; }
    </style>
</head>
<body>
    <h1>Papers to Fetch Manually</h1>
    <p>Total: """ + str(len(manual_fetch)) + """ papers</p>
    <table>
        <tr>
            <th>#</th>
            <th>Paper ID / Links</th>
            <th>Title</th>
            <th>Abstract</th>
        </tr>
""")
        for i, paper in enumerate(manual_fetch, 1):
            pid = paper['paper_id']
            title = paper['title']
            abstract = paper['abstract_snippet']
            
            # Generate links
            links = []
            if pid.startswith("10."):
                links.append(f'<a href="https://doi.org/{pid}" target="_blank">DOI</a>')
                links.append(f'<a href="https://scholar.google.com/scholar?q={pid}" target="_blank">Scholar</a>')
            elif "arxiv" in pid.lower():
                arxiv_id = re.search(r'(\d{4}\.\d{4,5})', pid)
                if arxiv_id:
                    links.append(f'<a href="https://arxiv.org/abs/{arxiv_id.group(1)}" target="_blank">arXiv</a>')
            links.append(f'<a href="https://www.google.com/search?q={urllib.parse.quote(title)}" target="_blank">Google</a>')
            
            f.write(f"""        <tr>
            <td>{i}</td>
            <td>{pid}<br>{' | '.join(links)}</td>
            <td>{title}</td>
            <td class="abstract">{abstract}...</td>
        </tr>
""")
        f.write("""    </table>
</body>
</html>
""")
    
    # Summary
    print("\n" + "=" * 60)
    print("PDF FETCHING COMPLETE")
    print("=" * 60)
    print(f"Total papers: {len(papers)}")
    print(f"Downloaded: {downloaded}")
    print(f"Need manual fetch: {len(manual_fetch)}")
    print(f"\nOutput files:")
    print(f"  {results_path.name}")
    print(f"  {manual_csv.name}")
    print(f"  {manual_html.name}")
    print(f"\nPDFs saved to: {PDF_DIR}")


if __name__ == "__main__":
    import urllib.parse
    main()
