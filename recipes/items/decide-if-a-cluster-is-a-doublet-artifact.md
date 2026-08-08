---
title: Decide whether a suspicious cluster is a doublet artifact
parent: All recipes
grand_parent: Recipes
nav_order: 7
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-08
summary: Use the bioSkills Doublet Detection skill plus two orthogonal checks to rule on whether an intermediate single-cell cluster is real or two cells in one droplet.
---

# Decide whether a suspicious cluster is a doublet artifact

Score a single-cell dataset for multi-cell droplets, aggregate the calls to the cluster you are worried about, and reach a stated verdict — real population, doublet artifact, or undetermined — instead of arguing about a UMAP island.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Your single-cell clustering returned a small population sitting between two well-defined lineages and co-expressing markers of both — CD3 and CD19, or an epithelial program alongside a fibroblast one. It could be a genuine transitional or hybrid state, which is a paper. It could be two cells captured in one droplet, which is an artifact. The UMAP looks the same either way, and a cluster of doublets lands exactly where a transitional state would.

The stakes are asymmetric and both directions hurt. Publish a doublet cluster as a novel intermediate and the finding does not replicate. Delete a real transitional population because a detector flagged it and you have thrown away the result. The decision also cannot be deferred: doublets distort clustering, marker genes and differential expression for the *whole* dataset, so it has to be made before the analysis is built on top of it.

"Solved" looks like: doublet scores computed correctly (per sample, on raw counts, at the right expected rate), aggregated per cluster, cross-checked against two pieces of evidence the scores do not use, and a recorded three-way verdict rather than a silent deletion.

## Recommended approach

One skill: [Doublet Detection (bioSkills)](../../catalog/tools/doublet-detection.html). Install it per its catalog page (the `single-cell` category installer, or copy the single skill directory), then install your chosen detector on first use.

1. **Get the expected doublet rate right before running anything.** It is roughly 0.8% per 1,000 recovered cells (`dbr.per1k = 0.008`), taken from the **recovered-cell count of the lane**. For a multiplexed pool this is the total lane count, not the demultiplexed subset you happen to be analysing — using the subset systematically underestimates the rate and is the single most common way this step is set up wrong. Write the number down.

2. **Score per sample, on raw counts, after basic QC and before integration or clustering.** All of these detectors work by simulating artificial doublets from the observed cells and asking which real cells look like the simulations. Run them on a merged or integrated object and the simulation pool is contaminated with cells from other samples, which is not what happened in any droplet. If you have already clustered, go back and score the pre-integration per-sample objects; you can map the calls forward onto your existing clusters by cell barcode.

3. **Have Claude Code write the analysis to a script.** Review it before running:

   ```
   Using the bioSkills doublet-detection skill, write doublet_call.R (or .py)
   that:

   1. Loops over per-sample raw-count objects -- never the merged object --
      and refuses to run if handed one with more than one sample in it.
   2. Sets the expected doublet rate from the LANE recovered-cell count
      (dbr.per1k = 0.008 unless I override it); records the number used.
   3. Runs TWO detectors from the skill's panel (scDblFinder and Scrublet as
      the default pair) and applies a homotypic adjustment via
      modelHomotypic() so same-cell-type pairs are discounted.
   4. Emits doublet_scores.csv: one row per cell barcode, with each method's
      score and call, plus n_methods_calling. Do not average the scores.
   5. Emits the Scrublet score histogram per sample. If it is not bimodal,
      flag the sample -- the automatic cutoff is unreliable there and needs
      a manual threshold recorded as a literal.
   6. Maps calls onto my existing cluster labels and emits
      cluster_doublet_summary.csv: per cluster, n_cells, fraction called by
      each method, median total UMI and median genes detected, and the same
      two medians for the dataset as a whole.
   7. Does NOT delete any cells. Flag only.
   ```

4. **Run the two checks the scores do not use.** These are what actually decide it, because a detector's score and a detector's score are not independent evidence:
   - **Library size.** A cluster of true doublets carries roughly twice the RNA of its parents. If the cluster's median total UMI and gene count sit near the sum of the two putative parent clusters' medians rather than between them, that is a doublet signature. A real transitional state has a normal library size.
   - **Additivity of the two programs.** In a doublet, the two lineage programs appear at roughly the level you would get by adding two cells' transcriptomes — both at near-parental strength, with no intermediate regulatory state. In a genuine hybrid or transitioning cell you typically see one program attenuated, the other rising, and transcription factors that belong to neither parent alone.

5. **Record a three-way verdict, defaulting to `undetermined`.** Write `verdict.md` naming the cluster and stating one of `doublet_artifact`, `real_population`, `undetermined`, with the doublet fraction, the library-size comparison and the additivity call listed as separate lines of evidence rather than merged into a score. Default to `undetermined` — and say so in the paper — when the detectors disagree, when the score histogram was not bimodal, or when the parents are closely related cell types. **A clean negative is not proof.** Homotypic doublets, two cells of the same type, are largely undetectable by any of these methods, so "no cells flagged" means the detectors found nothing, not that there is nothing there.

6. **Act on the verdict, then re-run downstream.** If `doublet_artifact`, remove those cells and repeat clustering from the beginning — removing cells changes the neighbourhood graph, so keeping the old labels is not valid. If `real_population` or `undetermined`, keep the cells and keep the doublet flag as a cell-level annotation so any downstream differential result can be re-checked with the flagged cells excluded.

7. **Pin and record.** `renv::snapshot()` or `requirements.txt`; `provenance.json` capturing the detector versions, the expected doublet rate **and the cell count it was derived from**, any manual score cutoff, the homotypic adjustment setting, a sha256 of the input matrices, and the model id that wrote the script.

Artifacts to commit: `doublet_call.R`, `doublet_scores.csv`, `cluster_doublet_summary.csv`, `verdict.md`, the lockfile and `provenance.json`. See [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) for the general pattern.

## Why this assembly

Rung 2, and it stops there. One skill owns the detector panel, the per-sample-raw-counts rule, the expected-rate arithmetic, the homotypic adjustment and the flag-don't-delete discipline. No second component and no autonomous system is needed.

Rung 1 fails on the setup, not the code. Plain Claude Code will call `scDblFinder(sce)` correctly — and then run it on the merged object, take the expected rate from the demultiplexed subset, skip the homotypic adjustment and drop the flagged cells in the same breath. None of those errors surfaces as a warning; they surface as a hit list you cannot reproduce. The skill states all four rules where the agent reads them. Steps 4–5 are the recipe's own addition, because the skill scores cells and the reader's question is about a cluster.

## Availability

Fully open. The bioSkills collection is MIT (root LICENSE confirmed on the catalog page's 2026-08-03 security review). scDblFinder, Scrublet (bundled with scanpy), DoubletFinder, Seurat and scanpy are separately installed open-source packages — check the individual license of whichever detector you pick before redistributing it inside a commercial pipeline.

Everything runs locally on your count matrices. No API key, account, upload or subscription, so this is usable on unpublished and consented-cohort data. Requires either a working R installation with `BiocManager` (scDblFinder, DoubletFinder) or Python with scanpy 1.10+ (Scrublet); the recommended default pair spans both, so a mixed environment is the path of least friction.

## Compute requirements

Laptop. Simulate-and-score detection on a typical 5,000–10,000-cell sample runs in one to a few minutes within 8–16 GB RAM. Cost scales with cell count per sample and with the number of simulated doublets, not with the number of samples — a 20-sample study is 20 short independent jobs and parallelizes trivially. No GPU.

The one place to watch memory is a very deeply loaded lane (50,000+ cells), where the simulated-doublet matrix doubles peak footprint; 32 GB is comfortable there. Re-running clustering after removal (step 6) is usually the longer wall-clock item, not the detection itself.

## Evidence

**Proposed.** No documented run of Claude Code driving this skill to adjudicate a specific cluster is known. The method layer underneath it is well benchmarked:

- **Nine detection methods compared on 16 real datasets with experimentally annotated doublets plus 112 realistic synthetic datasets**, scoring detection accuracy, impact on downstream analyses and computational efficiency. Methods "exhibited diverse performance and distinct advantages in different aspects"; DoubletFinder had the best detection accuracy overall and cxds the highest efficiency ([Xi & Li, *Cell Systems* 2021](https://doi.org/10.1016/j.cels.2020.11.008)). Two things follow for this recipe. The diversity of performance is why step 3 runs two detectors and keeps them as separate columns. And note the tension worth knowing: the benchmark's accuracy winner is DoubletFinder, while the skill's stated 2024–2026 default is scDblFinder — no benchmark of that generation of tools at this scale is available to arbitrate, which is a further reason not to let one score decide.
- **The methods are executable and comparable in practice**, via a package that installs and runs eight of them behind one interface ([Xi & Li, *STAR Protocols* 2021](https://doi.org/10.1016/j.xpro.2021.100699)) — useful if you want to add a third detector to step 3.
- **Doublet detection interacts with the rest of the pipeline** rather than sitting cleanly before it: a multi-step framework covering filtering, doublet detection, normalization, feature selection, dimensionality reduction and clustering found interactions between analysis steps that single-step benchmarks miss ([Germain, Sonrel & Robinson, *Genome Biology* 2020](https://doi.org/10.1186/s13059-020-02136-7)). This is the grounding for step 6's requirement to re-cluster from scratch after removal.
- **No benchmark exists** for the cluster-level adjudication in steps 4–5. Library-size doubling and program additivity are standard field practice rather than validated criteria; they are in the recipe because they are orthogonal to the detector score, not because their sensitivity is known.

## Alternatives considered

**Genetic or barcode demultiplexing, if your samples were pooled.** When several donors are multiplexed into one lane, SNP-based demultiplexing identifies cross-donor doublets directly from genotype rather than by simulation — much stronger evidence than a score. Leading tools reach 80–85% accuracy, with accuracy falling as the doublet percentage rises ([Fu et al., *Briefings in Bioinformatics* 2025](https://doi.org/10.1093/bib/bbaf371)). This only catches doublets between *different* donors, so it complements rather than replaces step 3. No demultiplexing tool is catalogued, so this recipe cannot give you a followable path to one.

**Fold it into general QC instead.** If you are at the start of an analysis with no particular cluster in question, [QC single-cell RNA-seq data](qc-single-cell-rna-seq.html) is the right recipe and doublet removal is one of its steps. Come here when you already have a clustering and a specific suspicious population — the deliverable there is a filtered object, the deliverable here is a verdict about one cluster.

**Just delete anything flagged.** Fast and wrong often enough to matter. The detectors are calibrated to an expected rate, so at a fixed threshold they will flag approximately that many cells whether or not they are doublets — meaning a cluster of a genuinely rare intermediate cell type is a prime candidate for deletion. Flag first, adjudicate, then delete.

## See also

- [Doublet Detection (bioSkills)](../../catalog/tools/doublet-detection.html)
- [QC single-cell RNA-seq data](qc-single-cell-rna-seq.html) — the upstream filtering step this follows.
- [Annotate cell types in single-cell data](annotate-cell-types-in-single-cell-data.html) — what you do once the cluster survives.
- [Integrate single-cell datasets](integrate-single-cell-datasets.html) — must happen *after* this, not before.
- [Infer cell–cell communication from scRNA-seq](infer-cell-cell-communication-from-scrnaseq.html) — an analysis that doublets corrupt particularly badly, since a doublet looks like a cell expressing both ligand and receptor.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills) — skill collection, MIT; verified 2026-08-08 (this run) against the catalog page (`verification: works` 2026-08-03, security cleared 2026-08-03).
- [Xi & Li — Benchmarking Computational Doublet-Detection Methods for Single-Cell RNA Sequencing Data, *Cell Systems* 12:176 (2021)](https://doi.org/10.1016/j.cels.2020.11.008) — published 2021; verified 2026-08-08 (this run).
- [Xi & Li — Protocol for executing and benchmarking eight computational doublet-detection methods, *STAR Protocols* (2021)](https://doi.org/10.1016/j.xpro.2021.100699) — published 2021; verified 2026-08-08 (this run).
- [Germain, Sonrel & Robinson — pipeComp, a general framework for the evaluation of computational pipelines, *Genome Biology* 21:227 (2020)](https://doi.org/10.1186/s13059-020-02136-7) — published 2020; verified 2026-08-08 (this run).
- [Fu et al. — Benchmarking of computational demultiplexing methods for single-nucleus RNA sequencing data, *Briefings in Bioinformatics* (2025)](https://doi.org/10.1093/bib/bbaf371) — published 2025; verified 2026-08-08 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=decide-if-a-cluster-is-a-doublet-artifact&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdecide-if-a-cluster-is-a-doublet-artifact.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
