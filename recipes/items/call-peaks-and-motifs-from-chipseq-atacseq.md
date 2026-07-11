---
title: Call peaks and find enriched motifs from ChIP-seq or ATAC-seq
parent: All recipes
grand_parent: Recipes
nav_order: 4
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology]
evidence_level: Proposed
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-11
summary: Chain the MACS3 peak-calling skill into the HOMER motif skill to turn aligned ChIP-seq/ATAC-seq BAMs into a called-peak set with nearest-gene annotation and enriched TF motifs.
---

# Call peaks and find enriched motifs from ChIP-seq or ATAC-seq

Hand Claude Code aligned ChIP-seq or ATAC-seq BAMs; get back a called-peak BED, peaks annotated with their nearest genes, and a ranked list of enriched transcription-factor motifs.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology |
| **Evidence level** | Proposed |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Laptop (no GPU) |

## Problem

After aligning a ChIP-seq, CUT&RUN, or ATAC-seq experiment and confirming the signal looks right, the substantive analysis is two coupled steps: **call** the enriched regions (where is the protein bound / where is the chromatin open?), then ask **which transcription factors** explain those regions (de novo and known-motif enrichment, plus nearest-gene context). MACS3 and HOMER are the field-standard pair, but they are a chain: MACS3 `callpeak` with the right narrow/broad mode and genome size, then HOMER `findMotifsGenome.pl` against a matched background and `annotatePeaks.pl` for gene context — and the peak file from the first has to be handed cleanly to the second. Solved looks like: BAMs in; a `narrowPeak`/`broadPeak` BED, a peak-to-gene annotation table, and a known/de-novo motif report out, with the peak mode and background choices explicit.

## Recommended approach

1. **Install the [MACS3](../../catalog/tools/macs3-peak-calling.html) and [HOMER](../../catalog/tools/homer-motif-analysis.html) skills.** Both ship in the SciAgent-Skills collection — clone once and load as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm `macs3-peak-calling` and `homer-motif-analysis` appear under `/plugin`. Each skill installs its own dependencies (MACS3; HOMER + a genome FASTA) on first use.

2. **Prepare inputs.** Provide coordinate-sorted, indexed BAMs (`*.bam` + `*.bam.bai`) for the IP/treatment and, ideally, a matched input/IgG control. Decide the peak mode up front: **narrow** for TF ChIP-seq and ATAC-seq, **broad** for H3K27me3/H3K9me3 and other broad histone marks. State the genome build so the effective genome size is correct.

3. **Call peaks with MACS3.** A minimal prompt:

   ```
   Use the macs3 skill. Run callpeak on ip.bam with control input.bam,
   genome size hs (GRCh38), narrow mode, q-value 0.05. Write the
   narrowPeak BED to peaks/ and report the peak count and FRiP if
   available.
   ```

   For a broad mark, say "broad mode, broad-cutoff 0.1" instead.

4. **Annotate and find motifs with HOMER.** Continue:

   ```
   Use the homer skill. Run annotatePeaks.pl on peaks/ip_peaks.narrowPeak
   against hg38 to assign nearest gene and TSS distance, then
   findMotifsGenome.pl on the same peaks vs hg38 (size 200) for known
   and de novo motif enrichment. Save the motif report to motifs/ and
   summarize the top enriched TFs.
   ```

5. **Sanity-check the motif against the assay.** For a TF ChIP-seq, the factor's own motif should top the enrichment list — if it doesn't, suspect the antibody, the peak set, or the background before interpreting downstream TFs.

## Why this assembly

Rung 3 of the simplicity ladder — a two-component toolbelt. Rung 2 (a single skill) doesn't solve it: peak calling and motif analysis are genuinely different tools (MACS3's Poisson model vs HOMER's motif enrichment), and the value is in the *handoff* — MACS3's peak BED becomes HOMER's input. Both skills come from the same collection and are designed to chain (HOMER's catalog page explicitly says "use after MACS3"), so the harness is two skills, not three. No autonomous system is warranted: the workflow is a fixed, well-understood two-step pipeline, not a generated multi-stage analysis. This recipe is the binding-site/motif companion to the [signal-profiling recipe](profile-chipseq-atacseq-signal-around-features.html), which deliberately stops before peak calling.

## Availability

Fully open. Both skills are OSS in [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) (CC BY 4.0); MACS3 is BSD-3-Clause and HOMER is GPL-3.0. HOMER requires downloading a genome FASTA/annotation package on first use (free). No subscription or institutional access.

## Compute requirements

Laptop-sufficient; no GPU. MACS3 `callpeak` on a typical mammalian ChIP-seq sample (20–40 M reads) runs in a few minutes on 4–8 GB RAM. HOMER `findMotifsGenome.pl` is the heavier step — de novo motif discovery over a few thousand peaks takes 10–30 minutes single-threaded and benefits from `-p` for parallelism; the one-time HOMER genome package download is a few GB of disk. `annotatePeaks.pl` is fast. Move to a workstation only for very large peak sets or many samples.

## Evidence

Proposed. No documented attempt at an LLM-driven (Claude + MACS3 + HOMER) peak-calling-plus-motif workflow is known. The grounding is component-level and canonical: MACS is the standard model-based ChIP-seq peak caller ([Zhang et al., "Model-based Analysis of ChIP-Seq (MACS)," *Genome Biology* 9:R137 (2008)](https://doi.org/10.1186/gb-2008-9-9-r137)), now maintained as MACS3, and HOMER is the standard motif-discovery and peak-annotation suite ([Heinz et al., *Molecular Cell* 38:576 (2010)](https://doi.org/10.1016/j.molcel.2010.05.004)). The MACS3 → HOMER chain is the textbook ChIP-seq/ATAC-seq downstream pipeline, and both skills were evaluated as part of the BixBench-benchmarked SciAgent-Skills collection (see the [MACS3](../../catalog/tools/macs3-peak-calling.html) and [HOMER](../../catalog/tools/homer-motif-analysis.html) catalog entries). The closest documented LLM analog is the cataloged [Biomni](../../autonomous-science/systems/biomni.html) agent composing genomics CLIs autonomously; this recipe pulls that to the lowest rung that solves the stated two-step problem.

## Alternatives considered

- **The [signal-profiling recipe](profile-chipseq-atacseq-signal-around-features.html) (deepTools, rung 2).** Reach for it when you already have a peak set (or TSS list) and want normalized coverage tracks and feature-centered heatmaps — visualization, not discovery. This recipe answers the upstream question of *where the peaks are and what binds there*.
- **Plain Claude Code shelling out to MACS3/HOMER.** Fine for a one-off audit of every flag, but you re-derive the narrow/broad mode, background, and gene-annotation conventions each time.
- **A Nextflow/Snakemake pipeline (nf-core/chipseq, nf-core/atacseq).** The right choice for production cohorts run repeatedly on a cluster — see the [Nextflow development skill](../../catalog/tools/nextflow-development.html). This recipe is for the interactive "I have BAMs, find the peaks and the motifs" case.

## See also

- [MACS3 (Claude Skill)](../../catalog/tools/macs3-peak-calling.html)
- [HOMER (Claude Skill)](../../catalog/tools/homer-motif-analysis.html)
- [Profile ChIP-seq or ATAC-seq signal around genomic features](profile-chipseq-atacseq-signal-around-features.html) — the visualization companion (deepTools); deliberately stops before peak calling.
- [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) — downstream of the genes HOMER assigns to peaks.

## Sources

- [MACS3 skill catalog entry](../../catalog/tools/macs3-peak-calling.html) — last verified 2026-06-11 (catalog).
- [HOMER skill catalog entry](../../catalog/tools/homer-motif-analysis.html) — last verified 2026-06-11 (catalog).
- [`jaechang-hits/SciAgent-Skills` repository](https://github.com/jaechang-hits/SciAgent-Skills) — verified 2026-07-11 (this run).
- [Zhang et al., "Model-based Analysis of ChIP-Seq (MACS)," *Genome Biology* 9:R137 (2008)](https://doi.org/10.1186/gb-2008-9-9-r137) — canonical peak-caller reference.
- [Heinz et al., "Simple Combinations of Lineage-Determining Transcription Factors...," *Molecular Cell* 38:576 (2010)](https://doi.org/10.1016/j.molcel.2010.05.004) — canonical HOMER reference.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=call-peaks-and-motifs-from-chipseq-atacseq&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fcall-peaks-and-motifs-from-chipseq-atacseq.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
