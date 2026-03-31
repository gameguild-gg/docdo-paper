"""
Real Literature Search Data Fetcher
====================================
Fetches REAL search results from PubMed and arXiv APIs for systematic review.

Usage:
    pip install biopython arxiv requests
    python fetch_real_data.py

Author: For 3D Organ Segmentation Survey
"""

import csv
import time
import os
from datetime import datetime

# ============================================================================
# CONFIGURATION - MODIFY THESE FOR YOUR SEARCH
# ============================================================================

# Your email (required for PubMed API)
EMAIL = "survey_search@literature.review"  # Generic email for API access

# Search queries
PUBMED_QUERY = """
(CT[Title/Abstract] OR "computed tomography"[Title/Abstract]) 
AND (segmentation[Title/Abstract]) 
AND (organ[Title/Abstract] OR liver[Title/Abstract] OR kidney[Title/Abstract] 
     OR spleen[Title/Abstract] OR pancreas[Title/Abstract])
AND ("deep learning"[Title/Abstract] OR "neural network"[Title/Abstract] 
     OR CNN[Title/Abstract] OR "U-Net"[Title/Abstract])
"""

ARXIV_QUERY = "ct segmentation organ deep learning"

# Maximum results per database
MAX_RESULTS_PUBMED = 1000
MAX_RESULTS_ARXIV = 500

# Output file
OUTPUT_FILE = "../S1_search_results_REAL.csv"

# ============================================================================
# PUBMED FETCHER
# ============================================================================

def fetch_pubmed_results(query, email, max_results=1000):
    """Fetch real results from PubMed using Entrez API with retry logic."""
    try:
        from Bio import Entrez
    except ImportError:
        print("ERROR: Install biopython first: pip install biopython")
        return []
    
    import socket
    socket.setdefaulttimeout(30)  # 30 second timeout
    
    Entrez.email = email
    results = []
    
    print(f"\n[PubMed] Searching with query...")
    print(f"[PubMed] Max results: {max_results}")
    
    try:
        # Search for IDs with retry
        for attempt in range(3):
            try:
                handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
                record = Entrez.read(handle)
                handle.close()
                break
            except Exception as e:
                print(f"[PubMed] Search attempt {attempt+1} failed: {e}")
                if attempt < 2:
                    time.sleep(5)
                else:
                    raise
        
        id_list = record["IdList"]
        total_found = record["Count"]
        print(f"[PubMed] Found {total_found} total results, fetching {len(id_list)}...")
        
        if not id_list:
            print("[PubMed] No results found.")
            return []
        
        # Fetch details in smaller batches of 50 with retry
        batch_size = 50
        for i in range(0, len(id_list), batch_size):
            batch_ids = id_list[i:i+batch_size]
            print(f"[PubMed] Fetching batch {i//batch_size + 1}/{(len(id_list)-1)//batch_size + 1}...")
            
            records = None
            for attempt in range(3):
                try:
                    handle = Entrez.efetch(db="pubmed", id=batch_ids, rettype="xml", retmode="xml")
                    records = Entrez.read(handle)
                    handle.close()
                    break
                except Exception as e:
                    print(f"[PubMed] Batch fetch attempt {attempt+1} failed: {e}")
                    if attempt < 2:
                        time.sleep(3)
                    else:
                        print(f"[PubMed] Skipping batch after 3 failures")
                        records = {"PubmedArticle": []}
            
            # Rate limiting - be nice to NCBI servers
            time.sleep(0.5)
            
            for article in records.get("PubmedArticle", []):
                try:
                    medline = article.get("MedlineCitation", {})
                    article_data = medline.get("Article", {})
                    
                    # Extract title
                    title = str(article_data.get("ArticleTitle", ""))
                    
                    # Extract authors
                    author_list = article_data.get("AuthorList", [])
                    authors = []
                    for author in author_list[:6]:  # First 6 authors
                        lastname = author.get("LastName", "")
                        initials = author.get("Initials", "")
                        if lastname:
                            authors.append(f"{lastname} {initials}")
                    authors_str = "; ".join(authors)
                    if len(author_list) > 6:
                        authors_str += " et al."
                    
                    # Extract year
                    pub_date = article_data.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
                    year = pub_date.get("Year", "")
                    if not year:
                        medline_date = pub_date.get("MedlineDate", "")
                        if medline_date:
                            year = medline_date[:4]
                    
                    # Extract journal
                    journal = article_data.get("Journal", {}).get("Title", "")
                    
                    # Extract DOI
                    doi = ""
                    for id_item in article.get("PubmedData", {}).get("ArticleIdList", []):
                        if id_item.attributes.get("IdType") == "doi":
                            doi = str(id_item)
                            break
                    
                    # Extract abstract
                    abstract_parts = article_data.get("Abstract", {}).get("AbstractText", [])
                    if abstract_parts:
                        if isinstance(abstract_parts, list):
                            abstract = " ".join(str(p) for p in abstract_parts)
                        else:
                            abstract = str(abstract_parts)
                        abstract = abstract[:500] + "..." if len(abstract) > 500 else abstract
                    else:
                        abstract = ""
                    
                    # PMID
                    pmid = str(medline.get("PMID", ""))
                    
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
                    print(f"[PubMed] Error parsing article: {e}")
                    continue
            
            time.sleep(0.5)  # Be nice to the API
        
        print(f"[PubMed] Successfully fetched {len(results)} results.")
        
    except Exception as e:
        print(f"[PubMed] Error: {e}")
    
    return results


# ============================================================================
# ARXIV FETCHER
# ============================================================================

def fetch_arxiv_results(query, max_results=500):
    """Fetch real results from arXiv API."""
    try:
        import arxiv
    except ImportError:
        print("ERROR: Install arxiv first: pip install arxiv")
        return []
    
    results = []
    
    print(f"\n[arXiv] Searching with query: {query}")
    print(f"[arXiv] Max results: {max_results}")
    
    try:
        # Search arXiv
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        client = arxiv.Client()
        
        for i, paper in enumerate(client.results(search)):
            if i % 50 == 0:
                print(f"[arXiv] Fetched {i} results...")
            
            try:
                # Extract authors
                authors = [author.name for author in paper.authors[:6]]
                authors_str = "; ".join(authors)
                if len(paper.authors) > 6:
                    authors_str += " et al."
                
                # Extract year
                year = paper.published.year if paper.published else ""
                
                # Extract abstract snippet
                abstract = paper.summary.replace("\n", " ")[:500]
                if len(paper.summary) > 500:
                    abstract += "..."
                
                # arXiv ID as DOI-like identifier
                arxiv_id = paper.entry_id.split("/")[-1]
                
                results.append({
                    "database": "arXiv",
                    "search_date": datetime.now().strftime("%Y-%m-%d"),
                    "title": paper.title.replace("\n", " "),
                    "authors": authors_str,
                    "year": str(year),
                    "journal_conference": "arXiv",
                    "doi": f"arXiv:{arxiv_id}",
                    "abstract_snippet": abstract,
                })
                
            except Exception as e:
                print(f"[arXiv] Error parsing paper: {e}")
                continue
            
            time.sleep(0.1)  # Be nice to the API
        
        print(f"[arXiv] Successfully fetched {len(results)} results.")
        
    except Exception as e:
        print(f"[arXiv] Error: {e}")
    
    return results


# ============================================================================
# SEMANTIC SCHOLAR FETCHER (Bonus - no auth needed)
# ============================================================================

def fetch_semantic_scholar_results(query, max_results=200):
    """Fetch results from Semantic Scholar API (free, no auth)."""
    try:
        import requests
    except ImportError:
        print("ERROR: Install requests first: pip install requests")
        return []
    
    results = []
    
    print(f"\n[Semantic Scholar] Searching with query: {query}")
    print(f"[Semantic Scholar] Max results: {max_results}")
    
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    try:
        offset = 0
        limit = 100  # API max per request
        
        while offset < max_results:
            params = {
                "query": query,
                "offset": offset,
                "limit": min(limit, max_results - offset),
                "fields": "title,authors,year,venue,externalIds,abstract"
            }
            
            print(f"[Semantic Scholar] Fetching offset {offset}...")
            
            response = requests.get(base_url, params=params)
            
            if response.status_code != 200:
                print(f"[Semantic Scholar] API error: {response.status_code}")
                break
            
            data = response.json()
            papers = data.get("data", [])
            
            if not papers:
                break
            
            for paper in papers:
                try:
                    # Authors
                    authors = [a.get("name", "") for a in paper.get("authors", [])[:6]]
                    authors_str = "; ".join(authors)
                    if len(paper.get("authors", [])) > 6:
                        authors_str += " et al."
                    
                    # DOI
                    ext_ids = paper.get("externalIds", {})
                    doi = ext_ids.get("DOI", "") or ext_ids.get("ArXiv", "") or ext_ids.get("PubMed", "")
                    
                    # Abstract
                    abstract = paper.get("abstract", "") or ""
                    abstract = abstract[:500] + "..." if len(abstract) > 500 else abstract
                    
                    results.append({
                        "database": "Semantic Scholar",
                        "search_date": datetime.now().strftime("%Y-%m-%d"),
                        "title": paper.get("title", ""),
                        "authors": authors_str,
                        "year": str(paper.get("year", "")),
                        "journal_conference": paper.get("venue", ""),
                        "doi": doi,
                        "abstract_snippet": abstract,
                    })
                    
                except Exception as e:
                    continue
            
            offset += limit
            time.sleep(1)  # Rate limiting
        
        print(f"[Semantic Scholar] Successfully fetched {len(results)} results.")
        
    except Exception as e:
        print(f"[Semantic Scholar] Error: {e}")
    
    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def write_csv(results, output_file):
    """Write results to CSV file."""
    if not results:
        print("No results to write!")
        return
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
    
    fieldnames = [
        "record_id", "database", "search_date", "query_string",
        "title", "authors", "year", "journal_conference", "doi",
        "abstract_snippet", "inclusion_status", "exclusion_reason"
    ]
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, result in enumerate(results, 1):
            row = {
                "record_id": f"R{i:04d}",
                "database": result["database"],
                "search_date": result["search_date"],
                "query_string": "See search protocol S3",
                "title": result["title"],
                "authors": result["authors"],
                "year": result["year"],
                "journal_conference": result["journal_conference"],
                "doi": result["doi"],
                "abstract_snippet": result["abstract_snippet"],
                "inclusion_status": "pending_screening",
                "exclusion_reason": ""
            }
            writer.writerow(row)
    
    print(f"\n✅ Wrote {len(results)} records to {output_file}")


def main():
    print("=" * 60)
    print("REAL LITERATURE SEARCH DATA FETCHER")
    print("For: 3D Organ Segmentation from CT Scans Survey")
    print("=" * 60)
    
    if EMAIL == "your_email@example.com":
        print("\n⚠️  WARNING: Please set your email in the EMAIL variable!")
        print("   PubMed requires a valid email for API access.\n")
    
    all_results = []
    
    # Fetch from PubMed
    pubmed_results = fetch_pubmed_results(PUBMED_QUERY, EMAIL, MAX_RESULTS_PUBMED)
    all_results.extend(pubmed_results)
    
    # Fetch from arXiv
    arxiv_results = fetch_arxiv_results(ARXIV_QUERY, MAX_RESULTS_ARXIV)
    all_results.extend(arxiv_results)
    
    # Fetch from Semantic Scholar (bonus)
    ss_results = fetch_semantic_scholar_results(
        "CT computed tomography organ segmentation deep learning", 
        max_results=300
    )
    all_results.extend(ss_results)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"PubMed:           {len(pubmed_results)} results")
    print(f"arXiv:            {len(arxiv_results)} results")
    print(f"Semantic Scholar: {len(ss_results)} results")
    print(f"TOTAL:            {len(all_results)} results")
    print("=" * 60)
    
    # Write to CSV
    write_csv(all_results, OUTPUT_FILE)
    
    print("\n📋 NEXT STEPS:")
    print("1. Review the generated CSV file")
    print("2. For IEEE/Scopus/ACM - manually export and add to CSV")
    print("3. Run AI screening on the results")
    print("4. Update inclusion_status and exclusion_reason columns")


if __name__ == "__main__":
    main()
