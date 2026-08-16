---
title: Enzyme Kinetics (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery, Molecular and Cellular Biology]
last_verified: 2026-08-16
summary: ToolUniverse agent skill that fits Michaelis-Menten kinetics to substrate-velocity data and classifies inhibition mechanism with a Ki estimate.
---

# Enzyme Kinetics (ToolUniverse Claude Skill)

A ToolUniverse agent skill that turns substrate-concentration and initial-velocity data into Km, Vmax, kcat and kcat/Km, and classifies an inhibitor as competitive, uncompetitive or non-competitive.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-enzyme-kinetics/`) |
| **Pricing** | Free / OSS (Apache-2.0); computation is local to the ToolUniverse server — no external API required |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-enzyme-kinetics`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-enzyme-kinetics ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the enzyme kinetics skill") rather than relying on automatic dispatch.

## What it does

Runs a five-phase kinetics workflow, primarily through the `EnzymeKinetics_calculate` tool (operations `michaelis_menten` and `inhibition`), with a bundled `fit_michaelis_menten.py` script for CSV input and Vmax→kcat conversion:

1. **Data preparation** — validates that the velocities are genuinely *initial* rates, that the substrate range actually spans Km, and that units are consistent; asks for the enzyme concentration (needed for kcat) and for at least **5–7 data points**.
2. **Michaelis-Menten fitting** — nonlinear regression over the concentration/velocity pairs returning Vmax, Km, R² and SSE. A Lineweaver-Burk transform is emitted **for reference only**, not as the basis of the fit.
3. **Parameter interpretation** — Km as substrate affinity, Vmax as saturation velocity, kcat as per-enzyme turnover, and kcat/Km as catalytic efficiency (the specificity constant), benchmarked against the diffusion-limited ~10⁸–10⁹ M⁻¹s⁻¹ range for catalytic perfection.
4. **Inhibition classification** — compares velocity curves with and without inhibitor to assign competitive, uncompetitive or non-competitive mechanism and compute Ki.
5. **Quality assurance** — flags substrate inhibition, a Km that falls outside the tested concentration range, a missing enzyme concentration, and systematic patterns in the residuals.

A fit is treated as good at **R² ≥ 0.98**.

**Primary use cases**: characterising a purified enzyme, mechanism-of-inhibition assignment for a screening hit, Ki determination for lead comparison.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. One scope exclusion is explicit upstream: this skill fits *your* data and is not a lookup of published constants — for that, use the BRENDA tools ([BRENDA](brenda-database.html)).

For cell- or organism-level potency rather than enzyme mechanism, [Dose-Response Analysis](tooluniverse-dose-response.html) fits the 4PL/Hill model instead. ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-enzyme-kinetics/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-enzyme-kinetics/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-enzyme-kinetics&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-enzyme-kinetics.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
