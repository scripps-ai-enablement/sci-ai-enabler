---
title: Identify a bacterial isolate from its 16S rRNA sequence
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-04
summary: Use the BLAST MCP server to search a Sanger 16S rRNA read against a pinned reference database and assign genus/species by the standard identity thresholds.
---

# Identify a bacterial isolate from its 16S rRNA sequence

Hand Claude Code a 16S rRNA gene sequence from a bacterial isolate (a colony-PCR Sanger read or an assembled 16S contig) and get back a ranked table of the closest named reference organisms, with percent identity and coverage interpreted against the accepted species/genus thresholds — anchored to the exact reference-database release you searched.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You picked a colony, ran 16S colony PCR with the universal primers (27F/1492R), and got back a Sanger read (or you pulled the 16S gene out of a draft assembly). The everyday microbiology question is "what is this?" The canonical answer is a similarity search of the 16S sequence against a curated database of type-strain 16S sequences, then reading the top hit against the accepted thresholds: **≥98.7% identity** to a type strain supports a species-level match, and **~94.5–95%** supports genus level; below that you may be looking at a novel taxon ([Kim et al., *Int. J. Syst. Evol. Microbiol.* 2014](https://doi.org/10.1099/ijs.0.059774-0); [Yarza et al., *Nat. Rev. Microbiol.* 2014](https://doi.org/10.1038/nrmicro3330)).

The mechanics are a `blastn` search, but the footguns are real: trusting a top hit that only covers half the read (a chimeric or truncated Sanger trace); reporting "species X" off a 96% hit that only supports genus; searching the general `nt` database (full of misannotated environmental clones) instead of a curated type-strain 16S set; and — the reproducibility killer — not recording which database release the call came from, so it can't be re-checked when the database moves. "Solved" looks like: point the agent at your 16S FASTA and one pinned 16S reference database, get back a `hits.csv` ranked by identity with coverage and a threshold-based `assignment` column, plus a provenance record naming the exact database release.

## Recommended approach

1. **Install the [BLAST (Bio-MCP) server](../../catalog/tools/blast.html).** It wraps NCBI BLAST+ and exposes `makeblastdb`, `blastn`, and `blastp` as MCP tools. Follow the catalog page's clone-and-`pip install -e .` steps and register it with `claude mcp add`. The BLAST+ binaries must be on `PATH` first.

2. **Download and pin a curated 16S reference database.** Use NCBI's targeted **`16S_ribosomal_RNA`** BLAST database (type-strain and reference 16S sequences), fetched with the BLAST+ helper:

   ```
   update_blastdb.pl --decompress 16S_ribosomal_RNA
   ```

   **Record the release date** printed by `update_blastdb.pl` (the set is versioned by NCBI build date) and compute a `sha256` of the downloaded `.tar.gz`. These are your pinned inputs. (SILVA or the GTDB 16S export are equally valid pinned alternatives — pick one and record its release.)

3. **Confirm the read is clean before searching.** A raw Sanger trace has low-quality ends and may need reverse-complementing; a good 16S query is ~1,300–1,500 bp of unambiguous sequence. Trim obvious low-quality tails and drop reads with excessive `N`s — a short or chimeric query produces confident-looking but wrong hits.

4. **Have the agent run the search into a committed script.** A prompt:

   ```
   Using the bio-blast MCP server, write me a script identify_16s.py that:
     1. Runs blastn of my query (query_16s.fasta) against the local
        16S_ribosomal_RNA database, with -perc_identity 90,
        -max_target_seqs 10, and outfmt 6 (qseqid sseqid pident length
        qlen slen mismatch gapopen evalue bitscore stitle).
     2. Computes query coverage = length / qlen for each hit and keeps
        hits with coverage >= 0.90.
     3. Sorts hits by pident (then bitscore) and writes hits.csv with
        the reference accession, organism name (from stitle), pident,
        coverage, alignment length, and evalue.
     4. Adds an `assignment` column per the standard thresholds:
        pident >= 98.7 -> "species-level"; 94.5 <= pident < 98.7 ->
        "genus-level"; pident < 94.5 -> "below genus / possible novel".
     5. Writes provenance.json: BLAST+ version, the 16S database
        release date and .tar.gz sha256, the query_16s.fasta sha256,
        the identity/coverage cutoffs, run date, and model id.
   Commit identify_16s.py; do not paste results back as prose I
   can't audit.
   ```

   Pin the environment with a `requirements.txt` (BLAST+ via conda, plus `pandas`). Keep `identify_16s.py`, the pinned env, and `provenance.json` under version control alongside the query FASTA and the database release string + hash.

5. **Read the assignment critically.** A single 16S gene resolves genus reliably but often cannot separate closely related species (e.g., within *Bacillus* or the *Enterobacteriaceae*), where multiple references tie at >99%. Treat a species-level call from 16S alone as provisional: if the top few hits are different species at near-identical identity, report the genus and flag the ambiguity. Definitive species delineation needs whole-genome average nucleotide identity (ANI) or multi-locus typing, not 16S.

6. **Re-run and hand off.** Because the database release and cutoffs are pinned in `provenance.json`, re-running `identify_16s.py` reproduces the assignment until you deliberately bump the database (which the provenance record makes visible). The identified organism name feeds the genus/species hint of the [bacterial-genome-annotation recipe](annotate-a-bacterial-genome.html); the 16S sequence itself can join a set for the [phylogenetic-tree recipe](build-phylogenetic-tree-from-sequences.html) to place the isolate among relatives.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged MCP server does the whole job. Plain Claude Code (rung 1) can shell out to `blastn`, but the BLAST MCP gives the agent first-class `makeblastdb`/`blastn` tools and keeps the invocation and the pinned database release auditable, which is exactly what makes an identification reproducible. Rung 3+ is unnecessary: a similarity search of one gene against one curated database, read against published thresholds, is a single well-bounded step. This recipe is the single-isolate identification counterpart to the community-level [16S diversity recipe](compute-16s-microbiome-diversity.html) and the multi-isolate [resistome screen](screen-genome-for-resistance-and-virulence-genes.html) — different question, same BLAST-MCP tool.

## Availability

Fully open. The BLAST MCP server is MIT-licensed and BLAST+ is public-domain NCBI software. The `16S_ribosomal_RNA` database is freely downloadable from NCBI; SILVA and GTDB alternatives are free for academic use (check SILVA's terms for commercial use). All computation runs locally on your sequence — no account, no API key, no upload.

## Compute requirements

Laptop-sufficient. The `16S_ribosomal_RNA` database is a few hundred MB; a single `blastn` of one ~1.5 kb query against it returns in seconds on a modern laptop with 8 GB RAM. No GPU. Batch-identifying a plate of hundreds of colony reads is embarrassingly parallel — loop the same script per query, or pass a multi-FASTA and group results by `qseqid`.

## Evidence

Reported. 16S rRNA similarity search for isolate identification is one of the most-used procedures in microbiology, and the identity thresholds this recipe applies are the community-standard reference points: **98.7% for species** and **~94.5% for genus** ([Kim et al., *Int. J. Syst. Evol. Microbiol.* 64:346 (2014)](https://doi.org/10.1099/ijs.0.059774-0); corroborated by the SILVA-scale analysis of [Yarza et al., *Nat. Rev. Microbiol.* 12:635 (2014)](https://doi.org/10.1038/nrmicro3330)). Countless species-description and isolate-characterization papers run exactly this `blastn`-against-a-curated-16S-database step (e.g., the type-strain characterizations returned for any new *sp. nov.*, which report the top 16S identity before confirming with ANI/dDDH).

No head-to-head benchmark of the *agent-driven* BLAST-MCP assembly versus a hand-typed `blastn` command is published — the MCP loop buys first-class BLAST tools, a pinned database release, and a recorded provenance file, not a new method. The underlying BLAST+ homology search and the identity thresholds are the validated components; the recipe's contribution is making the call reproducible.

## Alternatives considered

- **Plain Claude Code, no MCP (rung 1).** Fine if BLAST+ is already installed; the MCP gives the agent structured `makeblastdb`/`blastn` tools and a cleaner audit trail. Reach for rung 1 for a single one-off lookup you will not repeat.
- **NCBI web BLAST against `nt` (no agent).** Convenient but two traps: the general `nt` database is polluted with misannotated environmental clones, so a curated 16S set is safer, and a web run leaves no pinned-release provenance. Use the web tool for a quick eyeball; use this recipe when the identification goes in a record.
- **Whole-genome ANI / MLST for definitive species calls.** When 16S ties several species (common), reach for average nucleotide identity against reference genomes or multi-locus sequence typing. Neither an ANI tool (fastANI/pyani) nor an MLST caller is catalogued as a Claude tool today — surfaced as a missing component to the catalog curator. 16S identification is the fast first pass; ANI is the confirmation.

## See also

- [BLAST (Bio-MCP)](../../catalog/tools/blast.html) — the MCP server this recipe drives.
- [Screen a bacterial genome for resistance and virulence genes](screen-genome-for-resistance-and-virulence-genes.html) — the same BLAST-MCP tool on predicted proteins.
- [Annotate a single bacterial genome assembly](annotate-a-bacterial-genome.html) — consumes the genus/species hint this recipe produces.
- [Build a phylogenetic tree from a set of sequences](build-phylogenetic-tree-from-sequences.html) — place the isolate's 16S among its relatives.
- [Compute 16S microbiome alpha/beta diversity from a BIOM table](compute-16s-microbiome-diversity.html) — the community-level counterpart.

## Sources

- [Kim et al., "Towards a taxonomic coherence between average nucleotide identity and 16S rRNA gene sequence similarity for species demarcation of prokaryotes," *Int. J. Syst. Evol. Microbiol.* 64:346–351](https://doi.org/10.1099/ijs.0.059774-0) — the 98.7% species threshold; published 2014; verified 2026-07-04 (this run).
- [Yarza et al., "Uniting the classification of cultured and uncultured bacteria and archaea using 16S rRNA gene sequences," *Nat. Rev. Microbiol.* 12:635–645](https://doi.org/10.1038/nrmicro3330) — genus/species identity boundaries at SILVA scale; published 2014; verified 2026-07-04 (this run).
- [NCBI BLAST `16S_ribosomal_RNA` database (`update_blastdb.pl`)](https://blast.ncbi.nlm.nih.gov/) — curated type-strain/reference 16S set; verified 2026-07-04 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=identify-bacterial-isolate-from-16s-sequence&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fidentify-bacterial-isolate-from-16s-sequence.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
