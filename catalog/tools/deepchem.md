---
title: DeepChem (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-06-04
summary: Claude skill driving DeepChem for molecular machine learning — graph neural nets (GCN, GAT, MPNN, AttentiveFP), featurization, and the MoleculeNet benchmarks (toxicity, ADMET, quantum properties).
---

# DeepChem (Claude Skill)

Claude skill that drives [DeepChem](https://deepchem.io/), a deep-learning framework for **molecular machine learning** built on TensorFlow and PyTorch — graph neural networks for property prediction, featurization, pre-trained models, and the MoleculeNet benchmark suite.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS); DeepChem maintained by the [`deepchem/deepchem`](https://github.com/deepchem/deepchem) project |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS skill (MIT collection); DeepChem itself is MIT-licensed |
| **Capabilities** | Read/Write — Claude executes DeepChem via Python/Bash to featurize molecules, train models, and run MoleculeNet benchmarks |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `deepchem` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/deepchem ~/.claude/skills/
  pip install deepchem
  ```

Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- **Featurization** — molecular graphs, circular / Morgan fingerprints, 2D/3D descriptors, ConvMol, Weave, MolGraphConv
- **Graph neural networks** — GCN, GAT, MPNN, AttentiveFP, ChemBERTa, and pre-trained molecular foundation models for property prediction
- **MoleculeNet benchmarks** — 50+ curated datasets covering quantum-chemistry (QM7/QM8/QM9), physical-chemistry (ESOL, FreeSolv, Lipophilicity), biophysics (PCBA, MUV, HIV), and physiology (Tox21, ToxCast, SIDER, ClinTox, BBBP)
- **Workflows** — dataset loading, train/valid/test splits (random, scaffold, stratified), model training and hyperparameter optimization, model interpretation
- Integration with RDKit for chemical sanitization and feature extraction

**Primary use cases**: Toxicity prediction (Tox21, ClinTox, SIDER), ADMET property modeling, virtual-screening rank-ordering, binding-affinity prediction, quantum-property regression, blood-brain-barrier permeability classification.

## Notes

Pairs with the `pytdc`, `medchem`, `datamol`, `molfeat`, and `rdkit-skill` entries — DeepChem supplies models and MoleculeNet datasets while those skills supply orthogonal featurizers, filters, and benchmark splits. DeepChem auto-downloads benchmark datasets on first use (typically tens of MB to a few GB depending on dataset); allow disk and network access. TensorFlow / PyTorch backends are selectable per model class; GPU is optional but recommended for graph-neural-network training. Skill is documentation plus Python recipes — Claude calls DeepChem locally via Bash/Python.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/deepchem/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/deepchem/SKILL.md)
- [DeepChem project](https://deepchem.io/)
- [`deepchem/deepchem` on GitHub](https://github.com/deepchem/deepchem)
- [MoleculeNet benchmark](https://moleculenet.org/)
- [Wu et al., *Chem. Sci.* 2018 — MoleculeNet](https://pubs.rsc.org/en/content/articlelanding/2018/sc/c7sc02664a)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=deepchem&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdeepchem.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
