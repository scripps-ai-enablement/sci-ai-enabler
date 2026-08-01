---
title: MetaPhlAn Profiling (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-08-01
summary: "Profile shotgun metagenomes to species/SGB relative abundance with MetaPhlAn 4 clade-specific markers, with cell-fraction vs read-fraction and index-pinning guidance"
---

# MetaPhlAn Profiling (bioSkills)

A Claude Code skill that profiles shotgun metagenomes to species and species-level genome bin (SGB) abundance using MetaPhlAn 4's clade-specific marker genes, and keeps the resulting units interpretable.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — MetaPhlAn, Bowtie2, minimap2 and the marker database are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "metagenomics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/metagenomics/metaphlan-profiling ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install MetaPhlAn and download the marker index when prompted on first use.

## What it does

Runs marker-gene taxonomic profiling and explains the units it produces:

- **Workflow** — align reads to clade-specific markers (Bowtie2 for short reads, minimap2 for long reads), detect clades whose private markers are present, average per-marker coverage with a quantile-truncated robust mean (`--stat_q`), normalize to genome-size-aware cell fractions, optionally estimate the database-absent `UNCLASSIFIED` fraction, and re-profile cached mappings at other taxonomic levels.
- **Unit discipline** — a MetaPhlAn percentage is a genome-size-normalized *cell* fraction and must not be pooled with Kraken/Bracken *read* fractions; covers kSGB vs uSGB units for quantifying taxa absent from the database, the unknown-fraction rescaling and its version-default flip, and pinning `--index` because the database version is a batch variable.
- **Alternatives** — when mOTUs3 or `sourmash gather` are the better choice than marker profiling.
- **Components** — MetaPhlAn 4.1+ (~189 markers per SGB), Bowtie2 2.5.3+, minimap2 2.26+, pandas 2.2+, and the `mpa_vJun23_CHOCOPhlAnSGB` index family.

**Primary use cases**: species/SGB relative abundance from shotgun metagenomes, cross-study profile harmonization, long-read metagenome profiling.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-metagenomics-metaphlan`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/metaphlan-profiling`. Complements the catalogued [Kraken Classification](kraken-classification.html) skill, which produces read-fraction profiles from the same input — the skill is explicit that the two abundance types are not interchangeable. Feeds the strain-tracking and functional-profiling skills. Upstream directory: `metagenomics/metaphlan-profiling`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`metagenomics/metaphlan-profiling/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/metagenomics/metaphlan-profiling/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=metaphlan-profiling&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmetaphlan-profiling.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
