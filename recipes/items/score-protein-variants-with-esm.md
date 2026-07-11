---
title: Score point mutations for functional impact with a protein language model
parent: All recipes
grand_parent: Recipes
nav_order: 31
problem_class: Data analysis
subject_areas: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-07-11
summary: Use the ESM skill to compute zero-shot masked-marginal log-likelihood-ratio scores for a list of point mutations, ranking them by predicted functional effect without any labelled data.
---

# Score point mutations for functional impact with a protein language model

Hand Claude a wild-type protein sequence and a list of substitutions; get back a ranked table of zero-shot fitness scores — the masked-marginal log-likelihood ratio each mutation receives from a protein language model — with no deep-mutational-scanning data and no task-specific training.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Integrative Structural and Computational Biology, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

You have a protein and a set of single-residue substitutions — clinical VUS to triage, an enzyme you want to engineer, a panel of designed mutants to pre-screen before ordering DNA. You want a defensible, data-free ranking of which mutations are likely tolerated and which are likely deleterious, before committing wet-lab budget. Supervised predictors need labelled deep-mutational-scanning (DMS) data you don't have for this protein. A protein language model trained only on natural sequences solves this zero-shot: the log-probability it assigns to the mutant residue relative to the wild-type residue is a strong proxy for evolutionary tolerance, and the masked-marginal version of that score is the field-standard heuristic. Solved looks like: paste a FASTA sequence and a list like `A123G, R45K, ...`, get a CSV ranked by score with a plain-language tolerated/deleterious call per mutation.

## Recommended approach

1. **Install the [ESM skill](../../catalog/tools/esm.html)** (K-Dense `scientific-agent-skills`):

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   ```

   Enable the `esm` skill when prompted. For the input-fetch step (optional) also enable the [gget skill](../../catalog/tools/gget.html) so Claude can pull the canonical UniProt sequence by accession instead of you pasting it.

2. **Provide the sequence and the mutation list.** If you only have an accession, ask Claude to fetch the canonical sequence first (`gget` → UniProt), then confirm the residue numbering matches your mutation list (1-indexed, position 1 = the first residue of the canonical isoform).

3. **Prompt for masked-marginal scoring.** A minimal version:

   ```
   Use the esm skill to score these point mutations on the protein
   below with the masked-marginal log-likelihood-ratio scheme
   (Meier et al. 2021), using ESM C (or ESM-2 if available locally).

   For each mutation pos/wt/mut:
   1. Run a forward pass with that position MASKED.
   2. Read the per-position log-probabilities (logits -> log-softmax)
      over the 20 amino acids at the masked position.
   3. Score = log P(mut) - log P(wt) at that position.
   4. A more-negative score = more likely deleterious; near-zero or
      positive = likely tolerated.

   WT sequence (FASTA):
   >my_protein
   MK...   <paste full canonical sequence>

   Mutations: A123G, R45K, D88N, ...

   Return a CSV sorted ascending by score with columns:
   mutation, position, wt, mut, score, call
   where call = "deleterious" if score < -<threshold> else "tolerated".
   Pick the threshold from the score distribution (e.g. the 25th
   percentile) and state the value you used.
   ```

4. **Use the score distribution, not an absolute cutoff.** Zero-shot scores are relative within one protein; calibrate the tolerated/deleterious split from the spread of your own mutation set (or anchor it on a few known-benign and known-pathogenic mutations if you have them). State the threshold explicitly.

5. **For deep scans, switch to wt-marginal.** If you are scanning every position to all 20 amino acids (a full single-mutation landscape), ask for the wt-marginal scheme instead — one forward pass on the unmasked sequence scores the whole landscape, at a small accuracy cost versus per-position masking.

## Why this assembly

Rung 2. One skill (ESM, optionally a second read-only skill for the sequence fetch) computes the whole ranking; the masked-marginal score is a single model forward pass per mutation. Claude Code alone (rung 1) cannot do this — it has no protein-language-model weights and will confabulate scores. A rung-3 toolbelt or a rung-4 autonomous system buys nothing for a one-shot scoring table. The escalation that *would* justify rung 3 is closing a design-build-test-learn loop (score → synthesize → assay → retrain a fitness head on the results); for a standalone zero-shot ranking, the single skill is enough.

## Availability

Fully open. The ESM and gget skills are MIT-licensed OSS. ESM open weights are downloaded from EvolutionaryScale / Hugging Face under their model license (free for research; check the EvolutionaryScale Community License for ESM3/ESM C terms before commercial use). UniProt sequences are public. The cloud Forge/Biohub API path requires a free `ESM_API_KEY`; the local-weights path needs no account.

## Compute requirements

GPU workstation recommended. Running ESM C or ESM-2 (650M) locally for masked-marginal scoring is comfortable on a single GPU with ~8–16 GB VRAM; each masked forward pass is sub-second for a typical <500-residue protein, so a list of dozens of mutations finishes in well under a minute. Scoring a full single-mutation landscape (sequence length × 19) is heavier — prefer the wt-marginal one-pass scheme there, or batch on the GPU. CPU-only is possible for small proteins and short lists but slow. The largest models (ESM-2 3B/15B) want ≥24 GB VRAM; the Forge API offloads compute entirely if local GPU is unavailable.

## Evidence

Proposed. No documented attempt of this exact K-Dense `esm`-skill-driven scoring assembly is known. The underlying method is well-validated at the component level: **Meier et al. (NeurIPS 2021)** introduced ESM-1v and showed zero-shot masked-marginal log-likelihood-ratio scoring matches or beats supervised state-of-the-art on variant-effect prediction with a single forward pass, no labelled data ([bioRxiv 2021.07.09.450648](https://www.biorxiv.org/content/10.1101/2021.07.09.450648v1.full)). The masked-marginal heuristic is the canonical zero-shot scorer in the **ProteinGym** benchmark across hundreds of DMS assays ([Notin et al., *NeurIPS* 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10723403/)). The scheme is in active 2025 use: **Zhang et al. (*Nat. Commun.* 2025)** seed an automated biofoundry directed-evolution loop with ESM-2 zero-shot predictions of 96 variants, reaching up to 2.4-fold activity gains in four rounds over 10 days ([doi:10.1038/s41467-025-56751-8](https://doi.org/10.1038/s41467-025-56751-8)), and **ESM-Scan** packages the same scoring to guide amino-acid substitutions ([bioRxiv 2023.12.12.571273](https://www.biorxiv.org/content/10.1101/2023.12.12.571273v1.full)). What is not independently benchmarked is the convenience layer — Claude driving the K-Dense skill to assemble the ranked CSV.

## Alternatives considered

- **[Interpret a clinical variant](interpret-clinical-variant.html) (BioMCP, rung 2).** Reach for that instead when the variant is already catalogued — it reads ClinVar significance, gnomAD frequency, and curated predictor calls directly. The ESM recipe is the complement: it scores *novel or uncharacterized* substitutions that have no database entry, which is exactly where database lookups return nothing.
- **Supervised DMS models.** If you already have a deep-mutational-scanning dataset for this protein, a supervised model trained on it will beat zero-shot. Use zero-shot when you have no labels — its whole point is needing none.
- **Structure-aware scoring (e.g. graph + PLM ensembles).** Recent work shows combining ESM embeddings with structure graphs improves generalization to highly diverged sequences ([Ash et al., *bioRxiv* 2025](https://doi.org/10.1101/2025.11.04.686550)). That is a rung-3 toolbelt (needs a structure source plus a custom model) — escalate only if pure-sequence scores generalize poorly on your protein family.

## See also

- [ESM (Claude Skill)](../../catalog/tools/esm.html)
- [gget (Claude Skill)](../../catalog/tools/gget.html) — fetches the canonical UniProt sequence for the input step.
- [Triage an AlphaFold model for structure-based drug design](triage-alphafold-model-for-docking.html) — the structure-confidence counterpart for the same protein.
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — database-driven sibling for already-catalogued variants.

## Sources

- [Meier et al., "Language models enable zero-shot prediction of the effects of mutations on protein function" (*bioRxiv* / NeurIPS 2021)](https://www.biorxiv.org/content/10.1101/2021.07.09.450648v1.full) — published 2021-07-09; verified 2026-06-10 (this run).
- [Notin et al., "ProteinGym: Large-Scale Benchmarks for Protein Design and Fitness Prediction" (*NeurIPS* 2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10723403/) — masked-marginal as standard zero-shot scorer; verified 2026-06-10 (this run).
- [Zhang et al., "Integrating protein language models and automatic biofoundry for enhanced protein evolution" (*Nat. Commun.* 2025)](https://doi.org/10.1038/s41467-025-56751-8) — published 2025; ESM-2 zero-shot seeding a directed-evolution loop.
- [`K-Dense-AI/scientific-agent-skills` — `esm` SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/esm/SKILL.md) — exposes `model.logits(...)` for per-position log-probabilities; verified 2026-06-10 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=score-protein-variants-with-esm&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fscore-protein-variants-with-esm.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
