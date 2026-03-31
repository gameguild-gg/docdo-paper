"""Tests for docdo.screening — parsing, voting, and batch builders."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import patch

import pytest

from docdo.screening import (
    SCREENING_PROMPT,
    S3_CRITERIA,
    DATA_EXTRACTION_SCHEMA,
    _parse_screening_result,
    _error_result,
    determine_final_decision,
    build_screening_batch_requests,
    parse_screening_batch_results,
    unanimous_vote,
    build_fulltext_prompt,
)


# -----------------------------------------------------------------------
# _error_result
# -----------------------------------------------------------------------


class TestErrorResult:
    def test_returns_exclude(self):
        r = _error_result("test_reason")
        assert r["decision"] == "EXCLUDE"
        assert r["confidence"] == 0
        assert r["rationale"] == "test_reason"
        assert r["criteria_met"] == []
        assert r["criteria_failed"] == []


# -----------------------------------------------------------------------
# _parse_screening_result
# -----------------------------------------------------------------------


class TestParseScreeningResult:
    def test_valid_json(self):
        text = json.dumps({
            "decision": "INCLUDE",
            "confidence": 85,
            "rationale": "Good paper",
            "criteria_met": ["IC1", "IC2"],
            "criteria_failed": [],
        })
        r = _parse_screening_result(text)
        assert r["decision"] == "INCLUDE"
        assert r["confidence"] == 85

    def test_none_input(self):
        r = _parse_screening_result(None)
        assert r["decision"] == "EXCLUDE"
        assert r["rationale"] == "empty_response"

    def test_empty_string(self):
        r = _parse_screening_result("")
        assert r["decision"] == "EXCLUDE"
        assert r["rationale"] == "empty_response"

    def test_invalid_json(self):
        r = _parse_screening_result("not json")
        assert r["decision"] == "EXCLUDE"
        assert "error" in r["rationale"].lower()

    def test_defaults_applied(self):
        text = json.dumps({"confidence": 70})
        r = _parse_screening_result(text)
        assert r["decision"] == "EXCLUDE"  # default
        assert r["criteria_met"] == []
        assert r["criteria_failed"] == []

    def test_json_in_code_fence(self):
        text = '```json\n{"decision": "INCLUDE", "confidence": 90}\n```'
        r = _parse_screening_result(text)
        assert r["decision"] == "INCLUDE"


# -----------------------------------------------------------------------
# determine_final_decision (unanimous voting)
# -----------------------------------------------------------------------


class TestDetermineFinalDecision:
    def _run(self, decision: str, confidence: int) -> dict[str, Any]:
        return {
            "decision": decision,
            "confidence": confidence,
            "rationale": f"Test {decision}",
            "criteria_met": ["IC1"] if decision == "INCLUDE" else [],
            "criteria_failed": ["EC1"] if decision == "EXCLUDE" else [],
        }

    def test_unanimous_include(self):
        runs = [self._run("INCLUDE", 85), self._run("INCLUDE", 90), self._run("INCLUDE", 80)]
        result = determine_final_decision(runs)
        assert result["final_decision"] == "INCLUDE"
        assert result["avg_confidence"] == pytest.approx(85.0)

    def test_not_unanimous_excludes(self):
        runs = [self._run("INCLUDE", 85), self._run("EXCLUDE", 70), self._run("INCLUDE", 80)]
        result = determine_final_decision(runs)
        assert result["final_decision"] == "EXCLUDE"

    def test_all_exclude(self):
        runs = [self._run("EXCLUDE", 60), self._run("EXCLUDE", 55)]
        result = determine_final_decision(runs)
        assert result["final_decision"] == "EXCLUDE"

    def test_per_run_details(self):
        runs = [self._run("INCLUDE", 85), self._run("INCLUDE", 90)]
        result = determine_final_decision(runs)
        assert result["run_1_decision"] == "INCLUDE"
        assert result["run_2_decision"] == "INCLUDE"
        assert result["run_1_confidence"] == 85

    def test_criteria_aggregation(self):
        runs = [
            self._run("INCLUDE", 85),
            {
                "decision": "INCLUDE",
                "confidence": 80,
                "rationale": "ok",
                "criteria_met": ["IC1", "IC3"],
                "criteria_failed": [],
            },
        ]
        result = determine_final_decision(runs)
        assert "IC1" in result["criteria_met"]
        assert "IC3" in result["criteria_met"]


# -----------------------------------------------------------------------
# unanimous_vote
# -----------------------------------------------------------------------


class TestUnanimousVote:
    def test_all_include(self):
        runs = {
            "run_1": {"decision": "INCLUDE", "confidence": 85},
            "run_2": {"decision": "INCLUDE", "confidence": 90},
            "run_3": {"decision": "INCLUDE", "confidence": 80},
        }
        decision, avg, rationale = unanimous_vote(runs)
        assert decision == "INCLUDE"
        assert "unanimous" in rationale.lower()

    def test_mixed_votes(self):
        runs = {
            "run_1": {"decision": "INCLUDE", "confidence": 85},
            "run_2": {"decision": "EXCLUDE", "confidence": 70},
        }
        decision, avg, rationale = unanimous_vote(runs)
        assert decision == "EXCLUDE"
        assert "no consensus" in rationale.lower()

    def test_empty_runs(self):
        decision, avg, rationale = unanimous_vote({})
        assert decision == "EXCLUDE"
        assert avg == 0.0

    def test_invalid_decisions_filtered(self):
        runs = {
            "run_1": {"decision": "MAYBE", "confidence": 50},
            "run_2": {"decision": "INCLUDE", "confidence": 80},
        }
        decision, avg, rationale = unanimous_vote(runs)
        # Only one valid run with INCLUDE, so it's unanimous among valid
        assert decision == "INCLUDE"


# -----------------------------------------------------------------------
# build_screening_batch_requests
# -----------------------------------------------------------------------


class TestBuildScreeningBatchRequests:
    def test_generates_correct_count(self):
        papers = [
            {"id": "p1", "title": "Paper One", "abstract_snippet": "Abstract one."},
            {"id": "p2", "title": "Paper Two", "abstract_snippet": "Abstract two."},
        ]
        requests = build_screening_batch_requests(papers, num_runs=3)
        assert len(requests) == 6  # 2 papers × 3 runs

    def test_custom_ids_include_run_number(self):
        papers = [{"doi": "10.1234/test", "title": "Test", "abstract_snippet": "Abs"}]
        requests = build_screening_batch_requests(papers, num_runs=2)
        ids = [r["custom_id"] for r in requests]
        assert "10.1234/test__run1" in ids
        assert "10.1234/test__run2" in ids

    def test_uses_doi_as_id(self):
        papers = [{"doi": "10.1234/x", "title": "T", "abstract_snippet": "A"}]
        reqs = build_screening_batch_requests(papers, num_runs=1)
        assert reqs[0]["custom_id"].startswith("10.1234/x")

    def test_falls_back_to_title(self):
        papers = [{"title": "A Long Paper Title Indeed", "abstract_snippet": "A"}]
        reqs = build_screening_batch_requests(papers, num_runs=1)
        assert "A Long Paper Title Indeed" in reqs[0]["custom_id"]

    def test_empty_papers(self):
        reqs = build_screening_batch_requests([], num_runs=3)
        assert len(reqs) == 0


# -----------------------------------------------------------------------
# parse_screening_batch_results
# -----------------------------------------------------------------------


class TestParseScreeningBatchResults:
    def test_groups_by_paper(self, mock_batch_results):
        decisions = parse_screening_batch_results(mock_batch_results)
        assert "paper1" in decisions
        assert "paper2" in decisions

    def test_run_keys(self, mock_batch_results):
        decisions = parse_screening_batch_results(mock_batch_results)
        assert "run_1" in decisions["paper1"]
        assert "run_2" in decisions["paper1"]
        assert "run_3" in decisions["paper1"]

    def test_decisions_parsed(self, mock_batch_results):
        decisions = parse_screening_batch_results(mock_batch_results)
        assert decisions["paper1"]["run_1"]["decision"] == "INCLUDE"
        assert decisions["paper2"]["run_2"]["decision"] == "EXCLUDE"

    def test_error_result_on_api_failure(self):
        results = [
            {
                "custom_id": "paper3__run1",
                "response": {"status_code": 500},
                "error": {"message": "Server error"},
            }
        ]
        decisions = parse_screening_batch_results(results)
        assert decisions["paper3"]["run_1"]["decision"] == "EXCLUDE"


# -----------------------------------------------------------------------
# Prompt constants
# -----------------------------------------------------------------------


class TestPromptConstants:
    def test_screening_prompt_has_placeholders(self):
        assert "{title}" in SCREENING_PROMPT
        assert "{abstract}" in SCREENING_PROMPT

    def test_screening_prompt_has_criteria(self):
        assert "IC1" in SCREENING_PROMPT
        assert "EC1" in SCREENING_PROMPT

    def test_s3_criteria_not_empty(self):
        assert len(S3_CRITERIA) > 100

    def test_data_extraction_schema_has_keys(self):
        assert "architecture" in DATA_EXTRACTION_SCHEMA
        assert "best_dice" in DATA_EXTRACTION_SCHEMA
        assert "code_available" in DATA_EXTRACTION_SCHEMA


# -----------------------------------------------------------------------
# build_fulltext_prompt
# -----------------------------------------------------------------------


class TestBuildFulltextPrompt:
    def test_includes_paper_id(self):
        prompt = build_fulltext_prompt("paper123", "Some PDF text here")
        assert "paper123" in prompt

    def test_includes_pdf_text(self):
        prompt = build_fulltext_prompt("p1", "We present a 3D U-Net")
        assert "3D U-Net" in prompt

    def test_includes_criteria(self):
        prompt = build_fulltext_prompt("p1", "text")
        assert "INCLUDE" in prompt
        assert "EXCLUDE" in prompt
