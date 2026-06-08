---
title: Ax-Prover
parent: Systems
grand_parent: AI scientists
nav_order: 12
affiliation: Axiomatic AI (with ICFO, MIT, ICREA)
org_short: Axiomatic AI
lifecycle_stages: [Analysis]
validation_type: Benchmark
autonomy: Semi-autonomous
domain: Math & symbolic (formal theorem proving in Lean; quantum physics)
domain_group: Math & symbolic
availability: Open source
access: Open source
tagline: Multi-agent Lean theorem prover that gives general-purpose LLMs Lean tools to verify proofs across math and quantum physics.
last_verified: 2026-06-08
---

# Ax-Prover

A multi-agent system that equips general-purpose LLMs with Lean theorem-proving tools via the Model Context Protocol, generating formally verified proofs across mathematics and quantum physics either autonomously or in collaboration with domain experts.

| | |
|---|---|
| **Affiliation** | Axiomatic AI, with ICFO, MIT, and ICREA ([paper](https://arxiv.org/abs/2510.12787)) |
| **First introduced** | 2025-10 (arXiv:2510.12787; v4 2026-05-22) |
| **Lifecycle stages** | Analysis (autonomous formal reasoning: proof sketching, formalization, and machine-checked verification of given theorems) |
| **Autonomy level** | Semi-autonomous (runs autonomously as a prover or collaboratively with experts via standard human–agent interaction) |
| **Domain focus** | Formal theorem proving in Lean — mathematics and quantum physics |
| **Availability** | Open source — listed among open-sourced agents on the PutnamBench leaderboard |

## Approach

Ax-Prover is built around three role-specialized agents driven by the same LLM under distinct prompts: an Orchestrator, a Prover, and a Verifier. The Orchestrator schedules work — it forwards an unproven Lean statement to the Prover, routes diagnostic feedback from the Verifier, and decides when to stop the refinement loop (on a certified proof or when attempts exceed a configurable threshold). The Prover is the constructive core: it scans the input file for `sorry` placeholders, drafts a natural-language proof sketch, formalizes each step into Lean `have` statements, and substitutes Lean tactics step by step, checking each with diagnostic tools. The Verifier is an independent gatekeeper that compiles the file and certifies a proof only if no level-1 error and no remaining `sorry`/`admit` exist.

Rather than training a specialized prover, Ax-Prover connects frontier LLMs (Claude Sonnet 4 / 4.5 in the experiments) to Lean through the `lean-lsp-mcp` MCP server, plus filesystem tools. This lets the agent inspect goals, search Mathlib (via Loogle and Leansearch), diagnose errors, and verify proofs against the newest Mathlib version without retraining — avoiding the over-specialization and Mathlib-version brittleness of distilled prover models, while preserving tool use and conversational interaction.

## Validation

Evaluated as an autonomous prover at pass@1 against frontier-LLM and specialized-prover baselines (Claude Sonnet 4, DeepSeek-Prover-V2-671B, Kimina-Prover-72B) on two public benchmarks (NuminaMath-LEAN, PutnamBench) and two new Lean datasets the authors introduce: AbstractAlgebra (100 problems from Dummit & Foote) and QuantumTheorems (134 quantum-theory problems). Two researcher-facing case studies in classical and quantum cryptography demonstrate collaborative use, formalizing a matrix branch-number definition and a QKD entropy bound with domain experts. All proofs were checked by an external Lean compiler.

## Notable results

- PutnamBench: 14% accuracy, the top open-source model and third overall, solving 92 of 660 problems (avg. 182 lines) at a fraction of the compute of leaders Hilbert and Seed-Prover.
- QuantumTheorems: 96% overall (100% easy, 92% intermediate), versus 61% for DeepSeek-Prover and 57% for Kimina — a domain where specialized provers fail to generalize to custom physics definitions absent from Mathlib.
- AbstractAlgebra: 64% overall, outperforming all baselines.

## Primary paper

[Breen, Del Tredici, McCarran et al., "Ax-Prover: A Deep Reasoning Agentic Framework for Theorem Proving in Mathematics and Quantum Physics," arXiv:2510.12787](https://arxiv.org/abs/2510.12787).

## Other references

_None yet._

## Code

Open source — listed among open-sourced agents on the [PutnamBench leaderboard](https://trishullab.github.io/PutnamBench/).
