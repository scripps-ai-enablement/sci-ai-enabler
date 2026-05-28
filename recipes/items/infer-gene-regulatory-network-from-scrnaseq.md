---
title: Infer a gene-regulatory network from single-cell RNA-seq
parent: All recipes
grand_parent: Recipes
nav_order: 5
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-05-28
summary: Use the Arboreto Claude skill to run GRNBoost2 on a QC'd single-cell AnnData and recover a ranked TF–target edge list — the first step of a SCENIC regulon pipeline.
---

# Infer a gene-regulatory network from single-cell RNA-seq

Hand Claude Code a QC'd single-cell AnnData and a transcription-factor list; get back a GRNBoost2 importance-ranked edge table of TF → target relationships, ready to feed into cisTarget motif enrichment or use directly for regulator prioritisation.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

After you have integrated cell types and called clusters, the next question is usually mechanistic: which transcription factors drive the cell-state differences you see? Regulator inference asks the data to fit a tree-based regression for every target gene against every candidate TF, and rank the TFs by importance — a `(genes × genes)` problem that is embarrassingly parallel but computationally heavy. The canonical fast implementation is GRNBoost2, distributed via Dask, packaged in Arboreto, and consumed downstream by pySCENIC for cisTarget motif filtering and AUCell scoring. Solved looks like: an `adjacencies.tsv` of `(TF, target, importance)` triples that you can either feed directly into pySCENIC or threshold to a candidate regulator shortlist.

The non-obvious failure modes are (1) running GRNBoost2 on log-normalised data when it expects raw counts or `log1p` of CPM-normalised counts, (2) not restricting to a TF list (Arboreto defaults to all genes-as-regulators if you don't pass one), and (3) forgetting that GRNBoost2 is non-deterministic — single runs produce drifting regulons. The recipe surfaces all three.

## Recommended approach

1. **QC and integrate first.** Run the [single-cell-rna-qc recipe](qc-single-cell-rna-seq.html) and (if more than one batch) the [integration recipe](integrate-single-cell-datasets.html) before this step. GRN inference on raw, batch-confounded data finds technical regulators, not biological ones.

2. **Install the [Arboreto skill](../../catalog/tools/arboreto.html)** in Claude Code:

   ```
   /plugin marketplace add K-Dense-AI/claude-scientific-skills
   /plugin install arboreto@claude-scientific-skills
   ```

   Confirm with `/plugin list`. Have the [AnnData skill](../../catalog/tools/anndata.html) installed too — Arboreto consumes a `(cells × genes)` expression matrix, not an `.h5ad` directly.

3. **Obtain a transcription-factor list for your organism.** For human / mouse, the [Aerts lab cisTarget resources](https://resources.aertslab.org/cistarget/) ship curated TF lists (`allTFs_hg38.txt`, `allTFs_mm10.txt`). Download once and keep alongside the data. Without this, Arboreto will treat every gene as a candidate regulator and the runtime explodes.

4. **Extract the expression matrix.** A minimal prompt:

   ```
   Read data/integrated.h5ad with the AnnData skill, subset to the
   highly variable genes union the TF list at refs/allTFs_hg38.txt,
   and emit a pandas DataFrame of cells × genes with raw or log1p
   counts (Arboreto expects non-negative reals). Save to
   data/grn_input.parquet.
   ```

5. **Run GRNBoost2 with a fixed seed.** Drive the Arboreto skill explicitly:

   ```
   Use the Arboreto skill on data/grn_input.parquet:
     - method=grnboost2
     - tf_names=refs/allTFs_hg38.txt
     - seed=777
     - Dask LocalCluster, n_workers=8
     - wrap the call in the standard if __name__ == "__main__": guard
     - write the ranked (TF, target, importance) edge list to
       results/adjacencies.tsv and print the top 50 by importance.
   ```

   The `if __name__ == "__main__":` guard is mandatory — Dask spawns workers and will recurse on import otherwise. The skill's SKILL.md documents this; the prompt names it so Claude does not skip it.

6. **Run the inference 2–5 more times with different seeds.** GRNBoost2 is non-deterministic. The van de Sande 2020 *Nature Protocols* recommendation is to run the SCENIC pipeline up to ten times and keep only regulons that appear in most runs. For a regulator-shortlist application, three to five runs with distinct seeds and an intersection threshold is usually enough.

7. **(Optional) Hand off to pySCENIC.** The `adjacencies.tsv` is the input to `pyscenic ctx` (motif filtering against cisTarget databases) and `pyscenic aucell` (per-cell regulon activity scoring). pySCENIC is not yet a Claude skill in the catalog; run it directly from the CLI on the same machine after the inference step.

## Why this assembly

Rung 2 of the simplicity ladder. GRN inference has narrow input requirements (non-negative expression matrix, TF list, Dask launcher) and a few well-known footguns, all of which the [Arboreto skill](../../catalog/tools/arboreto.html) encapsulates. Plain Claude Code can run Arboreto but will reliably forget the `if __name__ == "__main__":` guard and the TF restriction. There is no need for an autonomous system because the workflow is bounded — a single inference step with documented hyperparameters.

## Availability

Fully open. The Arboreto skill is MIT-licensed (K-Dense Inc.); Arboreto itself is BSD-3-Clause; cisTarget databases are CC-BY. No subscription required.

## Compute requirements

Workstation with GPU is not strictly required — GRNBoost2 is CPU-bound and benefits from cores rather than VRAM. Budget: a 20k-cell × 2k-gene × 1.5k-TF run is roughly 30–90 minutes on 8 CPU cores; 100k-cell runs can take 4–12 hours and 32 GB RAM. For atlas-scale runs (>500k cells), use Dask on a multi-node cluster or downsample per cell-type to 10k–20k cells per cluster, run GRN per cluster, and merge. Memory rather than wall-clock is usually the constraint.

## Evidence

Reported. The Arboreto skill's [SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/arboreto/SKILL.md) documents the GRNBoost2 invocation this recipe wraps. Method evidence is strong: Moerman et al. ([*Bioinformatics* 2019, doi:10.1093/bioinformatics/bty916](https://doi.org/10.1093/bioinformatics/bty916)) introduced GRNBoost2 as a scalable replacement for GENIE3 and benchmarked it against the DREAM5 networks; van de Sande et al. ([*Nature Protocols* 2020, doi:10.1038/s41596-020-0336-2](https://doi.org/10.1038/s41596-020-0336-2)) published the canonical SCENIC workflow protocol around it. Bravo González-Blas et al. ([*Nature Methods* 2023, doi:10.1038/s41592-023-01938-4](https://doi.org/10.1038/s41592-023-01938-4)) showed that GRNBoost2-derived networks recover differentially expressed and ChIP-anchored TFs better than competing methods in the SCENIC+ benchmark. The stochasticity caveat in step 6 reflects the protocol's published guidance, not optional advice.

No peer-reviewed benchmark of "Claude + Arboreto skill" against a hand-written pySCENIC pipeline is known. The skill adds reproducibility and convenience.

## Alternatives considered

- **Plain Claude Code with `pip install arboreto`.** Works but the Dask multiprocessing guard and the TF-restriction footgun bite first-time runs. The skill prevents both.
- **CellOracle, SCENIC+, or deep-learning GRN methods (DeepSEM, scGRN).** SCENIC+ is the right answer when you have paired scATAC-seq and want enhancer-driven networks; SCENIC+ also uses GRNBoost2 internally, so this recipe is the first step inside the bigger pipeline. CellOracle and deep-learning methods are not yet wrapped in catalog tools — defer until they are.
- **Co-expression analysis (WGCNA) only.** Faster but does not separate TFs from targets and does not benefit from the cisTarget motif filtering layer downstream. Reach for WGCNA when you want module-level structure rather than TF→target edges.
- **An autonomous-science system (Biomni).** Biomni can run pySCENIC-style steps as part of a larger analysis but is overkill for a single-step inference. Reach for it when you want the GRN result wired into hypothesis generation, not as a one-off.

## See also

- [Arboreto (Claude Skill)](../../catalog/tools/arboreto.html)
- [Run first-pass QC on a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — the QC step before this recipe.
- [Integrate multiple single-cell RNA-seq datasets across batches](integrate-single-cell-datasets.html) — the integration step before this recipe.
- [AnnData (Claude Skill)](../../catalog/tools/anndata.html)
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — the recipe to consume regulator shortlists into a target dossier.

## Sources

- [`scientific-skills/arboreto/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/arboreto/SKILL.md) — K-Dense-AI, verified 2026-05-28.
- [Moerman T. et al., "GRNBoost2 and Arboreto: efficient and scalable inference of gene regulatory networks", *Bioinformatics* 2019](https://doi.org/10.1093/bioinformatics/bty916) — published 2019.
- [Van de Sande B. et al., "A scalable SCENIC workflow for single-cell gene regulatory network analysis", *Nature Protocols* 2020](https://doi.org/10.1038/s41596-020-0336-2) — published 2020.
- [Bravo González-Blas C. et al., "SCENIC+: single-cell multiomic inference of enhancers and gene regulatory networks", *Nature Methods* 2023](https://doi.org/10.1038/s41592-023-01938-4) — published 2023.
- [Arboreto documentation](https://arboreto.readthedocs.io/) — verified 2026-05-28 (this run).
- [pySCENIC documentation](https://pyscenic.readthedocs.io/) — verified 2026-05-28 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=infer-gene-regulatory-network-from-scrnaseq&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Finfer-gene-regulatory-network-from-scrnaseq.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
