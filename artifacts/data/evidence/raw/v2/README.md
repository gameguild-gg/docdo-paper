# Raw v2 Search Results (Task 4, 2026-09-08)

Immutable per-query fetch artifacts for the v2 re-search. This directory is
gitignored by policy (`raw/**` is private; see `.gitignore:192-197`) — the
CSVs live on disk only, like the v1 raw set. This README is the whitelisted
in-repo record of what exists here.

## Inventory (24 query CSVs + 2 derived files)

| Query ID | Records | | Query ID | Records |
|---|---|---|---|---|
| A-PUB-001 | 540 | | D-PUB-001 | 1000 |
| A-ARX-001 | 378 | | D-ARX-001 | 1000 |
| A-S2-001 | 0 (blocked) | | D-S2-001 | 0 (blocked) |
| A-GS-001 | 7 | | D-GS-001 | 100 |
| B-PUB-001 | 999 | | E-PUB-001 | 999 |
| B-ARX-001 | 1000 | | E-ARX-001 | 1000 |
| B-S2-001 | 0 (blocked) | | E-S2-001 | 0 (blocked) |
| B-GS-001 | 11 | | E-GS-001 | 100 |
| C-PUB-001 | 507 | | G-PUB-001 | 1000 |
| C-ARX-001 | 893 | | G-ARX-001 | 1000 |
| C-S2-001 | 0 (blocked) | | G-S2-001 | 0 (blocked) |
| C-GS-001 | 10 | | G-GS-001 | 100 |

**Total raw rows: 10,644** (PubMed 5,045 + arXiv 5,271 + Google Scholar 328 + Semantic Scholar 0).

Derived files (regenerable, never concat inputs):

- `_combined.csv` — deterministic concat of all per-query CSVs; sole input to the Task-5 dedup stage (`docdo fetch-v2 --concat`).
- `_provenance.csv` — append-only attempt ledger: one row per fetch attempt across first pass, recovery rounds, probes, and terminal classifications.

## Provenance summary

- Six Semantic Scholar cells are terminal **blocked** (persistent lane-level 429 storm on 2026-09-08; exact-query probes and a control query all returned 429/500 — not genuine zeros). Evidence: `_provenance.csv` rows and the stdout log snapshotted at `.omo/evidence/task-4-paper-coverage-gap-update.stdout.log` (local ledger).
- A-GS-001 (dep-error, then soft-block 0) and B-GS-001 (soft-block 0) were recovered in spaced retry rounds to 7 and 11 rows respectively.
- EBSCO ChampSearch: scripted + browser attempts executed the six rendered family templates (hit counts A=3,047 / B=71,037 / C=2,417 / D=7,439 / E=8,842 / G=38,537, guest campus-IP session); counts recorded, no records harvested — see `../supplementary/pipeline_outputs/S1v2_evidence_report.md`.

Full report: `artifacts/data/evidence/supplementary/pipeline_outputs/S1v2_evidence_report.md`.
Never edit a per-query CSV after write; regenerate `_combined.csv` only via the concat command.
