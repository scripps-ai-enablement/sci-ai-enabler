---
title: CogEEGAgent
parent: Systems
grand_parent: AI scientists
nav_order: 17
affiliation: Tohoku University (Graduate School of Information Sciences and Unprecedented-scale Data Analytics Center — Dengzhe Hou, Kazunori D. Yamada) with Texas A&M University and Worcester Polytechnic Institute
org_short: Tohoku University
lifecycle_stages: [Analysis]
validation_type: Benchmark
autonomy: Semi-autonomous
domain: Cognitive neuroscience — EEG / event-related potential analysis
domain_group: Biology & medicine
availability: Open source — GitHub repository stated in the paper
access: Open source
tagline: Cognitive-EEG analysis agent that gives the LLM semantic authority but keeps scientific authority deterministic.
last_verified: 2026-08-01
---

# CogEEGAgent

Tool-grounded LLM agent for auditable cognitive-EEG analysis whose harness separates the model's interpretive role from deterministic control over which analyses may be run and which results may be released.

| | |
|---|---|
| **Affiliation** | Tohoku University, with Texas A&M University and Worcester Polytechnic Institute |
| **First introduced** | 2026-07 (arXiv:2607.25045) |
| **Lifecycle stages** | Analysis |
| **Autonomy level** | Semi-autonomous — bounded autonomy by design; the harness can force abstention and block release |
| **Domain focus** | Cognitive EEG — ERP and spectral analysis over pre-loaded epochs via MNE-Python |
| **Availability** | Open source — [github.com/dengzhe-hou/CogEEGAgent](https://github.com/dengzhe-hou/CogEEGAgent) as stated in the paper |

## Approach

The motivating failure mode is that fluent agent reports cannot establish either that the agent selected the analysis actually requested, or that a confirmatory claim was evaluated independently of adaptive search — automation scales researcher degrees of freedom, since even successful tool calls do not preserve nominal error when an agent searches plausible analyses and reports the most favorable one. CogEEGAgent's EEG-specific scientific harness therefore separates *semantic authority* from *scientific authority*. The LLM interprets natural-language intent and selects a registered analysis; deterministic code owns contract materialization, preflight checks, data access, commitment, inference, falsification, and reporting. Two components implement this: a **Scientific Control Plane** provides the prospective release path — freezing a contract, splitting participants, letting a bounded LLM select one of nine frozen candidates, opening a hidden confirmation set once, replaying and falsifying, then binding evidence to release or abstention — and **Paradigm-Conditioned Verification (PCVR)** audits recorded MNE workflows post hoc, preserving valid nulls and bounding invalid numerics.

## Validation

Three prespecified prospective studies. A **routing benchmark** isolates language-to-contract choice under matched preflight. An **externally model-authored, outcome-blind 21-case campaign** carries selected contracts through participant-disjoint confirmation to release or abstention. **Policy stress testing** measures the false-positive rate under uncorrected adaptive search versus held-out confirmation. Evaluation is framed as boundary testing — whether the system fails closed — rather than task completion.

## Notable results

- On the prespecified routing benchmark the agent correctly routed 39/40 unique valid requests versus 33 for a matched deterministic FW-BM25 router, a bootstrap difference of 15.0 points (95% CI 2.5–28.6); shared preflight made both systems abstain whenever required.
- In the 21-case composed campaign the complete system released three supported ERP analyses (ERN, N400, MMN) with participant-disjoint confirmation, and blocked prespecified capability hazards and lifecycle-reuse requests.
- Policy stress testing showed held-out confirmation cut the null false-positive rate by 11.6 points (95% subject-cluster CI 11.0–12.1) to 4.9%, curbing false positives from uncorrected adaptive search.

## Primary paper

[Hou et al., "CogEEGAgent: Toward Autonomous Cognitive EEG Analysis with Grounded Execution and Selection-Aware Verification," arXiv:2607.25045](https://arxiv.org/abs/2607.25045).

## Other references

_None yet._

## Code

[Repository](https://github.com/dengzhe-hou/CogEEGAgent) — stated in the paper.
