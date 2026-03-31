# Research Repository Metadata

This directory contains [Schema.org](https://schema.org) structured metadata for all research outputs in this repository.

## Purpose

Schema.org JSON-LD metadata enables:
- **Machine-readable descriptions** of research outputs
- **Discoverability** via search engines (Google Dataset Search, Google Scholar)
- **Semantic linking** between related works
- **Standardized citation** information
- **Integration** with knowledge graphs and academic platforms

## Structure

```
metadata/
├── README.md
└── jsonld/                              # Schema.org JSON-LD descriptors
    ├── person.jsonld                    # Author profile (customize this!)
    ├── dissertations/
    │   └── README.md                    # Templates for thesis metadata
    ├── frameworks/
    │   └── README.md                    # Templates for framework metadata
    ├── papers/
    │   └── README.md                    # Templates for paper metadata
    └── datasets/
        └── README.md                    # Templates for dataset metadata
```

## Schema Types Used

| Content Type | Schema.org Type | Location |
|--------------|-----------------|----------|
| Author | `Person` | `jsonld/person.jsonld` |
| Dissertation | `Thesis` | `jsonld/dissertations/*.jsonld` |
| Papers | `ScholarlyArticle` | `jsonld/papers/*.jsonld` |
| Frameworks | `CreativeWork` + `DefinedTermSet` | `jsonld/frameworks/*.jsonld` |
| Datasets | `Dataset` | `jsonld/datasets/*.jsonld` |

## Relationship to Data Schemas

| Location | Format | Purpose |
|----------|--------|---------|
| `metadata/jsonld/` | JSON-LD | **Describes** research outputs (schema.org vocabulary) |
| `data/schemas/json-schema/` | JSON Schema | **Validates** data entries (structural validation) |

## Usage

### JSON-LD in HTML

Embed in `<head>` sections:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Thesis",
  "name": "Your Thesis Title",
  ...
}
</script>
```

### Academic Platforms

These schemas are compatible with:
- Google Scholar
- Microsoft Academic
- Semantic Scholar
- ORCID
- ResearchGate

### Citation Management

Import into:
- Zotero
- Mendeley
- EndNote

## Validation

Validate schemas at:
- https://validator.schema.org/
- https://search.google.com/test/rich-results

## Maintenance

Update metadata when:
- Publication status changes
- DOIs are assigned
- New works are added
- Affiliations change

## License

All metadata files use CC BY 4.0 license to match repository content.
