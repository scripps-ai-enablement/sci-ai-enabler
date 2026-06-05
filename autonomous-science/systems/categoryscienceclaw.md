---
title: CategoryScienceClaw
parent: Systems
grand_parent: AI scientists
nav_order: 57
affiliation: MIT (Laboratory for Atomistic and Molecular Mechanics — Biological / Civil / Mechanical Engineering, Schwarzman College of Computing)
org_short: MIT
lifecycle_stages: [Multi-stage]
validation_type: Benchmark
autonomy: Semi-autonomous
domain: Materials science / mechanics
domain_group: Chemistry & materials
availability: Open source
access: Open source
tagline: Discovery framework adding a category-theoretic, proof-carrying layer to ScienceClaw for verifiable transitions.
last_verified: 2026-06-05
---

# CategoryScienceClaw

Self-revising discovery framework that adds a category-theoretic, proof-carrying layer to the ScienceClaw agentic execution substrate so that regime transitions — schema changes admitting new evidence types — can be machine-verified and audited.

| | |
|---|---|
| **Affiliation** | MIT — Laboratory for Atomistic and Molecular Mechanics (Buehler group) |
| **First introduced** | 2026-05 (arXiv preprint) |
| **Lifecycle stages** | Multi-stage (hypothesis generation, simulation-based experiment design, analysis, with verified regime transitions) |
| **Autonomy level** | Semi-autonomous (typed skills, immutable artifacts, open needs, workflow mutation, gates, stress tests, and public discourse coordinated as a typed knowledge–computation graph) |
| **Domain focus** | Materials science / mechanics (protein-mechanics, fiber-network mechanics) |
| **Availability** | Open source |

## Approach

The paper develops a category-theoretic account of agentic scientific discovery. In a fixed regime, the system state is a copresheaf `Iₜ : Sb → Set` and provenance is the category of elements; **fixed-regime operation** is an endofunctorial update on such states. **Discovery** is instead a verified regime transition `u : Sb → Sb'` — old artifacts are preserved, transported by left Kan extension `Lan_u Iₜ`, and compared with the post-transition state to identify residual content beyond functorial transport. This distinguishes retrieval, search, and discovery without subjective novelty.

Two instantiations are presented. **Builder/Breaker** revises a protein-mechanics symbolic world model under a Minimum Description Length gate; the accepted law expresses within-chain flexibility as mode-conditioned compliance (all-mode elastic compliance conditioned by slow collective-mode participation). **CategoryScienceClaw** wraps the underlying ScienceClaw agentic execution substrate — where typed skills, immutable artifacts, open needs, workflow mutation, and public discourse form a knowledge–computation graph — with a categorical proof-carrying layer.

## Validation

A fiber-network mechanics worked example records candidate models, rejected alternatives, an AIC gate, perturbation tests, and an accepted **orientation-tensor anisotropic stiffness surrogate** that supersedes an isotropic fiber-count descriptor. Model selection itself — including the rejected alternative — is recorded as typed provenance.

The Builder/Breaker case study produces a 54.3-bit MDL gain on accumulated evidence; signed model-code changes confirm the discovery is genuine schema expansion rather than refit.

## Notable results

- First operational categorical account of self-revising AI scientific discovery, separating fixed-regime search from regime-extending discovery via Kan-extension transport.
- Builder/Breaker delivers a published mode-conditioned compliance law for protein mechanics, accepted under an MDL gate.
- Worked fiber-network example materializes accepted models, rejected alternatives, gates, stress tests, and regime-transition claims as typed artifacts and morphisms.

## Primary paper

[Wang & Buehler, "Self-Revising Discovery Systems for Science: A Categorical Framework for Agentic Artificial Intelligence," arXiv:2606.01444 (May 2026)](https://arxiv.org/abs/2606.01444).

## Other references

- [Buehler et al., "ScienceClaw × Infinite" (underlying agentic execution substrate), arXiv:2603.14312](https://arxiv.org/abs/2603.14312)

## Code

- [ScienceClaw](https://github.com/lamm-mit/scienceclaw) — base substrate.
- [Infinite](https://github.com/lamm-mit/infinite) — companion architectural layer.
- [CategoryScienceClaw mechanics branch](https://github.com/lamm-mit/scienceclaw/tree/categoryscienceclaw-mechanics) — the categorical layer demonstrated in the paper.
- [BreakingTheWorld](https://github.com/lamm-mit/BreakingTheWorld) — Builder/Breaker case study.
