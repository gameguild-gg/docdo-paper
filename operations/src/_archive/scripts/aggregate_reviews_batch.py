#!/usr/bin/env python3
"""Create a batch to aggregate all 52 peer reviews into a unified TODO.md.

Sends the full set of reviews 3 times (independent runs) to reduce hallucination,
then a reconciler script will merge the 3 outputs into a final consensus TODO.

Outputs:
- data/processed/peer_review/aggregate_batch_<timestamp>.jsonl
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PEER_REVIEW_DIR = REPO_ROOT / "data" / "processed" / "peer_review"
MODEL_NAME = "gpt-5.2"
NUM_RUNS = 3  # 3 independent aggregations for hallucination reduction


def find_latest(pattern: str) -> Path:
    candidates = sorted(PEER_REVIEW_DIR.glob(pattern), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise FileNotFoundError(f"No files matching {pattern} in {PEER_REVIEW_DIR}")
    return candidates[-1]


SYSTEM_PROMPT = """\
You are a senior academic editor helping authors respond to peer review.

You will receive 52 individual peer reviews of a systematic review paper on "3D Organ Segmentation from CT Scans."
Each review was written from the perspective of one of the 52 papers included in that systematic review.

Your task:
1. Read ALL 52 reviews carefully.
2. Identify recurring themes, concerns, and recommendations across reviewers.
3. Cluster findings into actionable codes (e.g., M01: Methodology, T01: Taxonomy, Q01: Quantitative synthesis, C01: Clinical claims, etc.).
4. For each code, list:
   - The issue/finding (synthesized across reviewers)
   - Which papers raised it (by their IDs)
   - Severity (Critical / Major / Minor) based on consensus
   - A concrete TODO action for the authors
5. Handle CONFLICTS: if reviewers disagree, note both views and recommend a balanced resolution.
6. Produce a clean, professional TODO.md document suitable for revision planning.

Output format: A single Markdown document with:
- Executive summary (key stats, overall verdict)
- Codebook table (code, theme, description)
- Detailed findings by code (issue, papers, severity, TODO action)
- Conflict resolution section (if any)
- Final prioritized checklist

Be thorough, precise, and actionable. Do not invent issues not present in the reviews.
"""


USER_PROMPT_TEMPLATE = """\
Below are 52 peer reviews of our systematic review paper. Each review is from the perspective of one included paper.

Please aggregate these into a unified TODO.md revision plan following the instructions above.

---
PEER REVIEWS (52 total)
---

{reviews_text}

---
END OF REVIEWS
---

Now produce the aggregated TODO.md document.
"""


def build_reviews_text(reviews: list) -> str:
    """Build a single text block with all 52 reviews."""
    parts = []
    for i, review in enumerate(reviews, 1):
        reviewer_id = review.get("reviewer_paper_id") or review.get("paper_id") or f"unknown_{i}"
        # Serialize the review to a readable format
        review_json = json.dumps(review, indent=2, ensure_ascii=False)
        parts.append(f"=== REVIEW {i}/52: {reviewer_id} ===\n{review_json}\n")
    return "\n".join(parts)


def main() -> int:
    # Load individual reviews
    individual_path = find_latest("individual_reviews_*.json")
    print(f"Loading reviews from: {individual_path.name}")
    
    reviews = json.loads(individual_path.read_text(encoding="utf-8"))
    if not isinstance(reviews, list):
        raise ValueError("Expected a JSON array")
    
    print(f"Loaded {len(reviews)} reviews")
    
    # Build the reviews text (will be same for all 3 runs)
    reviews_text = build_reviews_text(reviews)
    user_prompt = USER_PROMPT_TEMPLATE.format(reviews_text=reviews_text)
    
    # Estimate tokens
    total_chars = len(SYSTEM_PROMPT) + len(user_prompt)
    est_input_tokens = total_chars // 4
    print(f"Estimated input tokens per request: ~{est_input_tokens:,}")
    print(f"Total for {NUM_RUNS} runs: ~{est_input_tokens * NUM_RUNS:,} input tokens")
    
    # Build batch requests (3 independent runs)
    requests = []
    for run_id in range(1, NUM_RUNS + 1):
        request = {
            "custom_id": f"aggregate_run_{run_id}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.3,  # Low but not zero for diversity
                "max_completion_tokens": 16000,
            },
        }
        requests.append(request)
    
    # Write batch file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_file = PEER_REVIEW_DIR / f"aggregate_batch_{timestamp}.jsonl"
    
    with open(batch_file, "w", encoding="utf-8") as f:
        for req in requests:
            f.write(json.dumps(req, ensure_ascii=False) + "\n")
    
    print(f"\nBatch file saved: {batch_file}")
    print(f"Contains {len(requests)} requests (3 independent aggregation runs)")
    
    # Cost estimate for GPT-5.2
    # Input: $0.75/M tokens, Output: $3.00/M tokens
    input_cost = (est_input_tokens * NUM_RUNS / 1_000_000) * 0.75
    output_cost = (16000 * NUM_RUNS / 1_000_000) * 3.00  # max output estimate
    print(f"\nCOST ESTIMATE (gpt-5.2, worst case):")
    print(f"  Input:  ~{est_input_tokens * NUM_RUNS:,} tokens = ${input_cost:.2f}")
    print(f"  Output: ~{16000 * NUM_RUNS:,} tokens (max) = ${output_cost:.2f}")
    print(f"  TOTAL:  ~${input_cost + output_cost:.2f}")
    
    print(f"\nNext step: Submit the batch with:")
    print(f"  python supplementary/scripts/submit_aggregate_batch.py")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
