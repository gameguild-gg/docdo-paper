"""Verify QA sub-claims in main.tex against the recovered per-study QA JSON.

Checks:
1. Code availability (Q10) >=1 count vs paper's "15 studies (28.8%)"
2. Sensitivity-analysis subset claim (29 studies / 10 high quality)
   - we cannot verify the "verified DOI / peer-reviewed" subset without
     a ground-truth peer-review flag, so we only print the QA breakdown.

Run: python operations/src/_archive/scripts/verify_qa_subclaims.py
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA_JSON = ROOT / "artifacts" / "data" / "evidence" / "supplementary" / "recovered" / "qa_parsed_results_20260123_075645.json"

data = json.loads(QA_JSON.read_text(encoding="utf-8"))
n = len(data)
print(f"n papers in QA JSON: {n}")

q10_scores = [p["quality_assessment"]["methodology_quality"]["Q10_code_availability"]["score"] for p in data]
print(f"Q10 code-availability distribution: {dict(Counter(q10_scores))}")
ge1 = sum(1 for s in q10_scores if s >= 1)
eq2 = sum(1 for s in q10_scores if s == 2)
print(f"  partial-or-full (score >=1): {ge1} ({ge1/n*100:.1f}%)")
print(f"  full only       (score ==2): {eq2} ({eq2/n*100:.1f}%)")

# Quality rating breakdown for cross-check
ratings = [p["quality_assessment"]["quality_rating"] for p in data]
totals = [p["quality_assessment"]["total_score"] for p in data]
print(f"\nQuality rating distribution: {dict(Counter(ratings))}")
print(f"Total score: mean={sum(totals)/n:.2f} min={min(totals)} max={max(totals)}")
print(f"  high (>=24): {sum(1 for s in totals if s>=24)}")
print(f"  medium (15-23): {sum(1 for s in totals if 15<=s<=23)}")
print(f"  low (<15): {sum(1 for s in totals if s<15)}")

# Sensitivity-analysis subset: paper_id form
ids = [p["paper_id"] for p in data]
arxiv = [p for p in data if "arxiv" in p["paper_id"].lower()]
doi   = [p for p in data if "arxiv" not in p["paper_id"].lower()]
print(f"\npaper_id breakdown: arxiv-like={len(arxiv)}, doi-like={len(doi)}")
def by_rating(subset, rating):
    return sum(1 for p in subset if p["quality_assessment"]["quality_rating"] == rating)
for label, subset in [("doi-like (sensitivity subset)", doi), ("arxiv-like", arxiv)]:
    h, m, l = by_rating(subset, "High"), by_rating(subset, "Medium"), by_rating(subset, "Low")
    print(f"  {label}: n={len(subset)} High={h} Medium={m} Low={l}"
          + (f"  High%={h/len(subset)*100:.1f}" if subset else ""))

# Other reproducibility numbers cited in main.tex L991
def metq(k): return [p["quality_assessment"]["methodology_quality"][k]["score"] for p in data]
def evq(k):  return [p["quality_assessment"]["evaluation_quality"][k]["score"] for p in data]
print("\nReproducibility-related (>=1 = at least partial):")
print(f"  Q7 reproducibility   >=1: {sum(1 for x in metq('Q7_reproducibility') if x>=1)}")
print(f"  Q9 preprocessing     >=1: {sum(1 for x in metq('Q9_preprocessing') if x>=1)}")
print(f"  Q12 statistical      >=1: {sum(1 for x in evq('Q12_statistical_analysis') if x>=1)}")
q14 = evq("Q14_per_organ_results")
print(f"  Q14 per-organ ==2 (full): {sum(1 for x in q14 if x==2)}, ==1 (partial): {sum(1 for x in q14 if x==1)}, ==0: {sum(1 for x in q14 if x==0)}")
