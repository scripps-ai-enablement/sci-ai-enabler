---
title: ChatBattery
parent: Systems
grand_parent: AI scientists
nav_order: 14
affiliation: Université de Montréal and Mila – Québec AI Institute (Liu, Ai, Bengio) with University of Oxford, University College London, University of Ottawa, and the National Research Council Canada
org_short: Mila / U. Montréal
lifecycle_stages: [Multi-stage]
validation_type: Wet-lab
autonomy: Semi-autonomous
domain: Chemistry and materials (lithium-ion battery cathodes)
domain_group: Chemistry & materials
availability: Open source
access: Open source
tagline: Expert-guided LLM reasoning for cathode design, carried through DFT, synthesis, and electrochemical characterization.
last_verified: 2026-08-08
---

# ChatBattery

Agentic framework that injects battery-domain knowledge into LLM chain-of-thought reasoning to propose cathode compositions, then carries the top candidates through DFT screening, synthesis, and electrochemical characterization.

| | |
|---|---|
| **Affiliation** | Université de Montréal / Mila with Oxford, UCL, University of Ottawa, and the National Research Council Canada ([paper](https://arxiv.org/abs/2507.16110)) |
| **First introduced** | 2025-07 (arXiv:2507.16110, dated 2025-07-21) |
| **Lifecycle stages** | Multi-stage (hypothesis generation → computational screening → wet-lab synthesis and characterization) |
| **Autonomy level** | Semi-autonomous — a dedicated Human agent supplies expert judgment at problem conceptualization and wet-lab verification |
| **Domain focus** | Lithium-ion battery cathode materials, targeting the commercialized NMC811 (LiNi<sub>0.8</sub>Mn<sub>0.1</sub>Co<sub>0.1</sub>O<sub>2</sub>) |
| **Availability** | Open source — repository given in the paper's Code Availability statement; a Flask web UI fronts stages 1–4 |

## Approach

ChatBattery runs eight sequential stages split across two phases and orchestrated by seven agents. **Exploration** covers problem conceptualization, hypothesis generation (an LLM agent modifies input formulas under explicit constraints such as capacity thresholds and allowed elements), hypothesis feasibility evaluation against domain databases, and hypothesis testing via computational surrogates. These four stages recurse in cycles — with *k* = 5 candidates per cycle, *C* = 2 cycles, and *N* = 4 repeats, the reported run generated 100 candidate cathodes. **Exploitation** then deduplicates candidates, ranks them by a composite of total charge, structural/preparation complexity and predicted voltage, validates the survivors with DFT, and finally synthesizes and tests them in the lab.

The seven agents are an LLM agent (candidate generation and qualitative ranking), a Search agent (filters compounds that already exist in domain databases), a Decision agent (rejects candidates whose theoretical capacity does not exceed the input compound's), a Retrieval agent (supplies a similar valid compound as domain feedback when a candidate fails), a Rank agent (hierarchical ranking tree), a Domain agent (exact and range matching, capacity computation from Li count and molecular weight, formula-similarity scoring), and a Human agent for expert oversight. The design premise is that expert guidance embedded in the reasoning loop substitutes for fine-tuning or RL, both of which are impractical given the scarcity of battery-domain reasoning traces.

## Validation

Physical validation on a single target task: optimizing NMC811. Three agent-nominated compositions were synthesized, characterized by XRD, and assembled into 2032-type coin cells, cycled in a 2.6–4.3 V window.

## Notable results

- Three novel cathodes — NMC-SiMg (LiNi<sub>0.7</sub>Mn<sub>0.05</sub>Co<sub>0.05</sub>Si<sub>0.1</sub>Mg<sub>0.1</sub>O<sub>2</sub>), NMC-SiCa, and NMC-MgB — delivered third-cycle reversible capacities of **174, 169 and 160 mAh/g** against NMC811's ~135 mAh/g under identical testing, i.e. **28.8%, 25.2% and 18.5%** improvements.
- XRD confirmed the candidates retain rhombohedral R-3m (No. 166) symmetry, the same space group as NMC811, with stable cycling behaviour.
- A Li-rich variant, Li-rich-NMC-SiMg, reached **181 mAh/g** by the third cycle (34% above NMC811) with initial Coulombic efficiency approaching 100%.

## Primary paper

[Liu, Xu, Ai, Li, Bengio, Guo, "Expert-Guided LLM Reasoning for Battery Discovery: From AI-Driven Hypothesis to Synthesis and Characterization," arXiv:2507.16110](https://arxiv.org/abs/2507.16110).

## Other references

_None yet._

## Code

Released per the paper's Code Availability statement; the repository URL is embedded as a hyperlink in the preprint and is not recoverable from the archived text.
