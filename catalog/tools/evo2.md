---
title: Evo 2 (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Arc Institute
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-07-17
claude_science: true
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches ArcInstitute/evo2, Apache-2.0, active (pushed 2026-06-19, 3993 stars), no GitHub advisories"
summary: Evo 2 genome language model for DNA/RNA/protein sequence generation and variant scoring; local (Hopper GPU) or NVIDIA-hosted; a Claude Science skill.
---

# Evo 2 (Claude Skill)

Generates and scores biological sequences across DNA, RNA, and protein with the Evo 2 genome language model, driven as a Claude skill.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Arc Institute](https://github.com/ArcInstitute/evo2) |
| **Availability** | GA — Claude Science research skill |
| **Pricing** | Free / OSS (Apache-2.0); NVIDIA-hosted inference metered per NVIDIA terms |
| **Capabilities** | Read/Write — sequence generation and variant likelihood scoring |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches ArcInstitute/evo2, Apache-2.0, active, no advisories |

## How to install

- **Claude Science** — enable the built-in **Evo 2** research skill (Anthropic-hosted; not published to the public `anthropics/life-sciences` marketplace).
- **Run the model yourself** — the upstream model is open source:
  ```
  git clone https://github.com/ArcInstitute/evo2
  ```
  Follow the repo README for environment setup and model weights.

## What it does

Runs Evo 2 for long-context genomic sequence modelling: de novo sequence generation, zero-shot variant-effect scoring, and embedding extraction. Local inference needs a Hopper-class GPU (FP8); otherwise use the NVIDIA-hosted inference API (NVIDIA NIM / build.nvidia.com).

**Primary use cases**: Genomic sequence generation, zero-shot variant-effect prediction, regulatory-element design

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

Local runs require a Hopper GPU with FP8 support; a hosted NVIDIA NIM endpoint is the alternative.

## Sources

- [ArcInstitute/evo2](https://github.com/ArcInstitute/evo2)
- [NVIDIA build.nvidia.com](https://build.nvidia.com/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=evo2&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fevo2.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
