"""Tests for docdo.cli — Click CLI invocations via CliRunner."""

from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from docdo.cli import main


@pytest.fixture()
def runner():
    return CliRunner()


class TestCLI:
    def test_help(self, runner: CliRunner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "systematic review" in result.output.lower()

    def test_version(self, runner: CliRunner):
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_unknown_command(self, runner: CliRunner):
        result = runner.invoke(main, ["nonexistent-command"])
        assert result.exit_code != 0

    def test_deduplicate_command_exists(self, runner: CliRunner):
        result = runner.invoke(main, ["deduplicate", "--help"])
        assert result.exit_code == 0
        assert "dedup" in result.output.lower() or "CSV" in result.output or "--input" in result.output or "help" in result.output.lower()

    def test_stats_command_exists(self, runner: CliRunner):
        result = runner.invoke(main, ["stats", "--help"])
        assert result.exit_code == 0

    def test_fetch_pubmed_command_exists(self, runner: CliRunner):
        result = runner.invoke(main, ["fetch-pubmed", "--help"])
        assert result.exit_code == 0
        assert "--query" in result.output or "--max-results" in result.output

    def test_verify_dois_command_exists(self, runner: CliRunner):
        result = runner.invoke(main, ["verify-dois", "--help"])
        assert result.exit_code == 0

    def test_verify_traceability_command_exists(self, runner: CliRunner):
        result = runner.invoke(main, ["verify-traceability", "--help"])
        assert result.exit_code == 0

    def test_screen_command_exists(self, runner: CliRunner):
        result = runner.invoke(main, ["screen", "--help"])
        assert result.exit_code == 0

    def test_screen_batch_command_exists(self, runner: CliRunner):
        result = runner.invoke(main, ["screen-batch", "--help"])
        assert result.exit_code == 0

    def test_deduplicate_with_files(self, runner: CliRunner, sample_csv, tmp_path):
        """Test actual deduplication via CLI."""
        out = tmp_path / "cli_dedup.csv"
        result = runner.invoke(main, [
            "deduplicate",
            "--input", str(sample_csv),
            "--output", str(out),
        ])
        assert result.exit_code == 0
        assert out.exists()
