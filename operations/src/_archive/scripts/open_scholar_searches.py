#!/usr/bin/env python3
"""
Open Google Scholar searches in browser for manual PDF downloading.
Google Scholar blocks automated scraping, so this opens searches in your browser.
"""

import pandas as pd
import webbrowser
import urllib.parse
import time
import os
from pathlib import Path

# Paths
MISSING_FILE = Path("data/processed/pdf_fetching/papers_to_fetch_manually.csv")
PDF_DIR = Path("data/pdfs")

def get_missing_papers():
    """Load papers that still need PDFs."""
    if not MISSING_FILE.exists():
        print(f"Missing file not found: {MISSING_FILE}")
        return pd.DataFrame()
    
    df = pd.read_csv(MISSING_FILE)
    
    # Check which ones we already have
    existing_pdfs = set()
    if PDF_DIR.exists():
        for f in PDF_DIR.glob("*.pdf"):
            # Extract paper_id from filename
            paper_id = f.stem.split("_")[0] if "_" in f.stem else f.stem
            existing_pdfs.add(paper_id)
    
    # Filter out ones we already have
    df['paper_id_str'] = df['paper_id'].astype(str)
    df = df[~df['paper_id_str'].isin(existing_pdfs)]
    
    return df

def create_scholar_url(title):
    """Create Google Scholar search URL for a paper title."""
    # Clean the title
    title_clean = title.replace('"', '').replace("'", "")
    query = urllib.parse.quote(f'"{title_clean}"')
    return f"https://scholar.google.com/scholar?q={query}"

def open_in_batches(df, batch_size=5, delay_between_batches=2):
    """Open Scholar searches in batches."""
    total = len(df)
    
    print(f"\nTotal papers to search: {total}")
    print(f"Opening in batches of {batch_size}")
    print("=" * 60)
    
    for i in range(0, total, batch_size):
        batch = df.iloc[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        print(f"\n--- Batch {batch_num}/{total_batches} ---")
        
        for idx, row in batch.iterrows():
            title = row['title']
            paper_id = row['paper_id']
            url = create_scholar_url(title)
            
            print(f"  [{paper_id}] {title[:60]}...")
            webbrowser.open(url)
            time.sleep(0.5)  # Small delay between tabs
        
        if i + batch_size < total:
            print(f"\nOpened {min(i+batch_size, total)}/{total} searches")
            response = input("Press Enter for next batch, 'q' to quit, or number to skip to: ").strip()
            
            if response.lower() == 'q':
                print("Stopped by user.")
                break
            elif response.isdigit():
                skip_to = int(response)
                if skip_to > i + batch_size:
                    i = skip_to - batch_size
                    continue

def generate_scholar_links_html(df, output_file="data/processed/pdf_fetching/scholar_links.html"):
    """Generate HTML file with all Scholar links for easy clicking."""
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Google Scholar Links for PDF Download</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #1a0dab; }
        .paper { margin: 15px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
        .paper:hover { background: #f5f5f5; }
        .title { font-size: 16px; font-weight: bold; color: #1a0dab; }
        .meta { font-size: 12px; color: #666; margin: 5px 0; }
        .links { margin-top: 10px; }
        .links a { 
            display: inline-block; 
            margin-right: 10px; 
            padding: 5px 12px; 
            border-radius: 4px; 
            text-decoration: none;
            font-size: 13px;
        }
        .scholar { background: #4285f4; color: white; }
        .scholar:hover { background: #3367d6; }
        .scihub { background: #ff9800; color: white; }
        .scihub:hover { background: #f57c00; }
        .doi { background: #4caf50; color: white; }
        .doi:hover { background: #388e3c; }
        .downloaded { background: #e8f5e9; border-color: #4caf50; }
        .counter { 
            position: fixed; 
            top: 10px; 
            right: 10px; 
            background: #333; 
            color: white; 
            padding: 10px 20px;
            border-radius: 8px;
        }
        .instructions {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .checkbox { margin-right: 10px; transform: scale(1.3); }
    </style>
    <script>
        function updateCounter() {
            const checkboxes = document.querySelectorAll('.checkbox');
            const checked = Array.from(checkboxes).filter(cb => cb.checked).length;
            document.getElementById('counter').textContent = checked + '/' + checkboxes.length + ' downloaded';
        }
        function markDownloaded(id) {
            const paper = document.getElementById('paper-' + id);
            const checkbox = document.getElementById('cb-' + id);
            checkbox.checked = !checkbox.checked;
            paper.classList.toggle('downloaded', checkbox.checked);
            updateCounter();
            localStorage.setItem('downloaded-' + id, checkbox.checked);
        }
        function loadState() {
            const checkboxes = document.querySelectorAll('.checkbox');
            checkboxes.forEach(cb => {
                const id = cb.id.replace('cb-', '');
                const saved = localStorage.getItem('downloaded-' + id);
                if (saved === 'true') {
                    cb.checked = true;
                    document.getElementById('paper-' + id).classList.add('downloaded');
                }
            });
            updateCounter();
        }
        window.onload = loadState;
    </script>
</head>
<body>
    <h1>🔍 Google Scholar Links for PDF Download</h1>
    <div class="counter" id="counter">0/0 downloaded</div>
    
    <div class="instructions">
        <strong>Instructions:</strong>
        <ol>
            <li>Click "Scholar" to search for the paper on Google Scholar</li>
            <li>Look for [PDF] links on the right side of search results</li>
            <li>Download and save to <code>data/pdfs/</code> folder</li>
            <li>Click the checkbox to mark as downloaded (saves to browser storage)</li>
            <li>Alternative: Try Sci-Hub or DOI links if Scholar doesn't have PDF</li>
        </ol>
    </div>
    
    <div id="papers">
"""
    
    for idx, row in df.iterrows():
        paper_id = row['paper_id']
        title = row['title']
        doi = row.get('doi', '')
        authors = row.get('authors', 'Unknown')
        year = row.get('year', '')
        
        scholar_url = create_scholar_url(title)
        scihub_url = f"https://sci-hub.ru/{doi}" if pd.notna(doi) and doi else ""
        doi_url = f"https://doi.org/{doi}" if pd.notna(doi) and doi else ""
        
        html_content += f"""
        <div class="paper" id="paper-{paper_id}">
            <input type="checkbox" class="checkbox" id="cb-{paper_id}" onclick="markDownloaded('{paper_id}')">
            <span class="title">{title}</span>
            <div class="meta">
                <strong>ID:</strong> {paper_id} | 
                <strong>Year:</strong> {year} |
                <strong>Authors:</strong> {str(authors)[:100]}...
            </div>
            <div class="links">
                <a href="{scholar_url}" target="_blank" class="scholar">🔍 Scholar</a>
"""
        if scihub_url:
            html_content += f'                <a href="{scihub_url}" target="_blank" class="scihub">🔓 Sci-Hub</a>\n'
        if doi_url:
            html_content += f'                <a href="{doi_url}" target="_blank" class="doi">📄 DOI</a>\n'
        
        html_content += """            </div>
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding='utf-8')
    print(f"\nGenerated: {output_path}")
    print(f"Total papers: {len(df)}")
    return output_path

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Open Google Scholar searches for PDF downloading")
    parser.add_argument("--batch", type=int, default=5, help="Batch size for opening tabs")
    parser.add_argument("--html-only", action="store_true", help="Only generate HTML, don't open browser")
    parser.add_argument("--start", type=int, default=0, help="Start from paper index")
    args = parser.parse_args()
    
    df = get_missing_papers()
    
    if df.empty:
        print("No papers to fetch (all PDFs already downloaded or file not found)")
        return
    
    print(f"Found {len(df)} papers still needing PDFs")
    
    # Always generate HTML
    html_path = generate_scholar_links_html(df)
    
    if args.html_only:
        print(f"\nOpen {html_path} in your browser to manually download PDFs")
        return
    
    # Interactive batch opening
    print("\nOptions:")
    print("  1. Open HTML file in browser (recommended)")
    print("  2. Open Scholar searches in batches (auto-open tabs)")
    print("  3. Exit")
    
    choice = input("\nChoice [1]: ").strip() or "1"
    
    if choice == "1":
        webbrowser.open(str(html_path.absolute()))
    elif choice == "2":
        df_subset = df.iloc[args.start:]
        open_in_batches(df_subset, batch_size=args.batch)
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()
