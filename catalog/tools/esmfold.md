---
title: ESMFold (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Meta AI / EvolutionaryScale
availability: GA
tool_categories: [Molecular and Cellular Biology, Integrative Structural and Computational Biology]
last_verified: 2026-07-17
claude_science: true
summary: ESMFold single-sequence protein structure prediction (no MSA), run locally or via the ESM Atlas API; a Claude Science skill.
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "featured Claude Science skill and facebookresearch/esm MIT resolves, but the self-host upstream repo is archived (Meta moved ESM to EvolutionaryScale) so unmaintained"
---

# ESMFold (Claude Skill)

Predicts protein structure directly from a single sequence with ESMFold — no MSA required — driven as a Claude skill.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Meta AI / EvolutionaryScale](https://github.com/facebookresearch/esm) |
| **Availability** | GA — Claude Science research skill |
| **Pricing** | Free / OSS (MIT code; model weights per Meta AI terms) |
| **Capabilities** | Read/Write — writes predicted structures (PDB) with pLDDT |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — featured Claude Science skill, MIT, but self-host facebookresearch/esm repo is archived/unmaintained |

## How to install

- **Claude Science** — enable the built-in **ESMFold** research skill (Anthropic-hosted; not published to the public `anthropics/life-sciences` marketplace).
- **Run the model yourself** — the upstream model is open source:
  ```
  git clone https://github.com/facebookresearch/esm
  ```
  Follow the repo README for environment setup and model weights.

## What it does

Runs ESMFold (built on the ESM-2 protein language model) to fold single sequences without an MSA. Uses local inference, or the ESM Atlas fold API (api.esmatlas.com/foldSequence/v1/pdb/) for quick one-off predictions.

**Primary use cases**: Fast single-sequence folding, high-throughput proteome folding, orphan-protein modelling

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

For embeddings and generative ESM3 / ESM C design see the broader [ESM skill](esm.html); this entry covers ESMFold structure prediction.

## Sources

- [facebookresearch/esm](https://github.com/facebookresearch/esm)
- [ESM Atlas](https://esmatlas.com/)
- [Lin et al. 2023, Science](https://www.science.org/doi/10.1126/science.ade2574)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=esmfold&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fesmfold.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
