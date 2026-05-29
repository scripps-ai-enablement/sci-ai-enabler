---
title: Run first-pass QC on a single-cell RNA-seq dataset
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology, Neuroscience]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-29
summary: Use Anthropic's single-cell-rna-qc skill to MAD-filter a 10x .h5 or AnnData .h5ad file and emit standard QC figures before downstream Scanpy or scvi-tools work.
---

# Run first-pass QC on a single-cell RNA-seq dataset

Drop a 10x Cell Ranger `.h5` or an AnnData `.h5ad` file in front of Claude Code and get back a scverse-style MAD-filtered matrix plus the standard QC figures, ready to feed into Scanpy or scvi-tools.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology, Neuroscience |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Every single-cell RNA-seq analysis starts the same way: filter empty droplets, drop dying cells with high mitochondrial fraction, remove obvious doublets, and produce the canonical violin / scatter QC figures so the next person who looks at the data can sanity-check the thresholds. The mechanics are well understood (the scverse "single-cell best practices" book is the reference), but writing the filtering boilerplate against AnnData / Scanpy each time is friction every group rebuilds — and the thresholds are easy to set wrong by hand. Solved looks like: hand the agent a file, get back a filtered AnnData object, a one-page QC report, and a record of the thresholds that were applied.

## Recommended approach

1. **Install the [single-cell-rna-qc](../../catalog/tools/single-cell-rna-qc.html) skill.** From the `anthropics/life-sciences` marketplace:

   ```
   /plugin marketplace add anthropics/life-sciences
   /plugin install single-cell-rna-qc@life-sciences
   ```

   Confirm with `/plugin list`. The skill ships with Python helpers that perform the MAD-based filtering described in scverse best practices.

2. **Put the input file next to your project.** Either a 10x Cell Ranger `filtered_feature_bc_matrix.h5` or an AnnData `.h5ad`. The skill auto-detects format.

3. **Invoke the skill in chat with the file path and any species-specific overrides.** A minimal prompt:

   ```
   Run the single-cell-rna-qc skill on data/sample01.h5ad. Use the
   default scverse MAD thresholds on n_genes, total_counts, and
   pct_counts_mt. The species is mouse, so use mitochondrial gene
   prefix "mt-" (not "MT-"). Write the filtered AnnData to
   data/sample01_qc.h5ad and the QC figures to figures/sample01/.
   ```

4. **Review the QC figures and the threshold table** the skill emits before passing the filtered AnnData to your downstream pipeline. If the thresholds look off (e.g., a tissue with genuinely high mitochondrial content like cardiomyocytes or hepatocytes), re-run with explicit `mt_threshold` and `n_mads` overrides — the SKILL.md documents the knobs.

5. **Hand off to Scanpy or scvi-tools.** The filtered `.h5ad` is the entry point for [Scanpy-MCP](../../catalog/tools/scanpy.html) (interactive clustering / DE) or the [scvi-tools](../../catalog/tools/scvi-tools.html) skill (batch correction, deep-learning embeddings).

## Why this assembly

Rung 2 of the simplicity ladder. Plain Claude Code can write Scanpy QC code from scratch each time, but every group then quietly drifts in how they set thresholds. The single-cell-rna-qc skill encodes the scverse MAD-based recipe so the thresholds are consistent and the figures are standardized; that is a meaningful gain over rung 1. No need to escalate to a toolbelt or an autonomous system — QC is a well-defined, single-step problem and a skill is the right grain.

## Availability

Fully open. The skill is Apache-2.0-licensed and distributed via the `anthropics/life-sciences` plugin marketplace, free with any Claude plan. The underlying scverse stack (Scanpy, AnnData) is BSD-licensed. No subscription or institutional account required.

## Compute requirements

Laptop-sufficient for typical datasets — a 10k-cell 10x sample QCs in a few minutes on a modern laptop with 16 GB RAM. For very large atlases (>500k cells), use backed mode and expect tens of minutes of wall-clock; the skill itself does not require a GPU.

## Evidence

Reported. Anthropic's [tutorial for the single-cell-rna-qc skill](https://claude.com/resources/tutorials/how-to-use-the-single-cell-rna-qc-skill-with-claude) walks through this exact assembly on an example 10x dataset, producing filtered output and QC plots. The skill was published as the first Anthropic-authored scientific skill alongside the Claude for Life Sciences launch in October 2025.

No peer-reviewed benchmark of "Claude + this skill" against a hand-coded Scanpy QC pipeline is known. The closest quantitative anchor is the scverse single-cell best-practices guide that the skill's thresholds are drawn from; the agent loop adds convenience, not a new analytical method.

## Alternatives considered

- **Plain Claude Code, no skill.** Works — Claude can write the Scanpy QC code from scratch. Reach for this if you want to teach a student how the code works; reach for the skill if you want consistent thresholds across runs.
- **Scanpy-MCP alone.** The [Scanpy-MCP](../../catalog/tools/scanpy.html) server exposes `pp.*` filtering primitives. Reach for it when QC is interleaved with clustering / DE in the same conversation. The dedicated skill is a better fit when QC is a one-shot pre-processing step run before downstream work.
- **An autonomous-science system (Biomni).** Overkill for routine QC. Reach for Biomni only when QC is one node of a much larger autonomous pipeline (e.g., its published case study processing >336,000 single-nucleus profiles).

## See also

- [single-cell-rna-qc (Claude Skill)](../../catalog/tools/single-cell-rna-qc.html)
- [Scanpy-MCP](../../catalog/tools/scanpy.html)
- [scvi-tools (Claude Skill)](../../catalog/tools/scvi-tools.html)
- [AnnData (Claude Skill)](../../catalog/tools/anndata.html)

## Sources

- [single-cell-rna-qc tutorial (Anthropic)](https://claude.com/resources/tutorials/how-to-use-the-single-cell-rna-qc-skill-with-claude) — published 2025-10; verified 2026-05-21 (this run).
- [Claude for Life Sciences announcement](https://www.anthropic.com/news/claude-for-life-sciences) — published 2025-10-20; verified 2026-05-21 (this run).
- [`anthropics/life-sciences` marketplace (`single-cell-rna-qc` skill)](https://github.com/anthropics/life-sciences/blob/main/single-cell-rna-qc/SKILL.md) — last updated 2025-10; verified 2026-05-21 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=qc-single-cell-rna-seq&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fqc-single-cell-rna-seq.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
