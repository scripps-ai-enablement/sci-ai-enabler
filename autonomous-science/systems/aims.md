---
title: AIMS
parent: Systems
grand_parent: AI scientists
nav_order: 7
affiliation: Stanford University (Zhi-Xun Shen group, Physics / Applied Physics / Geballe Laboratory and SIMES at SLAC) with MIT Physics and Materials Science (Zhurun Ji), UT Austin, University of Florida, Boston College, and NYU
org_short: Stanford
lifecycle_stages: [Multi-stage]
validation_type: Wet-lab
autonomy: Semi-autonomous
domain: Condensed-matter physics — cryogenic microwave impedance microscopy of twisted bilayer MoSe2
domain_group: Physical sciences
availability: Code on request — data and code available from the corresponding authors on request
access: Code on request
tagline: Uncertainty-aware closed-loop experimentalist driving a cryogenic microwave impedance microscope on quantum materials.
last_verified: 2026-08-01
---

# AIMS

Closed-loop LLM agent that operates a cryogenic microwave impedance microscope end to end, converting three distinct kinds of experimental uncertainty — where the tip is, where to measure, and which physical mechanism explains the data — into the next concrete action.

| | |
|---|---|
| **Affiliation** | Stanford University Physics / Applied Physics and SIMES at SLAC, with MIT, UT Austin, University of Florida, Boston College, and NYU |
| **First introduced** | 2026-07 (arXiv:2607.16544) |
| **Lifecycle stages** | Multi-stage (instrument navigation, measurement selection, mechanism attribution) |
| **Autonomy level** | Semi-autonomous — autonomous where the task is well posed; researchers supply the guiding question, seed hypotheses, and experimental safeguards |
| **Domain focus** | Quantum matter — correlated insulating states and generalized Wigner crystals in twisted bilayer MoSe<sub>2</sub> |
| **Availability** | Code on request — the paper states data and code are available from the corresponding authors upon request |

## Approach

AIMS ("AI agent for Inference and Measurement in Science") links three nested loops, each keyed to a dominant uncertainty. The **navigation loop** addresses uncertain perception of tip position: instrument control is exposed through an MCP server, and the agent scans, predicts tip position by automated localization, moves, and re-scans until it reaches the target. When positional uncertainty is elevated it autonomously invokes recovery strategies — re-scanning at increased tip lift, or Gaussian-process reconstruction of a higher-resolution, higher-contrast image. The **measurement loop** addresses sample inhomogeneity: a large-area scan swept across gating voltage isolates strongly correlated regions, then grid spectroscopy maps local twist angle and disorder, scoring each site by the quality of its correlated features so that sample-quality uncertainty becomes a ranked landscape of candidate measurement positions. The **discovery loop** treats interpretation as evidence updating rather than a binary verdict: the agent reviews its database of experimental data, literature, and tools, ranks researcher-seeded and self-generated hypotheses by data-derived evidence, identifies the specific evidence gap when the data are insufficient, and proposes the follow-up calculation or measurement most likely to close it.

The model is accessed through LibreChat via API, with instrument control and analysis exposed as tools; guardrails prevent the agent from taking uncontrolled coding actions that could interfere with a running cryogenic experiment while preserving its ability to detect and handle failures.

## Validation

Evaluated against independent controls rather than task completion alone. Navigation was repeated from different initial positions and after cooldown to cryogenic temperature on a real device. Measurement selection was tested against the mapped twist-angle and generalized-Wigner-crystal-score landscape of a real twisted bilayer MoSe<sub>2</sub> sample. Mechanism attribution was tested by having the agent commission exact-diagonalization calculations that vary hopping and Coulomb scales, and by retaining sample morphology as a secondary testable variable rather than discarding it.

## Notable results

- Reduced total sample-navigation time from roughly 10 hours (human-driven with scripted instrument control) to roughly 4 hours, principally through fewer required scans under more confident position estimation and a more progressive movement policy.
- Autonomously invoked Gaussian-process regression to avert false position predictions caused by low image quality after cryogenic cooldown.
- Prioritized a quantum-fluctuation-renormalized origin for the anomalously robust ν = 1/2 crystal, and showed that twist disorder controls the spatial strength of the correlated response rather than the observed melting hierarchy.

## Primary paper

[Qiu, Suh et al., "AIMS: An uncertainty-aware AI experimentalist for quantum matter," arXiv:2607.16544](https://arxiv.org/abs/2607.16544).

## Other references

_None yet._

## Code

Not released — available from the corresponding authors on request.
