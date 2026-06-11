---
title: Profile ChIP-seq or ATAC-seq signal around genomic features
parent: All recipes
grand_parent: Recipes
nav_order: 20
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-11
summary: Use the deepTools Claude Skill to turn aligned ChIP-seq/ATAC-seq BAMs into normalized bigWig tracks and TSS/peak-centered profile and heatmap figures.
---

# Profile ChIP-seq or ATAC-seq signal around genomic features

Hand Claude Code a set of aligned ChIP-seq or ATAC-seq BAM files; get back normalized bigWig coverage tracks, a sample-correlation QC matrix, and profile/heatmap figures of signal centered on TSSs or a peak set.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop (no GPU) |

## Problem

After aligning a ChIP-seq, CUT&RUN, or ATAC-seq experiment, the next step is almost always the same: convert BAMs to normalized coverage tracks, check that replicates agree, and visualize signal aggregated around a feature set (transcription start sites, called peaks, enhancers). deepTools is the field-standard toolkit for this, but it is a chain of CLI tools (`bamCoverage`, `multiBamSummary`, `plotCorrelation`, `computeMatrix`, `plotHeatmap`, `plotProfile`) with normalization flags (`RPKM`, `CPM`, `BPM`, `--effectiveGenomeSize`) that are easy to mis-set, and the matrix/plotting steps need their arguments to line up. Solved looks like: BAMs in, a QC correlation figure plus a publication-ready TSS or peak heatmap out, with every normalization and binning choice explicit and reproducible.

## Recommended approach

1. **Install the [deepTools Claude Skill](../../catalog/tools/deeptools.html)** from the K-Dense collection:

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   ```

   Enable the `deeptools` skill when prompted. deepTools' own dependencies install on first use (the skill uses `uv` / `pip`).

2. **Prepare inputs.** Provide coordinate-sorted, indexed BAMs (`*.bam` + `*.bam.bai`) for each sample/replicate, a genome build (so the effective genome size is correct), and a feature file: a BED/GTF of TSSs or a peak BED (e.g., MACS2 `narrowPeak`). For ATAC-seq, decide up front whether to shift reads for Tn5 (`--Offset`) — state it in the prompt.

3. **Make normalized tracks and a replicate-QC matrix.** A minimal prompt:

   ```
   Use the deeptools skill. For each BAM in bams/, run bamCoverage with
   --normalizeUsing BPM --binSize 25 --effectiveGenomeSize 2913022398
   (GRCh38) and write bigWigs to tracks/. Then run multiBamSummary in
   bins mode over all BAMs and plotCorrelation (Spearman, heatmap) to
   qc/replicate_correlation.png so I can confirm replicates cluster.
   ```

4. **Center the signal on features and plot.** Continue:

   ```
   Now run computeMatrix reference-point --referencePoint TSS -b 3000
   -a 3000 --binSize 25 over the bigWigs in tracks/ against
   features/tss.bed, then plotHeatmap (sorted by mean signal) to
   figures/tss_heatmap.png and plotProfile to figures/tss_profile.png.
   Use scale-regions instead of reference-point if I give you gene
   bodies rather than TSSs.
   ```

5. **Inspect the correlation matrix first.** If replicates don't cluster above the rest, stop and check the alignment/QC upstream before trusting the heatmaps.

## Why this assembly

Rung 2 of the simplicity ladder. Plain Claude Code could shell out to deepTools from documentation, but the skill encodes the correct tool ordering (coverage → summary → matrix → plot), the normalization vocabulary (`BPM` vs `RPKM` vs `CPM`), and the effective-genome-size and bin-size conventions that make the tracks comparable across samples — the exact places ad-hoc scripts go wrong. This is a single well-bounded analysis served by a single toolkit, so there is no reason to escalate to a multi-tool harness or an autonomous system. Peak *calling* (MACS2) and differential binning (DiffBind/csaw) are separate steps not in this skill; this recipe stops at normalized tracks and feature-centered visualization.

## Availability

Fully open. The deepTools skill is OSS (BSD) in [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills); deepTools itself is BSD-licensed. No subscription or institutional access required.

## Compute requirements

Laptop-sufficient for a small experiment; no GPU. `bamCoverage` and `computeMatrix` are I/O- and CPU-bound, and runtime scales with BAM size and read depth. A typical mammalian ChIP-seq sample (20–40 M reads) converts to a 25-bp-bin bigWig in a few minutes per sample on 4–8 cores, and whole-experiment `computeMatrix` over thousands of TSSs is minutes more; expect a few hundred MB of bigWig per sample. Move to a workstation (16–32 GB RAM, more cores via `--numberOfProcessors`) only when you have many samples or run whole-genome bins.

## Evidence

Proposed. No documented attempt at an LLM-driven (Claude + deepTools skill) ChIP-seq/ATAC-seq profiling workflow is known. The grounding is component-level: deepTools is a peer-reviewed, widely cited toolkit ([Ramírez et al., *Nucleic Acids Research* 44:W160 (2016)](https://doi.org/10.1093/nar/gkw257)) whose `bamCoverage`/`computeMatrix`/`plotHeatmap` chain is the established convention for exactly this task, and the [deepTools skill catalog entry](../../catalog/tools/deeptools.html) documents that the skill drives these tools locally. The closest analogous documented LLM workflow is the cataloged [Biomni](../../autonomous-science/systems/biomni.html) agent, which composes genomics CLI tools (including coverage/visualization steps) inside an autonomous loop; this recipe pulls that capability down to the simplest rung that solves the stated problem.

## Alternatives considered

- **Plain Claude Code, no skill.** Fine for a one-off where you want to audit every flag, but you lose the encoded normalization conventions and re-derive the tool ordering each time.
- **A Nextflow/Snakemake pipeline (e.g., nf-core/chipseq).** The right choice for production cohorts run repeatedly on a cluster — see the [Nextflow development skill](../../catalog/tools/nextflow-development.html). This recipe is for the interactive, exploratory "I have BAMs, show me the signal" case, not a hardened batch pipeline.
- **An autonomous-science system (Biomni).** Overkill for a fixed visualization task; the autonomous loop only earns its overhead when track generation is one node in a larger generated analysis.

## See also

- [deepTools (Claude Skill)](../../catalog/tools/deeptools.html)
- [pysam (Claude Skill)](../../catalog/tools/pysam.html) — for upstream BAM filtering/region extraction before coverage.
- [Run bulk RNA-seq differential expression from a counts matrix](run-bulk-rnaseq-differential-expression.html) — sister NGS-quantification recipe.
- [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) — downstream of genes assigned to peaks.

## Sources

- [deepTools skill catalog entry](../../catalog/tools/deeptools.html) — last verified 2026-06-04 (catalog).
- [`K-Dense-AI/scientific-agent-skills` repository](https://github.com/K-Dense-AI/scientific-agent-skills) — verified 2026-06-11 (this run).
- [Ramírez et al., "deepTools2," *Nucleic Acids Research* 44:W160 (2016)](https://doi.org/10.1093/nar/gkw257) — published 2016; canonical method reference.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=profile-chipseq-atacseq-signal-around-features&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fprofile-chipseq-atacseq-signal-around-features.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
