---
title: Qiushi Discovery Engine
parent: Systems
grand_parent: AI scientists
nav_order: 32
affiliation: Zhejiang University (Yang and Chen groups), with EPFL, China Jiliang University, and Hangzhou City University
lifecycle_stages: [Multi-stage]
autonomy: Fully autonomous
domain: Optics / photonics (free-space optical platform)
availability: Unknown
last_verified: 2026-05-21
---

# Qiushi Discovery Engine

LLM-based agentic system that performs end-to-end autonomous scientific discovery on a real free-space optical platform, combining nonlinear research phases, a Meta-Trace memory, and a dual-layer architecture to deliver experimentally supported nontrivial results.

| | |
|---|---|
| **Affiliation** | State Key Laboratory of Extreme Photonics and Instrumentation, Zhejiang University (Yang and Chen groups), with EPFL, China Jiliang University, and Hangzhou City University |
| **First introduced** | 2026-04 (arXiv:2604.27092) |
| **Lifecycle stages** | Multi-stage (Explore: literature interpretation, hypothesis generation, observable design; Execute: coding, simulation, physical measurement, data analysis; Express: figure construction, manuscript writing, critical review) |
| **Autonomy level** | Fully autonomous — given an open-ended research theme, the system sustains thousands of LLM-mediated reasoning, measurement, and revision actions against the physical platform |
| **Domain focus** | Optics / photonics — free-space optical platform with >2M-pixel SLM, scattering diffuser, and camera detection |
| **Availability** | Unknown (no public repository disclosed in primary paper) |

## Approach

Dual-layer multi-agent architecture. The core research agent system runs four role-specialized agents — Lead Investigator (global planning, hypothesis formation), Method Builder (theory-to-method translation, algorithm design), Experimentalist (simulation, code execution, measurement, analysis), and Critical Reviewer (adversarial evaluation) — that operate across three nonlinear phases (Explore, Execute, Express), with each Agent Step occupying one of 12 role-phase configurations rather than following a fixed pipeline. A support research agent system supplies context-isolated sub-agents for history review, retrieval, hypothesis exploration, trajectory tracking, and evidence verification, returning compressed, task-relevant outputs through structured interfaces. Meta-Trace distils each Agent Step into a structured unit of scientific know-how (attempt, finding, supporting evidence, limitations, artifacts, next-agent objective), preserving long-horizon scientific state without flooding the active context. An infrastructure layer couples the agents to a free-space optical platform (~2,200,000 SLM configurations) and a digital execution environment.

## Validation

Three progressively more demanding studies. (1) Autonomously reproduced a published transmission-matrix experiment on a non-original optical platform. (2) Converted an abstract coherence-order theory into experimentally testable transport observables and validated the predicted ordering relation using measured optical operators — claimed first experimental validation of this class of coherence-order structure. (3) An open-ended 206-step autonomous study over 1,288 minutes used 145.9 million tokens, 3,242 LLM calls, and 1,242 tool invocations, producing 163 research notes and 44 scripts.

## Notable results

- Identified and experimentally validated "optical bilinear interaction" — a previously unreported physical mechanism in which coherent scattering and square-law detection generate pairwise optical features, structurally analogous to bilinear query–key computation in Transformer attention.
- Authors claim this is the first demonstration of an AI agentic system autonomously proposing and experimentally validating a nontrivial physical mechanism in a real experimental environment.
- Suggests a route toward high-speed, energy-efficient optical hardware for pairwise computation.

## Primary paper

[Yang et al., "End-to-end autonomous scientific discovery on a real optical platform," arXiv:2604.27092](https://arxiv.org/abs/2604.27092).

## Other references

_None yet._

## Code

Not released.
