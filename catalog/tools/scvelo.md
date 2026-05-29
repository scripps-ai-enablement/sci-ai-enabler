---
title: scVelo (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Molecular and Cellular Biology, Neuroscience]
last_verified: 2026-05-28
summary: Claude skill for RNA-velocity analysis with scVelo — estimates cell-state transitions from unspliced/spliced mRNA counts, infers trajectories, latent time, and driver genes.
---

# scVelo (Claude Skill)

Claude skill that drives [scVelo](https://scvelo.readthedocs.io/) for RNA-velocity analysis — estimating directed cell-state transitions from unspliced/spliced mRNA dynamics in single-cell RNA-seq data.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS skill (MIT collection); scVelo itself is BSD-3 |
| **Capabilities** | Read/Write — Claude executes scVelo via Python/Bash |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install scvelo@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/scvelo ~/.claude/skills/
  pip install scvelo
  ```

Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- Preprocessing unspliced/spliced counts from loom / velocyto / STARsolo / Kallisto-bustools outputs
- Steady-state, stochastic, and dynamical velocity models
- Velocity-embedding projections onto UMAP / t-SNE
- Latent-time inference and driver-gene identification
- Velocity confidence and coherence scoring
- Trajectory and lineage analysis paired with PAGA

**Primary use cases**: Mapping differentiation trajectories, identifying lineage-decision genes, dynamics analysis in development and disease, ordering cells by inferred latent time.

## Notes

Pairs with the catalog's `scanpy`, `anndata`, `cellxgene-census`, and `scvi-tools` skills for end-to-end single-cell trajectory workflows. RNA-velocity requires upstream alignment that emits spliced + unspliced count matrices (velocyto, kallisto-bustools, or STARsolo Velocyto mode) — scVelo cannot recover velocities from a counts-only AnnData. Skill is documentation plus Python recipes — Claude calls scVelo locally via Bash/Python.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`scientific-skills/scvelo/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/scvelo/SKILL.md)
- [scVelo documentation](https://scvelo.readthedocs.io/)
- [Bergen et al. *Nat Biotechnol* 2020](https://www.nature.com/articles/s41587-020-0591-3)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=scvelo&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fscvelo.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
