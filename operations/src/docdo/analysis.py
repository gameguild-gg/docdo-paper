"""Descriptive statistics from included-studies data."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from . import config


def load_studies(path: Path | None = None) -> pd.DataFrame:
    """Load included studies CSV into a DataFrame."""
    if path is None:
        candidates = sorted(config.FINAL_DIR.glob("final_included_papers_*.csv"), reverse=True)
        if candidates:
            path = candidates[0]
        else:
            path = config.SUPPLEMENTARY_DIR / "S2_final_included_studies.csv"
    df = pd.read_csv(path)
    print(f"  Loaded {len(df)} studies from {path.name}")
    return df


def year_distribution(df: pd.DataFrame) -> dict[int, int]:
    return df["year"].value_counts().sort_index().to_dict()


def architecture_distribution(df: pd.DataFrame) -> dict[str, int]:
    col = "architecture_type" if "architecture_type" in df.columns else "architecture"
    if col not in df.columns:
        return {}
    return df[col].value_counts().to_dict()


def study_type_distribution(df: pd.DataFrame) -> dict[str, int]:
    if "study_type" not in df.columns:
        return {}
    return df["study_type"].value_counts().to_dict()


def performance_statistics(df: pd.DataFrame) -> dict[str, dict[str, float]]:
    """Compute Dice and HD95 statistics for method-type studies."""
    subset = df.copy()
    if "study_type" in subset.columns:
        subset = subset[subset["study_type"] == "method"]

    stats: dict[str, dict[str, float]] = {}
    for col_name, label in [("dice_reported", "dice"), ("hd95_reported", "hd95")]:
        if col_name not in subset.columns:
            continue
        vals = pd.to_numeric(subset[col_name], errors="coerce").dropna()
        if vals.empty:
            continue
        stats[label] = {
            "count": int(len(vals)),
            "mean": float(vals.mean()),
            "std": float(vals.std()),
            "min": float(vals.min()),
            "max": float(vals.max()),
            "median": float(vals.median()),
        }
    return stats


def organ_statistics(df: pd.DataFrame) -> dict[str, Any]:
    """Count organs across studies."""
    col = "organ_focus" if "organ_focus" in df.columns else "organs_segmented"
    if col not in df.columns:
        return {"unique_organs": 0, "top_organs": [], "multi_organ_studies": 0}

    all_organs: list[str] = []
    multi = 0
    for val in df[col].dropna():
        parts = [o.strip() for o in str(val).split(";")]
        all_organs.extend(parts)
        if len(parts) > 1:
            multi += 1

    counts = Counter(all_organs)
    return {
        "unique_organs": len(counts),
        "top_organs": counts.most_common(10),
        "multi_organ_studies": multi,
    }


def code_availability(df: pd.DataFrame) -> dict[str, Any]:
    """Compute code availability rate for method studies."""
    subset = df.copy()
    if "study_type" in subset.columns:
        subset = subset[subset["study_type"] == "method"]
    if "code_available" not in subset.columns:
        return {"code_available": 0, "total_methods": len(subset), "availability_rate": 0.0}

    available = (subset["code_available"].astype(str).str.lower() == "yes").sum()
    total = len(subset)
    return {
        "code_available": int(available),
        "total_methods": total,
        "availability_rate": available / total if total > 0 else 0.0,
    }


def compute_all(path: Path | None = None) -> dict[str, Any]:
    """Compute all statistics and return a summary dict."""
    df = load_studies(path)
    return {
        "total": len(df),
        "years": year_distribution(df),
        "architectures": architecture_distribution(df),
        "study_types": study_type_distribution(df),
        "performance": performance_statistics(df),
        "organs": organ_statistics(df),
        "code_availability": code_availability(df),
    }


def print_statistics(stats: dict[str, Any]) -> None:
    """Pretty-print a stats dict to stdout."""
    print("\n" + "=" * 60)
    print("INCLUDED STUDIES STATISTICS")
    print("=" * 60)

    if stats.get("years"):
        print("\n--- Year Distribution ---")
        for year, count in sorted(stats["years"].items()):
            print(f"  {year}: {count}")

    if stats.get("architectures"):
        print("\n--- Architecture Distribution ---")
        for arch, count in stats["architectures"].items():
            print(f"  {arch}: {count}")

    if stats.get("performance"):
        print("\n--- Performance Statistics ---")
        for metric, vals in stats["performance"].items():
            n = vals["count"]
            print(f"  {metric} (n={n}):")
            print(f"    Mean ± Std: {vals['mean']:.3f} ± {vals['std']:.3f}")
            print(f"    Range: [{vals['min']:.3f}, {vals['max']:.3f}]")
            print(f"    Median: {vals['median']:.3f}")

    if stats.get("organs"):
        org = stats["organs"]
        print(f"\n--- Organ Statistics ---")
        print(f"  Unique organs: {org['unique_organs']}")
        print(f"  Multi-organ studies: {org['multi_organ_studies']}")
        if org["top_organs"]:
            print("  Top 10:")
            for name, cnt in org["top_organs"]:
                print(f"    {name}: {cnt}")

    if stats.get("code_availability"):
        ca = stats["code_availability"]
        print(f"\n--- Code Availability ---")
        print(f"  {ca['code_available']}/{ca['total_methods']} ({ca['availability_rate']:.1%})")

    print("\n" + "=" * 60)


def export_latex_year_table(stats: dict[str, Any], output_dir: Path) -> None:
    """Export year distribution as a LaTeX table."""
    output_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{tabular}{lr}",
        "\\toprule",
        "Year & Count \\\\",
        "\\midrule",
    ]
    for year, count in sorted(stats["years"].items()):
        lines.append(f"{year} & {count} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    (output_dir / "year_distribution.tex").write_text("\n".join(lines), encoding="utf-8")
