---
title: Brian2 (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroForge
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-07-12
summary: "Build spiking neural network simulations in Brian2 — equation-based neuron models, synaptic plasticity, monitors, and multicompartment morphology."
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "skills/brian2 dir + SKILL.md confirmed but GitHub license is null vs the page MIT claim, single-maintainer 4-star, stale (pushed 2026-02-24)"
---

# Brian2 (Claude Skill)

Guides Claude through building spiking neural network simulations with Brian2 — defining neuron populations from differential equations, wiring synapses with plasticity, recording activity, and running multicompartment models.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [NeuroForge](https://github.com/HughYau/neuroforge-skills) (community OSS, MIT) |
| **Availability** | GA — part of the NeuroForge neuroscience skill set |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude writes and runs Brian2 Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — skills/brian2 dir confirmed but GitHub license null vs MIT claim, single-maintainer, stale (2026-02-24) |

## How to install

- **Claude Code** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/HughYau/neuroforge-skills
  cp -r neuroforge-skills/skills/brian2 ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. The skill invokes Brian2 in your Python environment — install it first:
  ```
  pip install brian2
  ```
  (The skill targets Brian2 2.10.1; the C++ standalone backend additionally needs a working C++ compiler.)

## What it does

Covers the full Brian2 workflow for spiking neural network modeling:

- **Neuron modeling** — define populations with differential equations, threshold/reset dynamics, and state tracking via `NeuronGroup`.
- **Synaptic plasticity** — build connections with event-driven updates and STDP-style rules via `Synapses`.
- **Stimulation** — inject Poisson or time-varying (`TimedArray`) inputs.
- **Recording & analysis** — capture spikes, continuous variables, and population firing rates via `SpikeMonitor` / `StateMonitor`.
- **Execution control** — switch between Python runtime and `cpp_standalone` backends via `set_device`.
- **Spatial morphology** — simulate multicompartment neurons over dendritic/axonal trees with `SpatialNeuron` / `Morphology`.

**Primary use cases**: spiking neural network simulation, synaptic plasticity/STDP experiments, computational neuroscience modeling.

## Notes

Distributed as a `SKILL.md` plus `references/*.md` in the NeuroForge skill set — Claude executes Brian2 locally via Bash/Python rather than as an MCP server. Upstream skill front-matter `name` is `brian2`; the skill directory upstream is `skills/brian2`. Upstream license: MIT. The README documents context-injection usage for other agents, but the copy-into-`~/.claude/skills/` path above is the standard Claude Code Agent Skills install.

## Sources

- [`HughYau/neuroforge-skills`](https://github.com/HughYau/neuroforge-skills)
- [`skills/brian2/SKILL.md`](https://github.com/HughYau/neuroforge-skills/blob/main/skills/brian2/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=brian2&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbrian2.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
