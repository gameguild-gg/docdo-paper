# Datasets Metadata

JSON-LD metadata files for research datasets.

## Structure

```
datasets/
├── annotations.jsonld
├── evidence.jsonld
└── taxonomies.jsonld
```

## Template

```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Your Dataset Name",
  "description": "What the dataset contains",
  "creator": {
    "@type": "Person",
    "@id": "../person.jsonld"
  },
  "datePublished": "2026-01-01",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "distribution": {
    "@type": "DataDownload",
    "encodingFormat": "application/json",
    "contentUrl": "path/to/data"
  }
}
```
