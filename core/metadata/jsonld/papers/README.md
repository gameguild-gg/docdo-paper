# Papers Metadata

JSON-LD metadata files for research papers.

## Structure

Each paper has a corresponding JSON-LD file following Schema.org's ScholarlyArticle type:

```
papers/
├── example-paper-title.jsonld
└── another-paper.jsonld
```

## Template

Use this template to create metadata for new papers:

```json
{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "name": "Your Paper Title",
  "author": {
    "@type": "Person",
    "@id": "../person.jsonld"
  },
  "datePublished": "2026-01-01",
  "description": "Paper abstract or summary",
  "keywords": ["keyword1", "keyword2"],
  "inSupportOf": {
    "@type": "ResearchProject",
    "name": "Your Research Project"
  }
}
```

## Naming Convention

Use kebab-case matching the paper folder name:
- `my-first-paper.jsonld`
- `interaction-study.jsonld`
