---
title: MHC Binding Prediction (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-11
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier GPTomics, repo MIT and maintained (pushed 2026-07-18), no OSV advisories; local skill runs user-installed predictors"
summary: "Predict peptide-MHC class I binding and natural presentation with MHCflurry, NetMHCpan-4.1, and MixMHCpred to nominate candidate CD8 T-cell epitopes"
---

# MHC Binding Prediction (bioSkills)

A Claude Code skill that scores peptides for binding and natural presentation by MHC class I molecules to nominate candidate CD8 T-cell epitopes and neoantigens.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches GPTomics, MIT repo maintained, no OSV advisories |

## How to install

bioSkills is **not** an npm package — clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "immunoinformatics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `--list` to preview and `--dry-run` to see what would be copied.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/immunoinformatics/mhc-binding-prediction ~/.claude/skills/
  ```
  (run from inside your clone; otherwise replace `bioSkills/` with the absolute path of your clone). Install `MHCflurry` (`pip install mhcflurry && mhcflurry-downloads fetch`) when prompted; `NetMHCpan-4.1` and `MixMHCpred` are separate academic downloads.

## What it does

Ranks peptides for MHC class I binding and presentation using three complementary predictors:

- **MHCflurry** — pip-installable Python presentation predictor with flexible allele parsing.
- **NetMHCpan-4.1** — the field-standard predictor with the broadest allele coverage.
- **MixMHCpred** — mass-spec–grounded presentation scoring.

The skill teaches the practical distinctions that matter (binding-affinity vs. eluted-ligand scoring, `%Rank` vs. raw nM for cross-allele comparisons) and the common failure modes (eluted-ligand abundance bias under-ranking low-expression neoantigens; pan-model extrapolation error on rare alleles). It stresses that predicted binding is necessary but not sufficient for immunogenicity.

**Primary use cases**: scanning proteins for class I epitopes, scoring tumor neoantigen candidates, choosing the right predictor for a given allele/question.

## Notes

Distributed as a `SKILL.md` in the bioSkills collection — Claude executes the workflow locally via Bash/Python rather than as an MCP server. Upstream front-matter name: `bio-immunoinformatics-mhc-binding-prediction`. Complementary to the broader [Epitope Prediction](epitope-prediction.html) bioSkills skill (which also covers B-cell and class II). NetMHCpan/MixMHCpred require separate academic-use downloads from their vendors. Upstream directory: `immunoinformatics/mhc-binding-prediction`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`immunoinformatics/mhc-binding-prediction/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/mhc-binding-prediction/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=mhc-binding-prediction&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmhc-binding-prediction.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
