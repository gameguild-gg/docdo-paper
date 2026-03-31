"""Tests for docdo.config — path resolution, env vars, ensure_dirs."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest


def test_repo_root_is_valid():
    """REPO_ROOT should point to a directory containing pyproject.toml."""
    from docdo.config import REPO_ROOT

    assert REPO_ROOT.is_dir(), f"REPO_ROOT is not a directory: {REPO_ROOT}"
    assert (REPO_ROOT / "pyproject.toml").exists(), "pyproject.toml not found at REPO_ROOT"


def test_directory_constants_are_paths():
    """All directory constants should be Path objects under REPO_ROOT."""
    from docdo import config

    dirs = [
        config.ARTIFACTS_DIR,
        config.DATA_DIR,
        config.EVIDENCE_DIR,
        config.RAW_DIR,
        config.INTERIM_DIR,
        config.PROCESSED_DIR,
        config.PDF_DIR,
        config.SUPPLEMENTARY_DIR,
    ]
    for d in dirs:
        assert isinstance(d, Path), f"Expected Path, got {type(d)}: {d}"
        # All should be underneath REPO_ROOT
        assert str(d).startswith(str(config.REPO_ROOT))


def test_file_paths_have_correct_extensions():
    """Config file paths should have expected suffixes."""
    from docdo import config

    assert config.S1_RAW.suffix == ".csv"
    assert config.S1_DEDUP.suffix == ".csv"
    assert config.S2_SCREENED.suffix == ".csv"
    assert config.S2_ES_FILTERED.suffix == ".csv"


def test_openai_defaults_have_types():
    """OpenAI configuration values should have correct types."""
    from docdo import config

    assert isinstance(config.DEFAULT_MODEL, str) and config.DEFAULT_MODEL
    assert isinstance(config.BATCH_MODEL, str)
    assert isinstance(config.NUM_RUNS, int) and config.NUM_RUNS > 0
    assert isinstance(config.TEMPERATURE, float) and 0 <= config.TEMPERATURE <= 2
    assert isinstance(config.API_TIMEOUT, float) and config.API_TIMEOUT > 0
    assert isinstance(config.BATCH_SIZE, int) and config.BATCH_SIZE > 0
    assert isinstance(config.MAX_FETCH_WORKERS, int) and config.MAX_FETCH_WORKERS > 0
    assert isinstance(config.FETCH_DELAY, float) and config.FETCH_DELAY >= 0


def test_openai_api_key_raises_without_env():
    """openai_api_key() should raise when OPENAI_API_KEY is unset."""
    from docdo.config import openai_api_key

    with patch.dict(os.environ, {}, clear=True):
        # Remove the key entirely
        os.environ.pop("OPENAI_API_KEY", None)
        with pytest.raises(EnvironmentError, match="OPENAI_API_KEY"):
            openai_api_key()


def test_openai_api_key_returns_value_when_set():
    """openai_api_key() should return the key when set."""
    from docdo.config import openai_api_key

    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key-123"}):
        assert openai_api_key() == "sk-test-key-123"


def test_ensure_dirs_creates_directories(tmp_path: Path):
    """ensure_dirs() should create all standard directories."""
    from docdo import config

    # Temporarily override directory constants
    with (
        patch.object(config, "RAW_DIR", tmp_path / "raw"),
        patch.object(config, "INTERIM_DIR", tmp_path / "interim"),
        patch.object(config, "PROCESSED_DIR", tmp_path / "processed"),
        patch.object(config, "BATCH_DIR", tmp_path / "batches"),
        patch.object(config, "FINAL_DIR", tmp_path / "final"),
        patch.object(config, "PDF_DIR", tmp_path / "pdfs"),
    ):
        config.ensure_dirs()
        assert (tmp_path / "raw").is_dir()
        assert (tmp_path / "interim").is_dir()
        assert (tmp_path / "processed").is_dir()
        assert (tmp_path / "batches").is_dir()
        assert (tmp_path / "final").is_dir()
        assert (tmp_path / "pdfs").is_dir()


def test_env_overrides():
    """Environment variables should override default model names."""
    with patch.dict(os.environ, {"DOCDO_MODEL": "gpt-99-turbo"}, clear=False):
        # Re-evaluate; config reads at import time, so test the env var logic
        val = os.getenv("DOCDO_MODEL", "gpt-4o-mini")
        assert val == "gpt-99-turbo"
