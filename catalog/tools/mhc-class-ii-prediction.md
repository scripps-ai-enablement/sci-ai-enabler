---
title: MHC Class II Prediction (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-18
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches GPTomics/bioSkills, MIT, no OSV/GitHub advisories, read-only local class II prediction with free academic-download dependencies and no credential requests"
summary: "Predict peptide-MHC class II (HLA-DR/DQ/DP) binding for CD4 T-cell epitopes with NetMHCIIpan-4.3 and MixMHC2pred-2.0, with the reliability caveats class II demands"
---

# MHC Class II Prediction (bioSkills)

A Claude Code skill that predicts CD4 T-cell epitopes by scoring peptide binding to MHC class II (HLA-DR/DQ/DP) alleles, with explicit handling of the accuracy limits class II carries.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches GPTomics/bioSkills, MIT, no advisories, read-only local class II prediction |

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
  cp -r bioSkills/immunoinformatics/mhc-class-ii-prediction ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). The skill declares its external dependencies (NetMHCIIpan-4.3, MixMHC2pred-2.0) in `SKILL.md`; install them when prompted on first use.

## What it does

Predicts CD4 T-cell epitopes through class II binding with two complementary tools:

- **NetMHCIIpan-4.3** — pan-allele predictor covering DR, DQ, and DP isotypes; outputs EL scores and optional binding affinity.
- **MixMHC2pred-2.0** — mass-spec immunopeptidome-grounded motif tool that models the reverse-binding DP mode.

The skill is explicit about why class II is far less reliable than class I: the open binding groove, 9-mer core register ambiguity, sparse/noisy training data, and a DR > DP > DQ accuracy asymmetry. It flags the DQ/DP heterodimer alpha/beta pairing trap (scoring non-existent heterodimers) and recommends looser %Rank thresholds (≤1% strong, ≤5% weak) than class I, treating calls as ranked hypotheses rather than facts.

**Primary use cases**: CD4 epitope discovery for vaccine T-helper design, class II neoantigen mapping, scoring long peptides against DR/DQ/DP.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally via Bash/Python rather than as an MCP server. The upstream skill front-matter name is `bio-immunoinformatics-mhc-class-ii-prediction`; if you invoke it as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/mhc-class-ii-prediction`. For CD8/class I binding, use the `mhc-binding-prediction` skill instead. NetMHCIIpan and MixMHC2pred require a separate (free, academic) download/registration from their vendors. Upstream directory: `immunoinformatics/mhc-class-ii-prediction`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`immunoinformatics/mhc-class-ii-prediction/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/mhc-class-ii-prediction/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=mhc-class-ii-prediction&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmhc-class-ii-prediction.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
