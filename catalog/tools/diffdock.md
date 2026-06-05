---
title: DiffDock (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-06-04
summary: Claude skill driving DiffDock, a diffusion-based deep-learning docker that predicts protein–ligand binding poses from PDB plus SMILES with per-pose confidence scores.
---

# DiffDock (Claude Skill)

Claude skill that drives [DiffDock](https://github.com/gcorso/DiffDock) — a diffusion-generative model that predicts 3D protein–ligand binding poses directly from a protein structure (PDB) and a ligand SMILES, without exhaustive grid search.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS); DiffDock model from [`gcorso/DiffDock`](https://github.com/gcorso/DiffDock) (MIT) |
| **Availability** | GA — actively maintained in the K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS skill (MIT); DiffDock model weights MIT |
| **Capabilities** | Read/Write — Claude executes DiffDock locally via Python/Bash; writes generated poses (SDF / PDB) and confidence CSVs to disk |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `diffdock` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/diffdock ~/.claude/skills/
  git clone https://github.com/gcorso/DiffDock.git
  cd DiffDock && conda env create --file environment.yml && conda activate diffdock
  ```
  Project-scoped alternative: copy into `.claude/skills/` (inside your project) instead of `~/.claude/skills/`. DiffDock itself ships as a separate conda environment; the skill's `setup_check.py` validates Python, PyTorch + CUDA, PyTorch Geometric, RDKit, and ESM before any docking run.

## What it does

`SKILL.md` plus assets (`batch_template.csv`, `custom_inference_config.yaml`), references (`confidence_and_limitations.md`, `parameters_reference.md`, `workflows_examples.md`), and scripts (`analyze_results.py`, `prepare_batch_csv.py`, `setup_check.py`) with recipes for:

- **Pose generation** — take a protein PDB and a ligand SMILES, generate N diffusion-sampled binding poses (default 10–40) with per-pose confidence scores
- **Virtual screening** — batch many ligands against one protein via `prepare_batch_csv.py`; rank by confidence
- **Pose analysis** — `analyze_results.py` filters, clusters, and exports top-K poses as SDF / PDB for downstream MM/PBSA or visualization
- **Workflow handoff** — confidence-filtered poses feed `molecular-dynamics` for refinement, `deepchem` / `medchem` for re-scoring, and `molecule-mcp` (PyMOL / ChimeraX) for visualization

**Primary use cases**: blind docking against AlphaFold-predicted targets, lead-optimization pose prediction, virtual screening pre-filter ahead of MM/PBSA or FEP, allosteric-site exploration when binding pockets are uncertain.

## Notes

- **Poses only, not affinity.** DiffDock predicts binding geometry and a confidence score, **not** binding affinity (ΔG, K_d). Pair with GNINA / Vina / MM-GBSA / FEP for affinity ranking — the SKILL.md is explicit about this.
- **GPU strongly recommended.** Diffusion sampling on CPU is slow; the upstream environment ships with CUDA-pinned PyTorch. The K-Dense `molecular-docking` workflow example chains DiffDock with DeepChem rescoring and MedChem filtering.
- **Confidence interpretation.** Per `confidence_and_limitations.md`, confidence > 0 typically indicates a high-quality pose; confidence < -1.5 is unreliable. Always inspect top-K visually.
- Pairs with the [molecular-dynamics](molecular-dynamics.html), [molecule-mcp](molecule-mcp.html), [alphafold](alphafold.html), [pdb](pdb.html), and [deepchem](deepchem.html) catalog entries. The skill is documentation plus Python recipes — Claude drives DiffDock locally via Bash/Python; the skill does not ship binaries.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/diffdock/SKILL.md`](https://github.com/K-Dense-AI/claude-skills/blob/main/skills/diffdock/SKILL.md)
- [DiffDock — `gcorso/DiffDock`](https://github.com/gcorso/DiffDock)
- [Corso et al., *ICLR* 2023 — DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking](https://arxiv.org/abs/2210.01776)
- [Playbooks: diffdock skill](https://playbooks.com/skills/k-dense-ai/claude-skills/diffdock)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=diffdock&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdiffdock.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
