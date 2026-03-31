#!/usr/bin/env python3
"""
S2 - Elasticsearch-based Paper Filtering
Pre-filters papers using keyword matching before AI screening.

This reduces the paper count significantly by:
1. Indexing all papers in Elasticsearch
2. Running boolean queries for inclusion/exclusion criteria
3. Outputting filtered papers for manual review or AI screening
"""

import csv
import json
import time
from pathlib import Path
from elasticsearch import Elasticsearch

# Paths
INPUT_FILE = Path(__file__).parent.parent.parent.parent / "data" / "interim" / "S1_search_results_deduplicated.csv"
OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "data" / "processed"

ES_HOST = "http://localhost:9200"
INDEX_NAME = "papers"


def wait_for_elasticsearch():
    """Wait for Elasticsearch to be ready."""
    es = Elasticsearch(ES_HOST)
    print("Waiting for Elasticsearch...")
    for i in range(30):
        try:
            info = es.info()
            if info:
                print("✅ Elasticsearch is ready!")
                return es
        except Exception as e:
            pass
        time.sleep(2)
        print(f"  Waiting... ({i+1}/30)")
    raise Exception("Elasticsearch not available after 60 seconds")


def create_index(es):
    """Create the papers index with proper mappings."""
    mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text", "analyzer": "english"},
                "abstract": {"type": "text", "analyzer": "english"},
                "year": {"type": "integer"},
                "doi": {"type": "keyword"},
                "source": {"type": "keyword"},
                "combined_text": {"type": "text", "analyzer": "english"}
            }
        }
    }
    
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
    es.indices.create(index=INDEX_NAME, body=mapping)
    print(f"✅ Created index: {INDEX_NAME}")


def index_papers(es):
    """Index all papers from CSV."""
    papers = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)
    
    print(f"Indexing {len(papers)} papers...")
    
    for i, paper in enumerate(papers):
        title = paper.get('title', '')
        abstract = paper.get('abstract_snippet', '') or paper.get('abstract', '')
        
        doc = {
            "title": title,
            "abstract": abstract,
            "year": int(paper.get('year', 0)) if paper.get('year', '').isdigit() else 0,
            "doi": paper.get('doi', ''),
            "source": paper.get('source', ''),
            "combined_text": f"{title} {abstract}",
            "_original": paper  # Keep original data
        }
        
        es.index(index=INDEX_NAME, id=i, document=doc)
        
        if (i + 1) % 500 == 0:
            print(f"  Indexed {i+1}/{len(papers)}")
    
    es.indices.refresh(index=INDEX_NAME)
    print(f"✅ Indexed {len(papers)} papers")
    return papers


def filter_papers(es):
    """
    Filter papers using Elasticsearch boolean queries.
    
    INCLUSION (must have ALL):
    - Deep learning terms
    - Segmentation terms  
    - CT imaging terms
    - Organ terms
    
    EXCLUSION (must NOT have exclusively):
    - MRI-only, ultrasound-only
    - Detection/classification only (without segmentation)
    - Review/survey papers
    """
    
    # === INCLUSION QUERY ===
    # Papers must mention deep learning AND segmentation AND CT AND organs
    
    inclusion_query = {
        "bool": {
            "must": [
                # IC1: Deep Learning
                {
                    "bool": {
                        "should": [
                            {"match_phrase": {"combined_text": "deep learning"}},
                            {"match_phrase": {"combined_text": "neural network"}},
                            {"match_phrase": {"combined_text": "convolutional neural"}},
                            {"match": {"combined_text": "CNN"}},
                            {"match": {"combined_text": "U-Net"}},
                            {"match": {"combined_text": "UNet"}},
                            {"match_phrase": {"combined_text": "encoder decoder"}},
                            {"match": {"combined_text": "transformer"}},
                            {"match": {"combined_text": "ResNet"}},
                            {"match": {"combined_text": "VNet"}},
                            {"match_phrase": {"combined_text": "attention mechanism"}},
                            {"match_phrase": {"combined_text": "fully convolutional"}},
                            {"match": {"combined_text": "FCN"}},
                            {"match": {"combined_text": "nnU-Net"}},
                            {"match": {"combined_text": "nnUNet"}},
                            {"match": {"combined_text": "MONAI"}},
                            {"match": {"combined_text": "autoencoder"}},
                        ],
                        "minimum_should_match": 1
                    }
                },
                # IC2: Segmentation (3D preferred)
                {
                    "bool": {
                        "should": [
                            {"match": {"combined_text": "segmentation"}},
                            {"match": {"combined_text": "segmenting"}},
                            {"match_phrase": {"combined_text": "semantic segmentation"}},
                            {"match_phrase": {"combined_text": "volumetric segmentation"}},
                            {"match_phrase": {"combined_text": "3D segmentation"}},
                            {"match_phrase": {"combined_text": "multi-organ"}},
                            {"match_phrase": {"combined_text": "organ segmentation"}},
                            {"match": {"combined_text": "delineation"}},
                        ],
                        "minimum_should_match": 1
                    }
                },
                # IC3: CT imaging
                {
                    "bool": {
                        "should": [
                            {"match": {"combined_text": "CT"}},
                            {"match_phrase": {"combined_text": "computed tomography"}},
                            {"match_phrase": {"combined_text": "CT scan"}},
                            {"match_phrase": {"combined_text": "CT image"}},
                            {"match_phrase": {"combined_text": "CT volume"}},
                            {"match_phrase": {"combined_text": "abdominal CT"}},
                            {"match_phrase": {"combined_text": "chest CT"}},
                            {"match_phrase": {"combined_text": "contrast-enhanced"}},
                            {"match": {"combined_text": "CECT"}},
                        ],
                        "minimum_should_match": 1
                    }
                },
                # IC4: Organs
                {
                    "bool": {
                        "should": [
                            {"match": {"combined_text": "liver"}},
                            {"match": {"combined_text": "kidney"}},
                            {"match": {"combined_text": "spleen"}},
                            {"match": {"combined_text": "pancreas"}},
                            {"match": {"combined_text": "lung"}},
                            {"match": {"combined_text": "heart"}},
                            {"match": {"combined_text": "stomach"}},
                            {"match": {"combined_text": "gallbladder"}},
                            {"match": {"combined_text": "bladder"}},
                            {"match": {"combined_text": "prostate"}},
                            {"match": {"combined_text": "colon"}},
                            {"match": {"combined_text": "esophagus"}},
                            {"match_phrase": {"combined_text": "adrenal gland"}},
                            {"match_phrase": {"combined_text": "abdominal organ"}},
                            {"match_phrase": {"combined_text": "multi-organ"}},
                            {"match_phrase": {"combined_text": "organs at risk"}},
                            {"match": {"combined_text": "OAR"}},
                            {"match": {"combined_text": "hepatic"}},
                            {"match": {"combined_text": "renal"}},
                            {"match": {"combined_text": "pulmonary"}},
                            {"match": {"combined_text": "cardiac"}},
                        ],
                        "minimum_should_match": 1
                    }
                }
            ],
            # EXCLUSION: Filter out obvious non-matches
            "must_not": [
                # Exclude pure review/survey papers
                {"match_phrase": {"title": "systematic review"}},
                {"match_phrase": {"title": "literature review"}},
                {"match_phrase": {"title": "survey of"}},
                {"match_phrase": {"title": "a review"}},
                # Exclude if ONLY mentions non-CT modalities in title
                # (we keep papers that mention CT + other modalities)
            ]
        }
    }
    
    # Execute search - get all matching papers
    result = es.search(
        index=INDEX_NAME,
        query=inclusion_query,
        size=10000  # Get all matches
    )
    
    included_papers = []
    for hit in result['hits']['hits']:
        paper = hit['_source'].get('_original', {})
        paper['es_score'] = hit['_score']
        paper['es_id'] = hit['_id']
        included_papers.append(paper)
    
    return included_papers


def apply_exclusion_filters(papers):
    """
    Apply additional exclusion rules (STRICT/CONSERVATIVE).
    If there's any doubt, EXCLUDE the paper.
    """
    filtered = []
    excluded_reasons = {}
    
    for paper in papers:
        title = paper.get('title', '').lower()
        abstract = (paper.get('abstract_snippet', '') or paper.get('abstract', '')).lower()
        combined = f"{title} {abstract}"

        exclude = False
        reason = None

        # === STRICT IC2: Require explicit 3D/volumetric terms ===
        terms_3d = [
            '3d', '3-d', 'three-dimensional', 'volumetric', 'volume', 'v-net', 'vnet', '3d u-net', '3d unet',
            'volumetric segmentation', '3d segmentation', '3d convolution', '3d cnn', '3d network', '3d model', '3d architecture'
        ]
        has_3d = any(term in combined for term in terms_3d)
        if not has_3d:
            exclude = True
            reason = "No explicit 3D/volumetric method"

        # === EC2: Non-CT modalities exclusively ===
        if not exclude:
            ct_terms = ['ct ', 'ct,', 'ct.', 'computed tomography', 'ct scan', 'ct image', 'ct volume', 'ct data']
            has_ct = any(term in combined for term in ct_terms)

            mri_terms = ['mri', 'magnetic resonance', 'mr image', 'mr scan']
            us_terms = ['ultrasound', 'ultrasonography', 'sonograph', 'echocardiograph']
            xray_terms = ['x-ray', 'xray', 'radiograph', 'mammograph', 'fluoroscop']
            pet_terms = ['pet scan', 'pet image', 'positron emission']

            has_mri = any(term in combined for term in mri_terms)
            has_us = any(term in combined for term in us_terms)
            has_xray = any(term in combined for term in xray_terms)
            has_pet = any(term in combined for term in pet_terms)

            if not has_ct:
                exclude = True
                reason = "No CT mentioned"
            elif has_mri and not has_ct:
                exclude = True
                reason = "MRI-only"
            elif has_us and not has_ct:
                exclude = True
                reason = "Ultrasound-only"
            elif has_xray and not has_ct:
                exclude = True
                reason = "X-ray-only"

        # === EC3: Non-organ targets exclusively ===
        if not exclude:
            organ_terms = ['liver', 'kidney', 'spleen', 'pancreas', 'lung', 'heart',
                           'stomach', 'gallbladder', 'bladder', 'prostate', 'colon',
                           'esophagus', 'adrenal', 'organ', 'hepatic', 'renal', 'pulmonary', 'cardiac',
                           'multi-organ', 'abdominal organ', 'thoracic organ']
            has_organ = any(term in combined for term in organ_terms)

            # Tumor/lesion only papers
            tumor_terms = ['tumor', 'tumour', 'lesion', 'nodule', 'cancer', 'carcinoma',
                          'metastasis', 'malignant', 'benign', 'polyp', 'cyst']
            vessel_terms = ['vessel', 'artery', 'vein', 'aorta', 'vascular', 'angiograph']
            bone_terms = ['bone', 'skeletal', 'vertebra', 'spine', 'rib', 'fracture']
            muscle_terms = ['muscle', 'adipose', 'fat tissue', 'body composition']
            airway_terms = ['airway', 'bronchi', 'trachea']
            covid_terms = ['covid', 'coronavirus', 'sars-cov', 'infection', 'pneumonia']

            has_tumor = any(term in combined for term in tumor_terms)
            has_vessel = any(term in combined for term in vessel_terms)
            has_bone = any(term in combined for term in bone_terms)
            has_muscle = any(term in combined for term in muscle_terms)
            has_airway = any(term in combined for term in airway_terms)
            has_covid = any(term in combined for term in covid_terms)

            # Exclude if non-organ target and no organ mentioned
            if has_tumor and not has_organ:
                exclude = True
                reason = "Tumor/lesion only (no organ)"
            elif has_vessel and not has_organ:
                exclude = True
                reason = "Vessel only"
            elif has_bone and not has_organ:
                exclude = True
                reason = "Bone/skeletal only"
            elif has_muscle and not has_organ:
                exclude = True
                reason = "Muscle/adipose only"
            elif has_airway and not has_organ:
                exclude = True
                reason = "Airway only"
            elif has_covid and not has_organ:
                exclude = True
                reason = "COVID/infection only"

        # === EC1: Detection/classification only (no segmentation) ===
        if not exclude:
            seg_terms = ['segment', 'delineat', 'contour', 'boundary', 'mask']
            has_segmentation = any(term in combined for term in seg_terms)

            detect_terms = ['detection', 'detect ', 'classification', 'classify', 'diagnosis', 'diagnos']
            is_detection = any(term in combined for term in detect_terms)

            if is_detection and not has_segmentation:
                exclude = True
                reason = "Detection/classification only"

        # === EC4: 2D-only methods (already excluded by strict 3D requirement above) ===
        # No need to check again; all papers must have explicit 3D/volumetric terms

        # === EC5: Non-deep learning ===
        if not exclude:
            non_dl_terms = ['random forest', 'support vector', 'svm', 'decision tree',
                            'hand-crafted', 'handcrafted', 'traditional method', 'atlas-based',
                            'level set', 'active contour', 'region growing', 'watershed',
                            'thresholding', 'k-means', 'k-nearest', 'naive bayes', 'logistic regression']
            dl_terms = ['deep learning', 'neural network', 'cnn', 'convolutional', 'u-net', 'unet',
                       'transformer', 'encoder-decoder', 'resnet', 'vgg', 'densenet', 'attention']

            has_non_dl = any(term in combined for term in non_dl_terms)
            has_dl = any(term in combined for term in dl_terms)

            if has_non_dl and not has_dl:
                exclude = True
                reason = "Non-deep learning"

        # === EC6: Review/survey papers ===
        if not exclude:
            review_terms = ['systematic review', 'literature review', 'survey of', 'a review',
                          'state-of-the-art review', 'comprehensive review', 'overview of',
                          'meta-analysis', 'scoping review']
            is_review = any(term in title for term in review_terms)

            if is_review:
                exclude = True
                reason = "Review/survey paper"

        # === STRICT IC5: Require mention of method/approach/network/model/algorithm/architecture ===
        if not exclude:
            method_terms = ['method', 'approach', 'network', 'architecture', 'model', 'algorithm']
            has_method = any(term in combined for term in method_terms)
            dataset_terms = ['dataset', 'benchmark dataset', 'data collection', 'annotation']
            is_dataset_only = any(term in title for term in dataset_terms) and not has_method
            if not has_method or is_dataset_only:
                exclude = True
                reason = "No original method/approach/network/model/algorithm/architecture"

        # === Additional strict organ check ===
        if not exclude:
            organ_check = ['liver', 'kidney', 'spleen', 'pancreas', 'lung', 'heart',
                          'stomach', 'gallbladder', 'bladder', 'prostate', 'colon',
                          'esophagus', 'adrenal', 'abdominal', 'thoracic', 'multi-organ', 'oar']
            has_specific_organ = any(term in combined for term in organ_check)

            if not has_specific_organ:
                exclude = True
                reason = "No specific organ target"

        if exclude:
            excluded_reasons[reason] = excluded_reasons.get(reason, 0) + 1
        else:
            filtered.append(paper)
    
    print("\n📋 Exclusion summary (STRICT filtering):")
    for reason, count in sorted(excluded_reasons.items(), key=lambda x: -x[1]):
        print(f"   {reason}: {count} papers")
    
    return filtered


def save_results(papers, filename):
    """Save filtered papers to CSV."""
    output_file = OUTPUT_DIR / filename
    
    if not papers:
        print("No papers to save!")
        return
    
    # Get all fieldnames from first paper
    fieldnames = list(papers[0].keys())
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"✅ Saved {len(papers)} papers to {output_file}")


def main():
    print("=" * 60)
    print("  ELASTICSEARCH PAPER FILTERING")
    print("=" * 60)
    
    # Connect to Elasticsearch
    es = wait_for_elasticsearch()
    
    # Create index and load papers
    create_index(es)
    papers = index_papers(es)
    
    print(f"\n📊 Starting with {len(papers)} papers")
    
    # Filter using Elasticsearch
    print("\n🔍 Running Elasticsearch inclusion query...")
    es_filtered = filter_papers(es)
    print(f"   After ES query: {len(es_filtered)} papers ({len(es_filtered)/len(papers)*100:.1f}%)")
    
    # Apply additional exclusion filters
    print("\n🔍 Applying exclusion filters...")
    final_filtered = apply_exclusion_filters(es_filtered)
    print(f"   After exclusions: {len(final_filtered)} papers ({len(final_filtered)/len(papers)*100:.1f}%)")
    
    # Save results
    print("\n💾 Saving results...")
    save_results(final_filtered, "S2_elasticsearch_filtered.csv")
    
    # Summary
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"  Original papers:     {len(papers):,}")
    print(f"  After ES filtering:  {len(es_filtered):,} ({len(es_filtered)/len(papers)*100:.1f}%)")
    print(f"  After exclusions:    {len(final_filtered):,} ({len(final_filtered)/len(papers)*100:.1f}%)")
    print(f"  Reduction:           {len(papers) - len(final_filtered):,} papers removed ({(len(papers) - len(final_filtered))/len(papers)*100:.1f}%)")
    print("=" * 60)
    
    return final_filtered


if __name__ == "__main__":
    main()
