---
title: ARIS
parent: Systems
grand_parent: AI scientists
nav_order: 5
affiliation: Shanghai Jiao Tong University and Shanghai Innovation Institute
lifecycle_stages: [Multi-stage, Writing]
autonomy: Semi-autonomous
domain: Machine learning research
availability: Open source
last_verified: 2026-05-22
---

# ARIS

Autonomous research harness that coordinates ML research workflows via cross-model adversarial collaboration — pairing an executor model from one family with a reviewer model from a different family at each assurance checkpoint.

| | |
|---|---|
| **Affiliation** | Shanghai Jiao Tong University and Shanghai Innovation Institute (Yang, Li, Li) |
| **First introduced** | 2026-04/05 (technical report; arXiv:2605.03042) |
| **Lifecycle stages** | Multi-stage (idea discovery → implement & deploy → experiment bridge → paper writing → rebuttal), plus Writing |
| **Autonomy level** | Semi-autonomous (default Claude Code + GPT-5.4 pairing under a human-approved configuration; assurance checks at key milestones) |
| **Domain focus** | Machine learning research workflows |
| **Availability** | Open source ([github.com/wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)) |

## Approach

ARIS treats independent assurance as a first-class workflow layer. An orchestration layer coordinates five end-to-end workflows — Idea Discovery, Implement & Deploy, Auto-Review Loop, Paper Writing, and Rebuttal — built from reusable Markdown-defined skills. The default configuration pairs an executor model (e.g., Claude Code) with a reviewer model from a different family (e.g., GPT-5.4 xhigh), arguing that single-model self-review is the "stochastic bandits" case while cross-model review is genuinely adversarial: the reviewer probes weaknesses the executor did not anticipate. An assurance stack performs integrity verification, reviewer routing, and a three-stage check that claims are supported by evidence; executors retry up to a configurable limit (default three) before harness improvements are adopted. A prototype self-improvement loop closes the cycle.

## Validation

The technical report demonstrates ARIS across all five workflows on illustrative ML research tasks — for example, denoiser model post-training experiments with 4× A100 servers, an Auto-Review Loop that iteratively raised paper scores from 4/10 through 7.5/10 across three rounds, and a Rebuttal workflow that atomized reviewer concerns into structured responses with provenance, commitment, and lint checks.

## Notable results

- Introduces cross-model executor/reviewer pairing as an explicit architectural pattern, contrasting with single-model self-critique loops used by prior AI-scientist systems.
- Auto-Review Loop demonstrated rounds of paper improvement (Round 0 → Round 2: 4/10 → 7/10) with concrete fixes for overclaims, notation clash, and missing validation.
- Five-workflow design with explicit assurance checks at key experimental and writing milestones.

## Primary paper

[Yang, Li, Li, "ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration," ARIS Technical Report, April 2026 (arXiv:2605.03042)](https://arxiv.org/abs/2605.03042).

## Other references

_None yet._

## Code

[github.com/wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)
