# Pipelines

Pipeline definitions for the DocDo systematic review workflow.

## Review Pipeline Stages

The systematic review follows PRISMA 2020 methodology:

| Stage | Description | CLI Command |
|-------|-------------|-------------|
| **S1 — Identification** | Search databases, collect records | `docdo analyze` |
| **S2 — Screening** | Title/abstract screening against IC/EC criteria | `docdo screen` |
| **S2.5 — Deduplication** | Remove duplicate records across sources | `docdo dedup` |
| **S3 — Full-text review** | Retrieve and assess full papers | `docdo fetch` |
| **Verification** | Validate data integrity and statistics | `docdo verify` |

## Pipeline Orchestration

Pipeline orchestration is currently handled via the `Makefile` at the repository root.
Future pipeline definitions (e.g., DVC stages, Airflow DAGs) will be placed here.
