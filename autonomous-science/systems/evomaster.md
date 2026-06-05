---
title: EvoMaster
parent: Systems
grand_parent: AI scientists
nav_order: 24
affiliation: Shanghai Jiao Tong University / SciLand / DP Technology
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: General
availability: Open source
last_verified: 2026-05-27
---

# EvoMaster

Foundational, domain-agnostic agent framework whose ~100-line harness lets developers build self-evolving scientific agents that iteratively refine hypotheses, self-critique, and accumulate experience across cycles; underpins the SciMaster ecosystem of domain agents.

| | |
|---|---|
| **Affiliation** | School of AI, Shanghai Jiao Tong University / SciLand / DP Technology ([Code](https://github.com/sjtu-sai-agents/EvoMaster)) |
| **First introduced** | 2026-04 (arXiv:2604.17406) |
| **Lifecycle stages** | Multi-stage |
| **Autonomy level** | Semi-autonomous |
| **Domain focus** | General (ML, physics, frontier scientific reasoning, web retrieval, embodied intelligence) |
| **Availability** | Open source |

## Approach

EvoMaster decouples execution into three orthogonal layers — **Playground** (orchestration of multi-agent collaboration and domain workflows), **Exp** (single-experiment lifecycle, task instantiation, trajectory recording), and **Agent** (the reasoning / tool-use loop). The Agent Engine drives a multi-turn reactive loop (`reason → invoke tools → observe → self-critique`) backed by a ContextManager that uses dynamic LLM-based summarization and sliding windows to sustain hundreds of experimental turns without context degradation. A Capability Layer exposes a Tool System over the Model Context Protocol, a hierarchical Skill System (metadata in-context, executable instructions loaded on demand), and an LLM abstraction across 100+ models.

Multi-agent collaboration is materialized through declarative `AgentSlots` and a `@register_playground` decorator; specialized roles (solver, critic, rewriter) maintain independent LLM and tool configs and support sequential handoffs, parallel exploration, and iterative peer-review patterns. YAML configuration manifests and a thread-safe JSON trajectory system act as a "lab notebook" for reproducibility. On top of this harness the authors built the **SciMaster** ecosystem: ML-Master / ML-Master 2.0 (autonomous ML), X-Master / X-Master 2.0 (general scientific research / frontier reasoning), Browse-Master (web retrieval), PhysMaster (physics reasoning), and EmboMaster (embodied intelligence training).

## Validation

Head-to-head on four benchmarks against OpenClaw (both using GPT-5.4 as the backend, identical tools/skills, 24-hour limit on MLE-Bench). The SciMaster agent configured for each benchmark is the EvoMaster instance evaluated.

## Notable results

- **MLE-Bench Lite: 75.8%** medal rate (vs. OpenClaw 18.2%, +316% relative); also above MLE-STAR-Pro-1.5 (68.18%) and R&D-Agent (68.18%). 17 of 22 Kaggle competitions earned medals.
- **HLE: 41.1%** (vs. 13.6%, +202%); **BrowseComp: 73.3%** (vs. 28.3%, +159%, with 100% on Map+Search); **FrontierScience: 53.3%** (vs. 18.3%, +191%; 55% physics, 55% chemistry, 50% biology).
- Six SciMaster agents released or in pipeline across ML, web retrieval, frontier scientific reasoning, physics, and embodied intelligence; first four are open-sourced.

## Primary paper

[Zhu, Cai, Liu et al., "EvoMaster: A Foundational Agent Framework for Building Evolving Autonomous Scientific Agents at Scale," arXiv:2604.17406](https://arxiv.org/abs/2604.17406).

## Other references

- [SciMaster project — ML-Master / X-Master ecosystem](https://github.com/sjtu-sai-agents/EvoMaster)

## Code

[Repository](https://github.com/sjtu-sai-agents/EvoMaster).
