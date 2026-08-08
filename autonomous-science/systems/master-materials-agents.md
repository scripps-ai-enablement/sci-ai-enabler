---
title: MASTER
parent: Systems
grand_parent: AI scientists
nav_order: 30
affiliation: Los Alamos National Laboratory, Theoretical Division (Holby, Matanovic, Kort-Kamp) with the University of Connecticut
org_short: Los Alamos Nat. Lab
lifecycle_stages: [Multi-stage]
validation_type: Benchmark
autonomy: Semi-autonomous
domain: Chemistry and materials (electrocatalysis, density functional theory)
domain_group: Chemistry & materials
availability: Code on request
access: Code on request
tagline: Hierarchical LLM agents that design, run, and interpret DFT simulations in an active-learning loop for catalysis.
last_verified: 2026-08-08
---

# MASTER

Materials Agents for Simulation and Theory in Electronic-structure Reasoning: an active-learning framework in which LLM agents autonomously design, execute, and interpret density functional theory calculations to explore catalytic chemical space.

| | |
|---|---|
| **Affiliation** | Los Alamos National Laboratory, Theoretical Division, with the University of Connecticut ([paper](https://arxiv.org/abs/2512.13930)) |
| **First introduced** | 2025-12 (arXiv:2512.13930, dated 2025-12-15) |
| **Lifecycle stages** | Multi-stage (hypothesis about where to look → simulation design and execution → interpretation feeding the next choice) |
| **Autonomy level** | Semi-autonomous — humans set the chemical target and success criteria; agents choose, construct, repair, and interpret each calculation |
| **Domain focus** | Surface chemistry and electrocatalysis: CO adsorption on transition-metal adatoms on Cu(100), and on M–N–C single-atom catalysts |
| **Availability** | Code on request from the corresponding authors; supporting data in the Supplementary Information |

## Approach

MASTER splits the problem into a simulation layer and a reasoning layer. The **simulation layer** is a multimodal system that translates natural-language specifications ("build a Cu(100) slab 4×4 with 6 layers and 15 Å vacuum; place an Ag adatom at the fourfold hollow site; place a CO molecule C-down bonded atop the adatom; fix the bottom layers") into concrete DFT input geometries and workflows. A self-revision loop inspects the generated structure, diagnoses errors, and retries — addressing the standard bottleneck in which failed calculations require human intervention to repair.

The **reasoning layer** sits above it and decides which calculation to run next. Four strategies are compared: a single-agent baseline and three multi-agent designs — *peer review* (agents critique each other's proposals), *triage-ranking* (candidates are ranked and the top ones advanced), and *triage-forms* (structured elicitation of each agent's assessment). The framing is explicitly active learning: reasoning replaces trial-and-error enumeration over a chemical space of millions of configurations, and the paper's central claim is that the resulting trajectories are chemically motivated rather than an artifact of stochastic sampling or semantic similarity.

## Validation

Entirely in-silico. Two chemical applications — CO adsorption on transition-metal adatoms supported on Cu(100), and CO adsorption on M–N–C catalysts — with the geometry-generation subsystem benchmarked separately against subject-expert inspection across 18 representative transition-metal adatom configurations. Reasoning trajectories were audited against stochastic-sampling and semantic-bias null models.

## Notable results

- Reasoning-driven exploration reduced the number of atomistic simulations required to reach the chemical target by **up to 90%** relative to trial-and-error selection.
- The self-correcting simulation agents reached a **97.8% success rate** on adatom-only geometry construction, with most failures resolved on the first or second retry.
- Recorded reasoning traces showed chemically grounded decisions — e.g. correcting a CO molecule placed oxygen-down on an osmium adatom — that could not be reproduced by stochastic sampling or semantic-similarity baselines.

## Primary paper

[Rothfarb, Davis, Holby, Matanovic, Li, Kort-Kamp, "Hierarchical Multi-agent Large Language Model Reasoning for Autonomous Functional Materials Discovery," arXiv:2512.13930](https://arxiv.org/abs/2512.13930).

## Other references

_None yet._

## Code

Not publicly released — available from the corresponding authors upon reasonable request.
