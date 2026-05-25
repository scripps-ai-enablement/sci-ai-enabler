---
title: AutoResearchClaw
parent: Systems
grand_parent: AI scientists
nav_order: 9
affiliation: UNC-Chapel Hill (Liu, Qiu, Yao et al.) with UC Santa Cruz, CMU, NUS, UC Berkeley, Rutgers, NEC Labs America, Meta, Stanford, Google, University of Washington
lifecycle_stages: [Multi-stage, Writing]
autonomy: Semi-autonomous
domain: Machine learning, plus high-energy physics, systems biology, and statistics via sandboxed domain agents
availability: Open source
last_verified: 2026-05-24
---

# AutoResearchClaw

Multi-agent autonomous research pipeline that combines structured multi-agent debate for hypothesis generation and result analysis, a self-healing executor with a Pivot/Refine decision loop, verifiable result reporting against a numeric registry, seven human-in-the-loop intervention modes, and cross-run lesson accumulation.

| | |
|---|---|
| **Affiliation** | UNC-Chapel Hill–led consortium with UC Santa Cruz, CMU, NUS, UC Berkeley, Rutgers, NEC Labs America, Meta, Stanford, Google, University of Washington ([paper](https://arxiv.org/abs/2605.20025)) |
| **First introduced** | 2026-05 (arXiv:2605.20025, dated 2026-05-19) |
| **Lifecycle stages** | Multi-stage (Discovery → Experimentation → Writing across a 23-stage pipeline), plus Writing as a final stage |
| **Autonomy level** | Semi-autonomous — Full-Auto mode supported, but the recommended CoPilot mode uses targeted human intervention at six high-leverage decision points; SmartPause routes uncertain decisions to the researcher |
| **Domain focus** | Machine learning (ML01–ML25 in ARC-Bench) extended to 10 high-energy physics, 7 systems biology, and 3 statistics topics via sandboxed domain-skilled sub-agents |
| **Availability** | Open source ([github.com/aiming-lab/AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw)) |

## Approach

Five mechanisms span a 23-stage Discovery → Experimentation → Writing pipeline.

- **Structured multi-agent debate** at two stages. The hypothesis-stage panel pairs an Innovator, a Pragmatist, and a Contrarian; the result-stage panel pairs an Optimist, a Skeptic, and a Methodologist; a synthesizer integrates each panel's outputs into a single structured artifact.
- **Self-healing executor with Pivot/Refine.** Failures are treated as diagnostic information: the system either Proceeds, Refines (retry with targeted fixes), or Pivots (return to hypothesis generation with the failure recorded). A complexity score routes hard experiments to an external coding agent; easier ones are handled by a built-in multi-phase code agent with dependency-ordered file generation, AST summaries, and static validation gates. All execution runs in Docker under a three-phase network policy (Phase 2 disables network entirely during measurement).
- **Verifiable result reporting.** A numeric registry whitelists every value produced by experiment runs; a post-hoc verifier re-extracts numeric claims from the draft and rejects documents with unbacked numbers in Abstract/Results/Experiments. Citations pass a four-layer pipeline (CrossRef → OpenAlex → arXiv → Semantic Scholar) and an LLM relevance check classifying each reference as Verified, Suspicious, or Hallucinated.
- **Human-in-the-loop collaboration.** Seven intervention modes (Full-Auto, Gate-Only, CoPilot, Thorough, Step-by-Step, Pre-Experiment, Post-Experiment) plus a confidence-driven SmartPause that learns per-stage pause thresholds from researcher overrides.
- **Cross-run evolution.** A persistent lesson store ranks retrieved lessons by a time-decayed weight `w(l) = s(l) · exp(−ln 2 · Δt / T_½)` with a 30-day default half-life; lessons are injected as natural-language overlays into subsequent prompts.

## Validation

Introduces **ARC-Bench**, a 25-topic ML benchmark with a 20-topic scientific-domain extension (10 HEP, 7 systems biology, 3 statistics). Evaluated in three modes: experiment-stage (rubric-assisted strict judge, CD:CE:RA = 25:25:50), end-to-end (1–10 paper-quality scale with accept ≥ 5), and scientific-domain (same rubric on physics/biology/statistics tasks). All baselines run on the same GPT-5.3-codex backbone in the same sandbox.

## Notable results

- ARC-Bench experiment stage: AutoResearchClaw (CoPilot) overall **0.648** vs. AI Scientist v2 **0.419** (a **54.7% relative improvement**) and AIDE-ML **0.511**. The largest gap is Result Analysis: **0.523 vs. 0.261** (+100.4%). Full-Auto AutoResearchClaw (0.596) still beats both baselines.
- End-to-end HITL ablation (10 ML topics, 7 modes): **CoPilot 87.5% accept rate** (mean quality 7.27, 19 interventions) — beats Full-Auto (25%, 0 interventions) and Step-by-Step (50%, 29 interventions). Pre-Experiment HITL alone is widely valid but rarely lifts quality; Post-Experiment HITL alone improves faithfulness but is valid on only 6/10 topics.
- Cross-domain coverage: scientific-domain overall **0.867** vs. **0.090** for AIDE-ML and **0.084** for AI Scientist v2 — both baselines fail to install the required HEP and biology stacks. AutoResearchClaw reaches 0.912 on biology (COBRApy / BiGG) and 0.898 on statistics (DML, bootstrap), with 0.489 on HEP-ph after reproducing published cross-sections via FeynRules/MadGraph/MadAnalysis5.
- Component ablation: multi-agent debate is the largest quality contributor (−1.37 quality without it, p=0.003), self-healing is the largest completion contributor (10/10 → 6/10 without it), and removing the verification gate inflates apparent acceptance from 3/10 to 5/10 — three of those five papers contain values absent from any measurement record.

## Primary paper

[Liu et al., "AutoResearchClaw: Self-Reinforcing Autonomous Research with Human-AI Collaboration," arXiv:2605.20025](https://arxiv.org/abs/2605.20025).

## Other references

_None yet._

## Code

[github.com/aiming-lab/AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw).
