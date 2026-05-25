---
title: Deep Research (BioAgents)
parent: Systems
grand_parent: AI scientists
nav_order: 18
affiliation: bio.xyz / BioAgents
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Biology / biomedical
availability: Open source (orchestrator) + closed sub-agents
last_verified: 2026-05-22
---

# Deep Research (BioAgents)

Open-source interactive multi-agent system for biomedical research that runs in minutes per cycle, with state-of-the-art BixBench performance and two operational modes (semi-autonomous and fully autonomous).

| | |
|---|---|
| **Affiliation** | bio.xyz / BioAgents (Weidener, Brkić, Jovanović et al.) |
| **First introduced** | 2026-01 (arXiv:2601.12542) |
| **Lifecycle stages** | Multi-stage (planning, data analysis, literature search, novelty detection) |
| **Autonomy level** | Two operational modes — semi-autonomous with selective human checkpoints, and fully autonomous for extended cycles |
| **Domain focus** | Computational biology and biomedical research |
| **Availability** | Open source orchestrator ([github.com/bio-xyz/BioAgents](https://github.com/bio-xyz/BioAgents)); the bio-data-analysis and bio-literature sub-agents are not yet publicly released |

## Approach

The system positions itself against batch-mode AI scientists (Kosmos, Sakana AI Scientist) that require hours per cycle, arguing for interactive workflows with minute-scale turnaround. Specialized agents handle planning, data analysis, literature search, and novelty detection; a persistent world state maintains context across iterative research cycles so that researchers (in semi-autonomous mode) or the system itself (in fully autonomous mode) can refine direction without rerunning earlier stages. BioAgents is the public orchestrator; the data-analysis and literature components remain closed.

## Validation

Evaluated on BixBench v1.5 (54 capsules spanning genomics, transcriptomics, differential expression, RNA-seq, phylogenetics, WGS, and variant analysis). Only the data-analysis agent was benchmarked, under three regimes: Open Response (judge LLM compares free-form answers to expert references), MCQ with Refusal, and MCQ without Refusal. The study also implements a simplified code-free multiple-choice mapping to decouple option selection from notebook-state variability.

## Notable results

- 48.8% accuracy on BixBench Open Response — state-of-the-art, exceeding K-Dense Analyst (34.4%) and other published baselines by 14 to 26 percentage points.
- 55.1% on MCQ with Refusal and 64.4% on MCQ without Refusal.
- Demonstrates interactive workflows in case studies with minute-scale turnaround, contrasting with the multi-hour batch cycles of Kosmos and Sakana AI Scientist.

## Primary paper

[Weidener, Brkić, Jovanović et al., "Rethinking the AI Scientist: Interactive Multi-Agent Workflows for Scientific Discovery," arXiv:2601.12542 (2026)](https://arxiv.org/abs/2601.12542).

## Other references

_None yet._

## Code

[github.com/bio-xyz/BioAgents](https://github.com/bio-xyz/BioAgents) — orchestrator. Sub-agents (bio-data-analysis, bio-literature) not yet publicly released as of the preprint.
