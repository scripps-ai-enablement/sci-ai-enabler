---
title: ProteinMPNN (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Baker Lab, UW Institute for Protein Design
availability: GA
tool_categories: [Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-07-17
claude_science: true
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches dauparas/ProteinMPNN, MIT, stable research model (1796 stars, repo active), no GitHub advisories"
summary: ProteinMPNN deep-learning fixed-backbone protein sequence design; runs locally as a Claude Science skill.
---

# ProteinMPNN (Claude Skill)

Designs amino-acid sequences that fold to a target backbone using ProteinMPNN, driven as a Claude skill.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Baker Lab, UW Institute for Protein Design](https://github.com/dauparas/ProteinMPNN) |
| **Availability** | GA — Claude Science research skill |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — local inference; writes designed sequences (FASTA) with per-position scores |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches dauparas/ProteinMPNN, MIT, no advisories |

## How to install

- **Claude Science** — enable the built-in **ProteinMPNN** research skill (Anthropic-hosted; not published to the public `anthropics/life-sciences` marketplace).
- **Run the model yourself** — the upstream model is open source:
  ```
  git clone https://github.com/dauparas/ProteinMPNN
  ```
  Follow the repo README for environment setup and model weights.

## What it does

Runs ProteinMPNN to generate sequences for a fixed protein backbone (PDB input), with control over fixed/tied positions, temperature, and symmetry. Local inference only; commonly paired with RFdiffusion backbones and AlphaFold validation.

**Primary use cases**: De novo protein sequence design, backbone redesign, binder-sequence generation

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

Local (your compute). For ligand/metal/nucleotide context use [LigandMPNN](ligandmpnn.html); for solubility-tuned designs use [SolubleMPNN](solublempnn.html).

## Sources

- [dauparas/ProteinMPNN](https://github.com/dauparas/ProteinMPNN)
- [Dauparas et al. 2022, Science](https://www.science.org/doi/10.1126/science.add2187)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=proteinmpnn&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fproteinmpnn.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
