---
title: Taxonomy Assignment (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-25
summary: "Assign taxonomy to 16S/ITS/18S amplicon ASVs using DADA2, DECIPHER IDTAXA or QIIME2 classifiers against SILVA/GTDB/Greengenes2/UNITE, with region-specific training guidance"
---

# Taxonomy Assignment (bioSkills)

A Claude Code skill that assigns taxonomy to amplicon ASVs/OTUs using classifiers conditioned on the right reference database and primer region, and flags the confidence and over-classification trade-offs.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — DADA2, DECIPHER, QIIME2 and the reference databases are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/R), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "microbiome"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/microbiome/taxonomy-assignment ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the chosen classifier and reference database when prompted on first use.

## What it does

Classifies 16S/ITS/18S ASVs to taxonomy, choosing a classifier and database matched to the amplicon region and desired conservatism:

- **Classifiers** — DADA2 `assignTaxonomy` (RDP 8-mer naive Bayes + bootstrap) + `addSpecies` (exact 100% match); DECIPHER IDTAXA (tree-descent, novelty-aware, conservative); QIIME2 `classify-sklearn` (multinomial NB over 7-mers, region-matched training) and `classify-consensus-vsearch` (global alignment + consensus voting); weighted/clawback classifiers with habitat-specific abundance priors.
- **Reference databases** — SILVA (138.1/138.2, 16S), GTDB (r220, genome-based rank-normalized), Greengenes2 (2024.09), UNITE (fungal ITS), PR2 (5.x, protist 18S), and legacy RDP.
- **Guidance** — region-specific classifier training, confidence/bootstrap thresholds, and minimizing over-classification.

**Primary use cases**: taxonomic classification of microbiome ASVs, reference-database selection, confidence-thresholded genus/species calls.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-microbiome-taxonomy-assignment`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/taxonomy-assignment`. Takes the ASV table produced upstream by `amplicon-processing`; feeds the microbiome diversity/differential-abundance skills. Upstream directory: `microbiome/taxonomy-assignment`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`microbiome/taxonomy-assignment/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/microbiome/taxonomy-assignment/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=taxonomy-assignment&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftaxonomy-assignment.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
