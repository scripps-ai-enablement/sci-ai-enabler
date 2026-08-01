---
title: Functional Profiling (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-08-01
summary: "Profile metagenome functional potential with HUMAnN 3 tiered search, producing species-stratified gene-family and MetaCyc pathway abundances with normalization guidance"
---

# Functional Profiling (bioSkills)

A Claude Code skill that quantifies the functional potential of shotgun metagenomes with HUMAnN 3, producing gene-family and pathway abundances stratified by the species that contribute them.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — HUMAnN, MetaPhlAn, Bowtie2, DIAMOND and the UniRef/ChocoPhlAn databases are separately installed OSS |
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
  cp -r bioSkills/metagenomics/functional-profiling ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install HUMAnN and download the ChocoPhlAn/UniRef databases when prompted on first use.

## What it does

Runs HUMAnN 3's tiered search and interprets the output tables correctly:

- **Workflow** — host depletion and quality trimming (KneadData), a MetaPhlAn 4.1+ taxonomic prescreen that builds a sample-specific ChocoPhlAn pangenome, tier-1 Bowtie2 nucleotide alignment against that pangenome (high-confidence stratification), tier-2 DIAMOND six-frame translated search against UniRef90/50 (inferred stratification), RPK→CPM normalization before any cross-sample statistics, and regrouping to KO/EC/GO with stratified and unstratified tables split out.
- **Interpretation guidance** — a metagenome measures functional *potential*, not activity (RNA-level validation is required for activity claims); dropping the `UNMAPPED`/`UNINTEGRATED` rows biases every downstream comparison; species stratification is an estimate rather than a measurement; coverage vs abundance and the MinPath/gap-fill behaviour; UniRef90-vs-50 and biome-specific database bias.
- **Alternatives** — assembly-based functional annotation, eggNOG-mapper, dbCAN (CAZymes), and antiSMASH (biosynthetic gene clusters).

**Primary use cases**: MetaCyc pathway abundance across cohorts, gene-family (KO/EC/GO) profiles, choosing read-based vs assembly-based functional annotation.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-metagenomics-functional-profiling`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/functional-profiling`. HUMAnN's prescreen step means the catalogued [MetaPhlAn Profiling](metaphlan-profiling.html) skill covers its taxonomic half. The skill routes AMR-gene questions to [AMR Detection](amr-detection.html) and host-gene enrichment to pathway-analysis rather than answering them itself.  Upstream directory: `metagenomics/functional-profiling`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`metagenomics/functional-profiling/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/metagenomics/functional-profiling/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=functional-profiling&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ffunctional-profiling.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
