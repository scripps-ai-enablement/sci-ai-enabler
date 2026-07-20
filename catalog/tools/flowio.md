---
title: FlowIO (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-04
verification: works
verified_on: 2026-07-20
verification_note: "repo and skills/flowio dir resolve on K-Dense-AI/scientific-agent-skills; smoke run this cycle installed the K-Dense collection via npx skills add (pass)"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier K-Dense-AI, MIT repo wrapping BSD-3 flowio, maintained (pushed 2026-07-15), no OSV advisories"
summary: Skill that parses Flow Cytometry Standard (FCS v2–3.1) files into NumPy/pandas for immunophenotyping pipelines and metadata extraction.
---

# FlowIO (Claude Skill)

Claude skill wrapping the BSD-3 `flowio` library for parsing and emitting Flow Cytometry Standard (FCS) files — the entry point for any immunophenotyping or cytometry workflow.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (wraps BSD-3 `flowio`) |
| **Availability** | GA |
| **Pricing** | Free / OSS (BSD-3-Clause) |
| **Capabilities** | Read/Write — parses and emits FCS files |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches K-Dense-AI, MIT repo, maintained, no OSV advisories |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/cell-biology/flowio-flow-cytometry` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
Install via the Skills CLI (recommended): `npx skills add K-Dense-AI/scientific-agent-skills`, then enable the `flowio` skill. Or clone the repo manually:

```
git clone https://github.com/K-Dense-AI/scientific-agent-skills
cp -r scientific-agent-skills/skills/flowio ~/.claude/skills/
uv pip install flowio  # Python 3.9+
```

## What it does

- `FlowData` reader for FCS 2.0 / 3.0 / 3.1
- `create_fcs()` writer
- `read_multiple_data_sets()`
- Channel categorization (scatter, fluorescence, time)
- CSV / DataFrame export
- Transformations (gain, log, time scaling)

**Primary use cases**: Immunophenotyping FCS preprocessing, batch metadata extraction across cytometry experiments, conversion to tidy frames for downstream stats.

## Notes

No external services or auth required. For compensation, gating, or GatingML, pair with FlowKit (not yet a skill).

## Sources

- [`skills/flowio/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/flowio/SKILL.md)
- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=flowio&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fflowio.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
