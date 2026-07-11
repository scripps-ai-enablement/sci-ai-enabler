---
title: Immcantation BCR Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-11
summary: "Reconstruct B-cell clonal families, quantify somatic hypermutation and selection, and build antibody lineage trees from AIRR-seq data with the Immcantation R suite"
---

# Immcantation BCR Analysis (bioSkills)

A Claude Code skill that reconstructs B-cell clonal families, measures somatic hypermutation and antigen-driven selection, and infers antibody lineage trees from AIRR-format repertoire-sequencing data.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's R/Python workflow locally (Bash), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "tcr-bcr-analysis"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `--list` to preview and `--dry-run` to see what would be copied.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/tcr-bcr-analysis/immcantation-analysis ~/.claude/skills/
  ```
  (run from inside your clone; otherwise replace `bioSkills/` with the absolute path of your clone). The skill uses the Immcantation R suite (`alakazam`, `shazam`, `scoper`, `dowser`, `tigger`) plus IgBLAST/Change-O/IgPhyML — install these when prompted; the Immcantation Docker image is the simplest way to get the full toolchain.

## What it does

Runs a full BCR clonal-analysis pipeline on AIRR-format sequences using five Immcantation R packages:

- **shazam** — data-derived distance thresholding and mutation quantification.
- **scoper** — clonal clustering into families.
- **alakazam** — diversity metrics (Hill numbers).
- **dowser** — germline reconstruction and lineage-tree inference.
- **tigger** — personalized V-gene genotyping.

Key workflows: clonal partitioning using a *derived* (bimodal-valley) threshold rather than a hardcoded constant; replacement-vs-silent mutation profiling by CDR/FWR region; BASELINe selection testing; and germline-rooted, codon-aware lineage trees tracing affinity maturation and class switching.

**Primary use cases**: BCR clonal-family reconstruction, somatic-hypermutation profiling, selection testing, antibody lineage/affinity-maturation analysis.

## Notes

Distributed as a `SKILL.md` in the bioSkills collection — Claude executes the R/Python workflow locally via Bash rather than as an MCP server. Upstream front-matter name: `bio-tcr-bcr-analysis-immcantation-analysis`. This is the first Claude-installable wrapper for the Immcantation framework the catalog has surfaced (previously a tracked gap). Requires AIRR-formatted input (e.g., from IgBLAST or TRUST4). Upstream directory: `tcr-bcr-analysis/immcantation-analysis`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`tcr-bcr-analysis/immcantation-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/immcantation-analysis/SKILL.md)
- [Immcantation framework](https://immcantation.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=immcantation-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fimmcantation-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
