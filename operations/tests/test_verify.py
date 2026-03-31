"""Tests for docdo.verify — traceability checks."""

from __future__ import annotations

from pathlib import Path

import pytest

from docdo.verify import verify_traceability


class TestVerifyTraceability:
    def test_full_traceability(self, sample_csv: Path, tmp_path: Path):
        """When all S2 papers exist in S1, traceability should be FULL."""
        import csv

        # Create S2 CSV with only papers that exist in S1
        s2_path = tmp_path / "s2.csv"
        with s2_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh, fieldnames=["study_id", "title", "doi", "first_author", "year"]
            )
            writer.writeheader()
            writer.writerow({
                "study_id": "S001",
                "title": "3D U-Net for Liver Segmentation from CT Scans",
                "doi": "10.1234/mia.2023.001",
                "first_author": "Smith",
                "year": "2023",
            })

        report = tmp_path / "trace_report.txt"
        found, not_found, level = verify_traceability(
            s1_path=sample_csv,
            s2_path=s2_path,
            report_path=report,
        )
        assert found == 1
        assert not_found == 0
        assert level == "FULL"
        assert report.exists()

    def test_partial_traceability(self, sample_csv: Path, sample_s2_csv: Path, tmp_path: Path):
        """When some S2 papers are missing from S1, traceability < FULL."""
        report = tmp_path / "trace_report.txt"
        found, not_found, level = verify_traceability(
            s1_path=sample_csv,
            s2_path=sample_s2_csv,
            report_path=report,
        )
        assert found >= 1  # "3D U-Net for Liver Segmentation" exists
        assert not_found >= 1  # "Novel Paper Not in S1" missing
        assert report.exists()

    def test_writes_report_file(self, sample_csv: Path, sample_s2_csv: Path, tmp_path: Path):
        report = tmp_path / "nested" / "report.txt"
        verify_traceability(
            s1_path=sample_csv,
            s2_path=sample_s2_csv,
            report_path=report,
        )
        assert report.exists()
        content = report.read_text(encoding="utf-8")
        assert "TRACEABILITY" in content
        assert "S1 file" in content

    def test_doi_matching(self, tmp_path: Path):
        """DOI matching should work across prefix differences."""
        import csv

        # S1 with doi prefix
        s1 = tmp_path / "s1.csv"
        with s1.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=["title", "doi"])
            writer.writeheader()
            writer.writerow({"title": "Paper A", "doi": "https://doi.org/10.1234/test"})

        # S2 with clean doi
        s2 = tmp_path / "s2.csv"
        with s2.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh, fieldnames=["study_id", "title", "doi", "first_author", "year"]
            )
            writer.writeheader()
            writer.writerow({
                "study_id": "S1",
                "title": "Paper A",
                "doi": "10.1234/test",
                "first_author": "X",
                "year": "2023",
            })

        report = tmp_path / "report.txt"
        found, not_found, level = verify_traceability(
            s1_path=s1, s2_path=s2, report_path=report,
        )
        assert found == 1
        assert not_found == 0
        assert level == "FULL"
