---
title: AlphaFold2 (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Google DeepMind
availability: GA
tool_categories: [Drug Repurposing and Discovery, Integrative Structural and Computational Biology, Molecular and Cellular Biology]
last_verified: 2026-07-17
claude_science: true
summary: AlphaFold2 protein/complex structure prediction, run locally or via a hosted API with an optional ColabFold MSA server; a Claude Science skill.
---

# AlphaFold2 (Claude Skill)

Predicts 3D protein and complex structures with AlphaFold2, driven as a Claude skill over local or vendor-hosted inference.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Google DeepMind](https://github.com/google-deepmind/alphafold) |
| **Availability** | GA — Claude Science research skill |
| **Pricing** | Free / OSS (Apache-2.0 code; AlphaFold2 parameters CC BY 4.0) |
| **Capabilities** | Read/Write — Claude runs the model and writes predicted structures (PDB/mmCIF) plus per-residue pLDDT/PAE confidence |

## How to install

- **Claude Science** — enable the built-in **AlphaFold2** research skill (Anthropic-hosted; not published to the public `anthropics/life-sciences` marketplace).
- **Run the model yourself** — the upstream model is open source:
  ```
  git clone https://github.com/google-deepmind/alphafold
  ```
  Follow the repo README for environment setup and model weights.

## What it does

Runs AlphaFold2 to predict monomer and multimer structures from sequence. Builds multiple-sequence alignments locally or via the ColabFold MSA server (`--use_msa_server`, api.colabfold.com), or retrieves precomputed models from the AlphaFold DB API (alphafold.ebi.ac.uk/api). Emits ranked structures with pLDDT and PAE confidence.

**Primary use cases**: Structure prediction for a target list, complex/interface modelling, pre-docking model preparation

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

Runs locally (GPU recommended) or via a vendor-hosted API. For retrieval of already-deposited predictions (no compute) see the [AlphaFold MCP Server](alphafold.html); this skill does *de novo* prediction.

## Sources

- [google-deepmind/alphafold](https://github.com/google-deepmind/alphafold)
- [ColabFold](https://github.com/sokrypton/ColabFold)
- [Jumper et al. 2021, Nature](https://www.nature.com/articles/s41586-021-03819-2)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=alphafold2&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Falphafold2.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
