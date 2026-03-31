# Labeling Rules — DocDo Screening

Rules for consistent AI-assisted screening decisions, ensuring reproducibility and inter-rater agreement.

---

## Multi-Model Consensus Protocol

Screening uses **3 independent LLM passes** (models or runs) per paper.
Final decisions are determined by **unanimous voting**.

### S2 Abstract Screening

| Scenario | Votes | Final Decision |
|----------|-------|----------------|
| 3× INCLUDE | All agree | **INCLUDE** |
| 2× INCLUDE + 1× EXCLUDE | Majority, but not unanimous | **EXCLUDE** (conservative) |
| 1× INCLUDE + 2× EXCLUDE | Majority exclude | **EXCLUDE** |
| 3× EXCLUDE | All agree | **EXCLUDE** |

> **Conservative rule:** A paper is only included if **all** runs agree on INCLUDE.
> This minimizes false positives at the cost of potentially missing borderline papers.

### S3 Full-Text Screening

Same unanimous voting protocol applied to full-text review decisions.

---

## Confidence Thresholds

Each screening run reports a confidence score (70–95).

| Range | Interpretation |
|-------|---------------|
| 85–95 | High confidence — criteria clearly met or clearly failed |
| 75–84 | Moderate confidence — some ambiguity in abstract |
| 70–74 | Low confidence — significant uncertainty |

> Confidence is informational and does **not** override the binary INCLUDE/EXCLUDE decision.

---

## Tie-Breaking

There are no ties in a 3-vote unanimous system. Any disagreement → **EXCLUDE**.

If a dedicated tie-breaker model is configured (`TIEBREAKER_MODEL`), it can be used
as a 4th opinion for audit purposes, but the conservative unanimous rule remains authoritative.

---

## Batch Processing

- Papers are screened via the **OpenAI Batch API** for cost efficiency.
- Each batch request file (JSONL) contains one screening prompt per paper.
- Batch results are parsed and votes are tallied by `docdo screening` commands.
- All batch files are stored in `evidence/processed/batches*/` for reproducibility.

---

## Labeling Consistency

1. **Same prompt** is used across all runs (see `SCREENING_PROMPT` in `docdo.screening`).
2. **Temperature** is set to 0.3 — low but non-zero for slight diversity across runs.
3. **No human-in-the-loop** during S2; human review occurs at S3 full-text stage.
4. All intermediate results are stored for auditability.
