---
title: Epitope Prediction (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-11
summary: "Predict B-cell and T-cell epitopes for vaccine and epitope-mapping work with BepiPred-3.0, DiscoTope-3.0, the IEDB tools, and MHC presentation predictors"
---

# Epitope Prediction (bioSkills)

A Claude Code skill that identifies antibody-binding (B-cell) and MHC-presented (T-cell) immunogenic regions of an antigen for vaccine design and epitope mapping.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "immunoinformatics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview and `--dry-run` to see what would be copied.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/immunoinformatics/epitope-prediction ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). The skill declares its external dependencies (BepiPred-3.0, DiscoTope-3.0, NetMHCpan/MHCflurry) in `SKILL.md`; install them when prompted on first use.

## What it does

Scores candidate epitopes across the two arms of adaptive immunity:

- **B-cell (antibody) epitopes** — `BepiPred-3.0` for linear sequence-based scoring and `DiscoTope-3.0` for structure-based conformational prediction (the more defensible route when a 3D model/AlphaFold structure exists).
- **T-cell epitopes** — MHC class I presentation via `NetMHCpan-4.1` / `MHCflurry` and class II / integrated CTL prediction via `NetMHCIIpan` / `NetCTLpan`, with an `IEDB REST API` wrapper for multiple predictors.

The skill is explicit that T-cell prediction is mature (AUC > 0.9) while sequence-only B-cell prediction is unreliable because ~90% of real epitopes are conformational — steering the user to structure-based methods for B-cell work.

**Primary use cases**: vaccine antigen selection, epitope mapping, cross-strain epitope conservation checks.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally via Bash/Python rather than as an MCP server. The upstream skill front-matter name is `bio-immunoinformatics-epitope-prediction`; if you invoke it as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/epitope-prediction`. NetMHCpan and some IEDB standalone tools require a separate (free, academic) download/registration from their vendors. Upstream directory: `immunoinformatics/epitope-prediction`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`immunoinformatics/epitope-prediction/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/epitope-prediction/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=epitope-prediction&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fepitope-prediction.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
