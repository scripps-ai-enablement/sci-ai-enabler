---
title: Run a GWAS on case-control genotype data
parent: All recipes
grand_parent: Recipes
nav_order: 23
problem_class: Data analysis
subject_areas: [Translational Medicine, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-07-12
summary: Drive PLINK2 from QC through PCA-adjusted logistic-regression association on a case-control cohort, returning Manhattan-ready summary stats.
---

# Run a GWAS on case-control genotype data

Hand Claude a PLINK/VCF genotype set and a phenotype column; get back a QC'd, PCA-adjusted genome-wide association scan with Manhattan-ready summary statistics and a documented QC trail.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Translational Medicine, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation (laptop fine for &lt;10k samples) |

## Problem

A statistical geneticist who has genotyped a case-control cohort (custom array, imputed dosages, or sequencing-derived calls) faces the same checklist every time: filter low-call-rate samples and variants, drop SNPs failing Hardy-Weinberg equilibrium in controls, prune for linkage disequilibrium, derive principal components to correct for population stratification, then run the per-variant logistic regression with those PCs as covariates. The steps are individually standard and individually easy to get subtly wrong — the wrong HWE threshold, forgetting to compute PCs on an LD-pruned set, mixing case/control HWE filtering. "Solved" looks like: point Claude at the genotype files, get back a reproducible QC log, a covariate file of genotype PCs, and an association table ready to plot, with every threshold stated.

## Recommended approach

1. **Install the [PLINK2 skill](../../catalog/tools/plink2-gwas-analysis.html)** from the SciAgent-Skills collection (clone the repo, `/plugin install sciagent-skills`). The skill reads PLINK `.bed/.bim/.fam`, VCF, and BGEN, and exposes QC, IBD, PCA, and regression GWAS through local Python/Bash.

2. **Prompt with the cohort files, phenotype, and QC thresholds.** A worked version:

   ```
   Run a case-control GWAS on the PLINK fileset cohort.{bed,bim,fam}
   using the PLINK2 skill. Phenotype is in the .fam (1=control, 2=case).
   Assembly is GRCh38.

   Stage 1 — sample QC:
     - drop samples with call rate < 0.98 (--mind 0.02)
     - report and flag sex-check mismatches (--check-sex); do not auto-remove
     - flag heterozygosity outliers (>3 SD from the mean F)
   Stage 2 — variant QC:
     - --geno 0.02, --maf 0.01
     - --hwe 1e-6 applied in CONTROLS only
   Stage 3 — stratification:
     - LD-prune (--indep-pairwise 50 5 0.2) to an independent SNP set
     - compute 10 principal components on the pruned set (--pca 10)
   Stage 4 — association:
     - logistic regression (--glm) on the QC'd genotypes,
       covariates = first 10 PCs
     - output Manhattan-ready summary stats (CHR, POS, SNP, A1,
       OR, SE, P)

   Emit a QC log table (samples in/out, variants in/out per step) and
   the genomic inflation factor lambda_GC. Save the association table
   as gwas_results.tsv.
   ```

3. **Read off lambda_GC before trusting any hit.** A genomic inflation factor far above ~1.05 signals residual stratification or cryptic relatedness — re-prompt to add more PCs, tighten relatedness filtering (`--king-cutoff 0.0884` to remove up to second-degree relatives), or note that a mixed model is needed (see Alternatives).

4. **Plot and annotate the top loci.** Ask Claude to emit a Manhattan + QQ plot from `gwas_results.tsv`, then hand genome-wide-significant SNPs (P &lt; 5e-8) to the [GWAS Catalog skill](../../catalog/tools/gwas-database.html) to check whether each locus is already a known association for the trait.

## Why this assembly

Rung 2. A single skill (PLINK2) covers the entire QC → PCA → association arc; PLINK is the reference implementation these steps were defined against. Claude's value is orchestrating the multi-stage protocol correctly and keeping an auditable QC log, not replacing the engine. Claude Code alone (rung 1) cannot run PLINK and would hand-wave the genotype math. A rung-3 toolbelt adds nothing here — the GWAS Catalog lookup in step 4 is annotation, not analysis, and is optional. Escalate to rung 3/4 only for biobank-scale cohorts where a linear mixed model (regenie, SAIGE) is required to control inflation — and those tools are not yet catalogued (see Alternatives).

## Availability

Fully open. PLINK2 is GPL-3.0; the skill ships in the CC-BY-4.0 SciAgent-Skills collection. The GWAS Catalog REST API used for annotation is public and needs no auth. Genotype data itself is yours — no external upload; the skill runs locally, which matters for consented human-subjects data under your IRB/dbGaP data-use agreement.

## Compute requirements

Laptop-sufficient for cohorts up to ~10k samples × ~1M variants: PLINK2's bit-level parallelism runs QC and a `--glm` scan in minutes with a few GB of RAM. For larger imputed sets (10M+ variants, tens of thousands of samples) move to a workstation with 32–64 GB RAM; the `--pca` and `--glm` steps are the heavy ones. No GPU is used by PLINK itself — the front-matter tier reflects the upper end of in-scope cohorts. Biobank scale (100k+ samples) exceeds this recipe; see Alternatives.

## Evidence

Proposed. No published benchmark of an LLM-driven PLINK2 GWAS assembly is known. The closest grounding is the protocol literature this recipe encodes: PLINK's second-generation engine and its `--glm`/`--pca`/QC operators are documented in [Chang et al., *GigaScience* 4:7 (2015)](https://doi.org/10.1186/s13742-015-0047-8), and the exact QC-then-association staging (call rate, HWE-in-controls, LD pruning, PCA covariates, logistic-regression GWAS, lambda_GC check) follows the widely used tutorial of [Marees et al., *Int. J. Methods Psychiatr. Res.* 27:e1608 (2018)](https://doi.org/10.1002/mpr.1608). Both are standard references with thousands of citations; the assembly's individual steps are validated, the LLM-orchestrated composition is not independently benchmarked.

## Alternatives considered

- **Biobank-scale cohorts (rung 3/4).** With 100k+ samples or substantial relatedness/structure, fixed-effect logistic regression inflates; a linear mixed model (regenie, SAIGE, BOLT-LMM) is the standard. None is catalogued as a Claude component today, so this recipe stays at the array/small-cohort scale. Surfaced as a missing-component note for the catalog curator.
- **Claude Code alone (rung 1).** Insufficient — no live genotype-processing engine; the model would confabulate per-variant statistics.
- **The [GWAS Catalog skill](../../catalog/tools/gwas-database.html) alone.** That queries *published* SNP-trait associations; it interprets results, it does not compute them. Use it for step 4 annotation or when you only want prior-art lookups, not a fresh scan.

## See also

- [PLINK2 (Claude Skill)](../../catalog/tools/plink2-gwas-analysis.html)
- [GWAS Catalog (Claude Skill)](../../catalog/tools/gwas-database.html) — annotate genome-wide-significant loci against published associations.
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — drill into a single lead SNP after the scan.
- [Fit a survival model to censored clinical outcomes](fit-survival-model-to-clinical-outcomes.html) — the clinical-outcomes analysis sibling.

## Sources

- [Chang et al., *GigaScience* 4:7 (2015) — Second-generation PLINK](https://doi.org/10.1186/s13742-015-0047-8) — published 2015-02-25; verified 2026-06-14 (this run).
- [Marees et al., *Int. J. Methods Psychiatr. Res.* 27:e1608 (2018) — GWAS QC and statistical analysis tutorial](https://doi.org/10.1002/mpr.1608) — published 2018-02-27; verified 2026-06-14 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=run-gwas-on-case-control-genotypes&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Frun-gwas-on-case-control-genotypes.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
