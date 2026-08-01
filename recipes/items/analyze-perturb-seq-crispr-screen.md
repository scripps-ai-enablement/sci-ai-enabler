---
title: Analyze a Perturb-seq CRISPR screen for perturbation effects
parent: All recipes
grand_parent: Recipes
nav_order: 1
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-08-01
summary: Use the Perturb-seq Analysis skill to assign guides, remove escapers, test with a calibrated method, and rank perturbations by E-distance.
---

# Analyze a Perturb-seq CRISPR screen for perturbation effects

Hand Claude Code a single-cell CRISPR screen with guide counts; get back a calibrated per-perturbation differential-expression table and an E-distance effect-size ranking that does not treat cells as independent replicates.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

You ran a Perturb-seq (or CROP-seq) screen: a pooled sgRNA library, single-cell RNA-seq readout, and now an `.h5ad` with a guide-count layer and a few hundred perturbations. The question is which perturbations changed the transcriptome, by how much, and in which direction. The obvious move — call each perturbed cell a replicate and run `rank_genes_groups` against the non-targeting controls — is also the move that produces a hit list you cannot defend.

Three failure modes cause most of the damage. **Guide assignment** is a mixture problem, not a threshold problem: ambient guide reads mean a flat cutoff either drops real cells or admits contaminated ones. **Escapers** — cells that took up a guide but show no transcriptional effect, from incomplete editing or in-frame repair — dilute every comparison toward null. And the **replication unit is the transfection, not the cell**: per-cell tests treat thousands of correlated cells from one infection as independent, which inflates significance in essentially every dataset. A benchmark of low-MOI association testing methods found that existing approaches produce excess false positives from exactly this class of problem. Solved looks like: a guide-assignment table with posterior probabilities, a knockout/non-perturbed label per cell, a calibrated DE table, and a comparable effect magnitude per perturbation — all reproducible from a committed script.

## Recommended approach

1. **QC the transcriptome first.** Run the [single-cell QC recipe](qc-single-cell-rna-seq.html) on the expression matrix before touching guides. Ambient RNA and doublets corrupt guide calling and effect sizes at the same time; a doublet carrying two guides looks like a genetic interaction.

2. **Install the [Perturb-seq Analysis skill](../../catalog/tools/perturb-seq.html)** and keep [Scanpy](../../catalog/tools/scanpy.html) and [AnnData](../../catalog/tools/anndata.html) available for the data structures. The skill is a `SKILL.md` that Claude executes locally, so the Python stack (Pertpy, scanpy, anndata) installs on first use; the SCEPTRE and Seurat/scMAGeCK paths are R installs — decide up front whether you want the R leg, because it changes the environment file.

3. **Assign guides with the mixture-model posterior, not a threshold.** Ask for both, and keep the flat cutoff only as a sanity check:

   ```
   Use the Perturb-seq Analysis skill on data/screen.h5ad. The guide
   counts are in layer "guide_counts"; non-targeting controls are the
   guides whose name starts with "NTC_".

   Assign guides by mixture-model posterior. Write one row per cell to
   results/guide_assignment.csv with: cell_id, assigned_guide,
   assigned_target, posterior, n_guides_called, and a
   flat_threshold_call column at UMI >= 5 for comparison. Report how
   many cells the two methods disagree on. Do not drop unassigned
   cells silently — label them "unassigned" and keep the row.
   ```

   Record the MOI regime in the script header: low-MOI designs (~1 guide/cell) discard 70–90% of cells and constrain which tests are valid; high-MOI designs let you ask combinatorial questions but complicate assignment.

4. **Classify escapers with a Mixscape perturbation signature.** Have the skill compute the signature and the two-component knockout / non-perturbed split per target, then write the labels into the same table:

   ```
   Compute the Mixscape perturbation signature and the per-target
   knockout vs non-perturbed classification. Add mixscape_class and
   mixscape_p_ko columns to results/guide_assignment.csv, and emit
   results/escaper_rates.csv with one row per target: n_cells,
   n_ko, n_np, frac_escaper. Flag any target where frac_escaper > 0.5
   as low-efficiency rather than as a null result — those two are not
   the same claim.
   ```

   That last distinction is the point of the step. A target with 80% escapers and no DE signal is an editing-efficiency finding, not evidence that the gene does nothing.

5. **Test with a calibrated method, at the right replication unit.** Choose by design, and say so in the script:
   - **Low-MOI, one guide per cell:** SCEPTRE conditional resampling, which was built to fix the calibration failures in this regime.
   - **You have ≥2–3 independent transfection replicates:** pseudobulk per replicate per perturbation, then DESeq2 or edgeR — the same machinery as the [bulk RNA-seq DE recipe](run-bulk-rnaseq-differential-expression.html), applied to aggregated counts.

   Either way, forbid the shortcut explicitly:

   ```
   Do not run per-cell rank_genes_groups as the primary test. Use
   SCEPTRE (low-MOI) or pseudobulk-per-replicate DE with >= 2
   replicates. Write results/de_<target>.csv per target plus a
   results/de_summary.csv with target, n_replicates, method,
   n_sig_genes at FDR 0.05, and the test used. If a target has fewer
   than 2 replicates, emit it with method="underpowered" and no
   p-values rather than a per-cell test.
   ```

6. **Rank perturbations by E-distance in a fixed embedding.** E-distance is an energy statistic between the perturbed and control cell sets; computed in a single shared PCA space it gives magnitudes that are comparable across perturbations, which raw DE-gene counts are not. Fix the embedding once (same PCs, same HVG set, same scaling) and reuse it for every perturbation, or the ranking is an artifact of the embedding.

7. **Separate composition from expression.** If a perturbation shifts cell-state proportions, a within-state expression test will read as a change even when nothing inside a state moved. Run Milo or scCODA differential abundance alongside the DE, and keep the two answers in separate columns.

8. **If you are evaluating a perturbation-prediction model, benchmark it against the additive baseline.** Hold out whole perturbations (not random cells) and score against a deliberately simple linear/additive predictor. Five foundation models and two other deep-learning models failed to beat such baselines in a 2025 *Nature Methods* comparison, so the baseline is the bar, not a formality.

9. **Land the artifact.** The run should leave a committed `run_perturbseq.py` (or a `.claude/commands/perturbseq-screen.md` if you will repeat it across screens), a pinned `requirements.txt` (plus `renv.lock` if you took the R leg), the `results/*.csv` tables above, and a `provenance.json` recording: Pertpy / scanpy / anndata / SCEPTRE (or DESeq2, edgeR) versions, the bioSkills commit SHA, the input `.h5ad` sha256, the MOI regime, the guide-assignment posterior cutoff, the PCA parameters used for E-distance, and the model id. See the [reproducibility guide](../../guide/advanced/reproducibility.html) for the pattern.

## Why this assembly

Rung 2 of the simplicity ladder, and it stops there. The analysis is a bounded, single-dataset pipeline — no external database lookups, no literature search, no autonomous exploration — so nothing above rung 2 earns its cost. What plain Claude Code gets wrong is not the code but the statistics: given an `.h5ad` and a guide layer it will produce a threshold-based guide call and a per-cell Wilcoxon test, both of which run cleanly and are both wrong in the same direction. The skill encodes the mixture-model default, the Mixscape escaper step, the replication-unit rule, and the fixed-embedding E-distance convention, which is precisely the set of decisions a first-time analyst does not know to make.

## Availability

Fully open. The [Perturb-seq Analysis skill](../../catalog/tools/perturb-seq.html) is MIT (GPTomics bioSkills); Pertpy, scanpy and anndata are BSD-3-Clause. One caveat if you take the R leg: DESeq2 and edgeR are copyleft (LGPL and GPL respectively), which matters if you redistribute a derived pipeline rather than just run it. The Python-only path (Pertpy pseudobulk plus a permissively-licensed test) avoids that. No subscription or account is required, and nothing leaves your machine — relevant if the screen is unpublished.

## Compute requirements

No GPU is needed; this is CPU-, and mostly RAM-, bound. A typical targeted screen (~50k cells × 2k HVGs, a few hundred targets) runs comfortably in 16–32 GB: guide assignment and Mixscape are minutes, and E-distance across a few hundred perturbations in a fixed 50-PC space is minutes more. SCEPTRE resampling is the expensive step and scales with perturbations × genes tested — restrict to a candidate gene set rather than the full transcriptome for a first pass. Genome-scale screens (millions of cells) are where the `Workstation with GPU` tier applies for its RAM rather than its VRAM: expect to work on a backed `.h5ad` with chunked reads, or to split by target batch and merge the result tables. Budget disk for the per-target DE files — a few hundred targets × full-transcriptome output is easily tens of GB.

## Evidence

`Proposed`. No documented attempt at running this exact assembly — Claude Code driving the Perturb-seq Analysis skill — on a screen is known, and no benchmark compares it to a hand-written Pertpy pipeline. The individual steps, however, are unusually well evidenced, and each one exists in the skill because a published benchmark showed the naive alternative fails:

- **Calibrated testing.** Barry et al. ran the first comprehensive benchmark of association-testing methods for low-MOI Perturb-seq and found that existing methods produce excess false positives, tracing it to sparsity, confounding and model misspecification; SCEPTRE low-MOI was developed to resolve those and showed improved calibration and power ([*Genome Biology* 2024](https://doi.org/10.1186/s13059-024-03254-2)).
- **E-distance as effect size.** Peidli et al. harmonized 44 single-cell perturbation datasets and introduced E-statistics for quantifying perturbation effects and significance, demonstrating E-distance as a general distance between sets of single-cell profiles, with accompanying recommendations on cell counts and read depth ([*Nature Methods* 2024](https://doi.org/10.1038/s41592-023-02144-y)).
- **The framework itself.** Pertpy is peer-reviewed as a modular end-to-end perturbation-analysis framework in the scverse ecosystem, including the perturbation-distance implementations this recipe uses ([Heumos et al., *Nature Methods* 2026](https://doi.org/10.1038/s41592-025-02909-7)).
- **The model-benchmarking step.** Ahlmann-Eltze et al. compared five foundation models and two other deep-learning models against deliberately simple baselines for predicting transcriptome changes after single or double perturbations; none outperformed the baselines ([*Nature Methods* 2025](https://doi.org/10.1038/s41592-025-02772-6)). This is why step 8 requires the additive baseline rather than treating it as optional.

The closest documented analogue to the agent-driven form is the [GRN inference recipe](infer-gene-regulatory-network-from-scrnaseq.html), where a skill similarly exists to enforce invocation rules that a general-purpose agent reliably skips.

## Alternatives considered

- **Plain Claude Code with `pip install pertpy`.** Rung 1, and tempting, since Pertpy exposes all of these functions. Reach for it only if you already know which test your design licenses. Without the skill's guidance the default path is threshold guide-calling plus a per-cell test, which is fast, clean-looking, and the exact combination the Barry et al. benchmark showed to be miscalibrated.
- **Seurat + Mixscape in R.** A well-trodden route with the same escaper logic, and the right choice if your lab's screen analyses already live in R and you want scMAGeCK alongside. The skill covers this leg too; the Python path is the default here only because the QC and integration recipes upstream are scanpy-based.
- **A perturbation-prediction model (GEARS or a foundation model) instead of the screen analysis.** Different problem. Prediction models extrapolate to perturbations you did not run — GEARS reported 40% higher precision than prior approaches at classifying genetic-interaction subtypes ([Roohani et al., *Nature Biotechnology* 2024](https://doi.org/10.1038/s41587-023-01905-6)) — but they do not replace measuring the screen you have. Use step 8 to check any such model against the additive baseline before trusting it.
- **An autonomous-science system.** Overkill. The workflow is a fixed sequence over one dataset with no open-ended search; escalating adds cost and non-determinism without answering anything the skill cannot.

## See also

- [Perturb-seq Analysis (Claude Skill)](../../catalog/tools/perturb-seq.html)
- [Design CRISPR sgRNAs for a gene knockout](design-crispr-sgrnas-for-a-gene-knockout.html) — the library-design step upstream of the screen.
- [Run first-pass QC on a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — run before guide assignment.
- [Run differential expression on bulk RNA-seq counts](run-bulk-rnaseq-differential-expression.html) — the DESeq2/edgeR machinery the pseudobulk leg reuses.
- [Infer a gene-regulatory network from single-cell RNA-seq](infer-gene-regulatory-network-from-scrnaseq.html) — a complementary route to regulator shortlists when you have no screen.
- [Scanpy (Claude Skill)](../../catalog/tools/scanpy.html) · [AnnData (Claude Skill)](../../catalog/tools/anndata.html)

## Sources

- [`single-cell/perturb-seq/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/single-cell/perturb-seq/SKILL.md) — GPTomics bioSkills; catalog page verified 2026-08-01.
- [Barry T. et al., "Robust differential expression testing for single-cell CRISPR screens at low multiplicity of infection", *Genome Biology* 2024](https://doi.org/10.1186/s13059-024-03254-2) — published 2024; verified 2026-08-01 (this run).
- [Peidli S. et al., "scPerturb: harmonized single-cell perturbation data", *Nature Methods* 2024](https://doi.org/10.1038/s41592-023-02144-y) — published 2024; verified 2026-08-01 (this run).
- [Heumos L. et al., "Pertpy: an end-to-end framework for perturbation analysis", *Nature Methods* 2026](https://doi.org/10.1038/s41592-025-02909-7) — published 2026; verified 2026-08-01 (this run).
- [Ahlmann-Eltze C., Huber W., Anders S., "Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines", *Nature Methods* 2025](https://doi.org/10.1038/s41592-025-02772-6) — published 2025; verified 2026-08-01 (this run).
- [Roohani Y. et al., "Predicting transcriptional outcomes of novel multigene perturbations with GEARS", *Nature Biotechnology* 2024](https://doi.org/10.1038/s41587-023-01905-6) — published 2024; verified 2026-08-01 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=analyze-perturb-seq-crispr-screen&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fanalyze-perturb-seq-crispr-screen.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
