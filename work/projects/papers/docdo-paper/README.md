# DocDo Paper — Deep Learning for 3D CT Organ Segmentation

This directory contains the LaTeX source for the systematic review paper.

## Files

| File | Description |
|------|-------------|
| `main.tex` | Current paper source (IEEE Conference format) |
| `main_full.tex` | Extended version of the paper |
| `main_old.tex` | Previous version (archive) |
| `Makefile` | Build automation |

## Building

```bash
make        # Full build with bibliography
make quick  # Quick build (no bibtex)
make clean  # Remove build artifacts
```

## Bibliography

References are located in `scholar/bib/` at the repository root:
- `references.bib` — Primary bibliography
- `additional-references.bib` — Supplementary references
- `reviewed-papers.bib` — Papers included in the review
