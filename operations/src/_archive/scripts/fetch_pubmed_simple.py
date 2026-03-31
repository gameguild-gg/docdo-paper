"""
Simple PubMed Fetcher - Quick Test
Fetches 200 real papers to test the system works
"""

import csv
import time
import socket
from datetime import datetime

# Set timeout
socket.setdefaulttimeout(60)

# Configuration  
EMAIL = "survey_search@literature.review"
MAX_RESULTS = 200  # Small batch for testing
OUTPUT_FILE = "../S1_search_results_REAL.csv"

QUERY = """
(CT[Title/Abstract] OR "computed tomography"[Title/Abstract]) 
AND (segmentation[Title/Abstract]) 
AND (organ[Title/Abstract] OR liver[Title/Abstract] OR kidney[Title/Abstract])
AND ("deep learning"[Title/Abstract] OR "neural network"[Title/Abstract])
"""

def main():
    from Bio import Entrez
    Entrez.email = EMAIL
    
    print("=" * 60)
    print("FETCHING REAL PUBMED DATA")
    print("=" * 60)
    
    # Search
    print("\n[1] Searching PubMed...")
    handle = Entrez.esearch(db="pubmed", term=QUERY, retmax=MAX_RESULTS)
    record = Entrez.read(handle)
    handle.close()
    
    id_list = record["IdList"]
    print(f"    Found {record['Count']} total, fetching {len(id_list)}")
    
    results = []
    batch_size = 20
    
    for i in range(0, len(id_list), batch_size):
        batch = id_list[i:i+batch_size]
        batch_num = i//batch_size + 1
        total_batches = (len(id_list)-1)//batch_size + 1
        print(f"[2] Fetching batch {batch_num}/{total_batches}...")
        
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
                    for author in author_list[:5]:
                        lastname = author.get("LastName", "")
                        initials = author.get("Initials", "")
                        if lastname:
                            authors.append(f"{lastname} {initials}")
                    authors_str = "; ".join(authors)
                    if len(author_list) > 5:
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
                    
                    # Abstract
                    abstract_parts = article_data.get("Abstract", {}).get("AbstractText", [])
                    if abstract_parts:
                        if isinstance(abstract_parts, list):
                            abstract = " ".join(str(p) for p in abstract_parts)
                        else:
                            abstract = str(abstract_parts)
                        abstract = abstract[:300] + "..." if len(abstract) > 300 else abstract
                    else:
                        abstract = ""
                    
                    results.append({
                        "id": f"R{len(results)+1:04d}",
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
                    print(f"    Error parsing: {e}")
                    
        except Exception as e:
            print(f"    Batch error: {e}")
            
        time.sleep(0.5)  # Rate limit
    
    # Write CSV
    print(f"\n[3] Writing {len(results)} results to CSV...")
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, OUTPUT_FILE)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'database', 'search_date', 'title', 'authors', 
                      'year', 'journal_conference', 'doi', 'abstract_snippet']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n{'='*60}")
    print(f"SUCCESS! Wrote {len(results)} REAL papers to:")
    print(f"  {output_path}")
    print(f"{'='*60}")
    
    # Show first 5 titles
    print("\nFirst 5 papers fetched:")
    for i, r in enumerate(results[:5]):
        print(f"  {i+1}. {r['title'][:70]}...")
        print(f"     {r['authors'][:50]}... ({r['year']})")

if __name__ == "__main__":
    main()
