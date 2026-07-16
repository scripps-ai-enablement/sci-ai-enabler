#!/usr/bin/env python3
"""Interpret variants that gain or lose glycosylation sites — reproducible artifact.

This is the reference *artifact* for the recipe
"Interpret variants that gain or lose glycosylation sites". The point of this
file is the point of the whole reproducibility doctrine: the durable,
version-controlled record of an AI-assisted analysis is **code plus a pinned
environment and a provenance record** — not a chat transcript. An assistant
(Claude) may have authored or edited this script, but what you commit, cite, and
re-run is this directory.

What it does, per variant (`UniProt, protein_change` — e.g. `P01008, N167S`):

  1. Pull the protein's GlyGen glycosylation sites (glycosite ground truth).
  2. Reconcile the variant against the *canonical* UniProt sequence. If the
     stated wild-type residue does not match the canonical residue at that
     position, refuse to classify and log the variant as `unmapped` (the
     numbering could not be harmonized — the recipe's central trap).
  3. Classify by an N-X-S/T sequon delta (X != P) between wild-type and mutant
     sequence, plus GlyGen O-glycosite annotation:
        LOG  — destroys an N-sequon / removes an annotated O-glycosite
        GOG  — creates a new N-sequon
        none — no change to a glycosylation site
  4. Join ClinVar significance + CADD/PolyPhen/SIFT from BioMCP (MyVariant.info).
  5. Rank glyco-altering hits above `none`/`unmapped`, and emit
     `glyco_candidates.csv` + `provenance.json`.

Two modes:

  (default, offline)  Replay the recorded fixtures/ responses. Pure standard
                      library; no network; fully deterministic. This is the path
                      the test suite exercises and the path you use to prove the
                      analysis reproduces.

  --live              Drive the real tools the recipe prescribes: the GlyGen MCP
                      server over streamable HTTP (via the `mcp` SDK), UniProt
                      FASTA over HTTPS, and the `biomcp` CLI for the variant
                      annotation join. Requires `pip install -r requirements.txt`
                      and `uv tool install biomcp-cli`.

Determinism contract (offline): given the same variants.csv and fixtures, every
output byte is identical across runs and machines. No wall-clock timestamp leaks
into the outputs — the analysis date is recorded explicitly via --run-date
(default: the GlyGen release date carried by the fixture).

Usage:
    python glyco_variants.py --variants variants.csv --outdir results
    python glyco_variants.py --variants variants.csv --outdir results --live
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_VERSION = "1.0.0"       # bump when the classification logic changes
GLYGEN_MCP_URL = "https://mcp.glygen.org/mcp"

# Class ranking: glycosylation-altering hits first, then non-hits, then unmapped.
CLASS_PRIORITY = {"GOG": 0, "LOG": 0, "none": 1, "unmapped": 2}

HGVSP_RE = re.compile(r"^p?\.?([A-Z])(\d+)([A-Z])$")  # accepts "N167S" or "p.N167S"


# --------------------------------------------------------------------------- #
# Sequon classification — the scientific core. Pure functions, no I/O.
# --------------------------------------------------------------------------- #
def n_sequon_starts(seq: str) -> set[int]:
    """1-based Asn positions that start a valid N-X-[S/T] sequon (X != Pro)."""
    return {
        i + 1
        for i in range(len(seq) - 2)
        if seq[i] == "N" and seq[i + 1] != "P" and seq[i + 2] in "ST"
    }


def classify(seq: str, sites: dict[int, str], wt: str, pos: int, mt: str) -> tuple[str, str]:
    """Return (class, mechanism) for a single missense change on `seq`.

    `sites` maps a 1-based position to its GlyGen-annotated residue type
    (e.g. "ASN", "THR", "SER").
    """
    if pos < 1 or pos > len(seq) or seq[pos - 1] != wt:
        found = seq[pos - 1] if 1 <= pos <= len(seq) else "N/A"
        return "unmapped", (
            f"canonical UniProt residue {pos} is {found}, not {wt}; "
            "numbering could not be reconciled — flagged for manual review"
        )
    mutant = seq[: pos - 1] + mt + seq[pos:]
    wt_seq, mut_seq = n_sequon_starts(seq), n_sequon_starts(mutant)
    # Only consider sequons whose 3-residue window overlaps the mutated residue.
    gained = sorted(p for p in (mut_seq - wt_seq) if pos - 2 <= p <= pos)
    lost = sorted(p for p in (wt_seq - mut_seq) if pos - 2 <= p <= pos)
    if gained:
        p = gained[0]
        return "GOG", f"creates N-X-S/T sequon {mutant[p - 1:p + 2]} at residue {p}"
    if lost:
        p = lost[0]
        tag = "GlyGen-annotated glycosite" if p in sites else "predicted sequon, not GlyGen-annotated"
        return "LOG", f"destroys N-X-S/T sequon at residue {p} [{tag}]"
    if pos in sites and sites[pos] in ("THR", "SER") and mt not in "ST":
        return "LOG", f"removes GlyGen O-glycosite ({sites[pos].title()}) at residue {pos}"
    return "none", "no change to an N- or O-glycosylation site"


def predictors_miss(cls: str, clinvar: str, cadd, polyphen: str) -> bool:
    """True when a glyco-altering variant is called benign by standard predictors.

    These are the highest-value candidates: the glycosylation mechanism explains
    pathogenicity that sequence-based predictors do not capture.
    """
    if cls not in ("GOG", "LOG"):
        return False
    benign_cadd = cadd is not None and cadd < 20
    benign_pph = (polyphen or "").lower().startswith("benign")
    return (clinvar or "").lower().startswith("pathogenic") and benign_cadd and benign_pph


# --------------------------------------------------------------------------- #
# Fixture (offline) loaders
# --------------------------------------------------------------------------- #
def read_fasta(path: Path) -> str:
    return "".join(l.strip() for l in path.read_text().splitlines() if not l.startswith(">"))


def glygen_sites_from(obj) -> dict[int, str]:
    return {s["start_pos"]: str(s["amino_acid"]).upper()[:3] for s in obj}


def load_offline(uniprot: str, change: str, fx: Path):
    seq = read_fasta(fx / "uniprot" / f"{uniprot}.fasta")
    sites = glygen_sites_from(json.loads((fx / "glygen" / f"glycosylation_sites_{uniprot}.json").read_text()))
    bio_path = fx / "biomcp" / f"{uniprot}_{change}.json"
    bio = json.loads(bio_path.read_text()) if bio_path.exists() else {}
    if isinstance(bio, list):
        bio = bio[0] if bio else {}
    return seq, sites, bio


def glygen_release(fx: Path) -> dict:
    try:
        rel = json.loads((fx / "glygen" / "release_info.json").read_text())
        data = next((c for c in rel if c.get("component") == "data"), {})
        return {"data_version": data.get("version"), "data_release_date": data.get("release_date")}
    except Exception:
        return {}


# --------------------------------------------------------------------------- #
# Live loaders — the real tools the recipe prescribes
# --------------------------------------------------------------------------- #
def load_live(uniprot: str, gene: str, change: str):
    import requests  # pinned in requirements.txt

    seq = "".join(
        l.strip()
        for l in requests.get(f"https://rest.uniprot.org/uniprotkb/{uniprot}.fasta", timeout=30)
        .text.splitlines()
        if not l.startswith(">")
    )
    sites = glygen_sites_from(_glygen_call("get_protein_glycosylation_sites", {"uniprot_ac": uniprot}))
    bio = _biomcp_variant(gene, change)
    return seq, sites, bio


def _glygen_call(tool: str, args: dict):
    """One synchronous GlyGen MCP tool call over streamable HTTP."""
    import asyncio

    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    async def _run():
        async with streamablehttp_client(GLYGEN_MCP_URL) as (r, w, _):
            async with ClientSession(r, w) as s:
                await s.initialize()
                res = await s.call_tool(tool, args)
                return json.loads(res.content[0].text) if res.content else None

    return asyncio.run(_run())


def _biomcp_variant(gene: str, change: str) -> dict:
    """BioMCP variant_searcher -> variant_getter, via the `biomcp` CLI."""
    hit = _biomcp_json(["search", "variant", "-g", gene, "--hgvsp", f"p.{change}", "--limit", "5"])
    results = hit.get("results", hit) if isinstance(hit, dict) else hit
    match = next((r for r in results if r.get("hgvs_p") in (f"p.{change}", change)), None)
    if not match:
        return {}
    got = _biomcp_json(["get", "variant", match["id"]])
    return got[0] if isinstance(got, list) and got else got


def _biomcp_json(args: list[str]) -> dict | list:
    out = subprocess.run(["biomcp", *args, "--json", "--no-cache"], capture_output=True, text=True, timeout=90)
    out.check_returncode()
    return json.loads(out.stdout or "{}")


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(variants_path: Path, fixtures: Path, outdir: Path, live: bool = False, run_date: str | None = None) -> dict:
    """Classify + rank every variant in `variants_path`; write outputs to `outdir`.

    Returns the provenance dict. Offline (live=False) is pure standard library
    and deterministic; the test suite drives this path.
    """
    variants = list(csv.DictReader(variants_path.open()))
    release = glygen_release(fixtures)
    run_date = run_date or (release.get("data_release_date", "") or "")[:10] or "unknown"

    rows = []
    for v in variants:
        uniprot, gene, change = v["uniprot"].strip(), v["gene"].strip(), v["protein_change"].strip()
        m = HGVSP_RE.match(change)
        if not m:
            rows.append({"uniprot": uniprot, "gene": gene, "protein_change": change,
                         "class": "unmapped", "mechanism": "unparseable protein change"})
            continue
        wt, pos, mt = m.group(1), int(m.group(2)), m.group(3)
        if live:
            seq, sites, bio = load_live(uniprot, gene, change)
        else:
            seq, sites, bio = load_offline(uniprot, change, fixtures)

        cls, mechanism = classify(seq, sites, wt, pos, mt)
        cadd = bio.get("cadd_score")
        rows.append({
            "uniprot": uniprot,
            "gene": gene,
            "protein_change": change,
            "rsid": bio.get("rsid") or "",
            "class": cls,
            "mechanism": mechanism,
            "clinvar_significance": bio.get("significance") or "not_provided",
            "cadd": cadd if cadd is not None else "",
            "polyphen": bio.get("polyphen_pred") or "",
            "sift": bio.get("sift_pred") or "",
            "predictors_miss_it": predictors_miss(cls, bio.get("significance") or "", cadd, bio.get("polyphen_pred") or ""),
        })

    # Deterministic rank: class priority, then predictors_miss (novel first),
    # then ClinVar pathogenic, then CADD desc, then a stable identifier.
    def sort_key(r):
        cadd = r.get("cadd")
        cadd = float(cadd) if cadd not in (None, "") else -1.0
        return (
            CLASS_PRIORITY.get(r["class"], 3),
            0 if r.get("predictors_miss_it") else 1,
            0 if str(r.get("clinvar_significance", "")).lower().startswith("pathogenic") else 1,
            -cadd,
            f'{r["uniprot"]}:{r["protein_change"]}',
        )

    rows.sort(key=sort_key)
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    outdir.mkdir(parents=True, exist_ok=True)
    cols = ["rank", "uniprot", "gene", "protein_change", "rsid", "class", "mechanism",
            "clinvar_significance", "cadd", "polyphen", "sift", "predictors_miss_it"]
    out_csv = outdir / "glyco_candidates.csv"
    with out_csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})

    provenance = {
        "analysis": "interpret-glycosylation-altering-variants",
        "script": "glyco_variants.py",
        "script_version": SCRIPT_VERSION,
        "run_date": run_date,
        "mode": "live" if live else "offline-replay",
        "sources": {
            "glygen_mcp": {"endpoint": GLYGEN_MCP_URL, **release},
            "uniprot": {"api": "https://rest.uniprot.org", "note": "canonical sequence, per-accession"},
            "biomcp": {"cli": "biomcp", "provides": ["ClinVar significance", "CADD", "PolyPhen-2", "SIFT"],
                       "note": "AlphaMissense is not surfaced by BioMCP's default variant payload"},
        },
        "input_sha256": sha256(variants_path),
        "outputs": {out_csv.name: sha256(out_csv)},
        "biocompute_object": {
            "note": "GlyGen publishes its source datasets as IEEE-2791 BioCompute Objects; "
                    "cite them as input provenance.",
            "input_dataset_bcos": ["https://data.glygen.org/GLY_001534", "https://data.glygen.org/GLY_001537"],
            "emit_bco": "optional — serialize this run as a schema-validated IEEE-2791 BCO if a downstream consumer requires it",
        },
    }
    prov_path = outdir / "provenance.json"
    prov_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")

    hits = [r for r in rows if r["class"] in ("GOG", "LOG")]
    print(f"Wrote {out_csv} ({len(rows)} variants; {len(hits)} glycosylation-altering) and {prov_path}")
    for r in rows:
        flag = "  <- predictors miss it" if r.get("predictors_miss_it") else ""
        print(f"  #{r['rank']} {r['gene']} {r['protein_change']}: {r['class']} — {r['mechanism']}{flag}")
    return provenance


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--variants", default="variants.csv", type=Path)
    ap.add_argument("--fixtures", default="fixtures", type=Path)
    ap.add_argument("--outdir", default="results", type=Path)
    ap.add_argument("--live", action="store_true", help="drive the real GlyGen MCP + UniProt + BioMCP")
    ap.add_argument("--run-date", default=None, help="analysis date recorded in provenance (default: GlyGen release date)")
    args = ap.parse_args()
    run(args.variants, args.fixtures, args.outdir, live=args.live, run_date=args.run_date)
    return 0


if __name__ == "__main__":
    sys.exit(main())
