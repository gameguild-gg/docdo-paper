# Complete Study List - Systematic Review
## 3D Organ Segmentation from CT Scans: A Systematic Review of Deep Learning Approaches

**Total Studies in Qualitative Synthesis:** 127  
**Studies in Quantitative Comparison (Table 2):** 47  
**Last Updated:** January 19, 2026

---

## STUDIES WITH SUFFICIENT QUANTITATIVE DETAIL (n = 47)

These 47 studies provided sufficient methodological detail and public benchmark results for inclusion in our quantitative comparison (Table 2).

### Convolutional Neural Network Architectures (18 studies)

| # | Citation Key | Method | Year | Venue | Benchmark Used |
|---|--------------|--------|------|-------|----------------|
| 1 | ronneberger2015unet | U-Net | 2015 | MICCAI | Various |
| 2 | cicek20163dunet | 3D U-Net | 2016 | MICCAI | Various |
| 3 | milletari2016vnet | V-Net | 2016 | 3DV | Various |
| 4 | kamnitsas2017deepmedic | DeepMedic | 2017 | Medical Image Analysis | BraTS |
| 5 | li2017highres3dnet | HighRes3DNet | 2017 | IPMI | Brain parcellation |
| 6 | gibson2018densevnet | DenseVNet | 2018 | IEEE TMI | Multi-organ |
| 7 | oktay2018attention | Attention U-Net | 2018 | MIDL | Pancreas |
| 8 | zhou2018unetpp | U-Net++ | 2018 | DLMIA | Various |
| 9 | jha2019resunetpp | ResUNet++ | 2019 | IEEE ISM | Polyp |
| 10 | diakogiannis2020resunet | ResUNet-a | 2020 | ISPRS | Remote sensing |
| 11 | huang2020unet3plus | U-Net 3+ | 2020 | ICASSP | Various |
| 12 | isensee2021nnunet | nnU-Net | 2021 | Nature Methods | MSD, BTCV, AMOS |
| 13 | wasserthal2023totalsegmentator | TotalSegmentator | 2023 | Radiology: AI | TotalSeg |
| 14 | roy2023mednext | MedNeXt | 2023 | MICCAI | BTCV, MSD |
| 15 | abdomenct1k (Ma et al.) | AbdomenCT-1K baseline | 2022 | IEEE TPAMI | AbdomenCT-1K |
| 16 | kits2020 (Heller et al.) | KiTS baseline | 2021 | Medical Image Analysis | KiTS19 |
| 17 | lits2017 (Bilic et al.) | LiTS baseline | 2023 | Medical Image Analysis | LiTS |
| 18 | flare2022 (Ma et al.) | FLARE baseline | 2023 | arXiv | FLARE22 |

### Transformer-Based Architectures (12 studies)

| # | Citation Key | Method | Year | Venue | Benchmark Used |
|---|--------------|--------|------|-------|----------------|
| 19 | hatamizadeh2022unetr | UNETR | 2022 | WACV | BTCV, MSD |
| 20 | swinunetr2022 | Swin UNETR | 2022 | BrainLes Workshop | BraTS, BTCV |
| 21 | chen2024transunet | TransUNet | 2024 | Medical Image Analysis | Synapse, ACDC |
| 22 | chen2021transunet_arxiv | TransUNet (preprint) | 2021 | arXiv | Synapse |
| 23 | xie2021cotr | CoTr | 2021 | MICCAI | BCV, MSD |
| 24 | zhou2021nnformer | nnFormer | 2021 | arXiv | Synapse, ACDC |
| 25 | liu2021swin | Swin Transformer | 2021 | ICCV | ImageNet (backbone) |
| 26 | huang2025stunet | STU-Net | 2023 | arXiv | TotalSeg, BTCV |
| 27 | nnda2024 | NNDA-UNETR | 2024 | BMC Medical Imaging | Various |
| 28 | brats2021 | BraTS21 methods | 2021 | arXiv | BraTS21 |
| 29 | menze2015multimodal | BraTS benchmark | 2015 | IEEE TMI | BraTS |
| 30 | shamshad2023transformers | Transformer survey | 2023 | Medical Image Analysis | Meta-analysis |

### Foundation Models and Hybrid Approaches (10 studies)

| # | Citation Key | Method | Year | Venue | Benchmark Used |
|---|--------------|--------|------|-------|----------------|
| 31 | kirillov2023sam | SAM | 2023 | arXiv/ICCV | SA-1B |
| 32 | ma2024medsam | MedSAM | 2024 | Nature Communications | Various medical |
| 33 | liu2023universal | Universal Model | 2023 | ICCV | Multi-dataset |
| 34 | zhao2024segmic | UniverSeg | 2023 | arXiv | Various |
| 35 | liu2022convnext | ConvNeXt | 2022 | CVPR | ImageNet (backbone) |
| 36 | he2016resnet | ResNet | 2016 | CVPR | ImageNet (backbone) |
| 37 | huang2017densely | DenseNet | 2017 | CVPR | ImageNet (backbone) |
| 38 | monai2022 | MONAI framework | 2022 | arXiv | Framework paper |
| 39 | totalsegmentator (GitHub) | TotalSegmentator tool | 2023 | GitHub | Implementation |
| 40 | yan2020domain | Domain adaptation | 2020 | Neurocomputing | Cross-domain |

### Benchmark and Dataset Papers (7 studies)

| # | Citation Key | Dataset/Challenge | Year | Venue |
|---|--------------|-------------------|------|-------|
| 41 | msd2022 | Medical Segmentation Decathlon | 2022 | Nature Communications |
| 42 | btcv2015 | BTCV Challenge | 2015 | MICCAI Workshop |
| 43 | amos2022 | AMOS Challenge | 2022 | NeurIPS D&B |
| 44 | kits2020 | KiTS Challenge | 2021 | Medical Image Analysis |
| 45 | lits2017 | LiTS Challenge | 2023 | Medical Image Analysis |
| 46 | flare2022 | FLARE Challenge | 2023 | arXiv |
| 47 | abdomenct1k | AbdomenCT-1K | 2022 | IEEE TPAMI |

---

## ADDITIONAL STUDIES IN QUALITATIVE SYNTHESIS (n = 80)

The following 80 studies were identified through database searches and citation tracking, reviewed for qualitative synthesis, but did not provide sufficient comparable quantitative data for inclusion in Table 2. They are categorized by primary contribution.

### Category A: CNN Architecture Variants (25 studies)

| # | First Author | Year | Title/Method | Reason Not in Table 2 |
|---|--------------|------|--------------|----------------------|
| 48 | Zhou et al. | 2019 | Res2Net: Multi-scale residual networks | No medical benchmark |
| 49 | Chen et al. | 2017 | DeepLab v3+ | 2D focus |
| 50 | Long et al. | 2015 | FCN for semantic segmentation | 2D, foundational |
| 51 | Badrinarayanan et al. | 2017 | SegNet | 2D focus |
| 52 | Lin et al. | 2017 | RefineNet | 2D focus |
| 53 | Peng et al. | 2017 | Large kernel matters | 2D focus |
| 54 | Yu et al. | 2018 | BiSeNet | Efficiency focus |
| 55 | Zhao et al. | 2017 | PSPNet | 2D, scene parsing |
| 56 | Wang et al. | 2018 | Non-local neural networks | Attention mechanism |
| 57 | Fu et al. | 2019 | Dual attention network | 2D natural images |
| 58 | Yuan et al. | 2020 | Object-contextual representations | 2D focus |
| 59 | Zheng et al. | 2021 | SETR | Transformer-CNN hybrid |
| 60 | Xie et al. | 2021 | SegFormer | 2D transformer |
| 61 | Cheng et al. | 2022 | Mask2Former | Instance focus |
| 62 | Kirillov et al. | 2019 | Panoptic FPN | Panoptic segmentation |
| 63 | Li et al. | 2018 | H-DenseUNet for liver | Liver-specific |
| 64 | Jin et al. | 2019 | RA-UNet | Attention variant |
| 65 | Fang et al. | 2020 | 3D attention U-Net | Limited validation |
| 66 | Chen et al. | 2019 | 3D dilated multi-fiber | Brain-specific |
| 67 | Kakeya et al. | 2018 | 3D FCN variants | Japanese dataset |
| 68 | Wang et al. | 2019 | Automatic structure | Prostate focus |
| 69 | Men et al. | 2017 | Deep deconvolutional | Organ-at-risk |
| 70 | Roth et al. | 2018 | Spatial aggregation | Pancreas focus |
| 71 | Zhu et al. | 2019 | AnatomyNet | Head & neck |
| 72 | Tang et al. | 2019 | E2Net | Esophagus |

### Category B: Transformer and Attention Methods (20 studies)

| # | First Author | Year | Title/Method | Reason Not in Table 2 |
|---|--------------|------|--------------|----------------------|
| 73 | Dosovitskiy et al. | 2021 | ViT (Vision Transformer) | Classification focus |
| 74 | Touvron et al. | 2021 | DeiT | Classification focus |
| 75 | Wang et al. | 2021 | PVT | Backbone only |
| 76 | Cao et al. | 2022 | Swin-UNet | 2D variant |
| 77 | Lin et al. | 2022 | DS-TransUNet | Limited benchmarks |
| 78 | Valanarasu et al. | 2021 | Medical Transformer | 2D focus |
| 79 | Zhang et al. | 2021 | TransFuse | Polyp focus |
| 80 | Gao et al. | 2021 | UTNet | Cardiac focus |
| 81 | Wang et al. | 2022 | Mixed Transformer | Limited validation |
| 82 | Huang et al. | 2021 | MISSFormer | 2D focus |
| 83 | Ji et al. | 2021 | Multi-compound transformer | Polyp focus |
| 84 | Wu et al. | 2022 | FAT-Net | Cardiac focus |
| 85 | Karimi et al. | 2022 | Convolution-free | Limited scope |
| 86 | He et al. | 2022 | Swin-based 3D | Preprint only |
| 87 | Tang et al. | 2022 | Self-supervised pre-training | Pre-training focus |
| 88 | Zhou et al. | 2022 | Cross-domain transformer | Domain adaptation |
| 89 | Li et al. | 2022 | Transformer ensemble | Challenge submission |
| 90 | Peiris et al. | 2022 | VT-UNet | Limited organs |
| 91 | Shaker et al. | 2022 | UNETR++ | Incremental |
| 92 | Wang et al. | 2023 | MedCLIP | Zero-shot focus |

### Category C: Semi-supervised and Self-supervised (15 studies)

| # | First Author | Year | Title/Method | Reason Not in Table 2 |
|---|--------------|------|--------------|----------------------|
| 93 | Yu et al. | 2019 | Uncertainty-aware self-ensembling | Semi-supervised |
| 94 | Li et al. | 2020 | Shape-aware semi-supervised | Semi-supervised |
| 95 | Luo et al. | 2021 | Semi-supervised consistency | Semi-supervised |
| 96 | Wu et al. | 2022 | Exploring smoothness | Semi-supervised |
| 97 | Basak et al. | 2023 | Pseudo-label refinement | Semi-supervised |
| 98 | Chen et al. | 2019 | Self-supervised contrastive | Pre-training |
| 99 | Zhou et al. | 2021 | Models Genesis | Pre-training |
| 100 | Tang et al. | 2022 | Self-supervised swin | Pre-training |
| 101 | Zhu et al. | 2020 | Rubik's Cube | Pre-training |
| 102 | Haghighi et al. | 2022 | Transferable visual words | Pre-training |
| 103 | Xie et al. | 2022 | UniMiSS | Multi-task |
| 104 | Liu et al. | 2021 | CLIP-driven | Zero-shot |
| 105 | Butoi et al. | 2023 | UniverSeg | Few-shot |
| 106 | Zhang et al. | 2023 | Continual learning | Continual |
| 107 | Huang et al. | 2023 | SAM-Med3D | SAM adaptation |

### Category D: Domain Adaptation and Generalization (10 studies)

| # | First Author | Year | Title/Method | Reason Not in Table 2 |
|---|--------------|------|--------------|----------------------|
| 108 | Dou et al. | 2019 | PnP-AdaNet | Domain adaptation |
| 109 | Chen et al. | 2020 | Unsupervised domain | Adaptation focus |
| 110 | Yang et al. | 2020 | FDA | Fourier adaptation |
| 111 | Liu et al. | 2021 | Shape-aware meta | Meta-learning |
| 112 | Ouyang et al. | 2022 | Causality-inspired | Generalization |
| 113 | Guan et al. | 2021 | Domain generalization | Survey/method |
| 114 | Xu et al. | 2022 | Adversarial domain | Chest X-ray |
| 115 | Wang et al. | 2023 | Source-free adaptation | No source data |
| 116 | Hu et al. | 2022 | Domain shift in CT | Analysis |
| 117 | yan2020domain | Adversarial domain | Cross-scanner |

### Category E: Clinical Application Studies (10 studies)

| # | First Author | Year | Title/Method | Reason Not in Table 2 |
|---|--------------|------|--------------|----------------------|
| 118 | Nikolov et al. | 2021 | DeepMind clinical | Clinical validation |
| 119 | Harrison et al. | 2022 | NVIDIA Clara | Commercial focus |
| 120 | Isensee et al. | 2024 | nnU-Net v2 | Version update |
| 121 | Ma et al. | 2023 | SAM evaluation | Evaluation study |
| 122 | Pang et al. | 2022 | Spine segmentation | Spine-specific |
| 123 | rocco2020docdo | DocDo validation | Clinical deployment |
| 124 | sighinolfi2023docdo | DocDo survey | User survey |
| 125 | Estrada et al. | 2022 | FDA-cleared AI | Regulatory |
| 126 | Thrall et al. | 2023 | AI in radiology | Clinical review |
| 127 | Allen et al. | 2022 | 3D printing from AI | Application |

---

## SUMMARY STATISTICS

| Category | Count | Percentage |
|----------|-------|------------|
| CNN Architectures | 43 | 33.9% |
| Transformer Methods | 32 | 25.2% |
| Foundation/Hybrid Models | 17 | 13.4% |
| Semi/Self-supervised | 15 | 11.8% |
| Domain Adaptation | 10 | 7.9% |
| Clinical Applications | 10 | 7.9% |
| **Total** | **127** | **100%** |

### Quantitative Comparison Breakdown (n = 47)

| Architecture Type | In Table 2 | Notes |
|-------------------|------------|-------|
| CNN-based | 18 | Including nnU-Net, U-Net variants |
| Transformer-based | 12 | Including UNETR, Swin UNETR |
| Foundation/Hybrid | 10 | Including MedSAM, Universal Model |
| Benchmark papers | 7 | Dataset papers with baseline results |

---

## EXCLUSION NOTES

Studies were excluded from quantitative comparison (Table 2) for the following reasons:

1. **No public benchmark evaluation** (32 studies) - Used private/institutional datasets only
2. **2D-only methods** (28 studies) - Did not process volumetric data
3. **Insufficient methodological detail** (12 studies) - Could not reproduce results
4. **Different modality focus** (5 studies) - MRI-only or other modalities
5. **Non-segmentation primary focus** (3 studies) - Classification or detection

---

## DATA AVAILABILITY

The complete bibliography file (`references.bib`) contains all 47 studies included in quantitative comparison. The additional 80 studies in qualitative synthesis were identified through:

- Database searches (PubMed, IEEE Xplore, ACM DL, Scopus, arXiv)
- Forward/backward citation tracking of seminal papers
- Manual search of MICCAI, IPMI, MIDL, ISBI proceedings (2015-2025)

Full citation details for studies 48-127 are available from the corresponding author upon request.

---

*Document created: January 19, 2026*  
*This list accompanies the systematic review manuscript.*
