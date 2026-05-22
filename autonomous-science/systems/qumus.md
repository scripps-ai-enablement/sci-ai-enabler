---
title: Qumus
parent: Systems
grand_parent: AI scientists
nav_order: 21
affiliation: Princeton University (Sanfeng Wu group, with Princeton AI Lab and ECE), with University of Michigan, NIMS Tsukuba, and California State University Northridge
lifecycle_stages: [Multi-stage]
autonomy: Fully autonomous
domain: Quantum materials / 2D materials and van der Waals device fabrication
availability: Code on request (GitHub release stated as forthcoming)
last_verified: 2026-05-21
---

# Qumus

Embodied multi-agent AI system that autonomously plans, fabricates, and nano-processes atomically thin two-dimensional quantum materials and van der Waals device stacks inside a robotic mini-laboratory.

| | |
|---|---|
| **Affiliation** | Princeton University Department of Physics and Princeton AI Lab (Sanfeng Wu group), with University of Michigan CSE, NIMS Tsukuba (Watanabe and Taniguchi), and California State University Northridge |
| **First introduced** | 2026-05 (arXiv:2605.18407) |
| **Lifecycle stages** | Multi-stage (hypothesis generation, protocol planning, multi-step robotic execution, optical analysis, reporting) |
| **Autonomy level** | Fully autonomous — natural-language scientific goals trigger closed-loop fabrication and characterization with no human intervention beyond providing raw materials and electricity |
| **Domain focus** | Quantum materials — graphene, hBN, transition-metal dichalcogenides, and van der Waals stacks; field-effect transistor fabrication |
| **Availability** | Code on request — paper states code will be released on GitHub (link to be provided); demo videos at [qumus.ai](https://qumus.ai) |

## Approach

Multi-agent system embodied within a custom robotic minilab. A lead Qumus agent orchestrates four specialized sub-agents: Project Manager (literature, experimental history, registered Skills and recipes), Lab Manager (material inventory, instrument status, computer-vision tool positioning), Device Expert (vdW stacking order, positions, twist angles), and Processing Agent (executable laboratory actions). The Processing Agent operates a three-tier hierarchical workflow: fixed "Atom Workflows" (robotic-arm control, stage movement, camera, vacuum, tape handling); composable "Molecule Workflows" (exfoliation, automated flake search, relocation); and "Assembly Workflows" (repeated exfoliation, stacking, longer fabrication sequences) — AI self-generates the molecule and assembly levels while atom-level actions remain user-fixed. The hardware platform integrates automated Scotch-tape exfoliation, optical inspection with multi-magnification microscopy, precision 2D crystal transfer and vdW stacking, and sample storage in a single workstation. YOLO-based macroscopic vision plus micro-QR fiducials and motorized-focus optical microscopy provide multi-scale perception. The system was characterized across six leading LLM backbones (GPT, Gemini, Claude, Grok, Qwen, DeepSeek).

## Validation

End-to-end demonstrations on real hardware: AI-driven creation of graphene flakes, hexagonal boron nitride exfoliation, and AI fabrication of atomically thin field-effect transistors via vdW stacking. In an open-ended task ("I want a graphene flake larger than 200 μm²" with cleared history), Qumus (Claude Sonnet 4.6) explored the parameter space of substrate heating temperature, dwell time, massage cycles, and tape peel-off speed across five consecutive experimental runs over four hours, eventually producing a flake meeting the goal. The authors quantify each LLM's experimental personality along seven dimensions (protocol alignment, caution, bias for action, token efficiency, agent efficiency, consistency, report quality).

## Notable results

- First reported AI creation of graphene and first AI fabrication of complex nanodevices including atomically thin field-effect transistors via vdW stacking.
- Demonstrated autonomous error detection and recovery (e.g., recovering after a human removed an in-process chip mid-experiment, and after a Processing Agent hallucination mislabeled hBN as graphene).
- Goal-oriented long-horizon execution with closed-loop hypothesis–experiment–analysis iteration over multi-hour timescales.

## Primary paper

[Shi et al., "Qumus: Realization of An Embodied AI Quantum Material Experimentalist," arXiv:2605.18407](https://arxiv.org/abs/2605.18407).

## Other references

_None yet._

## Code

GitHub release stated as forthcoming (link to be provided). Demo videos at [qumus.ai](https://qumus.ai).
