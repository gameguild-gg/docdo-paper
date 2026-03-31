# External Data

Third-party datasets and benchmarks referenced by the systematic review on
**3D Organ Segmentation from CT Scans using Deep Learning**.

## Structure

```
external/
├── benchmarks/   # Public segmentation benchmarks (e.g., Medical Decathlon)
├── catalogs/     # Dataset registries, metadata catalogs
├── evidence/     # External evidence snapshots (API dumps, web captures)
└── staging/      # Temporary staging for incoming data
```

## Policy

- Nothing in `external/` is redistributable by default.
- Public releases go through `artifacts/data/public/`.
- Every source should be registered in `core/governance/registry/`.
