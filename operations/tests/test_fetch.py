"""Tests for docdo.fetch — ID extraction helpers."""

from __future__ import annotations

import pytest

from docdo.fetch import extract_arxiv_id, extract_doi


# -----------------------------------------------------------------------
# extract_arxiv_id
# -----------------------------------------------------------------------


class TestExtractArxivId:
    def test_from_abs_url(self):
        assert extract_arxiv_id("https://arxiv.org/abs/2301.12345") == "2301.12345"

    def test_from_abs_url_with_version(self):
        assert extract_arxiv_id("https://arxiv.org/abs/2301.12345v2") == "2301.12345"

    def test_from_arxiv_prefix(self):
        assert extract_arxiv_id("arXiv:2301.12345") == "2301.12345"

    def test_bare_id(self):
        assert extract_arxiv_id("2301.12345") == "2301.12345"

    def test_bare_id_with_version(self):
        assert extract_arxiv_id("2301.12345v1") == "2301.12345"

    def test_no_match(self):
        assert extract_arxiv_id("10.1234/not-arxiv") is None

    def test_empty(self):
        assert extract_arxiv_id("") is None

    def test_http_url(self):
        assert extract_arxiv_id("http://arxiv.org/abs/1912.05074") == "1912.05074"

    def test_five_digit_id(self):
        assert extract_arxiv_id("2312.00001") == "2312.00001"


# -----------------------------------------------------------------------
# extract_doi
# -----------------------------------------------------------------------


class TestExtractDOI:
    def test_simple_doi(self):
        assert extract_doi("10.1234/foo.bar") == "10.1234/foo.bar"

    def test_doi_in_url(self):
        assert extract_doi("https://doi.org/10.5678/test") == "10.5678/test"

    def test_no_doi(self):
        assert extract_doi("hello world") is None

    def test_doi_with_long_registrant(self):
        assert extract_doi("10.12345/some/thing") == "10.12345/some/thing"

    def test_empty(self):
        assert extract_doi("") is None

    def test_starts_with_10(self):
        assert extract_doi("10.1016/j.media.2023.001") == "10.1016/j.media.2023.001"
