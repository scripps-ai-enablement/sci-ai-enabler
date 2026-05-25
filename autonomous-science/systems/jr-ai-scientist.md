---
title: Jr. AI Scientist
parent: Systems
grand_parent: AI scientists
nav_order: 24
affiliation: The University of Tokyo (Aizawa lab) and Tokyo University of Science
lifecycle_stages: [Multi-stage, Writing]
autonomy: Fully autonomous
domain: Machine learning / computer vision
availability: Open source
last_verified: 2026-05-22
---

# Jr. AI Scientist

Autonomous AI scientist that mimics a novice student's workflow — analyzing a baseline paper's limitations, formulating improvement hypotheses, iterating experiments via modern coding agents, and writing the resulting paper.

| | |
|---|---|
| **Affiliation** | The University of Tokyo (Aizawa lab) and Tokyo University of Science (Miyai, Toyooka, Otonari, Zhao, Aizawa) |
| **First introduced** | 2026-02 (published in *TMLR*; arXiv:2511.04583) |
| **Lifecycle stages** | Multi-stage (limitation analysis → idea generation → multi-stage experimentation → manuscript creation), plus Writing |
| **Autonomy level** | Fully autonomous within a baseline-paper-anchored workflow (human mentor supplies the baseline paper) |
| **Domain focus** | Machine learning research, evaluated on NeurIPS, IJCV, and ICLR baseline papers |
| **Availability** | Open source ([github.com/Agent4Science-UTokyo/Jr.AI-Scientist](https://github.com/Agent4Science-UTokyo/Jr.AI-Scientist)) |

## Approach

The system takes a baseline paper (PDF + LaTeX source + codebase) from a human mentor and executes a four-phase workflow: Baseline Resources ingestion and limitation analysis; Idea Generation with novelty checks; three-stage Experimentation (implement the proposed method, improve it, then run ablation studies with LLM Review and feedback reflection); and Paper Write-Up (manuscript creation, review reflection, page adjustment). The architecture leans on modern coding agents to handle complex, multi-file implementations — explicitly addressing the prior limitation of AI-scientist systems being restricted to small-scale code experiments.

## Validation

Evaluated on three real baseline papers — a NeurIPS 2023 paper, an IJCV 2025 paper, and an ICLR 2025 paper — under three regimes: (1) automated DeepReviewer assessment comparing Jr. AI Scientist's outputs to other AI-generated papers; (2) author-led evaluation of papers built on the authors' own prior work; and (3) submission to the Agents4Science conference, a venue dedicated to AI-driven scientific contributions. The companion risk report comprehensively catalogues failure modes encountered during development.

## Notable results

- Generated papers receive higher DeepReviewer scores than existing fully automated AI-scientist systems.
- Successfully built on real NeurIPS / IJCV / ICLR papers by proposing and implementing novel methods (rather than only running small-scale toy experiments).
- The published risk inventory documents concrete failure modes — useful prior art for any group deploying autoresearch systems.

## Primary paper

[Miyai, Toyooka, Otonari, Zhao, Aizawa, "Jr. AI Scientist and Its Risk Report: Autonomous Scientific Exploration from a Baseline Paper," *TMLR* (2026)](https://openreview.net/forum?id=OeV062d8Sw) ([arXiv:2511.04583](https://arxiv.org/abs/2511.04583)).

## Other references

_None yet._

## Code

[github.com/Agent4Science-UTokyo/Jr.AI-Scientist](https://github.com/Agent4Science-UTokyo/Jr.AI-Scientist)
