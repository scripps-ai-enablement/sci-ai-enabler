---
title: Test which immune populations differ between groups in a cytometry cohort
parent: All recipes
grand_parent: Recipes
nav_order: 27
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Proposed
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-08
summary: Chain three bioSkills cytometry skills to compensate, cluster, and test a spectral-flow or CyTOF cohort for differential abundance and state without pseudoreplication.
---

# Test which immune populations differ between groups in a cytometry cohort

Take a folder of FCS files from a treated-versus-control immunophenotyping run and end up with a committed R script that emits a per-sample-per-cluster count matrix, an FDR-controlled differential-abundance table, a separate differential-state table, and a provenance record — with the pseudoreplication and compositionality traps closed by construction.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Proposed |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have run a 20–40 parameter spectral flow or mass cytometry panel across a cohort — treated versus control, responder versus non-responder, pre- versus post-vaccination — and the question is which immune population changed. The mechanics are individually well documented and the composition is where analyses go wrong. Three failures recur, and all three produce publishable-looking tables:

**Pseudoreplication.** With 500,000 cells per sample, a t-test or Wilcoxon across all cells has enormous apparent power and no valid error term, because cells within a donor are not independent observations. It will return significant p-values from cohorts with no biological difference at all. **Compositional artifact.** Cluster frequencies sum to 1, so one genuinely expanding population mechanically depresses every other proportion; half your "significant decreases" can be arithmetic. **Conflating abundance and state.** "More activated CD8 T cells" is two different claims — more CD8 T cells, or the same number expressing more CD69 — and they need different tests on different summary statistics.

"Solved" looks like: a committed script that anyone can re-run on the same FCS files and get the same tables, with the per-sample count matrix saved as the audit trail, abundance and state reported separately, and every claim traceable to a row.

## Recommended approach

Three [bioSkills](https://github.com/GPTomics/bioSkills) flow-cytometry skills, installed in one command. Follow the install instructions on each catalog page — the category installer places the whole chain at once:

- [Compensation and Transformation](../../catalog/tools/compensation-transformation.html) — spillover correction and the arcsinh/logicle transform.
- [Clustering and Phenotyping](../../catalog/tools/clustering-phenotyping.html) — FlowSOM/CATALYST population discovery and annotation.
- [Cytometry Differential Analysis](../../catalog/tools/cytometry-differential-analysis.html) — diffcyt DA and DS testing with sample-level aggregation.

1. **Write the two metadata files before touching the data.** They are the load-bearing inputs and they belong in version control:

   - `panel.csv` — one row per channel, with columns `fcs_colname`, `antigen`, `marker_class`. `marker_class` must be `type` (lineage: CD3, CD4, CD19, CD56) or `state` (activation, phospho-epitope, Ki-67) or `none`. The Clustering skill treats this distinction as non-negotiable: **clustering runs on type markers only**, because clustering on CD69 splits one lineage into activation states and makes every subsequent abundance comparison uninterpretable.
   - `metadata.csv` — one row per FCS file, with `file_name`, `sample_id`, `condition`, `patient_id`, `batch`. Include `patient_id` even for unpaired designs; you need it the moment someone asks for a paired analysis.

2. **Have Claude Code draft the pipeline as a script, not a chat.** Ask it to load the three skills and write `cytometry_da.R`, then review the script before running it:

   ```
   Using the bioSkills compensation-transformation, clustering-phenotyping and
   cytometry-differential-analysis skills, write cytometry_da.R that:

   1. Reads panel.csv and metadata.csv; aborts with an explicit message if any
      FCS file, channel, or metadata row is missing rather than silently dropping it.
   2. Compensates on untransformed data, THEN transforms. Record whether the
      spillover matrix came from the recorded $SPILLOVER keyword or was computed
      from single-stain controls. Never transform first.
   3. Builds the CATALYST SCE with prepData(); arcsinh cofactor 5 for CyTOF,
      per-channel via flowVS (or ~150) for fluorescence. Write the cofactor used
      to provenance.
   4. Clusters with FlowSOM on marker_class == "type" only, 10x10 grid,
      maxK 20, set.seed() pinned to a literal in the script.
   5. Emits counts.csv: one row per (sample_id, cluster), with n_cells and
      total_cells_in_sample. This file is the audit trail -- commit it.
   6. Flags any cluster whose MEDIAN cells-per-sample is < 50 as low_support in
      counts.csv. Do not drop it; label it.
   7. Runs diffcyt DA (edgeR on per-sample counts) and DS (limma on per-sample
      per-cluster arcsinh-median of state markers) as TWO separate tables,
      da_results.csv and ds_results.csv. Never merge them.
   8. Design formula includes batch as a covariate. Do not batch-normalize the
      expression before testing.
   9. BH FDR across clusters for DA, and across cluster x marker for DS.
   10. Aborts with untestable.md, not a result table, if any group has fewer
       than 3 biological replicates.
   ```

3. **Read `counts.csv` before you read the results.** Two patterns invalidate the run rather than qualifying it: a cluster present in only some samples usually means a batch or panel problem, not biology; and a `low_support` cluster driving your headline finding means the claim rests on a few dozen cells per donor. Both are cheaper to catch here than after the figure is drawn.

4. **Re-check every DA hit for compositionality.** Any significant cluster whose baseline proportion exceeds roughly 20%, and any hit pointing opposite to the largest observed shift, is suspect. The Differential Analysis skill routes these to simplex-aware methods (sccomp, scCODA, DCATS); mark each row `compositional_confirmed` or `compositional_suspect` in `da_results.csv`. Reporting an unvalidated decrease alongside a large confirmed increase is the single most common overclaim in this analysis.

5. **Capture the command so the next cohort is analysed by the same text.** Save the reviewed prompt as `.claude/commands/test-cytometry-da.md` and commit it with the script. Pin the environment with `renv::snapshot()` — Bioconductor releases change FlowSOM and diffcyt behaviour across versions, so an unpinned lockfile makes next year's re-run a different analysis.

6. **Emit `provenance.json`.** Record: R and Bioconductor release, CATALYST / FlowSOM / diffcyt / edgeR / limma versions, the pinned seed, the arcsinh cofactor, the spillover-matrix source, the design formula and contrast as literal strings, the FDR threshold, a sha256 per input FCS file, and the model id that wrote the script. The design formula in particular is the field reviewers ask about and the one nobody records.

The artifacts you keep: `panel.csv`, `metadata.csv`, `cytometry_da.R`, `.claude/commands/test-cytometry-da.md`, `renv.lock`, `counts.csv`, `da_results.csv`, `ds_results.csv`, `provenance.json`. See [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) for the general pattern.

## Why this assembly

Rung 3, and the escalation is forced by the pipeline's ordering constraints rather than by breadth. Rung 2 fails because no single catalogued skill spans it: compensation must precede transformation (compensation is a linear operation and is invalid after a nonlinear transform), clustering must precede aggregation, and aggregation must precede testing. Get any of those orderings wrong and the numbers still come out. Three skills is also the whole chain — the components share one installer and one `SingleCellExperiment` object, so this is a toolbelt rather than a harness you assemble yourself. Rung 4 buys nothing: there is no hypothesis search here, just a statistical pipeline with sharp edges.

Add the fourth skill, [Cytometry QC](../../catalog/tools/cytometry-qc.html), before step 2 when the run is long, multi-batch, or shows clogs and signal drift — it cleans time-based acquisition anomalies and flags outlier samples. It is conditional rather than core because a clean short acquisition does not need it, and its own ordering rule (margins before any density step) matters only once time-based cleaning is in play.

## Availability

Fully open. The bioSkills collection is MIT. CATALYST, FlowSOM, flowCore, flowWorkspace, diffcyt, edgeR and limma are Bioconductor packages under open licences, installed separately per the catalog pages; note that **edgeR and limma are free for academic use but their licences restrict commercial redistribution** — check before shipping a derived product. Rphenograph installs from GitHub rather than Bioconductor and is optional if you use FlowSOM.

Everything runs locally. No FCS file, panel, or patient metadata leaves the machine, which makes this usable on unpublished clinical cohorts and on data under a governance restriction that rules out cloud analysis. Requires a working R installation with `BiocManager` — the one real setup cost.

## Compute requirements

Laptop, with RAM as the binding constraint rather than CPU. A 20-sample fluorescence cohort at ~200,000 events per sample and 25 channels clusters in a few minutes within 16 GB. A 40-sample CyTOF cohort at 500,000 events per sample (2×10⁷ cells) needs roughly 32–64 GB to hold the `SingleCellExperiment` and will take tens of minutes for FlowSOM plus metaclustering; subsample per sample for the SOM if you are RAM-bound, but **cluster assignment and the counts matrix must use all cells** or rare-population frequencies are biased by the subsampling. UMAP is the one step to subsample without hesitation — 2,000 cells per sample is the skill default and embeddings are for display only. No GPU is used at any step.

## Evidence

**Proposed.** No documented end-to-end run of Claude Code driving these three skills on a real cytometry cohort, with quantitative pass/fail, is known. The underlying methods and each design gate are individually grounded:

- **diffcyt**, the testing engine, combines high-resolution clustering with empirical-Bayes moderated tests adapted from transcriptomics, reporting improved statistical performance "including for rare cell populations" alongside flexible experimental designs ([Weber et al., *Communications Biology* 2019](https://pubmed.ncbi.nlm.nih.gov/31098416/)). That result is the reason step 7 tests clusters rather than manually gated populations.
- **The pseudoreplication gate** (steps 5 and 7, aggregate to sample before testing) rests on the strongest available quantification of the failure, from single-cell transcriptomics rather than cytometry: methods that ignore variation between biological replicates are biased and "can discover hundreds of differentially expressed genes in the absence of biological differences" ([Squair et al., *Nature Communications* 2021](https://pubmed.ncbi.nlm.nih.gov/34584091/)). The statistical error is identical when the unit is a cluster frequency instead of a gene, but note the transfer — that paper is not a cytometry benchmark.
- **The type/state marker split and the arcsinh cofactors** follow the CATALYST CyTOF workflow ([Nowicka et al., *F1000Research* 2017](https://doi.org/10.12688/f1000research.11622.4)), which the Clustering skill implements directly.
- **No head-to-head benchmark** compares an agent-driven run of this chain against a hand-written CATALYST script. The agent's contribution is that the ordering rules, the seed, and the sample-level aggregation are encoded in a reviewed script rather than reconstructed from memory each cohort.

## Alternatives considered

**Manual gating instead of clustering.** Use [Gating Analysis](../../catalog/tools/gating-analysis.html) in place of step 4 when the populations of interest are canonical, a validated gating hierarchy already exists, or the result must be comparable to historical gated data from the same lab. Gates are reproducible and interpretable; they will not find a population nobody drew a gate for, which is exactly what a 30-parameter panel is for. The downstream test is the same either way — the Differential Analysis skill consumes gated populations or clusters interchangeably.

**Plain Claude Code writing CATALYST from scratch (rung 1).** Feasible, and wrong here for a specific reason: the failure modes are silent. A pipeline that transforms before compensating, or clusters on state markers, or tests per-cell, runs cleanly and produces a plausible table. The skills' value is that those three rules are stated where the agent will read them.

**Stop at parsing.** If you only need tidy events out of FCS files for your own Python analysis, [Parse FCS flow-cytometry files](parse-fcs-flow-cytometry-files.html) is rung 2 and sufficient — that recipe is intentionally I/O-only and does not compensate, gate, or cluster.

## See also

- [Compensation and Transformation (bioSkills)](../../catalog/tools/compensation-transformation.html)
- [Clustering and Phenotyping (bioSkills)](../../catalog/tools/clustering-phenotyping.html)
- [Cytometry Differential Analysis (bioSkills)](../../catalog/tools/cytometry-differential-analysis.html)
- [Cytometry QC (bioSkills)](../../catalog/tools/cytometry-qc.html) — the conditional fourth step.
- [Parse FCS flow-cytometry files for downstream immunophenotyping](parse-fcs-flow-cytometry-files.html) — the rung-2 Python I/O path upstream of this recipe.
- [Find which taxa differ between microbiome groups](find-taxa-differing-between-microbiome-groups.html) — the same compositional-data problem in a different assay.
- [Run first-pass QC on a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — analogous per-sample QC discipline on another single-cell modality.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills) — skill collection, MIT; verified 2026-08-08 (this run) via the three catalog pages, each `last_verified: 2026-08-08`.
- [Weber et al., *Communications Biology* 2:183 (2019) — diffcyt](https://pubmed.ncbi.nlm.nih.gov/31098416/) — published 2019; verified 2026-08-08 (this run).
- [Squair et al., *Nature Communications* 12:5692 (2021) — Confronting false discoveries in single-cell differential expression](https://pubmed.ncbi.nlm.nih.gov/34584091/) — published 2021; verified 2026-08-08 (this run).
- [Nowicka et al., *F1000Research* 6:748 (2017) — CyTOF workflow](https://doi.org/10.12688/f1000research.11622.4) — published 2017.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=test-cytometry-clusters-for-group-differences&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftest-cytometry-clusters-for-group-differences.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
