# Data Schemas

Validation schemas for structured data in this repository.

---

## Purpose

JSON Schema files define the **structure and validation rules** for screening
results and data extraction outputs, ensuring consistency across the pipeline.

## Structure

```
schemas/
├── README.md
└── json-schema/
    └── (add project-specific schemas here)
```

## Planned Schemas

| Schema | Purpose |
|--------|---------|
| `screening-result.schema.json` | Validates S2/S3 screening JSON output |
| `data-extraction.schema.json` | Validates S3 full-text extraction records |

## Screening Result Format

```json
{
  "decision": "INCLUDE",
  "confidence": 85,
  "rationale": "Proposes 3D U-Net for liver segmentation from CT scans.",
  "criteria_met": ["IC1", "IC2", "IC3", "IC4", "IC5"],
  "criteria_failed": []
}
```

## References

- https://json-schema.org/
