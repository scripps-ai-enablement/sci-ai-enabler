---
title: scGPT (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Bo Wang Lab, University of Toronto
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-07-17
claude_science: true
summary: scGPT single-cell foundation model for cell-type annotation, integration, and perturbation prediction; runs locally as a Claude Science skill.
---

# scGPT (Claude Skill)

Applies the scGPT single-cell foundation model to annotate, integrate, and perturb single-cell data, driven as a Claude skill.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Bo Wang Lab, University of Toronto](https://github.com/bowang-lab/scGPT) |
| **Availability** | GA — Claude Science research skill |
| **Pricing** | Free / OSS (MIT; weights on Hugging Face/Drive) |
| **Capabilities** | Read/Write — local inference; writes embeddings, annotations, and predictions |

## How to install

- **Claude Science** — enable the built-in **scGPT** research skill (Anthropic-hosted; not published to the public `anthropics/life-sciences` marketplace).
- **Run the model yourself** — the upstream model is open source:
  ```
  git clone https://github.com/bowang-lab/scGPT
  ```
  Follow the repo README for environment setup and model weights.

## What it does

Runs scGPT for zero-shot and fine-tuned single-cell tasks: cell-type annotation, batch integration, gene-network inference, and perturbation-response prediction on AnnData inputs. Local inference only; pretrained weights fetched from Hugging Face/Drive.

**Primary use cases**: Cell-type annotation, single-cell integration, perturbation prediction

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

Local (your compute); GPU recommended. Complements [scvi-tools](scvi-tools.html) (VAE-based single-cell models).

## Sources

- [bowang-lab/scGPT](https://github.com/bowang-lab/scGPT)
- [Cui et al. 2024, Nature Methods](https://www.nature.com/articles/s41592-024-02201-0)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=scgpt&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fscgpt.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
