#!/usr/bin/env python3
"""
Download and process Quality Assessment batch results.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from openai import OpenAI

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs): return False

REPO_ROOT = Path(__file__).parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

BATCH_ID = "batch_6972e053c6108190ac38ab54bd2987ec"
OUTPUT_DIR = REPO_ROOT / "data/processed/quality_assessment"

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Get batch info
    batch = client.batches.retrieve(BATCH_ID)
    print(f"Batch Status: {batch.status}")
    print(f"Completed: {batch.request_counts.completed}/{batch.request_counts.total}")
    print(f"Failed: {batch.request_counts.failed}")
    
    if batch.status != "completed":
        print("Batch not completed yet!")
        return
    
    # Download results
    print(f"\nDownloading results...")
    output_file_id = batch.output_file_id
    content = client.files.content(output_file_id)
    
    raw_file = OUTPUT_DIR / f"qa_batch_raw_{timestamp}.jsonl"
    raw_file.write_bytes(content.content)
    print(f"Saved raw: {raw_file}")
    
    # Parse results
    results = []
    
    for line in raw_file.read_text(encoding='utf-8').strip().split('\n'):
        if not line:
            continue
        
        data = json.loads(line)
        custom_id = data.get('custom_id', '')
        paper_id = custom_id.replace('qa_', '')
        
        response = data.get('response', {})
        body = response.get('body', {})
        choices = body.get('choices', [])
        
        if choices:
            content = choices[0].get('message', {}).get('content', '{}')
            try:
                parsed = json.loads(content)
                parsed['paper_id'] = paper_id
                results.append(parsed)
            except json.JSONDecodeError:
                print(f"  ⚠️ JSON parse error: {paper_id}")
                results.append({'paper_id': paper_id, 'error': 'JSON parse error'})
        else:
            print(f"  ⚠️ No choices: {paper_id}")
            results.append({'paper_id': paper_id, 'error': 'No response'})
    
    # Save parsed results
    parsed_file = OUTPUT_DIR / f"qa_parsed_results_{timestamp}.json"
    with open(parsed_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Saved parsed: {parsed_file}")
    print(f"\nTotal papers: {len(results)}")
    
    # Generate summary statistics
    print("\n" + "="*60)
    print("QUALITY ASSESSMENT SUMMARY")
    print("="*60)
    
    scores = []
    ratings = {'High': 0, 'Medium': 0, 'Low': 0}
    
    for r in results:
        if 'error' in r:
            continue
        
        qa = r.get('quality_assessment', {})
        score = qa.get('total_score', 0)
        rating = qa.get('quality_rating', 'Unknown')
        
        scores.append(score)
        if rating in ratings:
            ratings[rating] += 1
    
    if scores:
        print(f"\nQuality Scores:")
        print(f"  Mean: {sum(scores)/len(scores):.1f}/30")
        print(f"  Min: {min(scores)}/30")
        print(f"  Max: {max(scores)}/30")
        print(f"\nQuality Ratings:")
        print(f"  High (≥24): {ratings['High']}")
        print(f"  Medium (15-23): {ratings['Medium']}")
        print(f"  Low (<15): {ratings['Low']}")
    
    # Architecture summary
    architectures = {}
    for r in results:
        if 'error' in r:
            continue
        detail = r.get('detailed_extraction', {})
        method = detail.get('method', {})
        arch = method.get('architecture_name', 'Unknown')
        architectures[arch] = architectures.get(arch, 0) + 1
    
    print(f"\nTop Architectures:")
    for arch, count in sorted(architectures.items(), key=lambda x: -x[1])[:10]:
        print(f"  {arch}: {count}")
    
    # Create summary CSV
    import csv
    
    csv_file = OUTPUT_DIR / f"qa_summary_{timestamp}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'paper_id', 'title', 'year', 'architecture', 'organs',
            'dataset_quality', 'methodology_quality', 'evaluation_quality',
            'total_score', 'quality_rating', 'main_contribution'
        ])
        
        for r in results:
            if 'error' in r:
                continue
            
            qa = r.get('quality_assessment', {})
            detail = r.get('detailed_extraction', {})
            contrib = r.get('contribution_summary', {})
            
            # Calculate subscores
            dq = qa.get('dataset_quality', {})
            mq = qa.get('methodology_quality', {})
            eq = qa.get('evaluation_quality', {})
            
            dq_score = sum(v.get('score', 0) for v in dq.values() if isinstance(v, dict))
            mq_score = sum(v.get('score', 0) for v in mq.values() if isinstance(v, dict))
            eq_score = sum(v.get('score', 0) for v in eq.values() if isinstance(v, dict))
            
            organs = detail.get('organs', {})
            organs_list = organs.get('segmented_organs', [])
            
            writer.writerow([
                r.get('paper_id', ''),
                detail.get('title', ''),
                detail.get('year', ''),
                detail.get('method', {}).get('architecture_name', ''),
                ', '.join(organs_list) if isinstance(organs_list, list) else str(organs_list),
                dq_score,
                mq_score,
                eq_score,
                qa.get('total_score', ''),
                qa.get('quality_rating', ''),
                contrib.get('main_contribution', '')
            ])
    
    print(f"\nSaved summary CSV: {csv_file}")
    
    return results

if __name__ == "__main__":
    main()
