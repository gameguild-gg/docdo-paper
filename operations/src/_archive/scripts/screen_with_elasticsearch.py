#!/usr/bin/env python3
"""
S2 Alternative - Keyword-based Screening with Elasticsearch

Uses Elasticsearch to filter papers based on keyword matching.
This is a fast, deterministic pre-filter before AI screening.

Approach:
1. Index all papers in Elasticsearch
2. Query with MUST/SHOULD/MUST_NOT boolean logic
3. Score and rank papers by relevance
4. Output filtered set for further review

Requirements:
- Docker running
- elasticsearch Python package
"""

import csv
import json
import time
from pathlib import Path
from datetime import datetime

try:
    from elasticsearch import Elasticsearch, helpers
except ImportError:
    print("Installing elasticsearch package...")
    import subprocess
    subprocess.run(["pip", "install", "elasticsearch"])
    from elasticsearch import Elasticsearch, helpers

# Paths
INPUT_FILE = Path(__file__).parent.parent.parent / "data" / "interim" / "S1_search_results_deduplicated.csv"
OUTPUT_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_elasticsearch_filtered.csv"
STATS_FILE = Path(__file__).parent.parent.parent / "data" / "processed" / "S2_elasticsearch_stats.json"

# Elasticsearch config
ES_HOST = "http://localhost:9200"
INDEX_NAME = "papers"

# ============================================================================
# SCREENING CRITERIA AS ELASTICSEARCH QUERIES
# ============================================================================

# MUST contain at least one of these (deep learning indicators)
DEEP_LEARNING_TERMS = [
    "deep learning", "neural network", "CNN", "convolutional neural network",
    "U-Net", "UNet", "encoder-decoder", "transformer", "attention mechanism",
    "ResNet", "VNet", "V-Net", "DenseNet", "SegNet", "FCN", "fully convolutional",
    "3D CNN", "3D convolutional", "encoder decoder", "skip connection",
    "feature pyramid", "LSTM", "GAN", "generative adversarial",
    "self-supervised", "semi-supervised", "transfer learning", "fine-tuning",
    "backbone", "pretrained", "pre-trained", "end-to-end"
]

# MUST contain at least one of these (segmentation indicators)
SEGMENTATION_TERMS = [
    "segmentation", "segment", "delineation", "contour", "boundary",
    "volumetric", "voxel", "3D reconstruction", "mask", "region of interest",
    "ROI", "dice", "DSC", "IoU", "Hausdorff", "surface distance"
]

# MUST contain at least one of these (CT imaging indicators)
CT_TERMS = [
    "CT", "computed tomography", "CT scan", "CT image", "CT volume",
    "contrast-enhanced CT", "CECT", "non-contrast CT", "NCCT",
    "abdominal CT", "thoracic CT", "chest CT", "CT dataset"
]

# MUST contain at least one of these (organ indicators)
ORGAN_TERMS = [
    "liver", "kidney", "spleen", "pancreas", "lung", "heart", "stomach",
    "gallbladder", "bladder", "prostate", "colon", "esophagus", "adrenal",
    "organ", "multi-organ", "abdominal organ", "thoracic organ",
    "organs at risk", "OAR", "anatomy", "anatomical structure"
]

# SHOULD NOT contain these (exclusion indicators - reduces score but doesn't exclude)
EXCLUSION_SOFT = [
    "review paper", "survey paper", "literature review", "systematic review",
    "MRI only", "ultrasound only", "X-ray only", "mammography",
    "tumor detection", "lesion detection", "nodule detection",
    "bone segmentation", "vessel segmentation", "airway segmentation"
]

# MUST NOT contain these (hard exclusion)
EXCLUSION_HARD = [
    # These would be very strong indicators of irrelevance
    # Keep minimal to avoid false negatives
]


def load_papers():
    """Load papers from CSV."""
    papers = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            paper = {
                'id': i,
                'doi': row.get('doi', ''),
                'title': row.get('title', ''),
                'abstract': row.get('abstract_snippet', '') or row.get('abstract', ''),
                'year': row.get('year', ''),
                'source': row.get('source', ''),
                'authors': row.get('authors', '')
            }
            # Combine title and abstract for full-text search
            paper['full_text'] = f"{paper['title']} {paper['abstract']}"
            papers.append(paper)
    return papers


def wait_for_elasticsearch(es, max_wait=60):
    """Wait for Elasticsearch to be ready."""
    print("Waiting for Elasticsearch...")
    for i in range(max_wait):
        try:
            if es.ping():
                print("✅ Elasticsearch is ready!")
                return True
        except:
            pass
        time.sleep(1)
        if i % 10 == 0:
            print(f"  Still waiting... ({i}s)")
    return False


def create_index(es):
    """Create index with appropriate mappings."""
    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "doi": {"type": "keyword"},
                "title": {"type": "text", "analyzer": "english"},
                "abstract": {"type": "text", "analyzer": "english"},
                "full_text": {"type": "text", "analyzer": "english"},
                "year": {"type": "keyword"},
                "source": {"type": "keyword"},
                "authors": {"type": "text"}
            }
        },
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }
    
    if es.indices.exists(index=INDEX_NAME):
        print(f"Deleting existing index '{INDEX_NAME}'...")
        es.indices.delete(index=INDEX_NAME)
    
    print(f"Creating index '{INDEX_NAME}'...")
    es.indices.create(index=INDEX_NAME, body=mapping)


def index_papers(es, papers):
    """Bulk index papers."""
    print(f"Indexing {len(papers)} papers...")
    
    actions = [
        {
            "_index": INDEX_NAME,
            "_id": paper['id'],
            "_source": paper
        }
        for paper in papers
    ]
    
    helpers.bulk(es, actions, refresh=True)
    print(f"✅ Indexed {len(papers)} papers")


def build_screening_query(min_score=10):
    """
    Build Elasticsearch query based on screening criteria.
    
    Scoring:
    - Deep learning terms: +10 each (MUST have at least one)
    - Segmentation terms: +10 each (MUST have at least one)
    - CT terms: +10 each (MUST have at least one)
    - Organ terms: +10 each (MUST have at least one)
    - Exclusion terms: -5 each (soft penalty)
    """
    
    query = {
        "bool": {
            "must": [
                # Must have deep learning indicator
                {
                    "bool": {
                        "should": [
                            {"match_phrase": {"full_text": {"query": term, "boost": 10}}}
                            for term in DEEP_LEARNING_TERMS
                        ],
                        "minimum_should_match": 1
                    }
                },
                # Must have segmentation indicator
                {
                    "bool": {
                        "should": [
                            {"match_phrase": {"full_text": {"query": term, "boost": 10}}}
                            for term in SEGMENTATION_TERMS
                        ],
                        "minimum_should_match": 1
                    }
                },
                # Must have CT indicator
                {
                    "bool": {
                        "should": [
                            {"match_phrase": {"full_text": {"query": term, "boost": 10}}}
                            for term in CT_TERMS
                        ],
                        "minimum_should_match": 1
                    }
                },
                # Must have organ indicator
                {
                    "bool": {
                        "should": [
                            {"match_phrase": {"full_text": {"query": term, "boost": 10}}}
                            for term in ORGAN_TERMS
                        ],
                        "minimum_should_match": 1
                    }
                }
            ],
            "should": [
                # Boost papers with multiple matching terms
                {"match": {"full_text": {"query": " ".join(DEEP_LEARNING_TERMS[:10]), "boost": 2}}},
                {"match": {"full_text": {"query": " ".join(ORGAN_TERMS), "boost": 2}}},
                # Boost specific high-value phrases
                {"match_phrase": {"full_text": {"query": "3D segmentation", "boost": 20}}},
                {"match_phrase": {"full_text": {"query": "organ segmentation", "boost": 20}}},
                {"match_phrase": {"full_text": {"query": "CT segmentation", "boost": 20}}},
                {"match_phrase": {"full_text": {"query": "abdominal CT", "boost": 15}}},
                {"match_phrase": {"full_text": {"query": "multi-organ", "boost": 15}}},
            ],
            "must_not": [
                {"match_phrase": {"full_text": term}}
                for term in EXCLUSION_HARD
            ] if EXCLUSION_HARD else []
        }
    }
    
    return query


def run_screening(es):
    """Run the screening query and return results."""
    query = build_screening_query()
    
    # First, count total matches
    count_result = es.count(index=INDEX_NAME, body={"query": query})
    total_matches = count_result['count']
    print(f"\n📊 Query matched {total_matches} papers")
    
    # Get all matching papers with scores
    results = es.search(
        index=INDEX_NAME,
        body={
            "query": query,
            "size": total_matches,
            "sort": [{"_score": "desc"}],
            "_source": True
        }
    )
    
    papers = []
    for hit in results['hits']['hits']:
        paper = hit['_source']
        paper['es_score'] = hit['_score']
        papers.append(paper)
    
    return papers


def analyze_results(papers, all_papers):
    """Analyze and categorize results."""
    if not papers:
        return {
            'total_input': len(all_papers),
            'total_matched': 0,
            'reduction_rate': 100.0
        }
    
    scores = [p['es_score'] for p in papers]
    
    # Score distribution
    high_confidence = [p for p in papers if p['es_score'] >= 50]
    medium_confidence = [p for p in papers if 30 <= p['es_score'] < 50]
    low_confidence = [p for p in papers if p['es_score'] < 30]
    
    stats = {
        'total_input': len(all_papers),
        'total_matched': len(papers),
        'reduction_rate': round((1 - len(papers) / len(all_papers)) * 100, 1),
        'score_min': round(min(scores), 2),
        'score_max': round(max(scores), 2),
        'score_mean': round(sum(scores) / len(scores), 2),
        'high_confidence': len(high_confidence),
        'medium_confidence': len(medium_confidence),
        'low_confidence': len(low_confidence),
        'timestamp': datetime.now().isoformat()
    }
    
    return stats


def save_results(papers, stats):
    """Save filtered papers to CSV."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Save filtered papers
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'doi', 'title', 'abstract', 'year', 'source', 'authors', 'es_score', 'es_decision']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for paper in papers:
            row = {k: paper.get(k, '') for k in fieldnames if k != 'es_decision'}
            # Add decision based on score
            if paper['es_score'] >= 50:
                row['es_decision'] = 'HIGH_RELEVANCE'
            elif paper['es_score'] >= 30:
                row['es_decision'] = 'MEDIUM_RELEVANCE'
            else:
                row['es_decision'] = 'LOW_RELEVANCE'
            writer.writerow(row)
    
    print(f"\n✅ Saved {len(papers)} papers to {OUTPUT_FILE.name}")
    
    # Save stats
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"✅ Saved stats to {STATS_FILE.name}")


def main():
    print("=" * 60)
    print("ELASTICSEARCH KEYWORD SCREENING")
    print("=" * 60)
    
    # Load papers
    all_papers = load_papers()
    print(f"\n📄 Loaded {len(all_papers)} papers from {INPUT_FILE.name}")
    
    # Connect to Elasticsearch
    print(f"\n🔌 Connecting to Elasticsearch at {ES_HOST}...")
    es = Elasticsearch([ES_HOST])
    
    if not wait_for_elasticsearch(es):
        print("\n❌ Elasticsearch not available!")
        print("\nStart it with Docker:")
        print("  docker run -d --name elasticsearch -p 9200:9200 -e 'discovery.type=single-node' -e 'xpack.security.enabled=false' elasticsearch:8.11.0")
        return
    
    # Index papers
    create_index(es)
    index_papers(es, all_papers)
    
    # Run screening
    print("\n🔍 Running screening query...")
    filtered_papers = run_screening(es)
    
    # Analyze results
    stats = analyze_results(filtered_papers, all_papers)
    
    # Print summary
    print("\n" + "=" * 60)
    print("SCREENING RESULTS")
    print("=" * 60)
    print(f"📥 Input papers:     {stats['total_input']}")
    print(f"📤 Matched papers:   {stats['total_matched']}")
    print(f"📉 Reduction:        {stats['reduction_rate']}%")
    print(f"\n📊 Score distribution:")
    print(f"   High (≥50):       {stats.get('high_confidence', 0)} papers")
    print(f"   Medium (30-49):   {stats.get('medium_confidence', 0)} papers")
    print(f"   Low (<30):        {stats.get('low_confidence', 0)} papers")
    
    if filtered_papers:
        print(f"\n🏆 Top 5 papers by relevance score:")
        for i, paper in enumerate(filtered_papers[:5], 1):
            title = paper['title'][:60] + "..." if len(paper['title']) > 60 else paper['title']
            print(f"   {i}. [{paper['es_score']:.1f}] {title}")
    
    # Save results
    save_results(filtered_papers, stats)
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print(f"1. Review high-confidence papers ({stats.get('high_confidence', 0)}) - likely INCLUDE")
    print(f"2. AI-screen medium-confidence papers ({stats.get('medium_confidence', 0)})")
    print(f"3. Papers not matched by Elasticsearch are likely EXCLUDE")


if __name__ == "__main__":
    main()
