# PDFs — v2 Full-Text Acquisition

Directory for full-text PDFs of S2v2-included studies (Task 7 acquisition
target) and reference/background papers.

## Layout

```text
pdfs/
├── *.pdf                 # auto-acquired full texts (Task 7: OA-first, campus-IP)
├── manual-inbox/         # user-placed PDFs ONLY (ingested by docdo in Task 7)
└── README.md             # this file
```

## Naming convention (binding)

Every PDF is named by its **DOI or arXiv id**, slash- and colon-free:

| Source | Pattern | Example |
|--------|---------|---------|
| DOI | `<doi-with-slashes-replaced-by-underscores>.pdf` | `10.1016_j.media.2024.103207.pdf` |
| arXiv | `arXiv:<id>.pdf` (colon kept, no version suffix) | `arXiv:2406.05285.pdf`, `arXiv:2203.12362.pdf` |
| No identifier | `<first-author>-<year>-<first-3-title-words>.pdf` | `guo-2022-auto3dseg-benchmark.pdf` (last resort) |

Notes:

- v1 convention (`doi` slashes → underscores, e.g. `10.1088/1361-6560_aaf11c`)
  is preserved for join tooling (`pdf_filename` stem == `paper_id`).
- **Verified seed arXiv ids for inbox naming (Task 6 execution check):**
  MONAI framework paper `arXiv:2211.02701`; MONAI Label `arXiv:2203.12362`;
  VISTA3D `arXiv:2406.05285`; nnInteractive `arXiv:2503.08373`;
  U-Mamba `arXiv:2401.04722`; SegVol `arXiv:2311.13385`; MedSAM
  `arXiv:2304.12306`; SAM-Med3D `arXiv:2310.15161`; clDice `arXiv:2003.07311`.
  The plan's pinned ids 2011.08506 / 2209.13545 / 2203.12345 are WRONG
  (verified 2026-09-08 — they resolve to unrelated papers); do not use them.

## manual-inbox/ (user hand-off point)

Place PDFs you fetched personally here (paywalled items, library scans,
anything the automated routes could not obtain). Task 7 ingests them by the
naming convention above; anything placed here is treated as
user-authoritative and is never re-downloaded or renamed.

## Retrieval-route URL checks (Task 6, 2026-09-08)

| Route | URL | curl GET (redirects followed) | Browser check |
|-------|-----|-------------------------------|---------------|
| LibKey | https://subjectguides.champlain.edu/libkey | **200** | — |
| ILL form | https://docs.google.com/forms/d/e/1FAIpQLScg7AfJrWHMlcHQ2dQNsXuB92LnNo_VL_5b4_4yzEY-YwQmDQ/viewform | **401** on every UA/variant retry (Google bot-blocks non-browser clients) | form renders: page title "Interlibrary Loan Request Form" — live; browser-automation route viable for Task 7 |

