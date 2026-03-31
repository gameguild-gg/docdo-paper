# Changelog

All notable changes to the **docdo** project.

Follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and semantic versioning.

## Unreleased

### Added
- Comprehensive test suite: 150 pytest tests across 9 test modules (55% coverage)
- Data directory cleanup: removed template cruft, updated READMEs for PRISMA pipeline
- Coding scheme (IC1–IC5, EC1–EC6) and labeling rules (3-model unanimous voting)

## 0.1.0 — 2026-01-21

### Added
- `docdo` Python library with 9 modules: config, io, openai_utils, screening, fetch, dedup, verify, analysis, cli
- Click-based CLI with 13 subcommands for the full PRISMA pipeline
- Makefile with pipeline targets (fetch-pubmed, deduplicate, screen, stats, etc.)
- Archived 57 original scripts to `operations/src/_archive/`

### Changed
- Reorganized from flat script collection into 6-bucket academic template structure
- Consolidated ~815 duplicated lines into shared library modules
