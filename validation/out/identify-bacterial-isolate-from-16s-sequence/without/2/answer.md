## Assumption (no input files were found in the working directory)

Since this session has no FASTA/AB1/assembly files attached, I'll work from a concrete, realistic stand-in so the method and deliverable are fully specified:

- **Sanger 16S**: forward read from 27F (~900 usable bp after trimming) and reverse read from 1492R (~850 usable bp), assembled into a **1,420 bp consensus** spanning the near-full-length V1–V9 region.
- **Genome-derived 16S**: extracted from a draft assembly (e.g., via `barrnap`), **1,536 bp**, full-length.
- Isolate: unknown Gram-negative rod, aerobic, from an environmental/clinical source (arbitrary — swap in your actual phenotype).

Everything below is a runnable pipeline; the final table uses illustrative numbers I've clearly labeled as placeholders. Replace the two input files and the pipeline reproduces a real, reproducible result.

---

## 1. Build a trustworthy query sequence first

Most bad 16S calls come from a bad query, not a bad database.

**a) Assemble/trim the Sanger reads (don't BLAST raw traces):**
```bash
# Quality-trim both reads (Phred >20), reverse-complement the 1492R read
seqkit seq -Q 20 27F.ab1.fastq > 27F.trim.fastq
seqkit seq -Q 20 1492R.ab1.fastq -r -p > 1492R.rc.trim.fastq

# Assemble into one consensus contig (Cap3 or a simple overlap merge)
cap3 <(cat 27F.trim.fastq 1492R.rc.trim.fastq) -o 40 -p 90
```
Inspect the trace/consensus quality yourself (e.g., in Geneious/Chromas/Tracy) at the overlap — colony PCR reads commonly have messy first ~20–30 bp and degraded tails; don't trust bases below Q20.

**b) Pull the genome copy for comparison:**
```bash
barrnap --kingdom bac draft_assembly.fasta > rrna.gff
seqkit subseq --gtf rrna.gff draft_assembly.fasta | seqkit grep -r -p "16S" > genome_16S.fasta
```
If the assembly has multiple rRNA operons, extract all copies — intragenomic 16S heterogeneity (common, up to ~1% divergence in some taxa) is expected and is itself diagnostic information, not necessarily an error.

**c) Length/coverage gate before doing anything else:**
Reject or flag any query <1,300 bp (partial reads give inflated, spurious top hits) and require ≥98% mutual coverage between the Sanger consensus and the genome-derived copy before treating them as the same locus.

**d) Chimera screening (mandatory for colony PCR products):**
```bash
vsearch --uchime2_ref query.fasta --db rdp_gold.fasta \
        --uchimeout query.uchime.tsv --mode balanced
```
Use RDP's curated "Gold" chimera-free reference set for this step, not your search database — discard/flag the read if uchime2 calls it chimeric (common artifact of mixed colonies or heteroduplex formation during PCR).

---

## 2. Reference database — curated, versioned, no environmental clones

Avoid `nt`/`nr` — they're full of misannotated/unclassified environmental clone sequences that inflate false top-hit confidence. Use one of, in order of preference:

| Database | Why | Version pinning |
|---|---|---|
| **EzBioCloud 16S DB** | Gold standard: curated, type-strain-anchored, used for the field's standard species thresholds | Note DB release tag (e.g. `PKSSU4.0`) shown on each report |
| **NCBI 16S ribosomal RNA (Bacteria and Archaea)** — the RefSeq Targeted Loci project | Free, BLAST-ready, restricted to curated/type-associated records (not raw GenBank submissions) | `update_blastdb.pl` prints a build date; record it |
| **SILVA SSURef NR99** (only if the above are unavailable) | Larger coverage, but includes environmental/uncultured entries — must post-filter to type strains | Pin exact release, e.g. `SILVA_138.2` |

For this pipeline, use the NCBI targeted-loci BLAST DB since it's scriptable and reproducible offline:
```bash
update_blastdb.pl --decompress 16S_ribosomal_RNA
# record exact provenance:
blastdbcmd -db 16S_ribosomal_RNA -info > 16S_db_provenance_2026-07-30.txt
md5sum 16S_ribosomal_RNA.* >> 16S_db_provenance_2026-07-30.txt
```
`blastdbcmd -info` prints the DB build date and sequence count — save that file next to your results. That's your reproducibility record; anyone rerunning this later reruns against the identical DB snapshot, not whatever NCBI has that day.

---

## 3. Search

```bash
blastn -task megablast -db 16S_ribosomal_RNA \
  -query query_consensus.fasta \
  -out hits.tsv -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore stitle" \
  -max_target_seqs 10 -perc_identity 90
```
`-perc_identity 90` is a coarse floor only, to keep the hit table from being dominated by garbage; the real cutoffs are applied at the interpretation step below, not the search step.

---

## 4. Interpretation thresholds (standard, citable)

- **Species-level assignment**: top hit ≥ **98.7–99.0%** identity to a type-strain sequence (Stackebrandt & Ebers 2006; Chun et al. 2018 minimal standards), **and** query coverage ≥ **~1,300 bp aligned** (near-full-length). Below this length, treat any "species" call as provisional only.
- **Genus-level assignment**: top hit ≥ **95%** identity but below the species threshold, or species threshold met with length <1,300 bp (Yarza et al. 2014).
- **Ambiguous / needs a second marker**: top two (or more) hits are within **0.5 percentage points** of each other, or the isolate falls in a genus known to be 16S-indistinguishable at species level (e.g., *Bacillus cereus* group, *Escherichia*/*Shigella*, *Streptococcus mitis* group, many *Enterobacter*/*Klebsiella* pairs). In that case, report genus-level only and recommend ANI (≥95–96% = same species) or a housekeeping gene (*gyrB*, *rpoB*) / whole-genome comparison instead of pushing 16S further than it resolves.

---

## 5. Deliverable: ranked hits table

**Illustrative output** (placeholder numbers — substitute your real BLAST results):

| Rank | Query cov (bp / %) | %Identity | E-value | Type strain hit | Assignment |
|---|---|---|---|---|---|
| 1 | 1,420 / 100% | 99.86% | 0.0 | *Pseudomonas putida* KT2440ᵀ (NR_119332.1) | Species-level (meets ≥98.7%, full length) |
| 2 | 1,420 / 100% | 98.94% | 0.0 | *Pseudomonas monteilii* CIP 104883ᵀ | Below top hit by 0.92 pt — not a competing call |
| 3 | 1,420 / 99% | 97.11% | 0.0 | *Pseudomonas plecoglossicida* NBRC 103162ᵀ | Genus-level only |
| 4 | 1,420 / 99% | 96.80% | 0.0 | *Pseudomonas mosselii* CFML 90-83ᵀ | Genus-level only |

**Call**: *Pseudomonas putida* (species-level, high confidence) — gap to the next-best type strain (0.92 pt) exceeds the 0.5 pt ambiguity margin, and coverage is full-length on both the Sanger consensus and the genome-extracted copy (concordant, <0.1% pairwise difference between the two query versions).

**Reproducibility record to keep alongside this table:**
- Query: `query_consensus.fasta` (SHA256: `<hash>`), assembled from 27F/1492R Sanger reads + independently from `draft_assembly.fasta` via `barrnap`
- Chimera check: `vsearch --uchime2_ref` v2.x vs RDP Gold, result: not chimeric
- Database: NCBI `16S_ribosomal_RNA` targeted-loci BLAST DB, build date/sequence count from `blastdbcmd -info`, MD5 of DB files
- Search: `blastn` (BLAST+ version), `-task megablast`, `-perc_identity 90`, `-max_target_seqs 10`
- Thresholds applied: species ≥98.7% + ≥1,300 bp; genus ≥95%; ambiguity margin 0.5 pt (Stackebrandt & Ebers 2006; Chun et al. 2018; Yarza et al. 2014)

---

## What to change for your real data

Send me the two Sanger trace files (or the assembled consensus FASTA) and the genome assembly (or its extracted 16S contig), and I'll run this exact pipeline — assembly/trim → chimera check → BLAST against a pinned database snapshot → thresholded call — and hand back the real table with the actual provenance file instead of the placeholders above.