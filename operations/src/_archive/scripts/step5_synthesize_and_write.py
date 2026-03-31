#!/usr/bin/env python3
"""
Step 5: Synthesize extracted data and generate LaTeX tables for the paper.
Extracts REAL DATA from 52 papers and creates publication-ready content.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
import re

REPO_ROOT = Path(__file__).parent.parent.parent
QA_RESULTS = REPO_ROOT / "data/processed/quality_assessment/qa_parsed_results_20260123_075645.json"
OUTPUT_DIR = REPO_ROOT / "data/processed/synthesis"

def load_data():
    """Load all extracted data from QA batch."""
    with open(QA_RESULTS, encoding='utf-8') as f:
        return json.load(f)

def extract_dice_score(val):
    """Extract numeric Dice score from various formats."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        # Convert 0-1 to percentage if needed
        return val if val > 1 else val * 100
    if isinstance(val, str):
        # Extract number from strings like "0.85", "85%", "0.85 ± 0.03"
        match = re.search(r'(\d+\.?\d*)', val)
        if match:
            num = float(match.group(1))
            return num if num > 1 else num * 100
    return None

def analyze_architectures(data):
    """Analyze architecture distributions."""
    arch_types = Counter()
    arch_names = Counter()
    innovations = []
    
    for paper in data:
        if 'error' in paper:
            continue
        detail = paper.get('detailed_extraction', {})
        method = detail.get('method', {})
        
        arch_type = method.get('architecture_type', 'Unknown')
        arch_name = method.get('architecture_name', 'Unknown')
        
        arch_types[arch_type] += 1
        
        # Normalize architecture names
        name_lower = arch_name.lower()
        if 'unet' in name_lower or 'u-net' in name_lower:
            if '3d' in name_lower:
                arch_names['3D U-Net variants'] += 1
            elif '2d' in name_lower:
                arch_names['2D U-Net variants'] += 1
            else:
                arch_names['U-Net variants'] += 1
        elif 'vnet' in name_lower or 'v-net' in name_lower:
            arch_names['V-Net variants'] += 1
        elif 'transformer' in name_lower or 'swin' in name_lower or 'unetr' in name_lower:
            arch_names['Transformer-based'] += 1
        elif 'resnet' in name_lower or 'residual' in name_lower:
            arch_names['ResNet-based'] += 1
        elif 'fcn' in name_lower:
            arch_names['FCN-based'] += 1
        else:
            arch_names['Other'] += 1
        
        # Collect innovations
        innov = method.get('key_innovations', [])
        if innov:
            innovations.extend(innov)
    
    return arch_types, arch_names, innovations

def analyze_organs(data):
    """Analyze organ segmentation statistics."""
    organ_counts = Counter()
    multi_organ_count = 0
    single_organ_count = 0
    
    for paper in data:
        if 'error' in paper:
            continue
        detail = paper.get('detailed_extraction', {})
        organs = detail.get('organs', {})
        
        organ_list = organs.get('segmented_organs', [])
        if isinstance(organ_list, list):
            for org in organ_list:
                if org:
                    # Normalize organ names
                    org_lower = org.lower()
                    if 'liver' in org_lower:
                        organ_counts['Liver'] += 1
                    elif 'kidney' in org_lower:
                        organ_counts['Kidney'] += 1
                    elif 'spleen' in org_lower:
                        organ_counts['Spleen'] += 1
                    elif 'pancreas' in org_lower:
                        organ_counts['Pancreas'] += 1
                    elif 'lung' in org_lower:
                        organ_counts['Lung'] += 1
                    elif 'heart' in org_lower or 'cardiac' in org_lower:
                        organ_counts['Heart'] += 1
                    elif 'stomach' in org_lower:
                        organ_counts['Stomach'] += 1
                    elif 'gallbladder' in org_lower:
                        organ_counts['Gallbladder'] += 1
                    elif 'aorta' in org_lower:
                        organ_counts['Aorta'] += 1
                    elif 'bladder' in org_lower:
                        organ_counts['Bladder'] += 1
                    elif 'esophagus' in org_lower:
                        organ_counts['Esophagus'] += 1
                    elif 'adrenal' in org_lower:
                        organ_counts['Adrenal gland'] += 1
        
        is_multi = organs.get('multi_organ', False)
        if is_multi:
            multi_organ_count += 1
        else:
            single_organ_count += 1
    
    return organ_counts, multi_organ_count, single_organ_count

def analyze_datasets(data):
    """Analyze dataset usage."""
    dataset_counts = Counter()
    
    for paper in data:
        if 'error' in paper:
            continue
        detail = paper.get('detailed_extraction', {})
        dataset = detail.get('dataset', {})
        
        names = dataset.get('names', [])
        if isinstance(names, list):
            for name in names:
                if name:
                    name_lower = name.lower()
                    if 'lits' in name_lower or 'liver tumor' in name_lower:
                        dataset_counts['LiTS'] += 1
                    elif 'btcv' in name_lower or 'beyond the cranial' in name_lower:
                        dataset_counts['BTCV'] += 1
                    elif 'kits' in name_lower:
                        dataset_counts['KiTS'] += 1
                    elif 'amos' in name_lower:
                        dataset_counts['AMOS'] += 1
                    elif 'msd' in name_lower or 'decathlon' in name_lower:
                        dataset_counts['MSD'] += 1
                    elif 'miccai' in name_lower:
                        dataset_counts['MICCAI challenges'] += 1
                    elif 'tcia' in name_lower:
                        dataset_counts['TCIA'] += 1
                    elif 'institutional' in name_lower or 'private' in name_lower or 'clinical' in name_lower:
                        dataset_counts['Private/Institutional'] += 1
    
    return dataset_counts

def analyze_performance(data):
    """Extract performance metrics."""
    dice_scores = defaultdict(list)
    overall_dice = []
    
    for paper in data:
        if 'error' in paper:
            continue
        detail = paper.get('detailed_extraction', {})
        results = detail.get('results', {})
        
        # Overall Dice
        od = results.get('overall_dice')
        dice = extract_dice_score(od)
        if dice and dice > 0:
            overall_dice.append(dice)
        
        # Per-organ Dice
        dice_per_organ = results.get('dice_per_organ', {})
        if isinstance(dice_per_organ, dict):
            for organ, score in dice_per_organ.items():
                dice = extract_dice_score(score)
                if dice and dice > 0:
                    # Normalize organ name
                    org_lower = organ.lower()
                    if 'liver' in org_lower:
                        dice_scores['Liver'].append(dice)
                    elif 'kidney' in org_lower:
                        dice_scores['Kidney'].append(dice)
                    elif 'spleen' in org_lower:
                        dice_scores['Spleen'].append(dice)
                    elif 'pancreas' in org_lower:
                        dice_scores['Pancreas'].append(dice)
                    elif 'lung' in org_lower:
                        dice_scores['Lung'].append(dice)
                    elif 'stomach' in org_lower:
                        dice_scores['Stomach'].append(dice)
                    elif 'gallbladder' in org_lower:
                        dice_scores['Gallbladder'].append(dice)
                    elif 'aorta' in org_lower:
                        dice_scores['Aorta'].append(dice)
    
    return dict(dice_scores), overall_dice

def analyze_implementation(data):
    """Analyze implementation details."""
    frameworks = Counter()
    loss_functions = Counter()
    optimizers = Counter()
    has_3d = 0
    has_attention = 0
    
    for paper in data:
        if 'error' in paper:
            continue
        detail = paper.get('detailed_extraction', {})
        
        impl = detail.get('implementation', {})
        framework = impl.get('framework', '')
        if framework:
            fw_lower = framework.lower()
            if 'pytorch' in fw_lower:
                frameworks['PyTorch'] += 1
            elif 'tensorflow' in fw_lower or 'keras' in fw_lower:
                frameworks['TensorFlow/Keras'] += 1
            elif 'caffe' in fw_lower:
                frameworks['Caffe'] += 1
            else:
                frameworks['Other'] += 1
        
        method = detail.get('method', {})
        
        losses = method.get('loss_functions', [])
        if isinstance(losses, list):
            for loss in losses:
                if loss:
                    loss_lower = loss.lower()
                    if 'dice' in loss_lower:
                        loss_functions['Dice Loss'] += 1
                    if 'cross' in loss_lower or 'ce' in loss_lower:
                        loss_functions['Cross-Entropy'] += 1
                    if 'focal' in loss_lower:
                        loss_functions['Focal Loss'] += 1
                    if 'tversky' in loss_lower:
                        loss_functions['Tversky Loss'] += 1
                    if 'boundary' in loss_lower or 'hausdorff' in loss_lower:
                        loss_functions['Boundary Loss'] += 1
        
        opt = method.get('optimizer', '')
        if opt:
            opt_lower = opt.lower()
            if 'adam' in opt_lower:
                optimizers['Adam'] += 1
            elif 'sgd' in opt_lower:
                optimizers['SGD'] += 1
            elif 'rmsprop' in opt_lower:
                optimizers['RMSprop'] += 1
        
        if method.get('3d_processing'):
            has_3d += 1
        if method.get('attention_mechanism'):
            has_attention += 1
    
    return frameworks, loss_functions, optimizers, has_3d, has_attention

def generate_latex_tables(data, arch_types, arch_names, organ_counts, dataset_counts, 
                          dice_scores, overall_dice, frameworks, loss_functions):
    """Generate LaTeX tables for the paper."""
    
    latex = []
    
    # Table 1: Study Characteristics Summary
    latex.append(r"""
%==============================================================================
% AUTO-GENERATED SYNTHESIS TABLES FROM 52 INCLUDED STUDIES
%==============================================================================

% Table: Summary of Included Studies
\begin{table}[!htb]
\centering
\small
\caption{Summary Characteristics of 52 Included Studies}
\label{tab:study_characteristics}
\begin{tabular}{@{}lc@{}}
\toprule
\textbf{Characteristic} & \textbf{Count (\%)} \\
\midrule
\multicolumn{2}{@{}l}{\textit{Architecture Type}} \\
""")
    
    for arch, count in sorted(arch_types.items(), key=lambda x: -x[1]):
        pct = count / 52 * 100
        latex.append(f"\\quad {arch} & {count} ({pct:.1f}\\%) \\\\")
    
    latex.append(r"""
\midrule
\multicolumn{2}{@{}l}{\textit{Segmentation Scope}} \\
""")
    
    multi = sum(1 for p in data if p.get('detailed_extraction', {}).get('organs', {}).get('multi_organ'))
    single = 52 - multi
    latex.append(f"\\quad Multi-organ & {multi} ({multi/52*100:.1f}\\%) \\\\")
    latex.append(f"\\quad Single-organ & {single} ({single/52*100:.1f}\\%) \\\\")
    
    latex.append(r"""
\midrule
\multicolumn{2}{@{}l}{\textit{3D Processing}} \\
""")
    has_3d = sum(1 for p in data if p.get('detailed_extraction', {}).get('method', {}).get('3d_processing'))
    latex.append(f"\\quad True 3D & {has_3d} ({has_3d/52*100:.1f}\\%) \\\\")
    latex.append(f"\\quad 2D/2.5D & {52-has_3d} ({(52-has_3d)/52*100:.1f}\\%) \\\\")
    
    latex.append(r"""
\bottomrule
\end{tabular}
\end{table}
""")
    
    # Table 2: Architecture Distribution
    latex.append(r"""
\begin{table}[!htb]
\centering
\small
\caption{Architecture Categories in Reviewed Studies (n=52)}
\label{tab:architecture_distribution}
\begin{tabular}{@{}lcc@{}}
\toprule
\textbf{Architecture Family} & \textbf{Count} & \textbf{Percentage} \\
\midrule
""")
    
    for arch, count in sorted(arch_names.items(), key=lambda x: -x[1]):
        latex.append(f"{arch} & {count} & {count/52*100:.1f}\\% \\\\")
    
    latex.append(r"""
\bottomrule
\end{tabular}
\end{table}
""")
    
    # Table 3: Target Organs
    latex.append(r"""
\begin{table}[!htb]
\centering
\small
\caption{Frequency of Target Organs in Reviewed Studies}
\label{tab:organ_frequency}
\begin{tabular}{@{}lcc@{}}
\toprule
\textbf{Organ} & \textbf{Studies} & \textbf{Mean Dice (\%)} \\
\midrule
""")
    
    for organ, count in sorted(organ_counts.items(), key=lambda x: -x[1])[:12]:
        scores = dice_scores.get(organ, [])
        if scores:
            mean_dice = sum(scores) / len(scores)
            latex.append(f"{organ} & {count} & {mean_dice:.1f} \\\\")
        else:
            latex.append(f"{organ} & {count} & -- \\\\")
    
    latex.append(r"""
\bottomrule
\end{tabular}
\end{table}
""")
    
    # Table 4: Implementation Details
    latex.append(r"""
\begin{table}[!htb]
\centering
\small
\caption{Implementation Characteristics}
\label{tab:implementation}
\begin{tabular}{@{}lc|lc@{}}
\toprule
\textbf{Framework} & \textbf{Count} & \textbf{Loss Function} & \textbf{Count} \\
\midrule
""")
    
    fw_list = sorted(frameworks.items(), key=lambda x: -x[1])
    lf_list = sorted(loss_functions.items(), key=lambda x: -x[1])
    max_rows = max(len(fw_list), len(lf_list))
    
    for i in range(max_rows):
        fw = fw_list[i] if i < len(fw_list) else ('', '')
        lf = lf_list[i] if i < len(lf_list) else ('', '')
        latex.append(f"{fw[0]} & {fw[1] if fw[1] else ''} & {lf[0]} & {lf[1] if lf[1] else ''} \\\\")
    
    latex.append(r"""
\bottomrule
\end{tabular}
\end{table}
""")
    
    # Table 5: Per-Organ Dice Performance Summary
    latex.append(r"""
\begin{table*}[!htb]
\centering
\small
\caption{Per-Organ Dice Score Summary from Reviewed Studies (\%)}
\label{tab:dice_performance}
\begin{tabular}{@{}lccccc@{}}
\toprule
\textbf{Organ} & \textbf{Studies} & \textbf{Mean} & \textbf{Std} & \textbf{Min} & \textbf{Max} \\
\midrule
""")
    
    for organ in ['Liver', 'Kidney', 'Spleen', 'Pancreas', 'Lung', 'Stomach', 'Gallbladder', 'Aorta']:
        scores = dice_scores.get(organ, [])
        if len(scores) >= 3:
            mean = sum(scores) / len(scores)
            std = (sum((x - mean)**2 for x in scores) / len(scores)) ** 0.5
            latex.append(f"{organ} & {len(scores)} & {mean:.1f} & {std:.1f} & {min(scores):.1f} & {max(scores):.1f} \\\\")
    
    latex.append(r"""
\midrule
\textbf{Overall (all organs)} & """ + str(len(overall_dice)) + r""" & """ + 
f"{sum(overall_dice)/len(overall_dice):.1f}" if overall_dice else "--" + r""" & -- & -- & -- \\
\bottomrule
\end{tabular}
\end{table*}
""")
    
    return '\n'.join(latex)

def generate_findings_text(data, arch_types, arch_names, organ_counts, dice_scores, overall_dice):
    """Generate findings text for Results section."""
    
    total = 52
    
    # Architecture findings
    cnn_count = arch_types.get('CNN', 0)
    transformer_count = arch_types.get('Transformer', 0) + arch_types.get('Hybrid', 0)
    
    # Multi-organ stats
    multi = sum(1 for p in data if p.get('detailed_extraction', {}).get('organs', {}).get('multi_organ'))
    
    # 3D processing
    has_3d = sum(1 for p in data if p.get('detailed_extraction', {}).get('method', {}).get('3d_processing'))
    
    # Performance
    if overall_dice:
        mean_dice = sum(overall_dice) / len(overall_dice)
    else:
        mean_dice = 0
    
    text = f"""
%==============================================================================
% AUTO-GENERATED FINDINGS FROM SYNTHESIS
%==============================================================================

\\subsection{{Study Selection Results}}

Our systematic search identified 2,821 records after deduplication. Following Elasticsearch 
pre-filtering (n=638) and AI-assisted screening with strict consensus protocol, 52 studies 
met all inclusion criteria and were included in the final synthesis.

\\subsection{{Architectural Trends}}

Among the {total} included studies, convolutional neural networks (CNNs) dominated with 
{cnn_count} studies ({cnn_count/total*100:.1f}\\%), while transformer-based and hybrid 
architectures appeared in {transformer_count} studies ({transformer_count/total*100:.1f}\\%). 
The U-Net architecture and its variants remained the most prevalent, appearing in 
{arch_names.get('3D U-Net variants', 0) + arch_names.get('2D U-Net variants', 0) + arch_names.get('U-Net variants', 0)} 
studies ({(arch_names.get('3D U-Net variants', 0) + arch_names.get('2D U-Net variants', 0) + arch_names.get('U-Net variants', 0))/total*100:.1f}\\%).

True 3D volumetric processing was employed in {has_3d} studies ({has_3d/total*100:.1f}\\%), 
while the remaining {total-has_3d} studies used 2D or 2.5D approaches with post-hoc 
volume reconstruction.

\\subsection{{Target Organs}}

Multi-organ segmentation was addressed by {multi} studies ({multi/total*100:.1f}\\%), 
while {total-multi} studies focused on single-organ segmentation. The most frequently 
targeted organs were: {', '.join([f'{k} (n={v})' for k, v in sorted(organ_counts.items(), key=lambda x: -x[1])[:5]])}.

\\subsection{{Performance Summary}}

"""
    
    # Add per-organ performance
    for organ in ['Liver', 'Spleen', 'Kidney', 'Pancreas']:
        scores = dice_scores.get(organ, [])
        if len(scores) >= 3:
            mean = sum(scores) / len(scores)
            text += f"For {organ.lower()} segmentation, reported Dice scores ranged from {min(scores):.1f}\\% to {max(scores):.1f}\\% (mean: {mean:.1f}\\%). "
    
    return text

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Loading extracted data...")
    data = load_data()
    valid_data = [p for p in data if 'error' not in p]
    print(f"Loaded {len(data)} papers, {len(valid_data)} valid")
    
    print("\nAnalyzing architectures...")
    arch_types, arch_names, innovations = analyze_architectures(data)
    print(f"  Architecture types: {dict(arch_types)}")
    print(f"  Architecture families: {dict(arch_names)}")
    
    print("\nAnalyzing organs...")
    organ_counts, multi_count, single_count = analyze_organs(data)
    print(f"  Top organs: {dict(sorted(organ_counts.items(), key=lambda x: -x[1])[:5])}")
    print(f"  Multi-organ: {multi_count}, Single-organ: {single_count}")
    
    print("\nAnalyzing datasets...")
    dataset_counts = analyze_datasets(data)
    print(f"  Dataset usage: {dict(dataset_counts)}")
    
    print("\nAnalyzing performance...")
    dice_scores, overall_dice = analyze_performance(data)
    print(f"  Per-organ Dice scores collected for: {list(dice_scores.keys())}")
    if overall_dice:
        print(f"  Overall Dice: mean={sum(overall_dice)/len(overall_dice):.1f}%, n={len(overall_dice)}")
    
    print("\nAnalyzing implementation...")
    frameworks, loss_functions, optimizers, has_3d, has_attention = analyze_implementation(data)
    print(f"  Frameworks: {dict(frameworks)}")
    print(f"  Loss functions: {dict(loss_functions)}")
    print(f"  3D processing: {has_3d}, Attention: {has_attention}")
    
    print("\nGenerating LaTeX tables...")
    latex_tables = generate_latex_tables(
        data, arch_types, arch_names, organ_counts, dataset_counts,
        dice_scores, overall_dice, frameworks, loss_functions
    )
    
    tables_file = OUTPUT_DIR / f"synthesis_tables_{timestamp}.tex"
    with open(tables_file, 'w', encoding='utf-8') as f:
        f.write(latex_tables)
    print(f"Saved: {tables_file}")
    
    print("\nGenerating findings text...")
    findings = generate_findings_text(data, arch_types, arch_names, organ_counts, dice_scores, overall_dice)
    
    findings_file = OUTPUT_DIR / f"synthesis_findings_{timestamp}.tex"
    with open(findings_file, 'w', encoding='utf-8') as f:
        f.write(findings)
    print(f"Saved: {findings_file}")
    
    # Save summary JSON
    summary = {
        "total_studies": 52,
        "architecture_types": dict(arch_types),
        "architecture_families": dict(arch_names),
        "organ_counts": dict(organ_counts),
        "dataset_usage": dict(dataset_counts),
        "frameworks": dict(frameworks),
        "loss_functions": dict(loss_functions),
        "optimizers": dict(optimizers),
        "has_3d_processing": has_3d,
        "has_attention": has_attention,
        "multi_organ_studies": multi_count,
        "single_organ_studies": single_count,
        "dice_scores_per_organ": {k: {"n": len(v), "mean": sum(v)/len(v), "min": min(v), "max": max(v)} 
                                   for k, v in dice_scores.items() if len(v) >= 2},
        "overall_dice": {"n": len(overall_dice), "mean": sum(overall_dice)/len(overall_dice) if overall_dice else 0}
    }
    
    summary_file = OUTPUT_DIR / f"synthesis_summary_{timestamp}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print(f"Saved: {summary_file}")
    
    print("\n" + "="*60)
    print("SYNTHESIS COMPLETE")
    print("="*60)
    print(f"\nKey Statistics:")
    print(f"  Total studies: 52")
    print(f"  CNN-based: {arch_types.get('CNN', 0)}")
    print(f"  Multi-organ: {multi_count}")
    print(f"  3D processing: {has_3d}")
    print(f"  Top framework: {frameworks.most_common(1)[0] if frameworks else 'Unknown'}")
    print(f"  Top loss: {loss_functions.most_common(1)[0] if loss_functions else 'Unknown'}")
    
    print(f"\nGenerated files:")
    print(f"  - {tables_file}")
    print(f"  - {findings_file}")
    print(f"  - {summary_file}")

if __name__ == "__main__":
    main()
