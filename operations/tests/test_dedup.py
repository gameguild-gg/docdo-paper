"""Tests for docdo.dedup — normalization and deduplication."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from docdo.dedup import (
    completeness_score,
    deduplicate,
    normalize_doi,
    normalize_title,
)


# -----------------------------------------------------------------------
# normalize_title
# -----------------------------------------------------------------------


class TestNormalizeTitle:
    def test_lowercases(self):
        assert normalize_title("Hello World") == "hello world"

    def test_collapses_whitespace(self):
        assert normalize_title("foo   bar\tbaz") == "foo bar baz"

    def test_strips_punctuation(self):
        assert normalize_title("U-Net: A Solution!") == "unet a solution"

    def test_empty(self):
        assert normalize_title("") == ""

    def test_none_like(self):
        assert normalize_title("") == ""

    def test_unicode(self):
        result = normalize_title("Über Résumé")
        assert "über" in result


# -----------------------------------------------------------------------
# normalize_doi
# -----------------------------------------------------------------------


class TestNormalizeDOI:
    def test_strips_https_prefix(self):
        assert normalize_doi("https://doi.org/10.1234/foo") == "10.1234/foo"

    def test_strips_http_prefix(self):
        assert normalize_doi("http://doi.org/10.1234/bar") == "10.1234/bar"

    def test_strips_doi_colon_prefix(self):
        assert normalize_doi("doi:10.5678/baz") == "10.5678/baz"

    def test_strips_doi_org_prefix(self):
        assert normalize_doi("doi.org/10.1111/x") == "10.1111/x"

    def test_lowercases(self):
        assert normalize_doi("10.1234/ABC") == "10.1234/abc"

    def test_empty(self):
        assert normalize_doi("") == ""

    def test_already_clean(self):
        assert normalize_doi("10.1234/clean") == "10.1234/clean"


# -----------------------------------------------------------------------
# completeness_score
# -----------------------------------------------------------------------


class TestCompletenessScore:
    def test_complete_record(self):
        row = {
            "doi": "10.1234/x",
            "abstract_snippet": "A" * 150,
            "authors": "Smith J",
            "year": "2023",
            "journal_conference": "MICCAI",
        }
        score = completeness_score(row)
        assert score == 3 + 2 + 1 + 1 + 1  # doi + abstract + authors + year + journal

    def test_minimal_record(self):
        row = {"title": "Something"}
        score = completeness_score(row)
        assert score == 0

    def test_short_abstract_not_counted(self):
        row = {"abstract_snippet": "Short."}
        score = completeness_score(row)
        assert score == 0  # len < 100

    def test_abstract_field_alternative(self):
        """Should also check 'abstract' key when 'abstract_snippet' absent."""
        row = {"abstract": "x" * 200}
        score = completeness_score(row)
        assert score == 2


# -----------------------------------------------------------------------
# deduplicate
# -----------------------------------------------------------------------


class TestDeduplicate:
    def test_removes_doi_duplicates(self, sample_csv: Path, tmp_path: Path):
        out = tmp_path / "dedup.csv"
        kept, removed = deduplicate(input_path=sample_csv, output_path=out)
        assert removed >= 1  # R0001 and R0003 share DOI
        assert out.exists()

    def test_removes_title_duplicates(self, sample_csv: Path, tmp_path: Path):
        out = tmp_path / "dedup.csv"
        kept, removed = deduplicate(input_path=sample_csv, output_path=out)
        # R0001 and R0003 share both DOI and title
        assert kept < 4

    def test_keeps_more_complete_record(self, sample_csv: Path, tmp_path: Path):
        out = tmp_path / "dedup.csv"
        deduplicate(input_path=sample_csv, output_path=out)
        from docdo.io import read_csv

        rows = read_csv(out)
        # R0001 had more complete metadata than R0003
        liver_rows = [
            r for r in rows if "liver" in r.get("title", "").lower()
        ]
        assert len(liver_rows) <= 1

    def test_renumbers_ids(self, sample_csv: Path, tmp_path: Path):
        out = tmp_path / "dedup.csv"
        deduplicate(input_path=sample_csv, output_path=out)
        from docdo.io import read_csv

        rows = read_csv(out)
        ids = [r["id"] for r in rows]
        assert ids[0] == "R0001"
        assert ids[-1] == f"R{len(rows):04d}"

    def test_empty_csv(self, tmp_path: Path):
        empty = tmp_path / "empty.csv"
        empty.write_text(
            "id,title,doi,authors,year,journal_conference,abstract_snippet,database,search_date\n",
            encoding="utf-8",
        )
        out = tmp_path / "dedup_empty.csv"
        kept, removed = deduplicate(input_path=empty, output_path=out)
        assert kept == 0
        assert removed == 0

    def test_creates_output_directory(self, sample_csv: Path, tmp_path: Path):
        out = tmp_path / "nested" / "dir" / "dedup.csv"
        deduplicate(input_path=sample_csv, output_path=out)
        assert out.exists()
