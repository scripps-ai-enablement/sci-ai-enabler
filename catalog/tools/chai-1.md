---
title: Chai-1 (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Chai Discovery
availability: GA
tool_categories: [Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-07-17
claude_science: true
summary: Chai-1 biomolecular structure prediction (proteins, nucleic acids, ligands) run locally or via a hosted server; a Claude Science skill.
---

# Chai-1 (Claude Skill)

Predicts biomolecular complex structures with Chai-1, driven as a Claude skill over local or hosted inference.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Chai Discovery](https://github.com/chaidiscovery/chai-lab) |
| **Availability** | GA — Claude Science research skill |
| **Pricing** | Free / OSS (Apache-2.0, code + weights) |
| **Capabilities** | Read/Write — writes predicted complex structures with confidence scores |

## How to install

- **Claude Science** — enable the built-in **Chai-1** research skill (Anthropic-hosted; not published to the public `anthropics/life-sciences` marketplace).
- **Run the model yourself** — the upstream model is open source:
  ```
  git clone https://github.com/chaidiscovery/chai-lab
  ```
  Follow the repo README for environment setup and model weights.

## What it does

Runs Chai-1 to predict structures of proteins, nucleic acids, and protein–ligand complexes. Optionally uses the hosted web server (lab.chaidiscovery.com) or an MSA server; otherwise fully local.

**Primary use cases**: Complex structure prediction, protein–ligand modelling, antibody/antigen modelling

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

Local or vendor-hosted (lab.chaidiscovery.com). GPU recommended for local runs.

## Sources

- [chaidiscovery/chai-lab](https://github.com/chaidiscovery/chai-lab)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=chai-1&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fchai-1.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
