---
title: Curator state
parent: AI scientists
nav_exclude: true
---

# Curator state

## Recently surfaced

- **AutoSci** (added 2026-06-02) — Peking University (PKUDAIR) memory-centric agentic system for the full scientific research lifecycle. Four modules (SciMem schema-governed memory, SciFlow harness-based five-stage executor with 30+ skills, SciDAG DAG-shaped multi-agent operators, SciEvolve versioned self-evolution) and a Trust Guard on all memory writes. Two end-to-end case studies in GPU kernel optimization (6.3/10 automated ICLR-review) and biomedical drug discovery (5.8/10). Open source at github.com/skyllwt/AutoSci.
- **VIS Co-Scientist** (added 2026-06-02) — LLNL / Vanderbilt / Notre Dame end-to-end agentic harness that autonomously designs custom visualization applications (VIS Apps) given only a dataset and high-level task description. Orchestrator + EDA / Planner / Environment Builder / VIS Designer / Evaluator subagents with Playwright-based browser validation and a hierarchical markdown memory. Validated on IEEE SciVis Contests 2021, 2023, 2024, and 2026 (climate, materials, sonar, neuroscience, mantle convection).
- **DKPL** (added 2026-06-02) — Oak Ridge National Laboratory deep-kernel pairwise-learning framework for self-driving microscopy that replaces hand-engineered scalar BO objectives with a latent utility function learned from expert pairwise judgements (with indifference and confidence-weighted comparisons). Demonstrated on band-excitation piezoresponse spectroscopy of PbTiO3 and on ferroelectric domain-wall character in bismuth ferrite and erbium manganite (discovering head-to-head and tail-to-tail wall character).
- **MAD** (added 2026-06-02) — University of Maryland / NIST Multi-instrument Autonomous Discovery framework coordinating XRD and electrical-resistance measurement as cooperating agents over a multi-output GP with co-regionalization kernel. A single live run on the Mn-Sb-Te ternary thin-film system achieved phase mapping and Ramo maximization in 5 hours across 25 closed-loop iterations — a seven-fold speed-up over independent-GP autonomous experimentation.
- **LEAP** (added 2026-06-01) — Renmin University of China expert-in-the-loop closed-loop framework coupling a domain-specialized LLM (Perovskite-RL, SFT+RL on perovskite-additive literature) with Bayesian optimization for iterative perovskite-solar-cell precursor-additive discovery; three rounds of wet-lab validation produced mean device PCEs of 20.13% (6-CDQ) and 20.87% (2-CNA) vs 19.25% control with a 21.32% champion; mechanism-consistency benchmark 78.1% vs ≤50% for general-purpose baselines.

## Flagged for review

_None._

## Deferred — next-run priority

- **CORAL** (arXiv:2604.01658, Apr 2026) — Multi-agent evolutionary discovery framework from MIT/NUS/Singapore-MIT. PDF archived at `sources/2604.01658v1.pdf`; reported on Anthropic's kernel-engineering task and Polyominoes packing, not strictly natural-science hypothesis generation. Add when a more science-leaning evaluation surfaces.
- **AIDO.Harness** (bioRxiv 2026.04.20.719735) — Autonomous ML-model construction for biomedical tasks, framed as POMDP. Not downloaded; revisit next pass.
- **SAGA** (arXiv:2512.21782) — Goal-evolving autonomous discovery agent. Not downloaded; verify scope.
- **Virtual Lab** (Stanford / CZ Biohub, *Nature* 2025) — referenced in Kosmos and AgenticSciML papers; PDF blocked by Cloudflare on prior run.
