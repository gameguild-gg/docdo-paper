"""
COMPREHENSIVE LITERATURE SEARCH DATA FETCHER
============================================
Fetches ALL available results from PubMed and arXiv APIs.
For: 3D Organ Segmentation from CT Scans Survey

Usage:
    python fetch_all_real_data.py
    
Will output: S1_search_results_REAL_COMPLETE.csv
"""

import csv
import time
import socket
from datetime import datetime
import os

# Increase timeout
socket.setdefaulttimeout(120)

# Configuration  
EMAIL = "survey_search@literature.review"
OUTPUT_FILE = "../../data/raw/S1_search_results_REAL.csv"

# PubMed query for CT organ segmentation
PUBMED_QUERY = """
(CT[Title/Abstract] OR "computed tomography"[Title/Abstract]) 
AND (segmentation[Title/Abstract]) 
AND (organ[Title/Abstract] OR liver[Title/Abstract] OR kidney[Title/Abstract] 
     OR spleen[Title/Abstract] OR pancreas[Title/Abstract] OR lung[Title/Abstract])
AND ("deep learning"[Title/Abstract] OR "neural network"[Title/Abstract] 
     OR CNN[Title/Abstract] OR "U-Net"[Title/Abstract] OR transformer[Title/Abstract])
"""

# arXiv query
ARXIV_QUERY = "ct computed tomography segmentation organ deep learning"

MAX_PUBMED = 1000
MAX_ARXIV = 1000
MAX_SEMANTIC_SCHOLAR = 1000

def fetch_pubmed_results():
    """Fetch all available PubMed results."""
    from Bio import Entrez
    Entrez.email = EMAIL
    
    print("\n" + "=" * 60)
    print("FETCHING PUBMED DATA")
    print("=" * 60)
    
    # Search
    print("\n[1] Searching PubMed database...")
    handle = Entrez.esearch(db="pubmed", term=PUBMED_QUERY, retmax=MAX_PUBMED)
    record = Entrez.read(handle)
    handle.close()
    
    id_list = record["IdList"]
    total_found = int(record["Count"])
    print(f"    Total in database: {total_found}")
    print(f"    Fetching: {len(id_list)}")
    
    results = []
    batch_size = 30  # Smaller batches for stability
    total_batches = (len(id_list) - 1) // batch_size + 1
    
    for i in range(0, len(id_list), batch_size):
        batch = id_list[i:i+batch_size]
        batch_num = i // batch_size + 1
        print(f"[2] Fetching batch {batch_num}/{total_batches} ({len(results)} papers so far)...")
        
        try:
            handle = Entrez.efetch(db="pubmed", id=batch, rettype="xml", retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            
            for article in records.get("PubmedArticle", []):
                try:
                    medline = article.get("MedlineCitation", {})
                    article_data = medline.get("Article", {})
                    
                    title = str(article_data.get("ArticleTitle", ""))
                    
                    # Authors
                    author_list = article_data.get("AuthorList", [])
                    authors = []
                    for author in author_list[:6]:
                        lastname = author.get("LastName", "")
                        initials = author.get("Initials", "")
                        if lastname:
                            authors.append(f"{lastname} {initials}")
                    authors_str = "; ".join(authors)
                    if len(author_list) > 6:
                        authors_str += " et al."
                    
                    # Year
                    pub_date = article_data.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
                    year = pub_date.get("Year", "")
                    if not year:
                        medline_date = pub_date.get("MedlineDate", "")
                        if medline_date:
                            year = medline_date[:4]
                    
                    # Journal
                    journal = article_data.get("Journal", {}).get("Title", "")
                    
                    # DOI
                    doi = ""
                    for id_item in article.get("PubmedData", {}).get("ArticleIdList", []):
                        if hasattr(id_item, 'attributes') and id_item.attributes.get("IdType") == "doi":
                            doi = str(id_item)
                            break
                    
                    # PMID
                    pmid = str(medline.get("PMID", ""))
                    
                    # Abstract - FULL
                    abstract_parts = article_data.get("Abstract", {}).get("AbstractText", [])
                    if abstract_parts:
                        if isinstance(abstract_parts, list):
                            abstract = " ".join(str(p) for p in abstract_parts)
                        else:
                            abstract = str(abstract_parts)
                        # Keep full abstract
                    else:
                        abstract = ""
                    
                    results.append({
                        "database": "PubMed",
                        "search_date": datetime.now().strftime("%Y-%m-%d"),
                        "title": title,
                        "authors": authors_str,
                        "year": year,
                        "journal_conference": journal,
                        "doi": doi if doi else f"PMID:{pmid}",
                        "abstract_snippet": abstract,
                    })
                    
                except Exception as e:
                    pass  # Skip problematic articles
                    
        except Exception as e:
            print(f"    Batch error: {e}, retrying...")
            time.sleep(5)
            try:
                handle = Entrez.efetch(db="pubmed", id=batch, rettype="xml", retmode="xml")
                records = Entrez.read(handle)
                handle.close()
                # Process again (simplified)
                for article in records.get("PubmedArticle", []):
                    try:
                        medline = article.get("MedlineCitation", {})
                        article_data = medline.get("Article", {})
                        title = str(article_data.get("ArticleTitle", ""))
                        pmid = str(medline.get("PMID", ""))
                        results.append({
                            "database": "PubMed",
                            "search_date": datetime.now().strftime("%Y-%m-%d"),
                            "title": title,
                            "authors": "",
                            "year": "",
                            "journal_conference": "",
                            "doi": f"PMID:{pmid}",
                            "abstract_snippet": "",
                        })
                    except:
                        pass
            except:
                print(f"    Skipping batch after retry failure")
            
        time.sleep(0.4)  # Rate limit
    
    print(f"\n[3] PubMed fetch complete: {len(results)} papers")
    return results


def fetch_arxiv_results():
    """Fetch arXiv results using arxiv package."""
    try:
        import arxiv
    except ImportError:
        print("ERROR: Install arxiv package: pip install arxiv")
        return []
    
    print("\n" + "=" * 60)
    print("FETCHING arXiv DATA")
    print("=" * 60)
    
    results = []
    
    # Multiple queries to cover the topic
    queries = [
        "ct computed tomography organ segmentation deep learning",
        "medical image segmentation liver kidney",
        "U-Net CT segmentation",
        "transformer medical image segmentation",
    ]
    
    seen_titles = set()
    
    for q_idx, query in enumerate(queries):
        print(f"\n[{q_idx+1}] Searching arXiv: '{query[:50]}...'")
        
        try:
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=300,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            count = 0
            for paper in client.results(search):
                # Deduplicate by title
                title_key = paper.title.lower().strip()
                if title_key in seen_titles:
                    continue
                seen_titles.add(title_key)
                
                # Authors
                authors = "; ".join([a.name for a in paper.authors[:6]])
                if len(paper.authors) > 6:
                    authors += " et al."
                
                # Year
                year = paper.published.year if paper.published else ""
                
                # Abstract - FULL
                abstract = paper.summary.replace('\n', ' ')
                
                results.append({
                    "database": "arXiv",
                    "search_date": datetime.now().strftime("%Y-%m-%d"),
                    "title": paper.title,
                    "authors": authors,
                    "year": str(year),
                    "journal_conference": f"arXiv:{paper.get_short_id()}",
                    "doi": paper.doi if paper.doi else paper.entry_id,
                    "abstract_snippet": abstract,
                })
                count += 1
                
            print(f"    Found {count} unique papers from this query")
            
        except Exception as e:
            print(f"    Error: {e}")
        
        time.sleep(1)  # Rate limit between queries
    
    print(f"\n[5] arXiv fetch complete: {len(results)} unique papers")
    return results


def fetch_semantic_scholar_results():
    """Fetch results from Semantic Scholar API (free, no auth needed)."""
    import requests
    
    print("\n" + "=" * 60)
    print("FETCHING SEMANTIC SCHOLAR DATA")
    print("=" * 60)
    
    results = []
    seen_titles = set()
    
    # Multiple queries
    queries = [
        "CT computed tomography organ segmentation deep learning",
        "medical image segmentation liver kidney spleen",
        "U-Net transformer CT segmentation",
        "abdominal CT deep learning segmentation",
        "3D medical image segmentation neural network",
    ]
    
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    for q_idx, query in enumerate(queries):
        print(f"\n[{q_idx+1}] Searching: '{query[:40]}...'")
        
        offset = 0
        per_query_limit = 600
        rate_limit_wait = 30  # Start at 30s, increase progressively
        
        while offset < per_query_limit and len(results) < MAX_SEMANTIC_SCHOLAR:
            try:
                params = {
                    "query": query,
                    "offset": offset,
                    "limit": 100,
                    "fields": "title,authors,year,venue,externalIds,abstract"
                }
                
                response = requests.get(base_url, params=params, timeout=30)
                
                if response.status_code == 429:  # Rate limited
                    if rate_limit_wait > 600:
                        print(f"    Rate limited, max wait exceeded (600s), skipping to next query...")
                        break
                    print(f"    Rate limited, waiting {rate_limit_wait}s...")
                    time.sleep(rate_limit_wait)
                    rate_limit_wait = min(rate_limit_wait + 30, 600)  # 30, 60, 90, 120... up to 600
                    continue
                    
                if response.status_code != 200:
                    print(f"    Error {response.status_code}, skipping...")
                    break
                    
                data = response.json()
                papers = data.get("data", [])
                
                if not papers:
                    break
                
                for paper in papers:
                    title = paper.get("title", "")
                    if not title:
                        continue
                        
                    title_key = title.lower().strip()
                    if title_key in seen_titles:
                        continue
                    seen_titles.add(title_key)
                    
                    # Authors
                    author_list = paper.get("authors", [])
                    authors = "; ".join([a.get("name", "") for a in author_list[:6]])
                    if len(author_list) > 6:
                        authors += " et al."
                    
                    # Year
                    year = paper.get("year", "")
                    
                    # Venue
                    venue = paper.get("venue", "")
                    
                    # DOI
                    ext_ids = paper.get("externalIds", {})
                    doi = ext_ids.get("DOI", "")
                    if not doi:
                        doi = ext_ids.get("ArXiv", "")
                        if doi:
                            doi = f"arXiv:{doi}"
                    if not doi:
                        doi = ext_ids.get("CorpusId", "")
                        if doi:
                            doi = f"S2:{doi}"
                    
                    # Abstract - FULL
                    abstract = paper.get("abstract", "") or ""
                    
                    results.append({
                        "database": "Semantic Scholar",
                        "search_date": datetime.now().strftime("%Y-%m-%d"),
                        "title": title,
                        "authors": authors,
                        "year": str(year) if year else "",
                        "journal_conference": venue,
                        "doi": doi,
                        "abstract_snippet": abstract,
                    })
                    
                offset += 100
                rate_limit_wait = 30  # Reset countdown on successful fetch
                print(f"    Fetched {len(results)} unique papers so far...")
                time.sleep(1)  # Rate limit
                
            except Exception as e:
                print(f"    Error: {e}")
                break
        
        if len(results) >= MAX_SEMANTIC_SCHOLAR:
            break
            
        time.sleep(2)  # Between queries
    
    print(f"\n[6] Semantic Scholar fetch complete: {len(results)} unique papers")
    return results


def main():
    print("=" * 70)
    print("  COMPREHENSIVE REAL LITERATURE SEARCH DATA FETCHER")
    print("  For: 3D Organ Segmentation from CT Scans Survey")
    print("  Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)
    
    all_results = []
    
    # Fetch PubMed
    pubmed_results = fetch_pubmed_results()
    all_results.extend(pubmed_results)
    
    # Fetch arXiv
    arxiv_results = fetch_arxiv_results()
    all_results.extend(arxiv_results)
    
    # Fetch Semantic Scholar
    ss_results = fetch_semantic_scholar_results()
    all_results.extend(ss_results)
    
    # Assign IDs
    for i, result in enumerate(all_results):
        result["id"] = f"R{i+1:04d}"
    
    # Write to CSV
    print("\n" + "=" * 60)
    print("WRITING RESULTS")
    print("=" * 60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, OUTPUT_FILE)
    
    fieldnames = ['id', 'database', 'search_date', 'title', 'authors', 
                  'year', 'journal_conference', 'doi', 'abstract_snippet']
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)
    
    # Summary
    pubmed_count = len([r for r in all_results if r['database'] == 'PubMed'])
    arxiv_count = len([r for r in all_results if r['database'] == 'arXiv'])
    ss_count = len([r for r in all_results if r['database'] == 'Semantic Scholar'])
    
    print(f"\n{'=' * 70}")
    print("  FETCH COMPLETE!")
    print(f"{'=' * 70}")
    print(f"  PubMed papers:          {pubmed_count}")
    print(f"  arXiv papers:           {arxiv_count}")
    print(f"  Semantic Scholar:       {ss_count}")
    print(f"  TOTAL:                  {len(all_results)}")
    print(f"\n  Output file: {output_path}")
    print(f"{'=' * 70}")
    
    # Show sample
    print("\nSample of papers fetched:")
    print("-" * 70)
    for i, r in enumerate(all_results[:5]):
        print(f"  {r['id']}. [{r['database']}] {r['title'][:60]}...")
        print(f"       {r['authors'][:50]}... ({r['year']})")
    print("-" * 70)


if __name__ == "__main__":
    main()
