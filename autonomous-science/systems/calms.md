---
title: CALMS
parent: Systems
grand_parent: AI scientists
nav_order: 61
affiliation: Center for Nanoscale Materials and Advanced Photon Source, Argonne National Laboratory (Vriza, Prince, Zhou, Chan, Cherukara)
org_short: Argonne
lifecycle_stages: [Experiment design, Analysis]
validation_type: Wet-lab
autonomy: Semi-autonomous
domain: Materials science (synchrotron X-ray nanoprobe + robotic thin-film fabrication)
domain_group: Chemistry & materials
availability: Open source — code on GitHub (AdvancedPhotonSource/CALMS, sdl_agents branch)
access: Open source
tagline: Argonne multi-agent AI that operates an X-ray nanoprobe beamline and a robotic materials station, learning on the job from expert guidance.
last_verified: 2026-06-20
---

# CALMS

Argonne multi-agent framework, built on AutoGen, that autonomously operates two real scientific user facilities — a Hard X-ray Nanoprobe beamline and an N9 robotic thin-film station — orchestrating multistep workflows, interpreting multimodal data, and improving through in-context expert feedback.

| | |
|---|---|
| **Affiliation** | Argonne National Laboratory — Center for Nanoscale Materials and Advanced Photon Source ([GitHub](https://github.com/AdvancedPhotonSource/CALMS)) |
| **First introduced** | 2025-09 (arXiv:2509.00098; published npj Comput. Mater. 12, 160, 2026) |
| **Lifecycle stages** | Experiment design, Analysis |
| **Autonomy level** | Semi-autonomous — plans and executes multistep workflows but requests human approval before execution and learns from human feedback |
| **Domain focus** | Materials science — X-ray nanoprobe imaging and robotic polymer thin-film fabrication |
| **Availability** | Open source — code and data on GitHub |

## Approach

CALMS is built on the AutoGen (AG2) framework with vision-capable LLMs, structured into three levels: a human level (instructions, reference literature), an AI-agent level (orchestration over data, memories, and equipment protocols), and a physical-instrument level (an executor that runs generated code on the hardware and returns success/error feedback). Specialized agents include a code writer, a code critic, an administrator (human interaction + code execution), a paper scraper, an image explainer (vision analysis), and a teachability agent for memory retrieval.

A defining feature is *learning on the job*: human guidance is captured as input–output pairs and stored in a ChromaDB vector database via AutoGen's teachability mechanism, with a similarity-distance threshold added to avoid storing redundant memories. On a new task the agents perform a semantic similarity search to recall relevant past teachings. For the standardized X-ray experiments, the vision agent is seeded with expert-designed prompt templates encoding scanning and diffraction heuristics; for the open-ended robotic workflows, users explain procedures in real time and each instruction becomes a retrievable memory.

## Validation

Demonstrated live on two Argonne user facilities. At the Hard X-ray Nanoprobe (HXN) beamline, agents handled tasks of increasing complexity — translating a minimal natural-language prompt into a correct 2D-scan command (inferring start/end positions), and a cross-modality reasoning task identifying optimal scan regions by combining nano-diffraction (isolated bright spots) and nano-fluorescence (avoid clustered regions >10 µm) images. At the N9 robotic station, agents were given only low-level commands and the station layout (high-level routines removed) and had to compose full protocols, culminating in end-to-end fabrication of a defect-free PEDOT:PSS thin film after the literature-scraper agent extracted optimal coating parameters (90 °C, 1 mm/s) from a provided PDF.

Evaluation metrics covered code quality, correctness, execution, repeatability, and reproducibility across four trials per task, comparing GPT-4o, GPT-4o-mini, o3, and Claude 3.5.

## Notable results

- On multimodal cross-modality reasoning at the beamline, only the o3 model consistently identified optimal scan coordinates with high positional precision; GPT-4o excelled at language/function-calling tasks but was less reliable on image grounding.
- For the robotic station, memory-augmented "teachability" markedly improved performance on longer-horizon sequential tasks: GPT-4o and Claude 3.5 completed simple tasks zero-shot, but all models dropped sharply on complex multistep tasks until corrective demonstrations were stored and reused.
- A reported limitation: human feedback improves textual/function-calling tasks but does not compensate for a model's inherent visual-reasoning deficits.

## Primary paper

[Vriza, Prince, Zhou, Chan & Cherukara, "Operating advanced scientific instruments with AI agents that learn on the job," *npj Comput. Mater.* 12, 160 (2026); arXiv:2509.00098](https://arxiv.org/abs/2509.00098).

## Other references

_None yet._

## Code

[Repository](https://github.com/AdvancedPhotonSource/CALMS/tree/sdl_agents) — code and data publicly available on GitHub.
