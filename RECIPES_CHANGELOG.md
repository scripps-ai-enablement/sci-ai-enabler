---
title: Recipes updates
parent: Updates
nav_order: 4
permalink: /updates/recipes.html
---

# Recipes updates

Reverse-chronological log of changes to the [recipes cookbook](recipes/). Newest at the top.

<!-- Curator appends new dated entries directly below this line. -->

## 2026-05-21

### Added

- **Run first-pass QC on a single-cell RNA-seq dataset** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping Anthropic's `single-cell-rna-qc` skill for canonical scverse MAD-based filtering of 10x `.h5` / AnnData `.h5ad` inputs ([source](https://claude.com/resources/tutorials/how-to-use-the-single-cell-rna-qc-skill-with-claude)).
- **Run bulk RNA-seq differential expression from a counts matrix** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping the K-Dense PyDESeq2 skill for negative-binomial GLM differential expression, including pseudobulk single-cell handoff guidance ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/pydeseq2/SKILL.md)).
- **Build a target dossier from gene name to structure to cancer dependency** (Problem class: Knowledge synthesis; Evidence: Proposed) — first rung-3 toolbelt recipe composing Open Targets, UniProt, AlphaFold, and DepMap into a one-page target dossier; first `Proposed`-evidence entry in the cookbook ([closest analogue](https://doi.org/10.1101/2025.05.30.656746)).

### Updated

- **Triage a stack of new preprints in your field** — nav_order shifted from 1 to 4 to reflect alphabetical ordering after the three new Mol/Cell Bio additions; no content changes.

### Verified (no changes)

- 1 recipe spot-checked, current (`triage-new-preprints`, last_verified 2026-05-21).

## 2026-05-21 (initial seed)

### Added

- **Section bootstrap** — `recipes/` section created with landing page, landscape page, and the all-recipes index; `recipes/curator-state.md` initialized; `RECIPES_CHANGELOG.md` (this file) created. Curator prompt and daily workflow added at `RECIPE_AGENT.md` and `.github/workflows/recipes.yml`.
- **Triage a stack of new preprints in your field** (Problem class: Literature triage; Evidence: Reported) — first seed recipe demonstrating the schema and the lowest rung of the simplicity ladder (Claude Code alone + bioRxiv MCP) ([source](https://github.com/biorxiv/biorxiv-mcp)).
