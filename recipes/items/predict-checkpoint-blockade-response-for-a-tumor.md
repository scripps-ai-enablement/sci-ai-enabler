---
title: Predict checkpoint-blockade response for a tumor from its biomarker profile
parent: All recipes
grand_parent: Recipes
nav_order: 20
problem_class: Knowledge synthesis
subject_areas: [Immunology and Microbiology, Translational Medicine, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Institutional access
compute_requirements: Laptop
last_verified: 2026-08-01
summary: Use the ToolUniverse Immunotherapy Response Prediction skill to integrate TMB, MSI, PD-L1, HLA, and immune expression into an evidence-graded ICI response score.
---

# Predict checkpoint-blockade response for a tumor from its biomarker profile

Turn a tumor's molecular profile into an evidence-graded immune-checkpoint-inhibitor response assessment that names *which* biomarker is driving the call, so the axes disagree in the open rather than being averaged away.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Immunology and Microbiology, Translational Medicine, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Institutional access |
| **Compute** | Laptop |

## Problem

You have a tumor molecular profile — a TMB value from a panel or exome, MMR/MSI status, a PD-L1 IHC score, HLA genotype, and ideally bulk tumor RNA — and someone needs to know whether checkpoint blockade is worth pursuing, for a molecular tumor board, a trial-eligibility screen, or a retrospective cohort stratification. The single-biomarker answer is the trap. TMB-high and MSI-high both carry tumor-agnostic approvals, yet response within those groups is strikingly heterogeneous, and each biomarker fails differently: TMB reports neoantigen supply and says nothing about whether T cells are in the tumor, while a T-cell-inflamed expression signature reports the reverse and is nearly uncorrelated with TMB. Resistance genotypes (B2M loss, JAK1/JAK2 loss-of-function) can void a favorable score entirely.

What "solved" looks like is not a single number. It is a per-sample record that carries each biomarker axis separately with its cancer-type-specific threshold, names the resistance features found, grades how strong the clinical evidence is for that biomarker in *this* tumor type, and flags disagreement between axes as disagreement — plus enough provenance that the call can be re-derived when the underlying knowledgebases have moved on.

## Recommended approach

1. **Install the [ToolUniverse MCP server](../../catalog/tools/tooluniverse.html), then the [Immunotherapy Response Prediction skill](../../catalog/tools/tooluniverse-immunotherapy-response-prediction.html).** The skill is a reasoning layer over ToolUniverse tool calls, so the server must be registered first or every lookup fails. Follow the install paths on those pages. The skill ships `disable-model-invocation: true`, so you must ask for it by name.

2. **Assemble the inputs as a table, not as prose.** One row per sample, with the columns the skill actually consumes: cancer type (as a specific diagnosis, not "carcinoma"), TMB in mutations/Mb *with the assay it came from*, MMR/MSI status and method, PD-L1 score with the antibody clone and scoring convention (TPS vs CPS vs IC — they are not interchangeable), HLA class I genotype, and any somatic variants in `B2M`, `JAK1`, `JAK2`, `STK11`, `KEAP1`, `PTEN`, `CD274`. Commit this as `ici_inputs.csv`. Missing fields are fine and should stay blank — the skill grades evidence per axis, and a blank is more honest than an imputed value.

3. **Capture the workflow as a reusable command, not a one-off chat.** Write `.claude/commands/ici-response.md` so the same phrasing runs over every sample:

   ```
   Use the tooluniverse-immunotherapy-response-prediction skill on each
   row of ici_inputs.csv. For every sample:
     1. Classify TMB against the threshold for that specific cancer
        type, and record the threshold used and its source.
     2. Assess MMR/MSI and PD-L1 with the scoring convention named
        in the input; do not convert between TPS/CPS/IC.
     3. Evaluate the listed mutations as sensitizing or resistance
        features, citing the CIViC/FDA evidence behind each call.
     4. Profile the immune microenvironment from the expression
        table if one is supplied; otherwise mark that axis absent.
     5. Emit the 0-100 integrated score AND the per-axis component
        scores with their T1-T4 evidence grades - never the
        integrated score alone.
     6. Flag any sample where two axes disagree in direction.
   Append one row per sample to ici_biomarkers.csv with columns for
   each axis, its evidence grade, and the reason string. Write the
   narrative report to reports/<sample_id>.md, citing only values
   present in ici_biomarkers.csv.
   ```

4. **Record provenance, because none of this is byte-reproducible.** The skill queries live knowledgebases (CIViC, Open Targets, FDA labels, Human Protein Atlas, ClinicalTrials.gov, PubMed) whose contents change weekly. Have the run emit `provenance.json` capturing the ToolUniverse version, the skill's commit SHA, the UTC date of the query, the release date or accession of each knowledgebase consulted, the sha256 of `ici_inputs.csv`, and the model id. Commit `ici_inputs.csv`, the command file, `ici_biomarkers.csv`, `reports/`, and `provenance.json` together.

5. **Read the disagreements first.** The rows worth a human's time are the ones where axes conflict — TMB-high with a cold microenvironment, or PD-L1-positive with `B2M` loss. Treat the integrated 0–100 score as an index into the per-axis table, not as the answer. This output is a research aid; it is not a clinical decision tool and must not be used as one without independent review.

## Why this assembly

Rung 2, and it stops there. Plain Claude Code (rung 1) can look up a TMB threshold, but the work here is not lookup — it is applying *cancer-type-specific* thresholds, keeping the axes separate, and attaching evidence grades from the right knowledgebase to each call. That's a long, ordered protocol with many chances to quietly substitute a pan-cancer threshold for a tumor-specific one, which is exactly the error the skill's eleven-phase structure exists to prevent. One skill plus its MCP server covers every lookup the protocol needs — Open Targets, CIViC, FDA pharmacogenomics, HPA, IEDB, Enrichr, trials, PubMed — so a multi-tool harness would only re-implement what the skill already routes.

## Availability

Institutional access. The software is free: ToolUniverse and its skills are Apache-2.0, and every knowledgebase behind them is public. The gate is the data. Patient TMB, MSI, PD-L1, HLA, and expression values are clinical molecular-profiling results and sit inside your IRB, consent, and data-governance regime — and the MCP server sends query terms to external APIs, so confirm with your governance office what may leave the institution before running this on identifiable samples. De-identified cohort-level runs (TCGA, IMvigor210) have no such constraint and are `Fully open` in practice.

## Compute requirements

Laptop. Every step is an API call; there is no local model and no heavy computation. Wall-clock is dominated by the number of knowledgebase round-trips the skill's eleven phases make — expect a few minutes per sample, so a 200-sample cohort is an overnight batch rather than an interactive session, and you should rate-limit and checkpoint `ici_biomarkers.csv` incrementally so a mid-run failure doesn't cost the whole cohort.

## Evidence

Proposed. **No documented attempt of this exact assembly — the ToolUniverse skill driving a checkpoint-response assessment — is known**, and the skill's integrated 0–100 score has not been benchmarked against clinical outcomes by anyone. Treat the score as a structured summary of published biomarker logic, not as a validated predictor.

The individual axes it composes are well validated. The T-cell-inflamed gene expression profile was developed across 220 pembrolizumab-treated patients in 9 cancers and independently confirmed against PD-L1 IHC in 96 head-and-neck patients ([Ayers et al., *JCI* 2017](https://pubmed.ncbi.nlm.nih.gov/28650338/)). The central design choice of this recipe — keep the axes separate — comes from the pan-tumor analysis of >300 samples across 22 tumor types and four KEYNOTE trials showing TMB and the T-cell-inflamed GEP are **independently predictive and only weakly correlated**, capturing distinct neoantigenicity and T-cell-activation biology, with joint stratification revealing resistance patterns neither axis sees alone ([Cristescu et al., *Science* 2018](https://pubmed.ncbi.nlm.nih.gov/30309915/)).

Two findings justify the caution built into steps 2 and 5. In 5,621 metastatic breast cancers, TMB-high alone did **not** correlate with immune infiltrate or immune-response gene signatures; only concurrent PD-L1-positivity or dMMR/MSI-high identified T-cell-inflamed tumors, and `B2M` mutation and `CD274` amplification carried additional signal ([Sammons et al., *Front. Oncol.* 2023](https://pubmed.ncbi.nlm.nih.gov/37637072/)). Within dMMR/MSI-high tumors — a group with tumor-agnostic approval — response remains heterogeneous, and a 20-gene immune signature separated true responders at 55.6% vs 32.8% response in IMvigor210 ([Kim et al., *Cancers* 2025](https://pubmed.ncbi.nlm.nih.gov/41514531/)). A single-biomarker call, and an integrated score that hides which axis moved it, both fail on exactly these cases.

## Alternatives considered

- **[Annotate tumor somatic variants with clinical actionability evidence](annotate-tumor-variants-with-clinical-actionability.html) (rung 2, narrower).** Reach for that when the question is "what therapy does this variant match?" across all drug classes. It reads the same somatic VCF but answers a targeted-therapy question; it does not assemble the immune-axis biomarkers.
- **Compute the signatures yourself from the expression matrix (rung 1).** If you already have a bulk RNA matrix and want the T-cell-inflamed GEP or an MCP-counter deconvolution as *numbers* for a cohort analysis, score them directly with the [functional enrichment](run-functional-enrichment-on-a-gene-list.html) or [TF/pathway activity](infer-tf-and-pathway-activities-from-expression.html) paths. That is cheaper and fully reproducible. This recipe is for the case where you also need the clinical-evidence grading and resistance-genotype review attached.
- **A trained multimodal ICI-response model.** Nothing Claude-installable exists today; if you need a calibrated probability rather than a graded assessment, you are building it yourself from cohort data.

## See also

- [Immunotherapy Response Prediction (ToolUniverse Claude Skill)](../../catalog/tools/tooluniverse-immunotherapy-response-prediction.html) — the skill this recipe drives.
- [ToolUniverse](../../catalog/tools/tooluniverse.html) — the MCP server it requires.
- [Prioritize tumor neoantigens for a personalized cancer vaccine](prioritize-tumor-neoantigens-for-a-vaccine.html) — the neoantigen-supply axis, computed rather than summarized.
- [Annotate tumor somatic variants with clinical actionability evidence](annotate-tumor-variants-with-clinical-actionability.html) — the targeted-therapy read of the same profile.
- [Annotate TCR antigen specificity by clustering and database lookup](annotate-tcr-specificity-by-clustering.html) — the on-treatment T-cell readout.

## Sources

- [Cristescu et al., "Pan-tumor genomic biomarkers for PD-1 checkpoint blockade-based immunotherapy," *Science*](https://pubmed.ncbi.nlm.nih.gov/30309915/) — TMB and T-cell-inflamed GEP independently predictive, weakly correlated; >300 samples, 22 tumor types; published 2018; verified 2026-08-01 (this run).
- [Ayers et al., "IFN-γ-related mRNA profile predicts clinical response to PD-1 blockade," *JCI*](https://pubmed.ncbi.nlm.nih.gov/28650338/) — T-cell-inflamed GEP development and independent confirmation; published 2017; verified 2026-08-01 (this run).
- [Sammons et al., "Concurrent predictors of an immune responsive tumor microenvironment within tumor mutational burden-high breast cancer," *Front. Oncol.*](https://pubmed.ncbi.nlm.nih.gov/37637072/) — 5,621 samples; TMB-H alone insufficient; B2M and CD274 signal; published 2023; verified 2026-08-01 (this run).
- [Kim et al., "Finding the True Responders: Stratifying dMMR/MSI-H Tumors for ICI Response," *Cancers*](https://pubmed.ncbi.nlm.nih.gov/41514531/) — response heterogeneity within dMMR/MSI-H; 20-gene signature, 55.6% vs 32.8% in IMvigor210; published 2025; verified 2026-08-01 (this run).
- [`mims-harvard/ToolUniverse` — immunotherapy-response-prediction SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-immunotherapy-response-prediction/SKILL.md) — eleven-phase protocol, T1–T4 evidence grading; catalog page `last_verified` 2026-07-12.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=predict-checkpoint-blockade-response-for-a-tumor&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fpredict-checkpoint-blockade-response-for-a-tumor.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
