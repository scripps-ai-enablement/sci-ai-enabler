---
title: LabOS
parent: Systems
grand_parent: AI scientists
nav_order: 29
affiliation: Stanford University School of Medicine and Princeton AI Lab, with Oregon State University, University of Washington, and NVIDIA (corresponding authors Le Cong and Mengdi Wang)
org_short: Stanford / Princeton
lifecycle_stages: [Multi-stage]
validation_type: Mixed
autonomy: Semi-autonomous
domain: Biology & medicine (cancer immunology, stem-cell engineering; also materials science)
domain_group: Biology & medicine
availability: Open source (GitHub)
access: Open source
tagline: AI-XR co-scientist pairing self-evolving agents with smart glasses to reason about and act in the physical lab.
last_verified: 2026-06-09
---

# LabOS

An AI-XR co-scientist that couples a self-evolving multi-agent system for digital-lab reasoning with extended-reality smart glasses, a vision-language model, and robotics, letting AI perceive, reason about, and assist in the physical laboratory.

| | |
|---|---|
| **Affiliation** | Stanford University School of Medicine and Princeton AI Lab, with Oregon State, U. Washington, and NVIDIA ([paper](https://arxiv.org/abs/2510.14861)) |
| **First introduced** | 2025-10 (arXiv preprint; also bioRxiv 2025.10.16.679418) |
| **Lifecycle stages** | Multi-stage — closes the loop from hypothesis generation and experiment design through data analysis to human-in-the-loop physical execution and automated documentation |
| **Autonomy level** | Semi-autonomous — the digital agents reason and analyze autonomously; physical execution is human-in-the-loop via XR glasses, with an optional cobot module |
| **Domain focus** | Biomedical research (cancer immunology, stem-cell engineering); demonstrated in materials-science labs |
| **Availability** | Open source — GitHub |

## Approach

LabOS has two coupled modules. The digital (dry) lab is a self-evolving multi-agent system that extends the STELLA framework: a Manager/Planner agent decomposes scientific objectives into structured steps, a Developer agent generates and runs Python for bioinformatics analyses, and a Critic agent evaluates and refines intermediate results in an iterative loop. A Tool-Creation agent autonomously identifies, tests, and integrates new analytical tools, databases, and APIs from sources like PubMed into a shared "Tool Ocean," while a Template Library of successful reasoning workflows lets the system generalize from prior solutions — together enabling self-improvement that scales with inference-time compute.

The physical (wet) lab module connects AI reasoning to the bench through AR/XR smart glasses and multimodal sensing. Egocentric video is streamed in 5–10 s segments to a GPU server, where a lab-specialized vision-language model (LabOS-VLM, post-trained from Qwen-VL via SFT then GRPO reinforcement learning) interprets the scene, verifies actions against gold-standard protocols, and returns structured JSON feedback rendered on the glasses. LabOS also builds 3D/4D digital twins of lab workflows using MapAnything and 3D Gaussian splatting, and includes a proof-of-concept cobot module (xArm + gripper) for automating repetitive steps with human–robot handover.

## Validation

On biomedical reasoning benchmarks the digital agent reports approximately 32% on Humanity's Last Exam: Biomedicine, 61% on LAB-Bench: DBQA, and 65% on LAB-Bench: LitQA, outperforming the next-best models by up to 8%, with accuracy improving under test-time scaling. The authors introduce LabSuperVision (LSV), an expert-annotated benchmark of >200 egocentric lab-video sessions (recorded by 7 researchers across bench, tissue-culture, and instrument settings) for evaluating lab perception and reasoning; leading commercial VLMs scored poorly (Gemini-2.5 Pro reached only 2.86/5 on protocol alignment), motivating LabOS-VLM, whose 235B variant exceeds 90% error-detection accuracy on held-out data and outperforms Claude Opus-4.1, GPT-5, and Gemini 2.5 Pro on the evaluated metrics.

For wet-lab validation, LabOS generated hypotheses and analyzed functional-screening data to nominate CEACAM6 as a natural-killer-cell cancer-immunotherapy target, which was confirmed in a physical NK-tumor killing assay. A second study identified ITSN1 as a regulator of cell fusion, and a third had researchers wear smart glasses during stem-cell engineering, where LabOS provided step-level guidance and flagged operational deviations (e.g., sterile-technique breaches, incorrect incubation times).

## Notable results

- Agent-nominated CEACAM6 validated as an NK-cell anti-tumor target in a physical killing assay; ITSN1 identified as a cell-fusion regulator.
- LabOS-VLM-235B exceeds 90% error-detection accuracy on held-out lab video, outperforming Claude Opus-4.1, GPT-5, and Gemini 2.5 Pro.
- New benchmarks: ~32% on HLE: Biomedicine, 61% LAB-Bench: DBQA, 65% LAB-Bench: LitQA; plus the LabSuperVision (LSV) lab-video benchmark.

## Primary paper

[Cong, Smerkous, Wang et al., "LabOS: The AI-XR Co-Scientist That Sees and Works With Humans," arXiv:2510.14861 (2025)](https://arxiv.org/abs/2510.14861).

## Other references

- [bioRxiv preprint 2025.10.16.679418](https://www.biorxiv.org/content/10.1101/2025.10.16.679418v1)

## Code

[Repository](https://github.com/zaixizhang/LabOS).
