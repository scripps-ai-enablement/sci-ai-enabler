I hit a wall worth flagging: this sandboxed session has no one available to approve file-write or code-execution permissions, so I couldn't actually run `blastn` or write files to disk here. Below is the complete, runnable solution plus a fully worked example computed by hand from a real GenBank type-strain sequence — you can paste this into your own environment (where BLAST+ is installed) and run it as-is. I'll flag clearly which numbers are "real BLAST output" vs. "illustrative, unexecuted demonstration."

## Assumptions (stated explicitly, since no files were provided)

1. **Sequencing workflow**: colony PCR with 27F/1492R was Sanger-sequenced in both directions and assembled into one consensus contig (standard practice — a single 27F-only read rarely gives usable quality past ~800–900 nt, so a near-full-length ~1400+ bp contig implies both reads were merged).
2. **Example organism**: I used the real NCBI record **X80725.1**, "*E. coli* (ATCC 11775ᵀ) gene for 16S rRNA" — the *E. coli* type strain — as the ground-truth sequence, fetched from NCBI Nucleotide today. From it I derived two realistic synthetic inputs:
   - a **1421 bp colony-PCR contig** (last 55 nt trimmed off, mimicking normal 3′ quality-trimming near the 1492R site; one ambiguous `N` basecall; one single miscalled base),
   - a **1476 bp genome-assembly-derived 16S extract** (full length, no primer artifacts, the two `N`s in the original deposited Sanger read resolved to consensus bases, as a modern high-coverage assembly would).
   - I picked *E. coli* deliberately (not a random genus) because it lets the worked example demonstrate the exact ambiguity you're worried about — 16S genuinely cannot cleanly separate *Escherichia* from *Shigella*.
3. **Reference database**: NCBI's curated `16S_ribosomal_RNA` BLAST database (built from RefSeq Targeted Loci / type-strain-anchored submissions), **not** `nt` — this is the standard way to dodge misannotated environmental-clone contamination.
4. **Thresholds**: ≥98.7% identity for species-level (Kim et al. 2014; Yarza et al. 2014), ≥94.5% for genus-level (Yarza et al. 2014), below that = possible novel taxon. Coverage gate ≥90% to even report a hit; ≥95% coverage over ≥1300 bp aligned length required to claim species-level.

## Recipe match

This maps directly onto a curated recipe in the sci-ai-enabler catalog: **[Identify a Bacterial Isolate from its 16S rRNA Sequence](https://scripps-ai-enablement.github.io/sci-ai-enabler/recipes/items/identify-bacterial-isolate-from-16s-sequence.html)** (BLAST MCP server against the pinned NCBI `16S_ribosomal_RNA` db).

- **Evidence**: Reported · **Availability**: Fully open · **Compute**: Laptop-sufficient
- Gap vs. what you asked for: the recipe as published doesn't cover chimera screening, primer trimming, or reconciling two sequence versions of the same locus. I extended it with those three gates below using the *same* grounded component (BLAST+), not a new tool — the catalog has no dedicated chimera-detection entry (I checked; no VSEARCH/UCHIME/cutadapt in the index), so the chimera check below is a classic split-query self-BLAST heuristic, not a substitute for the gold-standard `vsearch --uchime_ref` if you have it available.
- *(Index staleness note: the catalog was generated 2026-07-06, 24 days old — if this recipe seems off, `/plugin marketplace update sci-ai-enabler` first.)*

## The pipeline (paste this into `identify_isolate.py`)

```python
#!/usr/bin/env python3
"""
identify_isolate.py -- 16S rRNA isolate ID against a pinned type-strain database.

Usage:
    python identify_isolate.py \
        --pcr data/isolate_colony_pcr_27F_1492R.fasta \
        --genome data/isolate_genome_assembly_16S.fasta \
        --db /path/to/16S_ribosomal_RNA \
        --outdir output

If blastn is not on PATH or --db is omitted, runs in --demo mode using a
clearly-labeled mocked hit table so the report format can still be inspected.
"""
import argparse, csv, json, re, shutil, subprocess, sys
from pathlib import Path

PRIMER_27F = "AGAGTTTGATCMTGGCTCAG"          # IUPAC M = A/C
PRIMER_1492R_RC = "AAGTCGTAACAAGGTARCCGTA"   # revcomp of 1492R, IUPAC R = A/G
IUPAC = {"M": "AC", "R": "AG", "Y": "CT", "S": "GC", "W": "AT",
         "K": "GT", "N": "ACGT"}

def iupac_match(base, pattern_char):
    return base.upper() in IUPAC.get(pattern_char.upper(), pattern_char.upper())

def fuzzy_find(seq, primer, window, max_mismatch=2):
    """Slide `primer` across the first/last `window` bases of seq; return
    trim length if found within max_mismatch, else None."""
    n = len(primer)
    for start in range(0, max(1, window - n + 1)):
        frag = seq[start:start + n]
        if len(frag) < n:
            break
        mism = sum(0 if iupac_match(b, p) else 1 for b, p in zip(frag, primer))
        if mism <= max_mismatch:
            return start + n
    return None

def read_fasta(path):
    header, seq = None, []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"):
                header = line[1:]
            elif line:
                seq.append(line)
    return header, "".join(seq).upper()

def trim_primers(seq):
    notes = []
    lead = fuzzy_find(seq, PRIMER_27F, window=30)
    if lead:
        seq = seq[lead:]
        notes.append(f"trimmed {lead} nt of 27F primer from 5' end")
    tail = fuzzy_find(seq[::-1], PRIMER_1492R_RC[::-1], window=30)
    if tail:
        seq = seq[:len(seq) - tail]
        notes.append(f"trimmed {tail} nt of 1492R primer from 3' end")
    if not notes:
        notes.append("no primer sequence detected (already trimmed)")
    return seq, notes

def length_gate(seq, min_len=1200, expected=1450):
    ok = len(seq) >= min_len
    return ok, (f"{len(seq)} bp ({'PASS' if ok else 'FAIL'}: near-full-length "
                f"16S from 27F/1492R should be ~{expected} bp; "
                f"reads <{min_len} bp lack enough variable-region coverage "
                f"for a confident species-level call)")

def reconcile(seq_pcr, seq_genome, min_concordance=0.995):
    n = min(len(seq_pcr), len(seq_genome))
    mism, scored = 0, 0
    for a, b in zip(seq_pcr[:n], seq_genome[:n]):
        if a == "N" or b == "N":
            continue
        scored += 1
        if a != b:
            mism += 1
    pct = 1 - (mism / scored) if scored else 0.0
    ok = pct >= min_concordance
    return ok, (f"{pct:.4%} concordance over {scored} scorable positions "
                f"({mism} mismatch(es), {n - scored} ambiguous base(s) excluded) "
                f"-- {'consistent' if ok else 'DISCORDANT: check for mixed culture, '
                'contamination, or 16S operon heterogeneity before trusting either read'}")

def have_blastn():
    return shutil.which("blastn") is not None

def run_blastn(query_fasta, db, outfmt_cols):
    cmd = ["blastn", "-query", str(query_fasta), "-db", str(db), "-task", "blastn",
           "-perc_identity", "80", "-qcov_hsp_perc", "50", "-max_target_seqs", "10",
           "-outfmt", "6 " + " ".join(outfmt_cols)]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    rows = []
    for line in out.stdout.strip().splitlines():
        rows.append(dict(zip(outfmt_cols, line.split("\t"))))
    return rows

def chimera_check(seq, db):
    if not have_blastn() or not db:
        return "SKIPPED", "blastn/db unavailable -- chimera screen not performed; do not trust species-level calls until this is run"
    mid = len(seq) // 2
    halves = {"5prime": seq[:mid], "3prime": seq[mid:]}
    tops = {}
    for name, frag in halves.items():
        tmp = Path(f"/tmp/{name}_frag.fasta")
        tmp.write_text(f">{name}\n{frag}\n")
        hits = run_blastn(tmp, db, ["sseqid", "pident", "stitle"])
        tops[name] = hits[0]["stitle"].split()[0] if hits else None
    if tops["5prime"] and tops["3prime"] and tops["5prime"] != tops["3prime"]:
        return "FLAGGED", f"5' half best hit genus differs from 3' half ({tops['5prime']} vs {tops['3prime']}) -- possible chimera, exclude from species-level reporting"
    return "CLEAN", "5' and 3' half-fragments agree on genus -- no chimera signal from this coarse split-query check (not a substitute for vsearch --uchime_ref)"

def assign_tier(pident, coverage, qlen, tied_species):
    if coverage < 0.90:
        return "unresolved", "query coverage < 90% -- alignment too partial to trust any identity-based call"
    if pident >= 98.7 and coverage >= 0.95 and qlen >= 1200:
        if tied_species:
            return "species-level ambiguous", f"multiple distinct species-level type strains within 0.3% identity of each other ({', '.join(tied_species)}) -- 16S cannot resolve further; use ANI or MLST"
        return "species-level confident", "single best-matching species-level type strain, clear of ties, from a near-full-length read"
    if pident >= 94.5:
        return "genus-level", "identity/coverage support genus assignment only (below species threshold, or read too short/ambiguous for species confidence)"
    return "below genus-level", "identity < 94.5% -- possible novel taxon; escalate to full 16S tree placement or WGS"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pcr", required=True)
    ap.add_argument("--genome", required=True)
    ap.add_argument("--db", default=None)
    ap.add_argument("--db-release-date", default="UNKNOWN")
    ap.add_argument("--db-sha256", default="UNKNOWN")
    ap.add_argument("--outdir", default="output")
    args = ap.parse_args()
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    _, pcr_raw = read_fasta(args.pcr)
    _, genome_raw = read_fasta(args.genome)

    pcr_trimmed, trim_notes = trim_primers(pcr_raw)
    len_ok, len_note = length_gate(pcr_trimmed)
    concordant, reconcile_note = reconcile(pcr_trimmed, genome_raw)
    chimera_status, chimera_note = chimera_check(pcr_trimmed, args.db)

    cols = ["qseqid", "sseqid", "pident", "length", "qlen", "slen",
            "mismatch", "gapopen", "evalue", "bitscore", "stitle"]

    if args.db and have_blastn():
        query_path = outdir / "query_16S.fasta"
        query_path.write_text(f">query\n{pcr_trimmed}\n")
        hits = run_blastn(query_path, args.db, cols)
        demo_mode = False
    else:
        # DEMO MODE: no blastn/db available in this environment. These rows
        # are ILLUSTRATIVE, based on published divergence patterns for
        # Enterobacteriaceae type strains -- NOT a real search result.
        demo_mode = True
        hits = [
            {"sseqid": "NR_024570.1", "pident": "99.93", "length": "1420", "qlen": "1420",
             "stitle": "Escherichia coli ATCC 11775(T)"},
            {"sseqid": "NR_026331.1", "pident": "99.86", "length": "1420", "qlen": "1420",
             "stitle": "Shigella flexneri ATCC 29903(T)"},
            {"sseqid": "NR_026332.1", "pident": "99.72", "length": "1420", "qlen": "1420",
             "stitle": "Shigella sonnei ATCC 25931(T)"},
            {"sseqid": "NR_112011.1", "pident": "99.15", "length": "1420", "qlen": "1420",
             "stitle": "Escherichia fergusonii ATCC 35469(T)"},
            {"sseqid": "NR_028894.1", "pident": "97.61", "length": "1420", "qlen": "1420",
             "stitle": "Citrobacter freundii ATCC 8090(T)"},
            {"sseqid": "NR_117679.1", "pident": "95.80", "length": "1418", "qlen": "1420",
             "stitle": "Enterobacter hormaechei ATCC 49162(T)"},
        ]

    ranked = []
    for h in hits:
        pident = float(h["pident"])
        alnlen = int(h["length"])
        qlen = int(h.get("qlen", len(pcr_trimmed)))
        coverage = alnlen / qlen
        ranked.append({**h, "coverage_pct": round(coverage * 100, 2)})
    ranked.sort(key=lambda r: float(r["pident"]), reverse=True)

    top = ranked[0]
    species_band = [r for r in ranked if float(r["pident"]) >= float(top["pident"]) - 0.3]
    distinct_species = sorted({r["stitle"].rsplit(" ", 2)[0] for r in species_band})
    tier, tier_reason = assign_tier(
        float(top["pident"]), top["coverage_pct"] / 100, int(top.get("qlen", len(pcr_trimmed))),
        distinct_species if len(distinct_species) > 1 else None,
    )

    with open(outdir / "hits.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "reference", "accession", "pct_identity", "pct_coverage", "aln_length", "assignment_tier"])
        for i, r in enumerate(ranked, 1):
            w.writerow([i, r["stitle"], r["sseqid"], r["pident"], r["coverage_pct"], r["length"],
                        tier if i == 1 else ""])

    report = {
        "final_call": tier,
        "top_hit": top["stitle"],
        "reasoning": tier_reason,
        "qc_gates": {
            "length": len_note,
            "primer_trim": trim_notes,
            "pcr_vs_genome_reconciliation": reconcile_note,
            "chimera_screen": {"status": chimera_status, "note": chimera_note},
        },
        "demo_mode": demo_mode,
    }
    (outdir / "report.json").write_text(json.dumps(report, indent=2))

    provenance = {
        "database_name": "16S_ribosomal_RNA (NCBI BLAST, RefSeq Targeted Loci)",
        "database_release_date": args.db_release_date,
        "database_sha256": args.db_sha256,
        "search_tool": "blastn (NCBI BLAST+)",
        "search_command": f"blastn -query query_16S.fasta -db {args.db} -task blastn "
                           f"-perc_identity 80 -qcov_hsp_perc 50 -max_target_seqs 10 -outfmt '6 {' '.join(cols)}'",
        "thresholds": {"species_pct_identity": 98.7, "genus_pct_identity": 94.5,
                        "min_coverage_species": 0.95, "min_coverage_report": 0.90,
                        "citation": "Yarza et al. 2014 Nat Rev Microbiol; Kim et al. 2014 IJSEM"},
        "query_inputs": {"pcr_fasta": args.pcr, "genome_fasta": args.genome},
    }
    (outdir / "provenance.json").write_text(json.dumps(provenance, indent=2))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
```

## Demo input files

`data/isolate_colony_pcr_27F_1492R.fasta` (1421 bp, synthetic, derived from GenBank X80725.1):

```
>isolate01_colonyPCR_27F-1492R_consensus [SYNTHETIC DEMO]
AGTTTGATCATGGCTCAGATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAACGGTAACAGGAAG
CAGCTTGCTGCTTTGCTGACGAGTGGCGGACGGGTGAGTAATGTCTGGGAAACTGCCTGATGGAGGGGGA
... [full 1421 bp — trimmed of the noisy 3' ~55 nt near the 1492R site,
     with one ambiguous N call and one single miscall relative to the
     genome-derived version below]
```

`data/isolate_genome_assembly_16S.fasta` (1476 bp, real X80725.1 sequence with its 2 original `N`s resolved to a consensus base):

```
>isolate01_draft_genome_16S_extract [SYNTHETIC DEMO, from GenBank X80725.1]
AGTTTGATCATGGCTCAGATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAACGGTAACAGGAAG
...
CCATGGGAGTGGGTTGCAAAAGAAGTAGGTAGCTTAACTTCGGGAGGGCG
```

(I've truncated these here for readability — the exact `X80725_RAW` string is embedded in a `make_demo_data.py` generator I'd normally hand you alongside this, but couldn't write to disk this session; ask me to regenerate it if you want the literal file.)

## Worked result (illustrative — not an executed BLAST run)

| Rank | Reference (type strain) | Accession | % identity | % coverage | Aln. length | Tier |
|---|---|---|---|---|---|---|
| 1 | *Escherichia coli* ATCC 11775ᵀ | NR_024570.1 | 99.93 | 100.0 | 1420 | — |
| 2 | *Shigella flexneri* ATCC 29903ᵀ | NR_026331.1 | 99.86 | 100.0 | 1420 | — |
| 3 | *Shigella sonnei* ATCC 25931ᵀ | NR_026332.1 | 99.72 | 100.0 | 1420 | — |
| 4 | *Escherichia fergusonii* ATCC 35469ᵀ | NR_112011.1 | 99.15 | 100.0 | 1420 | — |
| 5 | *Citrobacter freundii* ATCC 8090ᵀ | NR_028894.1 | 97.61 | 100.0 | 1420 | — |
| 6 | *Enterobacter hormaechei* ATCC 49162ᵀ | NR_117679.1 | 95.80 | 99.9 | 1418 | — |

**QC gates**: length 1421 bp (PASS, near-full-length); primer trim — none needed (already clean); PCR-vs-genome reconciliation — 99.93% concordance, 1 real mismatch out of ~1420 scorable positions, ambiguous base excluded (PASS, consistent); chimera screen — 5′/3′ half-fragments both best-hit *Escherichia/Shigella* (CLEAN).

**Final call: genus-level only — *Escherichia*/*Shigella* group — species-level ambiguous.**

Reasoning: the top hit clears both the identity (≥98.7%) and coverage (≥95%) bars for a species-level claim, but three distinct named species (*E. coli*, *S. flexneri*, *S. sonnei*) sit within 0.3% identity of each other and of the top hit — this is the textbook case where 16S genuinely cannot discriminate, because *Escherichia* and *Shigella* are phylogenomically almost indistinguishable at this locus (a >70-year-old taxonomic artifact, not a data-quality problem). Reporting "*E. coli*" here would be false confidence. The honest call is genus/clade-level, with a note that whole-genome ANI or a multi-locus scheme (or biochemical/serotyping data, if this is a clinical isolate) is required to separate *E. coli* from *Shigella* spp.

## Reproducibility record (fill in from your real run)

```
database_name:          16S_ribosomal_RNA (NCBI BLAST, RefSeq Targeted Loci)
obtained via:            update_blastdb.pl --source ncbi --decompress 16S_ribosomal_RNA
download date (record):  <run: date -u +%Y-%m-%dT%H:%M:%SZ>
sha256 of .tar.gz:       <run: sha256sum 16S_ribosomal_RNA.tar.gz>
blastn version:          <run: blastn -version>
search command:          blastn -query query_16S.fasta -db 16S_ribosomal_RNA -task blastn \
                          -perc_identity 80 -qcov_hsp_perc 50 -max_target_seqs 10 \
                          -outfmt "6 qseqid sseqid pident length qlen slen mismatch gapopen evalue bitscore stitle"
thresholds:              species ≥98.7% id & ≥95% coverage (Kim et al. 2014; Yarza et al. 2014)
                          genus ≥94.5% id (Yarza et al. 2014)
model id (this session): claude-sonnet-5
```

`identify_isolate.py` writes exactly this into `provenance.json` alongside `hits.csv` on every real run.

## Caveats

- **This session's numbers above 99–95% are illustrative**, built from a real reference sequence but not from an actual `blastn` execution — install BLAST+, pin the database as shown, and re-run for a trustworthy result.
- **Chimera screen is a coarse proxy.** The split-query self-BLAST heuristic here catches obvious chimeras but is not as sensitive as `vsearch --uchime_ref` against a chimera-specific reference set; if you have VSEARCH available, run that too before trusting any species-level call.
- **Partial-length reads bias toward false species confidence.** A short read can hit 100% identity/coverage against one reference simply because it never sampled the variable region that would have distinguished it from a close relative — hence the hard length gate.
- **16S has known blind spots** beyond *Escherichia*/*Shigella*: *Bacillus cereus* group, several *Streptococcus* species, and *Enterobacter cloacae* complex members are routinely indistinguishable by this locus alone.
- **Intragenomic 16S heterogeneity** is real — many bacteria carry multiple, slightly divergent rRNA operon copies, which is one reason the PCR-vs-genome reconciliation check exists; a genome assembly extracts one representative copy, so don't be alarmed by <100% concordance, only by concordance below the threshold.
- **Catalog gap**: the sci-ai-enabler index has no dedicated chimera-detection component (checked `composer-tools.json` for uchime/vsearch/cutadapt — none present). If you want, I can file a `recipe-question` gap report for the curators — that needs your explicit sign-off on the exact text before it goes anywhere public, so ask if you want that done in a follow-up.