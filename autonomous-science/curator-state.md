---
title: Curator state
parent: AI scientists
nav_exclude: true
---

# Curator state

## Recently surfaced

- **LEAP** (added 2026-06-01) — Renmin University of China expert-in-the-loop closed-loop framework coupling a domain-specialized LLM (Perovskite-RL, SFT+RL on perovskite-additive literature) with Bayesian optimization for iterative perovskite-solar-cell precursor-additive discovery; three rounds of wet-lab validation produced mean device PCEs of 20.13% (6-CDQ) and 20.87% (2-CNA) vs 19.25% control with a 21.32% champion; mechanism-consistency benchmark 78.1% vs ≤50% for general-purpose baselines.
- **AutoScientists** (added 2026-06-01) — Harvard (Zitnik lab) decentralized multi-agent system in which agents self-organize into teams around promising hypotheses, share a global experimental state, and run long-horizon computational experiments without a central planner; +8.33 percentile-point gain over Autoresearch on BioML-Bench (74.4% mean, 24 tasks), 1.9× faster to target val_bpb on GPT nanochat training, +12.5% Spearman on ACE2-Spike fitness with +6.5% averaged across all 217 ProteinGym assays. Code at github.com/mims-harvard/AutoScientists.
- **AutoLLMResearch** (added 2026-06-01) — Notre Dame agentic framework trained via reinforcement learning over a multi-fidelity LLMConfig-Gym environment (>1M GPU-hours of verifiable experiments) so it can extrapolate from cheap low-fidelity LLM experiments (≤3B / 10B tokens) to efficient configuration of expensive ones (7B / 20B tokens); addresses configuration-space and optimization-landscape shifts that defeat prior HPO and meta-learning. Code at github.com/taichengguo/AutoLLMResearch.
- **AtomisticSkills** (added 2026-05-31) — MIT (Gómez-Bombarelli and Coley groups) with Shell open-source agent harness empowering general-purpose AI coding agents to conduct atomistic research across materials, chemistry, and drug discovery via 100+ curated MCP tools and skills; validated on six campaigns (Li-ion solid-state electrolyte design, MOF CO2 capture screening, autonomous MLIP benchmarking and fine-tuning, structure-based virtual screening, multimodal XRD analysis, Fe-oxide OER catalyst screening).
- **ScientistOne** (added 2026-05-31) — Google Cloud AI Research end-to-end autonomous research system designed around the Chain-of-Evidence (CoE) standard; achieves 0/337 hallucinated references, 12/12 score verification, 14/15 method-code alignment across 75 audited papers from five systems on five ADRS frontier ML tasks; generalizes to medical imaging, fine-grained recognition, 3D perception, parameter-constrained LM with state-of-the-art on Parameter Golf and gold medals on MLE-Bench.

## Flagged for review

_None._

## Deferred — next-run priority

- **CORAL** (arXiv:2604.01658, Apr 2026) — Multi-agent evolutionary discovery framework from MIT/NUS/Singapore-MIT. PDF archived at `sources/2604.01658v1.pdf`; reported on Anthropic's kernel-engineering task and Polyominoes packing, not strictly natural-science hypothesis generation. Add when a more science-leaning evaluation surfaces.
- **AIDO.Harness** (bioRxiv 2026.04.20.719735) — Autonomous ML-model construction for biomedical tasks, framed as POMDP. Not downloaded; revisit next pass.
- **SAGA** (arXiv:2512.21782) — Goal-evolving autonomous discovery agent. Not downloaded; verify scope.
- **Virtual Lab** (Stanford / CZ Biohub, *Nature* 2025) — referenced in Kosmos and AgenticSciML papers; PDF blocked by Cloudflare on prior run.
