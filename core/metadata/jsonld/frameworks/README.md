# Frameworks Metadata

JSON-LD metadata files for theoretical frameworks.

## Structure

Each framework has a corresponding JSON-LD file:

```
frameworks/
├── example-framework.jsonld
└── another-framework.jsonld
```

## Template

```json
{
  "@context": "https://schema.org",
  "@type": "CreativeWork",
  "name": "Your Framework Name",
  "author": {
    "@type": "Person",
    "@id": "../person.jsonld"
  },
  "dateCreated": "2026-01-01",
  "description": "Framework description",
  "about": ["Topic 1", "Topic 2"]
}
```
