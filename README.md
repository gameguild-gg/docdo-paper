# Deep Learning for 3D CT Organ Segmentation: A Systematic Review

[![LaTeX](https://img.shields.io/badge/LaTeX-IEEE%20Conference-blue)](work/projects/papers/docdo-paper/main.tex)
[![Status](https://img.shields.io/badge/Status-Ready%20for%20Submission-green)]()

A comprehensive systematic literature review of deep learning methods for 3D organ segmentation from computed tomography (CT) scans, following PRISMA 2020 guidelines.

---

## Paper

- **Manuscript:** [docdo-paper](https://github.com/game-guild/docdo-paper) (separate repo)
- **Format:** IEEE Conference
- **Studies Reviewed:** 52 peer-reviewed papers (2015–2025)

## Key Findings

| Metric | Value |
|--------|-------|
| Papers reviewed | 52 |
| Architectures compared | CNN, Transformer, Hybrid |
| Datasets analyzed | BTCV, AMOS, KiTS, MSD, TotalSegmentator |
| Best overall method | nnU-Net (self-configuring) |
| Highest Dice (liver) | 97.2% |
| Highest Dice (pancreas) | 88.1% |

## Building the Paper

The LaTeX manuscript lives in <https://github.com/game-guild/docdo-paper>.
This repo holds the data, scripts, and governance.

---

## Repository Structure

```text
docdo-paper-research/
├── core/                       # Governance, glossary, metadata
│   ├── governance/
│   │   └── research-log/       #   Development log, task board, chat log
│   ├── conceptual-architecture/
│   └── metadata/
│
├── artifacts/                  # Data: search results, PDFs, annotations
│   ├── data/
│   │   └── evidence/
│   │       ├── raw/            #   Original search exports
│   │       ├── interim/        #   Deduplicated records
│   │       ├── processed/      #   Screening batches & results
│   │       ├── pdfs/           #   Downloaded papers
│   │       └── supplementary/  #   PRISMA supplementary materials (S1–S12)
│   └── reports/
│
├── work/                       # Authored outputs
│   └── projects/papers/        #   (LaTeX lives in separate docdo-paper repo)
│
├── operations/                 # Python library + tests
│   ├── src/docdo/              #   9-module pip-installable library
│   └── tests/                  #   150 pytest tests
│
├── scholar/                    # Bibliographic infrastructure
│   └── bib/                    #   references.bib, additional-references.bib, reviewed-papers.bib
│
└── documentation/              # Documentation & reports
    └── reports/                #   Peer review, critical analysis, QA reports
```

---

## Where to Put Things

| What | Where |
|------|-------|
| Search result CSVs | `artifacts/data/evidence/` |
| Downloaded PDFs | `artifacts/data/evidence/pdfs/` |
| PRISMA supplementary data | `artifacts/data/evidence/supplementary/` |
| BibTeX files | `scholar/bib/` |
| Python code | `operations/src/docdo/` |
| Tests | `operations/tests/` |
| Reports | `documentation/reports/` |

---

## Methodology

This review follows **PRISMA 2020** guidelines with:
- Systematic search across PubMed, IEEE Xplore, arXiv
- AI-assisted screening (GPT-4o cascade with human validation)
- Quality assessment using modified QUADAS-2
- Complete audit trail in supplementary materials

## Citation

```bibtex
@article{docdo2025segmentation,
  title={Deep Learning for 3D CT Organ Segmentation: A Systematic Review},
  author={[Authors]},
  journal={[Journal]},
  year={2025}
}
```

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [documentation/repository-structure.md](documentation/repository-structure.md) | Full structure tree + architecture rationale |
| [documentation/reports/](documentation/reports/) | Peer review, critical analysis, QA reports |
| [core/governance/research-log/](core/governance/research-log/) | Development history, task board |
| [artifacts/data/evidence/supplementary/](artifacts/data/evidence/supplementary/) | PRISMA supplementary materials |

---

## License

See [LICENSE.md](LICENSE.md).
