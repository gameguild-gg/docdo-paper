# FAQ

**What is this repo?**
Data, scripts, and governance for a PRISMA 2020 systematic review on deep learning for 3D organ segmentation in CT. The LaTeX paper lives in [docdo-paper](https://github.com/game-guild/docdo-paper).

**How do I install?**
`pip install -e ".[dev]"` — then `docdo --help`.

**What CLI commands exist?**
`fetch-pubmed`, `fetch-pdfs`, `fetch-oa`, `deduplicate`, `screen`, `screen-batch`, `check-batch`, `download-batch`, `compile`, `verify-dois`, `verify-traceability`, `stats`. See `docdo --help` for details.

**Where do search results go?**
`artifacts/data/evidence/` — raw CSV exports, deduplicated files, screening results.

**Where do PDFs go?**
`artifacts/data/evidence/pdfs/` — downloaded papers.

**What can be made public?**
Only `artifacts/data/public/`. PDFs and raw search exports stay private.

**How do I run tests?**
`pytest operations/tests/ -v --cov=docdo`

**What methodology?**
PRISMA 2020. Searching PubMed, arXiv, Semantic Scholar. AI-assisted screening with 3-model unanimous voting (GPT-4o-mini "strict", GPT-4o-mini "nano", GPT-4.5-preview). Human validation on disagreements.
