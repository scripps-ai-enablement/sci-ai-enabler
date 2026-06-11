---
title: PyTDC (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Drug Repurposing and Discovery, Chemistry, Translational Medicine]
last_verified: 2026-06-04
summary: Claude skill driving PyTDC for Therapeutics Data Commons benchmarks — ADMET, drug-target / drug-drug interactions, drug response, molecular generation, retrosynthesis.
---

# PyTDC (Claude Skill)

Claude skill that drives [PyTDC](https://tdcommons.ai/), the Python client for **Therapeutics Data Commons** — a curated benchmark suite of drug-discovery ML datasets spanning ADMET prediction, drug-target interaction, drug-drug interaction, drug-response prediction, molecular generation, and retrosynthesis.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS); PyTDC by Harvard [mims-harvard/TDC](https://github.com/mims-harvard/TDC) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS skill (MIT collection); PyTDC itself is MIT-licensed; TDC datasets follow per-dataset licenses |
| **Capabilities** | Read/Write — Claude executes PyTDC via Python/Bash to load datasets, run benchmarks, and call generation oracles |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/structural-biology-drug-discovery/pytdc-therapeutics-data-commons` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `pytdc` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/pytdc ~/.claude/skills/
  pip install pytdc
  ```

Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- Single-instance prediction (`single_pred`) — ADMET, toxicity, quantum properties, paratope, epitope
- Multi-instance prediction (`multi_pred`) — drug-target interaction (DTI), drug-drug interaction (DDI), GDA, drug response, PPI
- Generation (`generation`) — de-novo molecular generation, retrosynthesis, reaction yield, paired generation
- Bundled helper scripts: `load_and_split_data.py`, `benchmark_evaluation.py`, `molecular_generation.py`
- Reference docs: `datasets.md`, `oracles.md` (17+ molecule-generation oracles incl. QED, SA, DRD2, GSK3B, JNK3), `utilities.md`
- Standard data splits (random, scaffold, cold-start), leaderboard metrics, and TDC benchmark suites (`ADMET_Group`, `DTI_DG_Group`, `Drug_Response_Group`)

**Primary use cases**: Benchmarking ML models for drug discovery, ADMET property prediction, drug-target interaction screening, molecular generation with property oracles, retrosynthesis evaluation.

## Notes

Pairs with the `deepchem`, `medchem`, `datamol`, `rdkit-skill`, and `molfeat` entries — PyTDC supplies labelled benchmark splits while those skills supply featurizers and models. Some TDC datasets auto-download on first use (a few GB total across the full suite); allow disk space and network access. Skill is documentation plus Python recipes — Claude calls PyTDC locally via Bash/Python.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/pytdc/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/pytdc/SKILL.md)
- [Therapeutics Data Commons](https://tdcommons.ai/)
- [`mims-harvard/TDC`](https://github.com/mims-harvard/TDC)
- [Huang et al. *NeurIPS Datasets and Benchmarks* 2021](https://arxiv.org/abs/2102.09548)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pytdc&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpytdc.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
