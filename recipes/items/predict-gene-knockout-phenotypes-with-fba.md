---
title: Predict gene-knockout phenotypes with flux balance analysis
parent: All recipes
grand_parent: Recipes
nav_order: 19
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-11
summary: Use the COBRApy Claude Skill to load a genome-scale metabolic model and screen single/double gene deletions for growth phenotypes and essential genes.
---

# Predict gene-knockout phenotypes with flux balance analysis

Hand Claude Code a genome-scale metabolic model (SBML); get back a baseline growth-rate prediction, a ranked single-gene-deletion essentiality table, and an optional double-deletion synthetic-lethality screen.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Constraint-based modelling answers a recurring systems-biology question without a wet-lab experiment: if I knock out gene X (or the pair X,Y), does the organism still grow, and by how much is flux through my pathway of interest reduced? Flux balance analysis (FBA) on a genome-scale model gives a fast, genome-wide answer and is the standard way to nominate essential genes, antimicrobial targets, and metabolic-engineering knockouts. COBRApy is the reference Python implementation, but a correct run still requires loading the right model, confirming the medium and biomass objective are sensible, running the deletion screen the right way (`single_gene_deletion`, `double_gene_deletion`), and interpreting the growth-ratio cutoff for "essential." Solved looks like: a model in, an essentiality/synthetic-lethality table out, with the medium, objective, and essentiality threshold stated explicitly.

## Recommended approach

1. **Install the [COBRApy Claude Skill](../../catalog/tools/cobrapy.html)** from the K-Dense collection:

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   pip install cobra
   ```

   Enable the `cobrapy` skill when prompted.

2. **Provide a model.** A genome-scale model in SBML/JSON/YAML — your own reconstruction, a BiGG Models download (e.g., *E. coli* `iML1515`), or COBRApy's bundled `textbook`/`ecoli` test models for a dry run. Note the organism's growth medium if it differs from the model default.

3. **Sanity-check the baseline before screening.** A minimal prompt:

   ```
   Use the cobrapy skill. Load model.xml, report the biomass objective
   reaction and the medium, then run FBA (optimize) and tell me the
   predicted growth rate. Flag if growth is zero (likely a blocked
   medium or objective) before we go further.
   ```

4. **Run the deletion screen.** Continue:

   ```
   Now run single_gene_deletion across all genes. Rank genes by
   growth ratio (knockout growth / wild-type growth). Call a gene
   essential if growth ratio < 0.01. Write the full table to
   results/single_ko.csv and the essential-gene list to
   results/essential_genes.csv.
   ```

5. **Optionally screen for synthetic lethality.** For a focused gene set (it is combinatorial — do not run genome-wide double deletions on a laptop):

   ```
   Run double_gene_deletion over the gene list in candidates.txt and
   flag synthetic-lethal pairs (both single KOs viable, double KO
   growth ratio < 0.01). Write to results/double_ko.csv.
   ```

## Why this assembly

Rung 2 of the simplicity ladder. Plain Claude Code can write COBRApy from documentation, but the skill encodes the correct API for the deletion screens, the context-manager pattern for temporary medium/objective changes (so state reverts cleanly), and the FVA/pFBA conventions — the parts where ad-hoc scripts silently produce wrong flux distributions. FBA is one well-bounded optimization served by one library, so there is no need for a multi-tool harness or an autonomous system. Integrating expression/proteomics constraints or mapping flux hits to chemistry is a separate, larger task (see **Alternatives**); this recipe stops at the deletion-phenotype screen.

## Availability

Fully open. The COBRApy skill is OSS in [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills) (MIT collection). COBRApy itself is GPL-2.0 — review the license for commercial redistribution. The default GLPK solver is open; large genome-scale sampling benefits from CPLEX/Gurobi (free academic licenses). No subscription or institutional access required for the open path.

## Compute requirements

Laptop-sufficient. A single FBA solve on a genome-scale model is sub-second with GLPK; a genome-wide single-gene-deletion screen on a model like *E. coli* `iML1515` (~1500 genes) runs in seconds to a couple of minutes on a laptop CPU. Double-gene deletion is O(n²) — keep it to a curated candidate list (tens to low hundreds of genes), or move to a workstation and a faster solver for larger screens. No GPU. Memory footprint is small (well under 1 GB for standard models).

## Evidence

Proposed. No documented attempt at an LLM-driven (Claude + COBRApy skill) gene-knockout screen is known. The grounding is component-level: COBRApy is the peer-reviewed reference implementation of constraint-based analysis ([Ebrahim et al., *BMC Systems Biology* 7:74 (2013)](https://doi.org/10.1186/1752-0509-7-74)), and FBA-based gene-essentiality prediction is a long-established, validated method ([Orth, Thiele & Palsson, "What is flux balance analysis?", *Nature Biotechnology* 28:245 (2010)](https://doi.org/10.1038/nbt.1614)). The [COBRApy skill catalog entry](../../catalog/tools/cobrapy.html) documents that the skill drives exactly these `single_gene_deletion`/`double_gene_deletion` and FBA/FVA functions. The closest analogous documented LLM workflow is the cataloged [Biomni](../../autonomous-science/systems/biomni.html) agent, which can invoke metabolic-modelling tools inside an autonomous loop; this recipe pulls the capability down to the simplest rung that solves the stated problem.

## Alternatives considered

- **Plain Claude Code, no skill.** Workable for a single solve you want to audit line by line; you lose the encoded deletion-screen API and the safe context-manager pattern.
- **An autonomous-science system (Biomni).** Reach for it when the knockout screen is one node in a larger generated hypothesis loop (e.g., generate target → model knockout → propose follow-up assay). For a fixed essentiality screen it is overkill.
- **Integrating omics constraints (GIMME/iMAT-style context-specific models).** A genuinely larger task that layers expression data onto the model — compose the COBRApy skill with the [PyDESeq2](../../catalog/tools/pydeseq2.html) or [Scanpy-MCP](../../catalog/tools/scanpy.html) outputs as a follow-on, not in this recipe.

## See also

- [COBRApy (Claude Skill)](../../catalog/tools/cobrapy.html)
- [Biomni](../../autonomous-science/systems/biomni.html) — autonomous-loop path when the screen is one step of a larger hypothesis cycle.
- [Prioritize targets within a disease via Open Targets](prioritize-targets-within-a-disease.html) — orthogonal target-nomination recipe.
- [Run bulk RNA-seq differential expression from a counts matrix](run-bulk-rnaseq-differential-expression.html) — source of expression constraints for context-specific models.

## Sources

- [COBRApy skill catalog entry](../../catalog/tools/cobrapy.html) — last verified 2026-06-04 (catalog).
- [`K-Dense-AI/scientific-agent-skills` repository](https://github.com/K-Dense-AI/scientific-agent-skills) — verified 2026-06-11 (this run).
- [Ebrahim et al., "COBRApy: COnstraints-Based Reconstruction and Analysis for Python," *BMC Systems Biology* 7:74 (2013)](https://doi.org/10.1186/1752-0509-7-74) — published 2013; library reference.
- [Orth, Thiele & Palsson, "What is flux balance analysis?," *Nature Biotechnology* 28:245 (2010)](https://doi.org/10.1038/nbt.1614) — published 2010; method reference.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=predict-gene-knockout-phenotypes-with-fba&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fpredict-gene-knockout-phenotypes-with-fba.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
