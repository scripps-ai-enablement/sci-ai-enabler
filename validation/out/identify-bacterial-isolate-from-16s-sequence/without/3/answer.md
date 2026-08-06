File writes need approval I can't count on in a single-shot exchange, so I'll deliver everything inline instead. Here's the full protocol, thresholds, script, and worked example.

## Assumption (stated up front, since I have no file to read)

Your working directory is empty — no FASTA/AB1/genome file was attached. I'm assuming:
- `sanger_consensus.fasta` — a ~1,420 bp 27F/1492R Sanger consensus (near-full-length V1–V9)
- `genome_16S.fasta` — a ~1,540 bp 16S copy extracted from the draft assembly (e.g., via `barrnap`)
- Both belong to the same isolate, and you want one reconciled species/genus call from the two.

Everything below is written so you can drop in your real files and re-run it exactly as-is.

## 1. Database choice — the part that actually prevents "false confidence"

**Do not** search raw `nt`/GenBank. It's full of unculturable-clone entries, mislabeled deposits, and near-duplicate strain records that inflate apparent identity without a curated species anchor. Use one of these instead, and pin the version:

| DB | Why it fits | Version pinning |
|---|---|---|
| **NCBI "16S ribosomal RNA (Bacteria and Archaea)"** targeted-loci project (BioProject PRJNA33175) | Curated submissions only (RefSeq-associated + type-material flagged), no environmental clones | `update_blastdb.pl 16S_ribosomal_RNA`, record `blastdbcmd -db 16S_ribosomal_RNA -info` output + download timestamp + checksum |
| **LTP (All-Species Living Tree Project, SILVA)** | Type strains *only*, curated tree, explicit dated releases (e.g. `LTP_10_2023`) | The release string is the version; record it verbatim + sha256 of the download |

Recommendation: run against **both** — NCBI targeted-loci as primary (broader coverage of recently named species), LTP as a type-strain-only cross-check. If the two disagree, trust LTP's identity but flag it.

## 2. QC gates before trusting any number

1. **Length/coverage gate**: require ≥1,300 bp aligned and ≥98% query coverage before allowing a species-level claim. Below that (partial reads, single hypervariable region), cap the call at genus-level — short reads systematically misclassify at species resolution (Yarza et al. 2014, *Nat Rev Microbiol*).
2. **Primer trim**: strip residual 27F (`AGAGTTTGATCMTGGCTCAG`) / 1492R (`TACGGYTACCTTGTTACGACTT`) with `cutadapt -e 0.1 --discard-untrimmed` — untrimmed primer tails deflate identity scores.
3. **Cross-validate Sanger vs. genome copy**: `blastn -task blastn` the two sequences against each other. Expect ≥99.5% identity/full coverage. A bigger gap means either a chimeric Sanger read, a sequencing error, or (legitimately) an isolate carrying divergent *rrn* operon paralogs — don't average over it silently, report it.
4. **Chimera screen**: `vsearch --uchime_ref` (not `--uchime_denovo` — that mode needs multi-sample abundance data you don't have for a single isolate) against the same curated DB. Discard/flag anything called chimeric before it ever reaches the ranking step.
5. **Split-half sanity check**: BLAST the first and last ~750 bp of the read independently. If they point to different genera at high identity/coverage individually, that's a chimera signature the whole-read search can mask.

## 3. Search parameters

Use classic `blastn` (`-task blastn`), **not** `megablast`/`dc-megablast` — megablast's seed heuristics are tuned for ≥95% identity and silently drop more divergent true hits, which matters exactly when you're trying to catch a novel-genus call correctly.

```
blastn -task blastn -query sanger.nonchimeric.fasta -db 16S_ribosomal_RNA \
  -perc_identity 90 -qcov_hsp_perc 90 \
  -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore stitle" \
  -max_target_seqs 20 -num_threads 4 > blast_hits.tsv
```

## 4. Classification thresholds (Chun et al. 2018, *IJSEM* consensus; Kim et al. 2014)

| Result | Call |
|---|---|
| ≥98.7% identity, ≥1,300 bp aligned, ≥98% coverage | Candidate same species as top type strain — **but note 16S alone cannot confirm species below this line; ANI/dDDH is required for a final confirmatory call**, only exclude it |
| 95–98.7% identity | Same genus, distinct species — report genus-level ID, species "unresolved by 16S" |
| <95% identity | Genus-level call only; consider candidate novel genus if best hit is well below 95% |
| <1,300 bp or <98% coverage, regardless of identity | Cap any claim at genus-level — insufficient read length for species resolution |
| Chimera flag positive | Do not report an identity-based call at all; resequence/reassemble first |

## 5. Ranked hits table (illustrative — based on the assumed example, not a real search)

| Rank | Type strain | Accession | %ID | Aln len | Qcov | Chimera flag | Assignment |
|---|---|---|---|---|---|---|---|
| 1 | *Bacillus subtilis* subsp. *subtilis* DSM 10ᵀ | NR_027552.1 | 99.86 | 1418/1420 | 100% | none | Species-level: *B. subtilis* (pending ANI vs. genome assembly) |
| 2 | *Bacillus spizizenii* NRRL B-23049ᵀ | NR_112686.1 | 99.72 | 1417/1420 | 100% | none | Same-genus alternative — 16S alone can't separate from rank 1 |
| 3 | *Bacillus tequilensis* KCTC 13622ᵀ | NR_104919.1 | 99.51 | 1416/1420 | 100% | none | Same-genus alternative |
| 4 | *Bacillus licheniformis* DSM 13ᵀ | NR_118996.1 | 96.83 | 1404/1420 | 99% | none | Genus-confirmed, species excluded |
| 5 | *Bacillus altitudinis* 41KF2bᵀ | NR_042337.1 | 95.20 | 1401/1420 | 99% | none | Genus-confirmed, species excluded |

**Why this isn't a final species call as-is**: ranks 1–3 sit in the well-known *B. subtilis*/*spizizenii*/*tequilensis* complex, where 16S resolution genuinely tops out around 99.5–99.9% between valid species — this is the textbook case the 98.7% threshold exists for. The correct next step, not skippable, is **ANI or dDDH between your genome assembly and the top 2–3 type-strain genomes** (e.g., `fastANI` against RefSeq assemblies for ranks 1–3) before naming the species.

## 6. Reproducibility record (fill in for your real run)

```
Query:            sanger_consensus.fasta (SHA256: <hash>), genome_16S.fasta (SHA256: <hash>)
Primer trim:      cutadapt v<X>, 27F/1492R, -e 0.1
Chimera check:    vsearch v<X>, --uchime_ref, against DB below
Search DB:        NCBI 16S_ribosomal_RNA (BioProject PRJNA33175)
DB download date: <UTC timestamp from update_blastdb.pl run>
DB checksum:      <sha256 of downloaded db files>
Cross-check DB:   LTP_10_2023 (SILVA Living Tree Project), sha256 <hash>
Search tool:      blastn (blast+ v<X>), -task blastn, -perc_identity 90 -qcov_hsp_perc 90
Thresholds used:  Chun et al. 2018 IJSEM (98.7% species floor, 95% genus floor), Yarza et al. 2014 (length/coverage gating)
```

Record the four bolded values (query hashes, DB name+date+checksum, exact blastn command, threshold citation) every time — that's what makes the call reproducible without re-attaching files.

**What I couldn't do here**: run this against your actual sequence, since no file was provided — the ranked table above is illustrative, built around a stated assumption, not a real result. Swap in your real FASTAs and the pipeline (steps 1–5, with the exact commands given) is what to run to get the true table.