---
title: Co-Scientist (Google)
parent: Systems
grand_parent: AI scientists
nav_order: 8
affiliation: Google Cloud AI Research / Google DeepMind / Google Research, with Stanford, Imperial College London, Houston Methodist
lifecycle_stages: [Hypothesis, Experiment design]
autonomy: Semi-autonomous
domain: General (validated in biomedicine)
availability: Closed / API only
last_verified: 2026-05-20
---

# Co-Scientist (Google)

Gemini-based multi-agent reasoning engine focused on hypothesis generation, using a generation/reflection/ranking/evolution ensemble with Elo-style tournaments. Validated in three peer-reviewed biomedical case studies.

| | |
|---|---|
| **Affiliation** | Google Cloud AI Research / Google DeepMind / Google Research, with collaborators at Stanford, Imperial College London, and Houston Methodist ([Google Research](https://research.google/)) |
| **First introduced** | 2025-02 (initial blog announcement); peer-reviewed paper accepted 2026-05 |
| **Lifecycle stages** | Hypothesis, Experiment design |
| **Autonomy level** | Semi-autonomous (scientist-in-the-loop collaborative paradigm) |
| **Domain focus** | General; validated in biomedicine (drug repurposing, target discovery, antimicrobial resistance) |
| **Availability** | Closed / API only — full source not public; experimental access program announced; Gemini foundation model accessible via Google APIs |

## Approach

Multi-agent system built on Gemini, comprising specialized agents (Generation, Reflection, Ranking, Evolution, Proximity, Meta-review) coordinated via an asynchronous task framework. Uses self-play scientific debate for hypothesis generation, an Elo-style tournament to compare hypotheses, and an evolution loop to refine them by scaling test-time compute.

## Validation

Three biomedical case studies:

- Drug repurposing for acute myeloid leukemia (AML) with in vitro confirmation.
- Novel epigenetic targets for liver fibrosis confirmed in human hepatic organoids.
- Recapitulation of a then-unpublished bacterial gene-transfer mechanism in antimicrobial resistance, discovered independently by collaborators at Imperial College.

## Notable results

Identified novel single-agent and combination repurposing candidates for AML showing selective cytotoxicity at clinically relevant concentrations. Ranked epigenetic targets with anti-fibrotic activity in organoids. Independently recapitulated an unpublished AMR gene-transfer mechanism.

## Primary paper

[Gottweis et al., "Accelerating scientific discovery with Co-Scientist," *Nature* 2026](https://doi.org/10.1038/s41586-026-10644-y).

## Other references

- [*Nature* news on AI agents in science (AI Index 2026)](https://doi.org/10.1038/d41586-026-01199-z)
- [arXiv preprint, "Towards an AI co-scientist," 2502.18864](https://arxiv.org/abs/2502.18864)

## Code

Not released. Pseudocode and system prompts provided in supplementary notes.
