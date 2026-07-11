---
title: Quantify bulk RNA-seq FASTQ into a gene-level counts matrix
parent: All recipes
grand_parent: Recipes
nav_order: 21
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology]
evidence_level: Proposed
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-11
summary: Chain the fastp and Salmon skills, then aggregate with tximport, to turn raw bulk RNA-seq FASTQ into the gene-level counts matrix a DE analysis needs.
---

# Quantify bulk RNA-seq FASTQ into a gene-level counts matrix

Hand Claude Code raw bulk RNA-seq FASTQ files; get back trimmed reads, per-sample Salmon quantifications, and a single gene-level integer counts matrix ready for differential expression.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Laptop (no GPU) |

## Problem

Every bulk RNA-seq differential-expression analysis assumes a gene-level counts matrix already exists — but producing that matrix from raw FASTQ is the step that trips people up. The path is a short chain with sharp edges: adapter/quality trim the reads, quantify against a transcriptome with a **decoy-aware** index (so genomic multi-mappers don't inflate transcript counts), then collapse Salmon's transcript-level `quant.sf` estimates to gene level with a `tx2gene` map and `tximport` (which correctly propagates effective-length offsets — you cannot just `sum` the columns). Get the decoy or the `tx2gene` mapping wrong and every downstream log2FC is quietly biased. Solved looks like: FASTQ in; a `counts.csv` (genes × samples, raw integer counts) plus a matching `coldata.csv` out, with the transcriptome release and every flag recorded.

## Recommended approach

1. **Install the [fastp](../../catalog/tools/fastp-fastq-preprocessing.html) and [Salmon](../../catalog/tools/salmon-rna-quantification.html) skills.** Both ship in the SciAgent-Skills collection — clone once and load as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm `fastp-fastq-preprocessing` and `salmon-rna-quantification` appear under `/plugin`. Each skill installs its own dependencies on first use.

2. **Prepare inputs.** Provide paired-end FASTQ (`sample_R1.fastq.gz` / `sample_R2.fastq.gz`) per sample, a transcriptome FASTA and matching genome FASTA for the same release (e.g., GENCODE or Ensembl — note the exact version), and a `tx2gene.tsv` (transcript ID → gene ID) built from the same annotation GTF. State the organism and release up front so the index and mapping stay consistent.

3. **Trim, then quantify — captured in a committed script.** Have the assistant write the chain to a versioned `quantify_rnaseq.py` (or a Snakemake/`Makefile` if you prefer), not run it ad hoc. A minimal prompt:

   ```
   Use the fastp and salmon skills. Write quantify_rnaseq.py that, for
   each paired FASTQ under fastq/: (1) runs fastp with default adapter
   detection + quality trimming, writing trimmed reads and a JSON QC
   report per sample; (2) builds a decoy-aware Salmon index once from
   the transcriptome FASTA + genome decoys; (3) runs salmon quant in
   mapping mode with --gcBias --seqBias --validateMappings, writing
   quant/<sample>/quant.sf. Pin versions in requirements.txt.
   ```

4. **Aggregate to a gene-level counts matrix.** Continue in the same script:

   ```
   Add a step that uses tximport (type="salmon") with tx2gene.tsv to
   collapse the per-sample quant.sf files to a gene-level count matrix,
   writing counts.csv (genes x samples, raw integer counts) and a
   coldata.csv template. Record the transcriptome release and the fastp
   and salmon versions in provenance.json.
   ```

   pyroe/`tximeta` are acceptable substitutes for tximport if you stay in one language.

5. **Record provenance and commit the artifacts.** The deliverables — `quantify_rnaseq.py`, `requirements.txt` (pinned fastp/Salmon/tximport versions), the per-sample fastp JSON QC reports, `counts.csv`, and `provenance.json` (transcriptome source + release, index build flags, input FASTQ sha256, run date, model id) — all go under version control. See the [reproducibility guide](../../guide/advanced/reproducibility.md).

6. **Sanity-check before handing off.** Confirm fastp reports a reasonable pass rate and Salmon's mapping rate is in the expected band (typically >70% for a clean library); a low mapping rate usually means the wrong transcriptome release or contamination, not a downstream problem.

## Why this assembly

Rung 3 of the simplicity ladder — a two-skill toolbelt plus a tximport aggregation step. Rung 2 (one skill) doesn't cover it: trimming (fastp) and quantification (Salmon) are genuinely different tools, and the value is in the correct handoff plus the decoy-aware index and `tx2gene` aggregation that ad-hoc scripts get wrong. Both skills come from the same collection and are designed to chain. No autonomous system is warranted — this is a fixed, well-understood pipeline, not a generated multi-stage analysis. This recipe deliberately stops at the counts matrix; it is the upstream companion to the [bulk RNA-seq DE recipe](run-bulk-rnaseq-differential-expression.html), which begins where this one ends.

## Availability

Fully open. Both skills are OSS in [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) (CC BY 4.0); fastp is MIT-licensed and Salmon is GPL-3.0. Transcriptome/genome FASTA and annotation GTF are free downloads (GENCODE, Ensembl). No subscription or institutional access.

## Compute requirements

Laptop-sufficient; no GPU. Salmon's quasi-mapping is fast: a typical mammalian sample (20–40 M read pairs) quantifies in a few minutes on 4–8 cores after the one-time decoy-aware index build (10–20 min, ~8–16 GB RAM peak for a human transcriptome+genome decoy). fastp trimming is I/O-bound, roughly a minute per sample. Disk: the index is a few GB; keep the genome FASTA around only for the index build. Move to a workstation (more cores, `-p` for Salmon) only for large cohorts.

## Evidence

Proposed. No documented attempt at an LLM-driven (Claude + fastp + Salmon + tximport) FASTQ-to-counts workflow is known. The grounding is component-level and canonical: Salmon is a peer-reviewed, widely used quantifier whose selective-alignment/decoy-aware mode reduces spurious mapping ([Patro et al., "Salmon provides fast and bias-aware quantification of transcript expression," *Nature Methods* 14:417 (2017)](https://doi.org/10.1038/nmeth.4197); [Srivastava et al., "Alignment and mapping methodology influence transcript abundance estimation," *Genome Biology* 21:239 (2020)](https://doi.org/10.1186/s13059-020-02151-8)), and gene-level aggregation via tximport with effective-length offsets is the established convention ([Soneson et al., "Differential analyses for RNA-seq: transcript-level estimates improve gene-level inferences," *F1000Research* 4:1521 (2015)](https://doi.org/10.12688/f1000research.7563.2)). fastp is the standard all-in-one FASTQ preprocessor ([Chen et al., *Bioinformatics* 34:i884 (2018)](https://doi.org/10.1093/bioinformatics/bty560)). Comparative benchmarks confirm Salmon and kallisto among the most accurate transcript quantifiers ([Sarantopoulou et al., *BMC Bioinformatics* 22:266 (2021)](https://pubmed.ncbi.nlm.nih.gov/34034652/)). The closest documented LLM analog is the cataloged [Biomni](../../autonomous-science/systems/biomni.html) agent composing genomics CLIs autonomously; this recipe pulls that to the lowest rung that solves the stated chain.

## Alternatives considered

- **STAR + featureCounts (alignment-based counting).** Reach for the [STAR aligner](../../catalog/tools/star-rna-seq-aligner.html) + [featureCounts](../../catalog/tools/featurecounts-rna-counting.html) path when you need a genome-aligned BAM anyway (variant calling, coverage tracks, novel-junction discovery). It is slower and heavier (STAR needs ~30 GB RAM for a human genome index) but gives you the BAM. Salmon is the lighter choice when the counts matrix is all you want.
- **Plain Claude Code shelling out to Salmon.** Fine for a one-off audit of every flag, but you re-derive the decoy-aware index and `tx2gene` aggregation conventions each time.
- **A Nextflow/Snakemake pipeline (nf-core/rnaseq).** The right choice for production cohorts run repeatedly on a cluster — see the [Nextflow development skill](../../catalog/tools/nextflow-development.html). This recipe is for the interactive "I have FASTQ, give me a counts matrix" case.

## See also

- [Salmon (Claude Skill)](../../catalog/tools/salmon-rna-quantification.html)
- [fastp (Claude Skill)](../../catalog/tools/fastp-fastq-preprocessing.html)
- [STAR RNA-seq aligner (Claude Skill)](../../catalog/tools/star-rna-seq-aligner.html) — the alignment-based alternative when you need a BAM.
- [Run bulk RNA-seq differential expression from a counts matrix](run-bulk-rnaseq-differential-expression.html) — the downstream companion; begins where this recipe ends.
- [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) — downstream of the DE table.

## Sources

- [Salmon skill catalog entry](../../catalog/tools/salmon-rna-quantification.html) — last verified 2026-06-11 (catalog).
- [fastp skill catalog entry](../../catalog/tools/fastp-fastq-preprocessing.html) — last verified 2026-06-11 (catalog).
- [`jaechang-hits/SciAgent-Skills` repository](https://github.com/jaechang-hits/SciAgent-Skills) — verified 2026-07-11 (this run).
- [Patro et al., "Salmon provides fast and bias-aware quantification of transcript expression," *Nature Methods* 14:417 (2017)](https://doi.org/10.1038/nmeth.4197) — canonical quantifier reference.
- [Srivastava et al., "Alignment and mapping methodology influence transcript abundance estimation," *Genome Biology* 21:239 (2020)](https://doi.org/10.1186/s13059-020-02151-8) — decoy-aware selective alignment.
- [Soneson et al., "Differential analyses for RNA-seq...," *F1000Research* 4:1521 (2015)](https://doi.org/10.12688/f1000research.7563.2) — tximport gene-level aggregation.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=quantify-bulk-rnaseq-fastq-to-counts&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fquantify-bulk-rnaseq-fastq-to-counts.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
