#!/usr/bin/env python3
"""
Generate REAL reference data from 52 papers for the systematic review.
Creates:
1. BibTeX entries for references.bib  
2. LaTeX tables with REAL per-paper data
3. Summary statistics with paper citations
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent.parent
QA_RESULTS = REPO_ROOT / "data/processed/quality_assessment/qa_parsed_results_20260123_075645.json"
OUTPUT_DIR = REPO_ROOT / "data/processed/synthesis"

def load_data():
    with open(QA_RESULTS, encoding='utf-8') as f:
        return json.load(f)

def generate_bibtex_entries(data):
    """Generate BibTeX entries for all 52 papers."""
    bibtex = []
    
    for paper in data:
        if 'error' in paper:
            continue
        
        detail = paper.get('detailed_extraction', {})
        paper_id = paper.get('paper_id', '')
        
        # Create citation key
        authors = detail.get('authors', 'Unknown')
        year = detail.get('year', 2020)
        first_author = authors.split()[0].replace(',', '').replace('.', '').lower() if authors else 'unknown'
        cite_key = f"{first_author}{year}_{paper_id.split('_')[0].replace('.', '').replace('/', '')}"
        
        title = detail.get('title', 'Unknown Title')
        venue = detail.get('venue', 'Unknown Venue')
        doi = detail.get('doi', paper_id.replace('_', '/'))
        
        # Determine entry type
        if 'arXiv' in venue or 'arxiv' in paper_id.lower():
            entry = f"""@misc{{{cite_key},
  author = {{{authors}}},
  title = {{{title}}},
  year = {{{year}}},
  eprint = {{{doi}}},
  archivePrefix = {{arXiv}},
  primaryClass = {{cs.CV}}
}}"""
        elif 'MICCAI' in venue or 'IPMI' in venue or 'LNCS' in venue:
            entry = f"""@inproceedings{{{cite_key},
  author = {{{authors}}},
  title = {{{title}}},
  booktitle = {{{venue}}},
  year = {{{year}}},
  doi = {{{doi}}}
}}"""
        else:
            entry = f"""@article{{{cite_key},
  author = {{{authors}}},
  title = {{{title}}},
  journal = {{{venue}}},
  year = {{{year}}},
  doi = {{{doi}}}
}}"""
        
        bibtex.append(entry)
    
    return '\n\n'.join(bibtex)

def generate_detailed_comparison_table(data):
    """Generate LaTeX table with REAL data from each paper."""
    
    # Collect papers with Dice scores
    papers_with_dice = []
    
    for paper in data:
        if 'error' in paper:
            continue
        
        detail = paper.get('detailed_extraction', {})
        results = detail.get('results', {})
        method = detail.get('method', {})
        
        dice_per_organ = results.get('dice_per_organ', {})
        overall_dice = results.get('overall_dice')
        
        if dice_per_organ or overall_dice:
            # Get liver, kidney, spleen, pancreas Dice if available
            liver = None
            kidney = None
            spleen = None
            pancreas = None
            
            for organ, score in dice_per_organ.items():
                org_lower = organ.lower()
                if isinstance(score, (int, float)):
                    score_pct = score * 100 if score <= 1 else score
                    if 'liver' in org_lower and liver is None:
                        liver = score_pct
                    elif 'kidney' in org_lower and kidney is None:
                        kidney = score_pct
                    elif 'spleen' in org_lower and spleen is None:
                        spleen = score_pct
                    elif 'pancreas' in org_lower and pancreas is None:
                        pancreas = score_pct
            
            papers_with_dice.append({
                'paper_id': paper.get('paper_id'),
                'authors': detail.get('authors', 'Unknown'),
                'year': detail.get('year', 2020),
                'architecture': method.get('architecture_name', 'Unknown')[:40],
                'liver': liver,
                'kidney': kidney,
                'spleen': spleen,
                'pancreas': pancreas,
                'overall': float(overall_dice) * 100 if overall_dice and isinstance(overall_dice, (int, float)) and overall_dice <= 1 else (float(overall_dice) if isinstance(overall_dice, (int, float)) else None)
            })
    
    # Sort by year
    papers_with_dice.sort(key=lambda x: (x['year'] or 2020, x['paper_id']))
    
    # Generate LaTeX
    latex = [r"""
% REAL DATA TABLE: Per-Paper Performance from 52 Reviewed Studies
% Each row represents actual reported results from the corresponding paper
\begin{table*}[!htb]
\centering
\scriptsize
\caption{Detailed Performance Comparison from Reviewed Studies. Values are Dice scores (\%) as reported in original papers.}
\label{tab:detailed_papers}
\begin{tabular}{@{}p{3cm}cp{4cm}ccccc@{}}
\toprule
\textbf{Authors} & \textbf{Year} & \textbf{Architecture} & \textbf{Liver} & \textbf{Kidney} & \textbf{Spleen} & \textbf{Pancreas} & \textbf{Mean} \\
\midrule"""]
    
    for p in papers_with_dice[:30]:  # Top 30 papers
        authors = p['authors'][:20] + '...' if len(p['authors']) > 20 else p['authors']
        arch = p['architecture'][:35] + '...' if len(p['architecture']) > 35 else p['architecture']
        
        liver = f"{p['liver']:.1f}" if p['liver'] else '--'
        kidney = f"{p['kidney']:.1f}" if p['kidney'] else '--'
        spleen = f"{p['spleen']:.1f}" if p['spleen'] else '--'
        pancreas = f"{p['pancreas']:.1f}" if p['pancreas'] else '--'
        overall = f"{p['overall']:.1f}" if p['overall'] else '--'
        
        latex.append(f"{authors} & {p['year']} & {arch} & {liver} & {kidney} & {spleen} & {pancreas} & {overall} \\\\")
    
    latex.append(r"""\bottomrule
\end{tabular}
\end{table*}
""")
    
    return '\n'.join(latex), papers_with_dice

def generate_study_characteristics_table(data):
    """Generate summary characteristics table."""
    
    # Count by year
    years = defaultdict(int)
    architectures = defaultdict(int)
    organs_targeted = defaultdict(int)
    datasets_used = defaultdict(int)
    
    for paper in data:
        if 'error' in paper:
            continue
        
        detail = paper.get('detailed_extraction', {})
        
        # Year
        year = detail.get('year', 2020)
        years[year] += 1
        
        # Architecture
        method = detail.get('method', {})
        arch = method.get('architecture_type', 'Unknown')
        architectures[arch] += 1
        
        # Organs
        organs = detail.get('organs', {})
        for org in organs.get('segmented_organs', []):
            if org:
                organs_targeted[org.lower()] += 1
        
        # Datasets
        dataset = detail.get('dataset', {})
        for name in dataset.get('names', []):
            if name:
                datasets_used[name[:50]] += 1
    
    return years, architectures, organs_targeted, datasets_used

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Loading 52 papers' extracted data...")
    data = load_data()
    valid_data = [p for p in data if 'error' not in p]
    print(f"Loaded {len(valid_data)} valid papers")
    
    # Print some real examples
    print("\n" + "="*80)
    print("REAL DATA EXAMPLES FROM EXTRACTED PAPERS:")
    print("="*80)
    
    examples_shown = 0
    for paper in data:
        if 'error' in paper:
            continue
        
        detail = paper.get('detailed_extraction', {})
        results = detail.get('results', {})
        dice_per_organ = results.get('dice_per_organ', {})
        
        if dice_per_organ and examples_shown < 5:
            print(f"\n📄 Paper: {detail.get('title', 'Unknown')[:70]}...")
            print(f"   Authors: {detail.get('authors', 'Unknown')}")
            print(f"   Year: {detail.get('year', 'Unknown')}")
            print(f"   Venue: {detail.get('venue', 'Unknown')}")
            print(f"   Architecture: {detail.get('method', {}).get('architecture_name', 'Unknown')}")
            print(f"   Dice Scores (REAL from paper):")
            for organ, score in list(dice_per_organ.items())[:6]:
                if isinstance(score, (int, float)):
                    pct = score * 100 if score <= 1 else score
                    print(f"      - {organ}: {pct:.1f}%")
            examples_shown += 1
    
    # Generate outputs
    print("\n" + "="*80)
    print("GENERATING OUTPUT FILES...")
    print("="*80)
    
    # BibTeX
    print("\n1. Generating BibTeX entries...")
    bibtex = generate_bibtex_entries(data)
    bibtex_file = OUTPUT_DIR / f"reviewed_papers_{timestamp}.bib"
    with open(bibtex_file, 'w', encoding='utf-8') as f:
        f.write(bibtex)
    print(f"   Saved: {bibtex_file}")
    
    # Detailed comparison table
    print("\n2. Generating detailed comparison table...")
    table_latex, papers_dice = generate_detailed_comparison_table(data)
    table_file = OUTPUT_DIR / f"detailed_comparison_{timestamp}.tex"
    with open(table_file, 'w', encoding='utf-8') as f:
        f.write(table_latex)
    print(f"   Saved: {table_file}")
    print(f"   Papers with Dice data: {len(papers_dice)}")
    
    # Study characteristics
    print("\n3. Analyzing study characteristics...")
    years, archs, organs, datasets = generate_study_characteristics_table(data)
    
    print(f"\n   Publications by Year:")
    for year in sorted([y for y in years.keys() if y is not None]):
        print(f"      {year}: {years[year]} papers")
    
    print(f"\n   Top 10 Organs Studied:")
    for organ, count in sorted(organs.items(), key=lambda x: -x[1])[:10]:
        print(f"      {organ}: {count} papers")
    
    # Save full data as CSV
    print("\n4. Generating CSV with all extracted data...")
    import csv
    csv_file = OUTPUT_DIR / f"all_papers_data_{timestamp}.csv"
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'paper_id', 'title', 'authors', 'year', 'venue', 'doi',
            'architecture_name', 'architecture_type', '3d_processing', 'attention',
            'dataset_names', 'total_subjects', 'organs_segmented', 'num_organs',
            'framework', 'gpu', 'overall_dice', 'liver_dice', 'kidney_dice', 
            'spleen_dice', 'pancreas_dice', 'main_contribution'
        ])
        
        for paper in data:
            if 'error' in paper:
                continue
            
            detail = paper.get('detailed_extraction', {})
            method = detail.get('method', {})
            dataset = detail.get('dataset', {})
            organs = detail.get('organs', {})
            results = detail.get('results', {})
            impl = detail.get('implementation', {})
            contrib = paper.get('contribution_summary', {})
            
            dice_per_organ = results.get('dice_per_organ', {})
            
            # Extract organ-specific dice
            liver = kidney = spleen = pancreas = None
            for org, score in dice_per_organ.items():
                if isinstance(score, (int, float)):
                    s = score * 100 if score <= 1 else score
                    org_l = org.lower()
                    if 'liver' in org_l: liver = s
                    elif 'kidney' in org_l: kidney = s
                    elif 'spleen' in org_l: spleen = s
                    elif 'pancreas' in org_l: pancreas = s
            
            writer.writerow([
                paper.get('paper_id', ''),
                detail.get('title', ''),
                detail.get('authors', ''),
                detail.get('year', ''),
                detail.get('venue', ''),
                detail.get('doi', ''),
                method.get('architecture_name', ''),
                method.get('architecture_type', ''),
                method.get('3d_processing', ''),
                method.get('attention_mechanism', ''),
                '; '.join(dataset.get('names', [])),
                dataset.get('total_subjects', ''),
                '; '.join(organs.get('segmented_organs', [])[:10]),
                organs.get('num_organs', ''),
                impl.get('framework', ''),
                impl.get('gpu', ''),
                results.get('overall_dice', ''),
                liver,
                kidney,
                spleen,
                pancreas,
                contrib.get('main_contribution', '')[:200]
            ])
    
    print(f"   Saved: {csv_file}")
    
    print("\n" + "="*80)
    print("DONE! All files generated with REAL DATA from 52 papers.")
    print("="*80)
    
    print(f"\nOutput files:")
    print(f"  - {bibtex_file}")
    print(f"  - {table_file}")
    print(f"  - {csv_file}")

if __name__ == "__main__":
    main()
