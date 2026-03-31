#!/usr/bin/env python3
"""Clusterize (group) peer-review findings into coded themes.

This reads the most recent compiled peer-review outputs and produces:
- A single clustered summary report (Markdown)
- A machine-readable JSON artifact with clusters and assignments

The clustering is rule-based (keyword/pattern matching) to avoid external dependencies
and to keep codes stable across runs.

Outputs:
- data/processed/peer_review/CLUSTERED_FINDINGS_REPORT_<timestamp>.md
- data/processed/peer_review/clustered_findings_<timestamp>.json

Run:
  ./.venv/Scripts/python.exe supplementary/scripts/cluster_peer_review_findings.py
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PEER_REVIEW_DIR = REPO_ROOT / "data" / "processed" / "peer_review"


@dataclass(frozen=True)
class Code:
    code: str
    title: str
    description: str
    patterns: Tuple[str, ...]
    response: str
    priority: int  # lower = higher priority


CODEBOOK: Tuple[Code, ...] = (
    Code(
        code="C01",
        title="Systematic review methodology credibility",
        description=(
            "Concerns about PRISMA rigor, LLM-only screening, lack of human adjudication, "
            "strict unanimity exclusion, protocol registration, and bias introduced by limited full-text retrieval."
        ),
        patterns=(
            r"\bprisma\b",
            r"\bsystematic review\b",
            r"\bprotocol\b",
            r"\bregistration\b",
            r"\bscreening\b",
            r"\bunanimity\b",
            r"\bconsensus\b",
            r"\bexclude\b",
            r"\bfull[- ]text\b",
            r"\bpdf availability\b",
            r"\bselection bias\b",
            r"\bllm\b",
            r"\bgpt\b",
            r"\bautomated\b",
        ),
        response=(
            "Strengthen Methods: add protocol details, audit/validation of screening, human adjudication plan (even retroactively), "
            "explicit sensitivity analyses (e.g., alternative inclusion rules), and discuss accessibility bias from full-text retrieval limits."
        ),
        priority=1,
    ),
    Code(
        code="C02",
        title="Scope/taxonomy misses 2D/2.5D + fusion and pragmatic pipelines",
        description=(
            "Reviewers argue the taxonomy and scope under-cover multi-view 2D / 2.5D methods with 3D fusion/voting, "
            "coarse-to-fine/cascaded pipelines, and memory-constrained deployment strategies."
        ),
        patterns=(
            r"\b2\.5d\b",
            r"\b2d\b",
            r"\bmulti[- ]view\b",
            r"\bmulti[- ]planar\b",
            r"\bfusion\b",
            r"\bvoting\b",
            r"\bmajority voting\b",
            r"\bmemory\b",
            r"\bgpu\b",
            r"\bcoarse[- ]to[- ]fine\b",
            r"\bcascade\b",
        ),
        response=(
            "Update taxonomy and related-work coverage: add a dedicated subsection for 2D/2.5D+fusion and cascaded pipelines, "
            "and clarify whether exclusions are scope-limited vs value judgments."
        ),
        priority=2,
    ),
    Code(
        code="C03",
        title="Quantitative synthesis comparability and meta-analysis limits",
        description=(
            "Concerns that Dice/HD95 numbers are aggregated across datasets/papers without harmonized evaluation (label-set mismatches, "
            "different splits/preprocessing/scripts), leading to potentially misleading comparisons."
        ),
        patterns=(
            r"\bnot comparable\b",
            r"\bcomparability\b",
            r"\bharmoniz\w*\b",
            r"\blabel set\b",
            r"\bsplit\b",
            r"\bevaluation\b",
            r"\bscript\b",
            r"\bpreprocess\w*\b",
            r"\btable\b",
            r"\bmix\w* results\b",
            r"\bmeta[- ]analysis\b",
        ),
        response=(
            "Reframe quantitative table as descriptive (not a direct leaderboard), add comparability caveats per dataset/label-set, "
            "and add a harmonized-evaluation recommendation (or a minimal re-evaluation subset if feasible)."
        ),
        priority=3,
    ),
    Code(
        code="C04",
        title="Clinical readiness over-claimed / missing clinically meaningful metrics",
        description=(
            "Concerns that deployment readiness is inferred from mean Dice deltas; reviewers request failure-mode reporting (missing organ, swaps), "
            "uncertainty/calibration, detection rates, clinical endpoints, and more nuanced discussion of QA and safety."
        ),
        patterns=(
            r"\bdeployment\b",
            r"\bclinical\b",
            r"\breadiness\b",
            r"\bmean dice\b",
            r"\bfailure\b",
            r"\bmissing organ\b",
            r"\buncertainty\b",
            r"\bcalibration\b",
            r"\bqa\b",
            r"\bsafety\b",
        ),
        response=(
            "Tone down readiness claims and add a clinical-evaluation subsection: include error modes, QA/uncertainty, calibration, "
            "and what 'deployment-ready' should mean for surgical planning workflows."
        ),
        priority=4,
    ),
    Code(
        code="C05",
        title="Coverage gaps beyond public benchmarks",
        description=(
            "Requests to include clinically relevant literature outside common public benchmarks (e.g., radiotherapy OAR, head-and-neck, specialized domains), "
            "and clarify inclusion logic when studies use private/multi-center data."
        ),
        patterns=(
            r"\boutside public\b",
            r"\bprivate dataset\b",
            r"\bmulti[- ]center\b",
            r"\bradiotherap\w*\b",
            r"\boar\b",
            r"\bhead[- ]and[- ]neck\b",
            r"\bclinically relevant literature\b",
        ),
        response=(
            "Add a dedicated limitations+coverage section for domains underrepresented in public benchmarks; consider a supplementary table of 'important but excluded' domains/papers with reasons."
        ),
        priority=5,
    ),
    Code(
        code="C06",
        title="Factual/statement-level corrections needed",
        description=(
            "Concrete factual errors (dataset sizes, dates, benchmark descriptions) and over-precise quantitative claims without clear definitions/traceability."
        ),
        patterns=(
            r"\bfactual\b",
            r"\bmisreported\b",
            r"\bincorrect\b",
            r"\berror\b",
            r"\bsize\b",
            r"\bmischaracteriz\w*\b",
            r"\boverconfident\b",
            r"\bwithout clearly specifying\b",
        ),
        response=(
            "Create a 'Claims and Evidence' audit pass: link each quantitative statement to a cited source, define terms, and correct dataset facts; add an errata table if needed."
        ),
        priority=6,
    ),
    Code(
        code="C07",
        title="Missing modalities / acquisition variants (contrast, phases, DECT/spectral)",
        description=(
            "Gaps covering modality variants like DECT/spectral CT, contrast phases, acquisition heterogeneity and how they impact segmentation and domain shift."
        ),
        patterns=(
            r"\bdect\b",
            r"\bspectral\b",
            r"\bcontrast\b",
            r"\bphase\b",
            r"\bmulti[- ]energy\b",
            r"\bacquisition\b",
        ),
        response=(
            "Add an acquisition-variation subsection: phases/spectral CT considerations and how methods handle or fail under appearance shifts; optionally tag included papers by phase/modality."
        ),
        priority=7,
    ),
    Code(
        code="C08",
        title="Small-structure / vessel / low-contrast failure modes",
        description=(
            "Recurring note that small or low-contrast targets (esophagus, vessels) need separate treatment: evaluation, losses, priors, post-processing, and resolution issues."
        ),
        patterns=(
            r"\besophagus\b",
            r"\bvessel\w*\b",
            r"\bsmall[- ]structure\b",
            r"\blow[- ]contrast\b",
            r"\bhd95\b",
            r"\bboundary\b",
            r"\btopology\b",
        ),
        response=(
            "Add a failure-modes subsection: stratify results/claims by organ size and contrast; discuss dedicated techniques (multi-scale, boundary losses, priors, topology constraints) and their tradeoffs."
        ),
        priority=8,
    ),
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def find_latest(pattern: str) -> Path:
    candidates = sorted(PEER_REVIEW_DIR.glob(pattern), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise FileNotFoundError(f"No files matching {pattern} in {PEER_REVIEW_DIR}")
    return candidates[-1]


def iter_findings(review: Dict[str, Any]) -> Iterable[Tuple[str, str, Optional[str]]]:
    """Yield (category, text, severity/priority) findings from a review."""

    def add_list(cat: str, value: Any, sev_key: Optional[str] = None):
        if value is None:
            return
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    text = item.get("issue") or item.get("recommendation") or item.get("error") or str(item)
                    sev = item.get(sev_key) if sev_key else None
                    yield (cat, str(text), str(sev) if sev is not None else None)
                else:
                    yield (cat, str(item), None)
        elif isinstance(value, dict):
            # Sometimes a dict of booleans/details. We only extract free-text fields.
            for k in ("details",):
                if value.get(k):
                    yield (cat, str(value.get(k)), None)
        else:
            yield (cat, str(value), None)

    # High-signal lists
    yield from add_list("weakness", review.get("weaknesses"), sev_key="severity")
    yield from add_list("recommendation", review.get("recommendations"), sev_key="priority")
    yield from add_list("factual_error", review.get("factual_errors"), sev_key=None)

    # Additional sources
    acc = review.get("accuracy_of_representation")
    if isinstance(acc, dict):
        yield from add_list("mischaracterization", acc.get("mischaracterizations"))
        if acc.get("details"):
            yield ("accuracy_details", str(acc.get("details")), None)

    tech = review.get("technical_critique")
    if isinstance(tech, dict):
        yield from add_list("technical_error", tech.get("technical_errors"))
        yield from add_list("oversimplification", tech.get("oversimplifications"))
        if tech.get("details"):
            yield ("technical_details", str(tech.get("details")), None)

    cov = review.get("coverage_completeness")
    if isinstance(cov, dict):
        yield from add_list("missing_aspect", cov.get("missing_aspects"))
        if cov.get("details"):
            yield ("coverage_details", str(cov.get("details")), None)

    meth = review.get("methodological_rigor")
    if isinstance(meth, dict):
        yield from add_list("method_concern", meth.get("concerns"))

    syn = review.get("synthesis_quality")
    if isinstance(syn, dict):
        yield from add_list("unsupported_generalization", syn.get("unsupported_generalizations"))
        if syn.get("details"):
            yield ("synthesis_details", str(syn.get("details")), None)


def classify(text: str) -> List[str]:
    text_l = text.lower()
    matched: List[Tuple[int, str]] = []

    for code in CODEBOOK:
        hits = 0
        for pat in code.patterns:
            if re.search(pat, text_l, flags=re.IGNORECASE):
                hits += 1
        if hits > 0:
            # Prefer higher-priority codes, break ties with more hits
            matched.append((code.priority * 1000 - hits, code.code))

    matched.sort()
    # Return up to 3 codes (primary + secondary) to keep outputs usable.
    return [c for _score, c in matched[:3]]


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\r", " ").strip()


def build_report(
    aggregated: Dict[str, Any],
    reviews: List[Dict[str, Any]],
    clusters: Dict[str, Any],
    output_path: Path,
) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: List[str] = []
    lines.append("# Clustered Summary Report (52-Paper View)")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append(f"Total reviews: {aggregated.get('total_reviews', len(reviews))}")
    lines.append(f"Decisions: {json.dumps(aggregated.get('decisions', {}), ensure_ascii=False)}")
    lines.append("")

    lines.append("## Codebook")
    lines.append("")
    lines.append("| Code | Theme | What it means |")
    lines.append("|---|---|---|")
    for c in sorted(CODEBOOK, key=lambda x: x.priority):
        lines.append(f"| {c.code} | {md_escape(c.title)} | {md_escape(c.description)} |")

    lines.append("\n## Cluster Summary")
    lines.append("")
    lines.append("| Code | Mentions | Reviewers | Top categories |")
    lines.append("|---|---:|---:|---|")

    def top_cats(d: Dict[str, int]) -> str:
        items = sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:3]
        return ", ".join(f"{k}:{v}" for k, v in items) if items else "-"

    for code, cdata in sorted(clusters.items(), key=lambda kv: kv[1]["mention_count"], reverse=True):
        lines.append(
            f"| {code} | {cdata['mention_count']} | {len(cdata['reviewers'])} | {md_escape(top_cats(cdata['category_counts']))} |"
        )

    lines.append("\n## Detailed Findings (By Code)")
    for c in sorted(CODEBOOK, key=lambda x: x.priority):
        cdata = clusters.get(c.code)
        if not cdata:
            continue

        lines.append("")
        lines.append(f"### {c.code}: {c.title}")
        lines.append("")
        lines.append(c.description)
        lines.append("")
        lines.append(f"Mentions: {cdata['mention_count']}  ")
        lines.append(f"Unique reviewers: {len(cdata['reviewers'])}")

        # Severity/priority breakdowns
        if cdata.get("severity_counts"):
            sev = ", ".join(f"{k}:{v}" for k, v in sorted(cdata["severity_counts"].items(), key=lambda kv: kv[1], reverse=True))
            lines.append(f"Severity (weakness): {sev}")
        if cdata.get("priority_counts"):
            pr = ", ".join(f"{k}:{v}" for k, v in sorted(cdata["priority_counts"].items(), key=lambda kv: kv[1], reverse=True))
            lines.append(f"Priority (recommendation): {pr}")

        lines.append("")
        lines.append("**Representative excerpts**")
        for ex in cdata.get("examples", [])[:6]:
            lines.append(f"- {md_escape(ex)}")

        # Evidence: list a few reviewer ids
        reviewers = sorted(list(cdata.get("reviewers", [])))
        if reviewers:
            lines.append("")
            lines.append("**Reviewers mentioning this (sample)**")
            for rid in reviewers[:12]:
                lines.append(f"- {rid}")
            if len(reviewers) > 12:
                lines.append(f"- (+{len(reviewers) - 12} more)")

        lines.append("")
        lines.append("**Proposed author response**")
        lines.append(c.response)

    lines.append("\n## Action Checklist (Code-Driven)")
    lines.append("")
    lines.append("Use this to draft an author rebuttal / revision plan.")
    lines.append("")
    for c in sorted(CODEBOOK, key=lambda x: x.priority):
        if c.code in clusters and clusters[c.code]["mention_count"] > 0:
            lines.append(f"- [{c.code}] {c.title}: {c.response}")

    output_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def main() -> int:
    aggregated_path = find_latest("aggregated_reviews_*.json")
    individual_path = find_latest("individual_reviews_*.json")

    aggregated = _read_json(aggregated_path)
    reviews = _read_json(individual_path)
    if not isinstance(reviews, list):
        raise ValueError("Expected a JSON array in individual_reviews file")

    # Build clusters
    clusters: Dict[str, Any] = {}
    for code in CODEBOOK:
        clusters[code.code] = {
            "code": code.code,
            "title": code.title,
            "description": code.description,
            "response": code.response,
            "priority": code.priority,
            "mention_count": 0,
            "reviewers": set(),
            "category_counts": {},
            "severity_counts": {},
            "priority_counts": {},
            "examples": [],
        }

    def bump(d: Dict[str, int], key: str, amount: int = 1) -> None:
        d[key] = int(d.get(key, 0)) + amount

    for review in reviews:
        reviewer_id = str(review.get("reviewer_paper_id") or review.get("paper_id") or "unknown")
        for category, text, sev in iter_findings(review):
            if not text or len(text.strip()) < 4:
                continue

            codes = classify(text)
            if not codes:
                continue

            primary = codes[0]
            cdata = clusters.get(primary)
            if not cdata:
                continue

            cdata["mention_count"] += 1
            cdata["reviewers"].add(reviewer_id)
            bump(cdata["category_counts"], category)

            if category == "weakness" and sev:
                bump(cdata["severity_counts"], sev)
            if category == "recommendation" and sev:
                bump(cdata["priority_counts"], sev)

            # Keep a few diverse examples
            if len(cdata["examples"]) < 12:
                cdata["examples"].append(text.strip())

    # Convert sets for JSON
    clusters_json: Dict[str, Any] = {}
    for code, cdata in clusters.items():
        clusters_json[code] = {
            **{k: v for k, v in cdata.items() if k != "reviewers"},
            "reviewers": sorted(list(cdata["reviewers"])),
        }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = PEER_REVIEW_DIR / f"CLUSTERED_FINDINGS_REPORT_{ts}.md"
    json_path = PEER_REVIEW_DIR / f"clustered_findings_{ts}.json"

    build_report(aggregated=aggregated, reviews=reviews, clusters=clusters_json, output_path=report_path)
    json_path.write_text(json.dumps({
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "aggregated_source": aggregated_path.name,
        "individual_source": individual_path.name,
        "codebook": [c.__dict__ for c in sorted(CODEBOOK, key=lambda x: x.priority)],
        "clusters": clusters_json,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote clustered report: {report_path}")
    print(f"Wrote clustered JSON: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
