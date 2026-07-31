---
title: Compute 16S microbiome alpha/beta diversity from a BIOM table
parent: All recipes
grand_parent: Recipes
nav_order: 4
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-25
summary: Use the scikit-bio Claude skill to take a BIOM feature table and sample metadata through Shannon/Simpson/Faith's PD, UniFrac, PCoA, and PERMANOVA in one chat.
---

# Compute 16S microbiome alpha/beta diversity from a BIOM table

Hand Claude Code a QIIME 2 BIOM feature table and a sample-metadata TSV; get back the canonical alpha-diversity table, a weighted-UniFrac distance matrix, a PCoA ordination, and a PERMANOVA result for the grouping variable you care about — without writing the scikit-bio boilerplate by hand.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

After a 16S rRNA or shotgun-metagenomics run, the standard first analytical pass is the same regardless of the study: compute per-sample alpha diversity (Shannon, Simpson, Faith's PD), compute a between-sample beta-diversity distance matrix (weighted or unweighted UniFrac, Bray-Curtis), ordinate it with PCoA, and test whether your grouping variable (treatment, body site, time point) explains a significant fraction of the variance with PERMANOVA. The mechanics are well documented — QIIME 2 and scikit-bio are the canonical stacks — but writing the same `skbio.diversity` / `skbio.stats.ordination` / `skbio.stats.distance` calls each time is friction. "Solved" looks like: drop a BIOM file and a metadata TSV in the project, name the grouping column, and get back a tidy alpha table, a distance matrix, a PCoA plot, and a PERMANOVA p-value with effect size.

## Recommended approach

1. **Install the [scikit-bio (Claude Skill)](../../catalog/tools/scikit-bio.html).** From the K-Dense `scientific-agent-skills` repo:

   ```
   git clone https://github.com/K-Dense-AI/scientific-agent-skills
   cp -r scientific-agent-skills/skills/scikit-bio ~/.claude/skills/
   uv pip install scikit-bio
   ```

   Confirm the skill is discoverable with `/plugin list` (or list the `~/.claude/skills/` directory). The skill wraps the BSD-3 `scikit-bio` library and exposes BIOM/FASTA I/O, alpha/beta-diversity metrics, ordination, and PERMANOVA/ANOSIM/Mantel as primitives.

2. **Place the inputs alongside your project.** You need three files:

   - `feature-table.biom` — the BIOM v2 (HDF5) table emitted by QIIME 2 (`qiime tools export --input-path ... --output-path biom`) or your in-house DADA2/Deblur pipeline.
   - `metadata.tsv` — one row per sample, including the grouping column you want to test (e.g., `treatment`, `body_site`).
   - `tree.nwk` — a rooted phylogenetic tree over the feature IDs (required for Faith's PD and UniFrac; QIIME 2's `qiime phylogeny align-to-tree-mafft-fasttree` is the usual upstream step).

3. **Invoke the skill in chat with the file paths and grouping variable.** A minimal prompt:

   ```
   Run the scikit-bio skill on these inputs:
     feature_table = data/feature-table.biom
     metadata      = data/metadata.tsv
     tree          = data/tree.nwk
     grouping      = treatment   (column in metadata.tsv)

   Steps:
     1. Rarefy to the minimum sample depth (report what depth was used).
     2. Compute Shannon, Simpson, and Faith's PD per sample; write to
        out/alpha-diversity.tsv.
     3. Compute weighted and unweighted UniFrac distance matrices;
        write to out/unifrac-weighted.tsv and out/unifrac-unweighted.tsv.
     4. PCoA-ordinate weighted UniFrac; write the first 3 axes plus
        proportion explained to out/pcoa-weighted.tsv and plot PC1 vs
        PC2 coloured by `treatment` to figures/pcoa-weighted.png.
     5. Run PERMANOVA on weighted UniFrac by `treatment` with 999
        permutations; print pseudo-F, p, and the per-pair effect size.
   ```

4. **Review the rarefaction depth and PERMANOVA assumptions** before reporting. PERMANOVA conflates location and dispersion differences; if your groups have visibly different scatter on the PCoA, also run PERMDISP (`skbio.stats.distance.permdisp`) to disentangle the two. Adjust the rarefaction depth if you are dropping too many samples at the minimum — re-running with a higher floor at the cost of a few samples is often the right call.

5. **Hand off to downstream tooling.** The tidy alpha-diversity TSV and the PCoA axes drop straight into ggplot2 / matplotlib / your manuscript. If you need differential-abundance testing on top, ANCOM-BC and Maaslin2 live outside scikit-bio — those are separate downstream steps the skill does not cover.

## Why this assembly

Rung 2 of the simplicity ladder. Plain Claude Code can write the scikit-bio calls from scratch each session, but the parameter set is wide (rarefaction depth, metric choice, permutation count, grouping variable encoding) and small slips silently change the result. The skill encodes the canonical diversity-analysis workflow as a single discoverable action with documented defaults, which is the right grain for a one-shot analytical pre-processing step. No need to escalate to a multi-tool harness or an autonomous-science system — diversity computation is a well-defined, single-stage problem.

## Availability

Fully open. The scikit-bio library is BSD-3-Clause; the K-Dense skill wrapper is published under the same repository's open-source licence. The skill makes no external API calls — all computation runs locally on the user's data. No subscription, institutional account, or API key required. BIOM, Newick, and TSV are open formats.

## Compute requirements

Laptop-sufficient for a typical 16S study (10²–10³ samples, ~10⁴ features). A 200-sample / 5,000-feature dataset rarefies, computes weighted UniFrac, and PCoA-ordinates in seconds to a minute on a modern laptop with 16 GB RAM. UniFrac is the most expensive step; very large studies (>10⁴ samples) push you toward Unifrac's `--parallel` mode or QIIME 2's `unifrac` binary directly. The skill itself does not require a GPU.

## Evidence

Proposed. No documented end-to-end attempt of "Claude Code + the scikit-bio skill on a real BIOM table" with quantitative pass/fail is known to the curator at this time. The closest evidence is component-level and class-level:

- **scikit-bio itself** is the de-facto Python implementation of the diversity metrics used by QIIME 2; its UniFrac, PCoA, and PERMANOVA functions are the canonical reference and have been used in thousands of published microbiome studies.
- **Class-level LLM evidence** comes from [Huang et al., Biomni (bioRxiv 2025.05.30.656746)](https://doi.org/10.1101/2025.05.30.656746), whose published benchmark suite includes microbiome disease-taxa bioinformatics across five datasets (a Nature mouse study, MetaPhlAn2-processed human metagenomic studies, drinking-water OTU matrices, Human Microbiome Project data), reporting a ~4× improvement of the Biomni agent over base LLMs on biomedical task accuracy. That benchmark exercises the same metric family (alpha / beta diversity, distance-matrix statistics) this recipe runs through a single skill instead of a 150-tool environment.
- **No head-to-head benchmark** of "scikit-bio skill" versus hand-written scikit-bio code is published; the agent loop here is convenience and consistency, not a new analytical method.

## Alternatives considered

- **Plain Claude Code, no skill.** Works — Claude can write the scikit-bio calls from scratch. Reach for this when teaching a student how the calls compose, or when you need a one-off custom metric the skill does not expose. Reach for the skill when you want repeatable thresholds and a documented prompt template across studies.
- **QIIME 2 CLI directly (no agent).** The canonical microbiome stack. Reach for it when your group already runs the full QIIME 2 pipeline end-to-end (DADA2 → diversity → ANCOM-BC) and the agent loop is friction rather than help. The skill is the better fit when you are starting from a BIOM table emitted by an upstream pipeline and only need the diversity / ordination / PERMANOVA pass.
- **Biomni (autonomous-science system).** The [Biomni](../../autonomous-science/systems/biomni.html) agent exposes the same metric family inside a 150-tool environment. Reach for it when diversity computation is one node of a much larger multi-stage analysis (e.g., metagenomics → host-response transcriptomics → mechanism); reach for the focused skill when diversity is the whole job.

## See also

- [scikit-bio (Claude Skill)](../../catalog/tools/scikit-bio.html)
- [Biomni](../../autonomous-science/systems/biomni.html)
- [Profile shotgun metagenome taxa with Kraken2 and Bracken](profile-shotgun-metagenome-taxa-with-kraken2.html) — the shotgun-reads path that produces an abundance table for this diversity analysis.
- [Run bulk RNA-seq differential expression from a counts matrix](run-bulk-rnaseq-differential-expression.html) — analogous one-skill recipe on a different omics modality.

## Sources

- [`skills/scikit-bio/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scikit-bio/SKILL.md) — skill manifest; verified 2026-06-02 (this run).
- [scikit-bio documentation](https://scikit.bio/) — canonical library docs; verified 2026-06-02 (this run).
- [Huang et al., "Biomni: A General-Purpose Biomedical AI Agent," bioRxiv 2025.05.30.656746](https://doi.org/10.1101/2025.05.30.656746) — class-level LLM-agent evidence on microbiome bioinformatics; verified 2026-06-02 (this run).
- [QIIME 2 documentation: diversity analyses](https://docs.qiime2.org/) — canonical upstream context for BIOM / tree inputs; verified 2026-06-02 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=compute-16s-microbiome-diversity&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fcompute-16s-microbiome-diversity.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
