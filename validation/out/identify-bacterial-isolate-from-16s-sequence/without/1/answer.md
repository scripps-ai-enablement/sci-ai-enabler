The directory is empty — no sequence files were provided, so per your instruction I'm proceeding on a stated, concrete assumption rather than asking you to supply the FASTA. Here is the full workflow, with exact commands, thresholds, and a reproducibility record, illustrated with a labeled example.

## Assumption (stated explicitly)

You have two FASTA files for the same isolate:
- `colony_pcr_27F1492R.fasta` — Sanger consensus from colony PCR with 27F/1492R, ~1420 bp, one contig, no ambiguous-base runs at the ends (i.e., already primer-trimmed of vector/primer artifact but not necessarily of low-quality tails).
- `genome_16S_extracted.fasta` — a 16S copy pulled out of a draft assembly (e.g., via `barrnap` or `RNAmmer`), possibly one of several rRNA operons in that genome.

Organism identity is unknown (e.g., a Gram-negative rod from an environmental or clinical enrichment). I'm not fabricating a real BLAST result — actual identity requires running this pipeline on your real sequence — but I'll show the exact output format you should get, with clearly labeled illustrative numbers.

## Step 0 — QC before any search (this is where false confidence usually creeps in)

1. **Trim to quality, not just to primer.** If you have the `.ab1` trace, quality-trim with a Phred cutoff (Q20) rather than trusting the whole consensus — Sanger reads degrade badly in the last 50–100 bp:
   ```bash
   seqkit seq -M 1600 -m 1200 colony_pcr_27F1492R.fasta   # sanity length filter
   ```
2. **Length/coverage gate.** Require ≥ ~1300 bp of usable sequence spanning most of the 27F–1492R amplicon before trusting a species-level call. Partial reads (e.g., only V1–V3, <500–800 bp) can still give a genus call but should never be reported as species-level — this is the single most common source of false confidence in 16S IDs (Janda & Abbott, 2007).
3. **Reconcile the two sources.** Align the PCR amplicon against the assembly-extracted copy:
   ```bash
   mafft --auto <(cat colony_pcr_27F1492R.fasta genome_16S_extracted.fasta) > aligned.fasta
   ```
   - If they differ by 1–2 bp over ~1400 bp, that's normal intragenomic rRNA-operon microheterogeneity (most bacteria carry multiple, slightly divergent copies) — not a problem.
   - If they differ by many scattered SNPs or an internal breakpoint where the first half matches one lineage and the second half matches another, suspect a **PCR chimera** formed between two different rRNA operon copies within the same genome, or cross-contamination in the colony pick. Don't proceed to a species call until this is resolved.
   - If the genome has multiple rRNA operons, extract and compare all of them, not just one, so you know whether the PCR product is chimeric relative to what's actually in the genome.

## Step 1 — Chimera screening (dedicated step, not just eyeballing the alignment)

Run both sequences through a chimera detector against a chimera-free reference set before any identity search:
```bash
vsearch --uchime3_denovo colony_pcr_27F1492R.fasta --nonchimeras clean.fasta --chimeras flagged_chimeras.fasta
# or, reference-based against the Broad "gold" 16S set:
vsearch --uchime2_ref colony_pcr_27F1492R.fasta --db gold.fa --nonchimeras clean.fasta --uchimeout uchime.tsv
```
Discard or flag any read called as a chimera — don't let a chimeric read produce a confident-looking but meaningless top hit.

## Step 2 — Database choice (curated, type-strain-anchored — not raw nt)

Avoid NCBI `nt`/`nr` for this — they're full of misannotated environmental clones and mislabeled submissions. Use one of:

| Database | Why | Access |
|---|---|---|
| **NCBI "16S ribosomal RNA (Bacteria and Archaea)"** (BioProject PRJNA33175) | Curated, RefSeq Targeted Loci project, heavily weighted toward type-strain sequences, actively maintained by NCBI | `update_blastdb.pl --decompress 16S_ribosomal_RNA` or via BLAST web "16S ribosomal RNA sequences (Bacteria and Archaea)" tool |
| **EzBioCloud 16S DB** | Gold-standard type-strain-only database; the source of the Yarza/Chun identity thresholds below | Free with registration, ezbiocloud.net |

I recommend NCBI's curated 16S DB as the default here since it's freely scriptable and versioned via a dated download, which matters for your reproducibility requirement.

```bash
mkdir -p db/16S_$(date +%F)
cd db/16S_$(date +%F)
update_blastdb.pl --decompress 16S_ribosomal_RNA
blastdbcmd -db 16S_ribosomal_RNA -info > db_info.txt   # record sequence count, build date
```

## Step 3 — Search

Use classic `blastn` (not `megablast`), per NCBI's own recommendation for cross-species 16S identification — megablast's word size is tuned for near-identical/intraspecies matches and can miss valid genus-level hits:

```bash
blastn -task blastn -query clean.fasta -db db/16S_<date>/16S_ribosomal_RNA \
  -word_size 11 -evalue 1e-5 -max_target_seqs 20 \
  -outfmt "6 qseqid sseqid stitle pident length qcovs mismatch gapopen evalue bitscore" \
  -out hits.tsv
```
Do the same for `genome_16S_extracted.fasta` and confirm the two searches agree.

## Step 4 — Apply standard thresholds (Yarza et al. 2014 / Chun et al. 2018, adopted by IJSEM)

| Identity | Coverage | Call |
|---|---|---|
| ≥ 98.7% | ≥ 95% of query length aligned | Same species as top type-strain hit — but see caveat below |
| 95.0–98.65% | ≥ 95% | Same genus, distinct species (species-level call not justified) |
| < 95% | — | Likely different genus; re-check for chimera/contamination before accepting |
| Top 2+ hits within 0.1–0.3% of each other | — | Report as an ambiguous tie between those species — 16S alone cannot resolve |

**Caveat you should build in regardless of the number:** 16S is known to under-resolve species in several genera (*Bacillus*, *Streptomyces*, *Enterobacter/Klebsiella*, *Mycobacterium*, *Acinetobacter*, etc.). Since you already have a draft genome, the confirmatory step for any ≥98.7% call is **ANI or dDDH against the candidate type-strain genome**, not 16S alone:
```bash
fastANI -q your_genome.fasta -r candidate_type_strain_genome.fasta -o ani_result.txt
# ANI ≥ 95–96% with the type strain genome = confirms same species
```

## Step 5 — Ranked hits table (format — illustrative numbers, not a real result)

| Rank | Subject (type strain) | %Identity | Query Coverage | Align. Length | E-value | Assignment |
|---|---|---|---|---|---|---|
| 1 | *Pseudomonas putida* NBRC 14164ᵀ | 99.86% | 100% | 1418/1420 | 0.0 | Species-level match (≥98.7%, ≥95% cov) |
| 2 | *Pseudomonas monteilii* CIP 104883ᵀ | 98.9% | 100% | 1405/1420 | 0.0 | Below tie threshold vs. rank 1; secondary candidate |
| 3 | *Pseudomonas fulva* NRIC 0180ᵀ | 97.3% | 99% | 1390/1420 | 0.0 | Genus-level only |

Report only rows that pass the QC/chimera gates above; if the read fails length or chimera screening, report a genus-level call at most and say so explicitly, don't let a low-quality read masquerade as a species ID.

## Step 6 — Reproducibility record (write this to a log file alongside the results)

```
Date of analysis:        2026-07-30
Query files:             colony_pcr_27F1492R.fasta (md5: <run md5sum>)
                          genome_16S_extracted.fasta (md5: <run md5sum>)
Chimera check:            vsearch v2.x, --uchime2_ref against gold.fa
Reference database:       NCBI 16S ribosomal RNA (Bacteria and Archaea), BioProject PRJNA33175
DB download date:         2026-07-30 (record update_blastdb.pl timestamp)
DB sequence count:        <from blastdbcmd -info>
Search tool/version:      blastn 2.x (BLAST+), task=blastn, word_size=11, evalue=1e-5
Threshold scheme:         Yarza et al. 2014 / Chun et al. 2018 (98.7% species / 95% genus)
Confirmatory check:       fastANI vs. top type-strain genome (if ≥98.7% 16S hit)
```

Keep this block per isolate — it's what lets you or a reviewer reproduce the exact call later even after the NCBI database is updated.

**What I'd need from you to actually run this**, when you have it: the real FASTA content (or `.ab1` trace) for both sequences. Paste them in a new request and I can execute the QC → chimera → BLAST → threshold pipeline end-to-end and fill in the table with real numbers instead of the illustrative ones above.