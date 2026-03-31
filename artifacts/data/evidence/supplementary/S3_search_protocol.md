# S3: Complete Search Protocol and Query Strings

## 1. Search Objective

Comprehensive identification of studies addressing 3D organ segmentation from CT scans using deep learning methods, including foundational architectures, benchmark datasets, specialized loss functions, and clinical applications.

## 2. Eligibility Criteria

### 2.1 Inclusion Criteria

| Code | Criterion | Operationalization |
|------|-----------|-------------------|
| IC1 | Peer-reviewed publication | Published in indexed journals, conferences, or established preprint servers (arXiv) with >10 citations |
| IC2 | 3D medical imaging focus | Study addresses volumetric (3D) image analysis, not exclusively 2D |
| IC3 | Segmentation task | Primary focus on semantic/instance segmentation (not detection, classification, or registration only) |
| IC4 | Deep learning methods | Uses neural network approaches (CNN, Transformer, hybrid, foundation models) |
| IC5 | CT modality included | Includes CT imaging (may also include MRI or other modalities) |
| IC6 | Quantitative evaluation | Reports numerical performance metrics (Dice, IoU, Hausdorff distance, etc.) |

### 2.2 Exclusion Criteria

| Code | Criterion | Rationale |
|------|-----------|-----------|
| EC1 | Non-English publications | Language accessibility |
| EC2 | Abstract-only publications | Insufficient methodological detail |
| EC3 | Duplicate publications | Avoid counting same work multiple times |
| EC4 | 2D-only methods without 3D extension | Out of scope |
| EC5 | Pre-deep learning methods only | Historical context included in review sections only |
| EC6 | Conference abstracts without full paper | Insufficient detail for reproducibility |

## 3. Database Search Strategies

### 3.1 PubMed (executed 2025-09-15)

**Query ID: PUB-001**
```
((("deep learning"[Title/Abstract] OR "neural network"[Title/Abstract] OR 
"convolutional neural network"[Title/Abstract] OR "CNN"[Title/Abstract] OR 
"transformer"[Title/Abstract] OR "U-Net"[Title/Abstract] OR 
"encoder-decoder"[Title/Abstract] OR "attention"[Title/Abstract]))
AND
(("segmentation"[Title/Abstract] OR "semantic segmentation"[Title/Abstract] OR 
"organ segmentation"[Title/Abstract] OR "multi-organ"[Title/Abstract]))
AND
(("computed tomography"[Title/Abstract] OR "CT scan"[Title/Abstract] OR 
"CT imaging"[Title/Abstract] OR "abdominal CT"[Title/Abstract] OR 
"chest CT"[Title/Abstract] OR "3D imaging"[Title/Abstract] OR 
"volumetric"[Title/Abstract]))
AND
("2015"[Date - Publication] : "2025"[Date - Publication]))
```

**Filters applied:**
- Publication date: 2015-01-01 to 2025-09-15
- Article types: Journal Article, Review, Preprint
- Species: Humans
- Language: English

**Results: 487 records**

---

**Query ID: PUB-002 (Foundation models supplement)**
```
((("segment anything"[Title/Abstract] OR "SAM"[Title/Abstract] OR 
"foundation model"[Title/Abstract] OR "universal segmentation"[Title/Abstract] OR 
"MedSAM"[Title/Abstract] OR "SAM-Med"[Title/Abstract]))
AND
(("medical imaging"[Title/Abstract] OR "CT"[Title/Abstract] OR 
"organ"[Title/Abstract] OR "segmentation"[Title/Abstract]))
AND
("2023"[Date - Publication] : "2025"[Date - Publication]))
```

**Results: 78 records**

---

### 3.2 IEEE Xplore (executed 2025-09-16)

**Query ID: IEEE-001**
```
(("All Metadata":"deep learning" OR "All Metadata":"neural network" OR 
"All Metadata":"CNN" OR "All Metadata":"transformer" OR 
"All Metadata":"U-Net" OR "All Metadata":"UNETR")
AND
("All Metadata":"segmentation" OR "All Metadata":"semantic segmentation")
AND
("All Metadata":"CT" OR "All Metadata":"computed tomography" OR 
"All Metadata":"medical imaging" OR "All Metadata":"3D" OR 
"All Metadata":"volumetric")
AND
("All Metadata":"organ" OR "All Metadata":"liver" OR 
"All Metadata":"kidney" OR "All Metadata":"pancreas" OR 
"All Metadata":"spleen" OR "All Metadata":"multi-organ" OR 
"All Metadata":"abdominal"))
```

**Filters applied:**
- Year: 2015-2025
- Content Type: Journals, Conferences
- Publisher: IEEE

**Results: 312 records**

---

**Query ID: IEEE-002 (Loss functions supplement)**
```
(("All Metadata":"loss function" OR "All Metadata":"Dice loss" OR 
"All Metadata":"Hausdorff" OR "All Metadata":"boundary loss" OR 
"All Metadata":"focal loss" OR "All Metadata":"Tversky")
AND
("All Metadata":"segmentation" OR "All Metadata":"medical imaging")
AND
("All Metadata":"deep learning" OR "All Metadata":"neural network"))
```

**Results: 89 records**

---

### 3.3 arXiv (executed 2025-09-17)

**Query ID: ARXIV-001**
```
(ti:"segmentation" OR abs:"segmentation") AND 
(ti:"CT" OR ti:"computed tomography" OR abs:"CT scan" OR abs:"medical imaging") AND
(ti:"deep learning" OR ti:"neural network" OR ti:"transformer" OR 
ti:"U-Net" OR abs:"deep learning" OR abs:"convolutional")
```

**Categories searched:**
- cs.CV (Computer Vision)
- cs.LG (Machine Learning)
- eess.IV (Image and Video Processing)

**Date range:** 2015-01-01 to 2025-09-17

**Results: 234 records**

---

**Query ID: ARXIV-002 (State space models supplement)**
```
(ti:"Mamba" OR abs:"state space model" OR abs:"SSM") AND
(ti:"medical" OR ti:"segmentation" OR abs:"CT" OR abs:"MRI")
```

**Date range:** 2023-01-01 to 2025-09-17

**Results: 47 records**

---

### 3.4 Scopus (executed 2025-09-18)

**Query ID: SCOP-001**
```
TITLE-ABS-KEY(("deep learning" OR "neural network" OR "CNN" OR 
"convolutional" OR "transformer" OR "U-Net" OR "attention mechanism") 
AND ("segmentation" OR "semantic segmentation" OR "organ segmentation") 
AND ("CT" OR "computed tomography" OR "3D" OR "volumetric" OR "medical imaging") 
AND ("liver" OR "kidney" OR "pancreas" OR "spleen" OR "organ" OR "multi-organ" OR "abdominal"))
AND PUBYEAR > 2014 AND PUBYEAR < 2026
```

**Filters applied:**
- Document type: Article, Conference Paper, Review
- Source type: Journal, Conference Proceeding
- Language: English
- Subject area: Computer Science, Medicine, Engineering

**Results: 298 records**

---

### 3.5 ACM Digital Library (executed 2025-09-18)

**Query ID: ACM-001**
```
[[All: "deep learning"] OR [All: "neural network"] OR [All: "transformer"]] 
AND [[All: "segmentation"]] 
AND [[All: "medical imaging"] OR [All: "CT"] OR [All: "computed tomography"]]
AND [[All: "organ"] OR [All: "3D"] OR [All: "volumetric"]]
```

**Filters applied:**
- Publication Date: Custom range 2015-2025
- Content Type: Research Article, Review Article

**Results: 56 records**

---

## 4. Citation Tracking Protocol

### 4.1 Forward Citation Tracking

Starting from 12 seminal papers identified during initial screening:

| Seed Paper | Citations Screened | New Records |
|------------|-------------------|-------------|
| nnU-Net (Isensee 2021) | 3,847 | 34 |
| U-Net (Ronneberger 2015) | 47,892 | 28 |
| TotalSegmentator (Wasserthal 2023) | 412 | 12 |
| UNETR (Hatamizadeh 2022) | 1,234 | 18 |
| TransUNet (Chen 2021) | 2,156 | 15 |
| SAM (Kirillov 2023) | 4,567 | 21 |
| MedSAM (Ma 2024) | 234 | 8 |
| MSD (Antonelli 2022) | 567 | 11 |
| Swin UNETR (Hatamizadeh 2022) | 892 | 14 |
| CoTr (Xie 2021) | 423 | 9 |
| nnFormer (Zhou 2021) | 512 | 7 |
| STU-Net (Huang 2023) | 156 | 4 |

**Total forward citations screened: 62,892**
**New records identified: 181**
**After duplicate removal: 98**

### 4.2 Backward Citation Tracking

Reference lists of 47 included methods papers systematically screened:

- Total references screened: 2,847
- New records identified: 89
- After duplicate removal: 58

### 4.3 Citation Tracking Summary

| Source | Records Identified |
|--------|-------------------|
| Forward citations | 98 |
| Backward citations | 58 |
| **Total citation tracking** | **156** |

---

## 5. Search Results Summary

| Database | Query ID | Date | Records |
|----------|----------|------|---------|
| PubMed | PUB-001 | 2025-09-15 | 487 |
| PubMed | PUB-002 | 2025-09-15 | 78 |
| IEEE Xplore | IEEE-001 | 2025-09-16 | 312 |
| IEEE Xplore | IEEE-002 | 2025-09-16 | 89 |
| arXiv | ARXIV-001 | 2025-09-17 | 234 |
| arXiv | ARXIV-002 | 2025-09-17 | 47 |
| Scopus | SCOP-001 | 2025-09-18 | 298 |
| ACM DL | ACM-001 | 2025-09-18 | 56 |
| **Subtotal databases** | | | **1,601** |
| Duplicates removed | | | -354 |
| **Unique database records** | | | **1,247** |
| Citation tracking | | | 156 |
| **Total unique records** | | | **1,403** |

---

## 6. Screening Process

### 6.1 Title/Abstract Screening

**Method:** AI-assisted screening using Claude 3.5 Sonnet with 3-run consensus voting (see S4_ai_screening_protocol.md)

| Outcome | Count |
|---------|-------|
| Passed to full-text | 287 |
| Excluded | 1,116 |

### 6.2 Full-Text Screening

| Outcome | Count |
|---------|-------|
| Included | 127 |
| Excluded - No full text | 23 |
| Excluded - Wrong study type | 41 |
| Excluded - No quantitative results | 34 |
| Excluded - Not CT/3D | 28 |
| Excluded - Duplicate methods | 19 |
| Excluded - Other | 15 |

### 6.3 Final Included Studies

- **Total included: 127 studies**
  - Methods papers: 89
  - Review papers: 18
  - Benchmark/Challenge papers: 12
  - Framework/Software papers: 4
  - Application papers: 4

---

## 7. Inter-Rater Reliability

### 7.1 AI Screening Validation (10% sample)

- Sample size: 140 records
- Manual reviewers: 2 (MD, PhD)
- Agreement with AI consensus: 96.4% (135/140)
- Cohen's kappa (human-AI): κ = 0.89 (excellent agreement)
- Discrepancies resolved by third reviewer

### 7.2 Full-Text Screening

- Dual review: All 287 full-text articles
- Initial agreement: 94.1% (270/287)
- Cohen's kappa: κ = 0.87
- Discrepancies resolved by discussion (17 cases)

---

## 8. Search Update Protocol

### 8.1 Alert Setup

Automated weekly alerts configured for:
- PubMed: Saved search with email notification
- Google Scholar: Alerts for key terms
- Semantic Scholar: Author tracking for prolific groups

### 8.2 Final Update

- Date: 2025-10-01
- New records identified: 23
- Passed screening: 4
- Included in final analysis: 4 (included in 127 total)

---

## 9. Deviations from Protocol

None. Search protocol executed as planned in registered PROSPERO protocol (CRD42025xxxxxx).

---

## 10. Contact

For questions about the search protocol:
- Corresponding author: [corresponding author email]
- Information specialist: [librarian email]
- Last updated: 2025-10-01
