---
title: ARIA
parent: Systems
grand_parent: AI scientists
nav_order: 8
affiliation: Johns Hopkins University — Chemical and Biomolecular Engineering (Clancy group) and Computer Science (Van Durme, Yuille)
org_short: Johns Hopkins
lifecycle_stages: [Hypothesis, Analysis]
validation_type: Benchmark
autonomy: Semi-autonomous
domain: Materials science (2D materials synthesis, Process-Structure-Property reasoning)
domain_group: Chemistry & materials
availability: Open source — code at github.com/yicao-elina/ARIA (CC-BY-4.0 paper)
access: Open source
tagline: Causal-aware LLM framework gating knowledge on Process-Structure-Property completeness for trustworthy materials discovery.
last_verified: 2026-07-11
---

# ARIA

A causal-aware LLM framework that conditions knowledge use on the mechanistic completeness of Process-Structure-Property (PSP) evidence chains, routing each materials-discovery query through a three-tier adaptive cascade to produce physically consistent forward predictions and inverse synthesis protocols.

| | |
|---|---|
| **Affiliation** | Johns Hopkins University (Clancy, Van Durme, Yuille groups) ([code](https://github.com/yicao-elina/ARIA)) |
| **First introduced** | 2026-06 (arXiv:2606.22375; KDD '26) |
| **Lifecycle stages** | Hypothesis (inverse design of synthesis protocols), Analysis (forward property prediction) |
| **Autonomy level** | Semi-autonomous — reasons and proposes over PSP knowledge; no autonomous wet-lab execution |
| **Domain focus** | Materials science — 2D materials synthesis and design |
| **Availability** | Open source ([github.com/yicao-elina/ARIA](https://github.com/yicao-elina/ARIA)) |

## Approach

ARIA diagnoses a failure mode it terms *contextual tunneling*, in which knowledge-graph-augmented LLMs over-anchor on narrow retrieved evidence and suppress broader physical reasoning. To counter it, ARIA conditions knowledge use on causal completeness and routes each query through a three-tier cascade:

- **Tier 1 — direct causal reasoning** when a complete Process→Structure→Property evidence chain is available in the knowledge graph.
- **Tier 2 — physics-informed analogical transfer** for sparse or novel material systems, permitted only when the analogy satisfies physical hard filters (thermodynamic, stoichiometric, mass-conservation constraints).
- **Tier 3 — explicit parametric fallback** to the base LLM when external evidence is incomplete.

Grounding it is a Causal Knowledge Graph of 2,839 PSP relations extracted from peer-reviewed materials literature (extraction via Qwen2.5:7B), spanning processing methods (CVD, sol-gel, hydrothermal, exfoliation), structural descriptors, and properties. The prediction/design LLM is DeepSeek-R1:8B. ARIA-FULL adds real-time literature search to enrich evidence when static-KG coverage is incomplete, and produces auditable causal traces for each answer.

## Validation

Benchmark-only (in-silico), evaluated on a 149-case expert-curated dataset drawn from 2005–2026 literature: 117 in-domain cases (58 forward prediction, 59 inverse design) plus 32 out-of-domain cases from 2024–2026 publications post-dating the KG corpus. Six system variants (Baseline LLM, KG-Only, Naive KG+LLM, ARIA-CORE, ARIA-SEARCH, ARIA-FULL) were scored on Scientific Accuracy, Functional Equivalence, Completeness, and Interpretability, aggregated into a composite Overall Score. Automated checks covered thermodynamic feasibility (Materials Project API), stoichiometric consistency, and mass conservation; rubric scoring used DeepSeek-R1:14B as judge. Robustness was cross-checked with a four-expert human preference study (29/30 cases favored ARIA over baseline), model-free hard-constraint metrics, and judge-family variation.

## Notable results

- Naive KG+LLM failed to improve over the unaugmented baseline (contextual tunneling); ARIA-CORE recovered +21.6% over Naive KG+LLM and +20.6% over baseline on in-domain forward prediction (0.410±0.024).
- ARIA-FULL reached 0.512±0.039 on in-domain forward prediction (+50.6% over baseline) and maintained out-of-domain inverse-design performance (0.513±0.040, comparable to its 0.498 in-domain), attributed to Tier 2 analogical transfer.
- ARIA-FULL outperformed the Self-RAG adaptive-retrieval baseline by +13.0% on in-domain forward prediction and +27.7% on in-domain inverse design, with a +64.4% gain in out-of-distribution inverse design.

## Primary paper

[Cao, Wang, Chen, Van Durme, Yuille, Clancy. "ARIA: A Causal-Aware Framework for Rescuing LLM Reasoning in Trustworthy Materials Discovery." KDD '26.](https://doi.org/10.1145/3770855.3818954) ([arXiv:2606.22375](https://arxiv.org/abs/2606.22375))

## Other references

_None yet._

## Code

[Repository](https://github.com/yicao-elina/ARIA).
