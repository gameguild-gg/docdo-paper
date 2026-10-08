import requests
import time
import json
import re
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime

# --- CONFIG ---
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
REPO = Path('/Users/tolstenko/projects/docdo-paper-research')
SHADOW_DIR = REPO / 'artifacts/data/evidence/pdfs/shadow'
CORPUS_DIR = REPO / 'artifacts/data/evidence/pdfs'
ARXIV_HARVEST = Path('/tmp/pdf-dl/arxiv-harvest/harvest.jsonl')
BIO_HARVEST = Path('/tmp/pdf-dl/biorxiv-harvest/harvest.jsonl')
STATE_FILE = Path("/tmp/pdf-dl/arxiv_biorxiv2_state.json")

# DSL prefilter implementation from b8_fix_pipeline.py
_TOKEN_RE = re.compile(r"[a-z0-9]+")
def _tokens(text): return _TOKEN_RE.findall(text.lower())
def _has_phrase(tokens, phrase):
    parts = _TOKEN_RE.findall(phrase.lower())
    n = len(parts)
    return any(tokens[i:i + n] == parts for i in range(len(tokens) - n + 1))

def dsl_gate(title, abstract):
    combined = f"{title} {abstract}".lower()
    # Mimicking the core logic of b8_fix_pipeline's apply_exclusion_filters
    # 1. Review Exclusion
    review_terms = ['systematic review', 'literature review', 'survey of', 'a review', 'state-of-the-art review', 'comprehensive review', 'overview of', 'meta-analysis', 'scoping review']
    if any(term in title.lower() for term in review_terms): return False
    
    # 2. DL Requirement
    dl_terms = ['deep learning', 'neural network', 'cnn', 'convolutional', 'u-net', 'unet', 'transformer', 'encoder-decoder', 'resnet', 'vgg', 'densenet', 'attention']
    if not any(term in combined for term in dl_terms): return False
    
    # 3. CT Requirement
    ct_terms = ['ct ', 'ct,', 'ct.', 'computed tomography', 'ct scan', 'ct image', 'ct volume', 'ct data']
    if not any(term in combined for term in ct_terms): return False
    
    # 4. Organ Target
    organ_terms = ['liver', 'kidney', 'spleen', 'pancreas', 'lung', 'heart', 'stomach', 'gallbladder', 'bladder', 'prostate', 'colon', 'esophagus', 'adrenal', 'organ', 'hepatic', 'renal', 'pulmonary', 'cardiac', 'multi-organ', 'abdominal organ', 'thoracic organ']
    if not any(term in combined for term in organ_terms): return False
    
    # 5. Segmentation
    seg_terms = ['segment', 'delineat', 'contour', 'boundary', 'mask']
    if not any(term in combined for term in seg_terms): return False
    
    return True

def get_corpus_hashes():
    hashes = set()
    for p in CORPUS_DIR.rglob('*.pdf'):
        try:
            hashes.add(hashlib.md5(p.read_bytes()).hexdigest())
        except: pass
    return hashes

def download_pdf(url, filename):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as r:
            b = r.read()
            return b
    except Exception:
        # One Referer retry for 403s
        try:
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Referer': 'https://arxiv.org/' if 'arxiv' in url else 'https://www.biorxiv.org/'})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read()
        except: return None

def qa_pdf(b):
    if not b: return False
    if len(b) < 10000: return False
    if not b.startswith(b'%PDF'): return False
    try:
        import subprocess
        # Use pdftotext to check content
        temp_pdf = Path("/tmp/qa_check.pdf")
        temp_pdf.write_bytes(b)
        res = subprocess.run(['pdftotext', str(temp_pdf), '-'], capture_output=True, text=True, timeout=10)
        if len(res.stdout) < 100: return False
    except:
        # Fallback if pdftotext fails but header/size are ok
        pass
    return True

def main():
    SHADOW_DIR.mkdir(parents=True, exist_ok=True)
    corpus_hashes = get_corpus_hashes()
    print(f"Loaded {len(corpus_hashes)} corpus hashes.")
    
    total_downloaded = 0
    total_passed = 0
    
    # Process arXiv
    if ARXIV_HARVEST.exists():
        with open(ARXIV_HARVEST, 'r') as f:
            for i, line in enumerate(f):
                rec = json.loads(line)
                if not dsl_gate(rec['title'], rec['abstract']): continue
                
                url = rec['pdf_url']
                fid = re.sub(r'[^A-Za-z0-9._-]', '_', rec['arxiv_id']) + '.pdf'
                dest = SHADOW_DIR / fid
                
                b = download_pdf(url, fid)
                if b and qa_pdf(b):
                    h = hashlib.md5(b).hexdigest()
                    if h not in corpus_hashes:
                        dest.write_bytes(b)
                        corpus_hashes.add(h)
                        total_passed += 1
                
                total_downloaded += 1
                if total_downloaded % 15 == 0:
                    print(f"arXiv: Processed {i+1}, Passed {total_passed}...")
                if b and qa_pdf(b):
                    print(f"  SAVED: {fid}")

    # Process Bio/Med
    if BIO_HARVEST.exists():
        with open(BIO_HARVEST, 'r') as f:
            for i, line in enumerate(f):
                rec = json.loads(line)
                if not dsl_gate(rec['title'], rec['abstract']): continue
                
                doi = rec['doi']
                server = rec['server']
                version = rec.get('version', '1')
                url = f"https://www.{server}.org/content/{doi}v{version}.full.pdf"
                fid = re.sub(r'[^A-Za-z0-9._-]', '_', doi) + '.pdf'
                dest = SHADOW_DIR / fid
                
                b = download_pdf(url, fid)
                if b and qa_pdf(b):
                    h = hashlib.md5(b).hexdigest()
                    if h not in corpus_hashes:
                        dest.write_bytes(b)
                        corpus_hashes.add(h)
                        total_passed += 1
                
                total_downloaded += 1
                if total_downloaded % 15 == 0:
                    print(f"Bio: Processed {i+1}, Passed {total_passed}...")
                if b and qa_pdf(b):
                    print(f"  SAVED: {fid}")

    print(f"FINAL: {total_passed} new PDFs added to shadow/")

if __name__ == "__main__":
    main()
