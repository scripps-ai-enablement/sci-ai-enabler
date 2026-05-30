---
title: AMASE
parent: Systems
grand_parent: AI scientists
nav_order: 5
affiliation: University of Maryland Department of Materials Science and Engineering and Maryland Quantum Materials Center (Takeuchi group), with the National Institute of Standards and Technology
lifecycle_stages: [Multi-stage]
autonomy: Fully autonomous
domain: Materials science (thin-film phase diagrams)
availability: Open source — code and data released as part of the manuscript
last_verified: 2026-05-30
---

# AMASE

Autonomous Materials Search Engine that closes the experiment–theory loop in real time by interleaving robotic thin-film X-ray diffraction with CALPHAD-based Gibbs-free-energy phase-diagram prediction to autonomously map binary phase diagrams.

| | |
|---|---|
| **Affiliation** | University of Maryland MSE and Maryland Quantum Materials Center (Takeuchi group), with NIST (Kusne, McDannald) |
| **First introduced** | 2024-10 (arXiv:2410.17430) |
| **Lifecycle stages** | Multi-stage (active-learning experiment selection, robotic XRD measurement, peak detection and classification, CALPHAD thermodynamic update) |
| **Autonomy level** | Fully autonomous — a single live run completes without human intervention beyond mounting the composition-spread wafer |
| **Domain focus** | Materials science — thin-film eutectic binary phase diagrams; demonstrated on Sn–Bi |
| **Availability** | Open source — data and code released as part of the manuscript |

## Approach

AMASE runs threaded cyclical tasks that alternate measurement and thermodynamic computation:

- **Active-learning composition selection.** A variational Gaussian Process Classifier (VGPC) uses the current CALPHAD-evaluated phase boundary as its prior and selects the next composition to probe at a fixed temperature; convergence is signalled when the tracked Bi (012) or Sn (101) peak drops below noise on one side of a candidate boundary and is confirmed at ±0.01 in composition.
- **XRD measurement and peak detection.** A modified 1D YOLO object-detection model (adapted from computer vision) extracts peak positions, FWHMs, and intensities from each diffraction pattern; peaks are indexed against the Inorganic Crystal Structure Database.
- **CALPHAD update.** Once a phase-boundary composition is identified at a temperature, Thermo-Calc minimises Gibbs free energies of the three phases (β-Sn, Bi, liquid) using Redlich–Kister polynomials, run ten times to estimate uncertainty; the updated phase diagram is fed back as the prior for the next iteration.
- **Next-temperature selection.** A GP acquisition function in exploration mode chooses the next temperature within a 30 °C window above the current one, using uncertainty in the calculated solvus composition.
- **End-point detection.** A separate GP classifier detects vanishing of the solvus phase boundary and triggers a jump to the liquidus search routine.

The phase-boundary-search-routine averages six XRD iterations and ~40 min per temperature.

## Validation

End-to-end live demonstration on the Sn–Bi thin-film binary system. AMASE constructed the thin-film phase diagram in a single 8 h 22 min autonomous run consisting of 66 XRD measurements across 11 temperature points, deliberately seeded only with a 0.71 < x < 0.95 Sn-rich composition spread and the bulk phase-diagram free-energy functional forms. The predicted eutectic point was independently validated with a separate thin-film spread sample focused near x = 0.5.

## Notable results

- AMASE-predicted eutectic point at Sn 53.3 % ± 2 % and 133.1 °C ± 1 °C agreed within 3 % with the independently measured 55.5 % ± 1.5 %, 133.2 °C ± 10 °C — and deviated from the bulk eutectic (59.5 %, 140.7 °C) as expected for a thin film.
- **6-fold reduction** in experiments versus an exhaustive 10 °C × composition grid (66 vs ~400 XRD measurements; 8 h vs >60 h continuous run), critical for volatile Sn–Bi films that would oxidise during longer thermal exposure.
- Ablation against a GP-only navigation workflow (with post-hoc CALPHAD extrapolation): over 20 simulated runs, AMASE used significantly fewer measured points with tighter distributions, attributed to CALPHAD's ability to extrapolate phase-diagram features that GP alone cannot skip over.

## Primary paper

[Liang et al., "Real-time experiment-theory closed-loop interaction for autonomous materials science" (AMASE), arXiv:2410.17430](https://arxiv.org/abs/2410.17430).

## Other references

_None yet._

## Code

Data and code released as part of the manuscript ("Data that supports the finding of this study as well as the code have been made available as a part of the manuscript").
