#!/usr/bin/env python3
"""Reproducible functional-enrichment analysis.

This is the reference *artifact* for the recipe
"Run functional enrichment on a gene list". The point of this file is the
point of the whole reproducibility doctrine: the durable, version-controlled
record of an analysis is **code**, not a chat transcript. An assistant (Claude)
may have authored or edited this script, but what you commit, cite, and re-run
is the script itself — together with a pinned environment (requirements.txt)
and a provenance record (provenance.json) that this script emits.

Two modes:

  --offline FIXTURE   Replay a recorded Enrichr response (fixtures/...json).
                      Pure standard library; no network; fully deterministic.
                      This is the path exercised by the test suite and the path
                      you use to prove the analysis reproduces.

  (default, online)   Call the real Enrichr API via the `gget` library, exactly
                      as the recipe describes. Requires `pip install -r
                      requirements.txt`. Records gget's version in provenance.

Determinism contract (offline mode): given the same gene list, libraries, and
fixture, every output byte is identical across runs and machines. No wall-clock
timestamps leak into the outputs — the analysis date is recorded explicitly via
--run-date (default: the snapshot date carried by the fixture).

Usage:
    python enrichment.py --offline fixtures/enrichr_response.json \
        --genes genes.txt --outdir results/enrichment

    python enrichment.py --genes genes.txt --outdir results/enrichment   # live
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

# The five Enrichr libraries this recipe runs by default.
DEFAULT_LIBRARIES = [
    "GO_Biological_Process_2023",
    "KEGG_2021_Human",
    "Reactome_2022",
    "MSigDB_Hallmark_2020",
    "DisGeNET",
]
TOP_N = 10                 # rows kept per library
SIG_THRESHOLD = 0.05       # adjusted-p cutoff used by the summary + grounding
SCRIPT_VERSION = "1.0.0"   # bump when the analysis logic changes


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_genes(path: Path) -> list[str]:
    """One symbol per line; comments (#) and blanks ignored. Deduped + sorted
    so the *input identity* (and its hash) is independent of paste order."""
    seen = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        sym = raw.strip().upper()
        if sym and not sym.startswith("#"):
            seen.add(sym)
    return sorted(seen)


def fetch_offline(fixture_path: Path) -> tuple[dict, dict]:
    """Return (results_by_library, source_metadata) from a recorded response."""
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    return payload["results"], payload["source"]


def fetch_online(genes: list[str], libraries: list[str]) -> tuple[dict, dict]:
    """Call the real Enrichr API via gget. Not exercised in CI (network)."""
    try:
        import gget  # noqa
    except ImportError:
        sys.exit("gget not installed. `pip install -r requirements.txt`, "
                 "or use --offline FIXTURE for the deterministic replay.")
    results: dict = {}
    for lib in libraries:
        df = gget.enrichr(genes, database=lib)  # pandas DataFrame
        rows = []
        for _, r in df.iterrows():
            rows.append({
                "term": str(r.get("path_name", r.get("rank"))),
                "adj_p_val": float(r["adj_p_val"]),
                "combined_score": float(r["combined_score"]),
                "overlapping_genes": list(r["overlapping_genes"]),
                "accession": str(r.get("path_name", "")),
            })
        results[lib] = rows
    source = {
        "provider": "Enrichr (live) via gget",
        "gget_version": getattr(gget, "__version__", "unknown"),
        "snapshot_date": None,   # live call: no snapshot
    }
    return results, source


def write_tables(results: dict, libraries: list[str], outdir: Path) -> list[Path]:
    """One CSV per library, rows sorted deterministically by (adj_p, term)."""
    written = []
    for lib in libraries:
        rows = sorted(
            results.get(lib, []),
            key=lambda r: (float(r["adj_p_val"]), r["term"]),
        )[:TOP_N]
        path = outdir / f"{lib}.csv"
        with path.open("w", encoding="utf-8", newline="\n") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(["rank", "term", "adj_p_val", "combined_score",
                        "overlapping_genes", "accession"])
            for i, r in enumerate(rows, 1):
                w.writerow([
                    i, r["term"], f"{float(r['adj_p_val']):.3e}",
                    f"{float(r['combined_score']):.4f}",
                    ";".join(r["overlapping_genes"]), r["accession"],
                ])
        written.append(path)
    return written


def write_summary(results: dict, libraries: list[str], outdir: Path,
                  run_date: str) -> Path:
    """Markdown synthesis that cites ONLY terms present (and significant) in the
    saved tables — the grounding rule the recipe insists on."""
    lines = [
        "# Functional enrichment — summary",
        "",
        f"Analysis date: {run_date}",
        f"Significance threshold: adjusted p < {SIG_THRESHOLD}",
        "",
        "Each statement below cites a term that appears in the corresponding "
        "CSV with an adjusted p-value under the threshold. Terms that do not "
        "clear the threshold are not named.",
        "",
    ]
    for lib in libraries:
        sig = [r for r in sorted(results.get(lib, []),
                                 key=lambda r: (float(r["adj_p_val"]), r["term"]))
               if float(r["adj_p_val"]) < SIG_THRESHOLD][:TOP_N]
        lines.append(f"## {lib}")
        if not sig:
            lines.append("No terms cleared the significance threshold.")
        else:
            top = sig[0]
            lines.append(
                f"Top term: **{top['term']}** "
                f"(adj p = {float(top['adj_p_val']):.3e}; "
                f"accession `{top['accession']}`). "
                f"{len(sig)} term(s) significant in total."
            )
        lines.append("")
    path = outdir / "SUMMARY.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_provenance(outdir: Path, *, genes: list[str], libraries: list[str],
                     source: dict, run_date: str, outputs: list[Path]) -> Path:
    """Emit provenance.json — the record that makes the run auditable. Holds
    everything needed to understand and re-attempt the analysis: code version,
    pinned-environment pointer, the external source + its snapshot date, the
    exact input (count + content hash), and a sha256 of every output file.
    Deterministic: contains no wall-clock time."""
    record = {
        "analysis": "functional-enrichment",
        "script": "enrichment.py",
        "script_version": SCRIPT_VERSION,
        "environment": "requirements.txt (pinned)",
        "run_date": run_date,
        "parameters": {
            "libraries": libraries,
            "top_n": TOP_N,
            "sig_threshold": SIG_THRESHOLD,
        },
        "input": {
            "n_genes": len(genes),
            "genes_sha256": sha256_text("\n".join(genes)),
        },
        "external_source": source,
        "outputs": {
            p.name: {"sha256": sha256_text(p.read_text(encoding="utf-8"))}
            for p in sorted(outputs, key=lambda p: p.name)
        },
    }
    path = outdir / "provenance.json"
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    return path


def run(genes_path: Path, outdir: Path, libraries: list[str],
        offline: Path | None, run_date: str | None) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    genes = load_genes(genes_path)
    if offline is not None:
        results, source = fetch_offline(offline)
        run_date = run_date or source.get("snapshot_date") or "unknown"
    else:
        results, source = fetch_online(genes, libraries)
        if run_date is None:
            sys.exit("Live runs require --run-date YYYY-MM-DD so the output is "
                     "stamped with a fixed, recorded analysis date.")
    tables = write_tables(results, libraries, outdir)
    summary = write_summary(results, libraries, outdir, run_date)
    prov = write_provenance(outdir, genes=genes, libraries=libraries,
                            source=source, run_date=run_date,
                            outputs=tables + [summary])
    return {"tables": tables, "summary": summary, "provenance": prov}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--genes", type=Path, required=True,
                    help="text file, one gene symbol per line")
    ap.add_argument("--outdir", type=Path, default=Path("results/enrichment"))
    ap.add_argument("--libraries", default=",".join(DEFAULT_LIBRARIES),
                    help="comma-separated Enrichr library names")
    ap.add_argument("--offline", type=Path, default=None,
                    help="replay a recorded Enrichr response (deterministic)")
    ap.add_argument("--run-date", default=None,
                    help="analysis date stamped into outputs (YYYY-MM-DD)")
    args = ap.parse_args(argv)
    libraries = [s.strip() for s in args.libraries.split(",") if s.strip()]
    out = run(args.genes, args.outdir, libraries, args.offline, args.run_date)
    print(f"Wrote {len(out['tables'])} tables, {out['summary'].name}, "
          f"and {out['provenance'].name} to {args.outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
