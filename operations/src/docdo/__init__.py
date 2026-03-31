"""
docdo — PRISMA Systematic Review Pipeline Toolkit.

A library for automating systematic literature reviews following
PRISMA 2020 guidelines, with AI-assisted screening via OpenAI.

Modules:
    config          Centralized paths, settings, environment loading
    io              CSV / JSON / PDF I/O helpers
    openai_utils    OpenAI client factory, batch ops, JSON parsing
    screening       Screening prompts, multi-run voting, batch pipeline
    fetch           PubMed, arXiv, Unpaywall paper fetching
    dedup           Search-result deduplication
    verify          DOI resolution, S2→S1 traceability
    analysis        Descriptive statistics for included studies
    cli             Click-based command-line interface
"""

__version__ = "0.1.0"
