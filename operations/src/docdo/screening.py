"""Screening prompts, multi-run voting, and pipeline orchestration."""

from __future__ import annotations

import time
from typing import Any

from . import config
from .openai_utils import (
    chat,
    create_batch_request,
    parse_json_response,
)

# ---------------------------------------------------------------------------
# System prompt shared by all screening commands
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are a systematic review screening assistant. "
    "Always respond with valid JSON only."
)

# ---------------------------------------------------------------------------
# Screening prompt (strict: no UNCERTAIN)
# ---------------------------------------------------------------------------
SCREENING_PROMPT = """\
You are screening papers for a systematic review on \
"3D Organ Segmentation from CT Scans using Deep Learning".

## STRICT DECISION PROTOCOL: NO "UNCERTAIN" — You must decide INCLUDE or EXCLUDE.

## INCLUSION CRITERIA (ALL must be met):

**IC1 – Deep Learning Method:**
Uses neural networks (CNN, Transformer, U-Net, encoder-decoder, attention mechanisms).
NOT: Traditional ML (SVM, Random Forest), rule-based, classical image processing.

**IC2 – 3D Volumetric Segmentation:**
Processes volumetric data with 3D spatial context (3D conv, 2.5D, or slice-based with 3D post-processing).
NOT: Pure 2D single-slice without any volumetric aggregation.

**IC3 – CT Imaging Modality:**
Uses Computed Tomography (with or without contrast, multi-modal OK if includes CT).
NOT: MRI-only, ultrasound-only, X-ray-only, PET-only.

**IC4 – Anatomical Organ Segmentation:**
Segments organs: liver, kidney, spleen, pancreas, lung, heart, stomach, gallbladder, \
bladder, prostate, colon, esophagus, adrenal glands.
NOT: Tumors/lesions only, vessels only, bones only, muscles only, airways only.
OK: Organ + tumor together, organs-at-risk for radiotherapy.

**IC5 – Original Research:**
Presents novel method, architecture, training strategy, or benchmark comparison with insights.
NOT: Pure review/survey papers, dataset-only papers, editorials.

## EXCLUSION TRIGGERS (ANY one excludes):
- EC1: Detection/classification only (no spatial segmentation)
- EC2: Non-CT modalities exclusively
- EC3: Non-organ targets exclusively (tumors, vessels, bones, muscles, COVID lesions)
- EC4: 2D-only without volumetric context
- EC5: Non-deep learning methods
- EC6: Review papers without novel methodology

## DECISION RULE:
- If ALL IC1-IC5 are clearly met and NO EC triggers → **INCLUDE**
- If ANY doubt or missing information → **EXCLUDE** (conservative approach)
- NO "UNCERTAIN" ALLOWED

---
TITLE: {title}
ABSTRACT: {abstract}
---

Return ONLY valid JSON:
{{"decision": "INCLUDE" | "EXCLUDE", "confidence": 70-95, \
"rationale": "One sentence", "criteria_met": ["IC1",...], \
"criteria_failed": ["EC1",...]}}"""


# ---------------------------------------------------------------------------
# Full-text screening prompt
# ---------------------------------------------------------------------------
S3_CRITERIA = """\
## S3 Full-Text Screening Criteria

### INCLUDE if ALL of the following:
1. **Deep Learning Focus**: Uses deep learning (CNN, U-Net, Transformer, etc.) as PRIMARY method
2. **3D/Volumetric**: Processes 3D CT volumes (not just 2D slices independently)
3. **Organ Segmentation**: Segments anatomical organs (liver, kidney, spleen, pancreas, etc.)
4. **CT Modality**: Uses CT scans (not MRI, ultrasound, or X-ray only)
5. **Evaluation**: Reports quantitative metrics (Dice, IoU, Hausdorff, etc.)
6. **Novel Contribution**: Presents new method, architecture, or significant improvement

### EXCLUDE if ANY of the following:
1. Review/Survey without novel method
2. Deep learning is not the primary segmentation method
3. Only processes 2D slices without 3D context
4. Focuses on non-CT modalities
5. Only segments tumors/lesions, not organs
6. No quantitative evaluation metrics reported
7. Only applies existing methods without methodological contribution"""

DATA_EXTRACTION_SCHEMA: dict[str, str] = {
    "paper_id": "string – identifier from filename",
    "title": "string – paper title",
    "authors": "string – first author et al.",
    "year": "integer – publication year",
    "venue": "string – journal/conference name",
    "architecture": "string – main architecture (U-Net, V-Net, nnU-Net, Transformer, etc.)",
    "architecture_details": "string – specific variant or modifications",
    "is_3d": "boolean – true if 3D convolutions used",
    "loss_function": "string – loss function(s) used",
    "preprocessing": "string – preprocessing steps",
    "postprocessing": "string – postprocessing steps if any",
    "datasets": "list – dataset names used",
    "dataset_size": "string – number of CT scans/patients",
    "organs_segmented": "list – which organs",
    "multi_organ": "boolean – segments multiple organs",
    "best_dice": "float – best reported Dice score (0-1 or %)",
    "dice_per_organ": "dict – Dice scores per organ if reported",
    "other_metrics": "dict – other metrics (IoU, Hausdorff, etc.)",
    "comparison_methods": "list – methods compared against",
    "framework": "string – PyTorch, TensorFlow, etc.",
    "gpu_used": "string – GPU model if mentioned",
    "training_time": "string – training time if mentioned",
    "inference_time": "string – inference time if mentioned",
    "code_available": "boolean – is code publicly available",
    "code_url": "string – URL to code if available",
    "limitations": "string – stated limitations",
    "future_work": "string – suggested future work",
}

import json

def build_fulltext_prompt(paper_id: str, pdf_text: str) -> str:
    """Build the S3 full-text screening + extraction prompt."""
    return (
        "You are reviewing a scientific paper for a systematic review on "
        '"3D Organ Segmentation from CT Scans using Deep Learning".\n\n'
        f"{S3_CRITERIA}\n\n"
        "## Your Task\n"
        "1. **SCREEN**: Determine if this paper should be INCLUDED or EXCLUDED.\n"
        "2. **EXTRACT**: If INCLUDED, extract data per the schema below.\n\n"
        f"## Data Extraction Schema:\n{json.dumps(DATA_EXTRACTION_SCHEMA, indent=2)}\n\n"
        f"## Paper ID: {paper_id}\n\n"
        f"## Paper Content:\n{pdf_text}\n\n"
        '## Response (JSON only):\n'
        '{"screening_decision": "INCLUDE"|"EXCLUDE", '
        '"exclusion_reason": "...", "confidence": 0.0-1.0, '
        '"screening_notes": "...", "extracted_data": {...}}'
    )


# ---------------------------------------------------------------------------
# Single-paper screen (synchronous, with N runs)
# ---------------------------------------------------------------------------

def _parse_screening_result(text: str | None) -> dict[str, Any]:
    """Parse a single screening JSON response with defaults."""
    if not text:
        return _error_result("empty_response")

    parsed, err = parse_json_response(text)
    if err or parsed is None:
        return _error_result(err or "parse_error")

    # Apply defaults
    parsed.setdefault("decision", "EXCLUDE")
    parsed.setdefault("confidence", 50)
    parsed.setdefault("rationale", "")
    parsed.setdefault("criteria_met", [])
    parsed.setdefault("criteria_failed", [])
    return parsed


def _error_result(reason: str) -> dict[str, Any]:
    return {
        "decision": "EXCLUDE",
        "confidence": 0,
        "rationale": reason,
        "criteria_met": [],
        "criteria_failed": [],
    }


def screen_paper_once(
    title: str,
    abstract: str,
    *,
    model: str | None = None,
) -> dict[str, Any]:
    """Run a single screening pass on one paper."""
    prompt = SCREENING_PROMPT.format(
        title=title or "No title",
        abstract=abstract or "No abstract available",
    )
    text = chat(prompt, system=SYSTEM_PROMPT, model=model)
    return _parse_screening_result(text)


def determine_final_decision(
    runs: list[dict[str, Any]],
) -> dict[str, Any]:
    """Apply unanimous voting across screening runs.

    ``INCLUDE`` only if **all** runs agree; otherwise ``EXCLUDE``.
    """
    decisions = [r["decision"] for r in runs]
    confidences = [r["confidence"] for r in runs]

    n = len(runs)
    include_count = decisions.count("INCLUDE")
    avg_conf = sum(confidences) / n if n else 0

    final = "INCLUDE" if include_count == n else "EXCLUDE"

    result: dict[str, Any] = {
        "final_decision": final,
        "avg_confidence": avg_conf,
        "rationale": runs[0]["rationale"] if runs else "",
    }
    # Per-run details
    all_met: set[str] = set()
    all_failed: set[str] = set()
    for i, r in enumerate(runs, 1):
        result[f"run_{i}_decision"] = r["decision"]
        result[f"run_{i}_confidence"] = r["confidence"]
        all_met.update(r.get("criteria_met", []))
        all_failed.update(r.get("criteria_failed", []))

    result["criteria_met"] = ",".join(sorted(str(c) for c in all_met))
    result["criteria_failed"] = ",".join(sorted(str(c) for c in all_failed))
    return result


def screen_paper(
    title: str,
    abstract: str,
    *,
    num_runs: int | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """Screen a paper with *num_runs* independent passes + unanimous voting."""
    num_runs = num_runs or config.NUM_RUNS
    runs: list[dict[str, Any]] = []
    for _ in range(num_runs):
        runs.append(screen_paper_once(title, abstract, model=model))
        time.sleep(0.3)
    # Pad missing runs
    while len(runs) < num_runs:
        runs.append(_error_result("run_failed"))
    return determine_final_decision(runs)


# ---------------------------------------------------------------------------
# Batch request builders
# ---------------------------------------------------------------------------

def build_screening_batch_requests(
    papers: list[dict[str, str]],
    *,
    num_runs: int | None = None,
    model: str | None = None,
) -> list[dict]:
    """Build JSONL batch requests for all papers × num_runs."""
    num_runs = num_runs or config.NUM_RUNS
    requests: list[dict] = []
    for paper in papers:
        paper_id = paper.get("doi") or paper.get("id") or paper.get("title", "")[:50]
        title = paper.get("title", "")
        abstract = paper.get("abstract_snippet", "") or paper.get("abstract", "")
        prompt = SCREENING_PROMPT.format(
            title=title or "No title",
            abstract=abstract or "No abstract available",
        )
        for run in range(1, num_runs + 1):
            requests.append(
                create_batch_request(
                    custom_id=f"{paper_id}__run{run}",
                    prompt=prompt,
                    system=SYSTEM_PROMPT,
                    model=model,
                )
            )
    return requests


def build_fulltext_batch_requests(
    pdf_dir: str | None = None,
    *,
    model: str | None = None,
    max_chars: int = 45_000,
) -> list[dict]:
    """Build batch requests for S3 full-text screening from PDFs."""
    from .io import extract_pdf_text

    pdf_dir_path = config.PDF_DIR if pdf_dir is None else __import__("pathlib").Path(pdf_dir)
    model = model or config.FULLTEXT_MODEL
    requests: list[dict] = []

    for pdf in sorted(pdf_dir_path.glob("*.pdf")):
        text = extract_pdf_text(pdf, max_chars=max_chars)
        if text.startswith("ERROR"):
            continue
        prompt = build_fulltext_prompt(pdf.stem, text)
        requests.append(
            create_batch_request(
                custom_id=f"s3_screen_{pdf.stem}",
                prompt=prompt,
                model=model,
                max_tokens=4000,
                json_mode=True,
            )
        )
    return requests


def parse_screening_batch_results(
    results: list[dict],
) -> dict[str, dict[str, Any]]:
    """Parse batch JSONL results into ``{paper_id: {run_N: decision_dict}}``."""
    from .openai_utils import extract_batch_content

    decisions: dict[str, dict[str, Any]] = {}
    for result in results:
        cid = result.get("custom_id", "")
        if "__run" in cid:
            paper_id, run_part = cid.rsplit("__run", 1)
            run_key = f"run_{run_part}"
        else:
            paper_id = cid
            run_key = "run_1"

        decisions.setdefault(paper_id, {})
        content, err = extract_batch_content(result)
        if err or content is None:
            decisions[paper_id][run_key] = _error_result(err)
            continue

        parsed, perr = parse_json_response(content)
        if perr or parsed is None:
            decisions[paper_id][run_key] = _error_result(perr)
        else:
            d = parsed.get("decision", "EXCLUDE")
            if d not in ("INCLUDE", "EXCLUDE"):
                d = "EXCLUDE"
            decisions[paper_id][run_key] = {
                "decision": d,
                "confidence": parsed.get("confidence", 50),
                "rationale": parsed.get("rationale", ""),
                "criteria_met": parsed.get("criteria_met", []),
                "criteria_failed": parsed.get("criteria_failed", []),
            }
    return decisions


def unanimous_vote(runs: dict[str, dict]) -> tuple[str, float, str]:
    """Apply unanimous-INCLUDE rule to per-run dicts.

    Returns ``(decision, avg_confidence, rationale)``.
    """
    valid = [r for r in runs.values() if r.get("decision") in ("INCLUDE", "EXCLUDE")]
    if not valid:
        return "EXCLUDE", 0.0, "no_valid_runs"
    inc = sum(1 for r in valid if r["decision"] == "INCLUDE")
    avg = sum(r.get("confidence", 50) for r in valid) / len(valid)
    if inc == len(valid):
        return "INCLUDE", avg, f"{inc}/{len(valid)} INCLUDE (unanimous)"
    return "EXCLUDE", avg, f"{inc}I/{len(valid) - inc}E – no consensus"
