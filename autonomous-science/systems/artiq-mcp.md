---
title: ARTIQ-MCP (Duke trapped-ion agent)
parent: Systems
grand_parent: AI scientists
nav_order: 10
affiliation: Duke Quantum Center, Duke University (Kenneth R. Brown and Norbert M. Linke groups), with the Joint Quantum Institute and National Quantum Laboratory, University of Maryland
org_short: Duke / UMD
lifecycle_stages: [Experiment design, Analysis]
validation_type: Wet-lab
autonomy: Semi-autonomous
domain: Quantum physics (trapped-ion experiment control)
domain_group: Physical sciences
availability: Open source (safety-filter and artiq-mcp components)
access: Open source
tagline: LLM agent that writes native ARTIQ code and runs it on real trapped-ion hardware behind a per-call safety gate.
last_verified: 2026-06-27
---

# ARTIQ-MCP (Duke trapped-ion agent)

An LLM agent that autonomously writes native ARTIQ control code and runs it on real trapped-ion quantum hardware, behind a per-operation safety filter that authorizes each tool call only after isolated-simulation bounds-checking.

| | |
|---|---|
| **Affiliation** | Duke Quantum Center, Duke University (Brown and Linke groups), with University of Maryland ([arXiv:2606.27231](https://arxiv.org/abs/2606.27231)) |
| **First introduced** | 2026-06 (arXiv:2606.27231) |
| **Lifecycle stages** | Experiment design, Analysis |
| **Autonomy level** | Semi-autonomous — agent designs, codes, and iterates experiments within a per-call human/simulation safety gate |
| **Domain focus** | Trapped-ion quantum physics — calibration, Rabi/Ramsey sequences, magnetic-field stabilization |
| **Availability** | Open source — `safety-filter` and `artiq-mcp` components released |

## Approach

A single coordinating agent (Claude Opus 4.8, extended reasoning, 1M-token context) sits in the control path of a trapped-ion apparatus but never touches the hardware directly. The agent designs experiments from natural-language goals and emits native ARTIQ Python, which it submits as tool calls through two interposed software layers. `artiq-mcp` is a host-side Model Context Protocol server that wraps a running ARTIQ master's functions — submitting experiments, polling run status, reading/writing datasets, querying the device database, streaming logs — over ARTIQ's native sipyco RPC interfaces; it adds no real-time control logic. A `safety-filter` MCP proxy is the single enforcement point: no call reaches `artiq-mcp` unless it carries a content-bound, single-use authorization token. Tokens issue automatically via a two-stage pipeline (an AST denylist check for host-reachable constructs, then execution of the script in an isolated `dax.sim` simulation that traces every hardware operation and checks DDS/DAC/TTL parameters against per-device bounds) or manually by a human operator for sensitive actions; unmapped devices and non-deterministic verdicts are blocked by default. Because no context window spans a full campaign, the agent carries goal and working memory across sessions in external Markdown files and spawns short-lived subagents for code generation, log parsing, and fit analysis.

## Validation

Real-instrument (wet-lab) deployment on two independent ARTIQ platforms. On a co-trapped 40Ca+/40CaOH+ crystal at Duke, the agent autonomously built a full calibration stack (cooling, Rabi, and Ramsey sequences) from a small number of high-level prompts, then — with targeted operator guidance — closed a cross-instrument active magnetic-field-compensation loop coupling ARTIQ-based Ramsey interferometry with an external arbitrary waveform generator to suppress 60 Hz power-line magnetic-field noise. Interface-level portability was confirmed by running the identical safety-gated stack against a separate 171Yb+ ARTIQ system at the University of Maryland. The safety filter was characterized by an adversarial red-team campaign of 1932 bench scripts and roughly 250 harness-level tests, mapping the empirical boundary of its protection and quantifying the structural gap between evasion code and normal calibration code.

## Notable results

- First demonstration of an LLM agent generating new trapped-ion control code from scratch and executing it on real quantum hardware, versus prior demos that search only within fixed human-written routines.
- Cross-instrument closed loop spanning the ARTIQ master and external (non-ARTIQ) hardware under a single per-call authorization scheme.
- The authors attribute the agent's remaining limits to metacognitive control (recognizing when to re-frame a problem) rather than domain knowledge.

## Primary paper

[Wang et al., "A hardware-safety-gated system for LLM-written native ARTIQ control code on a trapped-ion platform," arXiv:2606.27231](https://arxiv.org/abs/2606.27231).

## Other references

_None yet._

## Code

[`artiq_mcp` repository](https://gitlab.oit.duke.edu/dw346/artiq_mcp) — `safety-filter` and `artiq-mcp` components.
