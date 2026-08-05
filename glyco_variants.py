#!/usr/bin/env python3
"""glyco_variants.py

Classify protein missense variants for their impact on glycosylation
(loss/gain of an N-X-S/T sequon or disruption of an annotated O-glycosite),
enrich each variant with ClinVar clinical significance and AlphaMissense
pathogenicity, then rank the candidates.

Design constraints (deliberately met by this script):
  * No MCP servers, plugins, BioMCP, or agent frameworks are used.
  * Only the Python standard library is required (no pip install needed).
  * All biological data is pulled directly from public REST APIs.
  * Missing data is reported as missing -- annotations are never fabricated.

Public REST APIs used (each is also documented at its call site):
  1. UniProtKB REST
     https://rest.uniprot.org/uniprotkb/{accession}.json
     -> canonical protein sequence, gene name, signal/transit/propeptide
        lengths (needed for residue-numbering harmonization) and the RefSeq
        protein accession (needed by Ensembl VEP).
  2. GlyGen REST
     https://api.glygen.org/protein/detail/{canonical_ac}/
     -> annotated glycosylation sites (via the `site_annotation` block).
  3. NCBI E-utilities (ClinVar)
     https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
     https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi
     -> germline clinical significance and review status (star rating).
  4. Ensembl VEP REST
     https://rest.ensembl.org/vep/human/hgvs/{refseq_np}:p.{Wt}{pos}{Alt}
     -> AlphaMissense pathogenicity score and class.

Usage:
    python glyco_variants.py                 # uses the built-in variant list
    python glyco_variants.py --out out.csv   # custom output path
    python glyco_variants.py -v              # debug logging
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger("glyco_variants")

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

# (UniProt accession, protein change in 1-letter HGVS-like notation).
# Numbering may follow either the canonical (precursor) sequence or a legacy
# mature-protein scheme; this is reconciled per-variant in `harmonize_position`.
DEFAULT_VARIANTS: list[tuple[str, str]] = [
    ("P01008", "N135S"),
    ("P38484", "T168N"),
    ("P01008", "P305H"),
]

# ---------------------------------------------------------------------------
# API endpoints (constants)
# ---------------------------------------------------------------------------

UNIPROT_ENTRY = "https://rest.uniprot.org/uniprotkb/{acc}.json"
GLYGEN_PROTEIN_DETAIL = "https://api.glygen.org/protein/detail/{acc}/"
EUTILS_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EUTILS_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
ENSEMBL_VEP_HGVS = "https://rest.ensembl.org/vep/human/hgvs/{hgvs}"

# Courtesy tool name sent to NCBI E-utilities (recommended, not required).
NCBI_TOOL = "glyco_variants"

# ---------------------------------------------------------------------------
# Amino-acid helpers
# ---------------------------------------------------------------------------

AA1_TO_3 = {
    "A": "Ala", "R": "Arg", "N": "Asn", "D": "Asp", "C": "Cys", "Q": "Gln",
    "E": "Glu", "G": "Gly", "H": "His", "I": "Ile", "L": "Leu", "K": "Lys",
    "M": "Met", "F": "Phe", "P": "Pro", "S": "Ser", "T": "Thr", "W": "Trp",
    "Y": "Tyr", "V": "Val",
}

# ClinVar significance -> ordinal used only for deterministic ranking tie-breaks.
CLINVAR_ORDER = {
    "pathogenic": 6,
    "likely pathogenic": 5,
    "pathogenic/likely pathogenic": 5,
    "uncertain significance": 3,
    "conflicting interpretations of pathogenicity": 3,
    "conflicting classifications of pathogenicity": 3,
    "likely benign": 2,
    "benign/likely benign": 2,
    "benign": 1,
}

# ClinVar review status -> gold-star rating (per ClinVar documentation).
REVIEW_STATUS_STARS = {
    "practice guideline": 4,
    "reviewed by expert panel": 3,
    "criteria provided, multiple submitters, no conflicts": 2,
    "criteria provided, conflicting classifications": 1,
    "criteria provided, conflicting interpretations": 1,
    "criteria provided, single submitter": 1,
    "no assertion criteria provided": 0,
    "no assertion provided": 0,
    "no classification provided": 0,
    "no classifications from unflagged records": 0,
}


def three_letter(aa1: str) -> str:
    """Convert a single-letter amino-acid code to its three-letter form."""
    return AA1_TO_3[aa1.upper()]


def is_nx_st_sequon(triple: str) -> bool:
    """True if a 3-residue window is a valid N-linked sequon: N-X-[S/T], X != P."""
    if len(triple) != 3:
        return False
    return triple[0] == "N" and triple[1] != "P" and triple[2] in ("S", "T")


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class Variant:
    """A parsed missense variant as supplied in the input list."""

    uniprot: str
    protein_change: str
    wt: str
    position: int  # position as given in the input (may be legacy numbering)
    alt: str


@dataclass
class ProteinRecord:
    """Sequence + annotation context assembled for one protein."""

    accession: str
    canonical_ac: str
    sequence: str
    gene: Optional[str]
    refseq_np: Optional[str]
    # candidate offsets that map input numbering -> canonical numbering
    offset_candidates: dict[int, str] = field(default_factory=dict)
    # annotated N-linked acceptor positions (the Asn), in canonical numbering
    n_glyco_sites: set[int] = field(default_factory=set)
    # annotated O-linked glycosite positions, in canonical numbering
    o_glyco_sites: set[int] = field(default_factory=set)


@dataclass
class Result:
    """Final per-variant output row."""

    uniprot: str
    protein_change: str
    site: str = ""
    variant_class: str = "unmapped"
    glygen_evidence: str = ""
    clinvar_significance: str = "not_provided"
    alphamissense: str = "not_available"
    rank: int = 0
    # internal, not written to CSV -- used for ranking only
    _am_score: Optional[float] = None
    _clinvar_ord: int = 0


# ---------------------------------------------------------------------------
# HTTP layer with retry/backoff
# ---------------------------------------------------------------------------

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def http_get(
    url: str,
    *,
    params: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
    max_retries: int = 4,
    timeout: int = 30,
) -> Optional[bytes]:
    """GET a URL with exponential backoff.

    Returns the raw response body, or None if all attempts fail (callers treat
    None as "data unavailable" and degrade gracefully rather than crashing).
    """
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req_headers = {"User-Agent": f"{NCBI_TOOL}/1.0", "Accept": "application/json"}
    if headers:
        req_headers.update(headers)

    delay = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code in RETRYABLE_STATUS and attempt < max_retries:
                retry_after = exc.headers.get("Retry-After")
                wait = float(retry_after) if retry_after else delay
                logger.warning(
                    "HTTP %s on %s (attempt %d/%d); retrying in %.1fs",
                    exc.code, url, attempt, max_retries, wait,
                )
                time.sleep(wait)
                delay *= 2
                continue
            logger.error("HTTP %s on %s: giving up", exc.code, url)
            return None
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < max_retries:
                logger.warning(
                    "Network error on %s (%s); retrying in %.1fs",
                    url, exc, delay,
                )
                time.sleep(delay)
                delay *= 2
                continue
            logger.error("Network error on %s: giving up (%s)", url, exc)
            return None
    return None


def http_get_json(url: str, **kwargs) -> Optional[object]:
    """GET a URL and parse the JSON body, returning None on any failure."""
    raw = http_get(url, **kwargs)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON from %s: %s", url, exc)
        return None


# ---------------------------------------------------------------------------
# Variant parsing
# ---------------------------------------------------------------------------

_VARIANT_RE = re.compile(r"^([A-Z])(\d+)([A-Z])$")


def parse_variant(uniprot: str, change: str) -> Optional[Variant]:
    """Parse a change string like 'N135S' into a Variant, or None if malformed."""
    m = _VARIANT_RE.match(change.strip().upper())
    if not m:
        logger.error("Cannot parse variant '%s' for %s", change, uniprot)
        return None
    wt, pos, alt = m.group(1), int(m.group(2)), m.group(3)
    return Variant(uniprot=uniprot, protein_change=change, wt=wt, position=pos, alt=alt)


# ---------------------------------------------------------------------------
# UniProt: sequence, gene, numbering offsets, RefSeq accession
# ---------------------------------------------------------------------------


def canonical_ac(accession: str) -> str:
    """GlyGen keys proteins by isoform accession; canonical is '-1'."""
    return accession if "-" in accession else f"{accession}-1"


def fetch_uniprot(accession: str) -> Optional[ProteinRecord]:
    """Fetch the canonical sequence and numbering context from UniProtKB.

    Endpoint: https://rest.uniprot.org/uniprotkb/{accession}.json
    Provides the authoritative canonical sequence plus feature annotations
    (SIGNAL / TRANSIT / PROPEP), whose lengths become candidate offsets for
    reconciling legacy "mature-protein" numbering with canonical numbering.
    """
    data = http_get_json(UNIPROT_ENTRY.format(acc=accession))
    if not isinstance(data, dict) or "sequence" not in data:
        logger.error("No UniProt entry for %s", accession)
        return None

    seq = data["sequence"]["value"]

    gene = None
    genes = data.get("genes") or []
    if genes and genes[0].get("geneName"):
        gene = genes[0]["geneName"]["value"]

    # RefSeq protein accession (with version) is required by Ensembl VEP.
    refseq_np = None
    for xref in data.get("uniProtKBCrossReferences", []):
        if xref.get("database") == "RefSeq" and xref.get("id", "").startswith("NP_"):
            refseq_np = xref["id"]
            break

    # offset 0 (input already canonical) is always a candidate.
    offsets: dict[int, str] = {0: "canonical"}
    for feat in data.get("features", []):
        ftype = feat.get("type")
        if ftype in ("Signal", "Transit peptide", "Propeptide"):
            try:
                end = int(feat["location"]["end"]["value"])
            except (KeyError, TypeError, ValueError):
                continue
            # A mature-numbered residue r corresponds to canonical r + end.
            offsets.setdefault(end, ftype.lower())

    return ProteinRecord(
        accession=accession,
        canonical_ac=canonical_ac(accession),
        sequence=seq,
        gene=gene,
        refseq_np=refseq_np,
        offset_candidates=offsets,
    )


# ---------------------------------------------------------------------------
# GlyGen: annotated glycosylation sites
# ---------------------------------------------------------------------------


def fetch_glygen_sites(record: ProteinRecord) -> None:
    """Populate annotated N-/O-glycosylation sites from GlyGen (in place).

    Endpoint: https://api.glygen.org/protein/detail/{canonical_ac}/
    The `site_annotation` block lists sequons with start/end positions and an
    `annotation` label (e.g. 'n_glycosylation_sequon', 'o_glycosylation_*').
    `start_pos` is the glycosylated acceptor residue in canonical numbering.
    """
    data = http_get_json(GLYGEN_PROTEIN_DETAIL.format(acc=record.canonical_ac))
    if not isinstance(data, dict):
        logger.warning(
            "No GlyGen record for %s; no annotated glycosites available",
            record.canonical_ac,
        )
        return

    # Sanity-check that GlyGen and UniProt describe the same sequence.
    gseq = (data.get("sequence") or {}).get("sequence")
    if gseq and gseq != record.sequence:
        logger.warning(
            "GlyGen sequence for %s differs from UniProt; using UniProt numbering",
            record.canonical_ac,
        )

    for ann in data.get("site_annotation", []) or []:
        label = (ann.get("annotation") or "").lower()
        start = ann.get("start_pos")
        if start is None or "glycosylation" not in label:
            continue
        if label.startswith("n_"):
            record.n_glyco_sites.add(int(start))
        elif label.startswith("o_"):
            record.o_glyco_sites.add(int(start))

    logger.info(
        "GlyGen %s: %d N-linked, %d O-linked annotated site(s)",
        record.canonical_ac, len(record.n_glyco_sites), len(record.o_glyco_sites),
    )


# ---------------------------------------------------------------------------
# Numbering harmonization
# ---------------------------------------------------------------------------


def harmonize_position(variant: Variant, record: ProteinRecord) -> tuple[Optional[int], str]:
    """Map the input position onto canonical numbering by matching the WT residue.

    Returns (canonical_position, note). canonical_position is None when the
    numbering cannot be reconciled confidently, in which case `note` explains why
    (e.g. the antithrombin Asn135<->Asn167 mature/precursor offset of +32).
    """
    seq = record.sequence
    matches: list[tuple[int, int, str]] = []  # (offset, canonical_pos, scheme)
    seen: list[str] = []
    for offset, scheme in sorted(record.offset_candidates.items()):
        canon = variant.position + offset
        if 1 <= canon <= len(seq):
            observed = seq[canon - 1]
            seen.append(f"offset+{offset}->{observed}{canon}")
            if observed == variant.wt:
                matches.append((offset, canon, scheme))

    if not matches:
        reason = (
            f"WT residue {variant.wt} not found at input position "
            f"{variant.position} under any known numbering offset "
            f"[{', '.join(seen) or 'none in range'}]"
        )
        logger.warning("%s %s unmapped: %s", variant.uniprot, variant.protein_change, reason)
        return None, reason

    if len(matches) == 1:
        offset, canon, scheme = matches[0]
        note = (
            f"canonical numbering ({scheme})"
            if offset == 0
            else f"remapped +{offset} from {scheme}: {variant.wt}{variant.position}->{variant.wt}{canon}"
        )
        return canon, note

    # Multiple offsets fit the WT residue. Prefer offset 0 (input already
    # canonical) but flag the ambiguity so a reviewer can check.
    for offset, canon, scheme in matches:
        if offset == 0:
            logger.warning(
                "%s %s: ambiguous numbering, defaulting to canonical (candidates: %s)",
                variant.uniprot, variant.protein_change,
                [m[1] for m in matches],
            )
            return canon, f"ambiguous; defaulted to canonical position {canon}"

    # Ambiguous with no canonical option -> not confident.
    reason = f"ambiguous numbering; multiple offsets fit WT ({[m[1] for m in matches]})"
    logger.warning("%s %s unmapped: %s", variant.uniprot, variant.protein_change, reason)
    return None, reason


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def classify(variant: Variant, canon_pos: int, record: ProteinRecord) -> tuple[str, str]:
    """Classify a harmonized variant as LOG, GOG, or none, with evidence text."""
    seq = record.sequence
    wt, alt = variant.wt, variant.alt

    # --- LOG: disruption of an annotated O-glycosite -----------------------
    if canon_pos in record.o_glyco_sites and alt != wt:
        return "LOG", (
            f"mutates annotated O-glycosite {wt}{canon_pos} "
            f"[GlyGen:site_annotation o_glycosylation]"
        )

    # --- LOG: disruption of an annotated N-X-S/T sequon --------------------
    # For each annotated Asn acceptor p, the sequon spans p..p+2. If the
    # mutated residue lies in that window and breaks the motif, it is a LOG.
    for p in sorted(record.n_glyco_sites):
        if p <= canon_pos <= p + 2 and p + 2 <= len(seq):
            wt_triple = seq[p - 1 : p + 2]
            idx = canon_pos - p
            mut_triple = wt_triple[:idx] + alt + wt_triple[idx + 1 :]
            if is_nx_st_sequon(wt_triple) and not is_nx_st_sequon(mut_triple):
                if canon_pos == p:
                    detail = f"removes N of annotated N-linked sequon N{p}"
                elif canon_pos == p + 1:
                    detail = f"introduces X=Pro in annotated N-linked sequon N{p}"
                else:
                    detail = f"removes +2 S/T of annotated N-linked sequon N{p}"
                return "LOG", f"{detail} [GlyGen:site_annotation n_glycosylation_sequon {p}-{p + 2}]"

    # --- GOG: creation of a new N-X-S/T sequon within the +/-2 window ------
    mutant = seq[: canon_pos - 1] + alt + seq[canon_pos:]
    for i in range(max(1, canon_pos - 2), canon_pos + 1):
        if i + 2 > len(seq):
            continue
        wt_triple = seq[i - 1 : i + 2]
        mut_triple = mutant[i - 1 : i + 2]
        if (
            is_nx_st_sequon(mut_triple)
            and not is_nx_st_sequon(wt_triple)
            and i not in record.n_glyco_sites
        ):
            return "GOG", (
                f"creates N-X-S/T sequon at N{i} "
                f"({'-'.join(mut_triple)}); not a pre-existing GlyGen site"
            )

    # --- none -------------------------------------------------------------
    all_sites = record.n_glyco_sites | record.o_glyco_sites
    if all_sites:
        nearest = min(all_sites, key=lambda p: abs(p - canon_pos))
        detail = (
            f"no sequon gained/lost; nearest annotated glycosite "
            f"{seq[nearest - 1]}{nearest} ({abs(nearest - canon_pos)} aa away)"
        )
    else:
        detail = "no sequon gained/lost; no annotated glycosites in GlyGen"
    return "none", detail


# ---------------------------------------------------------------------------
# ClinVar (NCBI E-utilities)
# ---------------------------------------------------------------------------

_last_ncbi_call = 0.0


def _ncbi_throttle() -> None:
    """Keep under NCBI's ~3 requests/second courtesy limit (no API key)."""
    global _last_ncbi_call
    elapsed = time.monotonic() - _last_ncbi_call
    if elapsed < 0.34:
        time.sleep(0.34 - elapsed)
    _last_ncbi_call = time.monotonic()


def fetch_clinvar(gene: Optional[str], wt: str, canon_pos: int, alt: str,
                  input_pos: int) -> tuple[str, int]:
    """Return (significance, review_stars) for a variant, or ('not_provided', 0).

    Endpoints:
      esearch.fcgi  -> resolve gene + protein change to ClinVar variation IDs
      esummary.fcgi -> germline_classification (significance + review status)
    The protein change is queried in canonical numbering first, then in the
    original input numbering as a fallback. Nothing is invented when absent.
    """
    if not gene:
        return "not_provided", 0

    wt3, alt3 = three_letter(wt), three_letter(alt)
    # Try canonical numbering, then the (possibly legacy) input numbering.
    positions = [canon_pos] if canon_pos == input_pos else [canon_pos, input_pos]

    variation_id: Optional[str] = None
    for pos in positions:
        term = f"{gene}[gene] AND {wt3}{pos}{alt3}"
        _ncbi_throttle()
        data = http_get_json(
            EUTILS_ESEARCH,
            params={"db": "clinvar", "retmode": "json", "term": term, "tool": NCBI_TOOL},
        )
        idlist = (
            data.get("esearchresult", {}).get("idlist", []) if isinstance(data, dict) else []
        )
        if idlist:
            variation_id = idlist[0]
            logger.info("ClinVar hit for '%s' -> id %s", term, variation_id)
            break

    if not variation_id:
        logger.info("ClinVar: no record for %s %s%d%s", gene, wt, canon_pos, alt)
        return "not_provided", 0

    _ncbi_throttle()
    summary = http_get_json(
        EUTILS_ESUMMARY,
        params={"db": "clinvar", "retmode": "json", "id": variation_id, "tool": NCBI_TOOL},
    )
    try:
        rec = summary["result"][variation_id]
        germ = rec.get("germline_classification", {})
        desc = germ.get("description") or "not_provided"
        review = (germ.get("review_status") or "").lower()
    except (KeyError, TypeError):
        logger.warning("ClinVar esummary parse failed for id %s", variation_id)
        return "not_provided", 0

    stars = REVIEW_STATUS_STARS.get(review, 0)
    return desc, stars


# ---------------------------------------------------------------------------
# AlphaMissense (Ensembl VEP REST)
# ---------------------------------------------------------------------------


def fetch_alphamissense(refseq_np: Optional[str], wt: str, canon_pos: int,
                        alt: str) -> tuple[Optional[float], Optional[str]]:
    """Return (am_pathogenicity, am_class) from Ensembl VEP, or (None, None).

    Endpoint:
      https://rest.ensembl.org/vep/human/hgvs/{NP_acc}:p.{Wt}{pos}{Alt}
      ?AlphaMissense=1
    AlphaMissense is reported per transcript under
    transcript_consequences[].alphamissense. We select the consequence whose
    protein position matches the canonical position (the MANE/canonical
    transcript) to avoid picking an alternative isoform's score.
    """
    if not refseq_np:
        logger.info("No RefSeq accession; skipping AlphaMissense lookup")
        return None, None

    hgvs = f"{refseq_np}:p.{three_letter(wt)}{canon_pos}{three_letter(alt)}"
    url = ENSEMBL_VEP_HGVS.format(hgvs=urllib.parse.quote(hgvs))
    data = http_get_json(
        url, params={"content-type": "application/json", "AlphaMissense": "1"}
    )
    if not isinstance(data, list) or not data:
        logger.info("VEP returned no data for %s", hgvs)
        return None, None

    consequences = data[0].get("transcript_consequences", []) or []
    scored = [c for c in consequences if "alphamissense" in c]
    if not scored:
        logger.info("No AlphaMissense score available for %s", hgvs)
        return None, None

    # Prefer the transcript whose protein position matches our canonical position.
    best = next((c for c in scored if c.get("protein_start") == canon_pos), scored[0])
    am = best["alphamissense"]
    return am.get("am_pathogenicity"), am.get("am_class")


# ---------------------------------------------------------------------------
# Ranking
# ---------------------------------------------------------------------------

# LOG/GOG rank above 'none'; 'unmapped' sinks to the bottom.
CLASS_PRIORITY = {"LOG": 0, "GOG": 0, "none": 1, "unmapped": 2}


def rank_results(results: list[Result]) -> None:
    """Assign 1-based ranks in place.

    Order: class priority (LOG/GOG > none > unmapped), then descending
    AlphaMissense pathogenicity, then descending ClinVar significance ordinal.
    """
    def sort_key(r: Result) -> tuple:
        am = r._am_score if r._am_score is not None else float("-inf")
        return (CLASS_PRIORITY.get(r.variant_class, 3), -am, -r._clinvar_ord)

    for i, r in enumerate(sorted(results, key=sort_key), start=1):
        r.rank = i
    # Re-sort the list itself so CSV rows come out in rank order.
    results.sort(key=lambda r: r.rank)


# ---------------------------------------------------------------------------
# Per-variant pipeline
# ---------------------------------------------------------------------------


def process_variant(uniprot: str, change: str,
                    cache: dict[str, Optional[ProteinRecord]]) -> Result:
    """Run the full pipeline for a single variant and return its output row."""
    variant = parse_variant(uniprot, change)
    if variant is None:
        return Result(uniprot=uniprot, protein_change=change,
                      variant_class="unmapped",
                      glygen_evidence="unparseable variant string")

    result = Result(uniprot=uniprot, protein_change=change)

    # 1. Resolve the canonical protein (cached per accession).
    if uniprot not in cache:
        rec = fetch_uniprot(uniprot)
        if rec is not None:
            fetch_glygen_sites(rec)  # 2. annotated glyco sites from GlyGen
        cache[uniprot] = rec
    record = cache[uniprot]

    if record is None:
        result.glygen_evidence = "protein record unavailable (UniProt lookup failed)"
        return result

    # 3. Harmonize numbering before any comparison.
    canon_pos, note = harmonize_position(variant, record)
    if canon_pos is None:
        result.variant_class = "unmapped"
        result.site = f"{variant.wt}{variant.position}"
        result.glygen_evidence = f"unmapped: {note}"
        # Per spec: do not attempt further classification or enrichment.
        result.clinvar_significance = "n/a"
        result.alphamissense = "n/a"
        return result

    result.site = f"{variant.wt}{canon_pos}"

    # 4. Classify against GlyGen annotations.
    result.variant_class, evidence = classify(variant, canon_pos, record)
    result.glygen_evidence = f"{evidence}; numbering: {note}"

    # 5. Enrich with ClinVar + AlphaMissense (public APIs, not BioMCP).
    sig, stars = fetch_clinvar(record.gene, variant.wt, canon_pos, variant.alt,
                               variant.position)
    result.clinvar_significance = (
        f"{sig} ({stars} star)" if sig != "not_provided" else "not_provided"
    )
    result._clinvar_ord = CLINVAR_ORDER.get(sig.lower(), 0)

    am_score, am_class = fetch_alphamissense(record.refseq_np, variant.wt,
                                             canon_pos, variant.alt)
    if am_score is not None:
        result.alphamissense = f"{am_score:.4f} ({am_class})"
        result._am_score = am_score
    else:
        result.alphamissense = "not_available"

    return result


# ---------------------------------------------------------------------------
# CSV output
# ---------------------------------------------------------------------------

CSV_COLUMNS = [
    "uniprot",
    "protein_change",
    "site",
    "class",
    "glygen_evidence",
    "clinvar_significance",
    "alphamissense",
    "rank",
]


def write_csv(results: list[Result], path: str) -> None:
    """Write the ranked results to a CSV with the required column schema."""
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(CSV_COLUMNS)
        for r in results:
            writer.writerow([
                r.uniprot,
                r.protein_change,
                r.site,
                r.variant_class,
                r.glygen_evidence,
                r.clinvar_significance,
                r.alphamissense,
                r.rank,
            ])
    logger.info("Wrote %d rows to %s", len(results), path)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", default="glyco_candidates.csv",
                        help="output CSV path (default: glyco_candidates.csv)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
    )

    cache: dict[str, Optional[ProteinRecord]] = {}
    results: list[Result] = []
    for uniprot, change in DEFAULT_VARIANTS:
        logger.info("=== Processing %s %s ===", uniprot, change)
        try:
            results.append(process_variant(uniprot, change, cache))
        except Exception as exc:  # never let one variant abort the whole run
            logger.exception("Unexpected error processing %s %s: %s", uniprot, change, exc)
            results.append(Result(uniprot=uniprot, protein_change=change,
                                  variant_class="unmapped",
                                  glygen_evidence=f"processing error: {exc}"))

    rank_results(results)
    write_csv(results, args.out)

    # Console summary.
    for r in results:
        logger.info("rank %d: %s %s -> %s (%s)", r.rank, r.uniprot,
                    r.protein_change, r.variant_class, r.site)


if __name__ == "__main__":
    main()
