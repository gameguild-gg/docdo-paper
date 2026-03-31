# Core

Rules, theory, and machine-readable identity for the project.

## Contents

| Directory | Purpose |
|-----------|---------|
| `governance/` | Research control: policies, registries, evidence ledger, legal, templates |
| `conceptual-architecture/` | Canon (definitions, notation) + theoretical foundations (literature synthesis) |
| `metadata/` | Machine-readable metadata (JSON-LD, structured data for tools) |

## Governance at a glance

```text
governance/
├── registry/        # Single source of truth (sources.yaml, datasets.yaml, id-maps/)
├── evidence/        # Audit trail ledger (metadata only; references artifacts/data/)
├── legal/           # Legal snapshots + release compliance
├── guidelines/      # Operational conventions (commits, workflows)
├── quality-assurance/
├── research-criteria/
├── research-log/
├── templates/
├── venues/
├── claims.md
├── decision-log.md
├── editorial-principles.md
└── terminology-matrix.md
```

## Key files

- [governance/registry/sources.yaml](governance/registry/sources.yaml) — external source definitions
- [governance/registry/datasets.yaml](governance/registry/datasets.yaml) — public dataset releases
- [governance/legal/release-compliance.md](governance/legal/release-compliance.md) — pre-release checklist
