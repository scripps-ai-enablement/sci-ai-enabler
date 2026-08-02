---
title: Dose-Response Analysis (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery, Molecular and Cellular Biology]
last_verified: 2026-08-02
summary: ToolUniverse agent skill that fits four-parameter logistic curves to concentration-response data, returning IC50/EC50, Hill slope, Emax, and fit quality.
---

# Dose-Response Analysis (ToolUniverse Claude Skill)

A ToolUniverse agent skill that fits the four-parameter logistic (Hill) model to paired concentration and response data and reports potency with an explicit quality verdict.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-dose-response/`) |
| **Pricing** | Free / OSS (Apache-2.0); computation is local to the ToolUniverse server — no external API required |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-dose-response`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-dose-response ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the dose-response skill") rather than relying on automatic dispatch.

## What it does

Runs a four-phase curve-fitting workflow over two ToolUniverse tools — `DoseResponse_calculate_ic50` for a single curve and `DoseResponse_compare_potency` for a head-to-head of two compounds:

1. **Data preparation** — put all concentrations on one linear scale (not log), drop zero-concentration points, optionally normalize responses to percent-of-control, and require at least four points spanning both the upper and lower plateaus.
2. **Curve fitting** — fit the 4PL/Hill sigmoidal model, returning IC50 or EC50, Hill slope, Emax, Emin, r², and confidence intervals.
3. **Parameter interpretation** — potency reads off IC50/EC50 (lower is more potent); Hill slopes above 1.5 or below 0.5 are flagged for scrutiny; Emax and Emin carry the efficacy and baseline.
4. **Quality gatekeeping** — curves without a visible plateau are reported as approximate; biphasic or non-monotonic data is rejected from 4PL analysis outright; a potency comparison is only endorsed when both curves reach r² ≥ 0.95 with concordant Hill slopes.

Fit quality below **r² = 0.90** triggers manual inspection before any potency number is reported, and IC50 values are always emitted with their concentration units.

**Primary use cases**: enzyme and cell-viability assay readouts, screening-hit potency ranking, agonist/antagonist pharmacology.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Scope is deliberately narrow — the skill declines image-derived dose-response (that is `tooluniverse-image-analysis` upstream) and survival or general regression modelling (`tooluniverse-statistical-modeling`).

Useful downstream of the [Drug Synergy](tooluniverse-drug-synergy.html) skill, which needs single-agent potency values before it can score a combination. For general-purpose curve fitting outside pharmacology, [statsmodels](statsmodels.html) and [scikit-learn](scikit-learn.html) cover the same math without the assay-specific guardrails. ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-dose-response/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-dose-response/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-dose-response&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-dose-response.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
