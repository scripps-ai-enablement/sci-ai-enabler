---
title: OpenFold3 (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: OpenFold Consortium / AQ Laboratory
availability: GA
tool_categories: [Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-07-17
claude_science: true
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches aqlaboratory/openfold, Apache-2.0, active (pushed 2025-12-16, 3397 stars), no GitHub advisories"
summary: OpenFold3 open-source biomolecular structure prediction (AlphaFold-class), run locally; a Claude Science skill.
---

# OpenFold3 (Claude Skill)

Predicts biomolecular structures with the open-source OpenFold3 model, driven as a Claude skill on local compute.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [OpenFold Consortium / AQ Laboratory](https://github.com/aqlaboratory/openfold) |
| **Availability** | GA — Claude Science research skill |
| **Pricing** | Free / OSS (Apache-2.0 code) |
| **Capabilities** | Read/Write — writes predicted structures with confidence |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches aqlaboratory/openfold, Apache-2.0, no advisories |

## How to install

- **Claude Science** — enable the built-in **OpenFold3** research skill (Anthropic-hosted; not published to the public `anthropics/life-sciences` marketplace).
- **Run the model yourself** — the upstream model is open source:
  ```
  git clone https://github.com/aqlaboratory/openfold
  ```
  Follow the repo README for environment setup and model weights.

## What it does

Runs OpenFold3, the open reimplementation/extension of the AlphaFold architecture, to predict protein and complex structures. MSA generation runs locally (jackhmmer) or via the ColabFold API; there is no vendor inference API.

**Primary use cases**: Open-source structure prediction, reproducible folding pipelines, complex modelling

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

Local (your compute); GPU recommended. Fully open training/inference stack.

## Sources

- [aqlaboratory/openfold](https://github.com/aqlaboratory/openfold)
- [OpenFold, Ahdritz et al. 2024, Nature Methods](https://www.nature.com/articles/s41592-024-02272-z)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=openfold3&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fopenfold3.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
