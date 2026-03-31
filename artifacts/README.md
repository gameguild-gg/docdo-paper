# Artifacts

All empirical evidence and generated outputs.

## Contents

| Directory | Purpose |
|-----------|---------|
| `data/` | Evidence pipeline (raw → interim → processed) + external sources + public releases |
| `reports/` | Generated analysis outputs (tables, figures, metrics) |

## Data at a glance

```text
data/
├── evidence/           # Search results and papers (raw → interim → processed)
│   ├── raw/            # Database exports as downloaded
│   ├── interim/        # Deduplicated, screened
│   └── processed/      # Final included papers
│
├── external/           # Third-party data (not necessarily redistributable)
│   ├── catalogs/       # Joinable metadata (IDs, platforms, organizations)
│   ├── evidence/       # Reviews, pages, media (often restricted)
│   └── staging/        # Partial downloads (ephemeral)
│
├── public/             # Redistributable outputs ONLY
│   ├── datasets/       # Versioned releases (dataset_card.md, LICENSE-DATASET, checksums)
│   └── open-media/     # Open-licensed binaries (if applicable)
│
├── catalogs/           # Reference datasets (non-evidential)
├── taxonomies/         # Classification systems
├── schemas/            # Data structure definitions
└── annotations/        # Coding infrastructure
```

## Safety rule

**Only `data/public/**` is allowed to be redistributed.**

Everything else is private/internal unless explicitly marked as open-licensed.
