---
title: PerTurboAgent
parent: Systems
grand_parent: AI scientists
nav_order: 31
affiliation: Genentech / Tsinghua / Stanford (Hao, Lee, Wang, Scalia, Regev)
lifecycle_stages: [Experiment design, Analysis]
autonomy: Semi-autonomous
domain: Biology — single-cell perturbation screens (Perturb-seq)
availability: Unknown
last_verified: 2026-05-25
---

# PerTurboAgent

Self-planning LLM agent from Genentech (Regev lab) that designs iterative Perturb-seq experiments by picking, at each round, which gene perturbations to screen next — choosing among prediction, reflection, and refinement actions over expression data and prior knowledge.

| | |
|---|---|
| **Affiliation** | Genentech, Tsinghua University, Stanford University ([proceedings](https://proceedings.mlr.press/v311/hao25b.html)) |
| **First introduced** | 2025-05 (bioRxiv 2025.05.25.656020; PMLR v311 MLCB 2025 hao25b) |
| **Lifecycle stages** | Experiment design, Analysis — sequential gene-panel selection with in-loop analysis of control and perturbed gene-expression profiles |
| **Autonomy level** | Semi-autonomous — human supplies a target phenotype defined by associated descriptive genes (ADGs); the agent then plans, analyzes, and selects each round's perturbations |
| **Domain focus** | Single-cell biology, specifically pooled CRISPR Perturb-seq screens |
| **Availability** | Unknown — no code repository disclosed in the proceedings PDF |

## Approach

PerTurboAgent runs sequential rounds of Perturb-seq experiments. At each round it selects a set of m gene perturbations from the untested pool to maximize identification of "hit" perturbations — those that drive a strong expression change in the user-defined associated descriptive genes (ADGs) relative to control.

Within each round the agent operates as a multi-step planner with an explicit **Action Pool**:

- **Agent-based actions** — Prediction (new perturbation candidates), Reflection (review results stored in memory), Refinement (refine existing predictions).
- **Data-driven actions** — GSEA on control-cell expression; enrichment on positive- and negative-hit perturbation cells; enrichment on the negative-hit subset.
- **Prediction-model-driven actions** — train a perturbation-prediction ML model, query perturbation embeddings, compute phenotype scores.

An **Action Memory** stores each (action, result) pair within the current round so subsequent steps can adapt the plan; at round end the agent emits its gene panel. The agent receives raw control-cell expression at round 0 and the raw expression of perturbed cells for previously selected perturbations in subsequent rounds. External knowledge (e.g., KEGG) is accessible as an additional tool.

## Validation

Evaluated on eleven phenotypes drawn from genome-scale Perturb-seq data (Replogle et al. 2022 and related), against agent-based and active-learning baselines: BioDiscoveryAgent, GeneDisco, DiscoBAX, and IterPert. Tested with both closed-source and open-source LLMs as the underlying planner.

## Notable results

- Outperforms prior agent-based (BioDiscoveryAgent) and active-learning (GeneDisco, DiscoBAX, IterPert) baselines across the eleven phenotypes.
- Compatible with both closed-source and open-source LLM backbones; more capable models give larger gains.
- Action-frequency and action-memory analyses provide interpretable insight into which reasoning steps drive selection — a transparency property absent from fixed-plan agent baselines.

## Primary paper

[Hao, Lee, Wang, Scalia, Regev, "PerTurboAgent: An LLM-based Agent for Designing Iterative Perturb-Seq Experiments," PMLR v311 (MLCB 2025); bioRxiv 2025.05.25.656020](https://proceedings.mlr.press/v311/hao25b.html).

## Other references

- [bioRxiv preprint](https://doi.org/10.1101/2025.05.25.656020)

## Code

Not released at proceedings time.
