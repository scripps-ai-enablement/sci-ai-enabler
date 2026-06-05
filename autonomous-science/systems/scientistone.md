---
title: ScientistOne
parent: Systems
grand_parent: AI scientists
nav_order: 45
affiliation: Google Cloud AI Research
org_short: Google
lifecycle_stages: [Multi-stage, Writing]
validation_type: Benchmark
autonomy: Fully autonomous
domain: General (frontier ML research, plus medical imaging, fine-grained recognition, 3D perception, parameter-constrained LM)
domain_group: General / multi-domain
availability: Closed / API only
access: Closed
tagline: End-to-end autonomous research system maintaining verifiable evidence chains for every claim.
last_verified: 2026-05-31
---

# ScientistOne

End-to-end autonomous research system that maintains verifiable evidence chains for every claim across literature review, solution discovery, and paper writing.

| | |
|---|---|
| **Affiliation** | Google Cloud AI Research |
| **First introduced** | 2026-05 (arXiv:2605.26340) |
| **Lifecycle stages** | Multi-stage (literature grounding → discovery → paper writing with claim verification); secondary Writing tag |
| **Autonomy level** | Fully autonomous within the Chain-of-Evidence (CoE) pipeline |
| **Domain focus** | Frontier computer-systems research (ADRS benchmark), with demonstrated generalization to medical imaging, fine-grained recognition, 3D perception, and parameter-constrained language modeling |
| **Availability** | Project website [scientist-one.github.io](https://scientist-one.github.io/); no open implementation announced |

## Approach

ScientistOne is built around the Chain-of-Evidence (CoE) standard, which requires every claim — citation, numerical, methodological, conclusion — to trace through a recorded evidence chain to a grounding source. The pipeline has three stages:

- **Stage 1 — Problem Investigator (PI):** starts from seed papers, builds a citation graph via scholarly database queries, reads up to 100 full-text PDFs per topic, and produces a structured research brief with provenance metadata.
- **Stage 2 — Discovery Engine:** an Ideator generates and scores candidate approaches; a Parallel Explore-Exploit (PEE) orchestrator runs Solver agents across multiple branches, each iterating up to E evaluated versions per node with task-specific evaluators; top-K branches are retained and replenished via fresh ideation; a best-run selector filters out specification violators.
- **Stage 3 — Paper Writer with Claim Verifier:** drafts the manuscript and checks every claim against its declared evidence source before producing the final paper.

The system is paired with **CoE Integrity Audit**, a post-hoc protocol with four checks: Score Verification (I1), Specification Violation, Reference Verification, and Method-Code Alignment.

## Validation

CoE Integrity Audit applied to 75 papers (15 per system) from five autonomous research systems on five ADRS frontier ML tasks. ScientistOne is benchmarked against AI Scientist-v2, AutoResearchClaw, DeepScientist, and AI-Researcher.

## Notable results

- Zero hallucinated references (0 / 337 bibliography entries) versus up to 21% for baseline systems.
- Perfect score verification (12 / 12) and the highest method-code alignment (14 / 15) among the five systems audited.
- Matches or exceeds human expert solver performance on all five ADRS tasks.
- Generalizes to six additional tasks: state-of-the-art on Parameter Golf; gold medals on MLE-Bench tasks where baselines fail entirely.

## Primary paper

[Meng et al., "ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence," arXiv:2605.26340 (2026)](https://arxiv.org/abs/2605.26340).

## Other references

- [Project website](https://scientist-one.github.io/)

## Code

Not released.
