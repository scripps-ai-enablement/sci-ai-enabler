---
title: Infer cell-cell communication from single-cell RNA-seq
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-13
summary: Use the LIANA-MCP server to run multiple ligand-receptor methods on an annotated AnnData object, aggregate their ranks, and plot the consensus communication network.
---

# Infer cell-cell communication from single-cell RNA-seq

Point Claude Code at an annotated single-cell `.h5ad`; get back a consensus ligand-receptor ranking across several methods plus circle-plot and dotplot figures of the communication network.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop (no GPU) |

## Problem

Once a single-cell dataset is QC'd, clustered, and cell-type annotated, a common next question is "which cell types are talking to each other, and through which ligand-receptor pairs?" The catch is that every inference tool (CellPhoneDB, CellChat, Connectome, NATMI, SingleCellSignalR) uses a different scoring metric and a different prior-knowledge resource, and their rankings disagree — a benchmark of 7 methods × 16 resources found that both choices strongly change the predicted interactions ([Dimitrov et al. 2022](https://doi.org/10.1038/s41467-022-30755-0)). Running one tool gives a brittle answer; running several by hand and reconciling them is the friction. Solved looks like: hand the agent an annotated object, get back a *consensus* ranking that several methods agree on, plus the network plots, with the method set and resource recorded.

## Recommended approach

1. **Install the [LIANA-MCP server](../../catalog/tools/liana-mcp.html).** Install the package, then register it with Claude Code over stdio:

   ```
   pip install liana-mcp
   claude mcp add --transport stdio liana -- liana-mcp run
   ```

2. **Prepare the input.** Provide an annotated `.h5ad` with a cell-type label in `.obs` (e.g., `cell_type`) and log-normalized expression in `.X`. If you don't have one yet, run the [scRNA-seq QC recipe](qc-single-cell-rna-seq.html) first and annotate clusters (CellTypist or marker genes). LIANA reads the loaded AnnData object — communication is only as good as the labels.

3. **List methods, then run multi-method inference and aggregate.** A minimal prompt:

   ```
   Use the liana tools. Load adata.h5ad with cell-type labels in
   obs['cell_type']. Run ls_ccc_method to show available methods, then
   run communicate across CellPhoneDB, Connectome, NATMI, and
   SingleCellSignalR, and rank_aggregate to produce a consensus
   ligand-receptor ranking. Use the consensus resource. Report the top
   20 source -> target -> ligand -> receptor tetrads.
   ```

4. **Plot the network.** Continue:

   ```
   Make a circle_plot of the aggregated communication network and a
   ccc_dotplot of the top interactions for the sender/receiver pairs I
   care about (e.g., Macrophage -> T cell). Save figures to ccc/.
   ```

5. **Read the consensus, not any single method.** Trust tetrads that rank highly across methods; treat method-specific hits as hypotheses to check against receptor protein abundance or spatial colocalization before believing them.

## Why this assembly

Rung 2 of the simplicity ladder. The whole value of this task is running *several* ligand-receptor methods and aggregating their ranks — which is exactly what LIANA does and what a single MCP call exposes. Plain Claude Code could script `liana-py` from documentation, but the MCP encodes the method list, the `rank_aggregate` step, and the plotting calls, so you stay in natural language and don't re-derive the consensus pipeline each time. One bounded analysis, one toolkit; no reason to escalate to a multi-tool harness or autonomous system.

## Availability

Fully open. LIANA-MCP is OSS in [`scmcphub/liana-mcp`](https://github.com/scmcphub/liana-mcp); `liana-py` is GPL-3.0. No subscription or institutional access required. The prior-knowledge resources LIANA ships (CellPhoneDB, etc.) are themselves freely available.

## Compute requirements

Laptop-sufficient; no GPU. Ligand-receptor inference is a per-cluster aggregation over the expression matrix — runtime scales with the number of cells and cell types, not deep computation. A typical dataset of tens of thousands of cells with a dozen cell types runs the full multi-method `rank_aggregate` in minutes on 8 GB RAM. Memory is dominated by holding the AnnData object; very large atlases (>500 k cells) benefit from 32 GB or subsetting to the cell types of interest first.

## Evidence

Proposed. No documented attempt at an LLM-driven (Claude + LIANA-MCP) cell-cell communication workflow is known. The grounding is component-level and strong: LIANA is the peer-reviewed framework whose entire purpose is multi-method consensus ligand-receptor inference ([Dimitrov et al., *Nature Communications* 13:3735 (2022)](https://doi.org/10.1038/s41467-022-30755-0)), and its consensus mode is in active use — e.g., a 2026 four-organ mouse ageing study applied LIANA's integrated methods to derive consensus communication predictions across life stages ([Wei et al., *PLOS ONE* 2026](https://doi.org/10.1371/journal.pone.0345045)). The need for consensus (rather than any single tool) is itself benchmarked: independent comparisons find method and resource choice strongly change predictions, so single-tool answers are unreliable ([Xie et al., *Biomolecules* 13:1211 (2023)](https://doi.org/10.3390/biom13081211)). The [LIANA-MCP catalog entry](../../catalog/tools/liana-mcp.html) documents that the server drives exactly the `communicate` → `rank_aggregate` → plot chain this recipe uses.

## Alternatives considered

- **Plain Claude Code scripting `liana-py`.** Workable when you want to audit every method parameter, but you re-derive the multi-method aggregation each run and lose the natural-language interface.
- **The CellChat skill (R) for a single high-quality method.** Reach for it when you specifically want CellChat's pathway-level aggregation and signaling-role analysis rather than a cross-method consensus; LIANA-MCP can also run CellChat as one of its methods.
- **An autonomous-science system.** Overkill — communication inference here is a fixed, well-bounded step, not a node in a generated multi-stage analysis.

## See also

- [LIANA-MCP](../../catalog/tools/liana-mcp.html)
- [Run first-pass QC on a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — upstream; produce the annotated object this recipe consumes.
- [Integrate multiple single-cell RNA-seq datasets across batches](integrate-single-cell-datasets.html) — sister single-cell recipe.
- [Infer a gene-regulatory network from single-cell RNA-seq](infer-gene-regulatory-network-from-scrnaseq.html) — complementary intracellular-network view.
- [Infer transcription-factor and pathway activities from expression](infer-tf-and-pathway-activities-from-expression.html) — sibling scmcphub MCP scoring regulator activities on the same object.

## Sources

- [LIANA-MCP catalog entry](../../catalog/tools/liana-mcp.html) — last verified 2026-06-13 (catalog).
- [`scmcphub/liana-mcp` repository](https://github.com/scmcphub/liana-mcp) — verified 2026-06-13 (this run).
- [Dimitrov et al., "Comparison of methods and resources for cell-cell communication inference," *Nature Communications* 13:3735 (2022)](https://doi.org/10.1038/s41467-022-30755-0) — canonical LIANA reference.
- [Wei et al., "Quantitative profiling of lifespan-dependent cell-cell communication potential," *PLOS ONE* (2026)](https://doi.org/10.1371/journal.pone.0345045) — recent consensus-LIANA application.
- [Xie et al., "A Comparison of Cell-Cell Interaction Prediction Tools," *Biomolecules* 13:1211 (2023)](https://doi.org/10.3390/biom13081211) — method-disagreement benchmark.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=infer-cell-cell-communication-from-scrnaseq&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Finfer-cell-cell-communication-from-scrnaseq.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
