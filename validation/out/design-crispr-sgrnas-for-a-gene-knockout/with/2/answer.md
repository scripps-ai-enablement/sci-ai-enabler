## Summary up front

**Recipe used:** `design-crispr-sgrnas-for-a-gene-knockout` (sci-ai-enabler knowledge base) — Evidence: **Reported**, Availability: **Fully open**, Compute: **Laptop**. Its ideal path is the dedicated *sgRNA Design* Skill (tiered: validated libraries → CRISPick → de novo Rule Set 2/CFD). In *this* sandboxed session I could not `git clone`/`/plugin install` it (network to GitHub was blocked) or execute Python/write files (blocked by this session's permission mode). So rather than hand you a plan you can't verify, I did the next best grounded thing: I pulled the **real GRCh38 TP53 sequence and exon structure live from the Ensembl REST API** this session, and computed the PAM scan/scoring by hand using only the shell primitives this sandbox allowed — cross-checking every step (lengths, alphabet, coordinate round-trips) so nothing below is a guessed sequence.

**Gene/assumption:** human *TP53*, GRCh38, canonical/MANE Select transcript ENST00000269305.9 (RefSeq NM_000546).

## The one design decision that matters most for TP53 specifically

Don't default to "pick an early exon" blindly. TP53 has an internal promoter in intron 4 that drives the Δ133p53/Δ160p53 isoforms, starting translation at internal ATGs in **exon 5** (Bourdon et al. 2005, *Genes Dev* 19:2122–2137). **Exons 2–4 are absent from those isoform transcripts**, so a guide there only knocks out full-length p53/Δ40p53, not all p53 protein products. **Exon 5 is the earliest exon shared by every major isoform** and is not the terminal exon (avoids NMD-escape risk of exon 11). That's why exon 5 — not exon 2 — is the target below.

## Ranked shortlist (top 5, exon 5, GRCh38, real fetched sequence)

Fetched: Ensembl REST `/lookup/symbol` and `/sequence/region`, 2026‑07‑30, region chr17:7,675,053–7,675,236 (exon 5, both strands).

| Rank | Protospacer (5'→3') | PAM | Strand | Genomic coords (protospacer) | On-target proxy* | Off-target flags** |
|---|---|---|---|---|---|---|
| 1 | `GCAGTCACAGCACATGACGG` | AGG | minus (gene-sense) | chr17:7,675,101–7,675,120 | 83 | none local; genome-wide **not** assessed |
| 2 | `AGCACATGACGGAGGTTGTG` | AGG | minus (gene-sense) | chr17:7,675,093–7,675,112 | 78 | none local; genome-wide **not** assessed |
| 3 | `GTGCTGTGACTGCTTGTAGA` | TGG | plus | chr17:7,675,108–7,675,127 | 75 | none local; genome-wide **not** assessed |
| 4 | `GAATCAACCCACAGCTGCAC` | AGG | plus | chr17:7,675,166–7,675,185 | 75 | none local; genome-wide **not** assessed |
| 5 | `CAAGCAGTCACAGCACATGA` | CGG | minus (gene-sense) | chr17:7,675,104–7,675,123 | 70 | overlaps #1's window — redundant, not independent |

\* Heuristic proxy (GC 40–60% band, poly‑T avoidance, PAM‑proximal G preference, homopolymer penalty) — **documented literature-informed heuristic, not the trained Doench 2016 Rule Set 2/Azimuth model.** Ranks #1/#2 are two overlapping PAM sites in the same ~40 bp GC-moderate window on the minus strand; #3/#4 are independent sites on the plus strand — good for backup diversity if the cluster fails real screening.

\** Local flags only checked seed-repeat within the ~300 bp fetched here, GC extremes, homopolymer runs ≥5, and BsmBI/BbsI cloning-site conflicts (none found in the top 5). **This is not a genome-wide off-target search.**

**Prior experimental validation:** not checked against CRISPick/Addgene/Broad GPP in this session (no network access to those services here) — flag all five as `NOT VERIFIED, cross-check before ordering`.

Two candidates were explicitly down-ranked and are worth naming so you don't re-derive them: `CGGCACCCGCGTCCGCGCCA` (score 30, GC 85% — too GC-rich) and `CAACAAGATGTTTTGCCAAC` (score 40, contains `TTTT` — premature Pol III termination risk under a U6 promoter).

## Runnable script (regenerate/extend to exon 6+ yourself)

```python
#!/usr/bin/env python3
"""CRISPR-Cas9 (SpCas9, NGG) knockout-guide scan for TP53 exon 5/6.
Sequences below are REAL GRCh38 sequence fetched from Ensembl REST API
(rest.ensembl.org) on 2026-07-30 -- not synthetic placeholders.
Scoring is a documented heuristic PROXY, not Rule Set 2/Azimuth or CFD.
Re-verify top hits in CRISPick + CRISPOR/Cas-OFFinder before ordering.
"""
import csv, json

EXONS = [
    {"exon": 2, "constitutive": False, "note": "absent from Delta133/Delta160p53 (P2-promoter) isoforms"},
    {"exon": 3, "constitutive": False, "note": "absent from Delta133/Delta160p53 isoforms"},
    {"exon": 4, "constitutive": False, "note": "absent from Delta133/Delta160p53 isoforms"},
    {"exon": 5, "constitutive": True,  "note": "earliest exon shared by ALL major p53 isoforms"},
    {"exon": 6, "constitutive": True,  "note": "shared by all major isoforms"},
    {"exon": 11, "constitutive": True, "note": "TERMINAL exon -- avoid, NMD-escape risk"},
]

EXON_SEQ_MINUS = {  # gene-sense orientation (strand=-1 fetch)
    5: "TACTCCCCTGCCCTCAACAAGATGTTTTGCCAACTGGCCAAGACCTGCCCTGTGCAGCTGTGGGTTGATTCCACACCCC"
       "CGCCCGGCACCCGCGTCCGCGCCATGGCCATCTACAAGCAGTCACAGCACATGACGGAGGTTGTGAGGCGCTGCCCCC"
       "ACCATGAGCGCTGCTCAGATAGCGATG",
    6: "GTCTGGCCCCTCCTCAGCATCTTATCCGAGTGGAAGGAAATTTGCGTGTGGAGTATTTGGATGACAGAAACACTTTTC"
       "GACATAGTGTGGTGGTGCCCTATGAGCCGCCTGAG",
}
EXON_SEQ_PLUS = {  # genomic plus-strand orientation (strand=1 fetch), exon 5 only shown above
    5: "CATCGCTATCTGAGCAGCGCTCATGGTGGGGGCAGCGCCTCACAACCTCCGTCATGTGCTGTGACTGCTTGTAGATGG"
       "CCATGGCGCGGACGCGGGTGCCGGGCGGGGGTGTGGAATCAACCCACAGCTGCACAGGGCAGGTCTTGGCCAGTTGG"
       "CAAAACATCTTGTTGAGGGCAGGGGAGTA",
}
EXON5_GENOMIC_START, EXON5_GENOMIC_END = 7675053, 7675236  # GRCh38, chr17

RESTRICTION_SITES = ["CGTCTC", "GAGACG", "GAAGAC", "GTCTTC"]  # BsmBI/Esp3I, BbsI


def gc(seq):
    return 100.0 * (seq.count("G") + seq.count("C")) / len(seq)


def has_homopolymer(seq, run=5):
    return any(b * run in seq for b in "ACGT")


def ontarget_score_proxy(p):
    s = 50.0
    g = gc(p)
    s += 20 if 40 <= g <= 60 else (5 if 30 <= g <= 70 else -20)
    if "TTTT" in p:
        s -= 30
    if has_homopolymer(p):
        s -= 15
    if p[-1] == "G":
        s += 8
    if p[0] == "G":
        s += 5
    return max(0.0, min(100.0, s))


def scan_forward(seq):
    hits = []
    for i in range(len(seq) - 22):
        w = seq[i:i + 23]
        if w[21:23] == "GG":
            hits.append({"pos": i + 1, "protospacer": w[0:20], "pam": w[20:23]})
    return hits


def to_genomic_minus(pos):  # gene-sense position -> GRCh38 chr17 coordinate
    return EXON5_GENOMIC_END + 1 - pos


def to_genomic_plus(pos):
    return EXON5_GENOMIC_START - 1 + pos


def build_candidates():
    out = []
    for h in scan_forward(EXON_SEQ_MINUS[5]):
        p = h["protospacer"]
        out.append({
            "protospacer": p, "pam": h["pam"], "strand": "minus(gene-sense)",
            "genomic_start": to_genomic_minus(h["pos"] + 19),
            "genomic_end": to_genomic_minus(h["pos"]),
            "score": round(ontarget_score_proxy(p), 1),
            "restriction_conflict": any(site in p for site in RESTRICTION_SITES),
        })
    for h in scan_forward(EXON_SEQ_PLUS[5]):
        p = h["protospacer"]
        out.append({
            "protospacer": p, "pam": h["pam"], "strand": "plus",
            "genomic_start": to_genomic_plus(h["pos"]),
            "genomic_end": to_genomic_plus(h["pos"] + 19),
            "score": round(ontarget_score_proxy(p), 1),
            "restriction_conflict": any(site in p for site in RESTRICTION_SITES),
        })
    out = [c for c in out if not c["restriction_conflict"]]
    out.sort(key=lambda c: c["score"], reverse=True)
    return out


if __name__ == "__main__":
    cands = build_candidates()
    with open("guides_shortlist.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cands[0].keys()))
        w.writeheader()
        w.writerows(cands[:5])
    provenance = {
        "gene": "TP53", "genome_build": "GRCh38",
        "transcript": "ENST00000269305.9 (MANE Select)",
        "source": "Ensembl REST API, fetched 2026-07-30",
        "on_target_model": "heuristic proxy, NOT Rule Set 2/Azimuth",
        "off_target_model": "NOT genome-wide -- rerun via CRISPOR/Cas-OFFinder",
        "isoform_reference": "Bourdon et al. 2005, Genes Dev 19:2122-2137",
    }
    with open("provenance.json", "w") as f:
        json.dump(provenance, f, indent=2)
    for c in cands[:5]:
        print(c)
```

Run it (`python3 crispr_sgrna_design.py`) in a normal shell to regenerate `guides_shortlist.csv` + `provenance.json`, and extend `EXON_SEQ_MINUS`/`EXON_SEQ_PLUS` with exon 6/7 (fetch via `https://rest.ensembl.org/sequence/region/human/17:7674859-7674971:-1?content-type=text/x-fasta`, etc.) if the exon-5 candidates don't clear real off-target screening.

## Before you order oligos — required, not optional

1. Re-score the top candidates in **CRISPick** (portals.broadinstitute.org/gppx/crispick/public) for real Rule Set 2 + CFD scores.
2. Run a genuine **genome-wide off-target search** (CRISPOR or Cas-OFFinder against full GRCh38 + common SNPs) — the flags above only checked ~300 bp of local sequence.
3. Re-confirm exact chromosome coordinates in a live genome browser (Ensembl/UCSC) — my arithmetic passed internal adjacency checks, but independent confirmation is standard practice.
4. Cross-check against a public validated knockout guide set (Addgene TP53 KO plasmids, Broad GPP, GenScript) if you specifically need prior-validation evidence for your methods section.

## Methods-section paragraph (draft — fill in after step 1–3 above)

> *sgRNAs targeting TP53 (GRCh38, ENST00000269305.9/NM_000546) were designed to target exon 5, the earliest coding exon shared by all major p53 isoforms (full-length, Δ40p53, Δ133p53, Δ160p53), avoiding exons 2–4 (excluded from Δ133p53/Δ160p53 transcripts driven by the intron-4 internal promoter; Bourdon et al. 2005) and the terminal exon 11 (NMD-escape risk). Candidate protospacers were identified by scanning both strands of the Ensembl GRCh38 exon-5 sequence (fetched [date]) for SpCas9 NGG PAMs, ranked by [Rule Set 2 score from CRISPick / heuristic proxy — specify which you used], and filtered for off-target risk using [CRISPOR/Cas-OFFinder against GRCh38 — specify]. The selected guide, [sequence], targets chr17:[coords] (GRCh38).*

## What I didn't do, and why

I did not file anything to the sci-ai-enabler knowledge base's issue tracker — this wasn't a genuine gap in the catalog (the `design-crispr-sgrnas-for-a-gene-knockout` recipe is sound), it was a session-specific sandbox restriction on network/execution, so filing a "missing component" report would be misleading to the curators.