---
title: Find differentially abundant proteins in a label-free proteomics experiment
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-08
summary: Use the MaxQuant skill to take LFQ raw files to a filtered protein table and a differential-abundance list whose imputation sensitivity is reported, not hidden.
---

# Find differentially abundant proteins in a label-free proteomics experiment

Take label-free mass-spectrometry raw files to a defensible list of proteins that changed between two conditions — with contaminants and decoys removed, protein groups reported as groups, and every hit that only exists because a missing value was imputed marked as such.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You ran a label-free shotgun proteomics experiment — treated versus control, knockout versus wild-type, four to six biological replicates a side — and the core facility handed back a folder of `.raw` files. You want the list of proteins whose abundance changed, at a stated FDR, with an effect size you can put in a figure.

Two things make this harder than the equivalent RNA-seq analysis. First, the output table is booby-trapped: MaxQuant's `proteinGroups.txt` ships decoy hits, common contaminants (keratin, trypsin, serum albumin from the FBS in your media) and site-only identifications in the same rows as your real proteins, and every one of them will pass a t-test if you leave it in. Second, **the data are pervasively missing, and the missingness is informative** — a protein is absent from a sample partly because it was genuinely lower and partly because it fell under the instrument's detection limit. How you fill those blanks changes which proteins come out significant, and the default Perseus-style fill is the one benchmarks single out as a poor performer.

"Solved" looks like: a committed script, the three MaxQuant flag columns filtered before anything else, a declared valid-value rule, and a results table where the hits that survive without imputation are distinguishable from the hits that do not.

## Recommended approach

One skill: the [MaxQuant (Claude Skill)](../../catalog/tools/maxquant-proteomics.html). Install it per its catalog page (copy the skill directory, or load SciAgent-Skills as a plugin), and install MaxQuant itself separately from maxquant.org — the skill drives it, it does not ship it.

1. **Fix the search parameters before you search, and commit them.** MaxQuant is configured by an `mqpar.xml`. Decide and write down: the FASTA (a UniProt reference proteome — record its **proteome ID and release**, not just "human"), the enzyme and missed cleavages, the fixed and variable modifications, PSM and protein FDR (1% each is the field default), and whether **match-between-runs** is on. Keep the variable-modification list short: each one multiplies the search space, costs hours, and inflates the number of decoy-competitive candidates. Commit `mqpar.xml` to the repository — it is the most under-shared file in proteomics and the reason most published searches cannot be repeated.

2. **Run the search, then stop and read `summary.txt`.** Before any statistics, check peptide and protein identification counts per raw file and the fraction of MS/MS identified. One file with half the IDs of its neighbours is an injection or column problem, not a biological finding, and it will drive the whole differential result if you let it through. Decide now whether to drop it, and record the decision.

3. **Have Claude Code write the analysis to a script.** Review it before running:

   ```
   Using the maxquant-proteomics skill, write proteomics_de.py that:

   1. Reads proteinGroups.txt and removes, in this order, every row flagged
      "Potential contaminant", "Reverse", or "Only identified by site".
      Writes how many rows each filter removed to the log. This filter is
      mandatory -- do not make it optional or configurable.
   2. Selects LFQ intensity columns only (not raw Intensity, not iBAQ) and
      records the "LFQ min. ratio count" setting used in the search.
   3. Keeps "Majority protein IDs" alongside the leading razor protein for
      every row, so protein groups stay identifiable as groups.
   4. Applies a valid-value rule stated as a literal: a protein is testable
      if it has >= N valid LFQ values in AT LEAST ONE group (not N across
      all samples pooled). Writes filtered_proteins.csv listing kept and
      dropped proteins with their per-group valid counts.
   5. Splits off proteins quantified in one group and in NO sample of the
      other into on_off_proteins.csv. These get reported as presence/absence,
      never as a fold change.
   6. log2-transforms, then median- (or VSN-) normalizes across samples.
      Emits a boxplot of per-sample distributions before and after.
   7. Runs the differential test TWICE on the remaining proteins:
        (a) with the declared imputation method applied, and
        (b) on complete cases only, with NO imputation.
      Emits de_results.csv with one row per protein carrying both sets of
      log2FC / p / BH-adjusted p, plus a boolean imputation_sensitive flag
      that is TRUE when the protein is significant in (a) but not in (b).
   8. Uses moderated t-statistics (limma) rather than a plain per-protein
      t-test, and states the FDR threshold and log2FC floor as literals.
   9. Sets the RNG seed if the imputation method is stochastic.
   ```

4. **Read the results with the `imputation_sensitive` column in view.** A protein significant in both the imputed and complete-case analyses is a finding. A protein significant only after imputation is a hypothesis about the detection limit, and it belongs in a supplementary table with that caveat attached. This one column is the difference between a hit list and a defensible hit list, and it costs one extra model fit.

5. **Report protein groups honestly.** A row in `proteinGroups.txt` is a set of proteins the peptide evidence cannot distinguish. If your headline hit's group contains three isoforms or a family of paralogs, the experiment identified the group, not the member — say so, and design the follow-up (an isoform-specific antibody, a targeted PRM assay) accordingly rather than writing the leading ID into the abstract.

6. **Pin and record.** `requirements.txt` for the Python environment; `provenance.json` capturing the MaxQuant version, the FASTA proteome ID **and release date**, the contaminant list version bundled with that MaxQuant release, the match-between-runs setting, the valid-value rule, the imputation method and seed, the FDR and fold-change thresholds, a sha256 of `proteinGroups.txt`, and the model id that wrote the script.

Artifacts to commit: `mqpar.xml`, `proteomics_de.py`, `filtered_proteins.csv`, `on_off_proteins.csv`, `de_results.csv`, `requirements.txt`, `provenance.json`. See [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) for the general pattern.

## Why this assembly

Rung 2, and it stops there. One skill spans the whole path — running MaxQuant, parsing `proteinGroups.txt`, the contaminant/decoy/site filter, normalization, imputation, FDR-controlled testing and the volcano plot — so no toolbelt is needed and no autonomous system applies.

Rung 1 fails for a specific, checkable reason: an agent writing this from general knowledge will read the LFQ columns and run a t-test. It will not reliably strip all three flag columns, it will not distinguish `LFQ intensity` from `Intensity` and `iBAQ`, and it will impute silently with the default down-shifted normal because that is what every tutorial does. Those are exactly the three errors that make a proteomics result wrong rather than noisy, and they are invisible in the output — a contaminated, imputation-driven hit list looks identical to a real one. The skill states the filter and the quantification-column rules where the agent reads them.

## Availability

Fully open in the sense that matters — no subscription, no account, no institutional gate on use. Two license details to know. The skill collection is community OSS (CC BY 4.0 for the skill text, Apache-2.0 upstream). **MaxQuant itself is free of charge but not open source**: the download requires accepting the Max Planck Institute of Biochemistry's terms, and Bioconda packages it as license-restricted, so you may not freely redistribute it inside a derived pipeline or container image you publish. Check the terms before baking it into a shared Docker image.

Platform is the practical gate: MaxQuant supports **Windows 10/11 or Server 2016+, and Ubuntu 20.04+**, and requires .NET 8.0 (since v2.6.3.0). There is no macOS build and no Linux GUI — on Linux you run `dotnet MaxQuant/bin/MaxQuantCmd.dll mqpar.xml` headless, which means the `mqpar.xml` is usually authored in the Windows GUI and then path-rewritten with `--changeFolder`. Everything runs locally, so unpublished raw files never leave your machine.

## Compute requirements

Laptop-class hardware works for a laptop-sized experiment; the search is the only expensive step and it is CPU- and disk-bound, not GPU-bound.

A two-group experiment with 5 replicates a side (10 raw files, ~1 GB each) against a human reference proteome with two variable modifications runs overnight on a 8-core machine with 32 GB RAM. Budget 32 GB as the floor and 64 GB as comfortable — MaxQuant is memory-hungry and a swap-thrashing run can take days. Note that large parts of a MaxQuant analysis are single-threaded regardless of the thread count you set, so adding cores gives sub-linear returns and fast local disk matters more than core count. Keep 3–5× the raw-file volume free for intermediate files.

Scale up hardware, not the recipe, past ~50 raw files: a many-core server, or the GPU-accelerated MSFragger/FragPipe search named under Alternatives. Everything from step 3 onward — the filtering, normalization and testing — is seconds on any machine.

## Evidence

**Proposed.** No documented run of Claude Code driving this skill on a real proteomics cohort with quantitative pass/fail is known. The two design decisions the recipe turns on are each grounded in a published benchmark:

- **Imputation choice changes the answer, and the popular choices are the bad ones.** Evaluating imputation methods against downstream-centric criteria rather than reconstruction error, "although many methods exist for imputing missing values, in practice, the most commonly used methods are among the worst performing", and imputation "does not necessarily improve the ability to identify differentially expressed peptides" ([Harris, Fondrie, Oh & Noble, *J. Proteome Research* 2023](https://doi.org/10.1021/acs.jproteome.3c00205)). This is the direct justification for step 7's paired imputed / complete-case run and the `imputation_sensitive` flag: if imputation may not help detection at all, its contribution to your hit list must be visible.
- **The sensitivity is driven by the MNAR fraction, which you cannot measure.** Across a large benchmark dataset and an immune-cell dataset with simulated missingness, imputation accuracy "is primarily affected by the MNAR rate rather than the MV rate, and downstream analysis can be largely impacted by the selection of imputation methods"; a random-forest method achieved the lowest error with a false altered-protein discovery rate under 5% ([Jin et al., *Scientific Reports* 2021](https://doi.org/10.1038/s41598-021-81279-4)). Since you do not know your MNAR rate, reporting both branches is cheaper than defending a choice.
- **The field has not settled.** A 2025 likelihood-based method that models the instrument censoring explicitly outperforms all pre-existing imputation methods across designs and metrics, and its authors call for a paradigm change in proteomics imputation ([Etourneau et al., *Biostatistics* 2025](https://doi.org/10.1093/biostatistics/kxaf006)) — another reason not to let a single imputation default carry a published claim.
- **The quantification layer is well validated.** MaxLFQ, the algorithm behind the LFQ columns step 3 selects, recovers known mixing ratios across the protein expression range on two-proteome benchmark datasets and quantifies fold changes over several orders of magnitude ([Cox et al., *Molecular & Cellular Proteomics* 2014](https://doi.org/10.1074/mcp.M113.031591)). The uncertainty in this recipe is downstream of the intensities, not in them.

## Alternatives considered

**Reanalyze a public dataset instead of generating one.** If the question is whether someone has already measured this, the [PRIDE (Claude Skill)](../../catalog/tools/pride-database.html) searches PRIDE Archive by organism, instrument, disease and software and pulls the RAW, RESULT and FASTA files. Fetching a matching project and running steps 1–6 on it is the same recipe with a different step 0, and it is the right first move before committing instrument time. It is not a separate recipe because everything after the download is identical.

**A different search engine.** FragPipe/MSFragger is dramatically faster and the right choice for open/wide-window searches or large cohorts; Proteome Discoverer is the path if your facility is Thermo-native and wants vendor support. The skill names both. Neither is catalogued, so this recipe cannot give you a followable path to them — the statistics from step 3 onward transfer unchanged to whatever protein table they emit.

**Skip imputation entirely.** Legitimate, and increasingly common: run only the complete-case branch and report the on/off proteins qualitatively. You lose the proteins missing in one or two samples of an otherwise complete group, which in a 5-replicate design is a real cost. Run it as branch (b) either way and see how much it actually costs you before deciding.

**Downstream enrichment.** Once you have the hit list, [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) picks up from the significant protein IDs — with the standing caveat that the background set must be the proteins you *detected*, not the whole genome.

## See also

- [MaxQuant (Claude Skill)](../../catalog/tools/maxquant-proteomics.html)
- [PRIDE (Claude Skill)](../../catalog/tools/pride-database.html) — public dataset discovery and download, the reanalysis entry point.
- [Run bulk RNA-seq differential expression](run-bulk-rnaseq-differential-expression.html) — the transcript-level counterpart, and a useful contrast: counts are not missing-not-at-random.
- [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) — what to do with the hit list.
- [Quantify western blot densitometry](quantify-western-blot-densitometry.html) — the orthogonal validation most reviewers will ask for.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) — skill collection; verified 2026-08-08 (this run) against the catalog page (`verification: works` 2026-07-20, security cleared 2026-07-20).
- [Harris, Fondrie, Oh & Noble — Evaluating Proteomics Imputation Methods with Improved Criteria, *J. Proteome Research* (2023)](https://doi.org/10.1021/acs.jproteome.3c00205) — published 2023; verified 2026-08-08 (this run).
- [Jin et al. — A comparative study of evaluating missing value imputation methods in label-free proteomics, *Scientific Reports* 11:1760 (2021)](https://doi.org/10.1038/s41598-021-81279-4) — published 2021; verified 2026-08-08 (this run).
- [Etourneau et al. — Penalized likelihood optimization for censored missing value imputation in proteomics, *Biostatistics* (2025)](https://doi.org/10.1093/biostatistics/kxaf006) — published 2025; verified 2026-08-08 (this run).
- [Cox et al. — Accurate proteome-wide label-free quantification by delayed normalization and maximal peptide ratio extraction, termed MaxLFQ, *Mol. Cell. Proteomics* 13:2513 (2014)](https://doi.org/10.1074/mcp.M113.031591) — published 2014; verified 2026-08-08 (this run).
- [MaxQuant Download & Installation documentation](https://cox-labs.github.io/coxdocs/Download_Installation.html) — platform, .NET 8 and headless-Linux requirements; verified 2026-08-08 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=find-differentially-abundant-proteins-in-lfq-ms&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ffind-differentially-abundant-proteins-in-lfq-ms.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
