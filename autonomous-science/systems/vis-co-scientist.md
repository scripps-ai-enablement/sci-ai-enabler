---
title: VIS Co-Scientist
parent: Systems
grand_parent: AI scientists
nav_order: 55
affiliation: Lawrence Livermore National Laboratory, Vanderbilt University, University of Notre Dame
org_short: LLNL
lifecycle_stages: [Analysis]
validation_type: Benchmark
autonomy: Fully autonomous
domain: Scientific visualization (cross-domain — climate, materials, sonar, neuroscience, mantle convection)
domain_group: Other
availability: Code release pending organizational review
access: Code on request
tagline: Agentic harness that autonomously designs custom visual-analysis apps from a dataset and task description.
last_verified: 2026-06-02
---

# VIS Co-Scientist

End-to-end agentic harness that, given only a dataset and a high-level task description, autonomously designs custom visual-analysis applications (VIS Apps) through a multi-agent loop spanning exploratory data analysis, planning, environment configuration, implementation, browser-based validation, and task evaluation.

| | |
|---|---|
| **Affiliation** | Lawrence Livermore National Laboratory; Vanderbilt University; University of Notre Dame |
| **First introduced** | 2026-05 (arXiv:2605.21825) |
| **Lifecycle stages** | Analysis (autonomous data exploration, interpretation, and visualization-application design) |
| **Autonomy level** | Fully autonomous over the VIS-App lifecycle; human input is the task description and dataset |
| **Domain focus** | Scientific visualization across natural-science and engineering domains evaluated via IEEE SciVis Contests (climate, materials discovery, sonar imaging, neuroscience, mantle convection) |
| **Availability** | Open source pending internal code-review completion at LLNL |

## Approach

VIS Co-Scientist is a multi-agent harness in which a main code agent (implemented on OpenAI Codex) orchestrates a workflow over specialized subagents that communicate through explicit artifacts (reports, plans, instructions, scorecards). An **Exploratory Data Analyzer** profiles datasets, identifies schemas, scale, missing values, and task-relevant variables, and emits an EDA Report. A **Planner** translates task and EDA Report into a concrete specification covering visual encodings, coordinated panels, interaction state, risks, and validation checks. An **Environment Builder** configures minimal dependencies for data access, visualization, and browser validation. A **VIS Designer** implements or repairs complex views — 3D volume rendering, progressive streaming, custom brushing, linked selections. An **Evaluator** tests the live VIS App against task goals through Playwright-based browser inspection and grades the App, returning a Feedback/Fixes report that the orchestrator either resolves directly or routes back to the VIS Designer.

A hierarchical memory layer inspired by LLM Wiki keeps human-readable markdown notes that accumulate insights about datasets, tasks, and visualization approaches across sessions; memory is currently used for post-run knowledge capture and auditability rather than retrieval-conditioned design. Custom skills and Model Context Protocol (MCP) connectors give the orchestrator targeted tool access.

## Validation

Evaluated end-to-end on the IEEE SciVis Contests for 2021, 2023, 2024, and 2026, spanning climate science, materials discovery, sonar imaging, neuroscience, and mantle convection. These contests encode ambiguous requirements, diverse data modalities, design trade-offs, and task-driven validation, and typically require graduate-level skills.

## Notable results

- Given only the data and target tasks, the system autonomously produced functional single-page VIS Apps with verified linked-view behavior across four SciVis Contest years.
- The Evaluator both verifies interactive mechanics (e.g., linked panels respond to selection) and grades whether the original analysis tasks can be achieved from the displayed visualization.
- Authors identify two persistent gaps: lack of creative visual design beyond established patterns, and limited multi-step visual perception and reasoning.

## Primary paper

[Miao, Li, Ai, Tang, Wang, Bremer, Liu, "Toward AI VIS Co-Scientists: A General and End-to-End Agent Harness for Solving Complex Data Visualization Tasks," arXiv:2605.21825 (2026)](https://arxiv.org/abs/2605.21825).

## Other references

_None yet._

## Code

Open source release pending internal code-review completion at the authoring organization (LLNL).
