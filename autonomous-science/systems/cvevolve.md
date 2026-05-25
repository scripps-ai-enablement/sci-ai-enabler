---
title: CVEvolve
parent: Systems
grand_parent: AI scientists
nav_order: 17
affiliation: Advanced Photon Source, Argonne National Laboratory (Du, Cherukara et al.)
lifecycle_stages: [Analysis]
autonomy: Semi-autonomous
domain: Scientific imaging — x-ray fluorescence microscopy, x-ray diffraction, high-energy diffraction microscopy
availability: Unknown
last_verified: 2026-05-24
---

# CVEvolve

Autonomous agentic harness from Argonne's Advanced Photon Source that discovers and refines scientific data-processing algorithms for unstructured experimental images via zero-code, lineage-aware search with optional visual inspection of intermediate outputs.

| | |
|---|---|
| **Affiliation** | Advanced Photon Source, Argonne National Laboratory ([paper](https://arxiv.org/abs/2605.11359)) |
| **First introduced** | 2026-05 (arXiv:2605.11359, dated 2026-05-12) |
| **Lifecycle stages** | Analysis — autonomous discovery of executable image-processing and feature-detection algorithms for downstream scientific interpretation |
| **Autonomy level** | Semi-autonomous — the user supplies a task description, a data directory, and optional metric hints; CVEvolve runs an open-ended search to a fixed round budget with optional holdout testing |
| **Domain focus** | Unstructured scientific imaging at synchrotron beamlines: image registration, peak detection, segmentation |
| **Availability** | Unknown — no public repository disclosed in the preprint |

## Approach

A controller wraps an LLM agent (Claude Opus 4.6 in all reported cases) that uses code-execution, evaluation, history, image-rendering, and web-search tools. Work is organized into three stages.

- **Preparation stage.** The agent inspects task data, examines representative images, fixes the primary optimization metric from the task description or user hints, and builds a minimal evaluation harness for later rounds. It can construct and manage its own local runtime (e.g., via `uv`) including dependency installation.
- **Baseline stage.** User-provided or agent-suggested baseline algorithms are evaluated; results are stored in a persistent SQL search-state database so later rounds avoid redundant reevaluation.
- **Algorithm development stage.** Each round picks one of *generate* (broad exploration), *tune* (exploitative refinement of a strong parent), or *evolve* (crossover of two parents). Branching is history-driven, with periodic forced generate rounds to preserve exploration. Parents are sampled with **lineage-aware stochastic sampling** inspired by MAP-Elites: a Gibbs distribution `p_i ∝ exp(−(r_i − 1)/τ)` over ranks, with a same-lineage penalty `λ^m_i` reducing the weight of candidates from already-selected lineages during evolve crossover. The agent starts each round with a fresh context (only the system and task prompts) to control context size.

CVEvolve exposes file-system tools, environment management/execution tools, an **image viewer** that handles floating-point/TIFF data with percentile dynamic-range selection and log scaling, search-state tools backed by a SQL database, and web-search tools (arXiv, Semantic Scholar, Tavily). An image-follow-up middleware injects rendered images back into the conversation when a tool returns an image path. An optional **holdout test** runs in a separate temporary workspace handled by a dedicated agent so the development agent never sees holdout data.

## Validation

Three case studies on real synchrotron data: (1) x-ray fluorescence microscopy translational image registration, (2) Bragg peak detection in x-ray diffraction images, (3) polycrystalline diffraction image segmentation. Run for 20–40 rounds with development and holdout sets; comparisons against task-appropriate baselines (brute-force error minimization, phase correlation) and against OpenEvolve (an open-source AlphaEvolve implementation) on the registration task.

## Notable results

- **XRF image registration.** Best candidate average Euclidean error **0.12** on the holdout set vs. **0.98** (brute force), **5.59** (phase correlation), and **0.23** (OpenEvolve at 500 iterations) — a roughly **eightfold reduction** over the best baseline.
- **Bragg peak detection.** Holdout F1 lifted from **0.298** (baseline) to **0.788** for the round-5 candidate, with precision improving from 0.237 → 0.839 and recall from 0.400 → 0.743. The holdout-test agent surfaced over-optimization that began after round 9 on the development image, demonstrating the value of holdout monitoring on small development sets.
- **Diffraction image segmentation.** Discovered a workflow combining radial-background subtraction, multi-pass peak detection (LoG / connected components / proximity-based recovery / SNR maxima), and prominence/shape validation; weighted IoU improves substantially over the baseline thresholding approach over 40 rounds.

## Primary paper

[Du et al., "CVEvolve: Autonomous Algorithm Discovery for Unstructured Scientific Data Processing," arXiv:2605.11359](https://arxiv.org/abs/2605.11359).

## Other references

_None yet._

## Code

Not released at preprint time.
