#!/usr/bin/env python3
"""
glyco_variants.py - classify missense variants by their effect on N-/O-glycosylation,
with an expression sanity-check, ClinVar/AlphaMissense join, and full run provenance.

Pipeline (see the BioCompute Object emitted at bco.json for the formal description):

  1. Parse the input variant list (uniprot, protein_change) and hash it.
  2. Resolve the canonical GlyGen protein (get_protein_summary) + sequence and pull
     known glycosites (get_site_summary / the protein-detail glycosylation block).
  3. Harmonize numbering. The input site frame may be *mature* (signal peptide
     stripped) while the GlyGen canonical frame is the full *precursor*. We reconcile
     per-variant by residue identity against candidate offsets {0, signal_peptide_len},
     the signal peptide taken from UniProt. Antithrombin Asn135(mature)==Asn167
     (precursor) is the canonical trap. A variant whose frame cannot be *uniquely*
     reconciled is refused (class="unmapped") and logged - never guessed.
  4. Classify:
       LOG  - mutation removes a residue in a known N-X-S/T sequon (the Asn, the +2
              Ser/Thr, or introduces Pro at X) or removes an annotated O-glycosite.
       GOG  - mutation creates a *new* N-X-S/T sequon absent in canonical (+/-2 window).
       none - neither.
  5. Expression sanity-check: does GlyGen (Bgee) report the protein expressed in the
     tissue context relevant to it (antithrombin -> liver/plasma; IFNGR2 -> lung/immune)?
     Source + snapshot date are recorded. Candidates lacking expression evidence are
     NOT dropped - they are ranked lower.
  6. Join ClinVar significance + AlphaMissense pathogenicity via BioMCP (MyVariant.info
     federates both). AlphaMissense is NOT in the getter's default view, so we request
     the `predictions` section. Lookups use the reconciled (precursor) frame.
  7. Rank and emit glyco_candidates.csv. Then emit provenance.json and an IEEE-2791
     BioCompute Object (bco.json), and validate the BCO against the published schema.

Ranking: GOG/LOG above none above unmapped; within class, expression evidence first
(context > broad > none), then AlphaMissense pathogenicity, then ClinVar significance.

Data paths (standalone; no MCP runtime required):
  GlyGen  REST : POST https://api.glygen.org/protein/detail/{ac}   (+ /misc/verlist)
  UniProt REST : GET  https://rest.uniprot.org/uniprotkb/{ac}.json (signal peptide)
  BioMCP  CLI  : biomcp get variant "GENE CHANGE" predictions --json
  MyVariant    : GET  https://myvariant.info/v1/metadata           (snapshot dates)

Usage:
  python3 glyco_variants.py                       # built-in 3 variants
  python3 glyco_variants.py --input variants.csv  # CSV rows: uniprot,protein_change
  python3 glyco_variants.py P01008,N135S P38484,T168N
  python3 glyco_variants.py --out glyco_candidates.csv --model-id claude-opus-4-8
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

GLYGEN_API_BASE = "https://api.glygen.org"
GLYGEN_DETAIL_URL = GLYGEN_API_BASE + "/protein/detail/{ac}"
GLYGEN_VERLIST_URL = GLYGEN_API_BASE + "/misc/verlist"
GLYGEN_MCP_ENDPOINT = "https://mcp.glygen.org/mcp"
UNIPROT_URL = "https://rest.uniprot.org/uniprotkb/{ac}.json?fields=ft_signal"
MYVARIANT_META_URL = "https://myvariant.info/v1/metadata"
HTTP_TIMEOUT = 45
HTTP_RETRIES = 2

# GlyGen source BioCompute Objects underlying the glycosylation dataset (cited in
# the BCO io_domain input provenance).
GLYGEN_SOURCE_BCOS = ["GLY_001534", "GLY_001537"]

# Release date of the GlyGen data component reported by get_release_info for the
# version below; used only when the live verlist head matches (else "unknown").
GLYGEN_KNOWN_RELEASE = {"2.11.1": "2026-05-04"}

DEFAULT_VARIANTS = [
    ("P01008", "N135S"),  # antithrombin: mature 135 -> precursor 167 (known N-site) => LOG
    ("P38484", "T168N"),  # IFNGR2: creates N168-S169-T170 sequon => GOG (ClinVar Pathogenic)
    ("P01008", "P305H"),  # antithrombin: precursor frame, no sequon change => none
]

# Relevant tissue context per protein for the expression sanity-check. Matching is
# case-insensitive substring against the GlyGen (Bgee) tissue-panel names.
EXPRESSION_CONTEXT = {
    "P01008": {  # antithrombin-III (SERPINC1)
        "context": "plasma / liver (coagulation)",
        "tissues": ["liver", "hepato", "blood", "plasma"],
        "note": "antithrombin is synthesized in hepatocytes and secreted into plasma",
    },
    "P38484": {  # IFN-gamma receptor 2 (IFNGR2)
        "context": "immune / lung (IFN-gamma immunity)",
        "tissues": ["lung", "blood", "spleen", "lymph", "immune", "bone marrow",
                    "thymus", "leukocyte", "macrophage"],
        "note": "IFNGR2 is broadly expressed; lung/immune compartments are relevant to "
                "IFN-gamma immunity and mycobacterial-disease susceptibility",
    },
}
PRESENT_LEVELS = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "ABSENT": 0}

AA3_TO_1 = {
    "Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C", "Gln": "Q",
    "Glu": "E", "Gly": "G", "His": "H", "Ile": "I", "Leu": "L", "Lys": "K",
    "Met": "M", "Phe": "F", "Pro": "P", "Ser": "S", "Thr": "T", "Trp": "W",
    "Tyr": "Y", "Val": "V", "Sec": "U", "Pyl": "O",
}
N_ANCHOR = "N"
O_HYDROXYL = ("S", "T")
CHANGE_RE = re.compile(r"^(?:p\.)?([A-Z][a-z]{2}|[A-Z])(\d+)([A-Z][a-z]{2}|[A-Z])$")

SCHEMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema", "ieee2791")


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #

def log(msg: str) -> None:
    print(msg, file=sys.stderr)


def to_one_letter(aa: str) -> str:
    if len(aa) == 3:
        return AA3_TO_1.get(aa.capitalize(), "?")
    return aa.upper()


def http_json(url: str, *, method: str = "GET", body: dict | None = None) -> dict | list:
    data = json.dumps(body or {}).encode() if method == "POST" else None
    headers = {"Accept": "application/json", "User-Agent": "glyco-variants/1.1"}
    if method == "POST":
        headers["Content-Type"] = "application/json"
    last_err: Exception | None = None
    for attempt in range(HTTP_RETRIES + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                return json.loads(resp.read().decode())
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_err = exc
            if attempt < HTTP_RETRIES:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"request failed: {url} :: {last_err}")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# Parsed variant + protein model
# --------------------------------------------------------------------------- #

@dataclass
class Variant:
    uniprot: str
    raw_change: str
    wt: str = ""
    pos: int = 0
    mut: str = ""
    ok: bool = False
    parse_error: str = ""

    @classmethod
    def parse(cls, uniprot: str, change: str) -> "Variant":
        v = cls(uniprot=uniprot.strip(), raw_change=change.strip())
        m = CHANGE_RE.match(v.raw_change)
        if not m:
            v.parse_error = f"unparseable protein_change '{change}'"
            return v
        v.wt = to_one_letter(m.group(1))
        v.pos = int(m.group(2))
        v.mut = to_one_letter(m.group(3))
        if "?" in (v.wt, v.mut):
            v.parse_error = f"unknown residue code in '{change}'"
            return v
        v.ok = True
        return v


@dataclass
class Expression:
    support: str = "unknown"   # context | broad | none | unknown
    summary: str = ""
    source: str = ""
    snapshot: str = ""


@dataclass
class Protein:
    uniprot: str
    canonical_ac: str
    gene: str
    sequence: str
    signal_len: int
    n_sites: set[int] = field(default_factory=set)
    o_sites: set[int] = field(default_factory=set)
    sequons: dict[int, tuple[int, int]] = field(default_factory=dict)
    glycan_counts: dict[int, int] = field(default_factory=dict)
    glytoucan_example: dict[int, str] = field(default_factory=dict)
    tissues: list[tuple[str, str, str]] = field(default_factory=list)  # (name, present, score)
    expression: Expression = field(default_factory=Expression)

    def res(self, pos: int) -> str:
        if 1 <= pos <= len(self.sequence):
            return self.sequence[pos - 1]
        return ""


# --------------------------------------------------------------------------- #
# GlyGen + UniProt resolution
# --------------------------------------------------------------------------- #

def fetch_protein(uniprot: str, glygen_version: str, glygen_release: str) -> Protein:
    canonical_ac = uniprot if "-" in uniprot else f"{uniprot}-1"
    detail = http_json(GLYGEN_DETAIL_URL.format(ac=canonical_ac), method="POST", body={})
    if not isinstance(detail, dict) or "sequence" not in detail:
        raise RuntimeError(f"GlyGen returned no detail for {canonical_ac}")

    sequence = detail["sequence"]["sequence"]
    gene = ""
    gnames = detail.get("gene_names") or detail.get("gene") or []
    if isinstance(gnames, list):
        rec = next((g for g in gnames if g.get("type") == "recommended"), None) or (gnames[0] if gnames else None)
        if rec:
            gene = rec.get("name", "")
    elif isinstance(gnames, dict):
        gene = gnames.get("name", "")

    prot = Protein(
        uniprot=uniprot,
        canonical_ac=detail.get("uniprot", {}).get("uniprot_canonical_ac", canonical_ac),
        gene=gene,
        sequence=sequence,
        signal_len=fetch_signal_len(uniprot),
    )

    feats = detail.get("sequence_features", {}) or {}
    prot.n_sites = {int(p) for p in feats.get("n_linked_sites", [])}
    prot.o_sites = {int(p) for p in feats.get("o_linked_sites", [])}
    for span in feats.get("sequon_annotation_sites", []):
        prot.sequons[int(span["start_pos"])] = (int(span["start_pos"]), int(span["end_pos"]))

    for row in detail.get("glycosylation", []) or []:
        pos = row.get("start_pos")
        if pos is None:
            continue
        pos = int(pos)
        aa1 = to_one_letter(row.get("start_aa", ""))
        gtype = (row.get("type") or "").lower()
        if "n-linked" in gtype or aa1 == N_ANCHOR:
            prot.n_sites.add(pos)
        elif "o-linked" in gtype or aa1 in O_HYDROXYL:
            prot.o_sites.add(pos)
        gac = row.get("glytoucan_ac")
        if gac:
            prot.glycan_counts[pos] = prot.glycan_counts.get(pos, 0) + 1
            prot.glytoucan_example.setdefault(pos, gac)

    for p in prot.n_sites:
        if p in prot.sequons:
            continue
        if prot.res(p) == N_ANCHOR and prot.res(p + 1) != "P" and prot.res(p + 2) in O_HYDROXYL:
            prot.sequons[p] = (p, p + 2)

    # Expression panel (GlyGen expression_tissue, Bgee-sourced).
    for row in detail.get("expression_tissue", []) or []:
        t = row.get("tissue", {}) or {}
        name = t.get("name") or ""
        if name:
            prot.tissues.append((name, row.get("present") or "", str(row.get("score") or "")))
    prot.expression = check_expression(prot, uniprot, glygen_version, glygen_release)
    return prot


def fetch_signal_len(uniprot: str) -> int:
    try:
        data = http_json(UNIPROT_URL.format(ac=uniprot))
    except RuntimeError as exc:
        log(f"  [warn] UniProt signal-peptide lookup failed for {uniprot}: {exc}")
        return 0
    for feat in data.get("features", []):
        if feat.get("type") == "Signal":
            end = feat.get("location", {}).get("end", {}).get("value")
            if isinstance(end, int):
                return end
    return 0


def check_expression(prot: Protein, uniprot: str, glygen_version: str, glygen_release: str) -> Expression:
    """Is the protein expressed in its relevant tissue context (GlyGen/Bgee)?"""
    src = f"GlyGen expression_tissue (Bgee), data release {glygen_version}"
    snap = glygen_release
    if not prot.tissues:
        return Expression("none", "no GlyGen expression data available", src, snap)

    ctx = EXPRESSION_CONTEXT.get(uniprot)
    if ctx:
        matched = [
            (name, present, score) for (name, present, score) in prot.tissues
            if present != "ABSENT" and any(k in name.lower() for k in ctx["tissues"])
        ]
        if matched:
            best = max(matched, key=lambda m: PRESENT_LEVELS.get(m[1], 0))
            return Expression(
                "context",
                f"expressed in {ctx['context']}: {best[0]} = {best[1]} (Bgee score {best[2]}); {ctx['note']}",
                src, snap,
            )

    present_ct = sum(1 for _, p, _ in prot.tissues if p != "ABSENT")
    total = len(prot.tissues)
    ctx_label = f" (context '{ctx['context']}' tissue absent from Bgee panel)" if ctx else ""
    if present_ct / total >= 0.5:
        return Expression(
            "broad",
            f"broadly expressed: detected in {present_ct}/{total} Bgee panel tissues{ctx_label}",
            src, snap,
        )
    return Expression(
        "none",
        f"no expression in relevant context: detected in only {present_ct}/{total} Bgee panel tissues{ctx_label}",
        src, snap,
    )


# --------------------------------------------------------------------------- #
# Numbering reconciliation
# --------------------------------------------------------------------------- #

@dataclass
class Reconciled:
    ok: bool
    pos: int = 0
    frame: str = ""
    reason: str = ""


def reconcile_frame(prot: Protein, v: Variant) -> Reconciled:
    candidates = [0]
    if prot.signal_len > 0:
        candidates.append(prot.signal_len)
    hits = [d for d in candidates if prot.res(v.pos + d) == v.wt]
    if len(hits) == 1:
        d = hits[0]
        frame = "precursor(+0)" if d == 0 else f"mature(+{d} signal peptide)"
        return Reconciled(ok=True, pos=v.pos + d, frame=frame)
    if not hits:
        seen = {d: (prot.res(v.pos + d) or "-") for d in candidates}
        return Reconciled(False, reason=f"WT {v.wt}{v.pos} matches no candidate frame "
                                        f"(observed {seen} for offsets {candidates})")
    return Reconciled(False, reason=f"WT {v.wt}{v.pos} matches multiple frames {hits} ambiguously")


# --------------------------------------------------------------------------- #
# Classification
# --------------------------------------------------------------------------- #

@dataclass
class Classification:
    label: str
    evidence: str


def classify(prot: Protein, v: Variant, pos: int) -> Classification:
    log_reason = _check_log(prot, v, pos)
    if log_reason:
        return Classification("LOG", log_reason)
    gog_reason = _check_gog(prot, v, pos)
    if gog_reason:
        return Classification("GOG", gog_reason)
    return Classification("none", "no known glycosite lost and no new N-X-S/T sequon created")


def _glycan_note(prot: Protein, pos: int) -> str:
    n = prot.glycan_counts.get(pos, 0)
    if n:
        return f"{n} glycan(s) reported in GlyGen (e.g. {prot.glytoucan_example.get(pos)})"
    return "annotated site, no attached glycans reported in GlyGen"


def _check_log(prot: Protein, v: Variant, pos: int) -> str:
    if pos in prot.o_sites and v.wt in O_HYDROXYL and v.mut not in O_HYDROXYL:
        return f"removes O-glycosite {v.wt}{pos} ({_glycan_note(prot, pos)})"
    for anchor, (start, end) in prot.sequons.items():
        asn, x, hyd = anchor, anchor + 1, anchor + 2
        seq_str = f"N{asn}-{prot.res(x)}{x}-{prot.res(hyd)}{hyd}"
        if pos == asn and v.wt == N_ANCHOR and v.mut != N_ANCHOR:
            return f"removes Asn anchor of sequon {seq_str} ({_glycan_note(prot, asn)})"
        if pos == hyd and v.wt in O_HYDROXYL and v.mut not in O_HYDROXYL:
            return f"removes +2 Ser/Thr of sequon {seq_str}; abolishes N-glycosylation at N{asn}"
        if pos == x and v.mut == "P" and v.wt != "P":
            return f"introduces Pro at X of sequon {seq_str}; N-X-Pro blocks N-glycosylation at N{asn}"
    return ""


def _is_sequon(seq: str, i: int) -> bool:
    if i < 1 or i + 2 > len(seq):
        return False
    return seq[i - 1] == N_ANCHOR and seq[i] != "P" and seq[i + 1] in O_HYDROXYL


def _check_gog(prot: Protein, v: Variant, pos: int) -> str:
    seq = prot.sequence
    if pos < 1 or pos > len(seq) or seq[pos - 1] != v.wt:
        return ""
    mutated = seq[: pos - 1] + v.mut + seq[pos:]
    for anchor in (pos, pos - 1, pos - 2):
        if _is_sequon(mutated, anchor) and not _is_sequon(seq, anchor):
            asn, x, hyd = anchor, anchor + 1, anchor + 2
            new_seq = f"N{asn}-{mutated[x - 1]}{x}-{mutated[hyd - 1]}{hyd}"
            role = {pos: "new Asn anchor", pos - 1: "removes blocking residue at X",
                    pos - 2: "new +2 Ser/Thr"}[anchor]
            return f"creates N-X-S/T sequon {new_seq} ({role}); absent in canonical sequence"
    return ""


# --------------------------------------------------------------------------- #
# BioMCP variant annotation (ClinVar + AlphaMissense)
# --------------------------------------------------------------------------- #

@dataclass
class Annotation:
    clinvar: str = ""
    alphamissense: str = ""
    am_class: str = ""
    am_score: float = -1.0
    note: str = ""

_BIOMCP = shutil.which("biomcp")


def annotate_variant(gene: str, wt: str, pos: int, mut: str) -> Annotation:
    change = f"{wt}{pos}{mut}"
    if not _BIOMCP:
        return Annotation(note="biomcp CLI not found on PATH")
    try:
        proc = subprocess.run(
            [_BIOMCP, "get", "variant", f"{gene} {change}", "predictions", "--json"],
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return Annotation(note="biomcp timed out")
    if proc.returncode != 0:
        return Annotation(note=f"biomcp exit {proc.returncode}: {proc.stderr.strip()[:120]}")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return Annotation(note=f"no BioMCP/MyVariant record for {gene} {change}")
    if isinstance(data, list):
        data = data[0] if data else {}
    ann = Annotation()
    ann.clinvar = data.get("significance") or ""
    for pred in data.get("expanded_predictions", []) or []:
        if (pred.get("tool") or "").lower() == "alphamissense":
            ann.am_class = (pred.get("prediction") or "").lower()
            score = pred.get("score")
            ann.am_score = float(score) if isinstance(score, (int, float)) else -1.0
            ann.alphamissense = (f"{pred.get('prediction', '')}:{score}"
                                 if score is not None else pred.get("prediction", ""))
            break
    return ann


# --------------------------------------------------------------------------- #
# Ranking
# --------------------------------------------------------------------------- #

def _class_rank(label: str) -> int:
    return {"GOG": 0, "LOG": 0, "none": 1}.get(label, 2)


def _expr_rank(support: str) -> int:
    return {"context": 0, "broad": 1}.get(support, 2)  # none/unknown demoted


def _am_category(am_class: str, am_score: float = -1.0) -> int:
    c = (am_class or "").strip().lower()
    if "pathogenic" in c or c == "p":
        return 2
    if "ambiguous" in c or c == "a":
        return 1
    if "benign" in c or c == "b":
        return 0
    if am_score >= 0:  # AlphaMissense thresholds: <0.34 benign, 0.34-0.564 ambiguous, >0.564 pathogenic
        return 2 if am_score > 0.564 else 1 if am_score >= 0.34 else 0
    return -1


def _clinvar_rank(sig: str) -> int:
    s = (sig or "").lower()
    if not s:
        return -1
    if "pathogenic" in s:
        return 4 if "likely" in s else 5
    if "conflicting" in s or "uncertain" in s:
        return 2
    if "benign" in s:
        return 1 if "likely" in s else 0
    return 0


# --------------------------------------------------------------------------- #
# Row model + orchestration
# --------------------------------------------------------------------------- #

@dataclass
class Row:
    uniprot: str
    site: str
    cls: str
    evidence: str
    expression: str
    clinvar: str
    alphamissense: str
    _expr: int = 2
    _am_cat: int = -1
    _am_score: float = -1.0
    _cv: int = -1


def process(variants: list[tuple[str, str]], glygen_version: str, glygen_release: str) -> list[Row]:
    rows: list[Row] = []
    cache: dict[str, Protein] = {}
    for uniprot, change in variants:
        v = Variant.parse(uniprot, change)
        tag = f"{uniprot} {change}"
        if not v.ok:
            log(f"[unmapped] {tag}: {v.parse_error}")
            rows.append(Row(uniprot, change, "unmapped", v.parse_error, "", "", ""))
            continue

        if uniprot not in cache:
            try:
                cache[uniprot] = fetch_protein(uniprot, glygen_version, glygen_release)
                p = cache[uniprot]
                log(f"[glygen] {uniprot} -> {p.canonical_ac} ({p.gene}), len={len(p.sequence)}, "
                    f"signal={p.signal_len}, N-sites={sorted(p.n_sites)}, O-sites={sorted(p.o_sites)}")
                log(f"[expr]   {uniprot}: {p.expression.support} - {p.expression.summary}")
            except RuntimeError as exc:
                log(f"[unmapped] {tag}: GlyGen resolution failed: {exc}")
                rows.append(Row(uniprot, change, "unmapped", f"GlyGen error: {exc}", "", "", ""))
                continue
        prot = cache[uniprot]

        rec = reconcile_frame(prot, v)
        if not rec.ok:
            log(f"[unmapped] {tag}: {rec.reason}")
            rows.append(Row(uniprot, change, "unmapped", rec.reason,
                            f"{prot.expression.support}: {prot.expression.summary}", "", ""))
            continue

        canon_change = f"{v.wt}{rec.pos}{v.mut}"
        frame_note = f"input {v.raw_change} [{rec.frame}] -> canonical {canon_change}"
        log(f"[frame]  {tag}: {frame_note}")

        cl = classify(prot, v, rec.pos)
        ann = annotate_variant(prot.gene, v.wt, rec.pos, v.mut)
        if ann.note:
            log(f"[biomcp] {tag}: {ann.note}")
        log(f"[class]  {tag}: {cl.label}  clinvar={ann.clinvar or '-'}  "
            f"alphamissense={ann.alphamissense or '-'}")

        expr = prot.expression
        expr_cell = (f"{expr.support}: {expr.summary} "
                     f"[src: {expr.source}; snapshot {expr.snapshot}]")
        rows.append(Row(
            uniprot=uniprot,
            site=canon_change,
            cls=cl.label,
            evidence=f"{frame_note}; {cl.evidence}",
            expression=expr_cell,
            clinvar=ann.clinvar,
            alphamissense=ann.alphamissense,
            _expr=_expr_rank(expr.support),
            _am_cat=_am_category(ann.am_class, ann.am_score),
            _am_score=ann.am_score,
            _cv=_clinvar_rank(ann.clinvar),
        ))

    # class > expression > AlphaMissense (category, score) > ClinVar.
    rows.sort(key=lambda r: (_class_rank(r.cls), r._expr, -r._am_cat, -r._am_score, -r._cv))
    return rows


def write_csv(rows: list[Row], path: str) -> None:
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["uniprot", "site", "class", "glygen_evidence", "expression",
                    "clinvar_significance", "alphamissense", "rank"])
        for i, r in enumerate(rows, start=1):
            w.writerow([r.uniprot, r.site, r.cls, r.evidence, r.expression,
                        r.clinvar, r.alphamissense, i])


# --------------------------------------------------------------------------- #
# Run metadata (versions + snapshot dates)
# --------------------------------------------------------------------------- #

def fetch_glygen_version() -> tuple[str, str]:
    try:
        vl = http_json(GLYGEN_VERLIST_URL, method="POST", body={})
        version = vl[0] if isinstance(vl, list) and vl else "unknown"
    except RuntimeError:
        version = "unknown"
    return version, GLYGEN_KNOWN_RELEASE.get(version, "unknown")


def fetch_myvariant_meta() -> dict:
    try:
        m = http_json(MYVARIANT_META_URL)
    except RuntimeError as exc:
        return {"error": str(exc)}
    src = m.get("src", {})
    return {
        "clinvar_version": src.get("clinvar", {}).get("version"),
        "dbnsfp_version": src.get("dbnsfp", {}).get("version"),
        "build_date": m.get("build_date"),
    }


def biomcp_version() -> str:
    if not _BIOMCP:
        return "not-found"
    try:
        out = subprocess.run([_BIOMCP, "version"], capture_output=True, text=True, timeout=30).stdout
        return out.strip().splitlines()[0] if out.strip() else "unknown"
    except Exception:
        return "unknown"


def git_user() -> str:
    try:
        out = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, timeout=10).stdout
        return out.strip() or "unknown"
    except Exception:
        return "unknown"


# --------------------------------------------------------------------------- #
# provenance.json
# --------------------------------------------------------------------------- #

def build_provenance(*, run_iso: str, model_id: str, input_path: str, input_sha: str,
                     out_csv: str, bco_path: str, glygen_version: str, glygen_release: str,
                     mv: dict, biomcp_ver: str) -> dict:
    return {
        "run_date": run_iso,
        "model_id": model_id,
        "recipe": "glyco_variants (LOG/GOG glycosylation-impact classification)",
        "input_variant_file": {"path": os.path.basename(input_path), "sha256": input_sha},
        "data_sources": {
            "glygen": {
                "role": "canonical protein, glycosites/sequons, tissue expression (Bgee)",
                "data_version": glygen_version,
                "data_release_date": glygen_release,
                "mcp_endpoint": GLYGEN_MCP_ENDPOINT,
                "rest_api_base": GLYGEN_API_BASE,
                "source_bcos": [f"https://data.glygen.org/{b}" for b in GLYGEN_SOURCE_BCOS],
            },
            "uniprot": {
                "role": "signal-peptide length (mature->precursor offset for frame reconciliation)",
                "rest_api_base": "https://rest.uniprot.org",
            },
            "biomcp": {
                "role": "ClinVar significance + AlphaMissense pathogenicity join",
                "version": biomcp_ver,
                "mcp_transport": "stdio (`biomcp mcp`) / CLI `biomcp get variant ... predictions`",
                "federator": "MyVariant.info",
            },
        },
        "snapshots": {
            "clinvar": {
                "served_by": "MyVariant.info",
                "version": mv.get("clinvar_version"),
                "myvariant_build_date": mv.get("build_date"),
            },
            "alphamissense": {
                "served_by": "MyVariant.info",
                "via": f"dbNSFP {mv.get('dbnsfp_version')}",
                "myvariant_build_date": mv.get("build_date"),
                "note": "requested through the BioMCP `predictions` (expanded) view; "
                        "not present in the default getter view",
            },
        },
        "outputs": {
            "candidates_csv": os.path.basename(out_csv),
            "biocompute_object": os.path.basename(bco_path),
        },
    }


# --------------------------------------------------------------------------- #
# IEEE-2791 BioCompute Object
# --------------------------------------------------------------------------- #

def _uri(u: str, filename: str | None = None, access_time: str | None = None) -> dict:
    o = {"uri": u}
    if filename:
        o["filename"] = filename
    if access_time:
        o["access_time"] = access_time
    return o


def build_bco(*, run_iso: str, model_id: str, input_path: str, input_sha: str,
              out_csv: str, prov_path: str, bco_path: str, glygen_version: str,
              glygen_release: str, mv: dict, biomcp_ver: str, n_variants: int,
              contributor: str) -> dict:
    script_uri = "file://" + os.path.abspath(__file__)
    glygen_bco_uris = [f"https://data.glygen.org/{b}" for b in GLYGEN_SOURCE_BCOS]

    description_domain = {
        "keywords": ["glycosylation", "N-glycosylation sequon", "loss of glycosylation",
                     "gain of glycosylation", "GlyGen", "ClinVar", "AlphaMissense",
                     "variant effect", "antithrombin", "IFNGR2"],
        "pipeline_steps": [
            {
                "step_number": 1, "name": "Parse and hash input variants",
                "description": "Read (uniprot, protein_change) rows and record the SHA-256 of the input file.",
                "input_list": [_uri("file://" + os.path.abspath(input_path), os.path.basename(input_path))],
                "output_list": [_uri("urn:glyco:parsed-variants", "parsed_variants")],
            },
            {
                "step_number": 2, "name": "Resolve canonical GlyGen protein + glycosites",
                "description": "get_protein_summary + protein sequence and glycosylation block "
                               "(N-linked sequons, O-glycosites) for each UniProt accession.",
                "input_list": [_uri(GLYGEN_API_BASE + "/protein/detail/", access_time=run_iso)],
                "output_list": [_uri("urn:glyco:glygen-protein-model", "glygen_protein_model")],
            },
            {
                "step_number": 3, "name": "Reconcile numbering frame",
                "description": "Map input site onto the GlyGen canonical (precursor) frame by residue "
                               "identity against offsets {0, signal_peptide_length}; UniProt supplies "
                               "the signal peptide. Non-unique matches are refused as unmapped.",
                "input_list": [_uri("https://rest.uniprot.org", access_time=run_iso)],
                "output_list": [_uri("urn:glyco:reconciled-site", "reconciled_site")],
            },
            {
                "step_number": 4, "name": "Classify LOG/GOG/none",
                "description": "LOG if the mutation removes a residue in a known N-X-S/T sequon or an "
                               "annotated O-glycosite; GOG if it creates a new N-X-S/T sequon (+/-2 window) "
                               "absent in canonical; else none.",
                "input_list": [_uri("urn:glyco:reconciled-site", "reconciled_site")],
                "output_list": [_uri("urn:glyco:class", "glyco_class")],
            },
            {
                "step_number": 5, "name": "Expression sanity-check",
                "description": "GlyGen (Bgee) tissue expression vs the protein's relevant context; "
                               "candidates lacking in-context expression are demoted, not dropped.",
                "input_list": [_uri(GLYGEN_API_BASE + "/protein/detail/", access_time=run_iso)],
                "output_list": [_uri("urn:glyco:expression", "expression_support")],
            },
            {
                "step_number": 6, "name": "Join ClinVar + AlphaMissense",
                "description": "BioMCP `get variant \"GENE CHANGE\" predictions` (MyVariant.info) in the "
                               "reconciled precursor frame; AlphaMissense taken from the expanded predictions.",
                "input_list": [_uri("https://myvariant.info/v1/variant", access_time=run_iso)],
                "output_list": [_uri("urn:glyco:annotation", "clinvar_alphamissense")],
            },
            {
                "step_number": 7, "name": "Rank and emit outputs",
                "description": "Rank GOG/LOG > none > unmapped; within class by expression, then "
                               "AlphaMissense, then ClinVar. Emit CSV, provenance.json and this BCO.",
                "input_list": [_uri("urn:glyco:class", "glyco_class"),
                               _uri("urn:glyco:annotation", "clinvar_alphamissense")],
                "output_list": [_uri("file://" + os.path.abspath(out_csv), os.path.basename(out_csv))],
            },
        ],
    }

    execution_domain = {
        "script": [{"uri": _uri(script_uri, os.path.basename(__file__))}],
        "script_driver": "python3",
        "software_prerequisites": [
            {"name": "Python", "version": "3.9+", "uri": _uri("https://www.python.org/")},
            {"name": "biomcp-cli", "version": biomcp_ver.replace("biomcp ", "") or "0.8.25",
             "uri": _uri("https://github.com/genomoncology/biomcp")},
            {"name": "mcp", "version": "1.28.1", "uri": _uri("https://pypi.org/project/mcp/")},
            {"name": "biomcp-python", "version": "0.7.3", "uri": _uri("https://pypi.org/project/biomcp-python/")},
            {"name": "jsonschema", "version": "4.22.0", "uri": _uri("https://pypi.org/project/jsonschema/")},
        ],
        "external_data_endpoints": [
            {"name": "GlyGen REST API", "url": GLYGEN_API_BASE},
            {"name": "GlyGen MCP", "url": GLYGEN_MCP_ENDPOINT},
            {"name": "UniProt REST API", "url": "https://rest.uniprot.org"},
            {"name": "MyVariant.info (via BioMCP)", "url": "https://myvariant.info"},
        ],
        "environment_variables": {},
    }

    parametric_domain = [
        {"param": "frame_candidate_offsets", "value": "{0, signal_peptide_length}", "step": "3"},
        {"param": "signal_peptide_source", "value": "UniProt ft_signal", "step": "3"},
        {"param": "n_glyc_sequon_motif", "value": "N-X-[S/T], X != Pro", "step": "4"},
        {"param": "gog_scan_window", "value": "+/-2 residues around mutation", "step": "4"},
        {"param": "expression_present_threshold", "value": "Bgee call != ABSENT", "step": "5"},
        {"param": "biomcp_view", "value": "predictions (adds AlphaMissense)", "step": "6"},
        {"param": "ranking_key", "value": "class > expression > AlphaMissense > ClinVar", "step": "7"},
    ]

    io_domain = {
        "input_subdomain": [
            {"uri": _uri("file://" + os.path.abspath(input_path), os.path.basename(input_path),
                         access_time=run_iso)},
            # GlyGen's own source BioCompute Objects for the glycosylation dataset:
            {"uri": _uri(glygen_bco_uris[0], "GLY_001534", run_iso)},
            {"uri": _uri(glygen_bco_uris[1], "GLY_001537", run_iso)},
            {"uri": _uri(GLYGEN_API_BASE + "/protein/detail/", "glygen_protein_detail", run_iso)},
            {"uri": _uri("https://rest.uniprot.org", "uniprot_signal_peptide", run_iso)},
            {"uri": _uri("https://myvariant.info", "clinvar_alphamissense_via_biomcp", run_iso)},
        ],
        "output_subdomain": [
            {"mediatype": "text/csv",
             "uri": _uri("file://" + os.path.abspath(out_csv), os.path.basename(out_csv), run_iso)},
            {"mediatype": "application/json",
             "uri": _uri("file://" + os.path.abspath(prov_path), os.path.basename(prov_path), run_iso)},
            {"mediatype": "application/json",
             "uri": _uri("file://" + os.path.abspath(bco_path), os.path.basename(bco_path), run_iso)},
        ],
    }

    error_domain = {
        "empirical_error": {
            "benchmark": "none - no gold-standard glyco-impact benchmark was run in this pipeline",
            "occupancy_caveat": "sequon presence is necessary but not sufficient for glycan occupancy; "
                                "GOG/LOG calls are candidates, not confirmed occupancy changes",
        },
        "algorithmic_error": {
            "variant_scope": "missense single-residue substitutions only; indels, frameshift, splice, "
                             "and nonsense variants are out of scope and are not classified",
            "unmapped_guard": "a variant whose wild-type residue cannot be UNIQUELY reconciled to the "
                              "GlyGen canonical frame (zero or multiple matching offsets) is refused "
                              "(class=unmapped) and logged rather than classified",
            "numbering_assumption": "only two frames are considered - precursor (offset 0) and mature "
                                    "(offset = signal-peptide length); isoform-specific frames are not modeled",
            "alphamissense_scope": "AlphaMissense scores protein destabilization, not glyco-mechanisms, so "
                                   "it can mislabel glyco-driven variants (e.g. IFNGR2 T168N: AlphaMissense "
                                   "Benign yet ClinVar Pathogenic via gained glycosylation)",
        },
    }

    provenance_domain = {
        "name": "Glyco-variant LOG/GOG classification with expression sanity-check and ClinVar/AlphaMissense join",
        "version": "1.0.0",
        "created": run_iso,
        "modified": run_iso,
        "contributors": [
            {"name": contributor or "unknown", "contribution": ["createdBy", "authoredBy"]},
            {"name": f"Claude ({model_id})", "contribution": ["createdWith"]},
            {"name": "GlyGen", "contribution": ["importedFrom"], "affiliation": "The GlyGen Project"},
        ],
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }

    usability_domain = [
        "Classify missense variants by predicted impact on N-/O-glycosylation (LOG/GOG/none), "
        "anchored on GlyGen glycosite annotations.",
        "Reconcile mature vs precursor residue numbering per-variant so that mature-frame inputs "
        "(e.g. antithrombin Asn135 == precursor Asn167) are not silently misclassified.",
        "Contextualize each call with a GlyGen/Bgee expression sanity-check and with ClinVar "
        "significance and AlphaMissense pathogenicity federated by MyVariant.info via BioMCP.",
    ]

    bco = {
        "object_id": f"urn:glyco-variants:bco:{run_iso.replace(':', '').replace('+', 'Z')}",
        "spec_version": "https://w3id.org/ieee/ieee-2791-schema/2791object.json",
        "etag": "",  # filled in below
        "provenance_domain": provenance_domain,
        "usability_domain": usability_domain,
        "description_domain": description_domain,
        "execution_domain": execution_domain,
        "parametric_domain": parametric_domain,
        "io_domain": io_domain,
        "error_domain": error_domain,
    }
    payload = json.dumps({k: v for k, v in bco.items() if k != "etag"}, sort_keys=True).encode()
    bco["etag"] = hashlib.sha256(payload).hexdigest()
    return bco


def validate_bco(bco: dict) -> list[str]:
    """Validate against the local copy of the published IEEE-2791 schema set."""
    try:
        import glob
        from jsonschema import Draft7Validator
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT7
    except ImportError as exc:
        return [f"validation skipped: {exc} (pip install jsonschema referencing)"]

    resources = []
    for path in glob.glob(os.path.join(SCHEMA_DIR, "*.json")):
        with open(path) as fh:
            doc = json.load(fh)
        resources.append((doc["$id"], Resource.from_contents(doc, default_specification=DRAFT7)))
    registry = Registry().with_resources(resources)
    with open(os.path.join(SCHEMA_DIR, "2791object.json")) as fh:
        top = json.load(fh)
    validator = Draft7Validator(top, registry=registry)
    return [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}"
            for e in sorted(validator.iter_errors(bco), key=lambda e: list(e.path))]


# --------------------------------------------------------------------------- #
# Input parsing + CLI
# --------------------------------------------------------------------------- #

def read_input_csv(path: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    with open(path, newline="") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw or raw.lower().startswith(("uniprot", "#")):
                continue
            parts = re.split(r"[,\t]", raw)
            if len(parts) >= 2:
                out.append((parts[0].strip(), parts[1].strip()))
    return out


def ensure_input_file(variants: list[tuple[str, str]], path: str) -> str:
    """Guarantee an on-disk input file exists (for hashing + provenance)."""
    if os.path.exists(path):
        return path
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["uniprot", "protein_change"])
        w.writerows(variants)
    return path


def parse_args(argv: list[str]):
    ap = argparse.ArgumentParser(description="Classify variants by glycosylation impact (LOG/GOG/none).")
    ap.add_argument("variants", nargs="*", help="variants as UNIPROT,CHANGE (e.g. P01008,N135S)")
    ap.add_argument("--input", default="variants.csv", help="CSV with rows: uniprot,protein_change")
    ap.add_argument("--out", default="glyco_candidates.csv", help="output CSV path")
    ap.add_argument("--provenance", default="provenance.json", help="provenance JSON path")
    ap.add_argument("--bco", default="bco.json", help="BioCompute Object JSON path")
    ap.add_argument("--model-id", default=os.environ.get("GLYCO_MODEL_ID", "claude-opus-4-8"),
                    help="orchestrating model id recorded in provenance/BCO")
    return ap.parse_args(argv)


def main(argv: list[str]) -> int:
    ns = parse_args(argv)

    variants: list[tuple[str, str]] = []
    input_path = ns.input
    if ns.variants:
        for tok in ns.variants:
            parts = tok.split(",")
            if len(parts) >= 2:
                variants.append((parts[0].strip(), parts[1].strip()))
        input_path = ensure_input_file(variants, ns.input)
    elif os.path.exists(ns.input):
        variants = read_input_csv(ns.input)
    else:
        variants = list(DEFAULT_VARIANTS)
        input_path = ensure_input_file(variants, ns.input)

    run_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    log(f"Processing {len(variants)} variant(s) from {input_path} ...\n")

    glygen_version, glygen_release = fetch_glygen_version()
    mv = fetch_myvariant_meta()
    biomcp_ver = biomcp_version()
    log(f"[meta]   GlyGen {glygen_version} ({glygen_release}); ClinVar {mv.get('clinvar_version')}; "
        f"AlphaMissense via dbNSFP {mv.get('dbnsfp_version')}; {biomcp_ver}\n")

    rows = process(variants, glygen_version, glygen_release)
    write_csv(rows, ns.out)

    input_sha = sha256_file(input_path)
    contributor = git_user()

    provenance = build_provenance(
        run_iso=run_iso, model_id=ns.model_id, input_path=input_path, input_sha=input_sha,
        out_csv=ns.out, bco_path=ns.bco, glygen_version=glygen_version, glygen_release=glygen_release,
        mv=mv, biomcp_ver=biomcp_ver,
    )
    with open(ns.provenance, "w") as fh:
        json.dump(provenance, fh, indent=2)

    bco = build_bco(
        run_iso=run_iso, model_id=ns.model_id, input_path=input_path, input_sha=input_sha,
        out_csv=ns.out, prov_path=ns.provenance, bco_path=ns.bco, glygen_version=glygen_version,
        glygen_release=glygen_release, mv=mv, biomcp_ver=biomcp_ver, n_variants=len(variants),
        contributor=contributor,
    )
    with open(ns.bco, "w") as fh:
        json.dump(bco, fh, indent=2)

    errors = validate_bco(bco)

    log("\n=== glyco_candidates ===")
    for i, r in enumerate(rows, 1):
        log(f"  {i}. {r.uniprot} {r.site:<8} {r.cls:<8} expr={r._expr} "
            f"clinvar={r.clinvar or '-':<20} alphamissense={r.alphamissense or '-'}")
    log(f"\nWrote {len(rows)} row(s) to {ns.out}")
    log(f"Wrote provenance to {ns.provenance}")
    log(f"Wrote BioCompute Object to {ns.bco}")
    if errors and not errors[0].startswith("validation skipped"):
        log(f"\nBCO VALIDATION FAILED ({len(errors)} error(s)) against IEEE-2791 schema:")
        for e in errors[:25]:
            log(f"  - {e}")
        return 1
    log(f"\nBCO validation: {'PASS (IEEE-2791)' if not errors else errors[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
