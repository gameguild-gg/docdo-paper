"""Tests for docdo.analysis — statistics from included studies."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from docdo.analysis import (
    architecture_distribution,
    code_availability,
    load_studies,
    organ_statistics,
    performance_statistics,
    year_distribution,
    compute_all,
    print_statistics,
    export_latex_year_table,
)


# -----------------------------------------------------------------------
# year_distribution
# -----------------------------------------------------------------------


class TestYearDistribution:
    def test_counts_years(self, sample_studies_csv: Path):
        df = pd.read_csv(sample_studies_csv)
        dist = year_distribution(df)
        assert dist[2022] == 1
        assert dist[2023] == 2

    def test_sorted(self, sample_studies_csv: Path):
        df = pd.read_csv(sample_studies_csv)
        dist = year_distribution(df)
        years = list(dist.keys())
        assert years == sorted(years)


# -----------------------------------------------------------------------
# architecture_distribution
# -----------------------------------------------------------------------


class TestArchitectureDistribution:
    def test_counts_architectures(self, sample_studies_csv: Path):
        df = pd.read_csv(sample_studies_csv)
        dist = architecture_distribution(df)
        assert dist["U-Net"] == 2
        assert dist["Transformer"] == 1

    def test_missing_column(self):
        df = pd.DataFrame({"year": [2022]})
        dist = architecture_distribution(df)
        assert dist == {}


# -----------------------------------------------------------------------
# performance_statistics
# -----------------------------------------------------------------------


class TestPerformanceStatistics:
    def test_dice_stats(self, sample_studies_csv: Path):
        df = pd.read_csv(sample_studies_csv)
        stats = performance_statistics(df)
        assert "dice" in stats
        assert stats["dice"]["count"] == 2  # only method studies with values
        assert stats["dice"]["mean"] == pytest.approx(0.935)

    def test_hd95_stats(self, sample_studies_csv: Path):
        df = pd.read_csv(sample_studies_csv)
        stats = performance_statistics(df)
        assert "hd95" in stats
        assert stats["hd95"]["count"] == 2

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=["study_type", "dice_reported", "hd95_reported"])
        stats = performance_statistics(df)
        assert stats == {}

    def test_filters_by_study_type(self, sample_studies_csv: Path):
        df = pd.read_csv(sample_studies_csv)
        stats = performance_statistics(df)
        # S003 is benchmark type and has empty dice — should be excluded
        assert stats["dice"]["count"] == 2


# -----------------------------------------------------------------------
# organ_statistics
# -----------------------------------------------------------------------


class TestOrganStatistics:
    def test_counts_organs(self, sample_studies_csv: Path):
        df = pd.read_csv(sample_studies_csv)
        result = organ_statistics(df)
        assert result["unique_organs"] >= 3  # liver, kidney, pancreas, spleen

    def test_multi_organ_count(self, sample_studies_csv: Path):
        df = pd.read_csv(sample_studies_csv)
        result = organ_statistics(df)
        assert result["multi_organ_studies"] == 2  # S001 and S003

    def test_top_organs_list(self, sample_studies_csv: Path):
        df = pd.read_csv(sample_studies_csv)
        result = organ_statistics(df)
        top_names = [name for name, _ in result["top_organs"]]
        assert "liver" in top_names or "kidney" in top_names

    def test_missing_column(self):
        df = pd.DataFrame({"year": [2022]})
        result = organ_statistics(df)
        assert result["unique_organs"] == 0


# -----------------------------------------------------------------------
# code_availability
# -----------------------------------------------------------------------


class TestCodeAvailability:
    def test_availability_rate(self, sample_studies_csv: Path):
        df = pd.read_csv(sample_studies_csv)
        result = code_availability(df)
        assert result["code_available"] == 1  # S001 only (method type)
        assert result["total_methods"] == 2
        assert result["availability_rate"] == pytest.approx(0.5)

    def test_no_code_column(self):
        df = pd.DataFrame({"study_type": ["method"], "year": [2023]})
        result = code_availability(df)
        assert result["availability_rate"] == 0.0


# -----------------------------------------------------------------------
# compute_all
# -----------------------------------------------------------------------


class TestComputeAll:
    def test_returns_all_sections(self, sample_studies_csv: Path):
        stats = compute_all(path=sample_studies_csv)
        assert "total" in stats
        assert "years" in stats
        assert "architectures" in stats
        assert "performance" in stats
        assert "organs" in stats
        assert "code_availability" in stats
        assert stats["total"] == 3


# -----------------------------------------------------------------------
# print_statistics
# -----------------------------------------------------------------------


class TestPrintStatistics:
    def test_does_not_crash(self, sample_studies_csv: Path, capsys):
        stats = compute_all(path=sample_studies_csv)
        print_statistics(stats)
        captured = capsys.readouterr()
        assert "Year Distribution" in captured.out
        assert "Architecture Distribution" in captured.out


# -----------------------------------------------------------------------
# export_latex_year_table
# -----------------------------------------------------------------------


class TestExportLatexYearTable:
    def test_creates_tex_file(self, sample_studies_csv: Path, tmp_path: Path):
        stats = compute_all(path=sample_studies_csv)
        export_latex_year_table(stats, tmp_path)
        tex_file = tmp_path / "year_distribution.tex"
        assert tex_file.exists()
        content = tex_file.read_text(encoding="utf-8")
        assert "\\begin{tabular}" in content
        assert "2022" in content
        assert "2023" in content
