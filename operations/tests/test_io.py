"""Tests for docdo.io — CSV, JSON, JSONL, BibTeX, and PDF helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from docdo.io import (
    parse_bib_keys,
    read_csv,
    read_json,
    read_jsonl,
    write_csv,
    write_json,
    write_jsonl,
    extract_pdf_text,
)


# -----------------------------------------------------------------------
# CSV
# -----------------------------------------------------------------------


class TestCSV:
    def test_read_csv_returns_list_of_dicts(self, sample_csv: Path):
        rows = read_csv(sample_csv)
        assert isinstance(rows, list)
        assert len(rows) == 4
        assert rows[0]["title"] == "3D U-Net for Liver Segmentation from CT Scans"

    def test_write_then_read_roundtrip(self, tmp_path: Path):
        data = [
            {"a": "1", "b": "2"},
            {"a": "3", "b": "4"},
        ]
        out = tmp_path / "out.csv"
        write_csv(out, data)
        result = read_csv(out)
        assert len(result) == 2
        assert result[0] == {"a": "1", "b": "2"}

    def test_write_csv_creates_parent_dirs(self, tmp_path: Path):
        nested = tmp_path / "a" / "b" / "data.csv"
        write_csv(nested, [{"x": "1"}])
        assert nested.exists()

    def test_write_csv_with_explicit_fieldnames(self, tmp_path: Path):
        data = [{"x": "1", "y": "2", "z": "3"}]
        out = tmp_path / "ordered.csv"
        write_csv(out, data, fieldnames=["z", "y", "x"])
        lines = out.read_text(encoding="utf-8").strip().split("\n")
        assert lines[0] == "z,y,x"

    def test_read_csv_empty_file(self, tmp_path: Path):
        p = tmp_path / "empty.csv"
        p.write_text("a,b\n", encoding="utf-8")
        rows = read_csv(p)
        assert rows == []

    def test_write_csv_empty_rows(self, tmp_path: Path):
        out = tmp_path / "empty_rows.csv"
        write_csv(out, [])
        assert out.exists()


# -----------------------------------------------------------------------
# JSON
# -----------------------------------------------------------------------


class TestJSON:
    def test_write_then_read_json(self, tmp_path: Path):
        data = {"key": "value", "nested": {"a": 1}}
        out = tmp_path / "data.json"
        write_json(out, data)
        result = read_json(out)
        assert result == data

    def test_json_handles_unicode(self, tmp_path: Path):
        data = {"title": "Résumé — über ñ 日本語"}
        out = tmp_path / "unicode.json"
        write_json(out, data)
        result = read_json(out)
        assert result["title"] == data["title"]

    def test_write_json_creates_parent(self, tmp_path: Path):
        nested = tmp_path / "x" / "y" / "data.json"
        write_json(nested, {"ok": True})
        assert nested.exists()


# -----------------------------------------------------------------------
# JSONL
# -----------------------------------------------------------------------


class TestJSONL:
    def test_read_jsonl(self, sample_jsonl: Path):
        items = read_jsonl(sample_jsonl)
        assert len(items) == 2
        assert items[0]["id"] == 1
        assert items[1]["text"] == "world"

    def test_write_then_read_jsonl(self, tmp_path: Path):
        data = [{"a": 1}, {"b": 2}, {"c": 3}]
        out = tmp_path / "test.jsonl"
        write_jsonl(out, data)
        result = read_jsonl(out)
        assert len(result) == 3
        assert result[2] == {"c": 3}

    def test_write_jsonl_creates_parent(self, tmp_path: Path):
        nested = tmp_path / "p" / "q" / "items.jsonl"
        write_jsonl(nested, [{"x": 1}])
        assert nested.exists()


# -----------------------------------------------------------------------
# BibTeX
# -----------------------------------------------------------------------


class TestBibTeX:
    def test_parse_bib_keys(self, sample_bib: Path):
        keys = parse_bib_keys(sample_bib)
        assert keys == {"smith2023liver", "lee2022transformer"}

    def test_parse_bib_keys_empty(self, tmp_path: Path):
        p = tmp_path / "empty.bib"
        p.write_text("% just a comment\n", encoding="utf-8")
        keys = parse_bib_keys(p)
        assert keys == set()


# -----------------------------------------------------------------------
# PDF
# -----------------------------------------------------------------------


class TestPDF:
    def test_extract_pdf_text_missing_file(self, tmp_path: Path):
        """Should return an ERROR string for non-existent file."""
        result = extract_pdf_text(tmp_path / "nonexistent.pdf")
        assert result.startswith("ERROR")

    def test_extract_pdf_text_invalid_file(self, tmp_path: Path):
        """A non-PDF file should return an ERROR string."""
        p = tmp_path / "fake.pdf"
        p.write_text("This is not a PDF", encoding="utf-8")
        result = extract_pdf_text(p)
        assert result.startswith("ERROR")
