# Coding Scheme — DocDo Screening

Defines the inclusion/exclusion criteria used during AI-assisted abstract screening (S2) and full-text review (S3).

---

## Inclusion Criteria (ALL must be met)

| Code | Criterion | Positive Indicators | Negative Indicators |
|------|-----------|---------------------|---------------------|
| **IC1** | Deep Learning Method | CNN, Transformer, U-Net, encoder-decoder, attention mechanisms | SVM, Random Forest, rule-based, classical image processing |
| **IC2** | 3D Volumetric Segmentation | 3D convolutions, 2.5D, slice-based + 3D post-processing | Pure 2D single-slice without volumetric aggregation |
| **IC3** | CT Imaging Modality | CT with/without contrast, multi-modal including CT | MRI-only, ultrasound-only, X-ray-only, PET-only |
| **IC4** | Anatomical Organ Segmentation | Liver, kidney, spleen, pancreas, lung, heart, stomach, gallbladder, bladder, prostate, colon, esophagus, adrenal glands; organs-at-risk for radiotherapy | Tumors/lesions only, vessels only, bones only, muscles only, airways only |
| **IC5** | Original Research | Novel method, architecture, training strategy, benchmark comparison with insights | Pure review/survey, dataset-only, editorials |

## Exclusion Triggers (ANY one excludes)

| Code | Trigger |
|------|---------|
| **EC1** | Detection/classification only (no spatial segmentation) |
| **EC2** | Non-CT modalities exclusively |
| **EC3** | Non-organ targets exclusively (tumors, vessels, bones, muscles, COVID lesions) |
| **EC4** | 2D-only without volumetric context |
| **EC5** | Non-deep learning methods |
| **EC6** | Review papers without novel methodology |

---

## Decision Rule

- **INCLUDE**: ALL IC1–IC5 clearly met AND no EC triggers.
- **EXCLUDE**: ANY doubt or missing information → conservative exclusion.
- No "UNCERTAIN" label allowed — forces binary decision.

## Output Schema

Each screening result is a JSON object:

```json
{
  "decision": "INCLUDE | EXCLUDE",
  "confidence": 70-95,
  "rationale": "One sentence justification",
  "criteria_met": ["IC1", "IC2", ...],
  "criteria_failed": ["EC3", ...]
}
```

## Data Extraction (S3)

Full-text included papers are coded for:

- **Architecture**: Model family (U-Net variant, Transformer, hybrid, etc.)
- **Organ targets**: Which organs are segmented
- **Dataset**: Training/test datasets used
- **Metrics**: Dice score, HD95, IoU, etc.
- **3D approach**: True 3D, 2.5D, slice-based + post-processing
- **Code availability**: Whether source code is publicly released
