# Public Datasets

This directory holds redistributable dataset artifacts.

Each dataset lives in its own folder, versioned as `vX.Y.Z/`.

## Registered Datasets

See `core/governance/registry/datasets.yaml` for the canonical registry.

## Expected Layout

```
datasets/
└── <dataset-name>/
    └── vX.Y.Z/
        ├── data/               # Derived artifacts (CSV, Parquet)
        ├── dataset_card.md     # Documentation
        ├── LICENSE-DATASET     # License
        └── checksums.sha256    # Integrity verification
```

## Policy

Only derived, non-copyrighted outputs belong here. See [data-policy.md](../../../documentation/data-policy.md).
