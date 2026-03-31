# Repository Structure

```
docdo-paper-research/
├── core/
│   ├── governance/             # registry, legal, evidence ledger, guidelines
│   ├── conceptual-architecture/# glossary, theoretical foundations
│   └── metadata/               # JSON-LD metadata
│
├── artifacts/
│   ├── data/
│   │   ├── evidence/           # search results (raw → interim → processed)
│   │   │   ├── pdfs/           # downloaded papers
│   │   │   └── supplementary/  # PRISMA S1–S12
│   │   ├── external/           # third-party data (private)
│   │   ├── annotations/        # coding scheme, screening labels
│   │   └── public/             # redistributable outputs only
│   └── reports/                # generated tables, figures
│
├── work/
│   └── projects/papers/        # paper metadata (manuscript in docdo-paper repo)
│
├── operations/
│   ├── src/docdo/              # Python library (9 modules)
│   ├── tests/                  # 150 pytest tests
│   └── src/_archive/           # original 57 scripts
│
├── scholar/bib/                # references.bib, reviewed-papers.bib, etc.
│
└── documentation/              # getting-started, FAQ, pipeline docs, reports
```
