"""Pure payload-to-row parsers for the v2 fetcher lanes.

Each parser maps one API payload shape (Entrez efetch dict, arXiv Atom XML,
S2 Graph JSON, scholarly pub dict) onto the exact v1 raw-record schema.
FULL abstracts are kept (archive fetch_all_real_data.py precedent — the
300-char truncation in docdo.fetch is NOT applied to raw v2 artifacts).
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any

_ATOM_NS = "{http://www.w3.org/2005/Atom}"
_ARXIV_NS = "{http://arxiv.org/schemas/atom}"


def today_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _author_list(names: list[str]) -> str:
    authors_str = "; ".join(n for n in names[:6] if n)
    if len(names) > 6:
        authors_str += " et al."
    return authors_str


def parse_pubmed_article(article: dict[str, Any]) -> dict[str, str] | None:
    try:
        medline = article.get("MedlineCitation", {})
        art = medline.get("Article", {})
        author_list = art.get("AuthorList", [])
        names = [
            f"{a.get('LastName', '')} {a.get('Initials', '')}".strip()
            for a in author_list
            if a.get("LastName")
        ]
        pub_date = art.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
        year = pub_date.get("Year", "") or str(pub_date.get("MedlineDate", ""))[:4]
        doi = ""
        for id_item in article.get("PubmedData", {}).get("ArticleIdList", []):
            if hasattr(id_item, "attributes") and id_item.attributes.get("IdType") == "doi":
                doi = str(id_item)
                break
        ab = art.get("Abstract", {}).get("AbstractText", [])
        abstract = " ".join(str(p) for p in ab) if isinstance(ab, list) else str(ab or "")
        return {
            "id": "",  # assigned per-file at write time
            "database": "PubMed",
            "search_date": today_iso(),
            "title": str(art.get("ArticleTitle", "")),
            "authors": _author_list(names),
            "year": year,
            "journal_conference": art.get("Journal", {}).get("Title", ""),
            "doi": doi if doi else f"PMID:{medline.get('PMID', '')}",
            "abstract_snippet": abstract,
        }
    except Exception:
        return None


def parse_arxiv_atom(text: str) -> list[dict[str, str]]:
    root = ET.fromstring(text)
    rows: list[dict[str, str]] = []
    for entry in root.findall(f"{_ATOM_NS}entry"):
        raw_id = (entry.findtext(f"{_ATOM_NS}id") or "").rsplit("/", 1)[-1]
        short_id = re.sub(r"v\d+$", "", raw_id)
        names = [
            e.findtext(f"{_ATOM_NS}name") or "" for e in entry.findall(f"{_ATOM_NS}author")
        ]
        doi = entry.findtext(f"{_ARXIV_NS}doi") or ""
        rows.append(
            {
                "id": "",
                "database": "arXiv",
                "search_date": today_iso(),
                "title": " ".join((entry.findtext(f"{_ATOM_NS}title") or "").split()),
                "authors": _author_list(names),
                "year": (entry.findtext(f"{_ATOM_NS}published") or "")[:4],
                "journal_conference": f"arXiv:{short_id}",
                "doi": doi if doi else f"arXiv:{short_id}",
                "abstract_snippet": " ".join(
                    (entry.findtext(f"{_ATOM_NS}summary") or "").split()
                ),
            }
        )
    return rows


def parse_s2_paper(paper: dict[str, Any]) -> dict[str, str] | None:
    title = paper.get("title", "")
    if not title:
        return None
    author_list = paper.get("authors", [])
    ext = paper.get("externalIds", {}) or {}
    doi = ext.get("DOI", "")
    if not doi and ext.get("ArXiv"):
        doi = f"arXiv:{ext['ArXiv']}"
    if not doi and ext.get("CorpusId"):
        doi = f"S2:{ext['CorpusId']}"
    return {
        "id": "",
        "database": "Semantic Scholar",
        "search_date": today_iso(),
        "title": title,
        "authors": _author_list([str(a.get("name", "")) for a in author_list]),
        "year": str(paper.get("year") or ""),
        "journal_conference": paper.get("venue", "") or "",
        "doi": doi,
        "abstract_snippet": paper.get("abstract") or "",
    }


def parse_gs_pub(pub: Any) -> dict[str, str] | None:
    bib = pub.get("bib", {}) if isinstance(pub, dict) else {}
    title = str(bib.get("title") or "")
    if not title:
        return None
    authors = bib.get("author") or []
    if isinstance(authors, str):
        authors = [authors]
    return {
        "id": "",
        "database": "Google Scholar",
        "search_date": today_iso(),
        "title": title,
        "authors": _author_list([str(a) for a in authors]),
        "year": str(bib.get("pub_year") or ""),
        "journal_conference": str(bib.get("venue") or ""),
        # frequently absent by design: dedup matches GS rows on normalized title
        "doi": str(bib.get("doi") or ""),
        "abstract_snippet": str(bib.get("abstract") or ""),
    }
