---
title: Arboreto (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Molecular and Cellular Biology, Drug Repurposing and Discovery]
last_verified: 2026-05-28
summary: Claude skill for gene-regulatory-network inference with Arboreto — GRNBoost2 / GENIE3 tree-based regression over bulk or single-cell expression, distributed via Dask.
---

# Arboreto (Claude Skill)

Claude skill that drives [Arboreto](https://arboreto.readthedocs.io/) for gene-regulatory-network (GRN) inference — fitting GRNBoost2 or GENIE3 regression models that identify transcription-factor → target-gene relationships from bulk or single-cell expression data.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS skill (MIT collection); Arboreto itself is BSD-3 |
| **Capabilities** | Read/Write — Claude executes Arboreto via Python/Bash; Dask handles parallelism |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install arboreto@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/arboreto ~/.claude/skills/
  pip install arboreto
  ```

Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- GRNBoost2 — gradient-boosting GRN inference with self-tuning early stopping (the recommended default)
- GENIE3 — classical random-forest GRN inference for reproducing legacy analyses
- TF-restricted inference using a curated transcription-factor list
- Single-cell GRN inference (compatible with pySCENIC pre-processing)
- Distributed execution via Dask — single machine to multi-node clusters
- Importance-threshold filtering and ranking of TF–target edges

**Primary use cases**: Transcription-factor regulon discovery, single-cell GRN inference as a step in pySCENIC pipelines, regulator prioritisation for target-discovery and drug-repurposing studies.

## Notes

Pairs with the `scanpy`, `pydeseq2`, and `cellxgene-census` skills — Arboreto consumes the (cells × genes) expression matrix produced by upstream QC. The Python script must include the standard `if __name__ == "__main__":` guard because Dask spawns child processes. Skill is documentation plus Python recipes — Claude calls Arboreto locally via Bash/Python.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`scientific-skills/arboreto/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/arboreto/SKILL.md)
- [Arboreto documentation](https://arboreto.readthedocs.io/)
- [Moerman et al. *Bioinformatics* 2019 (GRNBoost2)](https://academic.oup.com/bioinformatics/article/35/12/2159/5184284)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=arboreto&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Farboreto.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
