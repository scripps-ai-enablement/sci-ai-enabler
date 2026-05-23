---
title: AI co-mathematician
parent: Systems
grand_parent: AI scientists
nav_order: 3
affiliation: Google DeepMind
lifecycle_stages: [Multi-stage, Writing]
autonomy: Semi-autonomous
domain: Mathematics
availability: Closed / limited release
last_verified: 2026-05-23
---

# AI co-mathematician

Google DeepMind agentic workbench for open-ended mathematics research that orchestrates a project-coordinator agent and parallel workstreams across ideation, literature search, computational exploration, theorem proving, and theory building, with stateful tracking of failed hypotheses.

| | |
|---|---|
| **Affiliation** | Google DeepMind ([paper](https://arxiv.org/abs/2605.06651)) |
| **First introduced** | 2026-05 (arXiv:2605.06651, v2 2026-05-13) |
| **Lifecycle stages** | Multi-stage (ideation → computational exploration → proof → theory building), with native authored "working paper" artifact |
| **Autonomy level** | Semi-autonomous (interactive, asynchronous; user can intervene at any time, agents request human help when stalled) |
| **Domain focus** | Mathematics research |
| **Availability** | Closed — described as a "limited initial release" at preprint time |

## Approach

A workbench layered on top of Gemini language models. A top-level project-coordinator agent opens an interactive onboarding dialogue with the user to refine the research question and approve high-level goals before any work is delegated. Per-goal workstream coordinators run linear sequences of actions and dispatch specialized sub-agents (including Gemini Deep Think) for ideation, literature search, computational exploration, and proof attempts; agents communicate asynchronously over an internal messaging system and write to a shared workspace file system. The system centers its outputs on a living "working paper" rather than chat logs, with inline highlights and margin notes that record provenance, contentious claims, and stalled reasoning. Uncertainty is treated as a first-class state to be managed (version history, continuous review loops, systematic citation checking); failed explorations are preserved as durable first-class outcomes rather than discarded. The harness is designed to be model-agnostic and to host external engines such as AlphaEvolve, AlphaProof, and Aletheia inside its interactive loop.

## Validation

Two complementary regimes. (1) Qualitative early-access deployment with practicing mathematicians, who used the system to steer open-ended research on problems including upper bounds for variants of the moving-sofa problem; the paper reports examples of solving open problems, surfacing new research directions, and uncovering overlooked literature. (2) Independent benchmark evaluation on FrontierMath: Epoch AI administered Tier 4 to the system in final-answer mode.

## Notable results

- 48% on FrontierMath Tier 4 (Epoch AI evaluation), reported in the paper as a new high score among AI systems evaluated on this tier.
- Documented walkthrough of programmatic constraints and adversarial review loops that prevent the system from taking the easy path on intractable problems while running multi-day parallel workstreams.

## Primary paper

[Zheng et al., "AI co-mathematician: Accelerating mathematicians with agentic AI," arXiv:2605.06651](https://arxiv.org/abs/2605.06651).

## Other references

_None yet._

## Code

Not released — the paper describes the system as subject to a "limited initial release," with broader productization stated as a future goal.
