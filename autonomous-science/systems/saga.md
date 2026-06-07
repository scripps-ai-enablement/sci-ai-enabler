---
title: SAGA
parent: Systems
grand_parent: AI scientists
nav_order: 42
affiliation: Cornell University; Ohio State University; Yale University; Simon Fraser University; EPFL; UC Berkeley; Northeastern University; Broad Institute of MIT and Harvard; MIT; Wyss Institute; Whitehead Institute; Deep Principle; Georgia Tech; and others
org_short: Cornell + multi
lifecycle_stages: [Multi-stage]
validation_type: Wet-lab
autonomy: Semi-autonomous
domain: Scientific design (antibiotics, nanobodies, DNA sequences, materials, chemical processes)
domain_group: General / multi-domain
availability: Open source — MIT license (github.com/btyu/SAGA)
access: Open source
tagline: Bi-level agent that autonomously evolves the objective functions of a scientific design problem rather than treating them as fixed.
last_verified: 2026-06-07
---

# SAGA

The Scientific Autonomous Goal-evolving Agent (SAGA) is a bi-level multi-agent system that automates the design of a scientific problem's objective functions, evolving what to optimize for rather than treating the objectives as fixed inputs.

| | |
|---|---|
| **Affiliation** | Cornell, Ohio State, Yale, Simon Fraser, EPFL, UC Berkeley, Northeastern, Broad Institute, MIT, Deep Principle, Georgia Tech, and others ([code](https://github.com/btyu/SAGA)) |
| **First introduced** | 2025-12 (arXiv:2512.21782) |
| **Lifecycle stages** | Multi-stage |
| **Autonomy level** | Semi-autonomous — runs fully autonomous (autopilot) or with human steering of the planner/analyzer (co-pilot, semi-pilot) |
| **Domain focus** | Scientific design across biology, chemistry, and materials science |
| **Availability** | Open source — MIT license |

## Approach

SAGA targets a failure mode of objective-driven discovery agents: optimizers exploit the gap between a fixed scalar objective and reality, producing high-scoring but undesirable candidates, while the right set of objectives is rarely known upfront. SAGA reframes objective formulation as itself an iterative search problem and automates it with a **bi-level architecture**. An **outer loop** of four LLM agentic modules — a **Planner** that proposes new objectives from the task goal and current progress, an **Implementer** that compiles proposed objectives into executable scoring functions (e.g., generating RDKit-based scorers), an **Optimizer** that searches for candidate hypotheses maximizing the current objectives, and an **Analyzer** that examines optimization results and identifies failure modes — systematically explores the space of objectives and their trade-offs. An **inner loop** inside the Optimizer runs any optimization strategy (genetic algorithms, RL-based search) to evolve candidates under the current objectives.

The framework supports three automation levels: **co-pilot** (scientists collaborate with both Planner and Analyzer), **semi-pilot** (feedback only to the Analyzer), and **autopilot** (analysis and planning fully automated). Because what to optimize for is itself a scientific hypothesis, the system spans hypothesis/goal formulation, candidate/solution design, and result analysis.

## Validation

Demonstrated across five design domains — antibiotics, nanobodies, functional DNA sequences (enhancers/promoters), inorganic materials, and chemical-process flowsheets — with both in-silico evaluation and genuine wet-lab confirmation in the biology tasks. Antibiotic candidates were scored on antibacterial activity, novelty, safety, drug-likeness (QED), and synthesizability (SA); inorganic-material properties were validated by DFT.

## Notable results

- **Antibiotics:** discovered a structurally novel hit (Tanimoto distance >0.7 from all known antibiotics) with experimentally validated antibacterial activity against *E. coli* and no cytotoxicity in human cell lines.
- **Nanobodies:** experimentally confirmed three de novo PD-L1 binders (K_D 300–400 nM); the autonomously evolved composite scoring function separated binders from non-binders (p = 0.03) where no single in-silico metric did.
- **Functional DNA:** proposed cell-type-specific HepG2 enhancers with ~50% improvement over the best baseline; designed DFT-validated permanent magnets and superhard materials.

## Primary paper

[Du, Yu, Liu, Shen, Chen, Rittig, Sun, Zhang et al., "Accelerating Scientific Discovery with Autonomous Goal-evolving Agents," arXiv:2512.21782 (2026)](https://arxiv.org/abs/2512.21782).

## Other references

_None yet._

## Code

[Repository](https://github.com/btyu/SAGA) — MIT license.
