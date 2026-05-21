---
title: AI CFD Scientist
parent: Systems
grand_parent: AI scientists
nav_order: 2
affiliation: Rensselaer Polytechnic Institute (Pan group)
lifecycle_stages: [Multi-stage, Writing]
autonomy: Semi-autonomous
domain: Computational fluid dynamics
availability: Open source
last_verified: 2026-05-21
---

# AI CFD Scientist

Open-source AI scientist for computational fluid dynamics that spans literature-grounded ideation, validated solver execution, vision-based physics verification, source-code modification, and figure-grounded writing in one inspectable OpenFOAM workflow.

| | |
|---|---|
| **Affiliation** | Rensselaer Polytechnic Institute, Pan group ([csml-rpi](https://github.com/csml-rpi)) |
| **First introduced** | 2026-05 (arXiv:2605.06607) |
| **Lifecycle stages** | Multi-stage (ideation + execution + verification + source-code modification) + Writing (LaTeX manuscript generation) |
| **Autonomy level** | Semi-autonomous — user supplies a research topic and optional base case; the system runs end-to-end across three coupled pathways |
| **Domain focus** | Computational fluid dynamics (OpenFOAM-based) |
| **Availability** | Open source — code, prompts, and run artifacts at [csml-rpi/cfd-scientist](https://github.com/csml-rpi/cfd-scientist) |

## Approach

A central Orchestrator dispatches work across three first-class pathways running on OpenFOAM via Foam-Agent: (i) regular experimentation via literature-aware ideation, requirement validation, mesh-independence gating, and parametric sweeps; (ii) code modification that patches and compiles case-local C++ model libraries (headers, custom solvers, function objects); (iii) open-ended discovery that wraps both modules in an outer hypothesis loop driven by an LLM hypothesis generator and cross-case analysis. A vision-language physics-verification gate inspects PyVista-rendered flow fields before any result is accepted, rerun, or written into a manuscript — addressing failure modes (wrong geometry, missing flow features, sign errors in derived quantities) invisible to solver logs. Outputs include a LaTeX manuscript synthesized against figure-grounded evidence.

## Validation

Five tasks under a shared GPT-5.5 backbone. In the open-ended task, the system autonomously discovered a Spalart–Allmaras runtime correction that reduced lower-wall Cf RMSE against DNS by 7.89% on the periodic hill at Re_h = 5600. A controlled planted-failure ablation showed the vision-language gate detected 14 of 16 silent failures missed by solver-level checks. Under matched LLM cost, two general AI-scientist baselines (ARIS, DeepScientist) executed partial CFD workflows but lacked the domain-specific validity gates.

## Notable results

- First open-source CFD-specific AI scientist spanning ideation through manuscript writing in a single inspectable workflow.
- Autonomous discovery of a Spalart–Allmaras turbulence-model runtime correction validated against DNS reference data.
- Vision-language physics gate catches silent solver failures invisible to solver logs.

## Primary paper

[Somasekharan et al., "AI CFD Scientist: Toward Open-Ended Computational Fluid Dynamics Discovery with Physics-Aware AI Agents," arXiv:2605.06607](https://arxiv.org/abs/2605.06607).

## Other references

_None yet._

## Code

[csml-rpi/cfd-scientist](https://github.com/csml-rpi/cfd-scientist) — code, prompts, and run artifacts.
