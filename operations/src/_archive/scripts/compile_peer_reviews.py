#!/usr/bin/env python3
"""
Compile Peer Review Results into Comprehensive Report
======================================================
After the batch completes, this script:
1. Downloads and parses all 52 reviews
2. Aggregates findings across all reviewers
3. Generates a comprehensive peer review report
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from openai import OpenAI

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs): return False

REPO_ROOT = Path(__file__).parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

OUTPUT_DIR = REPO_ROOT / "data/processed/peer_review"


def load_results(results_file: Path) -> list:
    """Load results from JSONL file."""
    results = []
    with open(results_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    return results


def parse_review(result: dict) -> dict:
    """Parse a single review result."""
    custom_id = result.get('custom_id', '')
    paper_id = custom_id.replace('review_', '')
    
    try:
        response = result.get('response', {})
        body = response.get('body', {})
        choices = body.get('choices', [])
        
        if choices:
            content = choices[0].get('message', {}).get('content', '{}')
            review = json.loads(content)
            review['paper_id'] = paper_id
            review['status'] = 'success'
            return review
    except Exception as e:
        return {
            'paper_id': paper_id,
            'status': 'error',
            'error': str(e)
        }
    
    return {'paper_id': paper_id, 'status': 'error', 'error': 'Unknown'}


def aggregate_reviews(reviews: list) -> dict:
    """Aggregate findings across all reviews."""
    
    # Overall decisions
    decisions = Counter()
    confidences = Counter()
    
    # Scores
    all_scores = defaultdict(list)
    
    # Issues
    all_strengths = []
    all_weaknesses = []
    all_errors = []
    all_recommendations = []
    
    # Detailed analysis
    accuracy_issues = []
    technical_issues = []
    coverage_issues = []
    methodology_issues = []
    
    for review in reviews:
        if review.get('status') != 'success':
            continue
        
        # Extract judgment
        judgment = review.get('overall_judgment', {})
        decisions[judgment.get('decision', 'Unknown')] += 1
        confidences[judgment.get('confidence', 'Unknown')] += 1
        
        # Extract scores
        scores = review.get('scores', {})
        for key, value in scores.items():
            if isinstance(value, (int, float)):
                all_scores[key].append(value)
        
        # Extract strengths
        for strength in review.get('strengths', []):
            all_strengths.append({
                'reviewer': review.get('reviewer_paper_id', review.get('paper_id')),
                'strength': strength
            })
        
        # Extract weaknesses
        for weakness in review.get('weaknesses', []):
            if isinstance(weakness, dict):
                all_weaknesses.append({
                    'reviewer': review.get('reviewer_paper_id', review.get('paper_id')),
                    'issue': weakness.get('issue', str(weakness)),
                    'severity': weakness.get('severity', 'Unknown')
                })
            else:
                all_weaknesses.append({
                    'reviewer': review.get('reviewer_paper_id', review.get('paper_id')),
                    'issue': str(weakness),
                    'severity': 'Unknown'
                })
        
        # Extract errors
        for error in review.get('factual_errors', []):
            if isinstance(error, dict):
                all_errors.append({
                    'reviewer': review.get('reviewer_paper_id', review.get('paper_id')),
                    'error': error.get('error', str(error)),
                    'location': error.get('location', 'Unknown'),
                    'correction': error.get('correction', '')
                })
        
        # Extract recommendations
        for rec in review.get('recommendations', []):
            if isinstance(rec, dict):
                all_recommendations.append({
                    'reviewer': review.get('reviewer_paper_id', review.get('paper_id')),
                    'recommendation': rec.get('recommendation', str(rec)),
                    'priority': rec.get('priority', 'Unknown')
                })
        
        # Accuracy issues
        accuracy = review.get('accuracy_of_representation', {})
        if not accuracy.get('is_paper_accurately_represented', True):
            accuracy_issues.append({
                'reviewer': review.get('reviewer_paper_id', review.get('paper_id')),
                'details': accuracy.get('details', ''),
                'mischaracterizations': accuracy.get('mischaracterizations', [])
            })
        
        # Technical issues
        tech = review.get('technical_critique', {})
        if tech.get('technical_errors') or not tech.get('understanding_adequate', True):
            technical_issues.append({
                'reviewer': review.get('reviewer_paper_id', review.get('paper_id')),
                'errors': tech.get('technical_errors', []),
                'oversimplifications': tech.get('oversimplifications', []),
                'details': tech.get('details', '')
            })
        
        # Coverage issues
        coverage = review.get('coverage_completeness', {})
        if coverage.get('missing_aspects'):
            coverage_issues.append({
                'reviewer': review.get('reviewer_paper_id', review.get('paper_id')),
                'missing': coverage.get('missing_aspects', []),
                'details': coverage.get('details', '')
            })
        
        # Methodology issues
        method = review.get('methodological_rigor', {})
        if method.get('concerns'):
            methodology_issues.append({
                'reviewer': review.get('reviewer_paper_id', review.get('paper_id')),
                'concerns': method.get('concerns', [])
            })
    
    # Calculate average scores
    avg_scores = {}
    for key, values in all_scores.items():
        if values:
            avg_scores[key] = sum(values) / len(values)
    
    return {
        'total_reviews': len(reviews),
        'successful_reviews': sum(1 for r in reviews if r.get('status') == 'success'),
        'decisions': dict(decisions),
        'confidences': dict(confidences),
        'average_scores': avg_scores,
        'all_scores': {k: v for k, v in all_scores.items()},
        'strengths': all_strengths,
        'weaknesses': all_weaknesses,
        'factual_errors': all_errors,
        'recommendations': all_recommendations,
        'accuracy_issues': accuracy_issues,
        'technical_issues': technical_issues,
        'coverage_issues': coverage_issues,
        'methodology_issues': methodology_issues
    }


def generate_report(aggregated: dict, reviews: list, output_dir: Path) -> Path:
    """Generate comprehensive markdown report."""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Count severities
    critical_issues = [w for w in aggregated['weaknesses'] if w.get('severity') == 'Critical']
    major_issues = [w for w in aggregated['weaknesses'] if w.get('severity') == 'Major']
    minor_issues = [w for w in aggregated['weaknesses'] if w.get('severity') == 'Minor']
    
    critical_recs = [r for r in aggregated['recommendations'] if r.get('priority') == 'Critical']
    major_recs = [r for r in aggregated['recommendations'] if r.get('priority') == 'Major']
    
    report = f"""# Peer Review Report: Systematic Review on 3D Organ Segmentation
## Aggregated Critical Analysis from 52 Reviewed Papers

**Generated:** {timestamp}
**Total Reviewers:** {aggregated['total_reviews']}
**Successful Reviews:** {aggregated['successful_reviews']}

---

## Executive Summary

This report aggregates critical peer reviews of our systematic review paper from the perspective 
of each of the 52 papers included in the review. Each paper served as a "reviewer" providing 
critique from their specialized perspective.

### Overall Verdict Distribution

| Decision | Count | Percentage |
|----------|-------|------------|
"""
    
    total = sum(aggregated['decisions'].values())
    for decision, count in sorted(aggregated['decisions'].items(), key=lambda x: -x[1]):
        pct = (count / total * 100) if total > 0 else 0
        report += f"| {decision} | {count} | {pct:.1f}% |\n"
    
    report += f"""
### Reviewer Confidence

| Confidence | Count |
|------------|-------|
"""
    for conf, count in sorted(aggregated['confidences'].items(), key=lambda x: -x[1]):
        report += f"| {conf} | {count} |\n"
    
    report += f"""
### Average Scores (1-5 scale)

| Criterion | Average Score |
|-----------|---------------|
"""
    for criterion, score in sorted(aggregated['average_scores'].items()):
        report += f"| {criterion.replace('_', ' ').title()} | {score:.2f} |\n"
    
    report += f"""
---

## Issue Summary

| Category | Critical | Major | Minor | Total |
|----------|----------|-------|-------|-------|
| Weaknesses | {len(critical_issues)} | {len(major_issues)} | {len(minor_issues)} | {len(aggregated['weaknesses'])} |
| Recommendations | {len(critical_recs)} | {len(major_recs)} | {len(aggregated['recommendations']) - len(critical_recs) - len(major_recs)} | {len(aggregated['recommendations'])} |
| Factual Errors | - | - | - | {len(aggregated['factual_errors'])} |

---

## Critical Issues (Must Address)

"""
    
    if critical_issues:
        for i, issue in enumerate(critical_issues, 1):
            report += f"### {i}. {issue['issue'][:100]}...\n"
            report += f"**Reported by:** {issue['reviewer']}\n\n"
    else:
        report += "*No critical issues identified.*\n"
    
    report += """
---

## Major Issues

"""
    
    # Group similar issues
    issue_counts = Counter(w['issue'][:100] for w in major_issues)
    for issue_text, count in issue_counts.most_common(20):
        report += f"- **[x{count}]** {issue_text}...\n"
    
    report += f"""
---

## Factual Errors Identified

"""
    if aggregated['factual_errors']:
        for i, error in enumerate(aggregated['factual_errors'][:30], 1):
            report += f"### Error {i}\n"
            report += f"- **Reviewer:** {error['reviewer']}\n"
            report += f"- **Error:** {error['error']}\n"
            report += f"- **Location:** {error['location']}\n"
            report += f"- **Correction:** {error['correction']}\n\n"
    else:
        report += "*No factual errors identified.*\n"
    
    report += f"""
---

## Accuracy of Representation Issues

Papers that felt they were not accurately represented:

"""
    if aggregated['accuracy_issues']:
        for issue in aggregated['accuracy_issues']:
            report += f"### {issue['reviewer']}\n"
            report += f"{issue['details']}\n"
            if issue['mischaracterizations']:
                report += f"- Mischaracterizations: {', '.join(issue['mischaracterizations'])}\n"
            report += "\n"
    else:
        report += "*All papers felt they were accurately represented.*\n"
    
    report += f"""
---

## Coverage Gaps Identified

Aspects that reviewers felt were missing:

"""
    # Aggregate missing aspects
    all_missing = []
    for issue in aggregated['coverage_issues']:
        all_missing.extend(issue.get('missing', []))
    
    missing_counts = Counter(all_missing)
    for aspect, count in missing_counts.most_common(20):
        report += f"- **[x{count}]** {aspect}\n"
    
    report += f"""
---

## Strengths Identified

What reviewers appreciated about the systematic review:

"""
    # Group similar strengths
    strength_counts = Counter(s['strength'][:100] for s in aggregated['strengths'])
    for strength_text, count in strength_counts.most_common(15):
        report += f"- **[x{count}]** {strength_text}\n"
    
    report += f"""
---

## Priority Recommendations

### Critical Priority
"""
    if critical_recs:
        for rec in critical_recs[:10]:
            report += f"- {rec['recommendation']} *(from {rec['reviewer']})*\n"
    else:
        report += "*None*\n"
    
    report += """
### Major Priority
"""
    if major_recs:
        for rec in major_recs[:15]:
            report += f"- {rec['recommendation']} *(from {rec['reviewer']})*\n"
    else:
        report += "*None*\n"
    
    report += f"""
---

## Individual Reviews

Below are summaries from each reviewer:

"""
    for review in reviews:
        if review.get('status') != 'success':
            continue
        
        paper_id = review.get('reviewer_paper_id', review.get('paper_id', 'Unknown'))
        judgment = review.get('overall_judgment', {})
        
        report += f"### {paper_id}\n"
        report += f"- **Decision:** {judgment.get('decision', 'N/A')}\n"
        report += f"- **Confidence:** {judgment.get('confidence', 'N/A')}\n"
        report += f"- **Summary:** {judgment.get('summary', 'N/A')}\n\n"
    
    report += f"""
---

## Methodology Note

This peer review was conducted using an AI-assisted approach where each of the 52 papers 
included in our systematic review served as the basis for a critical review perspective. 
The reviews were generated using GPT-4o with access to both the full text of the reviewer 
paper and our systematic review manuscript.

**Limitations:**
- AI-generated reviews may not capture all nuances a human expert would
- Reviews are based on text extraction which may miss figures/tables
- Some papers may have had incomplete text extraction

**Interpretation:**
- Consensus issues (reported by multiple reviewers) should be prioritized
- Critical and Major severity items warrant immediate attention
- This report supplements, but does not replace, human peer review

---

*Report generated automatically from {aggregated['successful_reviews']} peer reviews.*
"""
    
    # Save report
    report_file = output_dir / f"PEER_REVIEW_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Save raw aggregated data
    data_file = output_dir / f"aggregated_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(aggregated, f, indent=2, default=str)
    
    # Save individual reviews
    reviews_file = output_dir / f"individual_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(reviews_file, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, default=str)
    
    return report_file


def main():
    print("=" * 70)
    print("Peer Review Results Compiler")
    print("=" * 70)
    
    # Find results file
    results_files = list(OUTPUT_DIR.glob("peer_reviews_results*.jsonl"))
    
    if not results_files:
        print(f"\n❌ No results file found in {OUTPUT_DIR}")
        print("Run check_peer_review_batch.py to download results first.")
        return
    
    # Use most recent
    results_file = max(results_files, key=lambda p: p.stat().st_mtime)
    print(f"\n📄 Loading results from: {results_file.name}")
    
    # Load and parse results
    raw_results = load_results(results_file)
    print(f"  Loaded {len(raw_results)} results")
    
    # Parse each review
    reviews = [parse_review(r) for r in raw_results]
    successful = sum(1 for r in reviews if r.get('status') == 'success')
    print(f"  Successfully parsed: {successful}/{len(reviews)}")
    
    # Aggregate
    print("\n📊 Aggregating findings...")
    aggregated = aggregate_reviews(reviews)
    
    # Generate report
    print("\n📝 Generating comprehensive report...")
    report_file = generate_report(aggregated, reviews, OUTPUT_DIR)
    
    print(f"\n✅ Report generated: {report_file}")
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Total reviews: {aggregated['total_reviews']}")
    print(f"Decisions: {aggregated['decisions']}")
    print(f"Critical issues: {len([w for w in aggregated['weaknesses'] if w.get('severity') == 'Critical'])}")
    print(f"Major issues: {len([w for w in aggregated['weaknesses'] if w.get('severity') == 'Major'])}")
    print(f"Factual errors: {len(aggregated['factual_errors'])}")
    
    return report_file


if __name__ == "__main__":
    main()
