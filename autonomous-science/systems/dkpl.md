---
title: DKPL
parent: Systems
grand_parent: AI scientists
nav_order: 53
affiliation: Oak Ridge National Laboratory
org_short: Oak Ridge
lifecycle_stages: [Experiment design, Analysis]
validation_type: Wet-lab
autonomy: Semi-autonomous
domain: Materials (nanoscale microscopy, ferroelectrics)
domain_group: Chemistry & materials
availability: Unknown
access: Unknown
tagline: Autonomous-microscopy framework that learns a utility from expert pairwise judgements to plan nanoscale experiments.
last_verified: 2026-06-02
---

# DKPL

Deep-Kernel Pairwise Learning — an autonomous-microscopy framework that replaces hand-engineered scalar Bayesian-optimization objectives with a latent utility function learned from expert pairwise judgements, and uses it to plan subsequent nanoscale experiments.

| | |
|---|---|
| **Affiliation** | Oak Ridge National Laboratory (Center for Nanophase Materials Sciences); University of Tennessee-Oak Ridge Innovation Institute; Institute of Science Tokyo; NTNU; University of Duisburg-Essen; Research Alliance Ruhr |
| **First introduced** | 2026-05 (arXiv:2605.21820) |
| **Lifecycle stages** | Experiment design, Analysis |
| **Autonomy level** | Semi-autonomous — closes the active-learning loop autonomously but is driven by intermittent expert pairwise comparisons |
| **Domain focus** | Self-driving microscopy for nanoscale materials, with case studies in ferroelectric domain-wall character |
| **Availability** | Unknown — no public code link in the preprint |

## Approach

DKPL targets a well-known failure mode of Bayesian-optimization-based self-driving laboratories: the requirement that experimental outcomes (1D spectra, 2D images, hyperspectral data) be reduced to a scalar descriptor before active learning can proceed. Predefined scalar metrics can introduce information loss, false optima, and misleading outliers, and many scientifically important phenomena resist scalar formalization. DKPL replaces the scalar objective with a **latent utility function** inferred from expert pairwise comparisons.

A neural-network feature extractor maps high-dimensional raw data (e.g., microscopy image patches) into a low-dimensional latent representation; a **pairwise Gaussian process** operates on the latent space, learning from comparisons in which the expert indicates which of two experimental outcomes is more promising. The GP provides principled uncertainty for active learning. Neural-network and GP hyperparameters are trained jointly by maximizing marginal likelihood. Each iteration samples two new candidates via Upper Confidence Bound (default β = 5), compares them with each other and with the current best, predicts a new utility map over 1,000 epochs, and continues. DKPL supports **indifference judgements** (tolerance band where two outcomes are treated as equally preferred) and **confidence-weighted comparisons** (weak/moderate/strong weights so low-confidence feedback contributes less).

## Validation

First benchmarked on a known-ground-truth dataset (band-excitation piezoresponse spectroscopy on PbTiO3 thin films) to evaluate whether DKPL reconstructs physically relevant domain structures from preference feedback. Then applied to autonomous investigation of ferroelectric domain-wall character in (a) bismuth ferrite and (b) erbium manganite.

## Notable results

- DKPL efficiently identified high-information measurement regions without predefined scalar metrics on the ground-truth BEPS dataset.
- In bismuth ferrite, DKPL distinguished between **high and low characteristic domain-wall angles**.
- In erbium manganite, DKPL discovered both **head-to-head and tail-to-tail domain-wall character** — multidimensional polarization behaviors that resist scalar description.

## Primary paper

[Bulanadi, Baxter, Biswas, Funakubo, Meier, Schultheiß, Vasudevan, Liu, "Beyond Scalar Objectives: Expert-Feedback-Driven Autonomous Experimentation for Scientific Discovery at the Nanoscale," arXiv:2605.21820 (2026)](https://arxiv.org/abs/2605.21820).

## Other references

_None yet._

## Code

Not released as part of the preprint.
