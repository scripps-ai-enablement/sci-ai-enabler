---
title: SolubleMPNN (Claude Skill)
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
security_note: "provenance matches dauparas/LigandMPNN (weights bundled there), MIT, active (605 stars), no GitHub advisories"
summary: Soluble-optimized ProteinMPNN weights that bias sequence design away from exposed hydrophobics; a Claude Science skill.
---

# SolubleMPNN (Claude Skill)

Designs protein sequences with ProteinMPNN using soluble-optimized weights that discourage surface hydrophobics, driven as a Claude skill.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Baker Lab, UW Institute for Protein Design](https://github.com/dauparas/LigandMPNN) |
| **Availability** | GA — Claude Science research skill |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — local inference; writes designed sequences (FASTA) |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches dauparas/LigandMPNN, MIT, no advisories |

## How to install

- **Claude Science** — enable the built-in **SolubleMPNN** research skill (Anthropic-hosted; not published to the public `anthropics/life-sciences` marketplace).
- **Run the model yourself** — the upstream model is open source:
  ```
  git clone https://github.com/dauparas/LigandMPNN
  ```
  Follow the repo README for environment setup and model weights.

## What it does

Runs ProteinMPNN with the SolubleMPNN weight set, which penalizes solvent-exposed hydrophobic residues to improve expression and solubility of designed proteins. Local inference only. The weights ship inside the ProteinMPNN / LigandMPNN repositories.

**Primary use cases**: Solubility-optimized protein design, improving expression of de novo designs

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

Local (your compute). A weight variant of [ProteinMPNN](proteinmpnn.html); bundled in the ProteinMPNN / LigandMPNN repos.

## Sources

- [dauparas/LigandMPNN](https://github.com/dauparas/LigandMPNN)
- [dauparas/ProteinMPNN](https://github.com/dauparas/ProteinMPNN)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=solublempnn&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fsolublempnn.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
