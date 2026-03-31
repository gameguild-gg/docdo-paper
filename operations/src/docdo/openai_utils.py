"""OpenAI client factory, batch operations, and JSON response parsing."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from openai import OpenAI

from . import config

# ---------------------------------------------------------------------------
# Client factory
# ---------------------------------------------------------------------------

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """Return a singleton OpenAI client (lazily created)."""
    global _client
    if _client is None:
        try:
            import httpx

            _client = OpenAI(
                api_key=config.openai_api_key(),
                timeout=httpx.Timeout(config.API_TIMEOUT, connect=10.0),
            )
        except ImportError:
            _client = OpenAI(api_key=config.openai_api_key())
    return _client


# ---------------------------------------------------------------------------
# JSON response parsing
# ---------------------------------------------------------------------------

_JSON_OBJ_RE = re.compile(r"\{.*\}", re.DOTALL)


def strip_code_fences(text: str) -> str:
    """Remove markdown code fences (```json ... ```) from API output."""
    t = (text or "").strip()
    if t.startswith("```"):
        parts = t.split("```")
        if len(parts) >= 2:
            t = parts[1]
        t = t.strip()
        if t.lower().startswith("json"):
            t = t[4:].strip()
    return t


def parse_json_response(text: str) -> tuple[dict | None, str]:
    """Parse a possibly-messy JSON response from the LLM.

    Returns ``(parsed_dict, error_string)``.  ``error_string`` is empty on
    success.
    """
    clean = strip_code_fences(text)
    try:
        return json.loads(clean), ""
    except Exception:
        m = _JSON_OBJ_RE.search(clean)
        if m:
            try:
                return json.loads(m.group(0)), ""
            except Exception as exc:
                return None, f"json_extract_error: {exc}"
        return None, "json_parse_error"


# ---------------------------------------------------------------------------
# Single-call chat completion
# ---------------------------------------------------------------------------

def chat(
    prompt: str,
    *,
    system: str = "",
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int = 300,
    retries: int = 3,
    json_mode: bool = False,
) -> str | None:
    """Run a single chat completion and return the assistant text.

    Retries on transient errors with exponential back-off.
    """
    client = get_client()
    model = model or config.DEFAULT_MODEL
    temperature = temperature if temperature is not None else config.TEMPERATURE

    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(**kwargs)
            return (resp.choices[0].message.content or "").strip()
        except Exception as exc:
            err = str(exc).lower()
            if "rate_limit" in err:
                wait = 30 * (attempt + 1)
            elif any(k in err for k in ("timeout", "connection", "network")):
                wait = 5 * (attempt + 1)
            else:
                wait = 2
            if attempt < retries - 1:
                time.sleep(wait)
            else:
                return None
    return None


# ---------------------------------------------------------------------------
# Batch API helpers
# ---------------------------------------------------------------------------

def create_batch_request(
    custom_id: str,
    prompt: str,
    *,
    system: str = "",
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int = 300,
    json_mode: bool = False,
) -> dict:
    """Build a single OpenAI Batch API request dict."""
    model = model or config.BATCH_MODEL
    temperature = temperature if temperature is not None else config.TEMPERATURE

    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}

    return {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": body,
    }


def submit_batch(
    jsonl_path: Path, description: str = ""
) -> str:
    """Upload a JSONL file and submit it as an OpenAI batch.

    Returns the batch ID.
    """
    client = get_client()

    with open(jsonl_path, "rb") as fh:
        uploaded = client.files.create(file=fh, purpose="batch")

    batch = client.batches.create(
        input_file_id=uploaded.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": description[:512]} if description else None,
    )
    return batch.id


def check_batch(batch_id: str) -> dict[str, Any]:
    """Return status info for a batch."""
    client = get_client()
    b = client.batches.retrieve(batch_id)
    return {
        "id": b.id,
        "status": b.status,
        "total": b.request_counts.total,
        "completed": b.request_counts.completed,
        "failed": b.request_counts.failed,
        "output_file_id": b.output_file_id,
    }


def download_batch_results(batch_id: str, dest: Path | None = None) -> list[dict]:
    """Download results from a completed batch. Optionally cache to *dest*.

    Returns a list of parsed JSONL result dicts.
    """
    client = get_client()
    info = check_batch(batch_id)

    if info["status"] != "completed":
        raise RuntimeError(f"Batch {batch_id} is not completed: {info['status']}")

    if not info["output_file_id"]:
        raise RuntimeError(f"Batch {batch_id} has no output file")

    content = client.files.content(info["output_file_id"])

    if dest:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content.text, encoding="utf-8")

    return [json.loads(line) for line in content.text.strip().split("\n") if line.strip()]


def wait_for_batch(batch_id: str, interval: int = 30, verbose: bool = True) -> dict:
    """Poll until a batch completes (or fails/expires/cancels)."""
    terminal = {"completed", "failed", "expired", "cancelled", "cancelling"}
    while True:
        info = check_batch(batch_id)
        if verbose:
            pct = (
                f"{100 * info['completed'] / info['total']:.0f}%"
                if info["total"]
                else "?"
            )
            print(
                f"  [{info['status']}] {info['completed']}/{info['total']} ({pct})"
            )
        if info["status"] in terminal:
            return info
        time.sleep(interval)


def extract_batch_content(result: dict) -> tuple[str | None, str]:
    """Extract the chat content from a single batch result line.

    Returns ``(content_text, error_string)``.
    """
    resp = result.get("response", {})
    if not isinstance(resp, dict):
        resp = {}

    if resp.get("status_code") == 200:
        body = resp.get("body", {})
        choices = body.get("choices", [])
        if choices:
            msg = choices[0].get("message", {})
            content = msg.get("content")
            return (str(content) if content is not None else ""), ""
        return None, "missing_choices"

    err = result.get("error", {})
    msg = err.get("message") if isinstance(err, dict) else str(err)
    return None, f"api_error: {msg}"
