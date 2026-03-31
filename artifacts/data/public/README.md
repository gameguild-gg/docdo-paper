# Public Data (Redistributable Only)

This folder contains **only redistributable outputs** intended for publication.

## Rule

**If it is not safe to redistribute, it must not be placed here.**

Everything in this folder should be publishable as-is:
- to a public Git repository (if small)
- or as a release artifact / dataset host (if large)

## Structure

- `datasets/` — versioned dataset releases (`{dataset-name}/vX.Y.Z/`)
- `open-media/` — open-licensed binaries only (must include license metadata)

## Required files per dataset release

Each `artifacts/data/public/datasets/<dataset-name>/vX.Y.Z/` must include:
- `data/` (derived artifacts)
- `dataset_card.md`
- `LICENSE-DATASET`
- `checksums.sha256`

## Provenance

Every public release must have a matching evidence record under:
`core/governance/evidence/releases/<dataset-name>/vX.Y.Z/`
