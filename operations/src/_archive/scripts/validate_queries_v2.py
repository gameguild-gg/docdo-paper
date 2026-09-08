#!/usr/bin/env python3
"""Validate queries_v2.yaml against the Task-2 acceptance matrix.

Plan: .omo/plans/paper-coverage-gap-update.md (Task 2). Rules enforced:

  1.  YAML parses.
  2.  Exactly six EXECUTED families (A, B, C, D, E, G), each with one query per
      database for all four databases (PubMed, arXiv, Semantic Scholar,
      Google Scholar).
  3.  Family F exists ONLY as a shared referenced fragment: no executed family
      'F', no 'F-*' query id, no query_id on the fragment, and no query whose
      block list is a bare F fragment (standalone F execution is forbidden).
  4.  Fielded databases (pubmed, arxiv, semantic_scholar):
        - every A/C/D/E/G query has exactly three AND-blocks: family-terms,
          the (segmentation OR "medical imaging") block, and the F anatomy
          fragment (referenced block present verbatim);
        - every B query is a single block containing all nine exact tool names
          and the framework vocabulary, with NO 'AND segmentation' clause and
          NO F anatomy fragment.
  5.  Family G present in every database block.
  6.  Google Scholar matrix:
        - no fielded ti:/abs:/[tiab]/[Title/Abstract] syntax in any GS block;
        - family-B GS block: tool-name phrases present, NO anatomy terms,
          NO 'AND segmentation';
        - A/C/D/E/G GS blocks: family terms + anatomy phrases present.
  7.  Family C exact-token rule: 'SAM' and 'SAT' never appear unquoted
      (checked after stripping quoted spans; quoted exact forms required).
  8.  Plan term lists (verbatim, embedded below) present per family per DB.
  9.  Date range starts 2015-01-01 and declares an end (execution date).

Exit 0 = all checks pass. Exit 1 = one line per violation.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

DEFAULT_PATH = Path(__file__).with_name("queries_v2.yaml")
ALL_DBS = ("pubmed", "arxiv", "semantic_scholar", "google_scholar")
FIELD_DBS = ("pubmed", "arxiv", "semantic_scholar")
GS = "google_scholar"
EXECUTED = ["A", "B", "C", "D", "E", "G"]
TEMPLATE_FAMILIES = ["A", "C", "D", "E", "G"]

# Plan Task-2 verbatim term lists (authoritative ground truth for checks).
TOOL_NAMES = ["MONAI", "Auto3DSeg", "MONAI Label", "MONAI Deploy", "VISTA-3D",
              "NV-Segment-CT", "nnInteractive", "NVIDIA Clara", "Holoscan"]
FRAMEWORK_VOCAB = ["open-source framework", "medical imaging toolkit",
                   "software framework", "deployment", "microservice",
                   "inference pipeline", "clinical workflow", "PACS", "DICOM",
                   "Grand Challenge"]
WILDCARD_STEMS = ["reproducib", "radiolog", "tomograph"]
FAMILY_TERMS = {
    "A": ["neuro-symbolic", "neurosymbolic", "knowledge-guided",
          "knowledge-based", "knowledge-infused", "domain knowledge",
          "anatomical prior", "anatomical knowledge", "shape prior",
          "topological constraint", "topology-aware", "clDice", "rule-based",
          "logic-based", "constraint-based", "ontology", "RadLex",
          "knowledge graph", "interpretable segmentation", "explainable",
          "symbolic"],
    "C": ["Segment Anything", "SAM", "SAM 2", "MedSAM", "MedSAM-2",
          "SAM-Med3D", "3DSAM-Adapter", "MA-SAM", "SAMed", "MobileSAM",
          "EfficientSAM", "EdgeSAM", "HQ-SAM", "SegVol", "SAT",
          "universal model", "foundation model", "vision-language",
          "promptable", "zero-shot segmentation", "open-vocabulary",
          "interactive segmentation", "click-based", "point prompt",
          "label-efficient", "annotation-efficient", "auto-label"],
    "D": ["Mamba", "state space model", "SSM", "U-Mamba", "SegMamba",
          "diffusion model", "MedSegDiff", "SegDiff", "denoising",
          "neural architecture search", "AutoML", "self-supervised",
          "semi-supervised", "test-time adaptation", "continual learning",
          "federated", "uncertainty quantification", "ensemble"],
    "E": ["TotalSegmentator", "AMOS", "FLARE", "KiTS", "LiTS", "BraTS",
          "BTCV", "AbdomenCT-1K", "Medical Segmentation Decathlon",
          "challenge", "leaderboard"],
    "G": ["deep learning", "neural network", "convolutional", "CNN", "U-Net",
          "V-Net", "nnU-Net", "ResNet", "encoder-decoder", "transformer",
          "TransUNet", "Swin"],
}
# F anatomy content tokens ("CT" excluded: too short for substring checks).
F_CONTENT_TERMS = ["abdominal", "thoracic", "multi-organ", "whole-body",
                   "liver", "kidney", "spleen", "pancreas", "lung", "vessel",
                   "vascular", "tubular", "computed tomography"]
# GS-specific anatomy phrases that must appear in A/C/D/E/G GS queries.
GS_ANATOMY_PROBES = ["liver", "pancreas", "computed tomography", "abdominal"]
EXACT_TOKENS_C = ["SAM", "SAT"]
FIELD_SYNTAX_RE = re.compile(
    r"\bti:|\babs:|\[tiab\]|\[Title/Abstract\]", re.IGNORECASE)
AND_SEGMENTATION_RE = re.compile(r"\bAND\s*\(?\s*\"?segmentation", re.IGNORECASE)


def strip_quoted(s: str) -> str:
    """Remove double-quoted spans so bare-token checks ignore phrase forms."""
    return re.sub(r'"[^"]*"', " ", s)


def join_blocks(query: dict) -> str:
    return " AND ".join(query["blocks"])


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    errors: list[str] = []

    def err(msg: str) -> None:
        errors.append(msg)

    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        print(f"VIOLATION: yaml does not parse: {exc}")
        return 1
    if not isinstance(data, dict):
        print("VIOLATION: yaml root is not a mapping")
        return 1

    # --- structure: families and databases ---------------------------------
    fams = data.get("executed_families")
    if not isinstance(fams, dict) or set(fams) != set(EXECUTED):
        err(f"executed families must be exactly {EXECUTED}, got "
            f"{sorted(fams) if isinstance(fams, dict) else fams!r}")
        fams = fams if isinstance(fams, dict) else {}
    for fam in EXECUTED:
        if fam not in fams:
            continue
        queries = fams[fam].get("queries", {})
        missing = [db for db in ALL_DBS if db not in queries]
        if missing:
            err(f"family {fam}: missing database blocks {missing}")
            continue
        for db in ALL_DBS:
            q = queries[db]
            if not isinstance(q.get("query_id"), str) or not q["query_id"]:
                err(f"family {fam}/{db}: missing query_id")
            if q["query_id"].startswith("F-"):
                err(f"family {fam}/{db}: query_id {q['query_id']} looks like "
                    "a standalone F query (forbidden)")
            blocks = q.get("blocks")
            if (not isinstance(blocks, list) or not blocks
                    or not all(isinstance(b, str) and b.strip() for b in blocks)):
                err(f"family {fam}/{db}: blocks must be a non-empty list of "
                    "non-empty strings")

    # --- family G present in every database block --------------------------
    g = fams.get("G", {}).get("queries", {})
    for db in ALL_DBS:
        if db not in g:
            err(f"family G missing from database block {db} "
                "(must be present in every database)")

    # --- F fragment: exists, referenced, never standalone -------------------
    frag = data.get("shared_fragments", {}).get("family_F_anatomy")
    if not isinstance(frag, dict):
        err("shared_fragments.family_F_anatomy missing")
        return fail(errors)
    if frag.get("query_id") is not None or "queries" in frag:
        err("F fragment carries a query_id/queries — it must never be "
            "executable")
    frag_blocks = frag.get("blocks", {})
    for db in ALL_DBS:
        fb = frag_blocks.get(db)
        if not isinstance(fb, str) or not fb.strip():
            err(f"F fragment block for {db} missing/empty")
            continue
        for term in F_CONTENT_TERMS:
            if term not in fb:
                err(f"F fragment ({db}) missing anatomy term {term!r}")
    for fam, fam_def in fams.items():
        for db, q in fam_def.get("queries", {}).items():
            blocks = q.get("blocks", [])
            if db in frag_blocks and blocks == [frag_blocks[db]]:
                err(f"family {fam}/{db}: blocks are a bare F fragment — "
                    "standalone F execution is forbidden")

    # --- per-family content checks ------------------------------------------
    for fam in EXECUTED:
        if fam not in fams:
            continue
        for db in ALL_DBS:
            q = fams[fam]["queries"].get(db)
            if q is None:
                continue
            joined = join_blocks(q)
            blocks = q.get("blocks", [])
            if fam == "B":
                if len(blocks) != 1:
                    err(f"B/{db}: pinned template is ONE top-level block, "
                        f"got {len(blocks)}")
                for tool in TOOL_NAMES:
                    if tool not in joined:
                        err(f"B/{db}: tool name {tool!r} missing")
                for term in FRAMEWORK_VOCAB:
                    if term not in joined:
                        err(f"B/{db}: framework vocabulary {term!r} missing")
                for stem in WILDCARD_STEMS:
                    if stem not in joined.lower():
                        err(f"B/{db}: wildcard stem {stem!r} missing")
                if AND_SEGMENTATION_RE.search(joined):
                    err(f"B/{db}: family B must NOT be ANDed with "
                        "segmentation")
                if db in frag_blocks and frag_blocks[db] in blocks:
                    err(f"B/{db}: family B must not carry the F anatomy "
                        "fragment")
            else:
                if len(blocks) != 3:
                    err(f"{fam}/{db}: pinned template is exactly "
                        f"[family, context, anatomy], got {len(blocks)} blocks")
                ctx = [b for b in blocks
                       if "segmentation" in b and "medical imaging" in b]
                if not ctx:
                    err(f"{fam}/{db}: missing the (segmentation OR "
                        '"medical imaging") AND block')
                if db in frag_blocks and frag_blocks[db] not in blocks:
                    err(f"{fam}/{db}: F anatomy fragment not referenced "
                        "(family-F block absent from AND-blocks)")
                for term in FAMILY_TERMS[fam]:
                    if term not in joined:
                        err(f"{fam}/{db}: plan term {term!r} missing")
            if fam == "C":
                bare = strip_quoted(joined)
                for tok in EXACT_TOKENS_C:
                    if re.search(rf"(?<![\w-]){tok}(?![\w-])", bare):
                        err(f"C/{db}: bare token {tok!r} — exact tokens must "
                            "be quoted phrase forms, never bare substrings")
                    if f'"{tok}"' not in joined:
                        err(f"C/{db}: quoted exact form \"{tok}\" missing")
            if db == GS:
                if FIELD_SYNTAX_RE.search(joined):
                    err(f"{fam}/GS: fielded ti:/abs: syntax forbidden in "
                        "Google Scholar blocks")
                if fam == "B":
                    low = joined.lower()
                    for term in F_CONTENT_TERMS:
                        if term in low:
                            err(f"B/GS: anatomy term {term!r} forbidden in "
                                "family-B GS block")
                    if AND_SEGMENTATION_RE.search(joined):
                        err("B/GS: family-B GS block must not contain "
                            "'AND segmentation'")
                else:
                    for probe in GS_ANATOMY_PROBES:
                        if probe not in joined:
                            err(f"{fam}/GS: anatomy phrase {probe!r} missing")

    # --- date range ----------------------------------------------------------
    dr = data.get("date_range", {})
    if dr.get("start") != "2015-01-01":
        err(f"date_range.start must be '2015-01-01', got {dr.get('start')!r}")
    if not dr.get("end"):
        err("date_range.end (execution date) must be declared")

    return fail(errors)


def fail(errors: list[str]) -> int:
    if errors:
        for msg in errors:
            print(f"VIOLATION: {msg}")
        print(f"\n{len(errors)} violation(s) in queries yaml.")
        return 1
    print("queries_v2.yaml: all Task-2 acceptance checks passed "
          "(6 executed families x 4 databases, F fragment referenced and "
          "never standalone, pinned template, GS matrix, C exact tokens).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
