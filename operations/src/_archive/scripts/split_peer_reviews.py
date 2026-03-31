#!/usr/bin/env python3
"""Split compiled peer reviews into one file per reviewer paper.

Reads the most recent `data/processed/peer_review/individual_reviews_*.json` and writes:
- `data/processed/peer_review/separated_reports/INDEX.md`
- `data/processed/peer_review/separated_reports/<reviewer_paper_id>.md`

This is intended to make it easy to browse each review separately.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PEER_REVIEW_DIR = REPO_ROOT / "data" / "processed" / "peer_review"
OUT_DIR = PEER_REVIEW_DIR / "separated_reports"


def _safe_filename(name: str) -> str:
    # Keep it readable but filesystem-safe.
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
    cleaned = cleaned.strip("._-")
    return cleaned or "unknown_paper"


def _md_escape(text: str) -> str:
    # Minimal escaping for markdown tables.
    return text.replace("|", "\\|")


def _as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def find_latest_individual_reviews() -> Path:
    candidates = sorted(PEER_REVIEW_DIR.glob("individual_reviews_*.json"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise FileNotFoundError(f"No individual_reviews_*.json found in {PEER_REVIEW_DIR}")
    return candidates[-1]


def render_review_md(review: dict) -> str:
    paper_id = str(review.get("reviewer_paper_id") or review.get("paper_id") or "unknown")
    title = str(review.get("reviewer_paper_title") or "(title unavailable)")

    overall = review.get("overall_judgment", {}) if isinstance(review.get("overall_judgment"), dict) else {}
    decision = str(overall.get("decision") or "Unknown")
    confidence = str(overall.get("confidence") or "Unknown")

    scores = review.get("scores", {}) if isinstance(review.get("scores"), dict) else {}

    def section(title_text: str, body: str) -> str:
        body = body.strip()
        if not body:
            return ""
        return f"\n## {title_text}\n\n{body}\n"

    lines = []
    lines.append(f"# Peer Review (Reviewer Paper: {paper_id})")
    lines.append("")
    lines.append(f"**Title:** {_md_escape(title)}")
    lines.append(f"**Decision:** {decision}")
    lines.append(f"**Confidence:** {confidence}")

    if scores:
        lines.append("\n## Scores\n")
        lines.append("| Metric | Score |")
        lines.append("|---|---:|")
        for k in sorted(scores.keys()):
            v = scores.get(k)
            if isinstance(v, (int, float, str)):
                lines.append(f"| {_md_escape(str(k))} | {_md_escape(str(v))} |")

    # Accuracy
    acc = review.get("accuracy_of_representation", {}) if isinstance(review.get("accuracy_of_representation"), dict) else {}
    if acc:
        parts = []
        parts.append(f"- Accurately represented: {acc.get('is_paper_accurately_represented', 'Unknown')}")
        parts.append(f"- Properly cited: {acc.get('properly_cited', 'Unknown')}")
        details = acc.get("details")
        if details:
            parts.append(f"- Details: {details}")
        mis = _as_list(acc.get("mischaracterizations"))
        if mis:
            parts.append("\n**Mischaracterizations**")
            for m in mis:
                parts.append(f"- {m}")
        lines.append(section("Accuracy Of Representation", "\n".join(parts)))

    # Technical critique
    tech = review.get("technical_critique", {}) if isinstance(review.get("technical_critique"), dict) else {}
    if tech:
        parts = []
        parts.append(f"- Understanding adequate: {tech.get('understanding_adequate', 'Unknown')}")
        if tech.get("comparison_fairness"):
            parts.append(f"- Comparison fairness: {tech.get('comparison_fairness')}")
        errors = _as_list(tech.get("technical_errors"))
        if errors:
            parts.append("\n**Technical errors**")
            for e in errors:
                parts.append(f"- {e}")
        overs = _as_list(tech.get("oversimplifications"))
        if overs:
            parts.append("\n**Oversimplifications**")
            for o in overs:
                parts.append(f"- {o}")
        if tech.get("details"):
            parts.append(f"\n**Details**\n\n{tech.get('details')}")
        lines.append(section("Technical Critique", "\n".join(parts)))

    # Coverage
    cov = review.get("coverage_completeness", {}) if isinstance(review.get("coverage_completeness"), dict) else {}
    if cov:
        parts = []
        if "taxonomy_appropriate" in cov:
            parts.append(f"- Taxonomy appropriate: {cov.get('taxonomy_appropriate')}")
        if "domain_challenges_addressed" in cov:
            parts.append(f"- Domain challenges addressed: {cov.get('domain_challenges_addressed')}")
        missing = _as_list(cov.get("missing_aspects"))
        if missing:
            parts.append("\n**Missing aspects**")
            for m in missing:
                parts.append(f"- {m}")
        if cov.get("details"):
            parts.append(f"\n**Details**\n\n{cov.get('details')}")
        lines.append(section("Coverage Completeness", "\n".join(parts)))

    # Methodology
    meth = review.get("methodological_rigor", {}) if isinstance(review.get("methodological_rigor"), dict) else {}
    if meth:
        parts = []
        for key in ("methodology_sound", "criteria_appropriate", "quality_assessment_adequate"):
            if key in meth:
                parts.append(f"- {key.replace('_', ' ').title()}: {meth.get(key)}")
        concerns = _as_list(meth.get("concerns"))
        if concerns:
            parts.append("\n**Concerns**")
            for c in concerns:
                parts.append(f"- {c}")
        lines.append(section("Methodological Rigor", "\n".join(parts)))

    # Synthesis
    syn = review.get("synthesis_quality", {}) if isinstance(review.get("synthesis_quality"), dict) else {}
    if syn:
        parts = []
        if "conclusions_supported" in syn:
            parts.append(f"- Conclusions supported: {syn.get('conclusions_supported')}")
        if "statistics_appropriate" in syn:
            parts.append(f"- Statistics appropriate: {syn.get('statistics_appropriate')}")
        unsup = _as_list(syn.get("unsupported_generalizations"))
        if unsup:
            parts.append("\n**Unsupported generalizations**")
            for u in unsup:
                parts.append(f"- {u}")
        if syn.get("details"):
            parts.append(f"\n**Details**\n\n{syn.get('details')}")
        lines.append(section("Synthesis Quality", "\n".join(parts)))

    # Strengths/Weaknesses
    strengths = _as_list(review.get("strengths"))
    if strengths:
        body = "\n".join(f"- {s}" for s in strengths)
        lines.append(section("Strengths", body))

    weaknesses = _as_list(review.get("weaknesses"))
    if weaknesses:
        items = []
        for w in weaknesses:
            if isinstance(w, dict):
                issue = w.get("issue", str(w))
                sev = w.get("severity", "Unknown")
                items.append(f"- ({sev}) {issue}")
            else:
                items.append(f"- {w}")
        lines.append(section("Weaknesses", "\n".join(items)))

    # Factual errors
    factual_errors = _as_list(review.get("factual_errors"))
    if factual_errors:
        items = []
        for fe in factual_errors:
            if isinstance(fe, dict):
                err = fe.get("error", str(fe))
                loc = fe.get("location", "")
                corr = fe.get("correction", "")
                suffix = ""
                if loc:
                    suffix += f" (location: {loc})"
                if corr:
                    suffix += f" (correction: {corr})"
                items.append(f"- {err}{suffix}")
            else:
                items.append(f"- {fe}")
        lines.append(section("Factual Errors", "\n".join(items)))

    # Recommendations
    recs = _as_list(review.get("recommendations"))
    if recs:
        items = []
        for r in recs:
            if isinstance(r, dict):
                rec = r.get("recommendation", str(r))
                pr = r.get("priority", "Unknown")
                items.append(f"- ({pr}) {rec}")
            else:
                items.append(f"- {r}")
        lines.append(section("Recommendations", "\n".join(items)))

    # Meta
    lines.append("\n---")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    latest = find_latest_individual_reviews()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    reviews = json.loads(latest.read_text(encoding="utf-8"))
    if not isinstance(reviews, list):
        raise ValueError("Expected a JSON array in individual_reviews file")

    index_lines = []
    index_lines.append("# Peer Review Reports (Separated)")
    index_lines.append("")
    index_lines.append(f"Source: {latest.name}")
    index_lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    index_lines.append("")
    index_lines.append("| Reviewer Paper ID | Decision | File |")
    index_lines.append("|---|---|---|")

    written = 0
    for review in reviews:
        reviewer_id = str(review.get("reviewer_paper_id") or review.get("paper_id") or "unknown")
        overall = review.get("overall_judgment", {}) if isinstance(review.get("overall_judgment"), dict) else {}
        decision = str(overall.get("decision") or "Unknown")

        filename = _safe_filename(reviewer_id) + ".md"
        out_path = OUT_DIR / filename
        out_path.write_text(render_review_md(review), encoding="utf-8")
        written += 1

        index_lines.append(f"| {_md_escape(reviewer_id)} | {_md_escape(decision)} | {filename} |")

    (OUT_DIR / "INDEX.md").write_text("\n".join(index_lines).strip() + "\n", encoding="utf-8")

    print(f"Wrote {written} separated review files to: {OUT_DIR}")
    print(f"Index: {OUT_DIR / 'INDEX.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
