---
title: Drug Synergy (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery]
last_verified: 2026-06-21
summary: ToolUniverse agent skill that quantifies drug-combination synergy using Bliss, HSA, Loewe, ZIP, and Chou-Talalay reference models.
---

# Drug Synergy (ToolUniverse Claude Skill)

A ToolUniverse agent skill that classifies a two-drug combination as synergistic, additive, or antagonistic by applying the appropriate standard reference model to measured effect data.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-drug-synergy/`) |
| **Pricing** | Free / OSS (Apache-2.0); the synergy calculators run locally over user-supplied effect data |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-drug-synergy`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-drug-synergy ~/.claude/skills/
  ```

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the drug-synergy skill") rather than relying on automatic dispatch.

## What it does

Guides a four-step synergy assessment:

- **Model selection** — pick the reference model from the data available, from a single dose pair (Bliss) up to a full dose-response matrix (ZIP).
- **Baseline explanation** — describe each model's additivity baseline (Bliss independence, HSA, Loewe additivity), noting that Bliss and Loewe can legitimately disagree for a given combination.
- **Calculation** — run the ToolUniverse calculator: `DrugSynergy_calculate_bliss`, `DrugSynergy_calculate_hsa`, `DrugSynergy_calculate_loewe`, `DrugSynergy_calculate_zip`, `DrugSynergy_calculate_ci` (Chou-Talalay Combination Index).
- **Interpretation** — apply standard thresholds (synergy > +10, additive −10 to +10, antagonism < −10 on a 0–100 scale; CI < 1 indicates synergy) and flag pitfalls such as scale mismatch, ceiling effects, and model-selection bias.

**Primary use cases**: scoring combination-screen results, deciding between Bliss/Loewe/ZIP for a given dataset, sanity-checking reported synergy claims.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. The skill operates on **user-supplied effect data** — single-drug and combination effects on a consistent inhibition scale, with ≥ 3 measurable-effect dose points per drug for Loewe/CI/ZIP — rather than pulling combination data from a database. ToolUniverse ships ~68 such skills; the research, repurposing, and target-validation workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-drug-synergy/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-synergy/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-drug-synergy&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-drug-synergy.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
