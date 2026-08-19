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
  4. Join AlphaMissense from EBI ProtVar, keyed by UniProt accession (one batched
     submission for the whole list), and ClinVar significance from BioMCP via the
     allele-specific rsID ProtVar returns, verified against the canonical change.
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
PROTVAR_API = "https://www.ebi.ac.uk/ProtVar/api"
AA3 = {"A": "Ala", "R": "Arg", "N": "Asn", "D": "Asp", "C": "Cys", "Q": "Gln", "E": "Glu",
       "G": "Gly", "H": "His", "I": "Ile", "L": "Leu", "K": "Lys", "M": "Met", "F": "Phe",
       "P": "Pro", "S": "Ser", "T": "Thr", "W": "Trp", "Y": "Tyr", "V": "Val"}
SPEC_VERSION = "https://w3id.org/ieee/ieee-2791-schema/2791object.json"
ARTIFACT_BASE = ("https://github.com/scripps-ai-enablement/sci-ai-enabler/blob/main/"
                 "recipes/examples/glyco-variants")

CLASS_PRIORITY = {"GOG": 0, "LOG": 0, "none": 1, "unmapped": 2}
HGVSP_RE = re.compile(r"^p?\.?([A-Z])(\d+)([A-Z])$")
# dbNSFP/BioMCP short codes and ProtVar's amClass both normalise to the same three labels.
AM_LABEL = {"B": "Benign", "P": "Pathogenic", "A": "Ambiguous",
            "BENIGN": "Benign", "PATHOGENIC": "Pathogenic", "AMBIGUOUS": "Ambiguous"}
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


def protvar_canonical(entry: dict) -> tuple[dict | None, list[str]]:
    """(canonical-isoform annotation, warnings) from one ProtVar /mapping input entry.

    ProtVar is keyed by UniProt accession, so the isoform flagged `canonical` is the one
    the analysis is about -- no positional guessing over dbNSFP's isoform-aligned arrays.
    Warnings are ProtVar's own reference-residue check, e.g. for `P01008 220 R C`:
    "User input reference amino acid (Arg) does not match the UniProt sequence (Lys) at
    position 220". A wild-type mismatch also makes the change non-SNV-reachable, so
    ProtVar enumerates every base of the codon: >1 derived variant is the same refusal.
    """
    warns = [m.get("text", "") for m in (entry.get("messages") or []) if m.get("type") == "WARN"]
    derived = entry.get("derivedGenomicVariants") or []
    if len(derived) != 1:
        warns.append(f"{len(derived)} derived genomic variants; not variant-specific")
    for gv in derived:
        for gene in gv.get("genes") or []:
            for iso in gene.get("isoforms") or []:
                if iso.get("canonical"):
                    return iso, warns
    return None, warns


def protvar_alphamissense(iso: dict | None) -> tuple[str, float | None]:
    am = (iso or {}).get("amScore") or {}
    return am.get("amClass") or "", am.get("amPathogenicity")


def protvar_clinvar(population: dict, alt1: str) -> tuple[str, str]:
    """(significance, rsid) for the specific alt residue -- ClinVar-sourced calls only.

    ProtVar's `clinicalSignificances` aggregates several sources; an Ensembl-only call is
    not a ClinVar submission. P01008 N167S is the trap: ProtVar reports Pathogenic with
    `sources: ["Ensembl"]` and no ClinVar xref, and MyVariant has no ClinVar record there
    -- rs121909570 marks the position, but N167T is the ClinVar allele, not N167S.
    """
    alt3 = AA3.get(alt1, alt1)
    for v in population.get("variants") or []:
        if v.get("alternativeSequence") != alt3:
            continue
        sig = next((c.get("type") for c in (v.get("clinicalSignificances") or [])
                    if "ClinVar" in (c.get("sources") or [])), "")
        if sig:
            rsid = next((x.get("id") for x in (v.get("xrefs") or []) if x.get("name") == "dbSNP"), "")
            return sig, rsid
    return "", ""


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


def protvar_entries(fx: Path, live: bool, variants: list[dict]) -> dict[str, dict]:
    """{"<ACC> <pos> <ref> <alt>": mapping entry} -- one batched call for the whole list."""
    if not live:
        batch = json.loads((fx / "protvar" / "mapping_batch.json").read_text())
    else:
        import requests
        lines = "\n".join(_protvar_key(v) for v in variants) + "\n"
        iid = requests.post(f"{PROTVAR_API}/input/text", data=lines.encode(),
                            headers={"Content-Type": "text/plain"}, timeout=90).json()["inputId"]
        batch = requests.get(f"{PROTVAR_API}/mapping/{iid}", params={"pageSize": 500}, timeout=180).json()
    return {e["inputStr"]: e for e in batch.get("content", {}).get("inputs", [])}


def protvar_population(fx: Path, live: bool, uniprot: str, pos: int) -> dict:
    if not live:
        fp = fx / "protvar" / f"population_{uniprot}_{pos}.json"
        return json.loads(fp.read_text()) if fp.exists() else {}
    import requests
    return requests.get(f"{PROTVAR_API}/population/{uniprot}/{pos}", timeout=90).json()


def _protvar_key(v: dict) -> str:
    m = HGVSP_RE.match(v["protein_change"].strip())
    wt, pos, mt = m.group(1), m.group(2), m.group(3)
    return f'{v["uniprot"].strip()} {pos} {wt} {mt}'


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
    return seq, sites, {}


def biomcp_clinvar(rsid: str, change: str, live: bool, fx: Path, uniprot: str) -> dict:
    """ClinVar record for an allele-specific rsID, verified against the canonical change.

    ProtVar supplies the rsID for the exact alt residue, but an rsID can still span several
    alleles at a position -- so the record is only used when its own `hgvs_p` agrees with the
    canonical protein change. That check is the point: it is what the old gene+hgvsp search
    could not do.
    """
    if not rsid:
        return {}
    if not live:
        fp = fx / "biomcp" / f"{uniprot}_{change}.json"
        rec = json.loads(fp.read_text()) if fp.exists() else {}
    else:
        rec = _biomcp_json(["get", "variant", "--json", "--no-cache", rsid, "all"])
    rec = rec[0] if isinstance(rec, list) and rec else rec
    if (rec or {}).get("hgvs_p", "").replace("p.", "") != change:
        print(f"  [warn] {rsid} returned {rec.get('hgvs_p') if rec else None}, not p.{change}; "
              "not using it for ClinVar", file=sys.stderr)
        return {}
    return rec


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
                 "description": ("Join AlphaMissense from ProtVar's canonical isoform (accession-keyed, batched) "
                                 "and ClinVar significance from BioMCP via ProtVar's allele-specific rsID, "
                                 "verified against the canonical protein change."),
                 "input_list": [_uri(PROTVAR_API), _uri("https://myvariant.info")],
                 "output_list": [_uri(f"{ARTIFACT_BASE}/fixtures/protvar"), _uri(f"{ARTIFACT_BASE}/fixtures/biomcp")]},
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
                {"name": "EBI ProtVar (AlphaMissense, accession-keyed)", "url": PROTVAR_API},
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
                # `filename` names the dataset file each GlyGen BCO distributes, so the
                # record keeps both the GLY_* identifier and the specific input file.
                {"uri": _uri("https://data.glygen.org/GLY_001534", "human_protein_mutation_germline_all.csv")},
                {"uri": _uri("https://data.glygen.org/GLY_001537", "human_protein_mutation_cancer_all.csv")},
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
                "variant_match_ambiguity": ("AlphaMissense is taken from ProtVar's canonical isoform for the "
                                            "accession under analysis, so it cannot drift onto another transcript's "
                                            "residue; a ProtVar reference-residue WARN, or a change that is not "
                                            "SNV-reachable, is refused as unmapped rather than annotated"),
                "clinvar_source_filter": ("ProtVar's clinicalSignificances aggregates several sources; only "
                                          "ClinVar-sourced calls are reported as ClinVar (an Ensembl-only call is "
                                          "not a ClinVar submission), and a BioMCP record is used only when its "
                                          "own hgvs_p matches the canonical change"),
                "alphamissense_coverage": ("AlphaMissense covers canonical isoforms; a variant on an accession it "
                                           "does not score returns no value rather than a substitute"),
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

    pv = protvar_entries(fixtures, live, variants)

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
        seq, sites, _ = (load_live(uniprot, gene, change) if live else load_offline(uniprot, change, fixtures))
        cls, evidence = classify(seq, sites, wt, pos, mt)

        # ProtVar resolves the variant against the *accession*, so the annotation join needs
        # no genomic coordinate and cannot drift onto another transcript's residue.
        iso, warns = protvar_canonical(pv.get(_protvar_key(v), {}))
        if warns:
            cls = "unmapped"
            evidence = "UNMAPPED — " + "; ".join(warns)
            rows.append({"uniprot": uniprot, "site": change, "class": cls,
                         "glygen_evidence": evidence, "clinvar_significance": "not_evaluated",
                         "alphamissense": "", "_am": -1.0, "_cv": 0})
            continue

        am_pred, am_score = protvar_alphamissense(iso)
        sig, rsid = protvar_clinvar(protvar_population(fixtures, live, uniprot, pos), mt)
        bio = biomcp_clinvar(rsid, change, live, fixtures, uniprot)
        clinvar = bio.get("significance") or sig or "not_in_ClinVar"
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
            "protvar": {"api": PROTVAR_API, "provides": ["AlphaMissense", "reference-residue check", "rsID"],
                        "note": ("accession-keyed: POST /input/text (batched) -> GET /mapping/{id}, "
                                 "AlphaMissense read from the isoform flagged canonical; "
                                 "GET /population/{acc}/{pos} for the allele's ClinVar call + rsID")},
            "biomcp": {"cli": "biomcp", "provides": ["ClinVar significance"],
                       "note": ("biomcp get variant <rsid> all, using ProtVar's allele-specific rsID; the record "
                                "is used only when its hgvs_p matches the canonical change")},
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
