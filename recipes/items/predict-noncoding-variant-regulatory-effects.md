---
title: Predict the regulatory effect of a non-coding variant
parent: All recipes
grand_parent: Recipes
nav_order: 30
problem_class: Knowledge synthesis
subject_areas: [Molecular and Cellular Biology, Integrative Structural and Computational Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Subscription required
compute_requirements: Laptop
last_verified: 2026-07-25
summary: Use the DeepMind AlphaGenome skill to score how a single non-coding variant changes expression, chromatin accessibility, histone marks, splicing, and TF binding.
---

# Predict the regulatory effect of a non-coding variant

Hand Claude Code a single `chr:pos:ref>alt` variant and get back AlphaGenome's predicted effect on expression, chromatin accessibility, histone marks, splicing, and transcription-factor binding — with tissue-resolved tracks and an in-silico mutagenesis logo for the disrupted motif.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Molecular and Cellular Biology, Integrative Structural and Computational Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Subscription required |
| **Compute** | Laptop |

## Problem

A GWAS hit or a rare-disease exome lands on a variant that is nowhere near a coding region. ClinVar is silent, the variant is in an intron or an intergenic enhancer, and the question is mechanistic: does this base change touch a regulatory element, and if so, which gene, which tissue, and which molecular readout (expression up/down, a lost TF footprint, a cryptic splice site)? Wet-lab follow-up — a reporter assay, an eQTL look-up — is slow and not always available for the right cell type. A sequence-to-function model can generate the testable hypothesis in seconds. Solved looks like: a ranked summary of the variant's predicted molecular consequences across relevant tissues, the affected gene, and a sequence logo showing what regulatory motif the alt allele breaks or creates.

## Recommended approach

1. **Get an AlphaGenome API key.** Sign up at [deepmind.google.com/science/alphagenome](https://deepmind.google.com/science/alphagenome/), accept the non-commercial research terms, and copy the key. Install `uv` if you don't have it:

   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   echo "ALPHAGENOME_API_KEY=<your-key>" >> ~/.env
   ```

2. **Install the [AlphaGenome single-variant skill](../../catalog/tools/alphagenome.html)** from DeepMind's science-skills collection (manual copy is the Claude path):

   ```
   git clone https://github.com/google-deepmind/science-skills
   cp -r science-skills/skills/alphagenome_single_variant_analysis ~/.claude/skills/
   cp -r science-skills/skills/scienceskillscommon ~/.claude/skills/
   ```

3. **Resolve the tissue context first.** The model is tissue-resolved, so name the cell type that matters for your phenotype. Have Claude run the skill's `resolve_ontology_terms.py` to map "pancreatic beta cell" or "CD4 T cell" to its UBERON/CL ID before scoring.

4. **Score the variant.** A minimal prompt:

   ```
   Run the alphagenome_single_variant_analysis skill on
   chr11:5226774:T>A (GRCh38). Score RNA-seq expression, DNASE
   accessibility, ChIP histone marks, and TF binding in the
   relevant blood/erythroid cell types. Identify the affected
   gene, rank the modalities by effect size, run analyze_ism.py
   for the disrupted motif, and run interpret_splicing.py if any
   splice signal changes.
   ```

5. **Read the ranked output and the ISM logo.** The skill emits reference-vs-alternate tracks per modality, a splicing-disruption analysis, and an in-silico mutagenesis sequence logo. Treat the top-ranked modality as the lead hypothesis (e.g., "abolishes a GATA1 footprint → reduces enhancer accessibility → lowers target expression in erythroid cells") and confirm the gene assignment with the skill's offline GTF lookup before reporting.

## Why this assembly

Rung 2 of the simplicity ladder. The hard part — a 1 Mb sequence-to-function model spanning every regulatory modality — is the AlphaGenome API; the skill is the thin orchestration layer that resolves ontologies, calls the API, and renders tracks and ISM logos. Plain Claude Code (rung 1) cannot predict molecular phenotypes from sequence; it has no model. There is nothing to escalate to at rung 3/4 — this is a single-model query, and the model is state of the art for the task. The one judgment call the recipe adds is naming the right tissue, because cell-type-specific regulation is exactly where the model is weakest.

## Availability

Subscription required (free-tier, but gated). The AlphaGenome API is a signup-gated research preview, free for non-commercial use with an API key and acceptance of the terms — commercial use is not covered. The skill code itself is OSS (Apache-2.0 code, CC-BY-4.0 docs). Note: the skill's primary `npx skills add` install path targets Gemini/Antigravity; for Claude use the manual copy shown above.

## Compute requirements

Laptop-sufficient on the client side — all heavy computation runs server-side on the AlphaGenome API. A single-variant scoring call returns in roughly a second to a few seconds of model time; the skill installs its own Python deps via `uv` on first run. No local GPU. Network access to the API is required.

## Evidence

Reported. AlphaGenome is peer-reviewed: [Advancing regulatory variant effect prediction with AlphaGenome, *Nature* 2026](https://www.nature.com/articles/s41586-025-10014-0) reports that the model matches or exceeds the strongest available external models on 25 of 26 variant-effect-prediction evaluations, and on 22 of 24 single-sequence prediction tasks — while being the only model that jointly predicts all assessed modalities. The paper recapitulates the mechanisms of clinically relevant variants near the *TAL1* oncogene as a worked case. Experts note a caveat the recipe inherits: cell-type-specific regulation remains the model's weakest dimension, so tissue choice matters.

No peer-reviewed benchmark of "Claude + the AlphaGenome skill" specifically is known; the agent loop wraps the published API and adds ontology resolution and visualization, not a new model. The quantitative anchor is the Nature paper.

## Alternatives considered

- **[Interpret a clinical variant](interpret-clinical-variant.html).** Reach for that recipe when the variant is coding or already in ClinVar/gnomAD — it does database-anchored clinical interpretation. This AlphaGenome recipe is for the non-coding, regulatory, mechanism-unknown case where the databases are silent.
- **eQTL/regulatory database lookup (GTEx).** If your variant is a known eQTL in the tissue you care about, a [GTEx](../../catalog/tools/gtex-database.html) lookup is cheaper and observational rather than predicted. AlphaGenome wins when no eQTL exists for your variant or your cell type.
- **Plain Claude Code.** Cannot predict sequence-to-function effects; it would only summarize what databases already say. Not an option for novel non-coding variants.

## See also

- [AlphaGenome Single-Variant Analysis (Claude Skill)](../../catalog/tools/alphagenome.html)
- [Interpret a clinical variant](interpret-clinical-variant.html)
- [Score protein variants with ESM](score-protein-variants-with-esm.html)
- [GTEx (database)](../../catalog/tools/gtex-database.html)

## Sources

- [Advancing regulatory variant effect prediction with AlphaGenome, *Nature* 2026](https://www.nature.com/articles/s41586-025-10014-0) — published 2026-01-28; verified 2026-06-20 (this run).
- [AlphaGenome preprint, *bioRxiv* 2025](https://www.biorxiv.org/content/10.1101/2025.06.25.661532v1) — published 2025-06-25; verified 2026-06-20 (this run).
- [`google-deepmind/science-skills` (`alphagenome_single_variant_analysis`)](https://github.com/google-deepmind/science-skills/blob/main/skills/alphagenome_single_variant_analysis/SKILL.md) — verified 2026-06-20 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=predict-noncoding-variant-regulatory-effects&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fpredict-noncoding-variant-regulatory-effects.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
