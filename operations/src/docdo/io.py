"""I/O helpers for CSV, JSON, PDF, and BibTeX files."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

def read_csv(path: Path | str) -> list[dict[str, str]]:
    """Read a CSV and return list of dicts (all values as strings)."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(
    path: Path | str,
    rows: list[dict[str, Any]],
    fieldnames: list[str] | None = None,
) -> Path:
    """Write list of dicts to CSV. Infers fieldnames from first row if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not fieldnames and rows:
        fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames or [])
        writer.writeheader()
        writer.writerows(rows)
    return path


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

def read_json(path: Path | str) -> Any:
    """Read a JSON file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path | str, data: Any, indent: int = 2) -> Path:
    """Write data to a JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=indent, ensure_ascii=False), encoding="utf-8")
    return path


def read_jsonl(path: Path | str) -> list[dict]:
    """Read a JSONL file (one JSON object per line)."""
    lines = Path(path).read_text(encoding="utf-8").strip().split("\n")
    return [json.loads(line) for line in lines if line.strip()]


def write_jsonl(path: Path | str, items: list[dict]) -> Path:
    """Write a JSONL file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for item in items:
            fh.write(json.dumps(item, ensure_ascii=False) + "\n")
    return path


# ---------------------------------------------------------------------------
# PDF text extraction
# ---------------------------------------------------------------------------

def extract_pdf_text(
    pdf_path: Path | str,
    max_pages: int = 30,
    max_chars: int = 50_000,
) -> str:
    """Extract text from a PDF using PyMuPDF (fitz).

    Returns the extracted text or a string starting with ``ERROR`` on failure.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return "ERROR: PyMuPDF not installed. Run: pip install PyMuPDF"

    try:
        doc = fitz.open(str(pdf_path))
        parts: list[str] = []
        total = 0
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            text = page.get_text()
            parts.append(text)
            total += len(text)
            if total > max_chars:
                break
        doc.close()
        return "".join(parts)[:max_chars]
    except Exception as exc:
        return f"ERROR extracting PDF: {exc}"


# ---------------------------------------------------------------------------
# BibTeX helpers
# ---------------------------------------------------------------------------

_BIB_KEY_RE = re.compile(r"@\w+\{([^,]+),")


def parse_bib_keys(path: Path | str) -> set[str]:
    """Return the set of BibTeX citation keys in a .bib file."""
    text = Path(path).read_text(encoding="utf-8")
    return {m.group(1).strip() for m in _BIB_KEY_RE.finditer(text)}
