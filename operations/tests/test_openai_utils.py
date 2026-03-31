"""Tests for docdo.openai_utils — JSON parsing, batch helpers."""

from __future__ import annotations

import json

import pytest

from docdo.openai_utils import (
    create_batch_request,
    extract_batch_content,
    parse_json_response,
    strip_code_fences,
)


# -----------------------------------------------------------------------
# strip_code_fences
# -----------------------------------------------------------------------


class TestStripCodeFences:
    def test_removes_json_fence(self):
        text = '```json\n{"key": "value"}\n```'
        result = strip_code_fences(text)
        assert result == '{"key": "value"}'

    def test_removes_plain_fence(self):
        text = '```\n{"a": 1}\n```'
        result = strip_code_fences(text)
        assert result == '{"a": 1}'

    def test_no_fences_passthrough(self):
        text = '{"decision": "INCLUDE"}'
        assert strip_code_fences(text) == text

    def test_empty_string(self):
        assert strip_code_fences("") == ""

    def test_none_becomes_empty(self):
        assert strip_code_fences(None) == ""

    def test_whitespace_around_fences(self):
        text = '  ```json\n  {"x": 1}\n  ```  '
        result = strip_code_fences(text)
        assert '"x"' in result


# -----------------------------------------------------------------------
# parse_json_response
# -----------------------------------------------------------------------


class TestParseJSONResponse:
    def test_clean_json(self):
        text = '{"decision": "INCLUDE", "confidence": 85}'
        parsed, err = parse_json_response(text)
        assert err == ""
        assert parsed["decision"] == "INCLUDE"
        assert parsed["confidence"] == 85

    def test_json_with_code_fences(self):
        text = '```json\n{"decision": "EXCLUDE"}\n```'
        parsed, err = parse_json_response(text)
        assert err == ""
        assert parsed["decision"] == "EXCLUDE"

    def test_json_embedded_in_text(self):
        text = 'Here is the result: {"decision": "INCLUDE", "confidence": 90} Done.'
        parsed, err = parse_json_response(text)
        assert err == ""
        assert parsed["decision"] == "INCLUDE"

    def test_completely_invalid(self):
        text = "This is not JSON at all."
        parsed, err = parse_json_response(text)
        assert parsed is None
        assert "json_parse_error" in err

    def test_malformed_json_with_brace(self):
        text = '{"decision": "INCLUDE", broken'
        parsed, err = parse_json_response(text)
        assert parsed is None
        assert err != ""

    def test_empty_string(self):
        parsed, err = parse_json_response("")
        assert parsed is None


# -----------------------------------------------------------------------
# create_batch_request
# -----------------------------------------------------------------------


class TestCreateBatchRequest:
    def test_basic_structure(self):
        req = create_batch_request(
            custom_id="paper1__run1",
            prompt="Test prompt",
        )
        assert req["custom_id"] == "paper1__run1"
        assert req["method"] == "POST"
        assert req["url"] == "/v1/chat/completions"
        assert "body" in req

    def test_includes_system_message(self):
        req = create_batch_request(
            custom_id="id1",
            prompt="Hello",
            system="You are a reviewer.",
        )
        messages = req["body"]["messages"]
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"

    def test_no_system_message(self):
        req = create_batch_request(custom_id="id1", prompt="Hello")
        messages = req["body"]["messages"]
        assert len(messages) == 1
        assert messages[0]["role"] == "user"

    def test_json_mode(self):
        req = create_batch_request(
            custom_id="id1", prompt="Test", json_mode=True
        )
        assert req["body"]["response_format"] == {"type": "json_object"}

    def test_default_model(self):
        from docdo import config

        req = create_batch_request(custom_id="id1", prompt="Test")
        assert req["body"]["model"] == config.BATCH_MODEL

    def test_custom_model(self):
        req = create_batch_request(
            custom_id="id1", prompt="Test", model="gpt-custom"
        )
        assert req["body"]["model"] == "gpt-custom"

    def test_temperature_default(self):
        from docdo import config

        req = create_batch_request(custom_id="id1", prompt="Test")
        assert req["body"]["temperature"] == config.TEMPERATURE


# -----------------------------------------------------------------------
# extract_batch_content
# -----------------------------------------------------------------------


class TestExtractBatchContent:
    def test_successful_result(self):
        result = {
            "response": {
                "status_code": 200,
                "body": {
                    "choices": [
                        {"message": {"content": '{"decision": "INCLUDE"}'}}
                    ]
                },
            }
        }
        content, err = extract_batch_content(result)
        assert err == ""
        assert '"INCLUDE"' in content

    def test_error_result(self):
        result = {
            "response": {"status_code": 500},
            "error": {"message": "Internal server error"},
        }
        content, err = extract_batch_content(result)
        assert content is None
        assert "api_error" in err

    def test_missing_choices(self):
        result = {
            "response": {"status_code": 200, "body": {"choices": []}},
        }
        content, err = extract_batch_content(result)
        assert content is None
        assert "missing_choices" in err

    def test_empty_response(self):
        result = {}
        content, err = extract_batch_content(result)
        assert content is None

    def test_none_content(self):
        result = {
            "response": {
                "status_code": 200,
                "body": {"choices": [{"message": {"content": None}}]},
            }
        }
        content, err = extract_batch_content(result)
        assert err == ""
        assert content == ""  # None → str("")
