"""Click-based CLI entry point for the docdo library."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from . import config


@click.group()
@click.version_option(package_name="docdo")
def main() -> None:
    """docdo — systematic review pipeline for 3D organ segmentation."""
    config.ensure_dirs()


# -------------------------------------------------------------------------
# Fetch
# -------------------------------------------------------------------------


@main.command()
@click.option("--query", default=None, help="PubMed search query (default: built-in).")
@click.option("--max-results", default=200, show_default=True, type=int)
@click.option("-o", "--output", type=click.Path(), default=None)
def fetch_pubmed(query: str | None, max_results: int, output: str | None) -> None:
    """Fetch papers from PubMed."""
    from .fetch import fetch_pubmed as _fetch, DEFAULT_PUBMED_QUERY

    q = query or DEFAULT_PUBMED_QUERY
    out = Path(output) if output else config.S1_RAW
    results = _fetch(q, max_results=max_results, output=out)
    click.echo(f"Fetched {len(results)} papers → {out}")


@main.command()
@click.option("-i", "--input", "input_csv", type=click.Path(exists=True), default=None)
@click.option("--pdf-dir", type=click.Path(), default=None)
def fetch_pdfs(input_csv: str | None, pdf_dir: str | None) -> None:
    """Download PDFs for included papers (arXiv + Unpaywall)."""
    from .fetch import fetch_pdfs as _fetch

    csv_path = Path(input_csv) if input_csv else None
    pd_path = Path(pdf_dir) if pdf_dir else None
    results = _fetch(csv_path, pdf_dir=pd_path)
    click.echo(
        f"Downloaded: {len(results['success'])}  "
        f"Existed: {len(results['already_exists'])}  "
        f"Failed: {len(results['failed'])}  "
        f"No ID: {len(results['no_identifier'])}"
    )


@main.command()
@click.argument("paywalled_csv", type=click.Path(exists=True))
@click.option("--pdf-dir", type=click.Path(), default=None)
def fetch_oa(paywalled_csv: str, pdf_dir: str | None) -> None:
    """Download PDFs from Open Access publishers."""
    from .fetch import fetch_oa_papers

    count = fetch_oa_papers(Path(paywalled_csv), pdf_dir=Path(pdf_dir) if pdf_dir else None)
    click.echo(f"Downloaded {count} OA papers")


# -------------------------------------------------------------------------
# Deduplicate
# -------------------------------------------------------------------------


@main.command()
@click.option("-i", "--input", "input_csv", type=click.Path(exists=True), default=None)
@click.option("-o", "--output", type=click.Path(), default=None)
def deduplicate(input_csv: str | None, output: str | None) -> None:
    """Deduplicate S1 search results by DOI and title."""
    from .dedup import deduplicate as _dedup

    inp = Path(input_csv) if input_csv else None
    out = Path(output) if output else None
    kept, removed = _dedup(inp, out)
    click.echo(f"Kept {kept}, removed {removed} duplicates")


# -------------------------------------------------------------------------
# Screen (synchronous)
# -------------------------------------------------------------------------


@main.command()
@click.option("-i", "--input", "input_csv", type=click.Path(exists=True), required=True)
@click.option("-o", "--output", type=click.Path(), required=True)
@click.option("--model", default=None, help="Override the screening model.")
@click.option("--num-runs", default=None, type=int)
@click.option("--limit", default=None, type=int, help="Max papers to screen.")
def screen(
    input_csv: str,
    output: str,
    model: str | None,
    num_runs: int | None,
    limit: int | None,
) -> None:
    """Screen papers synchronously (one-by-one, for small batches)."""
    from .io import read_csv, write_csv
    from .screening import screen_paper

    papers = read_csv(Path(input_csv))
    if limit:
        papers = papers[:limit]

    results = []
    for i, p in enumerate(papers, 1):
        title = p.get("title", "")
        abstract = p.get("abstract_snippet", "") or p.get("abstract", "")
        decision = screen_paper(title, abstract, model=model, num_runs=num_runs)
        row = {**p, **decision}
        results.append(row)
        click.echo(f"  [{i}/{len(papers)}] {decision['final_decision']} | {title[:50]}")

    write_csv(Path(output), results)
    inc = sum(1 for r in results if r["final_decision"] == "INCLUDE")
    click.echo(f"\nDone: {inc} INCLUDE / {len(results) - inc} EXCLUDE → {output}")


# -------------------------------------------------------------------------
# Screen (batch via OpenAI Batch API)
# -------------------------------------------------------------------------


@main.command()
@click.option("-i", "--input", "input_csv", type=click.Path(exists=True), required=True)
@click.option("-o", "--output-dir", type=click.Path(), default=None)
@click.option("--model", default=None)
@click.option("--num-runs", default=None, type=int)
def screen_batch(
    input_csv: str,
    output_dir: str | None,
    model: str | None,
    num_runs: int | None,
) -> None:
    """Submit a screening batch to the OpenAI Batch API."""
    from .io import read_csv, write_jsonl
    from .openai_utils import submit_batch
    from .screening import build_screening_batch_requests

    papers = read_csv(Path(input_csv))
    requests = build_screening_batch_requests(papers, model=model, num_runs=num_runs)

    out_dir = Path(output_dir) if output_dir else config.BATCH_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = out_dir / "screening_requests.jsonl"
    write_jsonl(jsonl_path, requests)

    batch_id = submit_batch(jsonl_path)
    click.echo(f"Batch submitted: {batch_id}")
    click.echo(f"  Requests: {len(requests)}")

    info = {"batch_id": batch_id, "requests": len(requests), "input": str(input_csv)}
    info_path = out_dir / f"batch_info_{batch_id}.json"
    info_path.write_text(json.dumps(info, indent=2), encoding="utf-8")


@main.command()
@click.argument("batch_id")
def check_batch(batch_id: str) -> None:
    """Check the status of a Batch API job."""
    from .openai_utils import check_batch as _check

    info = _check(batch_id)
    click.echo(json.dumps(info, indent=2))


@main.command()
@click.argument("batch_id")
@click.option("-o", "--output", type=click.Path(), default=None)
def download_batch(batch_id: str, output: str | None) -> None:
    """Download results from a completed batch."""
    from .openai_utils import download_batch_results

    out = Path(output) if output else config.BATCH_DIR / f"{batch_id}_output.jsonl"
    path = download_batch_results(batch_id, out)
    click.echo(f"Downloaded → {path}")


# -------------------------------------------------------------------------
# Compile final results (3-model consensus)
# -------------------------------------------------------------------------


@main.command()
@click.option("--strict-dir", type=click.Path(exists=True), default=None)
@click.option("--nano-dir", type=click.Path(exists=True), default=None)
@click.option("--gpt52-dir", type=click.Path(exists=True), default=None)
@click.option("-o", "--output-dir", type=click.Path(), default=None)
def compile(
    strict_dir: str | None,
    nano_dir: str | None,
    gpt52_dir: str | None,
    output_dir: str | None,
) -> None:
    """Compile 3-model consensus screening results."""
    from datetime import datetime

    from .io import read_csv, read_jsonl
    from .openai_utils import extract_batch_content
    from .screening import parse_screening_batch_results, unanimous_vote

    out_dir = Path(output_dir) if output_dir else config.FINAL_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    click.echo("Loading paper metadata...")
    meta_path = config.S2_ES_FILTERED
    papers = {
        (r.get("doi") or r.get("id") or r.get("title", "")[:50]).strip(): r
        for r in read_csv(meta_path)
    }
    click.echo(f"  {len(papers)} papers")

    # Helper: collect all output JSONL in a directory
    def _load_output_files(directory: Path | None) -> list[dict]:
        if directory is None:
            return []
        results = []
        for fp in sorted(directory.glob("*_output.jsonl")):
            results.extend(read_jsonl(fp))
        return results

    strict_results = _load_output_files(Path(strict_dir) if strict_dir else config.BATCH_DIR / "strict")
    nano_results = _load_output_files(Path(nano_dir) if nano_dir else config.BATCH_DIR / "nano")
    gpt52_results = _load_output_files(Path(gpt52_dir) if gpt52_dir else config.BATCH_DIR / "gpt52")

    strict_d = parse_screening_batch_results(strict_results)
    nano_d = parse_screening_batch_results(nano_results)
    gpt52_parsed = parse_screening_batch_results(gpt52_results)

    # Apply unanimous voting per model
    strict_decisions: dict[str, str] = {}
    for pid, runs in strict_d.items():
        dec, _, _ = unanimous_vote(runs)
        strict_decisions[pid] = dec

    nano_decisions: dict[str, str] = {}
    for pid, runs in nano_d.items():
        dec, _, _ = unanimous_vote(runs)
        nano_decisions[pid] = dec

    gpt52_decisions: dict[str, str] = {}
    for pid, runs in gpt52_parsed.items():
        dec, _, _ = unanimous_vote(runs)
        gpt52_decisions[pid] = dec

    # 3-model consensus
    final: dict[str, str] = {}
    stats = {"agree_include": 0, "agree_exclude": 0, "tiebreaker_include": 0, "tiebreaker_exclude": 0}
    for pid in papers:
        s = strict_decisions.get(pid, "EXCLUDE")
        n = nano_decisions.get(pid, "EXCLUDE")
        if s == n:
            final[pid] = s
            stats["agree_include" if s == "INCLUDE" else "agree_exclude"] += 1
        else:
            tb = gpt52_decisions.get(pid, "EXCLUDE")
            final[pid] = tb
            stats["tiebreaker_include" if tb == "INCLUDE" else "tiebreaker_exclude"] += 1

    inc = sum(1 for v in final.values() if v == "INCLUDE")
    click.echo(f"\nFinal: {inc} INCLUDE / {len(final) - inc} EXCLUDE")
    click.echo(f"  Agree-include: {stats['agree_include']}")
    click.echo(f"  Agree-exclude: {stats['agree_exclude']}")
    click.echo(f"  Tiebreaker-include: {stats['tiebreaker_include']}")
    click.echo(f"  Tiebreaker-exclude: {stats['tiebreaker_exclude']}")

    # Write outputs
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    import csv as _csv

    with open(out_dir / f"final_screening_results_{ts}.csv", "w", newline="", encoding="utf-8") as f:
        w = _csv.writer(f)
        w.writerow(["paper_id", "title", "abstract_snippet", "strict", "nano", "gpt52", "final"])
        for pid, meta in papers.items():
            w.writerow([
                pid, meta.get("title", ""), meta.get("abstract_snippet", "")[:500],
                strict_decisions.get(pid, ""), nano_decisions.get(pid, ""),
                gpt52_decisions.get(pid, ""), final.get(pid, ""),
            ])

    with open(out_dir / f"final_included_papers_{ts}.csv", "w", newline="", encoding="utf-8") as f:
        w = _csv.writer(f)
        w.writerow(["paper_id", "title", "abstract_snippet"])
        for pid, meta in papers.items():
            if final.get(pid) == "INCLUDE":
                w.writerow([pid, meta.get("title", ""), meta.get("abstract_snippet", "")])

    click.echo(f"Wrote results to {out_dir}")


# -------------------------------------------------------------------------
# Verify
# -------------------------------------------------------------------------


@main.command()
@click.option("-i", "--input", "input_csv", type=click.Path(exists=True), default=None)
@click.option("--per-db", default=5, show_default=True, type=int)
def verify_dois(input_csv: str | None, per_db: int) -> None:
    """Verify a sample of DOIs resolve correctly."""
    from .verify import verify_doi_sample

    inp = Path(input_csv) if input_csv else None
    results = verify_doi_sample(inp, per_db=per_db)
    click.echo(f"Verified: {results['verified']}  Failed: {results['failed']}  Skipped: {results['skipped']}")


@main.command()
@click.option("--s1", type=click.Path(exists=True), default=None)
@click.option("--s2", type=click.Path(exists=True), default=None)
def verify_traceability(s1: str | None, s2: str | None) -> None:
    """Verify S2 studies are traceable to S1 search results."""
    from .verify import verify_traceability as _verify

    found, missing, level = _verify(
        Path(s1) if s1 else None,
        Path(s2) if s2 else None,
    )
    click.echo(f"Found: {found}  Missing: {missing}  Level: {level}")


# -------------------------------------------------------------------------
# Analysis
# -------------------------------------------------------------------------


@main.command()
@click.option("-i", "--input", "input_csv", type=click.Path(exists=True), default=None)
@click.option("--latex-dir", type=click.Path(), default=None, help="Export LaTeX tables.")
def stats(input_csv: str | None, latex_dir: str | None) -> None:
    """Compute descriptive statistics for included studies."""
    from .analysis import compute_all, export_latex_year_table, print_statistics

    path = Path(input_csv) if input_csv else None
    all_stats = compute_all(path)
    print_statistics(all_stats)

    if latex_dir:
        export_latex_year_table(all_stats, Path(latex_dir))
        click.echo(f"LaTeX tables → {latex_dir}")
