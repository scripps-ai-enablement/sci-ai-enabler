---
title: EOS AI agent
parent: Systems
grand_parent: AI scientists
nav_order: 21
affiliation: UNC-Chapel Hill (Angelopoulos, Cahoon, Alterovitz)
lifecycle_stages: [Experiment design, Analysis]
autonomy: Semi-autonomous
domain: Laboratory automation across chemistry, biology, and materials science
availability: Unknown
last_verified: 2026-05-24
---

# EOS AI agent

UNC-Chapel Hill AI agent integrated with the Experiment Orchestration System (EOS) that creates, runs, monitors, and analyzes laboratory protocols and closed-loop optimization campaigns from natural-language requests, with a visual graph editor synchronized to its internal protocol representation.

| | |
|---|---|
| **Affiliation** | Department of Computer Science and Department of Chemistry, UNC-Chapel Hill ([paper](https://arxiv.org/abs/2605.16552)) |
| **First introduced** | 2026-05 (arXiv:2605.16552, dated 2026-05-15) |
| **Lifecycle stages** | Experiment design (protocol creation and submission, including closed-loop optimization campaigns) and Analysis (database queries, summary statistics, convergence and parameter-sensitivity interpretation) |
| **Autonomy level** | Semi-autonomous — runs an agentic loop with automated validation and error correction; read-only operations execute automatically while mutating operations require explicit user approval |
| **Domain focus** | Generalist laboratory orchestration across chemistry, biology, and materials science |
| **Availability** | Unknown — no public repository disclosed in the preprint |

## Approach

A REST-backed AI agent layered on top of the EOS laboratory orchestrator. A dynamically generated system prompt provides the LLM with the EOS domain model, task specifications, parameter schemas, device specifications, available laboratory resources, and the current view in the EOS interface. The agent edits protocols defined in YAML (directed acyclic graphs of tasks with parameters, dependencies, device assignments) that a renderer converts into an interactive visual protocol graph; the YAML and the graph share a single state store so AI edits and manual edits propagate bidirectionally.

EOS exposes **over 40 MCP tools** organized into eight categories — tasks/protocols/campaigns, devices, system administration, optimizer, data access, registry, and others — through an in-memory MCP server. The agent validates generated protocols against the EOS validation engine, which batches all structural and scientific-constraint errors so the agent can address them in a single correction step. The agent supports four scientist-facing functions: creating protocols, monitoring protocol runs and optimization campaigns, analyzing experimental data (SQL queries and code execution against a read-only PostgreSQL view, plus device/file inspection), and submitting work / managing the lab. A question-asking tool lets the agent solicit feedback on underspecified situations (up to 10 questions with multiple-choice answers and a custom-answer field). Reported integrations are Claude Sonnet 4.6 and Claude Opus 4.6.

## Validation

Three simulated automated labs spanning chemistry, biology, and materials-adjacent platforms.

- **Color mixing optimization campaign** in a virtual lab with a GPU-accelerated fluid solver (Stable Fluids–based). A 10-parameter Bayesian-optimization campaign over four ingredient colors plus mixing time/speed.
- **Solubility and purification screening** on PurPOSE (UBC self-driving robotic chemistry platform, 10 instruments, 16 task definitions) — HPLC standard-curve calibration, solubility screening, and cooling-crystallization campaigns with multi-objective Bayesian optimization.
- **Liquid-liquid extraction** vial-weighing protocol (also on PurPOSE).

## Notable results

- First-attempt protocol generation success: **94%** on the color-mixing prompt (33/35 trials) and **97% overall across 65 trials** spanning four prompts (linear, parallel-branch, and compositional protocols).
- Color-mixing campaign converged to **loss 0.00392** (~1/255, near-perfect color match) after ~16 experiments; the agent autonomously summarized convergence phases and correctly identified locked-constant and high-variance parameters in post-hoc analysis.
- Execution metrics (color-mixing protocol, N=35): mean **184 s** wall time, **6.6 reasoning steps**, **7.3 MCP tool calls**, **0.1 validation corrections**, **$0.50 LLM cost** per protocol generation.
- PurPOSE: standard-curve and solubility-screening protocols generated correctly on first attempt; the 15-task crystallization campaign was a close reproduction with minor discrepancies. Order-of-magnitude reduction in required user-interface actions versus manual EOS workflows.

## Primary paper

[Angelopoulos, Cahoon, Alterovitz, "From Prompts to Protocols: An AI Agent for Laboratory Automation," arXiv:2605.16552](https://arxiv.org/abs/2605.16552).

## Other references

_None yet._

## Code

Not released at preprint time.
