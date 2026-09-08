"""Network adapters for the v2 multi-query fetcher (Task 3).

Each lane reuses the battle-tested v1 patterns from
operations/src/_archive/scripts/fetch_all_real_data.py:

- PubMed: Entrez esearch (mindate/maxdate, datetype=pdat) + batched efetch
  (30/batch) with retry-after-5s on batch errors
- arXiv: fielded ti:/abs: API queries via requests *params* encoding
  (~2KB query strings are never concatenated into the URL), date via
  submittedDate range
- Semantic Scholar: Graph API paper/search relevance endpoint (NO fielded
  search exists — boolean-structured relevance strings pass through as-is),
  year filter param, progressive 429 backoff 30s -> +30s capped at 600s
- Google Scholar: `scholarly` scraper, FIRST 100 results per query (10 GS
  pages), CAPTCHA/block -> blocked status + partial rows, caller continues.
  Proxies / FreeProxy / use_proxy are deliberately NEVER configured.
- EBSCO: render-only lane for the ChampSearch advanced-search form; live
  attempts belong to Task 4, any failure degrades to a blocked status.
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any

import requests

from .fetch_v2_parsers import (
    parse_arxiv_atom,
    parse_gs_pub,
    parse_pubmed_article,
    parse_s2_paper,
    today_iso,
)

PUBMED_MAX = 1000
PUBMED_BATCH = 30
ARXIV_MAX = 1000
ARXIV_PAGE = 100
S2_PER_QUERY_LIMIT = 600
S2_PAGE = 100
GS_MAX_RESULTS = 100
GS_RESULTS_PER_PAGE = 10

ARXIV_API_URL = "http://export.arxiv.org/api/query"
S2_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
EBSCO_ADVANCED_URL = "https://research.ebsco.com/c/uomcmi/search/advanced/filters"


# ---------------------------------------------------------------------------
# PubMed
# ---------------------------------------------------------------------------


def fetch_pubmed_v2(
    query: str,
    *,
    date_start: str = "2015-01-01",
    date_end: str | None = None,
    max_results: int = PUBMED_MAX,
    batch_size: int = PUBMED_BATCH,
    email: str | None = None,
) -> tuple[list[dict[str, str]], str]:
    from Bio import Entrez

    from . import config

    end = date_end or today_iso()
    Entrez.email = email or config.PUBMED_EMAIL
    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results,
        datetype="pdat",
        mindate=date_start.replace("-", "/"),
        maxdate=end.replace("-", "/"),
    )
    record = Entrez.read(handle)
    handle.close()
    id_list = list(record["IdList"])

    rows: list[dict[str, str]] = []
    for i in range(0, len(id_list), batch_size):
        records = _efetch_with_retry(id_list[i : i + batch_size])
        for article in records.get("PubmedArticle", []):
            row = parse_pubmed_article(article)
            if row:
                rows.append(row)
        time.sleep(0.4)  # Entrez courtesy (v1 pattern)
    return rows, "ok"


def _efetch_with_retry(batch: list[str]) -> dict[str, Any]:
    from Bio import Entrez

    for attempt in (1, 2):
        try:
            handle = Entrez.efetch(db="pubmed", id=batch, rettype="xml", retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            return records
        except Exception as exc:
            if attempt == 2:
                print(f"  PubMed batch skipped after retry failure: {exc}")
                return {}
            time.sleep(5)
    return {}




def fetch_arxiv_v2(
    query: str,
    *,
    date_start: str = "2015-01-01",
    date_end: str | None = None,
    max_results: int = ARXIV_MAX,
    page_size: int = ARXIV_PAGE,
) -> tuple[list[dict[str, str]], str]:
    start_stamp = _arxiv_stamp(date_start, "0000")
    end_stamp = _arxiv_stamp(date_end or today_iso(), "2359")
    search_query = f"({query}) AND submittedDate:[{start_stamp} TO {end_stamp}]"
    rows: list[dict[str, str]] = []
    for start in range(0, max_results, page_size):
        params = {
            "search_query": search_query,
            "start": start,
            "max_results": page_size,
            "sortBy": "relevance",
        }
        resp = requests.get(ARXIV_API_URL, params=params, timeout=60)
        resp.raise_for_status()
        entries = parse_arxiv_atom(resp.text)
        rows.extend(entries)
        if len(entries) < page_size:
            break
        time.sleep(3)  # arXiv API courtesy (3s between requests)
    return rows, "ok"


def _arxiv_stamp(iso_date: str, hhmm: str) -> str:
    return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%Y%m%d") + hhmm




def fetch_semantic_scholar_v2(
    query: str,
    *,
    date_start: str = "2015-01-01",
    date_end: str | None = None,
    per_query_limit: int = S2_PER_QUERY_LIMIT,
    page_size: int = S2_PAGE,
) -> tuple[list[dict[str, str]], str]:
    year_filter = f"{date_start[:4]}-{(date_end or today_iso())[:4]}"
    offset = 0
    rate_limit_wait = 30  # progressive 429 backoff: 30s -> +30s, capped at 600s (v1)
    rows: list[dict[str, str]] = []
    while offset < per_query_limit:
        params = {
            "query": query,  # boolean-structured relevance string (no fielded search exists)
            "offset": offset,
            "limit": page_size,
            "year": year_filter,
            "fields": "title,authors,year,venue,externalIds,abstract",
        }
        resp = requests.get(S2_BASE_URL, params=params, timeout=30)
        if resp.status_code == 429:
            if rate_limit_wait > 600:
                return rows, "error: rate limited beyond 600s wait"
            time.sleep(rate_limit_wait)
            rate_limit_wait = min(rate_limit_wait + 30, 600)
            continue
        if resp.status_code != 200:
            return rows, f"error: HTTP {resp.status_code}"
        papers = resp.json().get("data", [])
        if not papers:
            break
        for paper in papers:
            row = parse_s2_paper(paper)
            if row:
                rows.append(row)
        offset += page_size
        rate_limit_wait = 30
        time.sleep(1)
    return rows, "ok"




def fetch_google_scholar_v2(
    query: str,
    *,
    max_results: int = GS_MAX_RESULTS,
) -> tuple[list[dict[str, str]], str]:
    try:
        from scholarly import scholarly
    except ImportError as exc:
        return [], f"error: scholarly not installed ({exc})"

    rows: list[dict[str, str]] = []
    status = "ok"
    try:
        for i, pub in enumerate(scholarly.search_pubs(query)):
            if i >= max_results:
                break
            row = parse_gs_pub(pub)
            if row:
                rows.append(row)
    except Exception as exc:  # CAPTCHA / bot-block: keep partial rows, record, continue
        status = f"blocked: {type(exc).__name__}: {exc}"
    return rows, status




def render_ebsco_queries(data: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Render the six family templates for the ChampSearch advanced-search form.

    The yaml has no EBSCO block; each family renders from its
    semantic_scholar blocks (field-free boolean) joined with AND.
    """
    rendered: dict[str, dict[str, str]] = {}
    for family, fam_def in data["executed_families"].items():
        s2 = fam_def["queries"]["semantic_scholar"]
        rendered[family] = {
            "query_id": f"{family}-EBSCO-001",
            "query": " AND ".join(s2["blocks"]),
        }
    return rendered


def fetch_ebsco(
    data: dict[str, Any],
    *,
    attempt_live: bool = False,
) -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    """Render the family templates; optionally ONE scripted ChampSearch attempt
    per family. Any failure degrades to a blocked status — never raises."""
    rendered = render_ebsco_queries(data)
    statuses = {e["query_id"]: "rendered" for e in rendered.values()}
    if attempt_live:
        for entry in rendered.values():
            try:
                resp = requests.post(
                    EBSCO_ADVANCED_URL, data={"query": entry["query"]}, timeout=30
                )
                statuses[entry["query_id"]] = f"attempted: HTTP {resp.status_code}"
            except Exception as exc:
                statuses[entry["query_id"]] = f"blocked: {exc}"
    return rendered, statuses
