# Pipeline

The systematic review runs through these stages, each mapped to a CLI command:

```
PubMed / arXiv / Semantic Scholar
        │
        ▼
   fetch-pubmed          → artifacts/data/evidence/raw/
        │
        ▼
   deduplicate           → artifacts/data/evidence/interim/
        │
        ▼
   screen / screen-batch → artifacts/data/evidence/processed/
        │
        ▼
   compile               → 3-model consensus (strict + nano + gpt52)
        │
        ▼
   fetch-pdfs / fetch-oa → artifacts/data/evidence/pdfs/
        │
        ▼
   verify-dois           → spot-check DOI resolution
   verify-traceability   → S2 papers ⊆ S1 searches
        │
        ▼
   stats                 → descriptive statistics, LaTeX tables
```

The Makefile wraps these into `make fetch-pubmed`, `make deduplicate`, `make screen`, etc.
See `make help` for the full list.
