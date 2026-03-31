"""Fetch papers from PubMed, arXiv, Unpaywall, and Open Access publishers."""

from __future__ import annotations

import csv
import json
import re
import socket
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

from . import config

# ---------------------------------------------------------------------------
# PubMed search
# ---------------------------------------------------------------------------
DEFAULT_PUBMED_QUERY = (
    '(CT[Title/Abstract] OR "computed tomography"[Title/Abstract]) '
    "AND (segmentation[Title/Abstract]) "
    "AND (organ[Title/Abstract] OR liver[Title/Abstract] OR kidney[Title/Abstract]) "
    'AND ("deep learning"[Title/Abstract] OR "neural network"[Title/Abstract])'
)


def fetch_pubmed(
    query: str = DEFAULT_PUBMED_QUERY,
    *,
    max_results: int = 200,
    batch_size: int = 20,
    output: Path | None = None,
    email: str | None = None,
) -> list[dict[str, str]]:
    """Search PubMed and return structured records.

    Parameters
    ----------
    query : str
        Entrez search query.
    max_results : int
        Maximum records to retrieve.
    batch_size : int
        Records per efetch call.
    output : Path | None
        If given, write results to this CSV.
    email : str | None
        Email for Entrez. Defaults to ``config.PUBMED_EMAIL``.

    Returns
    -------
    list[dict]
        Records with keys: id, database, search_date, title, authors, year,
        journal_conference, doi, abstract_snippet.
    """
    from Bio import Entrez

    socket.setdefaulttimeout(60)
    Entrez.email = email or config.PUBMED_EMAIL

    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    id_list = record["IdList"]

    results: list[dict[str, str]] = []
    for i in range(0, len(id_list), batch_size):
        batch = id_list[i : i + batch_size]
        try:
            handle = Entrez.efetch(db="pubmed", id=batch, rettype="xml", retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            for article in records.get("PubmedArticle", []):
                row = _parse_pubmed_article(article, len(results))
                if row:
                    results.append(row)
        except Exception as exc:
            print(f"  Batch error: {exc}")
        time.sleep(0.5)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        _FIELDNAMES = [
            "id", "database", "search_date", "title", "authors",
            "year", "journal_conference", "doi", "abstract_snippet",
        ]
        with open(output, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=_FIELDNAMES)
            writer.writeheader()
            writer.writerows(results)

    return results


def _parse_pubmed_article(article: dict, idx: int) -> dict[str, str] | None:
    """Extract a flat record from a PubMed article XML dict."""
    try:
        medline = article.get("MedlineCitation", {})
        art = medline.get("Article", {})

        title = str(art.get("ArticleTitle", ""))

        # Authors
        author_list = art.get("AuthorList", [])
        authors: list[str] = []
        for a in author_list[:5]:
            ln = a.get("LastName", "")
            ini = a.get("Initials", "")
            if ln:
                authors.append(f"{ln} {ini}")
        authors_str = "; ".join(authors)
        if len(author_list) > 5:
            authors_str += " et al."

        # Year
        pub_date = art.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
        year = pub_date.get("Year", "")
        if not year:
            md = pub_date.get("MedlineDate", "")
            if md:
                year = md[:4]

        journal = art.get("Journal", {}).get("Title", "")

        # DOI
        doi = ""
        for id_item in article.get("PubmedData", {}).get("ArticleIdList", []):
            if hasattr(id_item, "attributes") and id_item.attributes.get("IdType") == "doi":
                doi = str(id_item)
                break
        pmid = str(medline.get("PMID", ""))

        # Abstract
        ab_parts = art.get("Abstract", {}).get("AbstractText", [])
        if ab_parts:
            abstract = " ".join(str(p) for p in ab_parts) if isinstance(ab_parts, list) else str(ab_parts)
            abstract = abstract[:300] + "..." if len(abstract) > 300 else abstract
        else:
            abstract = ""

        return {
            "id": f"R{idx + 1:04d}",
            "database": "PubMed",
            "search_date": datetime.now().strftime("%Y-%m-%d"),
            "title": title,
            "authors": authors_str,
            "year": year,
            "journal_conference": journal,
            "doi": doi if doi else f"PMID:{pmid}",
            "abstract_snippet": abstract,
        }
    except Exception:
        return None


# ---------------------------------------------------------------------------
# PDF downloading
# ---------------------------------------------------------------------------
_UA = "Mozilla/5.0 (Academic Research Bot)"


def extract_arxiv_id(identifier: str) -> str | None:
    """Extract an arXiv ID from various formats."""
    patterns = [
        r"arxiv\.org/abs/(\d+\.\d+)(v\d+)?",
        r"arXiv:(\d+\.\d+)",
        r"^(\d{4}\.\d{4,5})(v\d+)?$",
    ]
    for pat in patterns:
        m = re.search(pat, identifier, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def extract_doi(identifier: str) -> str | None:
    """Extract a DOI from a string."""
    if identifier.startswith("10."):
        return identifier
    m = re.search(r"(10\.\d{4,}/[^\s]+)", identifier)
    return m.group(1) if m else None


def download_file(url: str, dest: Path, *, timeout: int = 30) -> tuple[bool, str]:
    """Download *url* to *dest*, returning ``(success, message)``."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read()
            if not content.startswith(b"%PDF"):
                return False, "Not a PDF"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
            return True, "OK"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, str(exc)[:50]


def fetch_from_arxiv(arxiv_id: str, dest: Path) -> tuple[bool, str]:
    """Download PDF from arXiv."""
    return download_file(f"https://arxiv.org/pdf/{arxiv_id}.pdf", dest)


def fetch_from_unpaywall(
    doi: str, dest: Path, *, email: str | None = None
) -> tuple[bool, str]:
    """Try to retrieve an OA PDF via the Unpaywall API."""
    email = email or config.UNPAYWALL_EMAIL
    try:
        api_url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
        req = urllib.request.Request(api_url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        best = data.get("best_oa_location")
        if best and best.get("url_for_pdf"):
            return download_file(best["url_for_pdf"], dest)
        for loc in data.get("oa_locations", []):
            if loc.get("url_for_pdf"):
                ok, msg = download_file(loc["url_for_pdf"], dest)
                if ok:
                    return ok, msg
        return False, "No OA PDF found"
    except Exception as exc:
        return False, str(exc)[:50]


def fetch_paper(
    paper_id: str,
    *,
    pdf_dir: Path | None = None,
    email: str | None = None,
) -> tuple[str, str, str | None]:
    """Try arXiv then Unpaywall for a single paper.

    Returns ``(paper_id, status_label, local_path_or_None)``.
    """
    pdf_dir = pdf_dir or config.PDF_DIR
    safe = re.sub(r"[^\w\-.]", "_", paper_id)[:100]
    dest = pdf_dir / f"{safe}.pdf"

    if dest.exists():
        return paper_id, "already_exists", str(dest)

    arxiv = extract_arxiv_id(paper_id)
    if arxiv:
        ok, _ = fetch_from_arxiv(arxiv, dest)
        if ok:
            return paper_id, "arxiv", str(dest)

    doi = extract_doi(paper_id)
    if doi:
        time.sleep(config.FETCH_DELAY)
        ok, msg = fetch_from_unpaywall(doi, dest, email=email)
        if ok:
            return paper_id, "unpaywall", str(dest)
        return paper_id, f"failed: {msg}", None

    return paper_id, "no_identifier", None


def fetch_pdfs(
    papers_csv: Path | None = None,
    *,
    pdf_dir: Path | None = None,
    email: str | None = None,
) -> dict[str, list[dict]]:
    """Fetch PDFs for all papers in a CSV file.

    Returns a summary dict with keys: success, already_exists, failed, no_identifier.
    """
    from .io import read_csv

    pdf_dir = pdf_dir or config.PDF_DIR
    pdf_dir.mkdir(parents=True, exist_ok=True)

    if papers_csv is None:
        # Find latest final_included_papers file
        candidates = sorted(config.FINAL_DIR.glob("final_included_papers_*.csv"), reverse=True)
        if not candidates:
            raise FileNotFoundError(f"No final_included_papers_*.csv in {config.FINAL_DIR}")
        papers_csv = candidates[0]

    papers = read_csv(papers_csv)
    results: dict[str, list[dict]] = {
        "success": [], "already_exists": [], "failed": [], "no_identifier": [],
    }

    for i, paper in enumerate(papers, 1):
        pid = paper.get("paper_id", paper.get("doi", ""))
        _, status, path = fetch_paper(pid, pdf_dir=pdf_dir, email=email)

        if status in ("arxiv", "unpaywall"):
            results["success"].append({"id": pid, "source": status, "path": path})
        elif status == "already_exists":
            results["already_exists"].append({"id": pid, "path": path})
        elif status == "no_identifier":
            results["no_identifier"].append({"id": pid})
        else:
            results["failed"].append({"id": pid, "reason": status})

        if i % 10 == 0:
            print(f"  [{i}/{len(papers)}] processed")
        time.sleep(0.5)

    return results


# ---------------------------------------------------------------------------
# Open Access publisher fetching
# ---------------------------------------------------------------------------
_OA_PREFIXES = ("10.3390", "10.3389", "10.1186")


def fetch_oa_papers(
    paywalled_csv: Path,
    *,
    pdf_dir: Path | None = None,
) -> int:
    """Download PDFs from known OA publishers (MDPI, Frontiers, BMC).

    Returns the number of successfully downloaded papers.
    """
    from .io import read_csv

    pdf_dir = pdf_dir or config.PDF_DIR
    pdf_dir.mkdir(parents=True, exist_ok=True)

    papers = read_csv(paywalled_csv)
    oa = [p for p in papers if any(p.get("paper_id", "").startswith(px) for px in _OA_PREFIXES)]

    downloaded = 0
    for i, paper in enumerate(oa, 1):
        doi = paper["paper_id"]
        safe = re.sub(r"[^\w\-.]", "_", doi)[:80] + ".pdf"
        dest = pdf_dir / safe

        if dest.exists():
            downloaded += 1
            continue

        try:
            req = urllib.request.Request(
                f"https://doi.org/{doi}",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Accept": "application/pdf,text/html",
                },
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                ct = resp.headers.get("Content-Type", "")
                if "pdf" in ct.lower():
                    content = resp.read()
                    if content.startswith(b"%PDF"):
                        dest.write_bytes(content)
                        downloaded += 1
                        continue
                html = resp.read().decode("utf-8", errors="ignore")
                final_url = resp.url

            # Scrape PDF link from HTML
            for pat in (
                r'href=["\']([^"\']+/pdf/[^"\']+\.pdf)["\']',
                r'href=["\']([^"\']+/article/[^"\']+/pdf[^"\']*)["\'?]',
                r'<a[^>]+href=["\']([^"\']+\.pdf)["\'][^>]*>[^<]*PDF',
            ):
                m = re.search(pat, html, re.IGNORECASE)
                if m:
                    pdf_url = m.group(1)
                    if not pdf_url.startswith("http"):
                        from urllib.parse import urljoin
                        pdf_url = urljoin(final_url, pdf_url)
                    ok, _ = download_file(pdf_url, dest, timeout=60)
                    if ok:
                        downloaded += 1
                        break
        except Exception:
            pass

        time.sleep(1)

    return downloaded
