---
title: DarkAgents
parent: Systems
grand_parent: AI scientists
nav_order: 20
affiliation: Università di Bologna and INFN Sezione di Bologna (Lucente, Pascoli, Sala, Zandi; Sala on leave from LPTHE, CNRS & Sorbonne U.)
org_short: U. Bologna / INFN
lifecycle_stages: [Multi-stage]
validation_type: Benchmark
autonomy: Semi-autonomous
domain: Theoretical astroparticle physics (cosmological phase transitions, gravitational waves)
domain_group: Physical sciences
availability: Open source
access: Open source
tagline: Language-driven multi-agent system that takes a particle-physics model to a fit against astroparticle data, with explicit assumption and prior auditing.
last_verified: 2026-06-10
---

# DarkAgents

Language-driven multi-agent system for theoretical astroparticle physics that orchestrates LLM agents and deterministic human-written code to go from a particle-physics model to a fit against observational data, while explicitly auditing the assumptions and priors entering the result.

| | |
|---|---|
| **Affiliation** | Università di Bologna and INFN Sezione di Bologna ([repository](https://github.com/PhysicsZandi/DarkAgents)) |
| **First introduced** | 2026-06 (arXiv:2606.11157) |
| **Lifecycle stages** | Multi-stage (model proposal/critique, pipeline computation, constraint analysis and parameter inference) |
| **Autonomy level** | Semi-autonomous — pauses for human audit after each sub-agent by default; can be run fully autonomous end-to-end |
| **Domain focus** | Theoretical astroparticle physics — cosmological first-order phase transitions and nanohertz gravitational waves |
| **Availability** | Open source |

## Approach

DarkAgents is built around an orchestrator that checks the environment, installs the deterministic backend, interprets the user's prompt, selects a supported pipeline branch, writes an explicit execution plan, and dispatches specialized sub-agents in order. Each sub-agent emits a human-readable Markdown report plus a fixed-schema machine-readable JSON handoff that the orchestrator checks before proceeding; by default it pauses after each step for human inspection and correction. Rather than a custom Python framework, the workflow is written primarily as plain-Markdown instructions and skills run on agentic command-line tools, making it LLM-agnostic — it maps generic agent/skill names onto Mistral, Anthropic (Claude Code, `CLAUDE.md`/`.claude`), OpenAI (Codex, `AGENTS.md`/`.codex`), and local LLMs via Ollama. All physical quantities are produced by deterministic, human-validated code to curb hallucination and silent failure.

The first implementation, DarkAgent-PT, runs three stages. A proposal stage (proposal, librarian/literature-review, and critic sub-agents) takes either a fully specified model or a looser "idea." A branch-dependent FOPT-PTA stage computes the effective potential, bounce action, and cosmological phase-transition parameters with a semi-analytic backend, then uses `PTArcade` to run an MCMC fit against the NANOGrav nanohertz gravitational-wave background. A novel astroparticle stage adds a constraint sub-agent (combining particle-physics, astrophysical, and cosmological bounds) and a prior sub-agent that audits assumptions, priors, approximations, and validity domains across the whole workflow, followed by a report sub-agent that writes a LaTeX summary.

## Validation

The authors carried out a traditional human analysis of the same problem with the same deterministic backend and compared posterior distributions, finding DarkAgent-PT reproduced the human Bayesian posteriors closely. They re-ran the same tasks across multiple LLM providers and repeatedly with the same prompt over March–June 2026: state-of-the-art models (Claude Code Opus 4.8, Codex GPT-5.5) completed the full workflow almost autonomously, while a less capable model (Mistral Vibe, mistral-medium-3.5) needed stronger guidance and was less reliable at identifying constraints and implicit assumptions. Fail-safe behavior was tested — given a model incompatible with the backend, the orchestrator stopped and reported the incompatibility rather than forcing an incorrect branch. A noted failure mode: when using web tools for literature search, the LLMs were observed to hallucinate some references in the final report.

## Notable results

- Identified inconsistencies in some published NANOGrav fits in the literature and produced novel fits based on the dissipative bulk-flow gravitational-wave template.
- Autonomously and correctly rejected the commonly used sound-wave spectrum template in the regime where it is invalid, selecting the dissipative bulk-flow template instead.
- Audited implicit pipeline assumptions, flagging missing treatments (renormalization-scale choice, daisy resummation, coupling running, gauge dependence, bubble-wall velocity) and identifying constraint analyses still needed (e.g., kinetic/scalar mixing) without fabricating their impact.

## Primary paper

[Lucente, Pascoli, Sala, Zandi, "DarkAgents: towards an agentic system for theoretical astroparticle physics," arXiv:2606.11157](https://arxiv.org/abs/2606.11157).

## Other references

_None yet._

## Code

[Repository](https://github.com/PhysicsZandi/DarkAgents) — open source, including test prompts and example runs (scripts, reports, handoffs, figures) for all LLM providers.
