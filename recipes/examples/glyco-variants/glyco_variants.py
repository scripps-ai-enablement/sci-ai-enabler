#!/usr/bin/env python3
"""Interpret variants that gain or lose glycosylation sites — reproducible artifact.

Reference *artifact* for the recipe "Interpret variants that gain or lose
glycosylation sites", regenerated to follow the recipe faithfully. The durable
record of an AI-assisted analysis is committed code + a pinned environment + a
provenance record — not a chat transcript.

Per variant (`UniProt, protein_change` — e.g. `P01008, N167S`):

  1. Pull the protein's GlyGen glycosylation sites (glycosite ground truth).
  2. Reconcile against the *canonical* UniProt sequence; if the stated wild-type
     residue does not match, refuse to classify (`unmapped`).
  3. Classify by an N-X-S/T sequon delta (X != P) + GlyGen O-glycosite loss:
     LOG / GOG / none.
  4. Join ClinVar significance + AlphaMissense pathogenicity from BioMCP's
     `predictions` section (MyVariant.info / dbNSFP).
  5. Rank GOG/LOG hits above `none` (unmapped last), and within that group by
     AlphaMissense pathogenicity then ClinVar significance — per the recipe.
     Emit `glyco_candidates.csv` (columns: uniprot, site, class, glygen_evidence,
     clinvar_significance, alphamissense, rank), `provenance.json`, and a
     schema-validated IEEE-2791 BioCompute Object (`glyco_run.bco.json`).

Modes:
  (default, offline)  Replay recorded fixtures/. Standard library only;
                      deterministic. The BCO is emitted with no deps; schema
                      validation runs only if `jsonschema` is importable.
  --live              Drive GlyGen MCP (streamable HTTP) + UniProt + the `biomcp`
                      CLI (`biomcp mcp` for the MCP transport; here the CLI).

Note on the expression sanity-check (recipe step 3): it demotes candidates not
expressed in the tissue/disease context of interest. The demo input carries no
tissue context, so no expression-based demotion is applied; this is recorded in
provenance and the BCO rather than silently skipped.

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

SCRIPT_VERSION = "3.0.0"       # 3.x: recipe-faithful 7-column output + recipe ranking
GLYGEN_MCP_URL = "https://mcp.glygen.org/mcp"
SPEC_VERSION = "https://w3id.org/ieee/ieee-2791-schema/2791object.json"
ARTIFACT_BASE = ("https://github.com/scripps-ai-enablement/sci-ai-enabler/blob/main/"
                 "recipes/examples/glyco-variants")

CLASS_PRIORITY = {"GOG": 0, "LOG": 0, "none": 1, "unmapped": 2}
HGVSP_RE = re.compile(r"^p?\.?([A-Z])(\d+)([A-Z])$")
AM_LABEL = {"B": "Benign", "P": "Pathogenic", "A": "Ambiguous"}
# ClinVar significance -> severity (higher = more pathogenic), for the secondary sort.
CLINVAR_SEVERITY = {
    "pathogenic": 5, "likely pathogenic": 4, "pathogenic/likely pathogenic": 4,
    "uncertain significance": 3, "conflicting": 3,
    "likely benign": 2, "benign": 1, "benign/likely benign": 1,
}


# --------------------------------------------------------------------------- #
# Sequon classification — the scientific core. Pure functions, no I/O.
# --------------------------------------------------------------------------- #
def n_sequon_starts(seq: str) -> set[int]:
    """1-based Asn positions that start a valid N-X-[S/T] sequon (X != Pro)."""
    return {i + 1 for i in range(len(seq) - 2)
            if seq[i] == "N" and seq[i + 1] != "P" and seq[i + 2] in "ST"}


def classify(seq: str, sites: dict[int, str], wt: str, pos: int, mt: str) -> tuple[str, str]:
    if pos < 1 or pos > len(seq) or seq[pos - 1] != wt:
        found = seq[pos - 1] if 1 <= pos <= len(seq) else "N/A"
        return "unmapped", (f"UNMAPPED — canonical UniProt residue {pos} is {found}, not {wt}; "
                            "no frame reconciles it (flagged for manual review)")
    mutant = seq[: pos - 1] + mt + seq[pos:]
    wt_seq, mut_seq = n_sequon_starts(seq), n_sequon_starts(mutant)
    gained = sorted(p for p in (mut_seq - wt_seq) if pos - 2 <= p <= pos)
    lost = sorted(p for p in (wt_seq - mut_seq) if pos - 2 <= p <= pos)
    if gained:
        p = gained[0]
        tri = mutant[p - 1:p + 2]
        return "GOG", f"creates N-X-S/T sequon {tri[0]}{p}-{tri[1]}{p+1}-{tri[2]}{p+2} (de-novo, not a known GlyGen site)"
    if lost:
        p = lost[0]
        tag = "known GlyGen N-glycosite" if p in sites else "predicted sequon (not GlyGen-annotated)"
        return "LOG", f"destroys {tag} at Asn{p} (sequon {seq[p-1]}{p}-{seq[p]}{p+1}-{seq[p+1]}{p+2})"
    if pos in sites and sites[pos] in ("THR", "SER") and mt not in "ST":
        return "LOG", f"removes GlyGen O-glycosite ({sites[pos].title()}) at residue {pos}"
    return "none", "no known glycosite removed and no new N-X-S/T sequon created"


def alphamissense(bio: dict):
    """(prediction, score) for AlphaMissense from BioMCP's `predictions` section."""
    for p in bio.get("expanded_predictions") or []:
        if p.get("tool") == "AlphaMissense":
            return p.get("prediction") or "", p.get("score")
    return "", None


def am_display(pred: str, score) -> str:
    pred = AM_LABEL.get(pred, pred)
    if not pred:
        return ""
    return f"{pred} ({score:.3f})" if isinstance(score, (int, float)) else pred


def am_pathogenicity(pred: str, score) -> float:
    """Sort weight: higher = more pathogenic. AlphaMissense score if present."""
    if isinstance(score, (int, float)):
        return float(score)
    return {"Pathogenic": 1.0, "Ambiguous": 0.5, "Benign": 0.0}.get(AM_LABEL.get(pred, pred), -1.0)


def clinvar_severity(sig: str) -> int:
    return CLINVAR_SEVERITY.get((sig or "").strip().lower(), 0)


# --------------------------------------------------------------------------- #
# Loaders
# --------------------------------------------------------------------------- #
def read_fasta(path: Path) -> str:
    return "".join(l.strip() for l in path.read_text().splitlines() if not l.startswith(">"))


def glygen_sites_from(obj) -> dict[int, str]:
    return {s["start_pos"]: str(s["amino_acid"]).upper()[:3] for s in obj}


def load_offline(uniprot: str, change: str, fx: Path):
    seq = read_fasta(fx / "uniprot" / f"{uniprot}.fasta")
    sites = glygen_sites_from(json.loads((fx / "glygen" / f"glycosylation_sites_{uniprot}.json").read_text()))
    bp = fx / "biomcp" / f"{uniprot}_{change}.json"
    bio = json.loads(bp.read_text()) if bp.exists() else {}
    return seq, sites, (bio[0] if isinstance(bio, list) and bio else bio)


def glygen_release(fx: Path) -> dict:
    try:
        rel = json.loads((fx / "glygen" / "release_info.json").read_text())
        data = next((c for c in rel if c.get("component") == "data"), {})
        return {"data_version": data.get("version"), "data_release_date": data.get("release_date")}
    except Exception:
        return {}


def load_live(uniprot: str, gene: str, change: str):
    import requests
    seq = "".join(l.strip() for l in requests.get(
        f"https://rest.uniprot.org/uniprotkb/{uniprot}.fasta", timeout=30).text.splitlines()
        if not l.startswith(">"))
    sites = glygen_sites_from(_glygen_call("get_protein_glycosylation_sites", {"uniprot_ac": uniprot}))
    return seq, sites, _biomcp_variant(gene, change)


def _glygen_call(tool: str, args: dict):
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
    hit = _biomcp_json(["search", "variant", "--json", "--no-cache", "-g", gene, "--hgvsp", f"p.{change}", "--limit", "5"])
    results = hit.get("results", hit) if isinstance(hit, dict) else hit
    match = next((r for r in results if r.get("hgvs_p") in (f"p.{change}", change)), None)
    if not match:
        return {}
    got = _biomcp_json(["get", "variant", "--json", "--no-cache", match["id"], "predictions"])
    return got[0] if isinstance(got, list) and got else got


def _biomcp_json(args):
    out = subprocess.run(["biomcp", *args], capture_output=True, text=True, timeout=90)
    out.check_returncode()
    return json.loads(out.stdout or "{}")


# --------------------------------------------------------------------------- #
# IEEE-2791 BioCompute Object
# --------------------------------------------------------------------------- #
def _uri(u, filename=None):
    d = {"uri": u}
    if filename:
        d["filename"] = filename
    return d


def build_bco(rows: list[dict], release: dict, run_date: str) -> dict:
    when = f"{run_date}T00:00:00Z"
    n_hit = sum(1 for r in rows if r["class"] in ("GOG", "LOG"))
    bco = {
        "object_id": f"{ARTIFACT_BASE}/results/glyco_run.bco.json",
        "spec_version": SPEC_VERSION,
        "provenance_domain": {
            "name": "Interpret variants that gain or lose glycosylation sites — reference run",
            "version": SCRIPT_VERSION,
            "created": when, "modified": when,
            "contributors": [{
                "contribution": ["authoredBy", "createdWith"],
                "name": "Claude (Anthropic), driven by the sci-ai-enabler recipe "
                        "'interpret-glycosylation-altering-variants'",
            }],
            "license": "https://github.com/scripps-ai-enablement/sci-ai-enabler "
                       "(repository license unspecified as of run)",
        },
        "usability_domain": [
            "Flags protein-coding missense variants that create (GOG) or destroy (LOG) N-/O-linked "
            "glycosylation sites, joins ClinVar + AlphaMissense, and ranks candidates where altered "
            "glycosylation is a plausible disease mechanism.",
            f"Reference run over a {len(rows)}-variant SERPINC1/IFNGR2 panel; {n_hit} glycosylation-altering hits.",
        ],
        "description_domain": {
            "keywords": ["glycosylation", "N-linked", "O-linked", "sequon", "variant interpretation",
                         "gain of glycosylation", "loss of glycosylation", "GlyGen", "BioMCP", "ClinVar", "AlphaMissense"],
            "pipeline_steps": [
                {"step_number": 1, "name": "GlyGen glycosite lookup",
                 "description": "Retrieve annotated N-/O-glycosylation sites per protein from the GlyGen MCP server.",
                 "input_list": [_uri(GLYGEN_MCP_URL)], "output_list": [_uri(f"{ARTIFACT_BASE}/fixtures/glygen")]},
                {"step_number": 2, "name": "Canonical sequence fetch",
                 "description": "Fetch the canonical UniProt sequence for the sequon check and numbering reconciliation.",
                 "input_list": [_uri("https://rest.uniprot.org")], "output_list": [_uri(f"{ARTIFACT_BASE}/fixtures/uniprot")]},
                {"step_number": 3, "name": "Harmonize numbering + classify LOG/GOG",
                 "description": "Reconcile each variant against the canonical residue (else 'unmapped'), then classify by an N-X-S/T sequon delta and GlyGen O-glycosite loss.",
                 "input_list": [_uri(f"{ARTIFACT_BASE}/variants.csv", "variants.csv")],
                 "output_list": [_uri(f"{ARTIFACT_BASE}/results/glyco_candidates.csv", "glyco_candidates.csv")]},
                {"step_number": 4, "name": "Annotation join (BioMCP)",
                 "description": "Join ClinVar significance and AlphaMissense via the BioMCP variant getter's `predictions` section (MyVariant.info / dbNSFP).",
                 "input_list": [_uri("https://myvariant.info")], "output_list": [_uri(f"{ARTIFACT_BASE}/fixtures/biomcp")]},
                {"step_number": 5, "name": "Rank + report",
                 "description": "Rank GOG/LOG above none (unmapped last); within by AlphaMissense pathogenicity then ClinVar significance. Emit the candidate table.",
                 "input_list": [_uri(f"{ARTIFACT_BASE}/results/glyco_candidates.csv", "glyco_candidates.csv")],
                 "output_list": [_uri(f"{ARTIFACT_BASE}/results/glyco_candidates.csv", "glyco_candidates.csv")]},
            ],
        },
        "execution_domain": {
            "script": [{"uri": _uri(f"{ARTIFACT_BASE}/glyco_variants.py", "glyco_variants.py")}],
            "script_driver": "python",
            "software_prerequisites": [
                {"name": "python", "version": "3.12", "uri": _uri("https://www.python.org/")},
                {"name": "mcp", "version": "1.12.0", "uri": _uri("https://pypi.org/project/mcp/")},
                {"name": "requests", "version": "2.33.0", "uri": _uri("https://pypi.org/project/requests/")},
                {"name": "biomcp-cli", "version": "0.8.25", "uri": _uri("https://pypi.org/project/biomcp-cli/")},
            ],
            "external_data_endpoints": [
                {"name": "GlyGen MCP server", "url": GLYGEN_MCP_URL},
                {"name": "UniProt REST", "url": "https://rest.uniprot.org"},
                {"name": "MyVariant.info (via BioMCP)", "url": "https://myvariant.info"},
            ],
            "environment_variables": {},
        },
        "parametric_domain": [
            {"param": "n_glycosylation_sequon", "value": "N-X-[S/T], X != Pro", "step": "3"},
            {"param": "sequon_search_window", "value": "mutated residue +/- 2", "step": "3"},
            {"param": "ranking", "value": "GOG/LOG above none (unmapped last); within by AlphaMissense pathogenicity then ClinVar significance", "step": "5"},
            {"param": "expression_check", "value": "not applied — no tissue/disease context in the input", "step": "5"},
        ],
        "io_domain": {
            "input_subdomain": [
                {"uri": _uri(f"{ARTIFACT_BASE}/variants.csv", "variants.csv")},
                {"uri": _uri("https://data.glygen.org/GLY_001534", "GlyGen human germline mutation dataset (BCO)")},
                {"uri": _uri("https://data.glygen.org/GLY_001537", "GlyGen human cancer mutation dataset (BCO)")},
            ],
            "output_subdomain": [
                {"mediatype": "text/csv", "uri": _uri(f"{ARTIFACT_BASE}/results/glyco_candidates.csv", "glyco_candidates.csv")},
                {"mediatype": "application/json", "uri": _uri(f"{ARTIFACT_BASE}/results/provenance.json", "provenance.json")},
            ],
        },
        "error_domain": {
            "empirical_error": {},
            "algorithmic_error": {
                "scope": "single-residue missense only; indels, frameshift, splice and nonsense variants are not classified",
                "expression_check": "recipe step 3 (demote candidates not expressed in the tissue of interest) is inert here — no tissue/disease context supplied",
                "ranking": "a triage heuristic (AlphaMissense pathogenicity + ClinVar), not a validated pathogenicity score",
                "numbering": "variants whose stated wild-type residue does not match the canonical UniProt residue are reported as 'unmapped' rather than classified",
            },
        },
    }
    if release.get("data_version"):
        bco["description_domain"]["xref"] = [{
            "namespace": "glygen.data.release", "name": "GlyGen data release",
            "ids": [release["data_version"]], "access_time": when,
        }]
    bco["etag"] = _etag(bco)
    return bco


def _etag(bco_without_etag: dict) -> str:
    payload = {k: v for k, v in bco_without_etag.items() if k != "etag"}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_bco(bco: dict, schema_dir: Path):
    try:
        import jsonschema
        from referencing import Registry, Resource
    except Exception as exc:  # pragma: no cover
        return None, [f"skipped ({exc}); install jsonschema + referencing to validate"]
    docs = [json.loads(p.read_text()) for p in sorted(schema_dir.glob("*.json"))]
    registry = Registry().with_resources([(d["$id"], Resource.from_contents(d)) for d in docs])
    main = next(d for d in docs if str(d["$id"]).endswith("2791object.json"))
    validator = jsonschema.validators.validator_for(main)(main, registry=registry)
    errors = [f"{list(e.path)}: {e.message}" for e in validator.iter_errors(bco)]
    return (len(errors) == 0), errors


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(variants_path: Path, fixtures: Path, outdir: Path, live: bool = False, run_date: str | None = None) -> dict:
    variants = list(csv.DictReader(variants_path.open()))
    release = glygen_release(fixtures)
    run_date = run_date or (release.get("data_release_date", "") or "")[:10] or "unknown"

    rows = []
    for v in variants:
        uniprot, gene, change = v["uniprot"].strip(), v["gene"].strip(), v["protein_change"].strip()
        m = HGVSP_RE.match(change)
        if not m:
            rows.append({"uniprot": uniprot, "site": change, "class": "unmapped",
                         "glygen_evidence": "unparseable protein change", "clinvar_significance": "not_evaluated",
                         "alphamissense": "", "_am": -1.0, "_cv": 0})
            continue
        wt, pos, mt = m.group(1), int(m.group(2)), m.group(3)
        seq, sites, bio = (load_live(uniprot, gene, change) if live else load_offline(uniprot, change, fixtures))
        cls, evidence = classify(seq, sites, wt, pos, mt)
        am_pred, am_score = alphamissense(bio)
        clinvar = bio.get("significance") or "not_provided"
        rows.append({
            "uniprot": uniprot, "site": change, "class": cls, "glygen_evidence": evidence,
            "clinvar_significance": clinvar, "alphamissense": am_display(am_pred, am_score),
            "_am": am_pathogenicity(am_pred, am_score), "_cv": clinvar_severity(clinvar),
        })

    # Recipe ranking: GOG/LOG above none (unmapped last); within group by
    # AlphaMissense pathogenicity, then ClinVar significance.
    rows.sort(key=lambda r: (CLASS_PRIORITY.get(r["class"], 3), -r["_am"], -r["_cv"], f'{r["uniprot"]}:{r["site"]}'))
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    outdir.mkdir(parents=True, exist_ok=True)
    cols = ["uniprot", "site", "class", "glygen_evidence", "clinvar_significance", "alphamissense", "rank"]
    out_csv = outdir / "glyco_candidates.csv"
    with out_csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})

    bco = build_bco(rows, release, run_date)
    bco_path = outdir / "glyco_run.bco.json"
    bco_path.write_text(json.dumps(bco, indent=2, sort_keys=True) + "\n")
    ok, errors = validate_bco(bco, fixtures / "ieee2791")

    provenance = {
        "analysis": "interpret-glycosylation-altering-variants",
        "script": "glyco_variants.py", "script_version": SCRIPT_VERSION,
        "run_date": run_date, "mode": "live" if live else "offline-replay",
        "ranking": "GOG/LOG above none (unmapped last); within by AlphaMissense pathogenicity then ClinVar significance",
        "expression_check": "not applied — no tissue/disease context supplied in the input",
        "sources": {
            "glygen_mcp": {"endpoint": GLYGEN_MCP_URL, **release},
            "uniprot": {"api": "https://rest.uniprot.org", "note": "canonical sequence, per-accession"},
            "biomcp": {"cli": "biomcp", "provides": ["ClinVar significance", "AlphaMissense"],
                       "note": "AlphaMissense from the `predictions` section (biomcp get variant <id> predictions)"},
        },
        "input_sha256": sha256(variants_path),
        "outputs": {out_csv.name: sha256(out_csv), bco_path.name: sha256(bco_path)},
        "biocompute_object": {"file": bco_path.name, "spec_version": SPEC_VERSION,
                              "object_id": bco["object_id"], "etag": bco["etag"],
                              "input_dataset_bcos": ["https://data.glygen.org/GLY_001534", "https://data.glygen.org/GLY_001537"]},
    }
    prov_path = outdir / "provenance.json"
    prov_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")

    hits = [r for r in rows if r["class"] in ("GOG", "LOG")]
    print(f"Wrote {out_csv} ({len(rows)} variants; {len(hits)} glycosylation-altering), {prov_path}, and {bco_path}")
    print("  " + ("BCO valid against IEEE-2791 schema" if ok
                  else "BCO INVALID:\n  " + "\n  ".join(errors) if ok is False
                  else f"BCO schema validation {errors[0]}"))
    for r in rows:
        print(f"  #{r['rank']} {r['uniprot']} {r['site']}: {r['class']} | ClinVar={r['clinvar_significance']} | AM={r['alphamissense']}")
    return {"provenance": provenance, "bco": bco, "bco_valid": ok, "bco_errors": errors, "rows": rows}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--variants", default="variants.csv", type=Path)
    ap.add_argument("--fixtures", default="fixtures", type=Path)
    ap.add_argument("--outdir", default="results", type=Path)
    ap.add_argument("--live", action="store_true", help="drive the real GlyGen MCP + UniProt + BioMCP")
    ap.add_argument("--run-date", default=None)
    args = ap.parse_args()
    res = run(args.variants, args.fixtures, args.outdir, live=args.live, run_date=args.run_date)
    return 0 if res["bco_valid"] in (True, None) else 1


if __name__ == "__main__":
    sys.exit(main())
