---
title: FlowIO (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-05-20
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

## How to install

```
git clone https://github.com/K-Dense-AI/scientific-agent-skills
cp -r scientific-agent-skills/scientific-skills/flowio ~/.claude/skills/
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

- [`scientific-skills/flowio/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/flowio/SKILL.md)
- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
