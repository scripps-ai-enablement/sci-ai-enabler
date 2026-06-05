---
title: MAD
parent: Systems
grand_parent: AI scientists
nav_order: 54
affiliation: University of Maryland; National Institute of Standards and Technology (NIST)
org_short: Maryland
lifecycle_stages: [Experiment design, Analysis]
validation_type: Wet-lab
autonomy: Fully autonomous
domain: Materials (phase-change memory thin films)
domain_group: Chemistry & materials
availability: Partial — some Python integration code on GitHub
access: Code on request
tagline: Closed-loop framework orchestrating multiple characterization instruments for thin-film materials discovery.
last_verified: 2026-06-02
---

# MAD

Multi-instrument Autonomous Discovery — a closed-loop framework that orchestrates multiple characterization instruments as cooperating agents over a shared probabilistic posterior, performing simultaneous structural mapping and functional-property optimization for thin-film materials discovery.

| | |
|---|---|
| **Affiliation** | University of Maryland (Department of Materials Science and Engineering; IREAP; Maryland Quantum Materials Center); NIST Materials Measurement Science Division |
| **First introduced** | 2026-05 (arXiv:2605.18033) |
| **Lifecycle stages** | Experiment design, Analysis (active-learning experiment selection plus joint structural/property inference) |
| **Autonomy level** | Fully autonomous over the closed loop; humans set the optimization objective |
| **Domain focus** | Combinatorial thin-film materials discovery — demonstrated on the Mn-Sb-Te (MST) ternary as a candidate phase-change memory system |
| **Availability** | Partial — Python integration code released on GitHub; full software stack not specified |

## Approach

MAD addresses the lack of real-time data-fusion in multi-instrument autonomous experimentation. Two compositionally identical Mn-Sb-Te thin-film spreads (177 4×4 mm gridded regions, compositions 7–78 % per element) are mounted on separate instruments — one annealed for x-ray diffraction (XRD), one amorphous for two-terminal electrical-resistance measurement on a contact probe station. The instruments are connected to a central main agent over a server–client network, with command-driven data exchange and centralized computation. In each iteration, the central controller performs joint inference across two property domains using a **multi-output Gaussian process** with a **co-regionalization kernel** that explicitly models structure-property correlations, while distinct acquisition functions drive each task: structural phase mapping (maximize knowledge of the crystal-structure distribution using non-negative matrix factorization) and functional optimization (find the composition with maximum amorphous-state resistance Ramo, a figure of merit for phase-change memory).

A faster instrument idles while awaiting the slower one (here, the diffractometer is the bottleneck); the authors discuss a multi-agent implementation that would mitigate this asymmetry by running asynchronous closed loops. The output probabilistic posterior provides uncertainty quantification that flows between structure and property tasks.

## Validation

Live closed-loop run on the Mn-Sb-Te ternary thin-film library — a previously unexplored materials system for phase-change memory, with candidate magnetic topological insulator MnSb2Te4 and potential room-temperature magnetic phase-change memory materials.

## Notable results

- A **single live run** simultaneously achieved phase mapping and materials optimization within **5 hours**, identifying synthesis-process-structure-property relationships in **25 closed-loop iterations**.
- Reports a **seven-fold speed-up** over autonomous experimentation employing independent Gaussian processes and over conventional grid mapping (which typically takes several days).
- Demonstrates simultaneous reconstruction of XRD patterns and quantitative elucidation of structure-property relationships across a multi-component ternary composition space.

## Primary paper

[Lee, Liang, Kim, McDannald, Ocampo, Kusne, Takeuchi, Rios, "Real-time Multi-instrument Autonomous Discovery of Novel Phase-change Memory Materials," arXiv:2605.18033 (2026)](https://arxiv.org/abs/2605.18033).

## Other references

_None yet._

## Code

Some custom Python data-integration components released on GitHub per the paper; primary URL not specified in the preprint.
