---
title: AutoScientists
parent: Systems
grand_parent: AI scientists
nav_order: 50
affiliation: Harvard University (Zitnik lab)
org_short: Harvard
lifecycle_stages: [Multi-stage]
validation_type: Benchmark
autonomy: Fully autonomous
domain: General (biomedical ML, language-model training, protein engineering)
domain_group: General / multi-domain
availability: Open source
access: Open source
tagline: Decentralized team of AI agents that self-organize around hypotheses and share results across teams.
last_verified: 2026-06-01
---

# AutoScientists

Decentralized team of AI agents that self-organize around promising hypotheses, critique proposals before spending experimental compute, and share successes and failures across teams for long-running computational scientific experimentation.

| | |
|---|---|
| **Affiliation** | Harvard University — Shanghua Gao, Ada Fang, Marinka Zitnik (Harvard Medical School / Kempner) |
| **First introduced** | 2026-05 (arXiv:2605.28655) |
| **Lifecycle stages** | Multi-stage (hypothesis generation + experiment design + execution + analysis, plus a research-findings report) |
| **Autonomy level** | Fully autonomous under matched experimental compute budget; no central planner |
| **Domain focus** | Computational scientific experimentation — biomedical ML, LM training optimization, protein fitness prediction |
| **Availability** | Open source — [mims-harvard/AutoScientists](https://github.com/mims-harvard/AutoScientists); project site at [autoscientists.openscientist.ai](https://autoscientists.openscientist.ai) |

## Approach

AutoScientists drops the single-trajectory and central-orchestrator patterns of prior AI scientists. *n* long-running agents (default: 3 analyst + 6 experiment agents) persist across the run and coordinate exclusively through a **shared state** with four layers: a champion model `p*` with full reproduction instructions; an experiment log `L`; a structured research forum `F` for proposals, results, and critique; and team-local state (per-team queues `Qk`, dead-end registries `Dk`, hypothesis docs) that is readable cross-team.

The system alternates two phases. In **discussion**, agents read the task, `p*`, and prior forum posts, propose modifications, critique competing proposals, and self-organize into *K* teams each pursuing one research axis; the last agent of the round consolidates a roster and writes it back. In **execution**, each team runs a continuous propose-execute loop: analyst agents audit untested directions and post ranked proposals; experiment agents claim items from `Qk`, apply the change to `p*`, train, and record outcomes (improvements within the empirical noise band are reconfirmed on a second seed before promotion). When `ℓeval` stagnates (no improvement in the last 10 experiments), agents reopen discussion and may create, merge, split, or rebalance teams. Failed directions are stored in `Dk` to avoid repeating them. All agents use the same backend — Claude Code with Claude Sonnet 4.6 — running on H100 GPUs.

## Validation

Three benchmarks under matched compute budgets against the strongest prior single-trajectory baseline (Autoresearch), the BioML-Bench published agents (MLAgentBench, AIDE, STELLA, Biomni), and ProteinGym state-of-the-art (Kermut).

## Notable results

- **BioML-Bench (24 tasks across biomedical imaging, drug discovery, protein engineering, single-cell omics)**: mean leaderboard percentile 74.40% vs 66.07% for Autoresearch (+8.33 points), with drug-discovery percentile rising from 47.91% (Biomni) to 64.52%; AutoScientists completed all 24 tasks.
- **GPT nanochat training optimization**: reaches val_bpb ≈ 0.978 in 34 experiments vs 65 for Autoresearch (1.9× fewer); continuing from an AutoScientists champion (0.9777) it accepts 7 improvements over 93 experiments reaching 0.9730, while Autoresearch accepts 0 improvements over 100 experiments.
- **ProteinGym ACE2-Spike fitness prediction**: a Kermut extension discovered by AutoScientists raises Spearman ρ from 0.747 to 0.840 (+12.5%); applied without modification to all 217 ProteinGym supervised-substitution assays it lifts the official average Spearman ρ from 0.657 to 0.700 (+6.5%).

## Primary paper

[Gao, Fang, Zitnik, "AUTOSCIENTISTS: Self-Organizing Agent Teams for Long-Running Scientific Experimentation," arXiv:2605.28655 (2026)](https://arxiv.org/abs/2605.28655).

## Other references

_None yet._

## Code

[mims-harvard/AutoScientists](https://github.com/mims-harvard/AutoScientists) — released with the preprint.
