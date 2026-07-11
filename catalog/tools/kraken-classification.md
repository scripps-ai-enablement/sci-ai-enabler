---
title: Kraken2 Metagenomic Classification (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-11
summary: "Classify shotgun metagenomic reads to taxa with Kraken2 minimizer/LCA matching, then re-estimate abundance with Bracken"
---

# Kraken2 Metagenomic Classification (bioSkills)

A Claude Code skill for taxonomic profiling of shotgun metagenomic reads with Kraken2, refined to abundance estimates with Bracken.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "metagenomics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `--list` to preview and `--dry-run` to see what would be copied.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/metagenomics/kraken-classification ~/.claude/skills/
  ```
  (run from inside your clone; otherwise replace `bioSkills/` with the absolute path of your clone). Install `kraken2`, `bracken`, and `KrakenTools` (bioconda) plus a reference database when prompted on first use.

## What it does

Teaches "who is there" taxonomic profiling of shotgun reads:

- **Kraken2** — fast k-mer minimizer + lowest-common-ancestor read classification against a chosen reference database.
- **Bracken** — Bayesian rank-level abundance re-estimation to correct read-level misassignments.
- **KrakenTools / KrakenUniq** — unique-minimizer filtering to control false positives.

The skill emphasizes that the database (not the algorithm) determines what can be detected, and draws the critical distinction between read classification, presence detection, and true abundance quantification. Covers database selection/building, confidence-threshold and hit-group tuning, and read-count-to-abundance conversion.

**Primary use cases**: metagenome taxonomic profiling, reference-database selection, false-positive control, community abundance estimation.

## Notes

Distributed as a `SKILL.md` in the bioSkills collection — Claude executes the workflow locally via Bash rather than as an MCP server. Upstream front-matter name: `bio-metagenomics-kraken`. Reference databases (e.g., Standard, PlusPF) are large downloads and are not bundled. Complementary to the `amr-detection` and MetaPhlAn bioSkills metagenomics skills. Upstream directory: `metagenomics/kraken-classification`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`metagenomics/kraken-classification/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/metagenomics/kraken-classification/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=kraken-classification&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fkraken-classification.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
