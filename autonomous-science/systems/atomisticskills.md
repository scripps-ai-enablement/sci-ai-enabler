---
title: AtomisticSkills
parent: Systems
grand_parent: AI scientists
nav_order: 44
affiliation: MIT (Gómez-Bombarelli and Coley groups), with Kookmin University, Harvard, and Shell
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Materials / chemistry / drug discovery (atomistic simulation)
availability: Open source
last_verified: 2026-05-31
---

# AtomisticSkills

Open-source agent harness that empowers general-purpose AI coding agents to conduct atomistic research across materials science, chemistry, and drug discovery through a library of more than 100 curated skills and tools.

| | |
|---|---|
| **Affiliation** | MIT Department of Materials Science and Engineering and Department of Chemical Engineering, with Kookmin University, Harvard, MIT Nuclear Science and Engineering, and Shell |
| **First introduced** | 2026-05 (arXiv:2605.24002) |
| **Lifecycle stages** | Multi-stage (literature review, research planning, simulation execution, MLIP benchmarking and fine-tuning, analysis) |
| **Autonomy level** | Semi-autonomous — general-purpose coding agents orchestrate skills end-to-end under user direction |
| **Domain focus** | Atomistic research: materials science (53 skills), chemistry (23), drug discovery (18), machine learning (14), general (11) |
| **Availability** | Open source |

## Approach

AtomisticSkills hierarchically decomposes scientific workflows for general-purpose coding agents into three layers:

- **MCP tool box** — fundamental research tools exposed via the Model Context Protocol (database queries, simulation engines such as FairChem, MatGL, MACE, Atomate2, ORCA, DiffCSP, MatterGen, structure visualization).
- **Skill library** — mid-level, semi-flexible atomistic research procedures (e.g., `mat-amorphization`, `mat-stability`, `mat-diffusion-analysis`, `ml-foundation-potentials`, `general-molecular-dynamics`) each composed of MCP tools plus declarative SKILL.md specifications.
- **Standards and rules** — research, skill, and workflow standards that constrain agent behavior toward reproducible and rigorous practice.

The framework is plug-and-play across coding agents and is designed to be extensible: new skills and MCP servers can be added without modifying the agent.

## Validation

The authors validate functional coverage against the scientific literature and demonstrate orchestration across six campaigns:

- Generative design of Li-ion solid-state electrolytes.
- High-throughput screening of metal-organic frameworks for CO2 capture.
- Autonomous MLIP benchmarking and fine-tuning.
- Multi-stage structure-based virtual screening for drug design.
- Multimodal X-ray diffraction pattern analysis.
- Screening of Fe-oxide catalysts for the oxygen evolution reaction.

## Notable results

- More than 100 human-curated multidisciplinary skills spanning database access, thermodynamics and kinetics modeling, MLIP-based and DFT-based simulation engines.
- Successful end-to-end orchestration of six independent atomistic campaigns by general-purpose coding agents, including an autonomous MLIP fine-tuning loop.
- Positioned as critical agent infrastructure toward fully autonomous AI scientists in atomistic domains.

## Primary paper

[Deng et al., "Harnessing AtomisticSkills for Agentic Atomistic Research," arXiv:2605.24002 (2026)](https://arxiv.org/abs/2605.24002).

## Other references

_None yet._

## Code

Described as open source by the authors; repository location to be confirmed.
