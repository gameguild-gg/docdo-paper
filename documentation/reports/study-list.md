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

---

## v2.2 Section (2026-10-01) — included studies (254)

Regenerated from `pipeline_outputs/s3v2_extracted_data_full.csv` (INCLUDE rows) after the second
shadow-library wave (+21 PDFs). The v1 list is preserved as history; the v2.1 section is superseded.
Total: **254 studies** (242 method, 9 framework/software, 3 benchmark).

### Method papers (n=242)

| # | paper_id | Year | Title | Venue |
|---|---------|------|-------|-------|
| 1 | `10.1007_978-3-319-46723-8_48` | 2016 | Automatic Liver and Lesion Segmentation in CT Using Cascaded Fully Convolutional Neural Ne | MICCAI 2016 (Springer LNCS) |
| 2 | `10.1088_1361-6560_61_24_8676` | 2016 | Automatic 3D liver segmentation based on deep learning and globally optimized surface evol | Physics in Medicine & Biology |
| 3 | `10.1002_mp.12480` | 2017 | Deep learning of the sectional appearances of 3D CT images for anatomical structure segmen | Medical Physics |
| 4 | `10.1002_mp.12593` | 2017 | Esophagus segmentation in CT via 3D fully convolutional neural network and random walk | Medical Physics |
| 5 | `10.1109_icsipa.2017.8120664` | 2017 | Fully automated esophagus segmentation with a hierarchical deep learning approach | IEEE International Conference on Signal  |
| 6 | `10.1109_isbi.2017.7950685` | 2017 | Segmentation of Organs at Risk in Thoracic CT Images Using a SharpMask Architecture and Co | IEEE International Symposium on Biomedic |
| 7 | `10.1117_12.2254201` | 2017 | Automated segmentation of 3D anatomical structures on CT images by using a deep convolutio | SPIE Medical Imaging 2017: Image Process |
| 8 | `10.1117_12.2255528` | 2017 | Segmentation of inner and outer bladder wall using deep-learning convolutional neural netw | SPIE Medical Imaging 2017: Computer-Aide |
| 9 | `10.1155_2017_6941306` | 2017 | A Multiorgan Segmentation Model for CT Volumes via Full Convolution-Deconvolution Network | BioMed Research International |
| 10 | `10.17918_d8p65k` | 2017 | Image analysis methods for identification and segmentation of biological structures using  | Drexel University (PhD Thesis) |
| 11 | `10.48550_arxiv.1702.00045` | 2017 | Spatial Aggregation of Holistically-Nested Convolutional Neural Networks for Automated Pan | arXiv preprint |
| 12 | `10.48550_arxiv.1711.08580` | 2017 | 3D Anisotropic Hybrid Network: Transferring Convolutional Features from 2D Images to 3D An | arXiv preprint |
| 13 | `10.1002_mp.13326` | 2018 | Deep-Learning Convolutional Neural Network: Inner and Outer Bladder Wall Segmentation in C | Medical Physics |
| 14 | `10.1007_s11548-018-1733-7` | 2018 | Automatic bladder segmentation from CT images using deep CNN and 3D fully connected CRF-RN | International Journal of Computer Assist |
| 15 | `10.1007_s11548-018-1797-4` | 2018 | TernaryNet: Faster Deep Model Inference without GPUs for Medical 3D Segmentation using Spa | MICCAI 2018 (Springer LNCS; arXiv 1801.0 |
| 16 | `10.1016_j.compmedimag.2018.03.001` | 2018 | An application of cascaded 3D fully convolutional networks for medical image segmentation | Computerized Medical Imaging and Graphic |
| 17 | `10.1109_bibm.2018.8621257` | 2018 | Automatic Liver Segmentation Using Multi-plane Integrated Fully Convolutional Neural Netwo | IEEE International Conference on Bioinfo |
| 18 | `10.1109_crc.2018.00010` | 2018 | Medical Images Sequence Normalization and Augmentation: Improve Liver Tumor Segmentation F | International Conference on Control, Rob |
| 19 | `10.1109_icpr.2018.8545143` | 2018 | Automatic Segmentation of Kidney and Renal Tumor in CT Images Based on 3D Fully Convolutio | 2018 24th International Conference on Pa |
| 20 | `10.1109_icpr.2018.8546017` | 2018 | SequentialSegNet: Combination with Sequential Feature for Multi-organ Segmentation | 2018 24th International Conference on Pa |
| 21 | `10.1109_ijcnn.2018.8489677` | 2018 | End-to-End Supervised Lung Lobe Segmentation | 2018 International Joint Conference on N |
| 22 | `10.1109_tmi.2018.2806309` | 2018 | Automatic Multi-organ Segmentation on Abdominal CT with Dense V-networks | IEEE Transactions on Medical Imaging |
| 23 | `10.1117_12.2293499` | 2018 | Towards dense volumetric pancreas segmentation in CT using 3D fully convolutional networks | SPIE Medical Imaging (arXiv:1711.06439v2 |
| 24 | `10.1145_3285996.3286014` | 2018 | Automatic Liver Segmentation in CT Volumes with Improved 3D U-net | ISICDM 2018 (ACM) |
| 25 | `10.1145_3290420.3290461` | 2018 | 3D Anisotropic Convolutional Neural Network with Step Transfer Learning for Liver Segmenta | ICCIP 2018 (ACM) |
| 26 | `10.1145_3301879.3301883` | 2018 | Automatic Segmentation of the Prostate on 3D CT Images by Using Multiple Deep Learning Net | ICBBE '18 (ACM International Conference  |
| 27 | `10.48550_arxiv.1805.12526` | 2018 | Fully Automated Organ Segmentation in Male Pelvic CT Images | arXiv preprint |
| 28 | `10.48550_arxiv.1807.02437` | 2018 | Deep Sequential Segmentation of Organs in Volumetric Medical Scans | arXiv preprint |
| 29 | `10.48550_arxiv.1809.10245` | 2018 | CYLINDRICAL TRANSFORM: 3D SEMANTIC SEGMENTATION OF KIDNEYS WITH LIMITED ANNOTATED IMAGES | IEEE Global Conference on Signal and Inf |
| 30 | `10.48550_arxiv.1810.04017` | 2018 | Comparison of U-net-based Convolutional Neural Networks for Liver Segmentation in CT | arXiv preprint |
| 31 | `10.1002_acm2.12784` | 2019 | Liver tumor segmentation based on 3D convolutional neural network with dual scale | Journal of Applied Clinical Medical Phys |
| 32 | `10.1002_mp.13438` | 2019 | U-Net-based Deep-Learning Bladder Segmentation in CT Urography | Medical Physics |
| 33 | `10.1002_mp.13466` | 2019 | Deep convolutional neural network for segmentation of thoracic organs-at-risk using croppe | Medical Physics |
| 34 | `10.1002_mp.13735` | 2019 | Automatic Liver Segmentation by Integrating Fully Convolutional Networks into Active Conto | Medical Physics |
| 35 | `10.1007_978-3-030-00889-5_32` | 2019 | Automatic Segmentation of Pulmonary Lobes Using a Progressive Dense V-Network | arXiv:1902.06362 (cs.CV); Springer DOI 1 |
| 36 | `10.1016_j.media.2019.02.006` | 2019 | OBELISK-Net: Fewer Layers to Solve 3D Multi-Organ Segmentation with Sparse Deformable Conv | Medical Image Analysis |
| 37 | `10.1038_s41598-019-40710-7` | 2019 | Measurement of Glomerular Filtration Rate using Quantitative SPECT/CT and Deep-learning-ba | Scientific Reports |
| 38 | `10.1088_1361-6560_ab2818` | 2019 | Attention-enabled 3D boosted convolutional neural networks for semantic CT segmentation us | Physics in Medicine & Biology |
| 39 | `10.1088_1361-6560_ab59a4` | 2019 | Prediction of major torso organs in low-contrast micro-CT images of mice using a two-stage | Physics in Medicine & Biology |
| 40 | `10.1109_access.2019.2899608` | 2019 | AHCNet: An Application of Attention Mechanism and Hybrid Connection for Liver Tumor Segmen | IEEE Access |
| 41 | `10.1109_access.2019.2941154` | 2019 | An Augmentation Strategy for Medical Image Processing Based on Statistical Shape Model and | IEEE Access |
| 42 | `10.1109_cbmi.2019.8877400` | 2019 | Automatic liver segmentation on CT images combining region-based techniques and convolutio | IEEE International Conference on Content |
| 43 | `10.1109_isbi.2019.8759309` | 2019 | Learning to Segment the Lung Volume from CT Scans Based on Semi-Automatic Ground-Truth | IEEE 16th International Symposium on Bio |
| 44 | `10.1109_isbi.2019.8759492` | 2019 | Automated Segmentation of Pulmonary Lobes Using Coordination-Guided Deep Neural Networks | IEEE International Symposium on Biomedic |
| 45 | `10.1109_iwssip.2019.8787253` | 2019 | Whole Heart Segmentation from CT images Using 3D U-Net architecture | IEEE International Conference on Systems |
| 46 | `10.1109_kst.2019.8687816` | 2019 | U-Net and Mean-Shift Histogram for Efficient Liver Segmentation from CT Images | IEEE International Conference on Knowled |
| 47 | `10.1109_qrs-c.2019.00075` | 2019 | Reliable automatic organ segmentation from CT images using deep CNN | IEEE 19th International Conference on So |
| 48 | `10.1109_siprocess.2019.8868690` | 2019 | Liver Segmentation in CT based on ResUNet with 3D Probabilistic and Geometric Post Process | IEEE 4th International Conference on Sig |
| 49 | `10.1109_sps.2019.8882073` | 2019 | Segmentation of Organs at Risk in Chest Cavity Using 3D Deep Neural Network | IEEE Signal Processing Society conferenc |
| 50 | `10.1145_3364836.3364842` | 2019 | Convolutional Neural Networks Based Level Set Framework for Pancreas Segmentation from CT  | ISICDM 2019 (ACM) |
| 51 | `10.1145_3364836.3364885` | 2019 | Deep Interactive Segmentation of Uncertain Regions with Shadowed Sets | ISICDM 2019 (ACM International Symposium |
| 52 | `10.24926_548719.002` | 2019 | Cascaded Semantic Segmentation for Kidney and Tumor | Not specified |
| 53 | `10.24926_548719.006` | 2019 | Coarse to Fine Framework for Kidney Tumor Segmentation | Unknown (likely MICCAI KiTS19 Challenge) |
| 54 | `10.24926_548719.012` | 2019 | Segmentation of Kidney and Renal Tumor in CT Scans Using Convolutional Networks | KiTS19 Challenge (MICCAI 2019) |
| 55 | `10.24926_548719.014` | 2019 | KiTS challenge: VNet with attention gates and deep supervision | KiTS Challenge (MICCAI) |
| 56 | `10.24926_548719.016` | 2019 | 3D Unet-based Kidney and Kidney Tumor Segmentation with Attentive Feature Learning | MICCAI 2019 (KiTS Challenge) |
| 57 | `10.24926_548719.018` | 2019 | Automatic Kidney and Tumor Segmentation with Hybrid Hierarchical Networks | MICCAI 2019 Kidney Tumor Segmentation Ch |
| 58 | `10.24926_548719.034` | 2019 | Renal Tumor Segmentation in CT using Cascade U-Net with 2.5D approach | Unknown (conference paper) |
| 59 | `10.24926_548719.049` | 2019 | Using Two-stage Network to Segment Kidneys and Kidney Tumors | Unknown (likely conference/workshop) |
| 60 | `10.24926_548719.055` | 2019 | A Multi-scale Attention Network for Kidney Tumor Segmentation on CT Scans | Unknown (likely MICCAI or similar) |
| 61 | `10.24926_548719.059` | 2019 | Kidney and Kidney Tumor Segmentation Using Two-stage Convolutional Neural Network | Not specified |
| 62 | `10.24926_548719.082` | 2019 | Kidney and Kidney Tumor Segmentation using a Logical Ensemble of U-nets with Volumetric Va | MICCAI 2019 Kidney Tumor Segmentation Ch |
| 63 | `10.48550_arxiv.1809.00960` | 2019 | Organ at Risk Segmentation in Head and Neck CT Images Using a Two-Stage Segmentation Frame | IEEE Access |
| 64 | `10.48550_arxiv.1907.05273` | 2019 | Accurate Congenital Heart Disease Model Generation for 3D Printing | arXiv |
| 65 | `10.48550_arxiv.1908.00360` | 2019 | A Method of Rapid Quantification of Patient-Specific Organ Dose for CT Using Coupled Deep- | arXiv |
| 66 | `10.48550_arxiv.1909.06684` | 2019 | 3D Kidneys and Kidney Tumor Semantic Segmentation using Boundary-Aware Networks | arXiv preprint |
| 67 | `10.1002_acm2.13024` | 2020 | Automatic segmentation and applicator reconstruction for CT-based brachytherapy of cervica | Journal of Applied Clinical Medical Phys |
| 68 | `10.1002_mp.13950` | 2020 | Automatic multi-organ segmentation in dual-energy CT (DECT) with dedicated 3D fully convol | Medical Physics |
| 69 | `10.1002_mp.14303` | 2020 | Improving the Slice Interaction of 2.5D CNN for Automatic Pancreas Segmentation | Medical Physics |
| 70 | `10.1002_mp.14422` | 2020 | Complete Abdomen and Pelvis Segmentation using U-Net Variant Architecture | Medical Physics |
| 71 | `10.1002_mp.14451` | 2020 | Deep Learning from Dual-Energy Information for Whole-Heart Segmentation in Dual-Energy and | Medical Physics |
| 72 | `10.1007_978-3-030-68107-4_12` | 2020 | PC-U Net: Learning to Jointly Reconstruct and Segment the Cardiac Walls in 3D from CT Data | MICCAI 2020 (Springer LNCS) |
| 73 | `10.1016_j.cmpb.2020.105447` | 2020 | Deeply self-supervised contour embedded neural network applied to liver segmentation | Computer Methods and Programs in Biomedi |
| 74 | `10.1016_j.imu.2020.100357` | 2020 | MSS U-Net: 3D segmentation of kidneys and tumors from CT images with a multi-scale supervi | Informatics in Medicine Unlocked |
| 75 | `10.1016_j.media.2020.101884` | 2020 | A Deep Learning Framework for Pancreas Segmentation with Multi-atlas Registration and 3D L | Medical Image Analysis |
| 76 | `10.1016_j.phro.2020.05.009` | 2020 | Cardio-pulmonary substructure segmentation of radiotherapy computed tomography images usin | Physics and Imaging in Radiation Oncolog |
| 77 | `10.1016_j.rpor.2020.09.005` | 2020 | Convolutional neural network-based automatic liver delineation on contrast-enhanced and no | Reports of Practical Oncology and Radiot |
| 78 | `10.1038_s41598-019-57242-9` | 2020 | Active learning for accuracy enhancement of semantic segmentation with CNN-corrected label | Scientific Reports |
| 79 | `10.1038_s41598-020-63285-0` | 2020 | Abdominal multi-organ autosegmentation using 3D-patch-based deep convolutional neural netw | Scientific Reports |
| 80 | `10.1038_s41598-020-67544-y` | 2020 | Domain-specific cues improve robustness of deep learning-based segmentation of CT volumes | Scientific Reports |
| 81 | `10.1049_iet-ipr.2019.0399` | 2020 | DRAN: Deep recurrent adversarial network for automated pancreas segmentation | IET Image Processing |
| 82 | `10.1088_1361-6560_ab6f99` | 2020 | Interactive 3D U-net for the segmentation of the pancreas in computed tomography scans | Physics in Medicine & Biology |
| 83 | `10.1088_1742-6596_1631_1_012049` | 2020 | 3D Densely Connected Convolution Neural Networks for Pulmonary Parenchyma Segmentation fro | Journal of Physics: Conference Series |
| 84 | `10.1109_access.2019.2961125` | 2020 | Automatic Pancreas Segmentation via Coarse Location and Ensemble Learning | IEEE Access |
| 85 | `10.1109_access.2019.2961410` | 2020 | Improving Whole-Heart CT Image Segmentation by Attention Mechanism | IEEE Access |
| 86 | `10.1109_access.2020.2985671` | 2020 | Cascade U-ResNets for Simultaneous Liver and Lesion Segmentation | IEEE Access |
| 87 | `10.1109_access.2020.2988647` | 2020 | Deep Learning Initialized and Gradient Enhanced Level-set Based Segmentation for Liver Tum | IEEE Access |
| 88 | `10.1109_access.2020.3019518` | 2020 | Eso-Net: A Novel 2.5D Segmentation Network With the Multi-Structure Response Filter for th | IEEE Access |
| 89 | `10.1109_access.2020.3024277` | 2020 | Automatic Segmentation Using a Hybrid Dense Network Integrated With an 3D-Atrous Spatial P | IEEE Access |
| 90 | `10.1109_access.2020.3028038` | 2020 | Prior Attention Enhanced Convolutional Neural Network Based Automatic Segmentation of Orga | IEEE Access |
| 91 | `10.1109_embc44109.2020.9175907` | 2020 | Automatic Pulmonary Vein and Left Atrium Segmentation for TAPVC Preoperative Evaluation Us | IEEE Engineering in Medicine and Biology |
| 92 | `10.1109_icieam48468.2020.9111950` | 2020 | Hybrid 3D-ResNet Deep Learning Model for Automatic Segmentation of Thoracic Organs at Risk | 2020 International Conference on Industr |
| 93 | `10.1109_isbi45749.2020.9098325` | 2020 | An Efficient Hybrid Model for Kidney Tumor Segmentation in CT Images | IEEE 17th International Symposium on Bio |
| 94 | `10.1109_isbi45749.2020.9098609` | 2020 | A Triple-Stage Self-Guided Network for Kidney Tumor Segmentation | IEEE 17th International Symposium on Bio |
| 95 | `10.1109_isbi45749.2020.9098615` | 2020 | Liver Segmentation in CT with MRI Data: Zero-Shot Domain Adaptation by Contour Extraction  | IEEE 17th International Symposium on Bio |
| 96 | `10.1109_isbi45749.2020.9098701` | 2020 | Deep Learning and Unsupervised Fuzzy C-Means Based Level-Set Segmentation for Liver Tumor | IEEE 17th International Symposium on Bio |
| 97 | `10.1109_jbhi.2020.3004296` | 2020 | Structure Correction for Robust Volume Segmentation in Presence of Tumors | IEEE Journal of Biomedical and Health In |
| 98 | `10.1109_spin48934.2020.9071339` | 2020 | Deep Dilated V-Net for 3D Volume Segmentation of Pancreas in CT images | 2020 7th International Conference on Sig |
| 99 | `10.1111_cpf.12611` | 2020 | Deep learning-based quantification of PET/CT prostate gland uptake: association with overa | Clinical Physiology and Functional Imagi |
| 100 | `10.1148_ryai.2020190102` | 2020 | Fully Automatic Volume Measurement of the Spleen at CT Using Deep Learning | Radiology: Artificial Intelligence |
| 101 | `10.21203_rs.3.rs-83236_v1` | 2020 | Compare the Segmentation Accuracy of Heart Substructure on Contrast Enhanced CT by Deep Co | Research Square (preprint) |
| 102 | `10.2478_acss-2020-0005` | 2020 | Applying 3D U-Net Architecture to the Task of Multi-Organ Segmentation in Computed Tomogra | Applied Computer Systems |
| 103 | `10.25073_2588-1086_vnucsce.241` | 2020 | Liver Segmentation on a Variety of CT Images Based on Convolutional Neural Networks Combin | VNU Journal of Science: Computer Science |
| 104 | `10.32985_ijeces.11.1.3` | 2020 | Neural Network Based Whole Heart Segmentation from 3D CT Images | International Journal of Electrical and  |
| 105 | `10.3389_fbioe.2020.605132` | 2020 | RA-UNet: A Hybrid Deep Attention-Aware Network to Extract Liver and Tumor in CT Scans | Frontiers in Bioengineering and Biotechn |
| 106 | `10.3389_fnbot.2020.00049` | 2020 | AutoPath: Image-Specific Inference for 3D Segmentation | Frontiers in Neurorobotics |
| 107 | `10.3390_app10196838` | 2020 | Point-Sampling Method Based on 3D U-Net Architecture to Reduce the Influence of False Posi | Applied Sciences (MDPI) |
| 108 | `10.48550_arxiv.2001.03111` | 2020 | Unpaired Multi-modal Segmentation via Knowledge Distillation | IEEE Transactions on Medical Imaging |
| 109 | `10.48550_arxiv.2002.06927` | 2020 | PATIENT-SPECIFIC FINETUNING OF DEEP LEARNING MODELS FOR ADAPTIVE RADIOTHERAPY IN PROSTATE  | arXiv preprint |
| 110 | `10.48550_arxiv.2006.15713` | 2020 | Generalizable Cone Beam CT Esophagus Segmentation using Physics-Based Data Augmentation | arXiv preprint |
| 111 | `10.48550_arxiv.2012.04701` | 2020 | 3D Graph Anatomy Geometry-Integrated Network for Pancreatic Mass Segmentation, Diagnosis,  | arXiv preprint |
| 112 | `10.1002_mp.14732` | 2021 | Automatic liver segmentation using 3D convolutional neural networks with a hybrid loss fun | Medical Physics |
| 113 | `10.1002_mp.14782` | 2021 | Two-stage deep learning model for fully automated pancreas segmentation on computed tomogr | Medical Physics |
| 114 | `10.1002_mp.14810` | 2021 | Automatic delineation of cardiac substructures using a region-based fully convolutional ne | Medical Physics |
| 115 | `10.1002_mp.14852` | 2021 | Interactive contouring through contextual deep learning | Medical Physics |
| 116 | `10.1007_s00330-020-07608-9` | 2021 | Automated segmentation of kidney and renal mass and automated detection of renal mass in C | European Radiology |
| 117 | `10.1016_j.cmpb.2021.106141` | 2021 | A Two-Phase Approach using Mask R-CNN and 3D U-Net for High-Accuracy Automatic Segmentatio | Computer Methods and Programs in Biomedi |
| 118 | `10.1016_j.radonc.2021.04.019` | 2021 | A deep learning-based auto-segmentation system for organs-at-risk on whole-body computed t | Radiotherapy and Oncology |
| 119 | `10.1088_1361-6560_abfce3` | 2021 | Pancreas Segmentation with Probabilistic Map Guided Bi-directional Recurrent UNet | Physics in Medicine & Biology (IOP Publi |
| 120 | `10.1088_1361-6560_ac3935` | 2021 | Efficient knowledge distillation for liver CT segmentation using growing assistant network | Physics in Medicine & Biology |
| 121 | `10.1088_1742-6596_1920_1_012060` | 2021 | Segmentation and Reconstruction of Abdominal Multi-tissues Based on Multiple Algorithms an | Journal of Physics: Conference Series |
| 122 | `10.1088_1757-899x_1128_1_012049` | 2021 | CT Guided Diagnosis: Cascaded U-Net for 3D Segmentation of Liver and Tumor | IOP Conference Series: Materials Science |
| 123 | `10.1093_jrr_rraa094` | 2021 | A slice classification model-facilitated 3D encoder–decoder network for segmenting organs  | Journal of Radiation Research |
| 124 | `10.1109_access.2021.3055803` | 2021 | Cross-Dataset Multiple Organ Segmentation From CT Imagery Using FBP-Derived Domain Adaptat | IEEE Access |
| 125 | `10.1109_access.2021.3089704` | 2021 | R2U3D: Recurrent Residual 3D U-Net for Lung Segmentation | IEEE Access |
| 126 | `10.1109_bibm52615.2021.9669823` | 2021 | CC-DenseUNet: Densely Connected U-Net with Criss-Cross Attention for Liver and Tumor Segme | IEEE International Conference on Bioinfo |
| 127 | `10.1109_embc46164.2021.9629671` | 2021 | An Efficient and Accurate 3D Multiple-Contextual Semantic Segmentation Network for Medical | 2021 43rd Annual International Conferenc |
| 128 | `10.1109_iccece51280.2021.9342350` | 2021 | 3D Segment and Pickup Framework for Pancreas Segmentation | 2021 IEEE International Conference on Co |
| 129 | `10.1109_jbhi.2021.3075752` | 2021 | Bridging the Gap between 2D and 3D Contexts in CT Volume for Liver and Tumor Segmentation | IEEE Journal of Biomedical and Health In |
| 130 | `10.1186_s12938-021-00932-1` | 2021 | A 2D–3D hybrid convolutional neural network for lung lobe auto-segmentation on standard sl | BioMedical Engineering OnLine |
| 131 | `10.1186_s13550-021-00796-5` | 2021 | Automated and robust organ segmentation for 3D-based internal dose calculation | EJNMMI Research |
| 132 | `10.1371_journal.pone.0252287` | 2021 | Multi-scale U-like network with attention mechanism for automatic pancreas segmentation | PLOS ONE |
| 133 | `10.21203_rs.3.rs-902758_v1` | 2021 | DALU-Net: Automated Liver Segmentation and Volumetry for Liver Transplantation in Abdomina | Research Square (preprint) |
| 134 | `10.2147_cmar.s330249` | 2021 | Automatic Segmentation of Clinical Target Volume and Organs-at-Risk for Breast Conservativ | Cancer Management and Research |
| 135 | `10.22215_etd_2021-15566` | 2021 | Development of an Integrated System for Automatic Tumor Detection for PET-CT Images | Carleton University (PhD Thesis) |
| 136 | `10.3389_fonc.2021.669437` | 2021 | Advanced Deep Learning Approach to Automatically Segment Malignant Tumors and Ablation Zon | Frontiers in Oncology |
| 137 | `10.3389_fphy.2021.743190` | 2021 | Deep Learning-Augmented Head and Neck Organs at Risk Segmentation From CT Volumes | Frontiers in Physics |
| 138 | `10.3390_a14050144` | 2021 | Boundary Loss-Based 2.5D Fully Convolutional Neural Networks Approach for Segmentation: A  | Algorithms (MDPI) |
| 139 | `10.3390_electronics10040431` | 2021 | Numerical Evaluation on Parametric Choices Influencing Segmentation Results in Radiology I | Electronics (MDPI) |
| 140 | `10.3390_tomography7040078` | 2021 | Evaluation of a Deep Learning Algorithm for Automated Spleen Segmentation in Patients with | Tomography (MDPI) |
| 141 | `10.48550_arxiv.2005.07462` | 2021 | MetricUNet: Synergistic Image- and Voxel-Level Learning for Precise Prostate Segmentation  | arXiv preprint |
| 142 | `10.48550_arxiv.2102.07899` | 2021 | A Deep-Learning Approach For Direct Whole-Heart Mesh Reconstruction | Medical Image Analysis |
| 143 | `10.1002_acm2.13631` | 2022 | RefineNet-based 2D and 3D automatic segmentations for clinical target volume and organs at | Journal of Applied Clinical Medical Phys |
| 144 | `10.1002_mp.15521` | 2022 | Technical note: Evaluation of a V-Net autosegmentation algorithm for pediatric CT scans: P | Medical Physics |
| 145 | `10.1007_978-3-031-16440-8_53` | 2022 | Self-supervised 3D anatomy segmentation using self-distilled masked image transformer (SMI | MICCAI 2022 (early accepted; Springer LN |
| 146 | `10.1007_s10916-022-01810-6` | 2022 | Automatic Cardiac Structure Contouring for Small Datasets with Cascaded Deep Learning Mode | Journal of Medical Systems |
| 147 | `10.1016_j.compbiomed.2021.105191` | 2022 | Deep learning-based whole-heart segmentation in 4D contrast-enhanced cardiac CT | Computers in Biology and Medicine |
| 148 | `10.1016_j.neucom.2022.07.024` | 2022 | Adaptable volumetric liver segmentation model for CT images using region-based features an | Neurocomputing |
| 149 | `10.1038_s41598-022-07848-3` | 2022 | Automated pancreas segmentation and volumetry using deep neural network on computed tomogr | Scientific Reports |
| 150 | `10.1038_s41598-022-09978-0` | 2022 | Deep 3D attention CLSTM U-Net based automated liver segmentation and volumetry for the liv | Scientific Reports |
| 151 | `10.1038_s41598-022-18173-0` | 2022 | Evaluation of a hybrid pipeline for automated segmentation of solid lesions based on mathe | Scientific Reports |
| 152 | `10.1038_s41598-022-20108-8` | 2022 | A pipeline for automated deep learning liver segmentation (PADLLS) from contrast enhanced  | Scientific Reports |
| 153 | `10.1038_s41598-022-21562-0` | 2022 | Deep supervision and atrous inception-based U-Net combining CRF for automatic liver segmen | Scientific Reports |
| 154 | `10.1097_as9.0000000000000155` | 2022 | nnU-Net Deep Learning Method for Segmenting Parenchyma and Determining Liver Volume From C | Annals of Surgery Open |
| 155 | `10.1109_elmar55880.2022.9899815` | 2022 | 3D U-Net based method for fast segmentation of whole heart from CT images | ELMAR 2022 (International Symposium Elec |
| 156 | `10.1109_wrcsara57040.2022.9903976` | 2022 | Two-Stage Multi-Organ Automatic Segmentation with Low GPU Memory Occupancy | 2022 WRC Symposium on Advanced Robotics  |
| 157 | `10.1186_s12880-022-00785-7` | 2022 | Heart and bladder detection and segmentation on FDG PET/CT by deep learning | BMC Medical Imaging |
| 158 | `10.1186_s13014-022-01985-9` | 2022 | Dosimetric impact of deep learning-based CT auto-segmentation on radiation therapy treatme | Radiation Oncology |
| 159 | `10.1186_s13014-022-02102-6` | 2022 | A deep image-to-image network organ segmentation algorithm for radiation treatment plannin | Radiation Oncology |
| 160 | `10.1186_s40001-022-00943-1` | 2022 | Automated quantitative assessment of pediatric blunt hepatic trauma by deep learning-based | European Journal of Medical Research |
| 161 | `10.21203_rs.3.rs-1582742_v1` | 2022 | MAD-UNet: Multi-scale attention and deep supervision-based 3D UNet for automatic liver seg | Research Square (preprint) |
| 162 | `10.21203_rs.3.rs-1740114_v1` | 2022 | DA-UNet: Deep supervision and atrous inception-based U-Net combining CRF for automatic liv | Research Square (preprint) |
| 163 | `10.22266_ijies2022.1231.47` | 2022 | A Weakly Reiterative Patches-Wise Framework for CT Liver and Lesions Segmentation | International Journal of Intelligent Eng |
| 164 | `10.3389_fmed.2021.794969` | 2022 | Three-Dimensional Liver Image Segmentation Using Generative Adversarial Networks Based on  | Frontiers in Medicine |
| 165 | `10.3389_fphys.2021.725865` | 2022 | Automatic Lung Segmentation and Quantification of Aeration in Computed Tomography of the C | Frontiers in Physiology |
| 166 | `10.3389_fvets.2022.1011804` | 2022 | A deep learning model for CT-based kidney volume determination in dogs and normal referenc | Frontiers in Veterinary Science |
| 167 | `10.3390_diagnostics12081788` | 2022 | Deep Segmentation Networks for Segmenting Kidneys and Detecting Kidney Stones in Unenhance | Diagnostics (MDPI) |
| 168 | `10.3390_jimaging8070195` | 2022 | Segmentation of Pancreatic Subregions in Computed Tomography Images | Journal of Imaging |
| 169 | `10.3934_mbe.2022066` | 2022 | An improved residual U-Net with morphological-based loss function for automatic liver segm | Mathematical Biosciences and Engineering |
| 170 | `10.3934_mbe.2023149` | 2022 | Hierarchical volumetric transformer with comprehensive attention for medical image segment | Mathematical Biosciences and Engineering |
| 171 | `10.5954_icarob.2022.gs2-3` | 2022 | Liver Segmentation in CT Images Using Residual U-Net and 3D CRF | The 2022 International Conference on Art |
| 172 | `10.1007_s10278-023-00804-1` | 2023 | Effect of Dataset Size and Medical Image Modality on Convolutional Neural Network Model Pe | Journal of Digital Imaging |
| 173 | `10.1038_s41598-023-32741-y` | 2023 | Localization of spleen and kidney organs from CT scans based on classification of slices i | Scientific Reports |
| 174 | `10.1038_s41598-023-34013-1` | 2023 | Graph matching and deep neural networks based whole heart and great vessel segmentation in | Scientific Reports |
| 175 | `10.1038_s41598-023-45140-0` | 2023 | Estimation of right lobe graft weight for living donor liver transplantation using deep le | Scientific Reports |
| 176 | `10.1109_access.2023.3313646` | 2023 | Semi-Supervised Learning With Fact-Forcing for Medical Image Segmentation | IEEE Access |
| 177 | `10.1109_iccvw60793.2023.00446` | 2023 | A Simple and Robust Framework for Cross-Modality Medical Image Segmentation applied to Vis | IEEE/CVF International Conference on Com |
| 178 | `10.1117_12.2651572` | 2023 | Analyzing Components of a Transformer under Different Dataset Scales in 3D Prostate CT Seg | Medical Imaging 2023: Image Processing ( |
| 179 | `10.1140_epjp_s13360-023-03896-4` | 2023 | Quantification of pulmonary involvement in COVID-19 pneumonia: an upgrade of the LungQuant | Eur. Phys. J. Plus |
| 180 | `10.21203_rs.3.rs-2466037_v1` | 2023 | Segmentation of Lung Lobes and Lesions in Chest CT for the Classification of COVID-19 Seve | Scientific Reports |
| 181 | `10.21203_rs.3.rs-3788726_v1` | 2023 | Deep Learning for Automated Measurement of Total Cardiac Volume for Heart Transplantation  | Research Square (preprint) |
| 182 | `10.24132_csrn.3301.6` | 2023 | Coordinate-Unet 3D for segmentation of lung parenchyma | WSCG 2023 Proceedings (Computer Science  |
| 183 | `10.3389_fonc.2023.1119008` | 2023 | Comprehensive clinical evaluation of deep learning-based auto-segmentation for radiotherap | Frontiers in Oncology |
| 184 | `10.3389_fonc.2023.1137803` | 2023 | Validation of clinical acceptability of deep-learning-based automated segmentation of orga | Frontiers in Oncology |
| 185 | `10.3389_fonc.2023.1169922` | 2023 | Automatic renal mass segmentation and classification on CT images based on 3D U-Net and Re | Frontiers in Oncology |
| 186 | `10.3389_fonc.2023.1172424` | 2023 | Clinical target volume and organs at risk segmentation for rectal cancer radiotherapy usin | Frontiers in Oncology |
| 187 | `10.3390_healthcare11020213` | 2023 | Lung and Infection CT-Scan-Based Segmentation with 3D UNet Architecture and Its Modificati | Healthcare (MDPI) |
| 188 | `10.3857_roj.2023.00444` | 2023 | Feasibility of artificial intelligence-driven interfractional monitoring of organ changes  | Radiation Oncology Journal |
| 189 | `10.3934_era.2023221` | 2023 | 2.5D cascaded context-based network for liver and tumor segmentation from CT images | Electronic Research Archive |
| 190 | `10.3934_mbe.2023059` | 2023 | Multi-scale attention and deep supervision-based 3D UNet for automatic liver segmentation  | Mathematical Biosciences and Engineering |
| 191 | `10.4111_icu.20220411` | 2023 | Feasibility of artificial intelligence-based decision supporting system in tolvaptan presc | Investig Clin Urol |
| 192 | `10.48550_arxiv.2310.02972` | 2023 | Fully Automatic Segmentation of Gross Target Volume and Organs-at-Risk for Radiotherapy Pl | arXiv preprint |
| 193 | `10.1002_mp.17300` | 2024 | Reinforcement learning-based anatomical maps for pancreas subregion and duct segmentation | Medical Physics |
| 194 | `10.1007_s00330-023-10235-9` | 2024 | External validation, radiological evaluation, and development of deep learning automatic l | European Radiology |
| 195 | `10.1007_s12194-024-00832-8` | 2024 | Development of deep learning-based novel auto-segmentation for the prostatic urethra on pl | Radiological Physics and Technology |
| 196 | `10.1007_s12559-023-10126-7` | 2024 | Large-Kernel Attention for 3D Medical Image Segmentation | Cognitive Computation |
| 197 | `10.1016_j.compbiomed.2024.109202` | 2024 | Robust and smooth Couinaud segmentation via anatomical structure-guided point-voxel networ | Computers in Biology and Medicine |
| 198 | `10.1016_j.imavis.2024.105055` | 2024 | GLIMS: Attention-Guided Lightweight Multi-Scale Hybrid Network for Volumetric Semantic Seg | Image and Vision Computing |
| 199 | `10.1038_s41598-024-55137-y` | 2024 | Fully-automated multi-organ segmentation tool applicable to both non-contrast and post-con | Scientific Reports |
| 200 | `10.1101_2024.04.06.588383` | 2024 | Deep learning-based detection of murine congenital heart defects from µCT scans | bioRxiv preprint |
| 201 | `10.1186_s40644-024-00729-0` | 2024 | Automation of Wilms' tumor segmentation by artificial intelligence | Cancer Imaging |
| 202 | `10.1371_journal.pone.0312105` | 2024 | Liver tumor segmentation method combining multi-axis attention and conditional generative  | PLOS ONE |
| 203 | `10.3390_diagnostics14141538` | 2024 | Novel Domain Knowledge-Encoding Algorithm Enables Label-Efficient Deep Learning for Cardia | Diagnostics (MDPI) |
| 204 | `10.36306_konjes.1404420` | 2024 | A 3D U-NET BASED ON EARLY FUSION MODEL: IMPROVEMENT, COMPARATIVE ANALYSIS WITH STATE-OF-TH | Konya Journal of Engineering Sciences |
| 205 | `10.48550_arxiv.2401.04722` | 2024 | U-Mamba: Enhancing Long-range Dependency for Biomedical Image Segmentation | arXiv preprint |
| 206 | `10.48550_arxiv.2404.04202` | 2024 | Deep-learning Segmentation of Small Volumes in CT images for Radiotherapy Treatment Planni | arXiv preprint |
| 207 | `10.48550_arxiv.2406.16724` | 2024 | µ-Net: A Deep Learning-Based Architecture for µ-CT Segmentation | arXiv preprint |
| 208 | `10.48550_arxiv.2410.10551` | 2024 | Preserving Cardiac Integrity: A Topology-Infused Approach to Whole Heart Segmentation | arXiv preprint |
| 209 | `10.1007_s00261-024-04581-5` | 2025 | Automated abdominal organ segmentation algorithms for non-enhanced CT for volumetry and 3D | Abdominal Radiology |
| 210 | `10.1007_s00330-025-11623-z` | 2025 | Deep learning for automatic volumetric bowel segmentation on body CT images | European Radiology |
| 211 | `10.1007_s10796-024-10485-y` | 2025 | Comprehensive 3D Analysis of the Renal System and Stones: Segmenting and Registering Non-C | Information Systems Frontiers |
| 212 | `10.1007_s11548-024-03281-1` | 2025 | Double-mix pseudo-label framework: enhancing semi-supervised segmentation on category-imba | International Journal of Computer Assist |
| 213 | `10.1038_s41598-025-01802-9` | 2025 | Pancreas segmentation using AI developed on the largest CT dataset with multi-institutiona | Scientific Reports |
| 214 | `10.1093_ehjimp_qyaf011` | 2025 | Accurate fully automated assessment of left ventricle, left atrium, and left atrial append | European Heart Journal - Imaging Methods |
| 215 | `10.1186_s12880-025-01682-5` | 2025 | A deep learning algorithm for automated adrenal gland segmentation on non-contrast CT imag | BMC Medical Imaging |
| 216 | `10.1186_s12880-025-01991-9` | 2025 | Incremental 2D self-labelling for effective 3D medical volume segmentation with minimal an | BMC Medical Imaging |
| 217 | `10.1186_s41205-025-00254-1` | 2025 | Generalizable deep learning framework for 3D medical image segmentation using limited trai | 3D Printing in Medicine |
| 218 | `10.1371_journal.pone.0332603` | 2025 | Improving segmentation precision in prostate cancer adaptive radiation therapy with a pati | PLOS One |
| 219 | `10.21203_rs.3.rs-7925953_v1` | 2025 | Deep Learning-Based CT Splenic Segmentation and Morphometrics: A Spleen Volume Prediction  | Research Square (preprint) |
| 220 | `10.3169_mta.13.83` | 2025 | Kidney and Renal Tumor Segmentation by nnU-Net Using 3D CT Data from Different Sources | ITE Transactions on Media Technology and |
| 221 | `10.3389_fonc.2025.1475133` | 2025 | TriSwinUNETR lobe segmentation model for computing DIR-free CT-ventilation | Frontiers in Oncology |
| 222 | `10.3389_fvets.2025.1681820` | 2025 | Deep-learning-based automatic liver segmentation using computed tomography images in dogs | Frontiers in Veterinary Science |
| 223 | `10.3390_app15020837` | 2025 | G-UNETR++: A Gradient-Enhanced Network for Accurate and Robust Liver Segmentation from Com | Applied Sciences (MDPI) |
| 224 | `10.3390_math13243942` | 2025 | Deep Learning Model with Attention Mechanism for a 3D Pancreas Segmentation in CT Scans | Mathematics (MDPI) |
| 225 | `10.3390_s25175603` | 2025 | DG-TTA: Out-of-Domain Medical Image Segmentation Through Augmentation, Descriptor-Driven D | Sensors (MDPI) |
| 226 | `10.3390_tomography11010003` | 2025 | Dual-Stage AI Model for Enhanced CT Imaging: Precision Segmentation of Kidney and Tumors | Tomography (MDPI) |
| 227 | `10.3803_enm.2025.2336` | 2025 | Deep Learning-Based Adrenal Gland Volumetry for the Prediction of Diabetes | Endocrinology and Metabolism (EnM) |
| 228 | `10.46310_tjim.1580929` | 2025 | Region segmentation for lung cancer Computed Tomography image using 3D U-Net model | Turkish Journal of Internal Medicine |
| 229 | `10.48084_etasr.9157` | 2025 | Efficient Liver Segmentation using Advanced 3D-DCNN Algorithm on CT Images | Engineering, Technology & Applied Scienc |
| 230 | `10.48550_arxiv.2511.14971` | 2025 | Clinical Validation and Prospective Deployment of an Automated Deep Learning-Based Coronar | arXiv preprint |
| 231 | `10.52783_jisem.v10i49s.9954` | 2025 | An Efficient Deep Learning Approach for Liver Segmentation in Medical Imaging | Journal of Information Systems Engineeri |
| 232 | `10.54254_2755-2721_2026.tj28958` | 2025 | Speed-Accuracy-Memory Cooperative Optimization of Lightweight Dynamic 3D U-Net for Efficie | Proceedings of CONF-SPML 2026 Symposium: |
| 233 | `10.58190_imiens.2025.126` | 2025 | Dual-Scale Transformer-Guided Attention Network for Efficient Multi-OAR Segmentation in He | Intelligent Methods in Engineering Scien |
| 234 | `10.61882_ist.202502.10.03` | 2025 | AbdomenAtlasNet-3.0: Multi-Phase Deep Learning for Robust Multi-Organ Segmentation of Core | InfoScience Trends |
| 235 | `10.1038_s41598-026-51057-1` | 2026 | Deformable multi-head cross attention-based 3D U-net for context-aware multi-modal cardiac | Scientific Reports |
| 236 | `10.1038_s41598-026-51801-7` | 2026 | Submanifold Sparse Convolutional Networks for Automated 3D Segmentation of Kidneys and Kid | Scientific Reports |
| 237 | `10.1186_s12880-025-02106-0` | 2026 | Deep learning-based volumetry of the future liver remnants and prediction of candidates fo | BMC Medical Imaging |
| 238 | `10.17758_uruae31.ua0226112` | 2026 | Adaptive Three-Dimensional Identification of Renal Masses and Normal Kidney Tissues in Abd | 48th LISBON International Conference on  |
| 239 | `10.3389_fmedt.2026.1708094` | 2026 | Mamba-enhanced codebook learning with anatomical constraints for liver and tumor segmentat | Frontiers in Medical Technology |
| 240 | `10.48550_arxiv.2606.23879` | 2026 | Promise and challenges of heart chamber segmentation from non-contrast CT scans using cont | arXiv preprint |
| 241 | `10.64898_2026.01.11.26343874` | 2026 | Onco-Seg: Adapting Promptable Concept Segmentation for Multi-Modal Medical Imaging | Preprint |
| 242 | `10.64898_2026.02.17.26346486` | 2026 | Quality versus quantity of training datasets for artificial intelligence–based whole liver | medRxiv (preprint, not peer reviewed) |

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
---

## v2.3 Section (2026-10-08) — wave-8 additions (+179 studies; corpus 433)

### New method papers (n=163) (n=163)

| # | paper_id | Year | Title | Venue |
|---|---------|------|-------|-------|
| 1 | `10.1002_acm2.13566` | 2022 | Three-dimensional deep neural network for automatic delineation of cervical cancer in planning  | Journal of Applied Clinical Medical Physics |
| 2 | `10.1002_acm2.14371` | 2024 | A deep learning-based 3D Prompt-nnUnet model for automatic segmentation in brachytherapy of pos | Journal of Applied Clinical Medical Physics |
| 3 | `10.1002_acm2.14397` | 2024 | Automated segmentation of liver and hepatic vessels on portal venous phase computed tomography  | Journal of Applied Clinical Medical Physics |
| 4 | `10.1002_acm2.70193` | 2025 | A multi-stage 3D convolutional neural network algorithm for CT-based lung segment parcellation | Journal of Applied Clinical Medical Physics |
| 5 | `10.1002_acm2.70651` | 2026 | Automatic adaptive radiotherapy triggering based on CBCT using deep learning for esophageal can | Journal of Applied Clinical Medical Physics |
| 6 | `10.1002_acm2.70677` | 2026 | FS-Mamba: Feature-wise scanning Mamba UNet for automatic image segmentation in liver tumor radi | Journal of Applied Clinical Medical Physics |
| 7 | `10.1002_acm2.70748` | 2026 | Deep learning auto-contouring of target and organs-at-risk on post-catheter CT images for prost | Journal of Applied Clinical Medical Physics |
| 8 | `10.1002_mp.13675` | 2018 | Fully Automatic Liver Attenuation Estimation combing CNN Segmentation and Morphological Operati | Medical Physics |
| 9 | `10.1002_mp.13940` | 2020 | Cardiac substructure segmentation with deep learning for improved cardiac sparing | Medical Physics |
| 10 | `10.1002_mp.14196` | 2020 | Pelvic multi-organ segmentation on cone-beam CT for prostate adaptive radiotherapy | Medical Physics |
| 11 | `10.1002_mp.15287` | 2022 | Weaving Attention U-net: A Novel Hybrid CNN and Attention-based Method for Organs-at-risk Segme | Medical Physics |
| 12 | `10.1002_mp.15310` | 2023 | A conventional-to-spectral CT image translation augmentation workflow for robust contrast injec | Medical Physics |
| 13 | `10.1002_mp.15351` | 2022 | Machine-Assisted Interpolation Algorithm for Semi-Automated Segmentation of Highly Deformable O | Medical Physics (Med Phys 49(1):41-51) |
| 14 | `10.1002_mp.15507` | 2022 | General and Custom Deep Learning Auto-Segmentation Models for Organs in Head and Neck, Abdomen, | Medical Physics |
| 15 | `10.1002_mp.15677` | 2022 | Registration-Guided Deep Learning Image Segmentation for Cone Beam CT-based Online Adaptive Rad | Medical Physics |
| 16 | `10.1002_mp.15723` | 2022 | Decoupled Pyramid Correlation Network for Liver Tumor Segmentation from CT images | Medical Physics |
| 17 | `10.1002_mp.15923` | 2022 | A reciprocal learning strategy for semisupervised medical image segmentation | Medical Physics |
| 18 | `10.1002_mp.17732` | 2025 | A general model for head and neck auto-segmentation with patient pre-treatment imaging during a | Medical Physics |
| 19 | `10.1002_mp.17782` | 2025 | Trade-off of different deep learning-based auto-segmentation approaches for treatment planning  | Medical Physics |
| 20 | `10.1002_mp.17815` | 2025 | Point-cloud segmentation with in-silico data augmentation for prostate cancer treatment | Medical Physics |
| 21 | `10.1002_mp.70583` | 2026 | An improved nnUNet with Axial Attention Mechanism and Attention Gated Units for Efficient and A | Medical Physics |
| 22 | `10.1002_rcs.70207` | 2026 | Development of an Artificial Intelligence-Driven Three-Dimensional Reconstruction Model of Rena | International Journal of Medical Robotics and Computer Assis |
| 23 | `10.1007_s11547-025-02166-w` | 2025 | Advanced lung segmentation on chest HRCT: comprehensive pipeline for quantification of airways, | La Radiologia Medica (Springer, Chest Radiology) |
| 24 | `10.1016_j.isci.2022.105712` | 2022 | Automated segmentation of lungs and lung tumors in mouse micro-CT scans | iScience |
| 25 | `10.1016_j.phro.2022.04.003` | 2022 | unknown - title page present only as non-OCR image | Physics and Imaging in Radiation Oncology |
| 26 | `10.1016_j.phro.2026.101011` | 2026 | Transformer-based cardiac substructure segmentation from contrast and non-contrast computed tom | Physics and Imaging in Radiation Oncology |
| 27 | `10.1016_j.radonc.2019.09.028` | 2019 | Synthetic MRI-aided Multi-organ Segmentation on Male Pelvic CT Using Cycle Consistent Deep Atte | Radiotherapy and Oncology |
| 28 | `10.1038_s41598-020-80936-4` | 2021 | CT image segmentation for inflamed and fibrotic lungs using a multi-resolution convolutional ne | Scientific Reports |
| 29 | `10.1038_s41598-021-87497-0` | 2021 | Quantitative salivary gland SPECT/CT using deep convolutional neural networks | Scientific Reports |
| 30 | `10.1038_s41598-022-16828-6` | 2022 | A lightweight neural network with multiscale feature enhancement for liver CT segmentation | Scientific Reports |
| 31 | `10.1038_s41598-022-21206-3` | 2022 | Multi-organ segmentation of abdominal structures from non-contrast and contrast enhanced CT ima | Scientific Reports |
| 32 | `10.1038_s41598-026-46244-z` | 2026 | FedLiverNet: a federated learning framework for privacy-preserving and efficient liver cancer d | Scientific Reports |
| 33 | `10.1038_s41598-026-48136-8` | 2026 | LobePrior Segments Lung Lobes on Computed Tomography Images in the Presence of Severe Abnormali | Scientific Reports |
| 34 | `10.1038_s41598-026-71324-5` | 2026 | A novel deep learning-based approach for liver segmentation from 3D CT images using probabilist | Scientific Reports (Article in Press) |
| 35 | `10.1038_s44172-024-00287-0` | 2024 | Towards a general computed tomography image segmentation model for anatomical structures and le | Communications Engineering (Nature Portfolio) |
| 36 | `10.1055_s-0046-1818558` | 2026 | Developing an Artificial Intelligence Solution to Autosegment the Edentulous Maxillary Bone for | European Journal of Dentistry (Thieme) |
| 37 | `10.1080_07853890.2025.2540596` | 2025 | Automatic recognition of adrenal incidentalomas using a two-stage cascade network: a multicente | Annals of Medicine (Taylor & Francis) |
| 38 | `10.1088_1361-6560_ab63bb` | 2020 | Male Pelvic Multi-Organ Segmentation Aided by CBCT-based Synthetic MRI | Physics in Medicine & Biology |
| 39 | `10.1088_1361-6560_acf2e2` | 2023 | Leveraging Global Binary Masks for Structure Segmentation in Medical Images | Physics in Medicine & Biology |
| 40 | `10.1088_1361-6560_ade197` | 2025 | Quantitative and automatic plan-of-the-day assessment to facilitate adaptive radiotherapy in ce | Physics in Medicine & Biology |
| 41 | `10.1109_access.2019.2908386` | 2019 | Nested Dilation Network (NDN) for Multi-Task Medical Image Segmentation | IEEE Access |
| 42 | `10.1109_access.2024.3437652` | 2024 | MulA-nnUNet: A Multi-Attention Enhanced nnUNet Framework for 3D Abdominal Multi-Organs Segmenta | IEEE Access |
| 43 | `10.1109_access.2024.3523766` | 2024 | RED-Net: A Neural Network for 3D Thyroid Segmentation in Chest CT Using Residual and Dilated Co | IEEE Access |
| 44 | `10.1109_access.2025.3559592` | 2025 | CUNet-CLSTM: A Novel Fusion of CUNet and CLSTM for Superior Liver Cancer Detection in CT Scans | IEEE Access |
| 45 | `10.1109_access.2025.3569073` | 2025 | Federated Knowledge Distillation With 3D Transformer Adaptation for Weakly Labeled Multi-Organ  | IEEE Access |
| 46 | `10.1109_access.2026.3678120` | 2026 | CT-to-Toxicity: A Proof-of-Concept AI Pipeline for Automatic Segmentation, Dose Estimation, and | IEEE Access |
| 47 | `10.1109_cbms52027.2021.00066` | 2021 | 3D Deep Learning for Anatomical Structure Segmentation in Multiple Imaging Modalities | Proc IEEE Int Symp Comput Based Med Syst (CBMS 2021) |
| 48 | `10.1109_icisce50968.2020.00302` | 2020 | 3D Liver and Tumor Segmentation in CT Scans with Robust Self-Paced Learning | IEEE ICISCE 2020 (10.1109/ICISCE50968.2020.00302) |
| 49 | `10.1109_ojemb.2024.3397623` | 2024 | BucketAugment: Reinforced Domain Generalisation in Abdominal CT Segmentation | IEEE Open Journal of Engineering in Medicine and Biology (OJ |
| 50 | `10.1109_tmi.2019.2930068` | 2019 | Reducing the Hausdorff Distance in Medical Image Segmentation with Convolutional Neural Network | IEEE Transactions on Medical Imaging (TMI 2019; UBC) |
| 51 | `10.1109_tmi.2020.2995108` | 2020 | Relational Modeling for Robust and Efficient Pulmonary Lobe Segmentation in CT Scans | IEEE Transactions on Medical Imaging (TMI) |
| 52 | `10.1109_wacv.2019.00020` | 2019 | Semi-Supervised 3D Abdominal Multi-Organ Segmentation via Deep Multi-Planar Co-Training | WACV 2019 (IEEE Winter Conference on Applications of Compute |
| 53 | `10.1117_1.jmi.11.2.024009` | 2024 | Cascaded cross-attention transformers and convolutional neural networks for multi-organ segment | Journal of Medical Imaging (SPIE) |
| 54 | `10.1117_12.2581101` | 2021 | Renal Cortex, Medulla and Pelvicaliceal System Segmentation on Arterial Phase CT Images with Ra | Proc. SPIE Medical Imaging 11596 |
| 55 | `10.1117_12.2611594` | 2022 | Semi-automated three-dimensional segmentation for cardiac CT images using deep learning and ran | Proc. SPIE Medical Imaging 12034 |
| 56 | `10.1117_12.2653387` | 2023 | Cascaded neural network segmentation pipeline for automated delineation of prostate and organs  | Proc SPIE Medical Imaging 12464 |
| 57 | `10.11817_j.issn.1672-7347.2026.260052` | 2026 | HAR-Net: Automatic delineation of clinical target volumes for cervical cancer guided by hierarc | Journal of Central South University (Medical Sciences), AI i |
| 58 | `10.1186_s40644-024-00675-x` | 2024 | Automated segmentation of lesions and organs at risk on [68Ga]Ga-PSMA-11 PET/CT images using se | Cancer Imaging (BMC) |
| 59 | `10.12122_j.issn.1673-4254.2020.11.07` | 2020 | Segmentation of organs at risk in nasopharyngeal cancer for radiotherapy using a self-adaptive  | Journal of Southern Medical University (南方医科大学学报) |
| 60 | `10.1371_journal.pone.0308181` | 2024 | Deep-learning-based segmentation using individual patient data on prostate cancer radiation the | PLOS ONE 19(7):e0308181 |
| 61 | `10.1681_asn.2021030404` | 2022 | Automated Segmentation of Kidney Cortex and Medulla in CT Images: A Multisite Evaluation Study | Journal of the American Society of Nephrology (JASN) |
| 62 | `10.2196_26151` | 2021 | Clinically Applicable Segmentation of Head and Neck Anatomy for Radiotherapy: Deep Learning Alg | Journal of Medical Internet Research (J Med Internet Res 202 |
| 63 | `10.3348_kjr.2020.0318` | 2021 | Automated Lung Segmentation on Chest Computed Tomography Images with Extensive Lung Parenchymal | Korean Journal of Radiology |
| 64 | `10.3389_fonc.2018.00215.s001` | 2018 | Deep Learning Renal Segmentation for Fully Automated Radiation Dose Estimation in Unsealed Sour | Frontiers in Oncology |
| 65 | `10.3389_fphy.2023.1266500` | 2023 | Segmentation of cardiac tissues and organs for CCTA images based on a deep learning model | Frontiers in Physics |
| 66 | `10.3389_frai.2022.1059007` | 2022 | DeepHeartCT: A fully automatic artificial intelligence hybrid framework based on convolutional  | Frontiers in Artificial Intelligence |
| 67 | `10.3390_app11093912` | 2021 | Whole Heart Segmentation Using 3D FM-Pre-ResNet Encoder-Decoder Based Architecture with Variati | Applied Sciences (MDPI), 11, 3912 |
| 68 | `10.3390_bioengineering11070737` | 2024 | Dual Attention-Based 3D U-Net Liver Segmentation Algorithm on CT Images | Bioengineering (MDPI) 2024, 11, 737 |
| 69 | `10.3390_jimaging11120433` | 2025 | DiagNeXt: A Two-Stage Attention-Guided ConvNeXt Framework for Kidney Pathology Segmentation and | Journal of Imaging 2025, 11(12):433, MDPI |
| 70 | `10.3390_s25061814` | 2025 | Multi-Scale Convolutional Attention and Structural Re-Parameterized Residual-Based 3D U-Net for | Sensors (MDPI) |
| 71 | `10.4103_jmp.jmp_169_25` | 2025 | A Combined Loss-driven Framework for Automated Parotid Segmentation in Head-and-Neck Computed T | Journal of Medical Physics |
| 72 | `10.4103_jmp.jmp_238_25` | 2025 | DART-Net: A Novel Deep Learning Framework for Precise Radiotherapy Planning with Automated Mult | Journal of Medical Physics |
| 73 | `10.48084_etasr.10115` | 2025 | Hybrid 3D U-Net and Attention Mechanisms for Whole Heart Segmentation from CT Images | Engineering, Technology & Applied Science Research (ETASR) |
| 74 | `10.65521_ijacect.v15i1.2391` | 2025 | Segmentation of ADPKD Computed Tomography Images with Deep Learning Approach for Predicting Tot | Biomedicines 2025;13(2):263 (MDPI) |
| 75 | `1607.00582v1` | 2015 | 3D Deeply Supervised Network for Automatic Liver Segmentation from CT Volumes | MICCAI 2015 (MLMI workshop; arXiv:1607.00582) |
| 76 | `1702.05970v2` | 2017 | Automatic Liver and Tumor Segmentation of CT and MRI Volumes Using Cascaded Fully Convolutional | arXiv preprint (TUM/LMU Grosshadern) |
| 77 | `1704.06382v1` | 2017 | Hierarchical 3D fully convolutional networks for multi-organ segmentation | arXiv preprint (not stated in excerpt) |
| 78 | `1707.08037v1` | 2017 | Automatic Liver Segmentation Using an Adversarial Image-to-Image Network | MICCAI 2017 (MLMI/LNCS); arXiv 1707.08037 |
| 79 | `1709.07330v3` | 2017 | H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes | arXiv (IEEE TMI format); CUHK |
| 80 | `1802.07800v2` | 2018 | Liver segmentation in CT images using three dimensional to two dimensional fully convolutional  | arXiv preprint 1802.07800v2 (conference-style manuscript) |
| 81 | `1804.02586v3` | 2018 | Semi-Supervised 3D Abdominal Multi-Organ Segmentation via Deep Multi-Planar Co-Training | arXiv 1804.02586v3 (2018) |
| 82 | `1806.02237v1` | 2018 | A multi-scale pyramid of 3D fully convolutional networks for abdominal multi-organ segmentation | arXiv (extended version of MICCAI 2016 MLMI paper) |
| 83 | `1806.03019v1` | 2018 | 3D FCN Feature Driven Regression Forest-Based Pancreas Localization and Segmentation | arXiv preprint (MICCAI-format) |
| 84 | `1808.04576v1` | 2018 | Automatic Airway Segmentation in chest CT using Convolutional Neural Networks | arXiv (1808.04576) |
| 85 | `1809.02268v1` | 2018 | Computation of Total Kidney Volume from CT images in Autosomal Dominant Polycystic Kidney Disea | arXiv preprint 1809.02268 (Fujifilm Corporation, Japan) |
| 86 | `1810.03968v2` | 2018 | Improving Myocardium Segmentation in Cardiac CT Angiography using Spectral Information | arXiv (SPIE Medical Imaging, UMC Utrecht) |
| 87 | `1811.11226v1` | 2018 | CT organ segmentation using GPU data augmentation, unsupervised labels and IOU loss | arXiv (submitted to IEEE; Stanford University) |
| 88 | `1903.00348v3` | 2020 | Transformation-consistent Self-ensembling Model for Semi-supervised Medical Image Segmentation | IEEE Transactions on Medical Imaging (arXiv:1903.00348) |
| 89 | `1903.04711v1` | 2019 | Deep Learning for Automated Medical Image Analysis | PhD Dissertation, UC Irvine (arXiv:1903.04711); qualifying c |
| 90 | `1906.02191v3` | 2020 | Uncertainty-based graph convolutional networks for organ segmentation refinement | MICCAI / arXiv:1906.02191v3 |
| 91 | `1906.12223v1` | 2019 | Adversarial optimization for joint registration and segmentation in prostate CT radiotherapy | arXiv 1906.12223 (MICCAI 2019, LNCS format) |
| 92 | `1907.02766v2` | 2019 | Data Efficient Unsupervised Domain Adaptation for Cross-Modality Image Segmentation | MICCAI 2019 (LNCS); arXiv:1907.02766 |
| 93 | `1907.12056v1` | 2019 | FocusNet: Imbalanced Large and Small Organ Segmentation with an End-to-End Deep Neural Network  | MICCAI 2019 (arXiv 1907.12056) |
| 94 | `1908.05062v4` | 2019 | Mask Mining for Improved Liver Lesion Segmentation | arXiv (1908.05062v4) |
| 95 | `1908.08588v1` | 2018 | A joint 3D UNet-Graph Neural Network-based method for Airway Segmentation from chest CTs | arXiv (1908.08588) |
| 96 | `1909.06685v1` | 2019 | Automated Multiclass Cardiac Volume Segmentation and Model Generation | arXiv preprint |
| 97 | `1909.07480v2` | 2019 | Z-Net: an Anisotropic 3D DCNN for Medical CT Volume Segmentation | arXiv (Imperial College London, Hamlyn Centre) |
| 98 | `1910.02235v2` | 2019 | Cascaded Volumetric Convolutional Network for Kidney Tumor Segmentation from CT volumes | MICCAI 2019 KiTS Challenge (arXiv 1910.02235) |
| 99 | `2001.09647v1` | 2020 | Basic Ensembles of Vanilla-Style Deep Learning Models Improve Liver Segmentation From CT Images | arXiv (IEEE-style manuscript; Dokuz Eylul Univ. + Bangor Uni |
| 100 | `2002.04098v1` | 2020 | Outlier Guided Optimization of Abdominal Segmentation | SPIE Medical Imaging (arXiv:2002.04098) |
| 101 | `2005.13690v2` | 2020 | Multiple resolution residual network for automatic thoracic organs-at-risk segmentation from CT | arXiv (MSKCC, Medical Physics dept.) |
| 102 | `2009.09571v4` | 2020 | Semi-supervised Semantic Segmentation of Prostate and Organs-at-Risk on 3D Pelvic CT Images | arXiv (2009.09571v4) |
| 103 | `2012.03352v1` | 2020 | An Uncertainty-Driven GCN Refinement Strategy for Organ Segmentation | arXiv 2012.03352 (MICCAI UNSURE workshop proceedings, CC-BY  |
| 104 | `2012.09279v1` | 2020 | Spatial Context-Aware Self-Attention Model For Multi-Organ Segmentation | arXiv |
| 105 | `2103.10504v3` | 2022 | UNETR: Transformers for 3D Medical Image Segmentation | WACV 2022 / arXiv (NVIDIA + Vanderbilt) |
| 106 | `2103.16328v2` | 2021 | Automatic airway segmentation from computed tomography using robust and efficient 3-D convoluti | arXiv (2103.16328v2) |
| 107 | `2105.05204v1` | 2021 | Development of a Multi-Task Learning V-Net for Pulmonary Lobar Segmentation on Computed Tomogra | arXiv (2105.05204) |
| 108 | `2105.14314v3` | 2021 | Automatic CT Segmentation from Bounding Box Annotations Using Convolutional Neural Networks | arXiv preprint |
| 109 | `2106.11330v1` | 2021 | Context-aware PolyUNet for Liver and Lesion Segmentation from Abdominal CT Images | arXiv preprint (CUHK; work for MICCAI 2017 LiTS Challenge) |
| 110 | `2108.03117v1` | 2021 | Uncertainty-Based Dynamic Graph Neighborhoods For Medical Segmentation | PRIME 2021 workshop @ MICCAI (Springer proceedings) |
| 111 | `2108.06669v1` | 2021 | CPNet: Cycle Prototype Network for Weakly-supervised 3D Renal Compartments Segmentation on CT I | MICCAI 2021 (arXiv:2108.06669) |
| 112 | `2109.01667v1` | 2021 | Hierarchical 3D Feature Learning for Pancreas Segmentation | arXiv 2109.01667 (LNCS/MICCAI format) |
| 113 | `2111.03368v2` | 2021 | Hepatic vessel segmentation based on 3D swin-transformer with inductive biased multi-head self- | arXiv (Springer journal format; final venue not visible in e |
| 114 | `2112.08232v2` | 2021 | RA V-Net: Deep learning network for automated liver segmentation | arXiv preprint (arXiv:2112.08232) |
| 115 | `2201.11000v1` | 2022 | One-shot PACS: Patient-specific Anatomic Context and Shape prior aware recurrent registration-s | arXiv 2201.11000 (MSKCC; submitted for review May 2021) |
| 116 | `2204.00631v2` | 2022 | UNetFormer: A Unified Vision Transformer Model and Pre-Training Framework for 3D Medical Image  | arXiv (NVIDIA) |
| 117 | `2204.06243v1` | 2022 | Rapid Model Transfer for Medical Image Segmentation via Iterative Human-in-the-Loop Update: Fro | ICASSP-style conference paper (arXiv 2204.06243) |
| 118 | `2206.00771v2` | 2022 | Dynamic Linear Transformer for 3D Biomedical Image Segmentation | arXiv (MICCAI-style; venue not explicitly visible) |
| 119 | `2207.09165v1` | 2022 | A Multi-Stage Framework for the 2022 Multi-Structure Segmentation for Renal Cancer Treatment | arXiv / KiPA2022 challenge (MICCAI 2022 working notes) |
| 120 | `2208.01382v1` | 2022 | A New Probabilistic V-Net Model with Hierarchical Spatial Feature Transform for Efficient Abdom | arXiv 2208.01382v1 (MICCAI-style) |
| 121 | `2210.04285v1` | 2022 | Improved Abdominal Multi-Organ Segmentation via 3D Boundary-Constrained Deep Neural Networks | arXiv (2210.04285) |
| 122 | `2212.02014v3` | 2022 | Med-Query: Steerable Parsing of 9-DoF Medical Anatomies with Query Embedding | arXiv (DAMO Academy, Alibaba Group); IEEE-style manuscript |
| 123 | `2212.02854v1` | 2021 | Automated Segmentation of Computed Tomography Images with Submanifold Sparse Convolutional Netw | arXiv preprint |
| 124 | `2302.00162v4` | 2023 | Continual Segment: Towards a Single, Unified and Non-forgetting Continual Segmentation Model of | ICCV 2023 (DAMO Academy, Alibaba Group; University at Buffal |
| 125 | `2302.09785v1` | 2022 | Towards Simultaneous Segmentation of Liver Tumors and Intrahepatic Vessels via Cross-Attention  | arXiv (ICASSP-style formatting; Fudan University) |
| 126 | `2306.15515v2` | 2023 | Abdominal Organ Segmentation via Deep Diffeomorphic Mesh Deformations | arXiv (TUM / LMU, Munich Center for Machine Learning) |
| 127 | `2307.12853v2` | 2023 | Spatiotemporal Modeling Encounters 3D Medical Image Analysis: Slice-Shift UNet with Multi-View  | arXiv (Free University of Bozen-Bolzano) |
| 128 | `2309.03383v1` | 2023 | Kidney abnormality segmentation in thorax-abdomen CT scans | arXiv (eess.IV), Radboud UMC |
| 129 | `2309.08842v1` | 2023 | MA-SAM: Modality-agnostic SAM Adaptation for 3D Medical Image Segmentation | arXiv (later Medical Image Analysis) |
| 130 | `2309.09730v1` | 2023 | Scribble-based 3D Multiple Abdominal Organ Segmentation via Triple-branch Multi-dilated Network | arXiv preprint 2309.09730 (MICCAI-format paper) |
| 131 | `2310.09099v2` | 2023 | Vision Transformers increase efficiency of 3D cardiac CT multi-label segmentation | arXiv (under submission to IEEE Transactions on Medical Imag |
| 132 | `2312.04796v1` | 2023 | Segmentation of Kidney Tumors on Non-Contrast CT Images using Protuberance Detection Network | arXiv (LNCS/MICCAI-style formatting; final venue not visible |
| 133 | `2312.05528v1` | 2023 | Exploring 3D U-Net Training Configurations and Post-Processing Strategies for the MICCAI 2023 K | arXiv / MICCAI 2023 KiTS23 Challenge Working Notes (Korea Un |
| 134 | `2312.06275v4` | 2025 | DG-TTA: Out-of-Domain Medical Image Segmentation through Augmentation and Descriptor-Driven Dom | arXiv preprint (2312.06275v4) |
| 135 | `2405.12367v3` | 2024 | Large-Scale Multi-Center CT and MRI Segmentation of Pancreas with Deep Learning | Medical Image Analysis (arXiv:2405.12367v3) |
| 136 | `2409.11299v3` | 2024 | TTT-UNet: Enhancing U-Net with Test-Time Training Layers for Biomedical Image Segmentation | arXiv (Lehigh University et al.) |
| 137 | `2410.01003v1` | 2024 | Y-CA-Net: A Convolutional Attention Based Network for Volumetric Medical Image Segmentation | arXiv (MBZUAI) |
| 138 | `2411.02815v1` | 2024 | Artificial Intelligence-Enhanced Couinaud Segmentation for Precision Liver Cancer Therapy | arXiv |
| 139 | `2504.06921v1` | 2025 | Leveraging Anatomical Priors for Automated Pancreas Segmentation on Abdominal CT | arXiv (SPIE Medical Imaging style; NIH CC) |
| 140 | `2504.20837v1` | 2025 | RadSAM: Segmenting 3D radiological images with a 2D promptable model | arXiv (Raidium / Universite Paris Cite, AP-HP) |
| 141 | `2505.07573v2` | 2026 | Robust Renal Mass Segmentation on CT: A Validation Study of an AI-Based Framework | MELBA (Machine Learning for Biomedical Imaging), 2026; arXiv |
| 142 | `2506.01073v1` | 2025 | A Large Convolutional Neural Network for Clinical Target and Multi-organ Segmentation in Gyneco | arXiv preprint |
| 143 | `2507.18177v2` | 2025 | Differential-UMamba: Rethinking Tumor Segmentation Under Limited Data Scenarios | arXiv (Elsevier submission, preprint) |
| 144 | `2507.19590v1` | 2025 | T-MPEDNet: Unveiling the Synergy of Transformer-aware Multiscale Progressive Encoder-Decoder Ne | Biomedical Signal Processing and Control (arXiv preprint, ac |
| 145 | `2508.02557v2` | 2026 | RL-U2Net: A Dual-Branch UNet with Reinforcement Learning-Assisted Multimodal Feature Fusion for | arXiv / AAAI 2026 |
| 146 | `2508.05137v1` | 2025 | FedGIN: Federated Learning with Dynamic Global Intensity Non-linear Augmentation for Organ Segm | arXiv (MICCAI-workshop style formatting; venue not visible) |
| 147 | `2511.08509v1` | 2025 | Fast Multi-Organ Fine Segmentation in CT Images with Hierarchical Sparse Sampling and Residual  | arXiv (Siemens Medical Solutions USA) |
| 148 | `2512.07574v1` | 2025 | Precise Liver Tumor Segmentation in CT Using a Hybrid Deep Learning-Radiomics Framework | arXiv preprint arXiv:2512.07574 (9 Dec 2025) |
| 149 | `2602.20773v2` | 2026 | Federated Learning for Cross-Modality Medical Image Segmentation via Augmentation-Driven Genera | arXiv (preprint, NTNU/St. Olavs Hospital) |
| 150 | `2604.06658v1` | 2026 | GPAFormer: Graph-guided Patch Aggregation Transformer for Efficient 3D Medical Image Segmentati | arXiv preprint |
| 151 | `2605.03098v1` | 2026 | One Sequence to Segment Them All: Efficient Data Augmentation for CT and MRI Cross-Domain 3D Sp | arXiv 2605.03098 (MICCAI LNCS format, blinded) |
| 152 | `2606.00491v2` | 2026 | Pre-Deployment Robustness Stress Testing for CT Segmentation Systems Using Clinically Motivated | arXiv (preprint, submitted to Elsevier; Seoul National Unive |
| 153 | `2608.00508v1` | 2026 | RadYOLO: Computationally Efficient 3D Object Detection and Segmentation in CT and MRI | arXiv (MICCAI-style LNCS format; Fraunhofer MEVIS) |
| 154 | `2608.27190v1` | 2026 | Unsupervised Adaptation of 3D CT Foundation Models for 3D CBCT Segmentation | arXiv (MICCAI-style formatting, preprint) |
| 155 | `2608.31073v1` | 2026 | LISynSeg: Data-Centric Label-to-Image Synthesis for Cross-Modality Whole-Heart Segmentation | arXiv preprint (MICCAI LNCS format; CARE 2026 Whole-Heart ch |
| 156 | `2609.13043v1` | 2026 | Unified CT-MRI Pancreas Segmentation for Label-Efficient Cross-Modality Subregion Transfer | not visible (IEEE-style conference format, under review) |
| 157 | `arxiv:1809.04430` | 2021 | Deep learning to achieve clinically applicable segmentation of head and neck anatomy for radiot | arXiv:1809.04430v3 (cs.CV) |
| 158 | `arxiv:2304.02713` | 2023 | NUMSnet: Nested-U Multi-class Segmentation network for 3D Medical Image Stacks | arXiv preprint |
| 159 | `https___openalex.org_w7153022846` | 2024 | LobePrior segments lung lobes on computed tomography images in the presence of severe abnormali | Scientific Reports |
| 160 | `pmc12149727` | 2025 | Histogram-matching-enhanced adversarial learning for unsupervised domain adaptation in medical  | Medical Physics (Wiley, AAPM); DOI 10.1002/mp.17757 |
| 161 | `pmc12381746` | 2025 | Efficient 3D Biomedical Image Segmentation by Parallelly Multiscale Transformer-CNN Aggregation | Chemical & Biomedical Imaging (ACS) 2025, 3, 522–533; doi 10 |
| 162 | `pmc12719378` | 2025 | Uncertainty-guided test-time optimization for personalizing segmentation models in longitudinal | Medical Physics (Wiley/AAPM) |
| 163 | `pmc12796375` | 2026 | Foundation model-guided multi-view semi-supervised CT segmentation of liver tumors in resource- | npj Digital Medicine (2026) 9:31; doi 10.1038/s41746-025-021 |

### New framework/software studies (n=4) (n=4)

| # | paper_id | Year | Title | Venue |
|---|---------|------|-------|-------|
| 1 | `10.3390_bioengineering13050572` | 2026 | Development of an Integrated Radiotherapy Simulation Platform with AI-Driven Segmentation and R | Bioengineering (MDPI) |
| 2 | `1910.09308v1` | 2019 | MIScnn: A Framework for Medical Image Segmentation with Convolutional Neural Networks and Deep  | MICCAI 2019 (LNCS format); arXiv 1910.09308 |
| 3 | `2208.05868v2` | 2023 | TotalSegmentator: Robust Segmentation of 104 Anatomical Structures in CT images | Radiology: Artificial Intelligence |
| 4 | `2512.15921v2` | 2026 | In search of truth: Evaluating concordance of AI-based anatomy segmentation models | Journal of Medical Imaging (SPIE) 13(06), 062204; arXiv 2512 |

### New benchmark papers (n=12) (n=12)

| # | paper_id | Year | Title | Venue |
|---|---------|------|-------|-------|
| 1 | `10.1002_mp.16197` | 2023 | HaN-Seg: The head and neck organ-at-risk CT and MR segmentation dataset | Medical Physics |
| 2 | `10.1016_j.dib.2026.112865` | 2026 | Not extractable — full text truncated/illegible (journal header only visible) | Data in Brief (Elsevier) |
| 3 | `10.1038_s41597-025-06473-9` | 2025 | A MultiRater MultiOrgan Abdominal CT Dataset for Calibration Analysis and Uncertainty Modeling  | Scientific Data (Nature) |
| 4 | `10.1038_s41598-025-26019-8` | 2025 | Deep learning for automatic segmentation of hepatocellular carcinoma in contrast enhanced CT sc | Scientific Reports |
| 5 | `1902.07880v1` | 2019 | Evaluation of Algorithms for Multi-Modality Whole Heart Segmentation: An Open-Access Grand Chal | arXiv (MMWHS challenge, MICCAI 2017) |
| 6 | `1912.01054v2` | 2021 | The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: R | Medical Image Analysis (arXiv:1912.01054v2) |
| 7 | `2007.15546v4` | 2022 | Comparative study of deep learning methods for the automatic segmentation of lung, lesion and l | arXiv eess.IV (icovid consortium; KU Leuven/VUB/KCL/imec/ico |
| 8 | `2206.08023v3` | 2022 | AMOS: A Large-Scale Abdominal Multi-Organ Benchmark for Versatile Medical Image Segmentation | arXiv (AMOS 2022 grand-challenge) |
| 9 | `2310.12646v1` | 2023 | TRUSTED: The Paired 3D Transabdominal Ultrasound and CT Human Data for Kidney Segmentation and  | arXiv |
| 10 | `2406.13674v1` | 2024 | Rethinking Abdominal Organ Segmentation (RAOS) in the clinical scenario: A robustness evaluatio | arXiv (MICCAI-style) |
| 11 | `2502.05330v1` | 2025 | Multi-Class Segmentation of Aortic Branches and Zones in Computed Tomography Angiography: The A | arXiv (AortaSeg24 MICCAI 2024 challenge summary; Elsevier-fo |
| 12 | `2603.18616v1` | 2026 | Benchmarking CNN-based Models against Transformer-based Models for Abdominal Multi-Organ Segmen | arXiv preprint 2603.18616v1 (MICCAI-style, FAU Erlangen-Nürn |

