---
title: Repertoire Visualization (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-25
summary: "Render TCR/BCR repertoire figures — V-J chord diagrams, spectratypes, clonal tracking, rarefaction curves, overlap heatmaps and similarity networks — with depth-robust metric guidance"
verification: works
verified_on: 2026-07-27
security: cleared
security_on: 2026-07-27
security_note: "provenance matches GPTomics/bioSkills, MIT, maintained (pushed 2026-07-25), no OSV advisories; VDJtools and R/Python deps are separately-installed OSS"
---

# Repertoire Visualization (bioSkills)

A Claude Code skill that renders publication-quality TCR/BCR repertoire figures and advises on which visualization and comparison metric to use for depth-robust conclusions.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — VDJtools and R/Python dependencies are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/R/Python), not as an MCP tool |
| **Verified** | works · 2026-07-27 — GPTomics/bioSkills resolves; clone + copy install path current |
| **Security** | cleared · 2026-07-27 — provenance matches GPTomics/bioSkills, MIT, maintained, no OSV advisories |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "tcr-bcr-analysis"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/tcr-bcr-analysis/repertoire-visualization ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the R/Python/CLI dependencies (below) when prompted on first use.

## What it does

Turns an assembled repertoire table (native or AIRR) into interpretable figures, with built-in guidance on metric choice so comparisons are not confounded by sequencing depth:

- **Figure types** — V-J usage chord/circos diagrams, CDR3 spectratypes, clonal-space stratification, clonal tracking across timepoints, rarefaction/extrapolation curves, overlap heatmaps, and clonotype-similarity networks.
- **Tools** — VDJtools (`PlotFancyVJUsage`, `RarefactionPlot`, `CalcSpectratype`); R `circlize` for chord diagrams and `iNEXT` for Hill-number rarefaction/extrapolation; Python `matplotlib`/`seaborn`/`networkx`/`rapidfuzz`.
- **Metric guidance** — Morisita-Horn (depth-robust overlap) vs. Jaccard (presence/absence); Hamming/Levenshtein for sequence-similarity networks; frequency-weighted vs. clonotype-weighted views.
- **Correct-comparison workflow** — clonotype definition → depth normalization → figure selection → metric choice → distance-threshold setting → interpretation at shared x-values with all parameters stated.

**Primary use cases**: TCR/BCR repertoire figure generation, depth-robust cross-sample overlap/diversity comparison, clonal tracking across timepoints.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally via Bash/R/Python rather than as an MCP server. The upstream skill front-matter name is `bio-tcr-bcr-analysis-repertoire-visualization`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/repertoire-visualization`. External dependencies: `matplotlib 3.8+`, `seaborn 0.13+`, `pandas 2.2+`, `numpy 1.26+`, R `circlize 0.4+`, R `iNEXT 3.0+`, and `VDJtools 1.2`. Upstream repertoire assembly is handled by `mixcr-analysis` (bulk) or `scirpy-analysis` (single-cell); diversity/overlap statistics by `vdjtools-analysis`. Upstream directory: `tcr-bcr-analysis/repertoire-visualization`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`tcr-bcr-analysis/repertoire-visualization/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/repertoire-visualization/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=repertoire-visualization&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Frepertoire-visualization.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
