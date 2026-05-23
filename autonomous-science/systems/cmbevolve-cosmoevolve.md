---
title: CMBEvolve and CosmoEvolve
parent: Systems
grand_parent: AI scientists
nav_order: 11
affiliation: University of Cambridge (Institute of Astronomy / Kavli Institute for Cosmology / Cavendish Astrophysics)
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Cosmology and astrophysics
availability: Code on request
last_verified: 2026-05-23
---

# CMBEvolve and CosmoEvolve

Cambridge cosmology pair of agentic systems for autonomous scientific discovery: CMBEvolve performs LLM-guided scientific-code evolution via typed tree search, and CosmoEvolve simulates a virtual research laboratory with a principal-investigator agent and student-scientist agents coordinated through a shared blackboard.

| | |
|---|---|
| **Affiliation** | University of Cambridge — Institute of Astronomy, Kavli Institute for Cosmology, Cavendish Astrophysics ([paper](https://arxiv.org/abs/2605.14791)) |
| **First introduced** | 2026-05 (arXiv:2605.14791, dated 2026-05-14) |
| **Lifecycle stages** | Multi-stage (CMBEvolve: hypothesis + experiment design via code evolution; CosmoEvolve: closed-loop hypothesis → exploration → analysis over a shared lab state) |
| **Autonomy level** | Semi-autonomous (human supplies the task and dataset; CMBEvolve iterates a tree search to a fixed budget; CosmoEvolve runs an open-ended virtual lab with no predefined scientific objective in the ACT DR6 demonstration) |
| **Domain focus** | Cosmology — weak-lensing out-of-distribution detection, CMB / ACT DR6 data analysis |
| **Availability** | Code on request — paper states both packages "Will be made available publicly" |

## Approach

Two complementary systems for different scientific settings.

- **CMBEvolve** targets tasks with explicit quantitative objectives. The search is represented as a rooted tree where nodes have one of four types (task, idea generation and selection, code generation, code mutation). Each node stores search statistics (best score *S\**, visit count *N*) plus generated content and execution outputs; scores are backpropagated from leaves to the root after evaluation, updating ancestor statistics. The workflow cycles through idea generation, branch selection, targeted mutation, execution, scoring, and score backpropagation.
- **CosmoEvolve** targets open-ended scientific workflows. It simulates a virtual research laboratory consisting of one principal-investigator (PI) agent and a community of student-scientist agents. The PI observes a summary of the current lab state and selects from a discrete action space (group meeting, individual meeting, task assignment). Student agents carry out work independently and can dispatch subtasks to specialized sub-agents (data and file exploration, planning, code implementation). Agents share role-specific instructions, a compact skill index, persistent memory, and a shared lab-state blackboard; skills load on-demand and tool access is governed by per-agent allowlists.

## Validation

Two cosmological demonstrations. (1) CMBEvolve is applied to the FAIR Universe Weak Lensing ML Uncertainty Challenge out-of-distribution-detection task on simulated Hyper Suprime-Cam-style weak-lensing maps. (2) CosmoEvolve is applied to autonomous analysis of public ACT DR6 data products with **no predefined scientific objective**, asked to explore the data and propose analysis paths.

## Notable results

- CMBEvolve iteratively improves its benchmark score on weak-lensing OoD detection over successive code refinements during tree search.
- CosmoEvolve produced a beam-aware split-cross pseudo-Cℓ study of ACT DR6 temperature maps, finding percent-level within-channel stability, tighter same-band cross-array agreement at 90 GHz than at 150 GHz, and few-percent cross-frequency residuals consistent with effective-frequency and foreground-weighting differences.
- A related CosmoEvolve multi-frequency coherence analysis showed that no single multipole cut is appropriate for all ACT DR6 channel pairs, recommending pair- and scale-dependent stability windows — a non-trivial, analysis-grade diagnostic identified autonomously.

## Primary paper

[Xu & Borrett, "Beyond AI as Assistants: Toward Autonomous Discovery in Cosmology," arXiv:2605.14791](https://arxiv.org/abs/2605.14791).

## Other references

_None yet._

## Code

Not released at preprint time; both CMBEvolve and CosmoEvolve are stated as "Will be made available publicly."
