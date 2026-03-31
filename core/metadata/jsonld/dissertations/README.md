# Dissertations Metadata

JSON-LD metadata files for dissertations and theses.

## Structure

```
dissertations/
├── phd-dissertation.jsonld
└── masters-thesis.jsonld
```

## Template

```json
{
  "@context": "https://schema.org",
  "@type": "Thesis",
  "name": "Your Dissertation Title",
  "author": {
    "@type": "Person",
    "@id": "../person.jsonld"
  },
  "datePublished": "2026-01-01",
  "inSupportOf": {
    "@type": "EducationalOccupationalCredential",
    "credentialCategory": "PhD",
    "recognizedBy": {
      "@type": "Organization",
      "name": "Your University"
    }
  }
}
```
