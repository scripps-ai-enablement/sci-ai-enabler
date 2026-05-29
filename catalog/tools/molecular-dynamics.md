---
title: Molecular Dynamics (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Drug Repurposing and Discovery]
last_verified: 2026-05-27
summary: Claude skill that runs and analyzes OpenMM molecular dynamics simulations and MDAnalysis trajectory analyses for proteins, ligands, and biomolecular complexes.
---

# Molecular Dynamics (Claude Skill)

Claude skill that sets up, runs, and analyzes molecular dynamics simulations end-to-end — OpenMM for the simulation engine and MDAnalysis for trajectory post-processing.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) |
| **Availability** | GA — distributed via the K-Dense `claude-scientific-skills` plugin marketplace |
| **Pricing** | Free / OSS (skill source); OpenMM is MIT, MDAnalysis is GPLv2+ |
| **Capabilities** | Read/Write — Claude writes and runs Python locally (system preparation, MD execution, trajectory analysis) |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install molecular-dynamics@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/molecular-dynamics ~/.claude/skills/
  pip install openmm MDAnalysis
  ```
  Project-scoped alternative: copy into `.claude/skills/` (inside your project) instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- **System preparation** — protein and small-molecule loading, solvation, ion placement, force-field assignment (AMBER, CHARMM, OPLS via OpenMM-compatible parameter sets)
- **Simulation** — energy minimization, NVT/NPT equilibration, production MD with checkpointing
- **Trajectory analysis** (MDAnalysis) — RMSD, RMSF, radius of gyration, contact maps, hydrogen-bond analysis, free-energy surfaces via PCA / order parameters
- **Visualization hooks** — outputs PDB / DCD / XTC that downstream PyMOL or ChimeraX sessions can consume (see also [Molecule-MCP](molecule-mcp.html))

**Primary use cases**: protein-stability assessment, ligand-binding-pose refinement and MM/PBSA-style scoring, conformational-ensemble generation for drug-discovery targets, biophysics teaching workflows.

## Notes

- **Compute-heavy.** Production MD assumes a CUDA-capable GPU; OpenMM's CPU platform works for small systems and tutorials. Cloud GPU runs are the typical pattern.
- **Skill is documentation plus Python recipes** — Claude executes OpenMM and MDAnalysis locally via Bash/Python. The skill does not ship binaries.
- Complements the [AlphaFold MCP Server](alphafold.html) and [PDB MCP Server](pdb.html) for structure retrieval, and [Molecule-MCP](molecule-mcp.html) for PyMOL/ChimeraX/GROMACS visualization and execution.

## Sources

- [`scientific-skills/molecular-dynamics/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/molecular-dynamics/SKILL.md)
- [K-Dense scientific-skills catalog](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/docs/scientific-skills.md)
- [OpenMM](https://openmm.org/)
- [MDAnalysis](https://www.mdanalysis.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=molecular-dynamics&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmolecular-dynamics.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
