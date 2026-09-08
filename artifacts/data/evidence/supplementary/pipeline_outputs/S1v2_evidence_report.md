# S1v2 Search Results - Evidence Report

**Generated:** 2026-09-08 20:05:00
**Purpose:** Document data quality and provenance for the v2 re-search (amended query families A, B, C, D, E, G; F is a shared anatomy fragment, never executed standalone) for reproducibility
**Predecessor:** `S1_evidence_report.md` (v1, 2026-01-21)

---

## Data Pipeline

| Stage | File | Records |
|-------|------|---------|
| Raw (per-query CSVs) | `data/evidence/raw/v2/*.csv` (24 files) | 10,644 |
| Combined (derived, sole dedup input) | `data/evidence/raw/v2/_combined.csv` | 10,644 |
| Provenance ledger | `data/evidence/raw/v2/_provenance.csv` | 62 attempt rows |

---

## Per-Query Record Counts (every query id + count + date)

All searches executed 2026-09-08. Counts are data rows per immutable CSV.

| Query ID | Database | Family | Records | Terminal state |
|----------|----------|--------|---------|----------------|
| A-PUB-001 | PubMed | A (neuro-symbolic) | 540 | ok |
| A-ARX-001 | arXiv | A | 378 | ok |
| A-S2-001 | Semantic Scholar | A | 0 | **blocked** (persistent 429, see S2 lane) |
| A-GS-001 | Google Scholar | A | 7 | ok (recovered round 2; first pass dep-error/soft-block) |
| B-PUB-001 | PubMed | B (frameworks/tooling) | 999 | ok |
| B-ARX-001 | arXiv | B | 1000 | ok |
| B-S2-001 | Semantic Scholar | B | 0 | **blocked** (persistent 429) |
| B-GS-001 | Google Scholar | B | 11 | ok (recovered round 1; first pass soft-block 0) |
| C-PUB-001 | PubMed | C (foundation/SAM) | 507 | ok |
| C-ARX-001 | arXiv | C | 893 | ok |
| C-S2-001 | Semantic Scholar | C | 0 | **blocked** (persistent 429) |
| C-GS-001 | Google Scholar | C | 10 | ok (partial, live rows on first pass) |
| D-PUB-001 | PubMed | D (SOTA architectures) | 1000 | ok |
| D-ARX-001 | arXiv | D | 1000 | ok |
| D-S2-001 | Semantic Scholar | D | 0 | **blocked** (persistent 429) |
| D-GS-001 | Google Scholar | D | 100 | ok (cap reached) |
| E-PUB-001 | PubMed | E (benchmarks) | 999 | ok |
| E-ARX-001 | arXiv | E | 1000 | ok |
| E-S2-001 | Semantic Scholar | E | 0 | **blocked** (persistent 429; HTTP 500s during storm) |
| E-GS-001 | Google Scholar | E | 100 | ok (cap reached) |
| G-PUB-001 | PubMed | G (v1 core DL) | 1000 | ok |
| G-ARX-001 | arXiv | G | 1000 | ok |
| G-S2-001 | Semantic Scholar | G | 0 | **blocked** (persistent 429; HTTP 500s during storm) |
| G-GS-001 | Google Scholar | G | 100 | ok (cap reached) |

**Total raw records: 10,644** (PubMed 5,045 + arXiv 5,271 + Google Scholar 328 + Semantic Scholar 0).

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total records (pre-dedup)** | 10,644 |
| **With abstract (>100 chars)** | 10,630 (99.9%) |
| **With DOI** | 10,316 (96.9%) |
| **Average abstract length** | 1,609 chars |
| **Median abstract length** | 1,601 chars |
| **Unique DOIs across raw set** | 8,088 (cross-family/cross-DB overlap expected; dedup is Task 5) |

---

## By Source

### PubMed (via Entrez/Biopython API)

| Metric | Value |
|--------|-------|
| Records | 5,045 |
| With abstract | 5,032 (99.7%) |
| With DOI | 5,045 (100.0%) |
| Average abstract | 1,885 chars |
| Median abstract | 1,811 chars |
| Year range | 2015 - 2026 |

### arXiv (via arXiv API, fielded ti:/abs:)

| Metric | Value |
|--------|-------|
| Records | 5,271 |
| With abstract | 5,271 (100.0%) |
| With DOI (arXiv id in DOI field) | 5,271 (100.0%) |
| Average abstract | 1,433 chars |
| Median abstract | 1,449 chars |
| Year range | 2015 - 2026 |

### Google Scholar (via `scholarly` scraper — supplementary source)

| Metric | Value |
|--------|-------|
| Records | 328 |
| With abstract snippet | 327 (99.7%; snippets, avg 178 chars) |
| With DOI | 0 (expected — GS records frequently lack DOIs; title-based dedup downstream) |
| Year range | 2000 - 2026 (pre-2015 possible by design; year eligibility enforced at screening) |

### Semantic Scholar (via Graph API v1) — BLOCKED

| Metric | Value |
|--------|-------|
| Records | 0 of 6 queries |
| Status | Lane hard-blocked by sustained rate-limit storm (2026-09-08 ~12:00-20:00 EDT); see degradation narrative |

---

## Degradation Narrative (visible, never silent)

### Semantic Scholar rate-limit storm → lane blocked

1. **First pass (12:07-16:48 EDT):** all six S2 queries returned HTTP 200 with empty `data` payloads (0 rows, status "ok" — the swallow path), except E-S2-001 which surfaced `HTTP 500`. The v1-pattern progressive 429 backoff (30s → +30s, capped 600s) fired repeatedly inside the fetcher, confirming active throttling.
2. **Recovery rounds (17:08-19:39 EDT):** the six header-only stubs were deleted and re-fetched in 3 capped rounds per query (pinned 2/5/10 min inter-round waits). 18 recorded attempts total: repeated 200-with-empty-data swallows, intermittent HTTP 500s, and attempts that hit a 900s watchdog while sleeping inside 429 backoff (the fetcher's own bail threshold is ~105 min of cumulative backoff per request — the watchdog caps pathological waiting while every attempt stays provenance-logged).
3. **Interactive exact-query probes (19:47 EDT):** one `requests` hit per query with the exact query string → HTTP 429 for five queries, HTTP 500 for G-S2-001. A control probe with a trivially matching query ("liver segmentation") **also returned HTTP 429**, proving a lane-level block rather than query-specific zero hits. Genuine-zero classification was therefore ruled out.
4. **Terminal state:** all six S2 cells recorded `blocked` with date (2026-09-08) and query-id; header-only stub CSVs written so the 24-CSV set is complete. S2 coverage loss is partially compensated by PubMed + arXiv + Google Scholar lanes (per plan, EBSCO-unreachable and S2-degraded cases fall back to the remaining sources).

### Google Scholar soft-block → both affected cells recovered

- A-GS-001 first pass failed on a missing dependency (`scholarly` import chain: `bibtexparser.bibdatabase`) — 0 rows; `scholarly` was installed during the run (C/D/E/G-GS then returned 10/100/100/100 rows).
- B-GS-001 first pass returned "ok" with 0 rows — the GS soft-block signature (empty iterator, no exception). An interactive `scholarly.search_pubs` probe had already proven the query yields publications.
- Recovery with ≥60 s spacing: B-GS-001 recovered on round 1 (11 rows); A-GS-001 recovered on round 2 (7 rows). Low counts reflect GS's partial pagination under bot-mitigation plus the highly specific quoted-phrase query strings; partial rows are the documented graceful-degradation outcome (100/query cap never exceeded).

### EBSCO ChampSearch — attempted (scripted + browser), counts recorded

- **Scripted attempt (fetch-v2 lane):** POST of each rendered family string to `https://research.ebsco.com/c/uomcmi/search/advanced/filters` → HTTP 200 with no parseable records (JS-rendered application shell). Status: `attempted: HTTP 200` ×6.
- **Browser-automation attempt (Chrome via DevTools MCP, guest session on Champlain campus IP, ~17:15-17:30 EDT):** direct form fill registered only one of three AND rows, so the six full family templates were re-rendered as `advanced-results` URLs (page titles confirm the complete 3-block boolean queries executed). Hit counts returned to the guest session:
  A=3,047; B=71,037; C=2,417; D=7,439; E=8,842; G=38,537.
- **Outcome:** EBSCO is reachable and queries execute, but the guest session exposes hit counts and the first results page only — no exportable record list was harvested into raw CSVs (render/count lane per Task-3 design). Pinned attempt depth (1 scripted + 1 browser) consumed; recorded, not retried.

---

## Data Quality Assessment

### Strengths
- 100% of PubMed and arXiv records carry DOIs; near-complete abstracts (screening-ready)
- All raw CSVs are immutable post-write; every fetch attempt (including failures) is provenance-logged
- Blocked/failed lanes are recorded with evidence rather than silently dropped

### Limitations
- Semantic Scholar contributed 0 records (lane blocked 2026-09-08; v1 drew 920 records from S2 — cross-source recall is reduced for this run)
- Google Scholar yields are partial (328 records; soft-block truncation) and non-reproducible by design
- GS records lack DOIs (0%) and carry short snippet abstracts — title-based dedup + title-only screening path required downstream

---

## Reproducibility Evidence

### API Sources
| Source | API | Package | Query Date |
|--------|-----|---------|------------|
| PubMed | Entrez E-utilities | biopython | 2026-09-08 |
| arXiv | arXiv API (fielded ti:/abs:) | requests | 2026-09-08 |
| Semantic Scholar | Graph API v1 paper/search | requests | 2026-09-08 (blocked) |
| Google Scholar | HTML scrape | scholarly | 2026-09-08 |
| EBSCO ChampSearch | advanced-results (browser render) | Chrome/DevTools MCP | 2026-09-08 |

### Search Queries
- Source of truth: `operations/src/_archive/scripts/queries_v2.yaml` (families A, B, C, D, E, G × 4 databases; F = shared anatomy fragment, never executed standalone)
- Executed strings: AND-joined blocks per query; date range 2015-01-01 to 2026-09-08 (GS: no query-level date filter — documented limitation)
- EBSCO rendered strings: semantic-scholar blocks AND-joined (see stdout log snapshot in `.omo/evidence/task-4-paper-coverage-gap-update.stdout.log`)

---

## Files

| File | Location | Description |
|------|----------|-------------|
| Raw per-query CSVs | `data/evidence/raw/v2/<QUERY_ID>.csv` | 24 immutable fetch artifacts |
| Combined CSV | `data/evidence/raw/v2/_combined.csv` | Derived concat, sole Task-5 dedup input |
| Provenance ledger | `data/evidence/raw/v2/_provenance.csv` | Every attempt: query id, date, count, status |
| Fetcher | `operations/src/docdo/fetch_v2*.py` | Task-3 multi-query fetcher |
| Stdout log | `.omo/evidence/task-4-paper-coverage-gap-update.stdout.log` | First pass + recovery log snapshot |

---

**Report Version:** 2.0
**Author:** Automated pipeline
**Date:** 2026-09-08
