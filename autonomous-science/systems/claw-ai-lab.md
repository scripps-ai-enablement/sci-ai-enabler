---
title: Claw AI Lab
parent: Systems
grand_parent: AI scientists
nav_order: 16
affiliation: Nanyang Technological University (Wu, Chen, Lin) with A*STAR, Moxin Technology, NUIST, Tsinghua University, and USTC
org_short: NTU Singapore
lifecycle_stages: [Multi-stage, Writing]
validation_type: Benchmark
autonomy: Semi-autonomous
domain: Machine learning research (idea generation, experimentation, reproduction)
domain_group: ML & scientific computing
availability: Open source
access: Open source
tagline: Lab-native platform that spins up a full multi-agent research team from one prompt, with monitoring and rollback.
last_verified: 2026-08-08
---

# Claw AI Lab

Autonomous research platform that instantiates a customizable multi-agent research team from a single prompt and exposes it through a dashboard with real-time event streams, artifact inspection, and rollback/resume control.

| | |
|---|---|
| **Affiliation** | Nanyang Technological University with A*STAR, Moxin Technology, NUIST, Tsinghua, and USTC ([paper](https://arxiv.org/abs/2605.22662)) |
| **First introduced** | 2026-05 (arXiv:2605.22662, dated 2026-05-21) |
| **Lifecycle stages** | Multi-stage (idea → plan → code → experiment → analysis), plus Writing as a final stage |
| **Autonomy level** | Semi-autonomous — a fully autonomous project mode exists and was used for the evaluation, but the platform is built around human steering: customizable roles, mid-run intervention, and one-click rollback |
| **Domain focus** | Machine learning research; the reported case studies cover video-generation hallucination, fake-news classification, RL for education data, and a reproduction task |
| **Availability** | Open source ([github.com/Claw-AI-Lab/Claw-AI-Lab](https://github.com/Claw-AI-Lab/Claw-AI-Lab)) |

## Approach

Claw AI Lab reframes autonomous research away from a hidden prompt-to-paper pipeline and toward an operable laboratory. Work flows through an Idea layer (multi-agent discussion proposes candidate ideas and converges on a consensus idea), a Planning layer (decomposition into tasks and milestones, refined and finalized before execution), and a Coding layer (context construction, tool calls, test-and-update cycles) before experiments run. Three research modes — Explore, Discussion, and Reproduce — select different collaboration patterns rather than forcing a single serial workflow.

The central engineering contribution is the **Claw-Code Harness**, which wires local codebases, datasets, and checkpoints into runnable experiments and feeds execution artifacts back into the research loop. The harness targets two named failure modes of prior end-to-end research agents: partial runs that are silently treated as complete, and malformed result reporting where the written paper drifts from what was actually measured. Every artifact is inspectable from the dashboard, and rollback lets a researcher rewind a project to an earlier state instead of restarting.

## Validation

Internal head-to-head evaluation against [AutoResearchClaw](autoresearchclaw.html) as baseline, on four topics (three research, one reproduction), with Claw AI Lab in fully autonomous project mode on a GPT-5.4 backbone. Each generated paper was scored by two independent LLM reviewers (ChatGPT 5.4 Thinking and Gemini 3.1 Pro) in fresh conversation windows across six dimensions: technical depth and reproducibility, structure and section flow, novelty and contributions, clarity and terminology, logical argumentation, and citations and evidence support. No wet-lab or physical validation.

## Notable results

- On the three research topics, average score improvements over AutoResearchClaw of **+15.5 to +16.5 points**, consistent across both LLM evaluators.
- On the reproduction topic (reproducing PhyCustom on Flux), the average score rose from **73.0/100 to 78.0/100**.
- Both evaluators preferred Claw AI Lab on every topic, which the authors attribute to the Claw-Code Harness producing execution records that better support the paper's claims.

Evaluation is judge-based and self-reported, with a single baseline and four topics — a much narrower regime than the benchmark suites used elsewhere in this cluster.

## Primary paper

[Wu, Chen, Tan et al., "Claw AI Lab: An Autonomous Multi-Agent Research Team," arXiv:2605.22662](https://arxiv.org/abs/2605.22662).

## Other references

_None yet._

## Code

[github.com/Claw-AI-Lab/Claw-AI-Lab](https://github.com/Claw-AI-Lab/Claw-AI-Lab).
