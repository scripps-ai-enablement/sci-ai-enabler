---
title: Deep Researcher Agent
parent: Systems
grand_parent: AI scientists
nav_order: 21
affiliation: University of Tokyo (Xiangyue Zhang)
lifecycle_stages: [Multi-stage]
autonomy: Fully autonomous
domain: Machine-learning / deep-learning research
availability: Open source
last_verified: 2026-05-25
---

# Deep Researcher Agent

Open-source framework that runs LLM agents 24/7 through complete deep-learning experiment cycles — hypothesis, code, GPU training, monitoring, and reflection — at near-zero LLM cost during the training phase.

| | |
|---|---|
| **Affiliation** | University of Tokyo ([paper](https://arxiv.org/abs/2604.05854)) |
| **First introduced** | 2026-04 (arXiv:2604.05854, dated 2026-04-07) |
| **Lifecycle stages** | Multi-stage — Think (hypothesis + experiment design) → Execute (code + GPU training) → Reflect (log parsing + next-action selection) |
| **Autonomy level** | Fully autonomous — runs continuously in persistent tmux sessions with three human-override mechanisms (a `HUMAN_DIRECTIVE.md` file consumed each cycle, a CLI flag, and direct edits to `MEMORY_LOG.md`) |
| **Domain focus** | Deep-learning experimentation (GPU training, hyperparameter and architecture iteration) |
| **Availability** | Open source ([GitHub repository](https://github.com/Xiangyue-Zhang/auto-deep-researcher-24x7)) |

## Approach

Deep Researcher Agent runs a continuous **Think → Execute → Reflect** main loop centered on three innovations.

- **Zero-Cost Monitoring.** During GPU training — typically 90–99% of wall-clock time — the framework makes zero LLM calls. Instead, an OS-level monitor performs `kill -0 $PID` process-liveness checks, `nvidia-smi` GPU-utilization checks, and a 50-line log tail at configurable intervals (default 15 minutes). The LLM is reinvoked only when the training process terminates, at which point accumulated log tail feeds the Reflect phase. Reported LLM cost: $0.08 per 24-hour cycle vs. ~$0.50 for a naive 5-minute-poll baseline.
- **Two-Tier Constant-Size Memory.** A frozen human-authored Project Brief (≤ 3,000 chars) is paired with an agent-maintained Memory Log split into Key Results (auto-compacted at 1,200 chars by dropping the oldest entry) and Recent Decisions (most-recent 15 entries retained). Total memory is provably bounded at ~5,000 characters regardless of run duration.
- **Minimal-Toolset Leader-Worker Architecture.** A Leader agent (3 tools: `log_memory`, `write_file`, `read_file`) coordinates three single-active Worker agents: Idea (literature + hypothesis, 4 tools), Code (implementation + experiment launch, 5 tools), and Writing (report generation, 3 tools). Cycle conversation history is reset between cycles. Reported ~73% per-call token-overhead reduction vs. full-toolset frameworks.

Safety mechanisms: mandatory dry-run (two forward-backward steps) before any real training launch; protected state files (`state.json`, `MEMORY_LOG.md`, `PROJECT_BRIEF.md`) cannot be overwritten by workers; anti-burn exponential cooldown on consecutive no-output cycles.

## Validation

Real-world deployment across 4 concurrent deep-learning research projects on 4 GPU servers (NVIDIA L20X 144 GB), each project running an independent agent instance in a persistent tmux session. Evaluation focuses on operational metrics — autonomous cycle count, continuous operation duration, monitoring cost, dry-run failure rate, post-dry-run crash rate — rather than benchmark scores on fixed tasks, because the agent ran open-ended ML research projects of its own choosing.

## Notable results

- 500+ autonomous experiment cycles, 30+ days of continuous operation, 4 concurrent projects managed.
- 52% improvement over baseline metrics in the best-performing project, from 200+ automated experiments.
- Average LLM cost of $0.08 per 24-hour cycle — a reported 10–20× reduction vs. conventional LLM-polling monitoring.

## Primary paper

[Zhang, "Deep Researcher Agent: An Autonomous Framework for 24/7 Deep Learning Experimentation with Zero-Cost Monitoring," arXiv:2604.05854](https://arxiv.org/abs/2604.05854).

## Other references

_None yet._

## Code

[Repository](https://github.com/Xiangyue-Zhang/auto-deep-researcher-24x7).
