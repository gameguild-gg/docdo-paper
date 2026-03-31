#!/usr/bin/env python3
"""Reconcile 3 independent aggregation runs into a final TODO.md.

This script:
1. Loads the 3 aggregation outputs from the batch
2. Sends them to GPT for reconciliation (identifying consensus vs conflicts)
3. Produces a final, authoritative TODO.md

This is the hallucination-reduction step: by comparing 3 independent runs,
we can identify stable findings vs potential hallucinations.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PEER_REVIEW_DIR = REPO_ROOT / "data" / "processed" / "peer_review"
MODEL_NAME = "gpt-5.2"


def find_latest(pattern: str) -> Path:
    candidates = sorted(PEER_REVIEW_DIR.glob(pattern), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise FileNotFoundError(f"No files matching {pattern} in {PEER_REVIEW_DIR}")
    return candidates[-1]


RECONCILE_SYSTEM = """\
You are a senior academic editor performing final quality control.

You will receive 3 INDEPENDENT aggregations of the same 52 peer reviews.
Each aggregation was produced by a separate GPT run, attempting to cluster findings into a TODO.md.

Your task:
1. Compare all 3 aggregations carefully.
2. Identify CONSENSUS items: findings/codes that appear consistently across all 3 runs.
3. Identify CONFLICTS: findings that appear in only 1-2 runs, or where runs disagree on severity/details.
4. For consensus items: include them in the final TODO.md with high confidence.
5. For conflicts: either exclude (if likely hallucination) or include with a note about uncertainty.
6. Produce a FINAL, AUTHORITATIVE TODO.md that:
   - Is clean, well-structured, and actionable
   - Uses a clear code system (e.g., M01, T01, Q01, C01, etc.)
   - Includes paper IDs that raised each issue (only if consistently cited across runs)
   - Marks severity levels (Critical/Major/Minor)
   - Provides concrete action items for each finding
   - Has a "Confidence" indicator (High/Medium/Low) based on cross-run agreement

Output: A single, final TODO.md document ready for the authors to use.
"""


RECONCILE_USER_TEMPLATE = """\
Below are 3 INDEPENDENT aggregations of 52 peer reviews. Please reconcile them into a final TODO.md.

=== RUN 1 ===
{run1}

=== RUN 2 ===
{run2}

=== RUN 3 ===
{run3}

=== END OF RUNS ===

Now produce the final, reconciled TODO.md document. Focus on consensus findings and flag any conflicts.
"""


def main() -> int:
    # Load aggregate results
    results_file = find_latest("aggregate_results_*.jsonl")
    print(f"Loading aggregate results from: {results_file.name}")
    
    results = []
    with open(results_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    
    print(f"Loaded {len(results)} results")
    
    if len(results) != 3:
        print(f"WARNING: Expected 3 runs, got {len(results)}")
    
    # Extract the 3 aggregation outputs
    runs = {}
    for result in results:
        custom_id = result.get("custom_id", "")
        try:
            content = result["response"]["body"]["choices"][0]["message"]["content"]
            runs[custom_id] = content
        except (KeyError, IndexError) as e:
            print(f"Error parsing {custom_id}: {e}")
            runs[custom_id] = "(Error: could not extract content)"
    
    # Sort by run number
    run_keys = sorted(runs.keys())
    if len(run_keys) < 3:
        print("WARNING: Less than 3 successful runs")
        # Pad with empty if needed
        while len(run_keys) < 3:
            run_keys.append(f"missing_run_{len(run_keys)+1}")
            runs[run_keys[-1]] = "(No output available)"
    
    run1 = runs.get(run_keys[0], "(No output)")
    run2 = runs.get(run_keys[1], "(No output)")
    run3 = runs.get(run_keys[2], "(No output)")
    
    print(f"\nRun outputs:")
    for k in run_keys[:3]:
        print(f"  {k}: {len(runs.get(k, '')):,} chars")
    
    # Now call GPT to reconcile
    print("\nCalling GPT to reconcile the 3 runs...")
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    user_prompt = RECONCILE_USER_TEMPLATE.format(run1=run1, run2=run2, run3=run3)
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": RECONCILE_SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_completion_tokens=16000,
    )
    
    final_todo = response.choices[0].message.content
    
    # Save the final TODO.md
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    todo_file = PEER_REVIEW_DIR / f"TODO_FINAL_{timestamp}.md"
    todo_file.write_text(final_todo, encoding="utf-8")
    print(f"\nFinal TODO saved: {todo_file}")
    
    # Also save to repo root for convenience
    root_todo = REPO_ROOT / "TODO_PEER_REVIEW.md"
    root_todo.write_text(final_todo, encoding="utf-8")
    print(f"Also saved to: {root_todo}")
    
    # Save the 3 individual runs for reference
    runs_file = PEER_REVIEW_DIR / f"aggregate_runs_{timestamp}.json"
    runs_file.write_text(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "runs": {k: runs.get(k, "") for k in run_keys[:3]},
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Individual runs saved: {runs_file}")
    
    print("\n" + "=" * 60)
    print("DONE! Final TODO.md is ready.")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
