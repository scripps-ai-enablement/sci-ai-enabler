#!/usr/bin/env python3
"""Interpret variants that gain or lose glycosylation sites — reproducible artifact.

Reference *artifact* for the recipe "Interpret variants that gain or lose
glycosylation sites". The durable record of an AI-assisted analysis is committed
code + a pinned environment + a provenance record — not a chat transcript. An
assistant (Claude) may author or edit this script; what you commit, cite, and
re-run is this directory.

Per variant (`UniProt, protein_change` — e.g. `P01008, N167S`):

  1. Pull the protein's GlyGen glycosylation sites (glycosite ground truth).
  2. Reconcile the variant against the *canonical* UniProt sequence; if the
     stated wild-type residue does not match, refuse to classify (`unmapped`).
  3. Classify by an N-X-S/T sequon delta (X != P) + GlyGen O-glycosite loss:
     LOG (destroys a site) / GOG (creates one) / none.
  4. Join ClinVar significance + CADD/PolyPhen/SIFT from BioMCP.
  5. Rank glyco-altering hits first; emit `glyco_candidates.csv`,
     `provenance.json`, and an **IEEE-2791 BioCompute Object**
     (`glyco_run.bco.json`), validated against the bundled 2791 JSON schema.

Modes:

  (default, offline)  Replay recorded fixtures/. Standard library only; no
                      network; deterministic. The BCO is still emitted (built
                      from the run); schema validation runs only if `jsonschema`
                      is importable, otherwise it is reported as skipped.
  --live              Drive the real tools: GlyGen MCP (streamable HTTP via the
                      `mcp` SDK), UniProt FASTA, and the `biomcp` CLI.

Determinism (offline): same variants.csv + fixtures => byte-identical
glyco_candidates.csv, provenance.json, and glyco_run.bco.json. The analysis date
is fixed via --run-date (default: the GlyGen release date from the fixture); no
wall-clock leaks into any output.

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

SCRIPT_VERSION = "2.0.0"       # 2.x: emits + validates an IEEE-2791 BCO
GLYGEN_MCP_URL = "https://mcp.glygen.org/mcp"
SPEC_VERSION = "https://w3id.org/ieee/ieee-2791-schema/2791object.json"
ARTIFACT_BASE = ("https://github.com/scripps-ai-enablement/sci-ai-enabler/blob/main/"
                 "recipes/examples/glyco-variants")

CLASS_PRIORITY = {"GOG": 0, "LOG": 0, "none": 1, "unmapped": 2}
HGVSP_RE = re.compile(r"^p?\.?([A-Z])(\d+)([A-Z])$")


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
        return "unmapped", (f"canonical UniProt residue {pos} is {found}, not {wt}; "
                            "numbering could not be reconciled — flagged for manual review")
    mutant = seq[: pos - 1] + mt + seq[pos:]
    wt_seq, mut_seq = n_sequon_starts(seq), n_sequon_starts(mutant)
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


def alphamissense(bio: dict):
    """(prediction, score) for AlphaMissense from BioMCP's `predictions` section.

    BioMCP's default variant view omits AlphaMissense; it lives in the expanded
    `predictions` section (dbNSFP via MyVariant.info). Returns ("", None) if absent.
    """
    for p in bio.get("expanded_predictions") or []:
        if p.get("tool") == "AlphaMissense":
            return p.get("prediction") or "", p.get("score")
    return "", None


def predictors_miss(cls: str, clinvar: str, cadd, polyphen: str, am_pred: str) -> bool:
    """A pathogenic glyco-altering variant that every sequence-based predictor
    (CADD, PolyPhen, and AlphaMissense) calls benign — the highest-value case."""
    if cls not in ("GOG", "LOG"):
        return False
    if not (clinvar or "").lower().startswith("pathogenic"):
        return False
    benign_cadd = cadd is not None and cadd < 20
    benign_pph = (polyphen or "").lower().startswith("benign")
    benign_am = (am_pred or "").lower().startswith("b")
    return benign_cadd and benign_pph and benign_am


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
    # The `predictions` section is a superset of the default view: the summary
    # fields (ClinVar/CADD/PolyPhen/SIFT) PLUS expanded_predictions incl.
    # AlphaMissense. Options must precede the ID; the section is a trailing arg.
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


def build_bco(rows: list[dict], release: dict, run_date: str, mode: str) -> dict:
    """Assemble an IEEE-2791 BioCompute Object describing this pipeline + run.

    `etag` is added last as a sha256 over the object with `etag` removed, so it
    is deterministic given the same inputs.
    """
    when = f"{run_date}T00:00:00Z"
    n_hit = sum(1 for r in rows if r.get("class") in ("GOG", "LOG"))
    bco = {
        "object_id": f"{ARTIFACT_BASE}/results/glyco_run.bco.json",
        "spec_version": SPEC_VERSION,
        "provenance_domain": {
            "name": "Interpret variants that gain or lose glycosylation sites — reference run",
            "version": SCRIPT_VERSION,
            "created": when,
            "modified": when,
            "contributors": [{
                "contribution": ["authoredBy", "createdWith"],
                "name": "Claude (Anthropic), driven by the sci-ai-enabler recipe "
                        "'interpret-glycosylation-altering-variants'",
            }],
            "license": "https://github.com/scripps-ai-enablement/sci-ai-enabler "
                       "(repository license unspecified as of run)",
        },
        "usability_domain": [
            "Flags protein-coding missense variants that create (gain of glycosylation, GOG) or "
            "destroy (loss of glycosylation, LOG) N-/O-linked glycosylation sites, joins ClinVar + "
            "CADD/PolyPhen/SIFT/AlphaMissense, and ranks candidates where altered glycosylation is a plausible "
            "disease mechanism — surfacing pathogenic variants that sequence-based predictors miss.",
            f"Reference run over a {len(rows)}-variant SERPINC1/IFNGR2 panel; "
            f"{n_hit} glycosylation-altering hits.",
        ],
        "description_domain": {
            "keywords": ["glycosylation", "N-linked", "O-linked", "sequon", "variant interpretation",
                         "gain of glycosylation", "loss of glycosylation", "GlyGen", "BioMCP", "ClinVar"],
            "pipeline_steps": [
                {"step_number": 1, "name": "GlyGen glycosite lookup",
                 "description": "Retrieve annotated N-/O-glycosylation sites per protein from the GlyGen MCP server.",
                 "input_list": [_uri(GLYGEN_MCP_URL)],
                 "output_list": [_uri(f"{ARTIFACT_BASE}/fixtures/glygen")]},
                {"step_number": 2, "name": "Canonical sequence fetch",
                 "description": "Fetch the canonical UniProt sequence for each accession (for the sequon check and numbering reconciliation).",
                 "input_list": [_uri("https://rest.uniprot.org")],
                 "output_list": [_uri(f"{ARTIFACT_BASE}/fixtures/uniprot")]},
                {"step_number": 3, "name": "Harmonize numbering + classify LOG/GOG",
                 "description": "Reconcile each variant against the canonical residue (else 'unmapped'), then classify by an N-X-S/T sequon delta and GlyGen O-glycosite loss.",
                 "input_list": [_uri(f"{ARTIFACT_BASE}/variants.csv", "variants.csv")],
                 "output_list": [_uri(f"{ARTIFACT_BASE}/results/glyco_candidates.csv", "glyco_candidates.csv")]},
                {"step_number": 4, "name": "Annotation join (BioMCP)",
                 "description": "Join ClinVar significance, CADD/PolyPhen/SIFT, and AlphaMissense via the BioMCP variant getter's `predictions` section (MyVariant.info / dbNSFP).",
                 "input_list": [_uri("https://myvariant.info")],
                 "output_list": [_uri(f"{ARTIFACT_BASE}/fixtures/biomcp")]},
                {"step_number": 5, "name": "Rank + report",
                 "description": "Rank glycosylation-altering hits first (predictor-discordant, then ClinVar-pathogenic, then CADD) and emit the candidate table.",
                 "input_list": [_uri(f"{ARTIFACT_BASE}/results/glyco_candidates.csv", "glyco_candidates.csv")],
                 "output_list": [_uri(f"{ARTIFACT_BASE}/results/glyco_candidates.csv", "glyco_candidates.csv")]},
            ],
        },
        "execution_domain": {
            "script": [_uri_wrap(f"{ARTIFACT_BASE}/glyco_variants.py", "glyco_variants.py")],
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
            {"param": "ranking", "value": "glyco-altering first; predictor-discordant; ClinVar pathogenic; CADD desc", "step": "5"},
        ],
        "io_domain": {
            "input_subdomain": [
                {"uri": _uri(f"{ARTIFACT_BASE}/variants.csv", "variants.csv")},
                {"uri": _uri("https://data.glygen.org/GLY_001534", "GlyGen human germline mutation dataset (BCO)")},
                {"uri": _uri("https://data.glygen.org/GLY_001537", "GlyGen human cancer mutation dataset (BCO)")},
            ],
            "output_subdomain": [
                {"mediatype": "text/csv",
                 "uri": _uri(f"{ARTIFACT_BASE}/results/glyco_candidates.csv", "glyco_candidates.csv")},
                {"mediatype": "application/json",
                 "uri": _uri(f"{ARTIFACT_BASE}/results/provenance.json", "provenance.json")},
            ],
        },
        "error_domain": {
            "empirical_error": {},
            "algorithmic_error": {
                "scope": "single-residue missense only; indels, frameshift, splice and nonsense variants are not classified",
                "ranking": "a triage heuristic that surfaces glycosylation-altering variants which sequence predictors (CADD/PolyPhen/SIFT/AlphaMissense) call benign; not a validated pathogenicity score",
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


def _uri_wrap(u, filename):
    # execution_domain.script items are {"uri": <uri-object>}
    return {"uri": _uri(u, filename)}


def _etag(bco_without_etag: dict) -> str:
    payload = {k: v for k, v in bco_without_etag.items() if k != "etag"}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_bco(bco: dict, schema_dir: Path):
    """Validate against the bundled IEEE-2791 schema. Returns (ok, errors).

    ok is None (with a note) if jsonschema/referencing are not installed — so the
    stdlib-only offline replay still runs; full validation happens when the
    pinned deps are present (live mode, or `pip install -r requirements.txt`).
    """
    try:
        import jsonschema
        from referencing import Registry, Resource
    except Exception as exc:  # pragma: no cover - exercised only without deps
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
            rows.append({"uniprot": uniprot, "gene": gene, "protein_change": change,
                         "class": "unmapped", "mechanism": "unparseable protein change"})
            continue
        wt, pos, mt = m.group(1), int(m.group(2)), m.group(3)
        seq, sites, bio = (load_live(uniprot, gene, change) if live
                           else load_offline(uniprot, change, fixtures))
        cls, mechanism = classify(seq, sites, wt, pos, mt)
        cadd = bio.get("cadd_score")
        am_pred, am_score = alphamissense(bio)
        rows.append({
            "uniprot": uniprot, "gene": gene, "protein_change": change,
            "rsid": bio.get("rsid") or "", "class": cls, "mechanism": mechanism,
            "clinvar_significance": bio.get("significance") or "not_provided",
            "cadd": cadd if cadd is not None else "",
            "polyphen": bio.get("polyphen_pred") or "", "sift": bio.get("sift_pred") or "",
            "alphamissense": am_pred, "alphamissense_score": am_score if am_score is not None else "",
            "predictors_miss_it": predictors_miss(cls, bio.get("significance") or "", cadd,
                                                  bio.get("polyphen_pred") or "", am_pred),
        })

    def sort_key(r):
        cadd = r.get("cadd")
        cadd = float(cadd) if cadd not in (None, "") else -1.0
        return (CLASS_PRIORITY.get(r["class"], 3),
                0 if r.get("predictors_miss_it") else 1,
                0 if str(r.get("clinvar_significance", "")).lower().startswith("pathogenic") else 1,
                -cadd, f'{r["uniprot"]}:{r["protein_change"]}')

    rows.sort(key=sort_key)
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    outdir.mkdir(parents=True, exist_ok=True)
    cols = ["rank", "uniprot", "gene", "protein_change", "rsid", "class", "mechanism",
            "clinvar_significance", "cadd", "polyphen", "sift", "alphamissense",
            "alphamissense_score", "predictors_miss_it"]
    out_csv = outdir / "glyco_candidates.csv"
    with out_csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})

    # IEEE-2791 BioCompute Object (required output).
    bco = build_bco(rows, release, run_date, "live" if live else "offline-replay")
    bco_path = outdir / "glyco_run.bco.json"
    bco_path.write_text(json.dumps(bco, indent=2, sort_keys=True) + "\n")
    ok, errors = validate_bco(bco, fixtures / "ieee2791")

    provenance = {
        "analysis": "interpret-glycosylation-altering-variants",
        "script": "glyco_variants.py", "script_version": SCRIPT_VERSION,
        "run_date": run_date, "mode": "live" if live else "offline-replay",
        "sources": {
            "glygen_mcp": {"endpoint": GLYGEN_MCP_URL, **release},
            "uniprot": {"api": "https://rest.uniprot.org", "note": "canonical sequence, per-accession"},
            "biomcp": {"cli": "biomcp", "provides": ["ClinVar significance", "CADD", "PolyPhen-2", "SIFT", "AlphaMissense"],
                       "note": "AlphaMissense comes from the `predictions` section (biomcp get variant <id> predictions)"},
        },
        "input_sha256": sha256(variants_path),
        "outputs": {out_csv.name: sha256(out_csv), bco_path.name: sha256(bco_path)},
        "biocompute_object": {
            "file": bco_path.name, "spec_version": SPEC_VERSION,
            "object_id": bco["object_id"], "etag": bco["etag"],
            "input_dataset_bcos": ["https://data.glygen.org/GLY_001534", "https://data.glygen.org/GLY_001537"],
        },
    }
    prov_path = outdir / "provenance.json"
    prov_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")

    hits = [r for r in rows if r["class"] in ("GOG", "LOG")]
    print(f"Wrote {out_csv} ({len(rows)} variants; {len(hits)} glycosylation-altering), "
          f"{prov_path}, and {bco_path}")
    verdict = ("BCO valid against IEEE-2791 schema" if ok
               else "BCO INVALID:\n  " + "\n  ".join(errors) if ok is False
               else f"BCO schema validation {errors[0]}")
    print(f"  {verdict}")
    for r in rows:
        flag = "  <- predictors miss it" if r.get("predictors_miss_it") else ""
        print(f"  #{r['rank']} {r['gene']} {r['protein_change']}: {r['class']} — {r['mechanism']}{flag}")
    return {"provenance": provenance, "bco": bco, "bco_valid": ok, "bco_errors": errors}


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
