"""Centralized configuration: paths, environment, and constants."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Repository root detection
# ---------------------------------------------------------------------------
# Walk up from this file to find the repo root (contains pyproject.toml).
_THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT: Path = _THIS_DIR.parent.parent.parent  # operations/src/docdo → repo root

# Load .env from repo root
load_dotenv(REPO_ROOT / ".env")

# ---------------------------------------------------------------------------
# Directory layout (6-bucket context model)
# ---------------------------------------------------------------------------
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
DATA_DIR = ARTIFACTS_DIR / "data"
EVIDENCE_DIR = DATA_DIR / "evidence"
RAW_DIR = EVIDENCE_DIR / "raw"
INTERIM_DIR = EVIDENCE_DIR / "interim"
PROCESSED_DIR = EVIDENCE_DIR / "processed"
PDF_DIR = EVIDENCE_DIR / "pdfs"
SUPPLEMENTARY_DIR = EVIDENCE_DIR / "supplementary"

SCHOLAR_DIR = REPO_ROOT / "scholar" / "bib"
WORK_DIR = REPO_ROOT / "work" / "projects" / "papers" / "docdo-paper"

# Derived paths — files
S1_RAW = RAW_DIR / "S1_search_results_REAL.csv"
S1_DEDUP = INTERIM_DIR / "S1_search_results_deduplicated.csv"
S2_SCREENED = PROCESSED_DIR / "S2_screened.csv"
S2_ES_FILTERED = PROCESSED_DIR / "S2_elasticsearch_filtered.csv"
BATCH_DIR = PROCESSED_DIR / "batches"
FINAL_DIR = PROCESSED_DIR / "final_results"

REFERENCES_BIB = SCHOLAR_DIR / "references.bib"
MAIN_TEX = WORK_DIR / "main.tex"

# ---------------------------------------------------------------------------
# OpenAI defaults
# ---------------------------------------------------------------------------
DEFAULT_MODEL = os.getenv("DOCDO_MODEL", "gpt-4o-mini")
BATCH_MODEL = os.getenv("DOCDO_BATCH_MODEL", "gpt-4o-mini")
FULLTEXT_MODEL = os.getenv("DOCDO_FULLTEXT_MODEL", "gpt-4o")
TIEBREAKER_MODEL = os.getenv("DOCDO_TIEBREAKER_MODEL", "gpt-5.2")
API_TIMEOUT = float(os.getenv("DOCDO_API_TIMEOUT", "60"))

# Screening parameters
NUM_RUNS = int(os.getenv("DOCDO_NUM_RUNS", "3"))
TEMPERATURE = float(os.getenv("DOCDO_TEMPERATURE", "0.3"))
BATCH_SIZE = int(os.getenv("DOCDO_BATCH_SIZE", "500"))

# Fetching
UNPAYWALL_EMAIL = os.getenv("DOCDO_EMAIL", "survey_search@literature.review")
PUBMED_EMAIL = UNPAYWALL_EMAIL
MAX_FETCH_WORKERS = int(os.getenv("DOCDO_MAX_WORKERS", "3"))
FETCH_DELAY = float(os.getenv("DOCDO_FETCH_DELAY", "1.0"))


def openai_api_key() -> str:
    """Return the OpenAI API key or raise."""
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise EnvironmentError(
            "OPENAI_API_KEY not set. Export it or add to .env at repo root."
        )
    return key


def ensure_dirs() -> None:
    """Create standard output directories if they don't exist."""
    for d in (RAW_DIR, INTERIM_DIR, PROCESSED_DIR, BATCH_DIR, FINAL_DIR, PDF_DIR):
        d.mkdir(parents=True, exist_ok=True)
