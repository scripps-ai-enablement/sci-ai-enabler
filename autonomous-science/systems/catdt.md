---
title: CatDT
parent: Systems
grand_parent: AI scientists
nav_order: 56
affiliation: Hong Kong University of Science and Technology (IAS Center for AI for Scientific Discoveries; Chemistry, CSE, CBE)
org_short: HKUST
lifecycle_stages: [Multi-stage]
validation_type: Benchmark
autonomy: Semi-autonomous
domain: Chemistry / heterogeneous catalysis
domain_group: Chemistry & materials
availability: Code on request (release pending publication)
access: Code on request
tagline: Self-evolving multi-agent system that builds a condition-aware digital twin of a heterogeneous catalyst.
last_verified: 2026-06-05
---

# CatDT

Self-evolving multi-agent system that constructs an autonomous, condition-aware digital twin of a working heterogeneous catalyst from only a bulk crystal and a natural-language reaction description.

| | |
|---|---|
| **Affiliation** | HKUST (IAS Center for AI for Scientific Discoveries; Departments of Chemistry, CSE, and Chemical & Biological Engineering) |
| **First introduced** | 2026-06 (arXiv preprint) |
| **Lifecycle stages** | Multi-stage (facet weighting, surface reconstruction, pathway enumeration, transition-state location, microkinetics) |
| **Autonomy level** | Semi-autonomous (5–30 min single-GPU runs from bulk crystal + reaction description; no manual intervention at intermediate links) |
| **Domain focus** | Chemistry / heterogeneous catalysis (gas–solid and liquid–solid) |
| **Availability** | Code on request — repository announced for release at github.com/AI4QC/catdt upon publication |

## Approach

Eight specialized agents coordinate 27 scientific tools to predict stable facets, reconstruct surfaces under operating conditions, enumerate and rank reaction pathways, locate transition states, and compute kinetics. Two innovations address the system's hardest steps. **UniMech** identifies dominant pathways for novel materials and under-explored reactions by fusing agent-guided proposals with energy-cached graph search over autonomously constructed reaction networks, operating at over 10³× lower cost than exhaustive enumeration. A **memory-augmented reinforcement loop** lifts barrier-calculation success from 41% to 84% across 600 diverse catalytic surfaces by learning to construct better initial and final states and path interpolations across runs.

The authors frame the decisive factor for a faithful catalyst digital twin not as raw LLM capability but as the engineered harness around it: deterministic tools, persistent memory, and verified self-improvement that compound across foundation-model upgrades, new tools, and runs.

## Validation

Seven gas–solid benchmarks: stepped metals, single-atom catalysts, ordered intermetallics, vacancy-rich 2D sulfides, 2D carbides, and a strong-metal–support-interaction (SMSI) interface. Every CatDT prediction lies between **0.5× and 2× experimental values** across measurements spanning four orders of magnitude.

## Notable results

- Barrier-calculation success across 600 diverse catalytic surfaces improved from 41% to 84% via the memory-augmented reinforcement loop.
- UniMech finds dominant pathways at >10³× lower cost than exhaustive enumeration.
- For propane dehydrogenation, CatDT independently discovered non-precious catalyst candidates rivaling the Pt-based industrial benchmark; the proposed **Ni@ZrO₂ SMSI overlayer reached a simulated TOF of 1.63 s⁻¹ at ~100% selectivity**.

## Primary paper

[Song, Zhang, Cheng, "Autonomous heterogeneous catalyst discovery with a self-evolving multi-agent digital twin," arXiv:2606.05050 (Jun 2026)](https://arxiv.org/abs/2606.05050).

## Other references

_None._

## Code

Announced release at [github.com/AI4QC/catdt](https://github.com/AI4QC/catdt) upon publication. RL-training trajectories, a 569-species thermodynamic-correction database, and CP-aware pretrained model parameters announced for release on Hugging Face upon publication.
