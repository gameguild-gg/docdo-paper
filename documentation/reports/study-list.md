<!-- v1-history -->

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

<!-- /v1-history -->

---

## v2.1 Section (2026-09-30) — included studies (236)

Regenerated from `pipeline_outputs/s3v2_extracted_data_full.csv` (INCLUDE rows).
The v1 list below is preserved as history. Total: **236 studies** (224 method, 9 framework/software, 3 benchmark).

### Method papers (n=224)

| # | paper_id | Year | Title | Venue |
|---|---------|------|-------|-------|
| 1 | `10.1007_978-3-319-46723-8_48` | 2016 | Automatic Liver and Lesion Segmentation in CT Using Cascaded Fully Convolutional Neural Ne | MICCAI 2016 (Springer LNCS) |
| 2 | `10.1002_mp.12480` | 2017 | Deep learning of the sectional appearances of 3D CT images for anatomical structure segmen | Medical Physics |
| 3 | `10.1109_isbi.2017.7950685` | 2017 | Segmentation of Organs at Risk in Thoracic CT Images Using a SharpMask Architecture and Co | IEEE International Symposium on Biomedic |
| 4 | `10.1117_12.2254201` | 2017 | Automated segmentation of 3D anatomical structures on CT images by using a deep convolutio | SPIE Medical Imaging 2017: Image Process |
| 5 | `10.1117_12.2255528` | 2017 | Segmentation of inner and outer bladder wall using deep-learning convolutional neural netw | SPIE Medical Imaging 2017: Computer-Aide |
| 6 | `10.17918_d8p65k` | 2017 | Image analysis methods for identification and segmentation of biological structures using  | Drexel University (PhD Thesis) |
| 7 | `10.48550_arxiv.1702.00045` | 2017 | Spatial Aggregation of Holistically-Nested Convolutional Neural Networks for Automated Pan | arXiv preprint |
| 8 | `10.48550_arxiv.1711.08580` | 2017 | 3D Anisotropic Hybrid Network: Transferring Convolutional Features from 2D Images to 3D An | arXiv preprint |
| 9 | `10.1002_mp.13326` | 2018 | Deep-Learning Convolutional Neural Network: Inner and Outer Bladder Wall Segmentation in C | Medical Physics |
| 10 | `10.1007_s11548-018-1797-4` | 2018 | TernaryNet: Faster Deep Model Inference without GPUs for Medical 3D Segmentation using Spa | MICCAI 2018 (Springer LNCS; arXiv 1801.0 |
| 11 | `10.1016_j.compmedimag.2018.03.001` | 2018 | An application of cascaded 3D fully convolutional networks for medical image segmentation | Computerized Medical Imaging and Graphic |
| 12 | `10.1109_bibm.2018.8621257` | 2018 | Automatic Liver Segmentation Using Multi-plane Integrated Fully Convolutional Neural Netwo | IEEE International Conference on Bioinfo |
| 13 | `10.1109_crc.2018.00010` | 2018 | Medical Images Sequence Normalization and Augmentation: Improve Liver Tumor Segmentation F | International Conference on Control, Rob |
| 14 | `10.1109_icpr.2018.8545143` | 2018 | Automatic Segmentation of Kidney and Renal Tumor in CT Images Based on 3D Fully Convolutio | 2018 24th International Conference on Pa |
| 15 | `10.1109_icpr.2018.8546017` | 2018 | SequentialSegNet: Combination with Sequential Feature for Multi-organ Segmentation | 2018 24th International Conference on Pa |
| 16 | `10.1109_ijcnn.2018.8489677` | 2018 | End-to-End Supervised Lung Lobe Segmentation | 2018 International Joint Conference on N |
| 17 | `10.1109_tmi.2018.2806309` | 2018 | Automatic Multi-organ Segmentation on Abdominal CT with Dense V-networks | IEEE Transactions on Medical Imaging |
| 18 | `10.1117_12.2293499` | 2018 | Towards dense volumetric pancreas segmentation in CT using 3D fully convolutional networks | SPIE Medical Imaging (arXiv:1711.06439v2 |
| 19 | `10.1145_3285996.3286014` | 2018 | Automatic Liver Segmentation in CT Volumes with Improved 3D U-net | ISICDM 2018 (ACM) |
| 20 | `10.1145_3290420.3290461` | 2018 | 3D Anisotropic Convolutional Neural Network with Step Transfer Learning for Liver Segmenta | ICCIP 2018 (ACM) |
| 21 | `10.48550_arxiv.1805.12526` | 2018 | Fully Automated Organ Segmentation in Male Pelvic CT Images | arXiv preprint |
| 22 | `10.48550_arxiv.1807.02437` | 2018 | Deep Sequential Segmentation of Organs in Volumetric Medical Scans | arXiv preprint |
| 23 | `10.48550_arxiv.1809.10245` | 2018 | CYLINDRICAL TRANSFORM: 3D SEMANTIC SEGMENTATION OF KIDNEYS WITH LIMITED ANNOTATED IMAGES | IEEE Global Conference on Signal and Inf |
| 24 | `10.48550_arxiv.1810.04017` | 2018 | Comparison of U-net-based Convolutional Neural Networks for Liver Segmentation in CT | arXiv preprint |
| 25 | `10.1002_acm2.12784` | 2019 | Liver tumor segmentation based on 3D convolutional neural network with dual scale | Journal of Applied Clinical Medical Phys |
| 26 | `10.1002_mp.13438` | 2019 | U-Net-based Deep-Learning Bladder Segmentation in CT Urography | Medical Physics |
| 27 | `10.1002_mp.13466` | 2019 | Deep convolutional neural network for segmentation of thoracic organs-at-risk using croppe | Medical Physics |
| 28 | `10.1002_mp.13735` | 2019 | Automatic Liver Segmentation by Integrating Fully Convolutional Networks into Active Conto | Medical Physics |
| 29 | `10.1007_978-3-030-00889-5_32` | 2019 | Automatic Segmentation of Pulmonary Lobes Using a Progressive Dense V-Network | arXiv:1902.06362 (cs.CV); Springer DOI 1 |
| 30 | `10.1016_j.media.2019.02.006` | 2019 | OBELISK-Net: Fewer Layers to Solve 3D Multi-Organ Segmentation with Sparse Deformable Conv | Medical Image Analysis |
| 31 | `10.1038_s41598-019-40710-7` | 2019 | Measurement of Glomerular Filtration Rate using Quantitative SPECT/CT and Deep-learning-ba | Scientific Reports |
| 32 | `10.1109_access.2019.2899608` | 2019 | AHCNet: An Application of Attention Mechanism and Hybrid Connection for Liver Tumor Segmen | IEEE Access |
| 33 | `10.1109_access.2019.2941154` | 2019 | An Augmentation Strategy for Medical Image Processing Based on Statistical Shape Model and | IEEE Access |
| 34 | `10.1109_cbmi.2019.8877400` | 2019 | Automatic liver segmentation on CT images combining region-based techniques and convolutio | IEEE International Conference on Content |
| 35 | `10.1109_isbi.2019.8759309` | 2019 | Learning to Segment the Lung Volume from CT Scans Based on Semi-Automatic Ground-Truth | IEEE 16th International Symposium on Bio |
| 36 | `10.1109_isbi.2019.8759492` | 2019 | Automated Segmentation of Pulmonary Lobes Using Coordination-Guided Deep Neural Networks | IEEE International Symposium on Biomedic |
| 37 | `10.1109_iwssip.2019.8787253` | 2019 | Whole Heart Segmentation from CT images Using 3D U-Net architecture | IEEE International Conference on Systems |
| 38 | `10.1109_kst.2019.8687816` | 2019 | U-Net and Mean-Shift Histogram for Efficient Liver Segmentation from CT Images | IEEE International Conference on Knowled |
| 39 | `10.1109_qrs-c.2019.00075` | 2019 | Reliable automatic organ segmentation from CT images using deep CNN | IEEE 19th International Conference on So |
| 40 | `10.1145_3364836.3364842` | 2019 | Convolutional Neural Networks Based Level Set Framework for Pancreas Segmentation from CT  | ISICDM 2019 (ACM) |
| 41 | `10.1145_3364836.3364885` | 2019 | Deep Interactive Segmentation of Uncertain Regions with Shadowed Sets | ISICDM 2019 (ACM International Symposium |
| 42 | `10.24926_548719.002` | 2019 | Cascaded Semantic Segmentation for Kidney and Tumor | Not specified |
| 43 | `10.24926_548719.006` | 2019 | Coarse to Fine Framework for Kidney Tumor Segmentation | Unknown (likely MICCAI KiTS19 Challenge) |
| 44 | `10.24926_548719.012` | 2019 | Segmentation of Kidney and Renal Tumor in CT Scans Using Convolutional Networks | KiTS19 Challenge (MICCAI 2019) |
| 45 | `10.24926_548719.014` | 2019 | KiTS challenge: VNet with attention gates and deep supervision | KiTS Challenge (MICCAI) |
| 46 | `10.24926_548719.016` | 2019 | 3D Unet-based Kidney and Kidney Tumor Segmentation with Attentive Feature Learning | MICCAI 2019 (KiTS Challenge) |
| 47 | `10.24926_548719.018` | 2019 | Automatic Kidney and Tumor Segmentation with Hybrid Hierarchical Networks | MICCAI 2019 Kidney Tumor Segmentation Ch |
| 48 | `10.24926_548719.034` | 2019 | Renal Tumor Segmentation in CT using Cascade U-Net with 2.5D approach | Unknown (conference paper) |
| 49 | `10.24926_548719.049` | 2019 | Using Two-stage Network to Segment Kidneys and Kidney Tumors | Unknown (likely conference/workshop) |
| 50 | `10.24926_548719.055` | 2019 | A Multi-scale Attention Network for Kidney Tumor Segmentation on CT Scans | Unknown (likely MICCAI or similar) |
| 51 | `10.24926_548719.059` | 2019 | Kidney and Kidney Tumor Segmentation Using Two-stage Convolutional Neural Network | Not specified |
| 52 | `10.24926_548719.082` | 2019 | Kidney and Kidney Tumor Segmentation using a Logical Ensemble of U-nets with Volumetric Va | MICCAI 2019 Kidney Tumor Segmentation Ch |
| 53 | `10.48550_arxiv.1809.00960` | 2019 | Organ at Risk Segmentation in Head and Neck CT Images Using a Two-Stage Segmentation Frame | IEEE Access |
| 54 | `10.48550_arxiv.1907.05273` | 2019 | Accurate Congenital Heart Disease Model Generation for 3D Printing | arXiv |
| 55 | `10.48550_arxiv.1908.00360` | 2019 | A Method of Rapid Quantification of Patient-Specific Organ Dose for CT Using Coupled Deep- | arXiv |
| 56 | `10.48550_arxiv.1909.06684` | 2019 | 3D Kidneys and Kidney Tumor Semantic Segmentation using Boundary-Aware Networks | arXiv preprint |
| 57 | `10.1002_acm2.13024` | 2020 | Automatic segmentation and applicator reconstruction for CT-based brachytherapy of cervica | Journal of Applied Clinical Medical Phys |
| 58 | `10.1002_mp.13950` | 2020 | Automatic multi-organ segmentation in dual-energy CT (DECT) with dedicated 3D fully convol | Medical Physics |
| 59 | `10.1002_mp.14303` | 2020 | Improving the Slice Interaction of 2.5D CNN for Automatic Pancreas Segmentation | Medical Physics |
| 60 | `10.1002_mp.14422` | 2020 | Complete Abdomen and Pelvis Segmentation using U-Net Variant Architecture | Medical Physics |
| 61 | `10.1002_mp.14451` | 2020 | Deep Learning from Dual-Energy Information for Whole-Heart Segmentation in Dual-Energy and | Medical Physics |
| 62 | `10.1007_978-3-030-68107-4_12` | 2020 | PC-U Net: Learning to Jointly Reconstruct and Segment the Cardiac Walls in 3D from CT Data | MICCAI 2020 (Springer LNCS) |
| 63 | `10.1016_j.imu.2020.100357` | 2020 | MSS U-Net: 3D segmentation of kidneys and tumors from CT images with a multi-scale supervi | Informatics in Medicine Unlocked |
| 64 | `10.1016_j.media.2020.101884` | 2020 | A Deep Learning Framework for Pancreas Segmentation with Multi-atlas Registration and 3D L | Medical Image Analysis |
| 65 | `10.1016_j.phro.2020.05.009` | 2020 | Cardio-pulmonary substructure segmentation of radiotherapy computed tomography images usin | Physics and Imaging in Radiation Oncolog |
| 66 | `10.1016_j.rpor.2020.09.005` | 2020 | Convolutional neural network-based automatic liver delineation on contrast-enhanced and no | Reports of Practical Oncology and Radiot |
| 67 | `10.1038_s41598-019-57242-9` | 2020 | Active learning for accuracy enhancement of semantic segmentation with CNN-corrected label | Scientific Reports |
| 68 | `10.1038_s41598-020-63285-0` | 2020 | Abdominal multi-organ autosegmentation using 3D-patch-based deep convolutional neural netw | Scientific Reports |
| 69 | `10.1038_s41598-020-67544-y` | 2020 | Domain-specific cues improve robustness of deep learning-based segmentation of CT volumes | Scientific Reports |
| 70 | `10.1049_iet-ipr.2019.0399` | 2020 | DRAN: Deep recurrent adversarial network for automated pancreas segmentation | IET Image Processing |
| 71 | `10.1088_1361-6560_ab6f99` | 2020 | Interactive 3D U-net for the segmentation of the pancreas in computed tomography scans | Physics in Medicine & Biology |
| 72 | `10.1088_1742-6596_1631_1_012049` | 2020 | 3D Densely Connected Convolution Neural Networks for Pulmonary Parenchyma Segmentation fro | Journal of Physics: Conference Series |
| 73 | `10.1109_access.2019.2961125` | 2020 | Automatic Pancreas Segmentation via Coarse Location and Ensemble Learning | IEEE Access |
| 74 | `10.1109_access.2019.2961410` | 2020 | Improving Whole-Heart CT Image Segmentation by Attention Mechanism | IEEE Access |
| 75 | `10.1109_access.2020.2985671` | 2020 | Cascade U-ResNets for Simultaneous Liver and Lesion Segmentation | IEEE Access |
| 76 | `10.1109_access.2020.2988647` | 2020 | Deep Learning Initialized and Gradient Enhanced Level-set Based Segmentation for Liver Tum | IEEE Access |
| 77 | `10.1109_access.2020.3019518` | 2020 | Eso-Net: A Novel 2.5D Segmentation Network With the Multi-Structure Response Filter for th | IEEE Access |
| 78 | `10.1109_access.2020.3024277` | 2020 | Automatic Segmentation Using a Hybrid Dense Network Integrated With an 3D-Atrous Spatial P | IEEE Access |
| 79 | `10.1109_access.2020.3028038` | 2020 | Prior Attention Enhanced Convolutional Neural Network Based Automatic Segmentation of Orga | IEEE Access |
| 80 | `10.1109_embc44109.2020.9175907` | 2020 | Automatic Pulmonary Vein and Left Atrium Segmentation for TAPVC Preoperative Evaluation Us | IEEE Engineering in Medicine and Biology |
| 81 | `10.1109_icieam48468.2020.9111950` | 2020 | Hybrid 3D-ResNet Deep Learning Model for Automatic Segmentation of Thoracic Organs at Risk | 2020 International Conference on Industr |
| 82 | `10.1109_isbi45749.2020.9098325` | 2020 | An Efficient Hybrid Model for Kidney Tumor Segmentation in CT Images | IEEE 17th International Symposium on Bio |
| 83 | `10.1109_isbi45749.2020.9098609` | 2020 | A Triple-Stage Self-Guided Network for Kidney Tumor Segmentation | IEEE 17th International Symposium on Bio |
| 84 | `10.1109_isbi45749.2020.9098615` | 2020 | Liver Segmentation in CT with MRI Data: Zero-Shot Domain Adaptation by Contour Extraction  | IEEE 17th International Symposium on Bio |
| 85 | `10.1109_isbi45749.2020.9098701` | 2020 | Deep Learning and Unsupervised Fuzzy C-Means Based Level-Set Segmentation for Liver Tumor | IEEE 17th International Symposium on Bio |
| 86 | `10.1109_jbhi.2020.3004296` | 2020 | Structure Correction for Robust Volume Segmentation in Presence of Tumors | IEEE Journal of Biomedical and Health In |
| 87 | `10.1111_cpf.12611` | 2020 | Deep learning-based quantification of PET/CT prostate gland uptake: association with overa | Clinical Physiology and Functional Imagi |
| 88 | `10.1148_ryai.2020190102` | 2020 | Fully Automatic Volume Measurement of the Spleen at CT Using Deep Learning | Radiology: Artificial Intelligence |
| 89 | `10.21203_rs.3.rs-83236_v1` | 2020 | Compare the Segmentation Accuracy of Heart Substructure on Contrast Enhanced CT by Deep Co | Research Square (preprint) |
| 90 | `10.2478_acss-2020-0005` | 2020 | Applying 3D U-Net Architecture to the Task of Multi-Organ Segmentation in Computed Tomogra | Applied Computer Systems |
| 91 | `10.25073_2588-1086_vnucsce.241` | 2020 | Liver Segmentation on a Variety of CT Images Based on Convolutional Neural Networks Combin | VNU Journal of Science: Computer Science |
| 92 | `10.32985_ijeces.11.1.3` | 2020 | Neural Network Based Whole Heart Segmentation from 3D CT Images | International Journal of Electrical and  |
| 93 | `10.3389_fbioe.2020.605132` | 2020 | RA-UNet: A Hybrid Deep Attention-Aware Network to Extract Liver and Tumor in CT Scans | Frontiers in Bioengineering and Biotechn |
| 94 | `10.3389_fnbot.2020.00049` | 2020 | AutoPath: Image-Specific Inference for 3D Segmentation | Frontiers in Neurorobotics |
| 95 | `10.3390_app10196838` | 2020 | Point-Sampling Method Based on 3D U-Net Architecture to Reduce the Influence of False Posi | Applied Sciences (MDPI) |
| 96 | `10.48550_arxiv.2001.03111` | 2020 | Unpaired Multi-modal Segmentation via Knowledge Distillation | IEEE Transactions on Medical Imaging |
| 97 | `10.48550_arxiv.2002.06927` | 2020 | PATIENT-SPECIFIC FINETUNING OF DEEP LEARNING MODELS FOR ADAPTIVE RADIOTHERAPY IN PROSTATE  | arXiv preprint |
| 98 | `10.48550_arxiv.2006.15713` | 2020 | Generalizable Cone Beam CT Esophagus Segmentation using Physics-Based Data Augmentation | arXiv preprint |
| 99 | `10.48550_arxiv.2012.04701` | 2020 | 3D Graph Anatomy Geometry-Integrated Network for Pancreatic Mass Segmentation, Diagnosis,  | arXiv preprint |
| 100 | `10.1002_mp.14782` | 2021 | Two-stage deep learning model for fully automated pancreas segmentation on computed tomogr | Medical Physics |
| 101 | `10.1002_mp.14810` | 2021 | Automatic delineation of cardiac substructures using a region-based fully convolutional ne | Medical Physics |
| 102 | `10.1002_mp.14852` | 2021 | Interactive contouring through contextual deep learning | Medical Physics |
| 103 | `10.1016_j.cmpb.2021.106141` | 2021 | A Two-Phase Approach using Mask R-CNN and 3D U-Net for High-Accuracy Automatic Segmentatio | Computer Methods and Programs in Biomedi |
| 104 | `10.1016_j.radonc.2021.04.019` | 2021 | A deep learning-based auto-segmentation system for organs-at-risk on whole-body computed t | Radiotherapy and Oncology |
| 105 | `10.1088_1361-6560_abfce3` | 2021 | Pancreas Segmentation with Probabilistic Map Guided Bi-directional Recurrent UNet | Physics in Medicine & Biology (IOP Publi |
| 106 | `10.1088_1361-6560_ac3935` | 2021 | Efficient knowledge distillation for liver CT segmentation using growing assistant network | Physics in Medicine & Biology |
| 107 | `10.1088_1742-6596_1920_1_012060` | 2021 | Segmentation and Reconstruction of Abdominal Multi-tissues Based on Multiple Algorithms an | Journal of Physics: Conference Series |
| 108 | `10.1093_jrr_rraa094` | 2021 | A slice classification model-facilitated 3D encoder–decoder network for segmenting organs  | Journal of Radiation Research |
| 109 | `10.1109_access.2021.3055803` | 2021 | Cross-Dataset Multiple Organ Segmentation From CT Imagery Using FBP-Derived Domain Adaptat | IEEE Access |
| 110 | `10.1109_access.2021.3089704` | 2021 | R2U3D: Recurrent Residual 3D U-Net for Lung Segmentation | IEEE Access |
| 111 | `10.1109_bibm52615.2021.9669823` | 2021 | CC-DenseUNet: Densely Connected U-Net with Criss-Cross Attention for Liver and Tumor Segme | IEEE International Conference on Bioinfo |
| 112 | `10.1109_iccece51280.2021.9342350` | 2021 | 3D Segment and Pickup Framework for Pancreas Segmentation | 2021 IEEE International Conference on Co |
| 113 | `10.1109_jbhi.2021.3075752` | 2021 | Bridging the Gap between 2D and 3D Contexts in CT Volume for Liver and Tumor Segmentation | IEEE Journal of Biomedical and Health In |
| 114 | `10.1186_s12938-021-00932-1` | 2021 | A 2D–3D hybrid convolutional neural network for lung lobe auto-segmentation on standard sl | BioMedical Engineering OnLine |
| 115 | `10.1186_s13550-021-00796-5` | 2021 | Automated and robust organ segmentation for 3D-based internal dose calculation | EJNMMI Research |
| 116 | `10.1371_journal.pone.0252287` | 2021 | Multi-scale U-like network with attention mechanism for automatic pancreas segmentation | PLOS ONE |
| 117 | `10.21203_rs.3.rs-902758_v1` | 2021 | DALU-Net: Automated Liver Segmentation and Volumetry for Liver Transplantation in Abdomina | Research Square (preprint) |
| 118 | `10.2147_cmar.s330249` | 2021 | Automatic Segmentation of Clinical Target Volume and Organs-at-Risk for Breast Conservativ | Cancer Management and Research |
| 119 | `10.22215_etd_2021-15566` | 2021 | Development of an Integrated System for Automatic Tumor Detection for PET-CT Images | Carleton University (PhD Thesis) |
| 120 | `10.3389_fonc.2021.669437` | 2021 | Advanced Deep Learning Approach to Automatically Segment Malignant Tumors and Ablation Zon | Frontiers in Oncology |
| 121 | `10.3389_fphy.2021.743190` | 2021 | Deep Learning-Augmented Head and Neck Organs at Risk Segmentation From CT Volumes | Frontiers in Physics |
| 122 | `10.3390_a14050144` | 2021 | Boundary Loss-Based 2.5D Fully Convolutional Neural Networks Approach for Segmentation: A  | Algorithms (MDPI) |
| 123 | `10.3390_electronics10040431` | 2021 | Numerical Evaluation on Parametric Choices Influencing Segmentation Results in Radiology I | Electronics (MDPI) |
| 124 | `10.3390_tomography7040078` | 2021 | Evaluation of a Deep Learning Algorithm for Automated Spleen Segmentation in Patients with | Tomography (MDPI) |
| 125 | `10.48550_arxiv.2005.07462` | 2021 | MetricUNet: Synergistic Image- and Voxel-Level Learning for Precise Prostate Segmentation  | arXiv preprint |
| 126 | `10.48550_arxiv.2102.07899` | 2021 | A Deep-Learning Approach For Direct Whole-Heart Mesh Reconstruction | Medical Image Analysis |
| 127 | `10.1002_mp.15521` | 2022 | Technical note: Evaluation of a V-Net autosegmentation algorithm for pediatric CT scans: P | Medical Physics |
| 128 | `10.1007_978-3-031-16440-8_53` | 2022 | Self-supervised 3D anatomy segmentation using self-distilled masked image transformer (SMI | MICCAI 2022 (early accepted; Springer LN |
| 129 | `10.1007_s10916-022-01810-6` | 2022 | Automatic Cardiac Structure Contouring for Small Datasets with Cascaded Deep Learning Mode | Journal of Medical Systems |
| 130 | `10.1016_j.compbiomed.2021.105191` | 2022 | Deep learning-based whole-heart segmentation in 4D contrast-enhanced cardiac CT | Computers in Biology and Medicine |
| 131 | `10.1038_s41598-022-07848-3` | 2022 | Automated pancreas segmentation and volumetry using deep neural network on computed tomogr | Scientific Reports |
| 132 | `10.1038_s41598-022-09978-0` | 2022 | Deep 3D attention CLSTM U-Net based automated liver segmentation and volumetry for the liv | Scientific Reports |
| 133 | `10.1038_s41598-022-18173-0` | 2022 | Evaluation of a hybrid pipeline for automated segmentation of solid lesions based on mathe | Scientific Reports |
| 134 | `10.1038_s41598-022-20108-8` | 2022 | A pipeline for automated deep learning liver segmentation (PADLLS) from contrast enhanced  | Scientific Reports |
| 135 | `10.1038_s41598-022-21562-0` | 2022 | Deep supervision and atrous inception-based U-Net combining CRF for automatic liver segmen | Scientific Reports |
| 136 | `10.1097_as9.0000000000000155` | 2022 | nnU-Net Deep Learning Method for Segmenting Parenchyma and Determining Liver Volume From C | Annals of Surgery Open |
| 137 | `10.1109_elmar55880.2022.9899815` | 2022 | 3D U-Net based method for fast segmentation of whole heart from CT images | ELMAR 2022 (International Symposium Elec |
| 138 | `10.1109_wrcsara57040.2022.9903976` | 2022 | Two-Stage Multi-Organ Automatic Segmentation with Low GPU Memory Occupancy | 2022 WRC Symposium on Advanced Robotics  |
| 139 | `10.1186_s12880-022-00785-7` | 2022 | Heart and bladder detection and segmentation on FDG PET/CT by deep learning | BMC Medical Imaging |
| 140 | `10.1186_s13014-022-01985-9` | 2022 | Dosimetric impact of deep learning-based CT auto-segmentation on radiation therapy treatme | Radiation Oncology |
| 141 | `10.1186_s13014-022-02102-6` | 2022 | A deep image-to-image network organ segmentation algorithm for radiation treatment plannin | Radiation Oncology |
| 142 | `10.1186_s40001-022-00943-1` | 2022 | Automated quantitative assessment of pediatric blunt hepatic trauma by deep learning-based | European Journal of Medical Research |
| 143 | `10.21203_rs.3.rs-1582742_v1` | 2022 | MAD-UNet: Multi-scale attention and deep supervision-based 3D UNet for automatic liver seg | Research Square (preprint) |
| 144 | `10.21203_rs.3.rs-1740114_v1` | 2022 | DA-UNet: Deep supervision and atrous inception-based U-Net combining CRF for automatic liv | Research Square (preprint) |
| 145 | `10.22266_ijies2022.1231.47` | 2022 | A Weakly Reiterative Patches-Wise Framework for CT Liver and Lesions Segmentation | International Journal of Intelligent Eng |
| 146 | `10.3389_fmed.2021.794969` | 2022 | Three-Dimensional Liver Image Segmentation Using Generative Adversarial Networks Based on  | Frontiers in Medicine |
| 147 | `10.3389_fphys.2021.725865` | 2022 | Automatic Lung Segmentation and Quantification of Aeration in Computed Tomography of the C | Frontiers in Physiology |
| 148 | `10.3389_fvets.2022.1011804` | 2022 | A deep learning model for CT-based kidney volume determination in dogs and normal referenc | Frontiers in Veterinary Science |
| 149 | `10.3390_diagnostics12081788` | 2022 | Deep Segmentation Networks for Segmenting Kidneys and Detecting Kidney Stones in Unenhance | Diagnostics (MDPI) |
| 150 | `10.3390_jimaging8070195` | 2022 | Segmentation of Pancreatic Subregions in Computed Tomography Images | Journal of Imaging |
| 151 | `10.3934_mbe.2022066` | 2022 | An improved residual U-Net with morphological-based loss function for automatic liver segm | Mathematical Biosciences and Engineering |
| 152 | `10.3934_mbe.2023149` | 2022 | Hierarchical volumetric transformer with comprehensive attention for medical image segment | Mathematical Biosciences and Engineering |
| 153 | `10.5954_icarob.2022.gs2-3` | 2022 | Liver Segmentation in CT Images Using Residual U-Net and 3D CRF | The 2022 International Conference on Art |
| 154 | `10.1007_s10278-023-00804-1` | 2023 | Effect of Dataset Size and Medical Image Modality on Convolutional Neural Network Model Pe | Journal of Digital Imaging |
| 155 | `10.1038_s41598-023-32741-y` | 2023 | Localization of spleen and kidney organs from CT scans based on classification of slices i | Scientific Reports |
| 156 | `10.1038_s41598-023-34013-1` | 2023 | Graph matching and deep neural networks based whole heart and great vessel segmentation in | Scientific Reports |
| 157 | `10.1038_s41598-023-45140-0` | 2023 | Estimation of right lobe graft weight for living donor liver transplantation using deep le | Scientific Reports |
| 158 | `10.1109_access.2023.3313646` | 2023 | Semi-Supervised Learning With Fact-Forcing for Medical Image Segmentation | IEEE Access |
| 159 | `10.1109_iccvw60793.2023.00446` | 2023 | A Simple and Robust Framework for Cross-Modality Medical Image Segmentation applied to Vis | IEEE/CVF International Conference on Com |
| 160 | `10.1117_12.2651572` | 2023 | Analyzing Components of a Transformer under Different Dataset Scales in 3D Prostate CT Seg | Medical Imaging 2023: Image Processing ( |
| 161 | `10.1140_epjp_s13360-023-03896-4` | 2023 | Quantification of pulmonary involvement in COVID-19 pneumonia: an upgrade of the LungQuant | Eur. Phys. J. Plus |
| 162 | `10.21203_rs.3.rs-2466037_v1` | 2023 | Segmentation of Lung Lobes and Lesions in Chest CT for the Classification of COVID-19 Seve | Scientific Reports |
| 163 | `10.21203_rs.3.rs-3788726_v1` | 2023 | Deep Learning for Automated Measurement of Total Cardiac Volume for Heart Transplantation  | Research Square (preprint) |
| 164 | `10.24132_csrn.3301.6` | 2023 | Coordinate-Unet 3D for segmentation of lung parenchyma | WSCG 2023 Proceedings (Computer Science  |
| 165 | `10.3389_fonc.2023.1119008` | 2023 | Comprehensive clinical evaluation of deep learning-based auto-segmentation for radiotherap | Frontiers in Oncology |
| 166 | `10.3389_fonc.2023.1137803` | 2023 | Validation of clinical acceptability of deep-learning-based automated segmentation of orga | Frontiers in Oncology |
| 167 | `10.3389_fonc.2023.1169922` | 2023 | Automatic renal mass segmentation and classification on CT images based on 3D U-Net and Re | Frontiers in Oncology |
| 168 | `10.3389_fonc.2023.1172424` | 2023 | Clinical target volume and organs at risk segmentation for rectal cancer radiotherapy usin | Frontiers in Oncology |
| 169 | `10.3390_healthcare11020213` | 2023 | Lung and Infection CT-Scan-Based Segmentation with 3D UNet Architecture and Its Modificati | Healthcare (MDPI) |
| 170 | `10.3857_roj.2023.00444` | 2023 | Feasibility of artificial intelligence-driven interfractional monitoring of organ changes  | Radiation Oncology Journal |
| 171 | `10.3934_era.2023221` | 2023 | 2.5D cascaded context-based network for liver and tumor segmentation from CT images | Electronic Research Archive |
| 172 | `10.3934_mbe.2023059` | 2023 | Multi-scale attention and deep supervision-based 3D UNet for automatic liver segmentation  | Mathematical Biosciences and Engineering |
| 173 | `10.4111_icu.20220411` | 2023 | Feasibility of artificial intelligence-based decision supporting system in tolvaptan presc | Investig Clin Urol |
| 174 | `10.48550_arxiv.2310.02972` | 2023 | Fully Automatic Segmentation of Gross Target Volume and Organs-at-Risk for Radiotherapy Pl | arXiv preprint |
| 175 | `10.1002_mp.17300` | 2024 | Reinforcement learning-based anatomical maps for pancreas subregion and duct segmentation | Medical Physics |
| 176 | `10.1007_s00330-023-10235-9` | 2024 | External validation, radiological evaluation, and development of deep learning automatic l | European Radiology |
| 177 | `10.1007_s12194-024-00832-8` | 2024 | Development of deep learning-based novel auto-segmentation for the prostatic urethra on pl | Radiological Physics and Technology |
| 178 | `10.1007_s12559-023-10126-7` | 2024 | Large-Kernel Attention for 3D Medical Image Segmentation | Cognitive Computation |
| 179 | `10.1016_j.compbiomed.2024.109202` | 2024 | Robust and smooth Couinaud segmentation via anatomical structure-guided point-voxel networ | Computers in Biology and Medicine |
| 180 | `10.1016_j.imavis.2024.105055` | 2024 | GLIMS: Attention-Guided Lightweight Multi-Scale Hybrid Network for Volumetric Semantic Seg | Image and Vision Computing |
| 181 | `10.1038_s41598-024-55137-y` | 2024 | Fully-automated multi-organ segmentation tool applicable to both non-contrast and post-con | Scientific Reports |
| 182 | `10.1101_2024.04.06.588383` | 2024 | Deep learning-based detection of murine congenital heart defects from µCT scans | bioRxiv preprint |
| 183 | `10.1186_s40644-024-00729-0` | 2024 | Automation of Wilms' tumor segmentation by artificial intelligence | Cancer Imaging |
| 184 | `10.1371_journal.pone.0312105` | 2024 | Liver tumor segmentation method combining multi-axis attention and conditional generative  | PLOS ONE |
| 185 | `10.3390_diagnostics14141538` | 2024 | Novel Domain Knowledge-Encoding Algorithm Enables Label-Efficient Deep Learning for Cardia | Diagnostics (MDPI) |
| 186 | `10.36306_konjes.1404420` | 2024 | A 3D U-NET BASED ON EARLY FUSION MODEL: IMPROVEMENT, COMPARATIVE ANALYSIS WITH STATE-OF-TH | Konya Journal of Engineering Sciences |
| 187 | `10.48550_arxiv.2401.04722` | 2024 | U-Mamba: Enhancing Long-range Dependency for Biomedical Image Segmentation | arXiv preprint |
| 188 | `10.48550_arxiv.2404.04202` | 2024 | Deep-learning Segmentation of Small Volumes in CT images for Radiotherapy Treatment Planni | arXiv preprint |
| 189 | `10.48550_arxiv.2406.16724` | 2024 | µ-Net: A Deep Learning-Based Architecture for µ-CT Segmentation | arXiv preprint |
| 190 | `10.48550_arxiv.2410.10551` | 2024 | Preserving Cardiac Integrity: A Topology-Infused Approach to Whole Heart Segmentation | arXiv preprint |
| 191 | `10.1007_s00261-024-04581-5` | 2025 | Automated abdominal organ segmentation algorithms for non-enhanced CT for volumetry and 3D | Abdominal Radiology |
| 192 | `10.1007_s00330-025-11623-z` | 2025 | Deep learning for automatic volumetric bowel segmentation on body CT images | European Radiology |
| 193 | `10.1007_s10796-024-10485-y` | 2025 | Comprehensive 3D Analysis of the Renal System and Stones: Segmenting and Registering Non-C | Information Systems Frontiers |
| 194 | `10.1007_s11548-024-03281-1` | 2025 | Double-mix pseudo-label framework: enhancing semi-supervised segmentation on category-imba | International Journal of Computer Assist |
| 195 | `10.1038_s41598-025-01802-9` | 2025 | Pancreas segmentation using AI developed on the largest CT dataset with multi-institutiona | Scientific Reports |
| 196 | `10.1093_ehjimp_qyaf011` | 2025 | Accurate fully automated assessment of left ventricle, left atrium, and left atrial append | European Heart Journal - Imaging Methods |
| 197 | `10.1186_s12880-025-01682-5` | 2025 | A deep learning algorithm for automated adrenal gland segmentation on non-contrast CT imag | BMC Medical Imaging |
| 198 | `10.1186_s12880-025-01991-9` | 2025 | Incremental 2D self-labelling for effective 3D medical volume segmentation with minimal an | BMC Medical Imaging |
| 199 | `10.1186_s41205-025-00254-1` | 2025 | Generalizable deep learning framework for 3D medical image segmentation using limited trai | 3D Printing in Medicine |
| 200 | `10.1371_journal.pone.0332603` | 2025 | Improving segmentation precision in prostate cancer adaptive radiation therapy with a pati | PLOS One |
| 201 | `10.21203_rs.3.rs-7925953_v1` | 2025 | Deep Learning-Based CT Splenic Segmentation and Morphometrics: A Spleen Volume Prediction  | Research Square (preprint) |
| 202 | `10.3169_mta.13.83` | 2025 | Kidney and Renal Tumor Segmentation by nnU-Net Using 3D CT Data from Different Sources | ITE Transactions on Media Technology and |
| 203 | `10.3389_fonc.2025.1475133` | 2025 | TriSwinUNETR lobe segmentation model for computing DIR-free CT-ventilation | Frontiers in Oncology |
| 204 | `10.3389_fvets.2025.1681820` | 2025 | Deep-learning-based automatic liver segmentation using computed tomography images in dogs | Frontiers in Veterinary Science |
| 205 | `10.3390_app15020837` | 2025 | G-UNETR++: A Gradient-Enhanced Network for Accurate and Robust Liver Segmentation from Com | Applied Sciences (MDPI) |
| 206 | `10.3390_math13243942` | 2025 | Deep Learning Model with Attention Mechanism for a 3D Pancreas Segmentation in CT Scans | Mathematics (MDPI) |
| 207 | `10.3390_s25175603` | 2025 | DG-TTA: Out-of-Domain Medical Image Segmentation Through Augmentation, Descriptor-Driven D | Sensors (MDPI) |
| 208 | `10.3390_tomography11010003` | 2025 | Dual-Stage AI Model for Enhanced CT Imaging: Precision Segmentation of Kidney and Tumors | Tomography (MDPI) |
| 209 | `10.3803_enm.2025.2336` | 2025 | Deep Learning-Based Adrenal Gland Volumetry for the Prediction of Diabetes | Endocrinology and Metabolism (EnM) |
| 210 | `10.46310_tjim.1580929` | 2025 | Region segmentation for lung cancer Computed Tomography image using 3D U-Net model | Turkish Journal of Internal Medicine |
| 211 | `10.48084_etasr.9157` | 2025 | Efficient Liver Segmentation using Advanced 3D-DCNN Algorithm on CT Images | Engineering, Technology & Applied Scienc |
| 212 | `10.48550_arxiv.2511.14971` | 2025 | Clinical Validation and Prospective Deployment of an Automated Deep Learning-Based Coronar | arXiv preprint |
| 213 | `10.52783_jisem.v10i49s.9954` | 2025 | An Efficient Deep Learning Approach for Liver Segmentation in Medical Imaging | Journal of Information Systems Engineeri |
| 214 | `10.54254_2755-2721_2026.tj28958` | 2025 | Speed-Accuracy-Memory Cooperative Optimization of Lightweight Dynamic 3D U-Net for Efficie | Proceedings of CONF-SPML 2026 Symposium: |
| 215 | `10.58190_imiens.2025.126` | 2025 | Dual-Scale Transformer-Guided Attention Network for Efficient Multi-OAR Segmentation in He | Intelligent Methods in Engineering Scien |
| 216 | `10.61882_ist.202502.10.03` | 2025 | AbdomenAtlasNet-3.0: Multi-Phase Deep Learning for Robust Multi-Organ Segmentation of Core | InfoScience Trends |
| 217 | `10.1038_s41598-026-51057-1` | 2026 | Deformable multi-head cross attention-based 3D U-net for context-aware multi-modal cardiac | Scientific Reports |
| 218 | `10.1038_s41598-026-51801-7` | 2026 | Submanifold Sparse Convolutional Networks for Automated 3D Segmentation of Kidneys and Kid | Scientific Reports |
| 219 | `10.1186_s12880-025-02106-0` | 2026 | Deep learning-based volumetry of the future liver remnants and prediction of candidates fo | BMC Medical Imaging |
| 220 | `10.17758_uruae31.ua0226112` | 2026 | Adaptive Three-Dimensional Identification of Renal Masses and Normal Kidney Tissues in Abd | 48th LISBON International Conference on  |
| 221 | `10.3389_fmedt.2026.1708094` | 2026 | Mamba-enhanced codebook learning with anatomical constraints for liver and tumor segmentat | Frontiers in Medical Technology |
| 222 | `10.48550_arxiv.2606.23879` | 2026 | Promise and challenges of heart chamber segmentation from non-contrast CT scans using cont | arXiv preprint |
| 223 | `10.64898_2026.01.11.26343874` | 2026 | Onco-Seg: Adapting Promptable Concept Segmentation for Multi-Modal Medical Imaging | Preprint |
| 224 | `10.64898_2026.02.17.26346486` | 2026 | Quality versus quantity of training datasets for artificial intelligence–based whole liver | medRxiv (preprint, not peer reviewed) |

### Framework/Software studies (n=9)

| # | paper_id | Year | Title | Venue |
|---|---------|------|-------|-------|
| 1 | `10.1101_2021.03.17.435903` |  | Portable framework to deploy deep learning segmentation models for medical images |  |
| 2 | `10.1001_jamanetworkopen.2020.27426` | 2020 | Evaluation of Deep Learning to Augment Image-Guided Radiotherapy for Head and Neck and Pro | JAMA Network Open |
| 3 | `10.1007_978-3-031-17027-0_2` | 2022 | DeepEdit: Deep Editable Learning for Interactive Segmentation of 3D Medical Images | MICCAI 2022 (Springer LNCS, ch. 978-3-03 |
| 4 | `10.48550_arxiv.2211.02701` | 2022 | MONAI: An open-source framework for deep learning in healthcare | arXiv preprint arXiv:2211.02701 |
| 5 | `10.1016_j.media.2024.103207` | 2024 | MONAI Label: A framework for AI-assisted Interactive Labeling of 3D Medical Images | Medical Image Analysis |
| 6 | `10.48550_arxiv.2406.05285` | 2024 | VISTA3D: A Unified Segmentation Foundation Model for 3D Medical Imaging | arXiv preprint arXiv:2406.05285 |
| 7 | `10.1007_s10278-025-01716-y` | 2025 | Liver Segment and Lesion Segmentation on CT and MRI: An Open-Source Contribution to TotalS | Journal of Imaging Informatics in Medici |
| 8 | `10.48550_arxiv.2503.08373` | 2025 | nnInteractive: Redefining 3D Promptable Segmentation | arXiv preprint arXiv:2503.08373 |
| 9 | `10.21203_rs.3.rs-9480032_v1` | 2026 | MHub.ai: A Standardized Platform for Reproducible AI Research in Medical Imaging | Research Square (preprint) |

### Benchmark papers (n=3)

| # | paper_id | Year | Title | Venue |
|---|---------|------|-------|-------|
| 1 | `10.1016_j.acra.2020.08.023` | 2020 | Deep Learning for Automated Liver Segmentation to Aid in the Study of Infectious Diseases  | Academic Radiology |
| 2 | `10.5152_dir.2019.19025` | 2020 | Comparison of semi-automatic and deep learning-based automatic methods for liver segmentat | Diagnostic and Interventional Radiology |
| 3 | `10.1145_3459930.3469564` | 2021 | Segmenting Thoracic Cavities with Neoplastic Lesions: A Head-to-head Benchmark with Fully  | ACM-BCB '21 (11th ACM International Conf |
