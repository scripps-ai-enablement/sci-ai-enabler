---
title: Kosmos
parent: Systems
grand_parent: AI scientists
nav_order: 25
affiliation: Edison Scientific Inc., with FutureHouse, University of Oxford, University College London, Washington University in St. Louis, MIT, Stanford, and additional collaborators
lifecycle_stages: [Multi-stage, Writing]
autonomy: Semi-autonomous
domain: General (data-driven discovery)
availability: Closed / API only
last_verified: 2026-05-21
---

# Kosmos

AI scientist that automates data-driven discovery by running up to 12-hour cycles of parallel data analysis, literature search, and hypothesis generation against a structured world model, citing every statement back to code or primary literature.

| | |
|---|---|
| **Affiliation** | Edison Scientific Inc., with FutureHouse, University of Oxford, UCL, Washington University in St. Louis, MIT, Stanford, and additional academic partners ([edisonscientific.com](https://www.edisonscientific.com/)) |
| **First introduced** | 2025-11 (arXiv:2511.02824) |
| **Lifecycle stages** | Multi-stage (literature search + data analysis + hypothesis generation) + Writing (synthesizes discoveries into traceable scientific reports) |
| **Autonomy level** | Semi-autonomous (scientist supplies an open-ended objective and dataset; the system runs end-to-end for up to 12 hours / 20 cycles) |
| **Domain focus** | General — demonstrated across metabolomics, materials science, neuroscience, and statistical genetics |
| **Availability** | Closed / API only — Edison Scientific–hosted platform; trajectories linked from the paper at `platform.edisonscientific.com` |

## Approach

Kosmos is initiated with a research objective and a dataset. At each cycle it launches parallel instances of two general-purpose Edison Scientific agents — a data-analysis agent and a literature-search agent — with up to ten tasks dispatched per cycle. A structured **world model** is continuously updated with task summaries and queried to propose the next cycle's tasks, enabling coherent goal-pursuit across roughly 200 agent rollouts per run. An average run executes ~42,000 lines of code across 166 data-analysis-agent rollouts and reads 1,500 full-length papers across 36 literature-review rollouts — a 9.8× increase in code generation over Robin. When Kosmos considers the objective complete, it synthesizes three or four scientific reports in which every statement and figure cites either a Jupyter notebook produced by the data-analysis agent or a publication surfaced by the literature-search agent.

## Validation

Independent expert scientists classified 102 statements from three representative Kosmos reports as Supported or Refuted; 79.4% were Supported. Collaborators reported that a single 20-cycle Kosmos run performed the equivalent of approximately six months of their own research time on average, with the number of valuable findings scaling roughly linearly with cycle count up to 20 cycles.

## Notable results

- Seven highlighted discoveries spanning metabolomics, materials science, neuroscience, and statistical genetics. Three independently reproduce findings from preprinted or unpublished manuscripts that were not accessed by Kosmos at runtime; four are claimed novel contributions.
- Generated novel statistical evidence that high circulating SOD2 may causally reduce myocardial fibrosis in humans.
- Identified a clinically relevant mechanism of neuronal aging in one of the case studies.

## Primary paper

[Mitchener et al., "Kosmos: An AI Scientist for Autonomous Discovery," arXiv:2511.02824](https://arxiv.org/abs/2511.02824).

## Other references

_None yet._

## Code

Not released. Figures and data for the paper are at [EdisonScientific/kosmos-figures](https://github.com/EdisonScientific/kosmos-figures); agent trajectories are viewable at `platform.edisonscientific.com/trajectories/`.
