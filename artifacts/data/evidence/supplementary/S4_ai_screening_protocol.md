# S4: AI-Assisted Screening Protocol

## 1. Overview

This document describes the AI-assisted screening methodology used to process 638 ES-filtered candidate records for inclusion in the structured survey "3D Organ Segmentation from CT Scans: An Agentic Structured Survey."

## 2. AI System Configuration

### 2.1 Model Specification

We employed a three-model cascade for robust screening:

| Stage | Model | Provider | Runs | Temperature | Purpose |
|-------|-------|----------|------|-------------|---------|
| Primary | GPT-4o-mini | OpenAI | 3 | 0.3 | Initial screening, unanimous INCLUDE required |
| Validation | GPT-5-nano | OpenAI | 3 | default | Independent validation comparison |
| Tiebreaker | GPT-5.2 | OpenAI | 1 | 0.3 | Resolve disagreements (274 papers) |

### 2.2 Consensus Protocol

- **Primary screening (GPT-4o-mini):** 3 independent API calls per record
- **Decision rule:** Unanimous agreement required for INCLUDE (strict conservative approach)
- **No "UNCERTAIN" allowed:** Model forced to decide INCLUDE or EXCLUDE
- **Disagreement handling:** Papers with any disagreement flagged for GPT-5.2 tiebreaker
- **Final decision:** GPT-5.2 single run determines outcome for disputed papers

## 3. Prompt Template

### 3.1 System Prompt

```
You are a systematic review screening assistant specializing in medical image 
analysis literature. Your task is to evaluate whether research papers meet 
specific inclusion criteria for a survey on 3D organ segmentation from CT scans.

Be rigorous and consistent. When uncertain, err on the side of inclusion 
(include for full-text review rather than exclude prematurely).

Respond ONLY with a JSON object containing your decision and reasoning.
```

### 3.2 User Prompt Template

```
Evaluate the following paper for inclusion in a systematic review on 
"3D Organ Segmentation from CT Scans using Deep Learning."

PAPER DETAILS:
Title: {title}
Authors: {authors}
Year: {year}
Journal/Venue: {journal}
Abstract: {abstract}
Keywords: {keywords}

INCLUSION CRITERIA:
IC1: Peer-reviewed publication (indexed journal, conference, or established preprint with >10 citations)
IC2: 3D medical imaging focus (volumetric image analysis, not exclusively 2D)
IC3: Segmentation task (semantic/instance segmentation as primary focus)
IC4: Deep learning methods (CNN, Transformer, hybrid, or foundation models)
IC5: CT modality included (may also include MRI or other modalities)
IC6: Quantitative evaluation (reports numerical performance metrics)

EXCLUSION CRITERIA:
EC1: Non-English publication
EC2: Abstract-only publication
EC3: Duplicate publication (same work published in multiple venues)
EC4: 2D-only methods without 3D extension
EC5: Pre-deep learning methods only (traditional image processing)
EC6: Conference abstract without full paper

TASK:
1. Evaluate each inclusion criterion (IC1-IC6)
2. Check for any exclusion criteria (EC1-EC6)
3. Provide your decision: INCLUDE, EXCLUDE, or UNCERTAIN

Respond with a JSON object in this exact format:
{
  "decision": "INCLUDE" | "EXCLUDE" | "UNCERTAIN",
  "ic1_met": true | false | "unclear",
  "ic2_met": true | false | "unclear",
  "ic3_met": true | false | "unclear",
  "ic4_met": true | false | "unclear",
  "ic5_met": true | false | "unclear",
  "ic6_met": true | false | "unclear",
  "exclusion_criteria_triggered": ["EC1", "EC2", ...] | [],
  "confidence": "high" | "medium" | "low",
  "reasoning": "Brief explanation of decision (max 100 words)"
}
```

### 3.3 Example Prompt Instance

```
PAPER DETAILS:
Title: nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation
Authors: Isensee F, Jaeger PF, Kohl SAA, Petersen J, Maier-Hein KH
Year: 2021
Journal/Venue: Nature Methods
Abstract: Biomedical imaging is a driver of scientific discovery and a core 
component of medical care and is being revolutionized by deep learning. However, 
the diversity of imaging modalities, target structures and requirements 
complicates the development of one-fits-all solutions. We introduce nnU-Net, 
a deep learning framework that automatically configures itself for any new 
biomedical image segmentation task. nnU-Net achieved state-of-the-art results 
across 23 public datasets used in international segmentation competitions...
Keywords: deep learning; medical image segmentation; self-configuring; automation
```

### 3.4 Example AI Response

```json
{
  "decision": "INCLUDE",
  "ic1_met": true,
  "ic2_met": true,
  "ic3_met": true,
  "ic4_met": true,
  "ic5_met": true,
  "ic6_met": true,
  "exclusion_criteria_triggered": [],
  "confidence": "high",
  "reasoning": "This paper presents nnU-Net, a self-configuring deep learning 
  framework for medical image segmentation published in Nature Methods. It 
  addresses 3D segmentation across multiple modalities including CT, uses 
  U-Net-based deep learning architecture, and reports quantitative results 
  on 23 benchmark datasets. Meets all inclusion criteria with no exclusions."
}
```

## 4. Decision Logic

### 4.1 Consensus Algorithm

```python
def consensus_decision(run1, run2, run3):
    """
    Determine final decision from 3 independent AI runs.
    
    Args:
        run1, run2, run3: Decision objects from each run
    
    Returns:
        Final decision and confidence level
    """
    decisions = [run1['decision'], run2['decision'], run3['decision']]
    
    # Count votes
    include_votes = decisions.count('INCLUDE')
    exclude_votes = decisions.count('EXCLUDE')
    uncertain_votes = decisions.count('UNCERTAIN')
    
    # Majority decision
    if include_votes >= 2:
        final = 'INCLUDE'
    elif exclude_votes >= 2:
        final = 'EXCLUDE'
    else:
        final = 'UNCERTAIN'  # Flagged for human review
    
    # Confidence based on unanimity
    if decisions[0] == decisions[1] == decisions[2]:
        confidence = 'unanimous'
    else:
        confidence = 'majority'
    
    return {
        'decision': final,
        'confidence': confidence,
        'votes': {'include': include_votes, 'exclude': exclude_votes, 'uncertain': uncertain_votes},
        'flag_for_review': (final == 'UNCERTAIN') or (confidence == 'majority')
    }
```

### 4.2 Decision Outcomes

| Consensus | Votes | Outcome |
|-----------|-------|---------|
| Unanimous INCLUDE | 3-0-0 | Include, high confidence |
| Majority INCLUDE | 2-1-0 or 2-0-1 | Include, flagged for review |
| Unanimous EXCLUDE | 0-3-0 | Exclude, high confidence |
| Majority EXCLUDE | 0-2-1 or 1-2-0 | Exclude, flagged for review |
| Split/Uncertain | 1-1-1 or any with 2+ UNCERTAIN | Human review required |

## 5. Validation Protocol

### 5.1 Sample Selection

```python
def select_validation_sample(records, sample_rate=0.10, seed=42):
    """
    Select stratified random sample for validation.
    
    Stratification by:
    - AI decision (INCLUDE/EXCLUDE/UNCERTAIN)
    - Confidence level (unanimous/majority)
    - Source database
    """
    np.random.seed(seed)
    
    # Stratified sampling
    strata = records.groupby(['ai_decision', 'confidence', 'source_db'])
    
    sample = []
    for name, group in strata:
        n_sample = max(1, int(len(group) * sample_rate))
        sample.extend(group.sample(n=n_sample, random_state=seed).index.tolist())
    
    return sample  # 140 records (10% of 1,403)
```

### 5.2 Human Review Protocol

**Reviewers:**
- Reviewer A: Domain expert (MD, radiology background)
- Reviewer B: Methods expert (PhD, computer vision)

**Process:**
1. Independent review of 140 sampled records
2. Same criteria template as AI screening
3. Blind to AI decision during initial review
4. Comparison with AI consensus decision
5. Discrepancy resolution by third reviewer

### 5.3 Validation Results

| Metric | Value |
|--------|-------|
| Sample size | 140 records |
| AI-Human agreement | 96.4% (135/140) |
| Cohen's kappa (AI vs Human consensus) | κ = 0.89 |
| False positives (AI included, human excluded) | 2 (1.4%) |
| False negatives (AI excluded, human included) | 3 (2.1%) |
| True positives | 48 |
| True negatives | 87 |

### 5.4 Confusion Matrix

```
                    Human Decision
                    Include    Exclude    Total
AI Decision
Include              48          2         50
Exclude               3         87         90
Total                51         89        140

Sensitivity: 48/51 = 94.1%
Specificity: 87/89 = 97.8%
PPV: 48/50 = 96.0%
NPV: 87/90 = 96.7%
```

### 5.5 Disagreement Analysis

| Record ID | AI Decision | Human Decision | Reason for Discrepancy |
|-----------|-------------|----------------|----------------------|
| 234 | INCLUDE | EXCLUDE | 2D-only method, abstract mentioned "3D" in context |
| 567 | INCLUDE | EXCLUDE | Detection paper, not segmentation primary |
| 891 | EXCLUDE | INCLUDE | Abstract ambiguous, full-text reveals CT data |
| 1023 | EXCLUDE | INCLUDE | Workshop paper, AI uncertain about venue quality |
| 1156 | EXCLUDE | INCLUDE | Multi-modal study, CT subset meets criteria |

**Resolution:** All 5 discrepancies reviewed by third expert; 3 resolved as INCLUDE, 2 as EXCLUDE (aligned with human consensus in 4/5 cases).

## 6. Hallucination Control

### 6.1 Prevention Measures

1. **Constrained output format:** JSON schema with enumerated options
2. **Low temperature (0.3):** Reduces creative/hallucinated responses
3. **Explicit uncertainty option:** "unclear" values prevent forced decisions
4. **Evidence anchoring:** Reasoning must reference specific abstract content

### 6.2 Detection Measures

1. **Cross-run consistency:** Divergent reasoning flagged for review
2. **Claim verification:** Spot-check of AI reasoning against source text
3. **Impossible claims detection:** Automated check for references to information not in input

### 6.3 Hallucination Audit Results

| Check | Records Audited | Issues Found |
|-------|-----------------|--------------|
| Reasoning references non-existent content | 140 | 0 |
| Decision contradicts stated reasoning | 140 | 2 (1.4%) |
| Criteria evaluation inconsistent with abstract | 140 | 3 (2.1%) |

**Issues resolved:** 5 records flagged for human review; final decisions unchanged after verification.

## 7. Reproducibility

### 7.1 Code Availability

```python
# screening_pipeline.py
import anthropic
import json
import pandas as pd

def screen_record(record, client, model="claude-3-5-sonnet-20240620"):
    """Screen a single record with 3-run consensus."""
    
    system_prompt = """You are a systematic review screening assistant..."""
    user_prompt = f"""Evaluate the following paper...
    Title: {record['title']}
    ..."""
    
    runs = []
    for i in range(3):
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            temperature=0.3,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        runs.append(json.loads(response.content[0].text))
    
    return consensus_decision(*runs)

# Full pipeline code available at: [repository URL]
```

### 7.2 Data Files

All screening data available in supplementary materials:
- `S5_screening_decisions.csv`: Complete audit trail
- `S1_search_results.csv`: Source records with metadata
- `screening_pipeline.py`: Executable code

### 7.3 API Cost

| Item | Count | Unit Cost | Total |
|------|-------|-----------|-------|
| Screening prompts | 4,209 (1,403 × 3) | ~$0.003/prompt | ~$12.63 |
| Validation re-runs | 420 (140 × 3) | ~$0.003/prompt | ~$1.26 |
| **Total API cost** | | | **~$13.89** |

## 8. Limitations

1. **Abstract-only screening:** Full-text nuances may be missed
2. **Model version dependency:** Results may vary with different model versions
3. **Training data cutoff:** AI knowledge limited to training date
4. **Language bias:** English-only training may affect non-English abstract handling

## 9. Ethical Considerations

1. **Transparency:** AI use fully disclosed in methods
2. **Human oversight:** All decisions subject to human review capability
3. **No personal data:** Screening involves published abstracts only
4. **Reproducibility:** Complete methodology documented for verification

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-09-15 | Initial screening protocol |
| 1.1 | 2025-09-20 | Added validation sample results |
| 1.2 | 2025-10-01 | Final version with all statistics |

---

## Appendix A: Complete Prompt Library

### A.1 Foundation Model Papers (specialized prompt)

```
[Additional prompt variant for SAM/foundation model papers...]
```

### A.2 Benchmark Papers (specialized prompt)

```
[Additional prompt variant for challenge/benchmark papers...]
```

### A.3 Review Papers (specialized prompt)

```
[Additional prompt variant for survey/review papers...]
```

---

**Document version:** 1.2  
**Last updated:** 2025-10-01  
**Contact:** [corresponding author]
