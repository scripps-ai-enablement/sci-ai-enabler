---
title: LigandMPNN (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Baker Lab, UW Institute for Protein Design
availability: GA
tool_categories: [Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-07-17
claude_science: true
summary: LigandMPNN ligand-aware protein sequence design (fixed-backbone) accounting for small molecules, metals, and nucleotides; a Claude Science skill.
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches Baker Lab dauparas/LigandMPNN MIT via GitHub API, featured Claude Science skill, local inference no credentials"
---

# LigandMPNN (Claude Skill)

Designs protein sequences for a fixed backbone while accounting for bound ligands, metals, and nucleic acids using LigandMPNN, driven as a Claude skill.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Baker Lab, UW Institute for Protein Design](https://github.com/dauparas/LigandMPNN) |
| **Availability** | GA — Claude Science research skill |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — local inference; writes designed sequences (FASTA) and scores |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches Baker Lab, MIT, featured Claude Science skill, local inference no credentials |

## How to install

- **Claude Science** — enable the built-in **LigandMPNN** research skill (Anthropic-hosted; not published to the public `anthropics/life-sciences` marketplace).
- **Run the model yourself** — the upstream model is open source:
  ```
  git clone https://github.com/dauparas/LigandMPNN
  ```
  Follow the repo README for environment setup and model weights.

## What it does

Runs LigandMPNN to design amino-acid sequences for a target backbone (PDB), conditioning on non-protein context (ligands, metals, nucleotides). Local inference only.

**Primary use cases**: Ligand-binding-site redesign, enzyme active-site design, metalloprotein sequence design

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

Local (your compute). Same family as ProteinMPNN with explicit non-protein atom context.

## Sources

- [dauparas/LigandMPNN](https://github.com/dauparas/LigandMPNN)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=ligandmpnn&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fligandmpnn.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
