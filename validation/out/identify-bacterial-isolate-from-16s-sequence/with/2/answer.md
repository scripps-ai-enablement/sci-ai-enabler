File writes need approval I don't have in this session, so I'll deliver the complete pipeline inline instead.

## Reference database — pin the exact version

```bash
mkdir -p db && cd db
update_blastdb.pl --decompress 16S_ribosomal_RNA   # NCBI curated 16S rRNA (Bacteria/Archaea) DB
blastdbcmd -db 16S_ribosomal_RNA -info > db_info.txt
md5sum 16S_ribosomal_RNA*.gz > db_checksums.txt
date -u +"%Y-%m-%dT%H:%M:%SZ" > db_download_timestamp_utc.txt
```

Use this DB, not `nt`: it's built from the RefSeq Targeted Loci project, its `stitle` field tags type-strain entries with `(T)`, and it excludes the bulk of the misannotated/uncultured environmental-clone records that pollute `nt`. `db_info.txt` + the checksum + timestamp is your reproducibility record — keep those three files with the results forever.

## Step 1 — trim primers, don't trust raw Sanger ends

```bash
cutadapt -g AGAGTTTGATCMTGGCTCAG \
         -a AAGTCGTAACAAGGTARCCGTA \
         -e 0.1 --discard-untrimmed -m 200 \
         -o sanger_trimmed.fasta sanger_contig.fasta
```

## Step 2 — extract the 16S copy from the draft genome

```bash
barrnap --kingdom bac --quiet genome_assembly.fasta > rrna.gff
seqkit subseq --gtf rrna.gff genome_assembly.fasta | seqkit grep -r -n "16S" > genome_16S.fasta
```

Draft genomes often carry several rRNA operons; extract all copies, not just one — divergence between a strain's own operon copies above ~1% is itself a QC flag (contamination, misassembly, or genuine intragenomic heterogeneity).

## Step 3 — length/coverage gate (kills false confidence from partial reads)

```bash
seqkit fx2tab -nl sanger_trimmed.fasta genome_16S.fasta
```

Require **≥1200 bp aligned and ≥98% query coverage** before any species-level claim is allowed downstream. Below that, the result is capped at genus level regardless of identity.

## Step 4 — chimera screen against the same reference set

```bash
blastdbcmd -db db/16S_ribosomal_RNA -entry all -outfmt "%f" > db/16S_ribosomal_RNA.fasta
vsearch --uchime_ref query_all.fasta --db db/16S_ribosomal_RNA.fasta \
        --nonchimeras query_nonchimeric.fasta --chimeras query_chimeric.fasta \
        --uchimeout uchime.tab
```

Anything landing in `query_chimeric.fasta` gets no identification — re-sequence/re-assemble instead of reporting a number.

## Step 5 — cross-check Sanger read against the genome-derived copy

```bash
blastn -query sanger_trimmed.fasta -subject genome_16S.fasta \
       -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore"
```

The two should agree at >99% identity, ~100% coverage. Disagreement means one of them is wrong (mixed colony, contig misassembly, wrong primer read) — resolve this before trusting either against the reference DB.

## Step 6 — search, rank, and call

```bash
blastn -query query_nonchimeric.fasta -db db/16S_ribosomal_RNA \
       -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs stitle" \
       -max_target_seqs 20 -perc_identity 90 > blast_hits.tsv
```

Sort by `pident` desc, then `bitscore` desc, keep top ~15–20, join `qcovs` and parse the type-strain flag `(T)` out of `stitle`.

**Call logic** (Chun et al. 2018 / Yarza et al. 2014):

| Top-hit identity | Coverage / length | Call |
|---|---|---|
| ≥98.7% | ≥98% cov, ≥~1300 bp | Same species as top type strain **only if** the next-best type strain is >0.3% lower; otherwise report "unresolved species complex" |
| 95.0–98.6% | ≥98% cov | Same genus, likely undescribed species |
| <95.0% | — | Family/order only — flag as possible novel genus |
| any | <1200 bp aligned or <95% cov | No species call — genus-level only, state why |

## Worked illustrative example (not your real isolate — format only)

Assumed input: 1,465 bp trimmed Sanger contig + 1,522 bp genome-extracted copy, both passing chimera and length gates, agreeing at 99.9% to each other.

| Rank | Accession | Type strain | %ID | Aln len | Qcov% | Call basis |
|---|---|---|---|---|---|---|
| 1 | NR_xxxxxx | *Bacillus velezensis* DSM 7ᵀ | 99.86 | 1461/1465 | 100 | above species threshold |
| 2 | NR_xxxxxx | *Bacillus amyloliquefaciens* DSM 7ᵀ | 99.79 | 1461/1465 | 100 | within 0.07% of top hit |
| 3 | NR_xxxxxx | *Bacillus subtilis* subsp. *subtilis* NCIB 3610ᵀ | 99.52 | 1458/1465 | 100 | within 0.34% of top hit |

**Reported call:** Genus-level confident (*Bacillus*, ≥99.5% to multiple congeners); species-level **not** resolvable from 16S alone — the *B. subtilis* operational group is known to be under-resolved by this locus. Since a draft genome is already in hand, the correct next step isn't a better 16S database, it's **ANI (FastANI) or GTDB-Tk against GTDB** using the assembly, which will cleanly separate these species where 16S can't.

## Reproducibility record to keep with every result

- DB name + build date from `blastdbcmd -info`, plus the checksum/timestamp files above
- `blastn`/`vsearch`/`cutadapt`/`barrnap` versions (`--version`)
- Exact command lines used (the script above, verbatim)
- Query sequence hash (`sha256sum`) and its trimming log

Send me the actual FASTA files (Sanger contig + assembly) in a follow-up and I'll run this for real and give you the true ranked table and call instead of the illustrative one above.