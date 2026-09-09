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

---

## Addendum — Task 6 seed-recall fix loop (2026-09-08, revision r1)

Appended per the Task-6 binding seed-recall oracle (plan §6). One sanctioned
query-layer fix loop executed; `-001` CSVs remain immutable.

**Root causes found and fixed:**

1. **VISTA-3D hyphen defect** — the canonical paper (arXiv:2406.05285) is
   titled "VISTA3D" (unhyphenated); the pinned family-B term "VISTA-3D"
   cannot match it in any fielded index. Fix: `queries_v2.yaml` r1 adds the
   exact token `VISTA3D` to family B in all four databases (query ids bumped
   to `B-PUB-002` / `B-ARX-002` / `B-S2-002` / `B-GS-002`); ES whitelist
   `FRAMEWORK_TOOL_NAMES` synced (+ "VISTA3D").
2. **arXiv API parse flakiness** — the family-C arXiv query (~1.8 KB boolean)
   returned `totalResults` 893 and 185,098 for the identical query string
   within minutes (2026-09-08); the fetch-time sample missed the SAM-Med3D
   canonical. Fix: resample under `C-ARX-002` (query text unchanged).
   Subsequent analysis showed the 893-row parse is stable and the SAM-Med3D
   miss is template-inherent (canonical abstract has zero family-F anatomy
   tokens) — see `S2v2_seed_recall.md` row 9.
3. **Framework tool papers dropped at the pre-filter** — `apply_exclusion_filters`
   applied the method-paper EC3/organ checks to framework-bypass rows
   (nnInteractive excluded as "Bone/skeletal only"). Fix: the EC3 and
   strict-organ checks now skip **tool-name** framework matches only
   (`is_tool_name_candidate`); vocabulary-only matches remain under the
   method-paper anatomy criteria (pinned Task-3 behavior preserved for the
   heuristic lane).

**Fix-loop fetch results (provenance rows in `raw/v2/_provenance.csv`):**

| Query id | DB | Records | Status |
|----------|----|--------:|--------|
| B-PUB-002 | PubMed | 999 | ok |
| B-ARX-002 | arXiv | 1,000 | ok (VISTA3D canonical captured, R0128) |
| B-S2-002 | Semantic Scholar | 0 | error: HTTP 500 (storm persists; control probes 429 at both spaced retries) |
| B-GS-002 | Google Scholar | 10 | blocked: MaxTriesExceeded (partial rows kept; informational only) |
| C-ARX-002 | arXiv | 893 | ok (stable parse; template-inherent miss confirmed) |

**Downstream (idempotent re-runs):** `docdo fetch-v2 --concat` (10,644 →
13,546 rows over 29 immutable per-query CSVs) → `docdo deduplicate`
(8,147 → 8,161) → `v2_filter_and_funnel.py` → `S2v2_elasticsearch_filtered.csv`
**901 rows** (464 standard + 437 bypass), checker green; `S1v2_funnel.md`
regenerated. Tests: `operations/tests/` 191 passed (3 added:
VISTA3D bypass sample, tool-name organ-skip, vocab-only counter-test).

**Known unrecovered (documented, not silent):** MONAI Deploy canonical
(JMIR AI 2024, PMID 39653370) is PubMed-indexed but unreachable — no
tool-name tiab match, vocabulary arm matches 20,929 records, and the
1,000-record fetch window is date-descending and 2026-dominated (997/999
B-PUB-001 rows from 2026). Recovery requires a fetcher-level window fix
(sort/pagination in `fetch_pubmed_v2`), outside the Task-6 amendable
surface — filed for orchestrator sanction.

**Report Version:** 2.1 (addendum)

---

## Addendum r2 — PubMed window remediation + seed PMID recovery (2026-09-08)

Key-free Task-6 continuation. Two bounded supplementary fetches (the complete
set; documented in `queries_v2.yaml` `supplementary_queries`, validator green
unweakened; provenance rows in `raw/v2/_provenance.csv`):

| Query id | DB | Records | Status |
|----------|----|--------:|--------|
| B-PUB-002-pmid | PubMed (direct efetch) | 1 | seed-oracle PMID recovery: MONAI Deploy canonical (Gupta et al., JMIR AI 2024, PMID 39653370, DOI 10.2196/55833) — dedup R1754, bypass lane |
| G-PUB-002-r | PubMed (sort=relevance) | 1,000 | retention probe; year spread 2019-2026 (vs 995/1000 rows from 2026 in G-PUB-001's default-ordered window) |

**Fetcher changes** (`operations/src/docdo/fetch_v2_fetchers.py`):
`fetch_pubmed_v2(sort=...)` (Entrez relevance window option) and
`fetch_pubmed_by_pmids(...)` (direct efetch by known ids). Red-first tests;
suite 196 green.

**Retention probe result:** G-PUB-002-r recovered **7 of the 26 v1-missed
studies** (complete abdomen/pelvis U-Net variant; 3D-patch-based abdominal
multi-organ; 3D self-attention U-Net multi-organ; DECT multi-organ;
interactive 3D U-Net pancreas; DNN pancreas segmentation+volumetry;
kidney+renal-mass segmentation/detection). v1 retention 26/52 -> **32/52**
(9 DOI + 23 title). The remaining 20 misses are attributed to the family-F
`organ[tiab]` gap and the blocked S2 lane (unchanged diagnosis; Task 9
reconciles).

**Funnel after r2:** raw 14,547 (31 immutable per-query CSVs) -> dedup 8,846
-> `es_pass_total` **1,101** (641 standard + 460 bypass), checker green.
MONAI Deploy seed: BLOCKED -> in screening pool (see `S2v2_seed_recall.md`).

**Report Version:** 2.2 (addendum r2)

---

## Addendum r3 — S2 lane recovery attempt (2026-09-08 evening)

**Trigger:** orchestrator control probe returned HTTP 200 with live JSON
(`paper/search?query=liver+segmentation&limit=2`, total=1,025,418) minutes
after an evening of 429s + one transient 500 — the lane appeared recovered,
possibly temporarily.

**Attempt:** the six zero-row S2 stubs (A/B/C/D/E/G-S2-001 + the r1
B-S2-002 header-only stub; all verified 1-line before deletion) were removed
and the six cells re-fetched through the package fetcher (built-in
progressive 429 backoff, 900 s watchdog per cell, targeted driver — NOT
`docdo fetch-v2` run_all, which would re-fire the EBSCO scripted lane past
the pinned 1+1 attempt depth).

**Result: lane re-closed — zero cells landed.**

| Cell | Records | Status (provenance row) |
|------|--------:|-------------------------|
| A-S2-001 | 0 | blocked: watchdog timeout (900s) — 2026-09-08 |
| B-S2-002 | 0 | blocked: watchdog timeout (900s) — 2026-09-08 |
| C-S2-001 | 0 | blocked: watchdog timeout (900s) — 2026-09-08 |
| D-S2-001 | 0 | blocked: watchdog timeout (900s) — 2026-09-08 |
| E-S2-001 | 0 | blocked: watchdog timeout (900s) — 2026-09-08 |
| G-S2-001 | 0 | blocked: watchdog timeout (900s) — 2026-09-08 |

Post-run control probes: two spaced probes both HTTP 429 (45 s apart). Every
in-fetcher request exhausted its built-in backoff inside the watchdog — the
200-window the orchestrator observed did not recur for this client during
the ~90 min attempt. Header-only terminal stubs restored for all six cells
(B-S2-001 intentionally not recreated: the r1 amendment renamed family B's
current id to B-S2-002; the original B-S2-001 provenance history stands).

**Impact: none on funnel numbers.** `_combined.csv` re-concatenated
(14,547 rows over 30 per-query CSVs — the count drop is the retired B-S2-001
stub), dedup 8,846, `es_pass_total` 1,101 (641 + 460), checker green; v1
retention unchanged 32/52; all 12 seed states in `S2v2_seed_recall.md`
re-verified unchanged. The S2 lane remains the single largest known gap
(v1 drew 1,084 records from S2); a future open window re-runs the same
driver unchanged.

**Report Version:** 2.3 (addendum r3)
