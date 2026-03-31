# GitHub Actions Workflows

This directory contains automated workflows to maintain repository integrity, enforce compliance, and assist with research operations.

## Workflow Overview

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [Structure Validation](#structure-validation) | Push, PR | Validates 6-bucket model, doc links, scaffolds |
| [Release Compliance](#release-compliance) | Changes to `artifacts/data/public/` | Validates public releases meet requirements |
| [Source Legal Compliance](#source-legal-compliance) | Changes to sources.yaml, legal/ | Ensures sources have legal documentation |
| [Evidence Ledger Integrity](#evidence-ledger-integrity) | Changes to evidence/ | Validates audit trail records |
| [YAML Validation](#yaml-validation) | Changes to *.yaml/*.yml | Validates YAML syntax |
| [Scheduled Maintenance](#scheduled-maintenance) | Weekly (Monday 9am UTC) | Maintenance checks and reports |

---

## Structure Validation

**File:** `structure-validation.yml`

**Runs on:** Push to main/develop, PRs to main

**Checks:**
- All 6 context buckets exist (core, artifacts, work, operations, scholar, documentation)
- No misplaced `reports/` inside `artifacts/data/`
- Documentation links are valid
- Paper scaffolds have required files (README.md, paper.md)

**How to fix failures:**
- Run `make init` to create missing directories
- Run `make check-links` locally to identify broken links
- Run `make scaffold-paper name=...` to create proper paper structure

---

## Release Compliance

**File:** `release-compliance.yml`

**Runs on:** Changes to `artifacts/data/public/datasets/**`

**Checks:**
- Each release has: `dataset_card.md`, `LICENSE-DATASET`, `checksums.sha256`, `data/`
- Evidence ledger exists for the release
- Scans for potentially restricted content (HTML, large files, media)

**How to fix failures:**
1. Create missing files using `make scaffold-dataset name=... ver=...`
2. Ensure evidence ledger exists at `core/governance/evidence/releases/<name>/<version>/`
3. Review any flagged files for redistribution compliance
4. Complete checklist at `core/governance/legal/release-compliance.md`

---

## Source Legal Compliance

**File:** `source-legal-compliance.yml`

**Runs on:** Changes to `sources.yaml` or `core/governance/legal/sources/**`

**Checks:**
- Every source in `sources.yaml` has a legal folder
- Legal folder contains `notes.md`
- Terms snapshot exists (`terms-YYYYMMDD.*`)
- Checksums exist for terms snapshots

**How to fix failures:**
1. Create legal folder: `make scaffold-source id=<source_id>`
2. Fill in `notes.md` with source legal notes
3. Capture terms of service snapshot at ingestion time
4. Generate checksum: `sha256sum terms-YYYYMMDD.pdf > terms-YYYYMMDD.pdf.sha256`

---

## Evidence Ledger Integrity

**File:** `evidence-ledger.yml`

**Runs on:** Changes to `core/governance/evidence/**`

**Checks:**
- Download records have `run.json` and `manifest.jsonl`
- Processing records have required files and environment spec
- Release records have `release.json` and `checksums.sha256`
- JSON files are syntactically valid
- Cross-references between ledger and public releases

**How to fix failures:**
- Ensure pipelines write required audit files
- Validate JSON syntax with `jq . file.json`
- Check that every public release has a corresponding ledger entry

---

## YAML Validation

**File:** `yaml-validation.yml`

**Runs on:** Changes to any `*.yaml` or `*.yml` file

**Checks:**
- YAML syntax is valid
- Line length warnings (max 120)
- Consistent indentation
- Registry files have expected top-level keys

**How to fix failures:**
- Run `yamllint <file>` locally
- Fix syntax errors (indentation, missing colons, etc.)
- Ensure registry files have `sources:` or `datasets:` keys

---

## Scheduled Maintenance

**File:** `scheduled-maintenance.yml`

**Runs on:** Weekly (Monday 9:00 AM UTC), or manual dispatch

**Checks:**
- Orphan data files at repo root
- Empty directories needing `.gitkeep`
- Research log freshness
- Repository size summary
- DVC configuration status

**To run manually:**
1. Go to Actions tab in GitHub
2. Select "Scheduled Maintenance"
3. Click "Run workflow"

---

## Local Testing

You can run most checks locally before pushing:

```bash
# Run all structure checks
make check

# Check documentation links
make check-links

# Validate a specific release
make validate-release name=my-dataset ver=v1.0.0

# Run YAML linting (requires yamllint)
pip install yamllint
yamllint core/governance/registry/*.yaml
```

---

## Adding New Workflows

When adding new workflows:

1. Place in `.github/workflows/`
2. Use descriptive filename with dashes
3. Include header comment explaining purpose
4. Add entry to this README
5. Test locally when possible

---

## Disabling Workflows

To temporarily disable a workflow:

1. Rename file to add `.disabled` extension
2. Or comment out the `on:` triggers
3. Or use GitHub UI: Actions → Workflow → Disable

---

## Badge Status

Add these badges to your main README:

```markdown
![Structure](../../actions/workflows/structure-validation.yml/badge.svg)
![Releases](../../actions/workflows/release-compliance.yml/badge.svg)
![Legal](../../actions/workflows/source-legal-compliance.yml/badge.svg)
```
