---
title: Find which taxa differ between microbiome groups
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-08
summary: Use the bioSkills Differential Abundance skill to test an amplicon feature table with several compositionally-aware methods and report their consensus, not one tool's hit list.
---

# Find which taxa differ between microbiome groups

Take a 16S feature table and sample metadata to a defensible list of taxa that differ between your groups — tested by several compositionally-aware methods at once, with the intersection reported as high-confidence and every per-taxon disagreement kept visible instead of hidden by the tool you happened to pick.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have an ASV or OTU table from a 16S run and a grouping variable — case versus control, antibiotic-exposed versus naive, diet arm A versus B. Diversity analysis has already told you the communities differ overall. The next question, and the one that ends up in the abstract, is *which taxa*.

This is the step where microbiome papers become irreproducible, and the reason is measured rather than anecdotal: run 14 differential-abundance methods on the same table and they return drastically different numbers and sets of significant features, with the count for many tools tracking sample size and sequencing depth rather than biology. Pick one tool, report its list, and you have reported a property of the tool. Two further traps compound it: counts are **compositional** — they carry relative, not absolute, abundance, so "*Bacteroides* decreased" may mean something else increased — and RNA-seq methods like DESeq2 and edgeR, which are the reflexive choice for anyone arriving from transcriptomics, misfire on this data type.

"Solved" looks like: a committed script, a declared prevalence filter, at least two methods run on the identical filtered table, and a results file with one row per taxon *per method* so the agreement is inspectable rather than asserted.

## Recommended approach

One skill: the [Differential Abundance (bioSkills)](../../catalog/tools/differential-abundance.html) Claude skill. Install it per its catalog page (the `microbiome` category installer, or copy the single skill directory), then let it install the R packages for the methods you choose on first use.

1. **Assemble the inputs and decide the design first.** You need a feature table (BIOM or counts TSV), a taxonomy table, sample metadata, and — if you have one — a phylogeny. Write the design down before running anything: the grouping variable, any covariates (sequencing batch, age, BMI), and whether samples are repeated within subject. A longitudinal or covariate-adjusted design narrows the method panel immediately, because only the GLM-based methods take random effects.

2. **Declare the prevalence filter as a parameter, not a default.** The skill's stated range is 10–25% of samples; dropping rare features stabilizes multiple-testing correction, and the threshold changes the hit list. Fix one value, record it, and do not tune it after seeing results — a filter chosen to make a taxon significant is the cheapest form of p-hacking available here.

3. **Have Claude Code write the analysis to a script.** Review it before running:

   ```
   Using the bioSkills differential-abundance skill, write microbiome_da.R that:

   1. Builds a phyloseq object from the feature table, taxonomy, metadata and
      tree; aborts if any sample is present in one input and absent from another.
   2. Applies a prevalence filter at <YOUR VALUE>% of samples. Writes
      filtered_features.csv listing every feature retained and every feature
      dropped, with its prevalence. Both lists, not just the survivors.
   3. Runs at least TWO methods from the skill's panel on that identical filtered
      table -- ALDEx2 and ANCOM-BC2 as the default pair; add MaAsLin2 or LinDA
      instead if the design needs covariates or random effects.
   4. Emits da_by_method.csv: one row per (feature, method), with effect size,
      raw p, adjusted p, and the method's own diagnostic flag (ANCOM-BC2
      passed_ss, ALDEx2 effect). Do not average or pool across methods.
   5. Emits da_consensus.csv: one row per feature, with n_methods_significant,
      the method names that called it, and a tier -- high_confidence for the
      intersection of all methods run, exploratory for the union minus the
      intersection.
   6. Gates on an effect-size floor as well as BH/FDR; states both thresholds
      as literals in the script.
   7. Sets the RNG seed for ALDEx2 Monte-Carlo sampling and records mc.samples.
   8. Does NOT use DESeq2 or edgeR on this table, and refuses if asked.
   ```

4. **Read `da_consensus.csv` by tier and report it that way.** The intersection is what belongs in a results sentence. The union-minus-intersection is a follow-up list, and calling it that in the manuscript is both honest and defensible — a taxon that ALDEx2 calls and ANCOM-BC2 does not is a real observation about borderline evidence, not a failure to be resolved by picking the friendlier tool. If your headline finding sits only in the exploratory tier, that is the result.

5. **State the compositional limit explicitly in whatever you write.** Without a microbial-load anchor — qPCR of total 16S copies, flow-cytometric cell counts, or a spike-in — a significant change is a change in *proportion*. Write "relative abundance of X was higher" rather than "X increased", unless you measured load. This is a one-line discipline that survives peer review.

6. **Pin and record.** `renv::snapshot()` for the R environment; `provenance.json` capturing R and Bioconductor release, the version of each method package, the prevalence filter, the FDR and effect-size thresholds, the seed and `mc.samples`, the taxonomy reference database **and its release version** (SILVA 138 vs 138.1 relabels genera and will change your taxon names), a sha256 of the input feature table, and the model id that wrote the script.

Artifacts to commit: `microbiome_da.R`, `filtered_features.csv`, `da_by_method.csv`, `da_consensus.csv`, `renv.lock`, `provenance.json`. See [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) for the general pattern.

## Why this assembly

Rung 2, and it stops there. One skill covers the whole problem: it owns the method panel, the prevalence-filter guidance, the consensus reconciliation, and the compositional caveats. Plain Claude Code (rung 1) can call ALDEx2 and ANCOM-BC2 — the reason not to is that the *choices* are where this analysis fails, not the code. An agent writing from general knowledge will happily reach for DESeq2, report a single tool's list as the answer, and pick a prevalence filter silently. The skill states those three rules where the agent reads them, which is exactly the value of rung 2 over rung 1. No second component is needed and no autonomous system applies.

Scope note: this is the **amplicon** path. The skill deliberately routes whole-community diversity questions and shotgun-metagenomics differential abundance elsewhere; see Alternatives.

## Availability

Fully open. The bioSkills collection is MIT (root LICENSE confirmed on the catalog page's 2026-08-03 security review). phyloseq, ALDEx2, ANCOMBC, MaAsLin2/3, LinDA and ZicoSeq are open-source R/Bioconductor packages installed separately; LEfSe and QIIME 2's `q2-composition` are alternative front-ends if you already run QIIME.

Everything executes locally — the feature table, metadata and any clinical covariates stay on your machine, which matters for human-cohort microbiome studies under IRB restriction. Requires a working R installation with `BiocManager`. No API key, account, or subscription.

## Compute requirements

Laptop. A typical study — a few thousand ASVs across 50–200 samples, post-filter — runs the ALDEx2 plus ANCOM-BC2 pair in single-digit minutes within 8–16 GB RAM. Two knobs dominate the cost: ALDEx2's Monte-Carlo `mc.samples` (128 is the usual setting; raising it multiplies runtime linearly) and ZicoSeq's permutation count, which is the slowest option in the panel and the one to add last. Nothing here uses a GPU. If a run is taking tens of minutes on a table this size, the prevalence filter is probably not being applied.

## Evidence

**Proposed.** No documented run of Claude Code driving this skill on a real cohort with quantitative pass/fail is known. The design is grounded in the benchmark that motivates the consensus deliverable:

- **The core result.** Fourteen differential-abundance methods across 38 two-group 16S datasets "identified drastically different numbers and sets of significant ASVs", with results depending on pre-processing and, for many tools, the number of hits correlating with sample size, sequencing depth and effect size rather than biology. ALDEx2 and ANCOM-II were the most consistent across studies and agreed best with the intersection of approaches, and the authors' explicit recommendation is a **consensus approach based on multiple methods** ([Nearing et al., *Nature Communications* 2022](https://pubmed.ncbi.nlm.nih.gov/35039521/)). Steps 3–4 implement that recommendation, and the default ALDEx2 + ANCOM-BC2 pair follows its finding.
- **Independent re-validation is underway** rather than settled: a pre-registered synthetic-data study explicitly replicates the Nearing methodology against current method versions, following SPIRIT reporting ([Kohnert & Kreutz, *F1000Research* 2024/2025](https://pubmed.ncbi.nlm.nih.gov/39866725/)). Worth tracking — if it revises the ALDEx2/ANCOM ranking, the default pair in step 3 should change with it.
- **No benchmark** compares an agent-written consensus pipeline against a hand-written one. The agent's contribution is that the filter, the seed, the method set and the tiering are captured in a reviewable script rather than chosen ad hoc.

## Alternatives considered

**Ask a whole-community question instead.** If the question is whether communities differ overall rather than which taxon drives it, [Compute 16S microbiome alpha/beta diversity from a BIOM table](compute-16s-microbiome-diversity.html) is the right recipe and a cheaper answer — Shannon/UniFrac/PCoA/PERMANOVA, no per-taxon multiple-testing burden. In practice diversity runs first and this recipe runs second; they are complements, not substitutes.

**Shotgun rather than amplicon.** For metagenomic species or functional profiles, [Profile shotgun metagenome taxa with Kraken2](profile-shotgun-metagenome-taxa-with-kraken2.html) produces the table, but note that the Differential Abundance skill explicitly routes shotgun differential testing to the metagenomics category rather than answering it here. The compositional logic and the consensus discipline carry over; the specific method panel may not.

**A single method, reported as such.** Defensible in one situation: a pre-registered analysis plan that named the method before data collection. Then run that method, report it, and cite the Nearing result as a stated limitation. Choosing one method *after* seeing several is the case this recipe exists to prevent.

## See also

- [Differential Abundance (bioSkills)](../../catalog/tools/differential-abundance.html)
- [Amplicon Processing (bioSkills)](../../catalog/tools/amplicon-processing.html) — builds the ASV table this recipe consumes.
- [Taxonomy Assignment (bioSkills)](../../catalog/tools/taxonomy-assignment.html) — labels it, and owns the reference-database version you must record.
- [Compute 16S microbiome alpha/beta diversity from a BIOM table](compute-16s-microbiome-diversity.html) — the whole-community counterpart.
- [Profile shotgun metagenome taxa with Kraken2](profile-shotgun-metagenome-taxa-with-kraken2.html) — the shotgun profiling path.
- [Test which immune populations differ between groups in a cytometry cohort](test-cytometry-clusters-for-group-differences.html) — the same compositional trap in a different assay.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills) — skill collection, MIT; verified 2026-08-08 (this run) against the catalog page (`verification: works`, `last_verified: 2026-08-01`, security cleared 2026-08-03).
- [Nearing et al., *Nature Communications* 13:342 (2022) — Microbiome differential abundance methods produce different results across 38 datasets](https://pubmed.ncbi.nlm.nih.gov/35039521/) — published 2022; verified 2026-08-08 (this run).
- [Kohnert & Kreutz, *F1000Research* — Leveraging synthetic data to validate a benchmark study for differential abundance tests](https://pubmed.ncbi.nlm.nih.gov/39866725/) — published 2024, revised version 2; verified 2026-08-08 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=find-taxa-differing-between-microbiome-groups&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ffind-taxa-differing-between-microbiome-groups.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
