---
title: Borzoi (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Calico Life Sciences
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-07-17
claude_science: true
summary: Borzoi sequence-to-expression model predicting RNA-seq coverage from DNA sequence; runs locally as a Claude Science skill.
---

# Borzoi (Claude Skill)

Predicts cell-type-resolved RNA-seq coverage directly from DNA sequence using Calico's Borzoi model, driven as a Claude skill.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Calico Life Sciences](https://github.com/calico/borzoi) |
| **Availability** | GA — Claude Science research skill |
| **Pricing** | Free / OSS (Apache-2.0; weights on Hugging Face) |
| **Capabilities** | Read/Write — local inference; writes per-track predicted coverage and variant-effect scores |

## How to install

- **Claude Science** — enable the built-in **Borzoi** research skill (Anthropic-hosted; not published to the public `anthropics/life-sciences` marketplace).
- **Run the model yourself** — the upstream model is open source:
  ```
  git clone https://github.com/calico/borzoi
  ```
  Follow the repo README for environment setup and model weights.

## What it does

Runs Borzoi to predict RNA-seq (and related assay) coverage tracks from input DNA sequence, and to score the regulatory effect of sequence variants. Local inference only — no external API call.

**Primary use cases**: Sequence-to-expression prediction, regulatory variant-effect scoring, enhancer/promoter dissection

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

Local (your compute); GPU recommended. Weights distributed via Hugging Face.

## Sources

- [calico/borzoi](https://github.com/calico/borzoi)
- [Linder et al. 2025, Nature Genetics](https://www.nature.com/articles/s41588-024-02053-6)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=borzoi&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fborzoi.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
