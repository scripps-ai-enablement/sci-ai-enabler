---
title: Biomni
parent: Systems
grand_parent: AI scientists
nav_order: 4
affiliation: Stanford University (Snap group, Leskovec lab), with Genentech, Arc Institute, Princeton, University of Washington, UCSF
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Biomedicine (general purpose)
availability: Open source
last_verified: 2026-05-20
---

# Biomni

General-purpose biomedical AI agent coupling a 150-tool, 105-package, 59-database environment with a code-executing planner. Matches expert humans on LAB-Bench DbQA/SeqQA.

| | |
|---|---|
| **Affiliation** | Stanford University (Snap group, Leskovec lab), with Genentech, Arc Institute, Princeton, University of Washington, UCSF ([Biomni](https://biomni.stanford.edu/)) |
| **First introduced** | 2025-05 (bioRxiv preprint 2025.05.30.656746) |
| **Lifecycle stages** | Multi-stage (experiment design, analysis, hypothesis generation) |
| **Autonomy level** | Semi-autonomous (closed-loop with checkpoints; LLM-generated code is executed with system privileges by default) |
| **Domain focus** | Biomedicine (general purpose across 25 biomedical subfields) |
| **Availability** | Open source (Apache-2.0 for Biomni itself; integrated tools/databases may carry separate licenses); free no-code web UI at biomni.stanford.edu |

## Approach

Two-component agent.

- **Biomni-E1** is an environment mined from tens of thousands of biomedical publications, exposing 150 specialized tools, 105 software packages, and 59 databases as a unified action space.
- **Biomni-A1** is an LLM agent that dynamically selects tools, plans tasks, and executes Python code that composes loops, parallelization, and conditional steps; an adaptive planning loop iteratively refines plans during execution.

## Validation

On LAB-Bench: 74.4% accuracy on DbQA (vs. 74.7% human experts) and 81.9% on SeqQA (vs. 78.8% human experts). On a 52-question HLE subset spanning 14 biomedical subfields: 17.3% accuracy (reported as a 4× improvement over base LLMs).

Real-world case studies: a 10-step wearable-sensor pipeline analyzing 458 files and 227 nights of sleep data; multi-omics processing of >336,000 single-nucleus RNA-seq / ATAC-seq profiles.

## Notable results

Matched or exceeded expert performance on LAB-Bench DbQA/SeqQA. Autonomously authored multi-stage bioinformatics pipelines with figures and reports across heterogeneous biomedical data types.

## Primary paper

[Huang et al., "Biomni: A General-Purpose Biomedical AI Agent," bioRxiv 2025.05.30.656746](https://doi.org/10.1101/2025.05.30.656746).

## Other references

- [Biomni project page](https://biomni.stanford.edu/)
- [GitHub README and DETAILS.md](https://github.com/snap-stanford/Biomni)

## Code

[Repository](https://github.com/snap-stanford/Biomni)
