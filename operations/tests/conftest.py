"""Shared pytest fixtures for docdo tests."""

from __future__ import annotations

import csv
import json
import textwrap
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest


# ---------------------------------------------------------------------------
# Temporary file fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_csv(tmp_path: Path) -> Path:
    """Create a minimal S1-like CSV with a few records."""
    rows = [
        {
            "id": "R0001",
            "database": "PubMed",
            "search_date": "2024-01-01",
            "title": "3D U-Net for Liver Segmentation from CT Scans",
            "authors": "Smith J; Doe A",
            "year": "2023",
            "journal_conference": "Medical Image Analysis",
            "doi": "10.1234/mia.2023.001",
            "abstract_snippet": "We propose a novel 3D U-Net variant for automatic liver segmentation from abdominal CT scans. " * 3,
        },
        {
            "id": "R0002",
            "database": "arXiv",
            "search_date": "2024-01-01",
            "title": "Transformer-based Multi-organ Segmentation",
            "authors": "Lee K",
            "year": "2022",
            "journal_conference": "MICCAI",
            "doi": "10.5678/miccai.2022.042",
            "abstract_snippet": "A transformer architecture for segmenting 12 abdominal organs in CT volumes.",
        },
        {
            "id": "R0003",
            "database": "PubMed",
            "search_date": "2024-01-01",
            "title": "3D U-Net for Liver Segmentation from CT Scans",  # duplicate title
            "authors": "Smith J",
            "year": "2023",
            "journal_conference": "",
            "doi": "10.1234/mia.2023.001",  # duplicate DOI
            "abstract_snippet": "Short.",
        },
        {
            "id": "R0004",
            "database": "Semantic Scholar",
            "search_date": "2024-01-01",
            "title": "SVM-based Lung Segmentation from X-ray",
            "authors": "Williams P",
            "year": "2021",
            "journal_conference": "IJCARS",
            "doi": "",
            "abstract_snippet": "Traditional machine learning for lung boundary detection.",
        },
    ]
    path = tmp_path / "search_results.csv"
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


@pytest.fixture()
def sample_s2_csv(tmp_path: Path) -> Path:
    """Create a minimal S2 included-studies CSV."""
    rows = [
        {
            "study_id": "S001",
            "title": "3D U-Net for Liver Segmentation from CT Scans",
            "doi": "10.1234/mia.2023.001",
            "first_author": "Smith",
            "year": "2023",
        },
        {
            "study_id": "S002",
            "title": "Novel Paper Not in S1",
            "doi": "10.9999/novel.2024",
            "first_author": "Unknown",
            "year": "2024",
        },
    ]
    path = tmp_path / "s2_studies.csv"
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


@pytest.fixture()
def sample_jsonl(tmp_path: Path) -> Path:
    """Create a sample JSONL file."""
    items = [
        {"id": 1, "text": "hello"},
        {"id": 2, "text": "world"},
    ]
    path = tmp_path / "data.jsonl"
    with path.open("w", encoding="utf-8") as fh:
        for item in items:
            fh.write(json.dumps(item) + "\n")
    return path


@pytest.fixture()
def sample_bib(tmp_path: Path) -> Path:
    """Create a sample BibTeX file."""
    content = textwrap.dedent("""\
        @article{smith2023liver,
          author = {Smith, J.},
          title = {3D U-Net for Liver Segmentation},
          year = {2023},
        }

        @inproceedings{lee2022transformer,
          author = {Lee, K.},
          title = {Transformer Multi-organ Segmentation},
          year = {2022},
        }
    """)
    path = tmp_path / "refs.bib"
    path.write_text(content, encoding="utf-8")
    return path


@pytest.fixture()
def sample_studies_csv(tmp_path: Path) -> Path:
    """Create a studies CSV for analysis tests."""
    rows = [
        {
            "study_id": "S001",
            "year": "2022",
            "architecture": "U-Net",
            "architecture_type": "U-Net",
            "study_type": "method",
            "dice_reported": "0.95",
            "hd95_reported": "3.2",
            "organ_focus": "liver;kidney",
            "code_available": "yes",
        },
        {
            "study_id": "S002",
            "year": "2023",
            "architecture": "nnU-Net",
            "architecture_type": "U-Net",
            "study_type": "method",
            "dice_reported": "0.92",
            "hd95_reported": "4.1",
            "organ_focus": "pancreas",
            "code_available": "no",
        },
        {
            "study_id": "S003",
            "year": "2023",
            "architecture": "Swin UNETR",
            "architecture_type": "Transformer",
            "study_type": "benchmark",
            "dice_reported": "",
            "hd95_reported": "",
            "organ_focus": "liver;spleen;kidney",
            "code_available": "yes",
        },
    ]
    path = tmp_path / "studies.csv"
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


@pytest.fixture()
def mock_openai_response() -> dict[str, Any]:
    """A mock screening JSON response from the LLM."""
    return {
        "decision": "INCLUDE",
        "confidence": 85,
        "rationale": "Proposes 3D U-Net for liver segmentation from CT.",
        "criteria_met": ["IC1", "IC2", "IC3", "IC4", "IC5"],
        "criteria_failed": [],
    }


@pytest.fixture()
def mock_batch_results() -> list[dict]:
    """Sample batch API result lines."""
    def _make(custom_id: str, decision: str, confidence: int) -> dict:
        return {
            "custom_id": custom_id,
            "response": {
                "status_code": 200,
                "body": {
                    "choices": [
                        {
                            "message": {
                                "content": json.dumps(
                                    {
                                        "decision": decision,
                                        "confidence": confidence,
                                        "rationale": f"Test {decision}",
                                        "criteria_met": ["IC1"] if decision == "INCLUDE" else [],
                                        "criteria_failed": ["EC1"] if decision == "EXCLUDE" else [],
                                    }
                                )
                            }
                        }
                    ]
                },
            },
        }

    return [
        _make("paper1__run1", "INCLUDE", 85),
        _make("paper1__run2", "INCLUDE", 90),
        _make("paper1__run3", "INCLUDE", 80),
        _make("paper2__run1", "INCLUDE", 75),
        _make("paper2__run2", "EXCLUDE", 70),
        _make("paper2__run3", "INCLUDE", 80),
    ]
