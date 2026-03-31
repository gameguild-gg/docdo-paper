#!/usr/bin/env python3
"""
Update final included papers list based on PDF availability.
Papers without PDFs are excluded with reason: "Full-text not publicly available"
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import re

# Paths
PDF_DIR = Path("data/pdfs")
FINAL_RESULTS_DIR = Path("data/processed/final_results")
OUTPUT_DIR = Path("data/processed/final_results")

def get_available_pdfs():
    """Get set of paper identifiers from downloaded PDFs."""
    pdf_ids = set()
    
    if not PDF_DIR.exists():
        return pdf_ids
    
    for pdf_file in PDF_DIR.glob("*.pdf"):
        filename = pdf_file.stem
        
        # Extract identifier from various filename patterns
        # DOI-based: 10.1002_mp.12480.pdf
        # arXiv-based: arXiv_1704.06382.pdf or http___arxiv.org_abs_1707.08037v1.pdf
        
        pdf_ids.add(filename)
        
        # Also try to extract DOI
        if filename.startswith("10."):
            doi = filename.replace("_", "/")
            pdf_ids.add(doi)
        
    return pdf_ids

def match_paper_to_pdf(row, pdf_files):
    """Check if a paper has a matching PDF."""
    doi = str(row.get('doi', '')) if pd.notna(row.get('doi')) else ''
    arxiv_id = str(row.get('arxiv_id', '')) if pd.notna(row.get('arxiv_id')) else ''
    url = str(row.get('url', '')) if pd.notna(row.get('url')) else ''
    
    # Check DOI match
    if doi:
        doi_filename = doi.replace("/", "_")
        if f"{doi_filename}.pdf" in pdf_files:
            return True, f"{doi_filename}.pdf"
    
    # Check arXiv match
    if arxiv_id:
        if f"arXiv_{arxiv_id}.pdf" in pdf_files:
            return True, f"arXiv_{arxiv_id}.pdf"
    
    # Check URL-based match (arxiv URLs)
    if 'arxiv.org' in url:
        url_filename = url.replace(":", "_").replace("/", "_")
        for pdf in pdf_files:
            if url_filename in pdf or pdf.startswith("http___arxiv"):
                # More flexible matching for arxiv
                arxiv_match = re.search(r'(\d{4}\.\d{4,5})', url)
                if arxiv_match:
                    arxiv_num = arxiv_match.group(1)
                    if arxiv_num in pdf:
                        return True, pdf
    
    # Direct filename check with various patterns
    for pdf in pdf_files:
        if doi and doi.replace("/", "_") in pdf:
            return True, pdf
        if arxiv_id and arxiv_id in pdf:
            return True, pdf
    
    return False, None

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Find the most recent final results file
    final_files = list(FINAL_RESULTS_DIR.glob("final_included_papers_*.csv"))
    if not final_files:
        print("ERROR: No final_included_papers file found!")
        return
    
    latest_final = max(final_files, key=lambda x: x.stat().st_mtime)
    print(f"Loading: {latest_final}")
    
    # Load data
    df_included = pd.read_csv(latest_final)
    print(f"Original included papers: {len(df_included)}")
    
    # Get list of PDF files
    pdf_files = [f.name for f in PDF_DIR.glob("*.pdf")]
    print(f"Available PDFs: {len(pdf_files)}")
    
    # Match papers to PDFs
    matches = []
    for idx, row in df_included.iterrows():
        has_pdf, pdf_file = match_paper_to_pdf(row, pdf_files)
        matches.append({
            'has_pdf': has_pdf,
            'pdf_file': pdf_file
        })
    
    df_included['has_pdf'] = [m['has_pdf'] for m in matches]
    df_included['pdf_file'] = [m['pdf_file'] for m in matches]
    
    # Split into with/without PDFs
    df_with_pdf = df_included[df_included['has_pdf'] == True].copy()
    df_without_pdf = df_included[df_included['has_pdf'] == False].copy()
    
    print(f"\nPapers WITH PDFs: {len(df_with_pdf)}")
    print(f"Papers WITHOUT PDFs: {len(df_without_pdf)}")
    
    # Add exclusion reason for papers without PDFs
    df_without_pdf['exclusion_reason'] = "Full-text not publicly available (not found via open access, institutional access, or public repositories)"
    df_without_pdf['exclusion_stage'] = "S3_fulltext_retrieval"
    
    # Save updated files
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Final included (only with PDFs)
    output_included = OUTPUT_DIR / f"final_included_with_pdfs_{timestamp}.csv"
    df_with_pdf.to_csv(output_included, index=False)
    print(f"\nSaved: {output_included}")
    
    # 2. Excluded due to no PDF
    output_excluded = OUTPUT_DIR / f"excluded_no_fulltext_{timestamp}.csv"
    df_without_pdf.to_csv(output_excluded, index=False)
    print(f"Saved: {output_excluded}")
    
    # 3. Summary report
    summary = f"""# Full-Text Retrieval Results
Generated: {datetime.now().isoformat()}

## Summary

| Stage | Count |
|-------|-------|
| Papers after AI screening (S2) | {len(df_included)} |
| Full-text retrieved | {len(df_with_pdf)} |
| Full-text NOT available | {len(df_without_pdf)} |
| **Final for full-text review** | **{len(df_with_pdf)}** |

## Exclusion Reason

Papers excluded at this stage (n={len(df_without_pdf)}):
- **Reason**: Full-text not publicly available
- **Details**: PDF not found via open access repositories (Unpaywall, arXiv, PubMed Central), 
  Sci-Hub, publisher open access, or institutional access

## Files Generated

1. `{output_included.name}` - {len(df_with_pdf)} papers with PDFs (proceed to full-text review)
2. `{output_excluded.name}` - {len(df_without_pdf)} papers excluded (no full-text)

## PRISMA Flow Update

```
Records after AI screening: {len(df_included)}
    ↓
Full-text articles assessed: {len(df_with_pdf)}
Full-text not available: {len(df_without_pdf)}
    ↓
Studies for data extraction: {len(df_with_pdf)}
```

## Papers Excluded (No Full-Text)

| # | Paper ID | Title | DOI |
|---|----------|-------|-----|
"""
    
    for i, (_, row) in enumerate(df_without_pdf.iterrows(), 1):
        title = str(row.get('title', 'N/A'))[:60] + "..."
        doi = row.get('doi', 'N/A')
        paper_id = row.get('paper_id', 'N/A')
        summary += f"| {i} | {paper_id} | {title} | {doi} |\n"
    
    summary_file = OUTPUT_DIR / f"S3_fulltext_retrieval_report_{timestamp}.md"
    summary_file.write_text(summary, encoding='utf-8')
    print(f"Saved: {summary_file}")
    
    # 4. Update PRISMA numbers
    prisma_update = f"""
## PRISMA Numbers Update (for main.tex)

% After S2 AI Screening
\\def\\afterAIscreening{{{len(df_included)}}}

% S3 Full-text retrieval
\\def\\fulltextRetrieved{{{len(df_with_pdf)}}}
\\def\\fulltextNotAvailable{{{len(df_without_pdf)}}}

% Final for review
\\def\\finalForReview{{{len(df_with_pdf)}}}
"""
    print(prisma_update)
    
    return len(df_with_pdf), len(df_without_pdf)

if __name__ == "__main__":
    main()
