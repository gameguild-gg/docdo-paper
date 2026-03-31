# Data — DocDo Systematic Review

All empirical data for the systematic review on
**"3D Organ Segmentation from CT Scans using Deep Learning"**
following a PRISMA 2020 pipeline: **raw → interim → processed**.

---

## Structure

```text
data/
├── evidence/                  # PRISMA pipeline data
│   ├── raw/                   # S1: Original search results
│   │   └── S1_search_results_REAL.csv
│   │
│   ├── interim/               # S1 deduplicated, evidence reports
│   │   ├── S1_search_results_deduplicated.csv
│   │   └── S1_evidence_report.md
│   │
│   ├── processed/             # S2 screening, S3 full-text, final results
│   │   ├── S2_elasticsearch_filtered.csv
│   │   ├── batches*/          # OpenAI Batch API files
│   │   ├── batch_downloads/   # Downloaded batch outputs
│   │   ├── comparisons/       # Model comparison CSVs
│   │   ├── final_results/     # 3-model consensus results
│   │   ├── s3_fulltext_screening/  # Full-text screening + extraction
│   │   ├── peer_review/       # AI-assisted peer review
│   │   ├── quality_assessment/  # Quality scoring
│   │   └── synthesis/         # Final synthesis tables, BibTeX
│   │
│   ├── pdfs/                  # Downloaded paper PDFs
│   │   ├── *.pdf              # DOI-named and arXiv-named PDFs
│   │   ├── included-papers/   # Curated set for full-text review
│   │   └── reference-pdfs/    # Reference/background papers
│   │
│   └── supplementary/        # PRISMA supplementary materials (S0–S12)
│       ├── S0_data_provenance.md
│       ├── S2_included_studies.csv
│       ├── S3_search_protocol.md
│       ├── S4_ai_screening_protocol.md
│       └── ...
│
├── external/                  # Third-party benchmarks & datasets
├── public/                    # Redistributable outputs
├── schemas/                   # Validation schemas
├── catalogs/                  # Structured reference metadata
├── taxonomies/                # Classification systems
└── annotations/               # Coding scheme for data extraction
```

> **Note:** Generated reports (statistics, tables, figures) are at [reports/](../reports/)

---

## Pipeline Semantics

| Stage | PRISMA Phase | Contents |
|---|---|---|
| `evidence/raw/` | S1 Identification | PubMed/arXiv/Semantic Scholar search results |
| `evidence/interim/` | S1 Dedup | Deduplicated results, evidence reports |
| `evidence/processed/` | S2–S3 Screening | AI screening, consensus, full-text review |
| `evidence/pdfs/` | S3 Full-text | Downloaded paper PDFs |
| `evidence/supplementary/` | Documentation | PRISMA supplementary files (S0–S12) |

---

## Key Files

| File | Records | Description |
|---|---|---|
| `evidence/raw/S1_search_results_REAL.csv` | ~2,200 | Original search across 3 databases |
| `evidence/interim/S1_search_results_deduplicated.csv` | ~1,400 | After DOI + title dedup |
| `evidence/processed/S2_elasticsearch_filtered.csv` | ~640 | After Elasticsearch pre-filter |
| `evidence/processed/final_results/final_included_papers_*.csv` | ~50 | 3-model consensus INCLUDEs |
| `evidence/supplementary/S2_included_studies.csv` | ~50 | Final included studies list |

---

## Format Standards

| Stage | Format | Notes |
|---|---|---|
| `raw/` | CSV | Original format preserved |
| `interim/` | CSV, Markdown | Structured transformations |
| `processed/` | CSV, JSONL, BibTeX | Analysis-ready, documented |
| `pdfs/` | PDF | Named by DOI or arXiv ID |
| `external/` | CSV, JSON | Third-party with attribution |

---

## Adding New Data

1. **Raw data**: Place in `evidence/raw/`, preserve original format, never modify after collection.
2. **Processed data**: Create from pipeline scripts (`docdo` CLI), document in supplementary.
3. **External data**: Add to `external/` with attribution. Register in `core/governance/`.

---

## Annotations

| File | Purpose |
|---|---|
| `coding-scheme.md` | Inclusion/exclusion criteria (IC1–IC5, EC1–EC6) |
| `labeling-rules.md` | 3-model consensus voting and tie-breaking rules |

Annotations guide the AI-assisted screening from `evidence/interim/` to `evidence/processed/`.
