---
title: Differential Abundance (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-08-01
summary: "Test which microbiome taxa differ between groups using compositionally-aware methods (ALDEx2, ANCOM-BC2, MaAsLin, LinDA, ZicoSeq) and report a multi-tool consensus"
verification: works
verified_on: 2026-08-03
reviewed_on: 2026-08-03
security: cleared
security_on: 2026-08-03
security_note: "GPTomics/bioSkills root LICENSE confirmed MIT this run, not archived, 1.1k stars, skill dir current"
---

# Differential Abundance (bioSkills)

A Claude Code skill that tests which individual taxa differ between groups in an amplicon feature table, using compositionally-aware methods and reporting the consensus across several of them rather than one tool's hit list.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — phyloseq, ALDEx2, ANCOMBC, MaAsLin, LinDA, ZicoSeq, LEfSe and QIIME2 are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (R), not as an MCP tool |
| **Verified** | works · 2026-08-03 |
| **Security** | cleared · 2026-08-03 — GPTomics/bioSkills MIT confirmed, provenance matches, no advisories |

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
  cp -r bioSkills/microbiome/differential-abundance ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the R packages for the chosen methods when prompted on first use.

## What it does

Runs several differential-abundance methods on one feature table and reconciles them:

- **Workflow** — load a phyloseq object and apply a prevalence filter (10–25% of samples) to drop rare features and stabilize multiple-testing correction; run at least two methods from the panel on the same table; intersect the significant-taxa sets, reporting the intersection as high-confidence and the union as exploratory with per-taxon tool agreement; gate results on an effect-size floor alongside BH/FDR.
- **Method panel** — ALDEx2 (Dirichlet Monte-Carlo CLR, conservative), ANCOM-BC2/ANCOMBC (sampling-fraction bias correction, structural zeros, `passed_ss`, Holm default), MaAsLin2/MaAsLin3 (multivariable GLM with random effects and a prevalence/abundance split), LinDA (CLR mixed-model regression), ZicoSeq (permutation FDR), LEfSe, and QIIME2 `q2-composition ancombc`.
- **Interpretation guidance** — the Nearing benchmark finding that the hit list depends more on the chosen tool than on the biology (hence the consensus deliverable); why a relative change is not an absolute one without a microbial-load anchor; the prevalence-filter knob; and why DESeq2/edgeR misfire on compositional amplicon data.

**Primary use cases**: taxa differing between case and control groups, covariate-adjusted or longitudinal microbiome designs, choosing a differential-abundance method.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-microbiome-differential-abundance`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/differential-abundance`. Consumes the ASV table built by [Amplicon Processing](amplicon-processing.html) and labelled by [Taxonomy Assignment](taxonomy-assignment.html). The skill routes whole-community questions to the microbiome diversity-analysis skill and shotgun differential abundance to the metagenomics category instead of answering them here. Upstream directory: `microbiome/differential-abundance`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`microbiome/differential-abundance/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/microbiome/differential-abundance/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=differential-abundance&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdifferential-abundance.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
