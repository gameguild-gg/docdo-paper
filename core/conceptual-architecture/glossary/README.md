# Glossary — DocDo Systematic Review

Key terms and definitions used in this research project.

---

## Segmentation & Imaging

| Term | Definition |
|------|-----------|
| **3D Organ Segmentation** | Voxel-wise labeling of anatomical structures in volumetric medical images |
| **CT (Computed Tomography)** | X-ray based imaging modality producing 3D volumetric scans |
| **Dice Score (DSC)** | Overlap metric for segmentation quality: 2\|A∩B\| / (\|A\|+\|B\|), range [0,1] |
| **HD95 (Hausdorff Distance 95)** | 95th percentile of surface-to-surface distances between prediction and ground truth (mm) |
| **IoU (Intersection over Union)** | Overlap metric: \|A∩B\| / \|A∪B\|, also called Jaccard index |
| **Multi-organ segmentation** | Simultaneously segmenting multiple anatomical structures in a single scan |

## Deep Learning Architectures

| Term | Definition |
|------|-----------|
| **U-Net** | Encoder-decoder architecture with skip connections for biomedical image segmentation |
| **V-Net** | 3D extension of U-Net using volumetric convolutions and Dice loss |
| **nnU-Net** | Self-configuring framework that automatically adapts U-Net to new datasets |
| **Swin UNETR** | Transformer-based architecture combining Swin Transformer encoder with U-Net decoder |
| **Encoder-decoder** | Architecture pattern: encoder compresses input, decoder reconstructs spatial output |
| **Attention mechanism** | Learned weighting that highlights relevant spatial or channel features |

## Systematic Review Methodology

| Term | Definition |
|------|-----------|
| **PRISMA 2020** | Preferred Reporting Items for Systematic Reviews and Meta-Analyses — reporting guideline |
| **S1 Identification** | Initial database search and record collection |
| **S2 Screening** | Title/abstract screening against inclusion/exclusion criteria |
| **S3 Full-text review** | Full-text assessment of remaining papers |
| **Inclusion criteria (IC)** | Conditions a study must meet to be included (IC1–IC5) |
| **Exclusion criteria (EC)** | Conditions that exclude a study regardless of ICs (EC1–EC6) |
| **Unanimous voting** | Decision rule: INCLUDE only if all screening runs agree |
