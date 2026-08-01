---
title: Prioritize tumor neoantigens for a personalized cancer vaccine
parent: All recipes
grand_parent: Recipes
nav_order: 20
problem_class: Experimental design
subject_areas: [Immunology and Microbiology, Translational Medicine, Drug Repurposing and Discovery]
evidence_level: Validated
complexity: One skill or MCP
availability: Institutional access
compute_requirements: Workstation with GPU
last_verified: 2026-08-01
summary: Use the Neoantigen Prediction skill to turn a patient's somatic variants, HLA type, and tumor RNA into a filtered, tiered neoantigen shortlist for vaccine design.
---

# Prioritize tumor neoantigens for a personalized cancer vaccine

Hand Claude Code a patient's somatic VCF, HLA genotype, and tumor expression, and get back a tiered neoantigen candidate table that has already survived the filters that kill most predictions — clonality, expression, HLA loss-of-heterozygosity, and wild-type similarity — as a committed, re-runnable pipeline rather than a spreadsheet of raw binders.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Immunology and Microbiology, Translational Medicine, Drug Repurposing and Discovery |
| **Evidence level** | Validated |
| **Complexity** | One skill or MCP |
| **Availability** | Institutional access |
| **Compute** | Workstation with GPU |

## Problem

You have tumor/normal exome (or genome) sequencing plus tumor RNA-seq for a patient, and you need to nominate the handful of mutant peptides that go into a personalized vaccine construct or a neoantigen-reactive T-cell screen. Binding prediction alone gives you hundreds to thousands of "strong binders", and the overwhelming majority are dead ends: the mutation is subclonal and present in a minority of tumor cells, the transcript isn't expressed, the restricting HLA allele has been lost in the tumor, or the mutant peptide is indistinguishable from its wild-type counterpart and the T-cell repertoire is tolerant to it.

The failure mode that matters clinically is silent. A confidently-predicted strong binder restricted to an HLA allele the tumor has deleted will never be presented, and nothing in the binding score tells you that. "Solved" looks like: a `neoantigens.tsv` where every surviving candidate carries its variant allele frequency, cancer cell fraction, transcript-level expression, mutant-versus-wild-type binding gap, reference-proteome similarity, and the HLA-LOH status of its restricting allele — plus a tier assignment and a provenance record naming every algorithm version and reference release, because this table has to be defensible to a trial review board months later.

## Recommended approach

1. **Install the [Neoantigen Prediction skill](../../catalog/tools/neoantigen-prediction.html).** Clone the bioSkills repo and copy the one skill (`cp -r bioSkills/immunoinformatics/neoantigen-prediction ~/.claude/skills/`), following the catalog page. The skill declares its external dependencies — pVACtools, Ensembl VEP (with the Wildtype and Frameshift plugins), an HLA typer, and LOHHLA — and prompts you to install them on first use. Budget disk for the VEP cache.

2. **Fix your inputs before predicting.** You need: a somatic VCF (SNVs + indels) annotated with VEP including the Wildtype/Frameshift plugins; a four-digit HLA class I (and class II, if you want CD4 help) genotype from the *normal* sample; a transcript-level expression table from tumor RNA-seq; and — if you have tumor and normal BAMs — the LOHHLA inputs. Missing expression or missing HLA-LOH data is not fatal, but record its absence: it changes how much the shortlist can be trusted.

3. **Have the skill write a committed pipeline, not a chat answer.** A prompt:

   ```
   Use the neoantigen-prediction skill to write me a pipeline
   run_neoantigens.sh plus a filter_candidates.py that:
     1. Runs pVACseq on somatic.vep.vcf for the alleles in
        hla_class_i.txt over 8-11mers, with an ensemble of the
        installed class I predictors, emitting both binding
        affinity and presentation/percentile scores.
     2. Runs pVACfuse on the fusion calls if arriba/STAR-Fusion
        output is present; skip cleanly if not.
     3. Joins each candidate to: tumor DNA VAF, cancer cell
        fraction (clonal vs subclonal), transcript TPM, and the
        matched wild-type peptide's score.
     4. Adds LOHHLA status per restricting allele and drops
        candidates restricted to a lost allele into a separate
        rejected_loh.tsv rather than deleting them.
     5. Computes agretopicity (MT/WT score ratio) and flags
        candidates whose mutant peptide matches the reference
        proteome.
     6. Writes neoantigens.tsv with a tier column and the reason
        string for every exclusion, and provenance.json:
        pVACtools version, each predictor's version, VEP version
        and cache release, reference genome build, LOHHLA
        version, input VCF/expression sha256s, run date, model id.
   Commit the scripts and provenance.json. Do not paste the
   candidate peptides back as prose.
   ```

   Pin the environment (a `requirements.txt` or the pVACtools container digest) and commit `run_neoantigens.sh`, `filter_candidates.py`, `neoantigens.tsv`, `rejected_loh.tsv`, and `provenance.json` alongside the input manifests.

4. **Review the tiers by hand — this step is not automatable yet.** Load `neoantigens.tsv` into `pvacview` and walk the top tier variant-by-variant, checking read support in IGV for anything headed into a construct. Published protocols treat this two-stage review (algorithmic tiering, then manual variant assessment) as mandatory, and the automation of it is an active research problem rather than a solved one.

5. **Hand off with the exclusions attached.** Ship the shortlist to peptide synthesis or construct design together with `rejected_loh.tsv` and `provenance.json`, so a reviewer can see what was dropped and why. Because every algorithm version and reference release is pinned, re-running the pipeline months later reproduces the same tiering — which is what makes the selection auditable when the trial reports out.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill drives the whole chain. Plain Claude Code (rung 1) could install pVACtools and run `pvacseq run`, and would produce a long list of strong binders that looks finished and isn't: the value here is the *filters*, and the skill is built around the position that binding prediction is the easy part. It encodes HLA-LOH, cancer cell fraction, expression, and agretopicity as first-class steps rather than optional extras, which is exactly what separates a candidate list from a shortlist. Rung 3+ is unnecessary: this is one well-bounded pipeline with one decision point (the manual review), not a multi-tool search.

## Availability

Institutional access. pVACtools itself is open source, but the assembly has real gates: the IEDB standalone prediction tools bundled by pVACtools are free for academic/non-commercial use only, VEP requires a large cache download, and several class I predictors (NetMHCpan, MixMHCpred) need separate academic registration. More importantly, the inputs are patient tumor/normal sequencing — this recipe sits inside whatever IRB, consent, and data-governance regime covers that data, and the run should stay on institution-controlled compute. Verify the IEDB tool licensing before any commercial use.

## Compute requirements

Server- or workstation-class, no GPU. The prediction step is CPU-bound: an exome-scale somatic VCF (a few hundred coding variants) against six HLA alleles with a multi-algorithm ensemble runs in tens of minutes to a few hours on 8–16 cores. The heavy resources are storage and RAM, not FLOPs — the VEP cache is tens of GB, and LOHHLA works from tumor and normal BAMs, so plan for the alignment files as well. A hypermutated tumor (MSI-high, POLE-mutant) multiplies the candidate count by an order of magnitude and is the case that pushes the run onto a cluster.

## Evidence

Validated. pVACtools is the field's most widely used neoantigen toolkit and is validated in clinical use, not just on benchmarks. The **ImmunoNX** protocol built on pVACtools has supported **over 185 patients across 11 clinical trials**, and its published demonstration on the HCC1395 breast-cancer dataset narrowed **322 initial predictions to 78 high-confidence candidates**, with vaccine design completed in under three months ([Singhal et al. 2025](https://pubmed.ncbi.nlm.nih.gov/41415611/)). A phase 1 neoantigen DNA vaccine trial in triple-negative breast cancer used pVACtools to select and prioritize the encoded neoantigens (mean 11 per patient, range 4–20): **14 of 18 patients** developed neoantigen-specific T-cell responses by ELISpot and flow cytometry, with 87.5% recurrence-free survival at 36 months median follow-up ([Zhang et al., *Genome Medicine* 2024](https://pubmed.ncbi.nlm.nih.gov/39538331/)). The toolkit itself is described in [Hundal et al., *Cancer Immunol. Res.* 2020](https://pubmed.ncbi.nlm.nih.gov/31907209/), and the current v6 release adds presentation scoring, immunogenicity prediction, anchor-residue analysis, reference-proteome similarity, and `pVACsplice` ([Hoang et al. 2026](https://pubmed.ncbi.nlm.nih.gov/42396206/)).

The manual-review step in step 4 is a known bottleneck rather than a curator's caution: a machine-learning triage model (NEAT), trained on 1,943 peptides from 33 patients across 3 trials, reaches sensitivity 0.847 / specificity 0.924 / AUC 0.955 and is being folded into pVACtools v7 precisely because expert manual review currently limits scalability ([Yao et al. 2026](https://pubmed.ncbi.nlm.nih.gov/42428096/)). No head-to-head benchmark of the *agent-driven skill* versus a hand-run pVACtools invocation exists; the skill buys correct filter ordering and a pinned provenance record, not a new prediction method.

## Alternatives considered

- **[Scan a protein for candidate CD8 T-cell epitopes](scan-protein-for-cd8-t-cell-epitopes.html) (rung 2, simpler).** Reach for that when you have a protein sequence and an allele list and just want peptides ranked by predicted presentation — a pathogen antigen, or a single known driver mutation. It is the right call when there is no matched normal, no expression data, and no clonality question. This recipe exists because a *patient vaccine* selection needs the tumor-context filters that a sequence-only scan cannot apply.
- **pVACtools by hand, no agent (rung 0).** Entirely reasonable for a lab that runs this weekly and already has a WDL/Nextflow harness — [ImmunoNX](https://pubmed.ncbi.nlm.nih.gov/41415611/) is exactly that, and if you have it, use it. The agent path suits groups doing this occasionally, where the risk is a forgotten filter rather than throughput.
- **Waiting for automated triage.** If your bottleneck is the manual review in step 4, watch for the NEAT model shipping in pVACtools v7; until your installed version includes it, do not skip the review.

## See also

- [Neoantigen Prediction (bioSkills)](../../catalog/tools/neoantigen-prediction.html) — the skill this recipe drives.
- [Scan a protein for candidate CD8 T-cell epitopes](scan-protein-for-cd8-t-cell-epitopes.html) — the sequence-only, tumor-context-free sibling.
- [Scan a protein for candidate CD4 T-cell (helper) epitopes](scan-protein-for-cd4-t-cell-epitopes.html) — class II candidates for the same construct.
- [Annotate tumor somatic variants with clinical actionability evidence](annotate-tumor-variants-with-clinical-actionability.html) — the therapy-matching read of the same somatic VCF.
- [Predict checkpoint-blockade response for a tumor from its biomarker profile](predict-checkpoint-blockade-response-for-a-tumor.html) — the ICI-eligibility read, where TMB summarizes the neoantigen supply this recipe enumerates.
- [Annotate TCR antigen specificity by clustering and database lookup](annotate-tcr-specificity-by-clustering.html) — the post-vaccination readout, when you sequence the responding T cells.

## Sources

- [Singhal et al., "ImmunoNX: a robust bioinformatics workflow to support personalized neoantigen vaccine trials"](https://pubmed.ncbi.nlm.nih.gov/41415611/) — 185+ patients across 11 trials; 322 → 78 candidates on HCC1395; published 2025; verified 2026-08-01 (this run).
- [Zhang et al., "Neoantigen DNA vaccines are safe, feasible, and induce neoantigen-specific immune responses in triple-negative breast cancer patients," *Genome Medicine*](https://pubmed.ncbi.nlm.nih.gov/39538331/) — pVACtools-selected neoantigens; 14/18 responders; published 2024; verified 2026-08-01 (this run).
- [Hundal et al., "pVACtools: A Computational Toolkit to Identify and Visualize Cancer Neoantigens," *Cancer Immunol. Res.*](https://pubmed.ncbi.nlm.nih.gov/31907209/) — the toolkit; published 2020; verified 2026-08-01 (this run).
- [Hoang et al., "pVACtools v6: A comprehensive suite for neoantigen prediction, visualization, and therapy design"](https://pubmed.ncbi.nlm.nih.gov/42396206/) — presentation scoring, anchor analysis, pVACsplice; published 2026; verified 2026-08-01 (this run).
- [Yao et al., "Automating neoantigen selection for personalized cancer vaccine design"](https://pubmed.ncbi.nlm.nih.gov/42428096/) — NEAT triage model, AUC 0.955, headed for pVACtools v7; published 2026; verified 2026-08-01 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=prioritize-tumor-neoantigens-for-a-vaccine&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fprioritize-tumor-neoantigens-for-a-vaccine.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
