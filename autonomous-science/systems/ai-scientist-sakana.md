---
title: AI Scientist (Sakana)
parent: Systems
grand_parent: AI scientists
nav_order: 1
affiliation: Sakana AI, with FLAIR (Oxford), University of British Columbia, Vector Institute
lifecycle_stages: [Multi-stage, Writing]
autonomy: Fully autonomous
domain: Machine-learning research
availability: Open source
last_verified: 2026-05-20
---

# AI Scientist (Sakana)

End-to-end LLM agent that generates research ideas, searches literature, writes and executes code, runs experiments, produces figures and a full LaTeX manuscript, and runs an Automated Reviewer over its own output.

| | |
|---|---|
| **Affiliation** | Sakana AI, with FLAIR (Oxford), University of British Columbia, Vector Institute ([Sakana AI](https://sakana.ai/)) |
| **First introduced** | 2024-08 (arXiv v1); v2 preprint 2025-04; published in *Nature* 2026-03 |
| **Lifecycle stages** | Multi-stage, Writing |
| **Autonomy level** | Fully autonomous (v1 within a fixed code-template starting point; v2 removes the template requirement) |
| **Domain focus** | Machine-learning research (diffusion modelling, transformer LMs, learning dynamics in v1; broader ML domains in v2) |
| **Availability** | Open source (v1 code on GitHub; v2 codebase open-sourced alongside the preprint) |

## Approach

An end-to-end LLM agent that generates research ideas, searches literature, writes and executes code, runs experiments, produces figures and a full LaTeX manuscript, and runs an Automated Reviewer (Area-Chair-style ensemble of five LLM reviews). v2 replaces v1's human-written code templates with a progressive agentic tree search managed by a dedicated experiment-manager agent.

## Validation

v1 generated full ML papers at ~$15 per paper and reported papers exceeding a top-ML-conference acceptance threshold under the Automated Reviewer. v2 submitted three fully AI-generated manuscripts to an ICLR 2025 workshop, with one accepted at the "I Can't Believe It's Not Better" (ICBINB) workshop — the first AI-generated paper to pass human peer review. The *Nature* paper reports a scaling law tying paper quality to underlying foundation-model capability.

## Notable results

- First end-to-end AI-generated paper to pass peer review (ICLR 2025 workshop, v2).
- Automated Reviewer reaches ~69% balanced accuracy on NeurIPS-style review tasks (v1).

## Primary paper

[Lu et al., "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery," arXiv:2408.06292](https://arxiv.org/abs/2408.06292); peer-reviewed version Lu et al., *Nature* 651, 914–919 (2026).

## Other references

- [Yamada et al., "The AI Scientist-v2," arXiv:2504.08066](https://arxiv.org/abs/2504.08066)
- [Sakana AI *Nature* announcement](https://sakana.ai/ai-scientist-nature/)
- [*Nature* news, "How to build an AI scientist"](https://www.nature.com/articles/d41586-026-00899-w)

## Code

- [AI-Scientist (v1)](https://github.com/SakanaAI/AI-Scientist)
- [AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)
