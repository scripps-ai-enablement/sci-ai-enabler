---
title: Immunogenicity Scoring (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology, Translational Medicine]
last_verified: 2026-08-01
summary: "Rank neoantigen and epitope candidates by likely T-cell response using NeoFox features, PRIME2.0, BigMHC-IM, the fitness model and pVACtools tiering"
---

# Immunogenicity Scoring (bioSkills)

A Claude Code skill that prioritizes neoantigen and epitope candidates by the likelihood of an actual T-cell response, rather than by binding affinity alone.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — NeoFox, PRIME2.0, BigMHC-IM, MixMHCpred and pVACtools are separately installed and carry their own (in some cases academic-only) terms |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "immunoinformatics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/immunoinformatics/immunogenicity-scoring ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install NeoFox and the chosen recognition predictors when prompted on first use.

## What it does

Turns a candidate epitope list into an auditable, feature-annotated shortlist:

- **Workflow** — NeoFox annotates ~16 presentation and recognition features without ranking; non-negotiable expression and clonality filters are applied first (gene TPM ≥ 1, RNA VAF ≥ 0.25); PRIME2.0 or BigMHC-IM scores class-I immunogenicity; agretopicity (mutant-vs-wild-type binding gain) and foreignness are computed defensively; candidates are ranked *within* a patient by presentation strength, abundance and quality; pVACtools rule-based tiers quarantine anchor-position artifacts and subclonal traps; the output is presented for human curation with uncertainty stated.
- **Method panel** — NeoFox (DAI, foreignness, dissimilarity, PRIME, PHBR), PRIME2.0 (presentation × TCR recognition, requires MixMHCpred v3.0+), BigMHC-IM (pan-allelic transfer-learned immunogenicity), pVACtools (tiering), and IEDB as a reference database that the skill treats as a weak standalone predictor.

**Primary use cases**: personalized cancer-vaccine candidate selection, TCR-therapy target triage, ranking a pVACseq/NeoFox candidate list.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-immunoinformatics-immunogenicity-scoring`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/immunogenicity-scoring`. This is the ranking stage downstream of the catalogued [Neoantigen Prediction](neoantigen-prediction.html), [MHC Binding Prediction](mhc-binding-prediction.html) and [Epitope Prediction](epitope-prediction.html) skills, which generate the candidates it scores. Several bundled predictors (notably MixMHCpred/PRIME) are distributed under academic-use licenses by their own authors — check each before commercial use; the MIT grant covers the bioSkills skill text only.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`immunoinformatics/immunogenicity-scoring/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/immunogenicity-scoring/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=immunogenicity-scoring&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fimmunogenicity-scoring.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
