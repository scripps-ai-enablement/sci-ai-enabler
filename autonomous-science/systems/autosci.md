---
title: AutoSci
parent: Systems
grand_parent: AI scientists
nav_order: 52
affiliation: Peking University (PKUDAIR)
lifecycle_stages: [Multi-stage, Writing]
autonomy: Fully autonomous
domain: General (case studies in GPU kernel optimization and biomedical drug discovery)
availability: Open source
last_verified: 2026-06-02
---

# AutoSci

Memory-centric agentic system that executes the full scientific research lifecycle — literature understanding, ideation, experimentation, manuscript writing, and rebuttal — over a schema-governed persistent memory and evolves its own skills and templates across projects.

| | |
|---|---|
| **Affiliation** | Peking University, Data and Intelligence Research (PKUDAIR), Beijing |
| **First introduced** | 2026-05 (arXiv:2605.31468) |
| **Lifecycle stages** | Multi-stage (literature → ideation → experiment → writing → rebuttal), with Writing as a downstream stage |
| **Autonomy level** | Fully autonomous over the five-stage lifecycle; trust-guarded memory writes use an independent reviewer agent |
| **Domain focus** | General — case studies in GPU kernel optimization and biomedical drug discovery |
| **Availability** | Open source — [github.com/skyllwt/AutoSci](https://github.com/skyllwt/AutoSci) |

## Approach

AutoSci is organized around four interlocking modules. **SciMem** is a schema-governed persistent research memory split into two regions: a Long-Term Knowledge Memory of typed entities (Topic, Paper, Foundation, Concept, Method, People) connected by 20+ typed relations into a navigable knowledge graph, and an Active Research Memory of project-level artifacts (Idea, Experiment, Manuscript, Review) carrying explicit lifecycle states. **SciFlow** is a harness-based lifecycle executor that runs over SciMem with more than 30 research skills spanning the five stages, making long-horizon research interruptible, resumable, and reviewable rather than a stream of free-form agent conversations. **SciDAG** augments difficult stages with DAG-shaped multi-agent operators (generate, variation, debate, refine, review — 9 reusable operators) and reusable stage-specific templates. **SciEvolve** converts traces and feedback from users, experiments, and reviews into versioned updates to SciMem organization, SciFlow skills, and SciDAG templates.

All memory writes pass through a Trust Guard that checks schema/lifecycle/link validity (deterministic linting) and evidence-support/consistency (independent reviewer agent), assigning PASS / WARN / BLOCK. Blocked artifacts are quarantined until resolved, preventing memory errors from propagating across projects.

## Validation

Two end-to-end case studies covering GPU kernel optimization and biomedical drug discovery. Each produced reviewable paper-level artifacts that received automated ICLR-style review scores.

## Notable results

- AutoSci v1.0.0 implements 4 modules, 10 typed long-term entity types with 20+ typed relations, 30+ research skills across the five lifecycle stages, 9 reusable multi-agent operators, and 3 evolution skills.
- The GPU kernel optimization case study yielded an artifact with an automated ICLR-review score of **6.3/10**.
- The biomedical drug-discovery case study yielded an artifact with an automated ICLR-review score of **5.8/10**.

## Primary paper

[Qian, Xu, Xie, Fan, Tang et al., "AutoSci: A Memory-Centric Agentic System for the Full Scientific Research Lifecycle," arXiv:2605.31468 (2026)](https://arxiv.org/abs/2605.31468).

## Other references

_None yet._

## Code

[skyllwt/AutoSci](https://github.com/skyllwt/AutoSci) — released with the preprint.
