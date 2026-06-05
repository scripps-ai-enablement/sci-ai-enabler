---
title: COBRApy (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Molecular and Cellular Biology, Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-06-04
summary: Claude skill driving COBRApy for constraint-based metabolic modelling — FBA, FVA, gene knockouts, flux sampling, gapfilling on SBML genome-scale models.
---

# COBRApy (Claude Skill)

Claude skill that drives [COBRApy](https://cobrapy.readthedocs.io/) for **constraint-based reconstruction and analysis (COBRA)** of genome-scale metabolic models — flux balance analysis, flux variability analysis, gene/reaction knockouts, flux sampling, and gapfilling on SBML / JSON / YAML models.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS); COBRApy maintained by the [`opencobra/cobrapy`](https://github.com/opencobra/cobrapy) project |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS skill (MIT collection); COBRApy itself is GPL-2.0-licensed — review license terms for commercial use |
| **Capabilities** | Read/Write — Claude executes COBRApy via Python/Bash to load models, run optimisation, and produce flux distributions / knockout screens |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `cobrapy` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/cobrapy ~/.claude/skills/
  pip install cobra
  ```

Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- **Model I/O** — load and save SBML / JSON / YAML genome-scale models; inspect reactions, metabolites, genes, gene-protein-reaction (GPR) associations
- **Flux balance analysis (FBA)** — `optimize()`, `slim_optimize()`, parsimonious FBA (pFBA), geometric FBA; biomass / ATP / metabolite-production objectives
- **Flux variability analysis (FVA)** — including loopless FVA when thermodynamic feasibility matters, with `fraction_of_optimum` control to explore suboptimal space
- **Knockout screens** — single and double gene/reaction deletions, parallelised for double deletions
- **Flux sampling** — Markov-chain Monte Carlo sampling of the solution polytope, with validation utilities
- **Production envelopes** — trade-off curves between biomass and product flux for metabolic-engineering design
- **Gapfilling and model refinement** — identify minimal reaction sets that restore feasibility against a target medium / objective
- **Context managers** — apply temporary model changes (`with model: …`) so state reverts automatically

**Primary use cases**: Systems-biology phenotype prediction, metabolic-engineering strain design (yield / titre / rate optimisation), drug-target identification via essentiality analysis, host-microbiome interaction modelling, integration of expression / proteomics constraints into genome-scale models.

## Notes

Solver backends are pluggable via `model.solver` — defaults to GLPK, with CPLEX and Gurobi recommended for large genome-scale models or heavy sampling workloads. Skill is documentation plus Python recipes — Claude calls COBRApy locally via Bash/Python. Pairs naturally with the `scanpy`, `pydeseq2`, and `gget` entries when integrating omics data into constraint-based models, and with `chembl` / `pubchem` when mapping flux solutions to chemistry-side targets.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/cobrapy/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/cobrapy/SKILL.md)
- [COBRApy documentation](https://cobrapy.readthedocs.io/)
- [`opencobra/cobrapy` on GitHub](https://github.com/opencobra/cobrapy)
- [Ebrahim et al., *BMC Syst. Biol.* 2013 — COBRApy](https://bmcsystbiol.biomedcentral.com/articles/10.1186/1752-0509-7-74)
- [Playbooks: cobrapy skill](https://playbooks.com/skills/k-dense-ai/claude-skills/cobrapy)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cobrapy&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcobrapy.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
