import requests
import time
import json
import re
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
ARXIV_QUERIES = [
    'all:"organ segmentation" AND all:CT',
    'all:"computed tomography" AND all:segmentation',
    'all:"deep learning" AND all:CT AND all:segmentation',
    'all:U-Net AND all:"computed tomography"',
    'all:segmentation AND all:(liver OR kidney OR spleen OR pancreas)',
    'all:"medical image segmentation" AND all:transformer'
]
Biorxiv_Servers = ['biorxiv', 'medrxiv']
STATE_FILE = Path("/tmp/pdf-dl/arxiv_biorxiv2_state.json")
ARXIV_OUT = Path("/tmp/pdf-dl/arxiv-harvest/harvest.jsonl")
BIO_OUT = Path("/tmp/pdf-dl/biorxiv-harvest/harvest.jsonl")

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"arxiv_queries_done": [], "bio_windows_done": []}

def harvest_arxiv(state):
    print("--- Starting arXiv Harvest (Regex Mode) ---", flush=True)
    for query in ARXIV_QUERIES:
        if query in state["arxiv_queries_done"]:
            continue
        
        print(f"Querying arXiv: {query}", flush=True)
        start = 0
        while start < 500:
            url = f"http://export.arxiv.org/api/query?search_query={requests.utils.quote(query)}&start={start}&max_results=100&sortBy=relevance"
            try:
                resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20)
                if resp.status_code != 200:
                    break
                
                content = resp.text
                entries = re.findall(r'<entry.*?>(.*?)</entry>', content, re.DOTALL)
                if not entries:
                    break
                    
                count = 0
                for entry in entries:
                    eid_match = re.search(r'<id.*?>(.*?)</id>', entry)
                    if not eid_match: continue
                    full_id = eid_match.group(1)
                    eid = full_id.split('/')[-1]
                    
                    doi_match = re.search(r'<doi.*?>(.*?)</doi>', entry)
                    doi = doi_match.group(1) if doi_match else ""
                    
                    title_match = re.search(r'<title.*?>(.*?)</title>', entry, re.DOTALL)
                    title = title_match.group(1).strip().replace('\n', ' ') if title_match else ""
                    
                    summary_match = re.search(r'<summary.*?>(.*?)</summary>', entry, re.DOTALL)
                    abstract = summary_match.group(1).strip().replace('\n', ' ') if summary_match else ""
                    
                    pub_match = re.search(r'<published.*?>(.*?)</published>', entry)
                    published = pub_match.group(1) if pub_match else ""
                    
                    pdf_url = f"https://arxiv.org/pdf/{eid}.pdf"
                    
                    with open(ARXIV_OUT, "a") as f:
                        f.write(json.dumps({"arxiv_id": eid, "doi": doi, "title": title, "abstract": abstract, "published": published, "pdf_url": pdf_url}) + "\n")
                    count += 1
                
                print(f"  Start {start}: found {count} entries", flush=True)
                start += 100
                time.sleep(3)
            except Exception as e:
                print(f"arXiv Exception: {e}", flush=True)
                break
        
        state["arxiv_queries_done"].append(query)
        save_state(state)
    print("arXiv Harvest Complete.", flush=True)

def harvest_bio(state):
    print("--- Starting bioRxiv/medRxiv Harvest ---", flush=True)
    years = range(2020, 2027)
    months = range(1, 13)
    
    for server in Biorxiv_Servers:
        for year in years:
            for month in months:
                if year == 2026 and month > 1: break
                win_id = f"{server}_{year}_{month:02d}"
                if win_id in state["bio_windows_done"]:
                    continue
                
                start_date = f"{year}-{month:02d}-01"
                if month == 12: end_date = f"{year+1}-01-01"
                else: end_date = f"{year}-{month+1:02d}-01"
                
                print(f"Querying {server} window: {start_date} to {end_date}", flush=True)
                cursor = 0
                while True:
                    url = f"https://api.biorxiv.org/details/{server}/{start_date}/{end_date}/{cursor}"
                    try:
                        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20)
                        if resp.status_code != 200:
                            break
                        
                        data = resp.json()
                        collections = data.get("collection", [])
                        if not collections:
                            break
                        
                        count = 0
                        for rec in collections:
                            text = (rec.get("title", "") + " " + rec.get("abstract", "")).lower()
                            keywords = ["segmentation", "computed tomography", "ct", "organ", "u-net", "deep learning"]
                            if any(k in text for k in keywords):
                                with open(BIO_OUT, "a") as f:
                                    f.write(json.dumps({
                                        "doi": rec.get("doi"),
                                        "server": server,
                                        "title": rec.get("title"),
                                        "abstract": rec.get("abstract"),
                                        "date": rec.get("date"),
                                        "version": rec.get("version")
                                    }) + "\n")
                                count += 1
                        
                        print(f"  Cursor {cursor}: kept {count}/{len(collections)}", flush=True)
                        cursor += 30
                        time.sleep(0.4)
                    except Exception as e:
                        print(f"BioRxiv Exception: {e}", flush=True)
                        break
                
                state["bio_windows_done"].append(win_id)
                save_state(state)
    print("BioRxiv Harvest Complete.", flush=True)

if __name__ == "__main__":
    state = load_state()
    harvest_arxiv(state)
    harvest_bio(state)
