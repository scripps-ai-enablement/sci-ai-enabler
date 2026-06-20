---
title: Infer transcription-factor and pathway activities from expression
parent: All recipes
grand_parent: Recipes
nav_order: 17
problem_class: Data analysis
subject_areas: [Immunology and Microbiology, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-20
summary: Drive the decoupler-MCP server to score per-cell or per-sample transcription-factor (CollecTRI) and pathway (PROGENy) activities from an expression matrix, then read off the regulators that move between conditions.
---

# Infer transcription-factor and pathway activities from expression

Turn an expression matrix into *activities*: which transcription factors and signalling pathways are switched on in each cell or sample — a footprint-based readout that complements over-representation enrichment, driven by the decoupler-MCP server.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Differential expression and over-representation enrichment tell you *which genes changed* and *what gene sets they fall in*, but not *which regulators are driving the change*. A T-cell that has upregulated dozens of interferon-stimulated genes is reporting **STAT1/IRF activity**; a tumour sample with a scattered EMT signature is reporting **TGF-β pathway activity**. Footprint methods recover that hidden regulator state by scoring the expression of a transcription factor's known targets (a regulon) or a pathway's responsive genes, rather than the regulator's own mRNA — which is often a poor proxy for its activity. The mechanics are fiddly: pick a network (CollecTRI for TFs, PROGENy for pathways), pick a statistic (ULM, MLM, consensus), align gene IDs to the network, and keep per-cell vs per-cluster scoring straight. Solved looks like: hand over an annotated expression object, get back a TF-activity and a pathway-activity matrix plus a short list of the regulators that differ between your conditions, each traceable to the network and method that produced it.

## Recommended approach

1. **Install the [decoupler-MCP server](../../catalog/tools/decoupler-mcp.html).** Install the package, then register it over stdio (Claude Code launches the process itself):

   ```
   pip install decoupler-mcp
   claude mcp add --transport stdio decoupler -- decoupler-mcp run
   ```

2. **Have an annotated expression object ready.** decoupler-MCP operates on a loaded AnnData. For single-cell, produce it with the [scRNA-seq QC recipe](qc-single-cell-rna-seq.html) (filtered, normalised, clustered, cell-type-labelled). Bulk RNA-seq works too — wrap your normalised counts (samples × genes) in an AnnData with the condition labels in `.obs`.

3. **Infer transcription-factor activities (CollecTRI).** A minimal prompt:

   ```
   Using the decoupler MCP on the loaded AnnData:
     - run tf_activity (CollecTRI network, ULM method) to score
       transcription-factor activities per cell.
   Then aggregate the activity scores by the cell-type label in
   .obs and report the top 15 TFs whose mean activity differs most
   between <condition A> and <condition B>. Save the per-cell
   activity matrix to results/activities/tf_activity.csv and the
   ranked between-condition table to results/activities/tf_diff.csv.
   ```

4. **Infer pathway activities (PROGENy).** In the same session:

   ```
   Now run pathway_activity (PROGENy, MLM method) on the same object.
   Report the 14 PROGENy pathways ranked by mean activity difference
   between the two conditions, and save the matrix to
   results/activities/pathway_activity.csv.
   ```

5. **Ground the interpretation.** Ask Claude to write a short summary that names only TFs and pathways present in the saved CSVs, with their activity scores and direction (up/down in which condition). The activity matrices are the audit trail — the model should not invoke a regulator that is not in the table.

6. **Sanity-check against the biology.** A positive control beats trust: if your conditions are, say, IFN-stimulated vs control, STAT1/STAT2/IRF activity should rise and the PROGENy JAK-STAT pathway should light up. If a known driver does not appear, suspect a gene-ID mismatch between your object and the network before reading further.

## Why this assembly

Rung 2 of the simplicity ladder. The entire footprint workflow — network choice, the linear-model statistic, the per-cell scoring — lives inside one MCP server, so a single tool solves it. Rung 1 (plain Claude Code) would have to re-derive the decoupler API and the right network/method pairing each time and is more likely to confuse activity inference with ordinary enrichment. A toolbelt (rung 3) buys nothing: activity inference is single-source against one Python package. This recipe is deliberately *not* the [functional-enrichment recipe](run-functional-enrichment-on-a-gene-list.html) — that does over-representation analysis on a hit list (which gene sets are over-represented), whereas this scores continuous regulator activity from the full expression profile (which regulators are on). Reach for both: enrichment names the processes, activity inference names the drivers.

## Availability

Fully open. decoupler-MCP is OSS (scmcphub ecosystem); the underlying [decoupler](https://decoupler.readthedocs.io/) package is GPL-3.0; the CollecTRI and PROGENy networks are distributed via OmniPath under open academic terms. No subscription, no institutional account, no API key — all computation is local against the loaded object.

## Compute requirements

Laptop. Footprint scoring is a set of matrix multiplications against a network; ULM/MLM over tens of thousands of cells and a few thousand network genes runs in seconds-to-a-minute on CPU. No GPU. Memory is dominated by the AnnData already in memory, not by the activity step; the output matrices (cells × ~15 pathways, cells × hundreds of TFs) are a few MB. For very large objects, score per-cluster pseudobulk rather than per-cell to cut runtime.

## Evidence

Proposed. No documented end-to-end attempt of "Claude + the decoupler-MCP server" on a real dataset, with quantitative pass/fail, is known to the curator. The evidence is component-level:

- **decoupler is the reference framework** for footprint-based activity inference, benchmarking an ensemble of methods (ULM, MLM, consensus, VIPER, AUCell, and others) within one API ([Badia-i-Mompel et al., "decoupleR: ensemble of computational methods to infer biological activities from omics data," *Bioinformatics Advances* 2:vbac016, 2022](https://doi.org/10.1093/bioadv/vbac016)).
- **The networks are the standard resources.** PROGENy derives pathway-responsive gene signatures from perturbation experiments ([Schubert et al., *Nat. Commun.* 9:20, 2018](https://doi.org/10.1038/s41467-017-02391-6)); CollecTRI is a curated TF–target collection that outperforms prior regulons for activity inference ([Müller-Dott et al., *Nucleic Acids Research* 51:10934, 2023](https://doi.org/10.1093/nar/gkad841)).
- **No head-to-head benchmark** of the MCP-driven assembly versus hand-written decoupler code is published; the MCP buys natural-language orchestration and a repeatable prompt, not new statistics. The closest analogous cataloged-component recipe is the [cell-cell communication recipe](infer-cell-cell-communication-from-scrnaseq.html), which drives a sibling scmcphub server (LIANA-MCP) on the same kind of annotated AnnData.

## Alternatives considered

- **Over-representation enrichment (rung 2).** [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) answers a different question — which gene sets are over-represented in a hit list — and is the right tool when you already have a discrete DE gene list rather than a full expression matrix. Use both together.
- **GRN inference (rung 2).** [Infer a gene-regulatory network from single-cell RNA-seq](infer-gene-regulatory-network-from-scrnaseq.html) *learns* a regulatory network de novo from co-expression, whereas this recipe *uses* a curated network (CollecTRI) to score activities. Reach for GRN inference when you want to discover regulons; reach for this when you want to score known ones.
- **Plain Claude Code + decoupler (rung 1).** Viable if decoupler is already installed and you want a throwaway one-off; the MCP earns its place by pinning the network/method choices and keeping the workflow reproducible.
- **An autonomous system (Biomni).** Overkill for a single activity-inference step; reach for it only when activity inference is one node in a larger autonomous loop.

## See also

- [decoupler-MCP](../../catalog/tools/decoupler-mcp.html)
- [QC and cluster a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — produces the annotated AnnData this recipe scores.
- [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) — over-representation companion to activity inference.
- [Infer a gene-regulatory network from single-cell RNA-seq](infer-gene-regulatory-network-from-scrnaseq.html) — de-novo network alternative.
- [Infer cell-cell communication from single-cell RNA-seq](infer-cell-cell-communication-from-scrnaseq.html) — sibling scmcphub MCP on the same object.

## Sources

- [Badia-i-Mompel et al., "decoupleR: ensemble of computational methods to infer biological activities from omics data," *Bioinformatics Advances* 2:vbac016 (2022)](https://doi.org/10.1093/bioadv/vbac016) — verified 2026-06-20 (this run).
- [Schubert et al., "Perturbation-response genes reveal signaling footprints in cancer gene expression," *Nat. Commun.* 9:20 (2018)](https://doi.org/10.1038/s41467-017-02391-6) — PROGENy.
- [Müller-Dott et al., "Expanding the coverage of regulons from high-confidence prior knowledge for accurate estimation of transcription factor activities," *Nucleic Acids Research* 51:10934–10949 (2023)](https://doi.org/10.1093/nar/gkad841) — CollecTRI.
- [decoupler documentation](https://decoupler.readthedocs.io/en/latest/) — verified 2026-06-20 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=infer-tf-and-pathway-activities-from-expression&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Finfer-tf-and-pathway-activities-from-expression.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
