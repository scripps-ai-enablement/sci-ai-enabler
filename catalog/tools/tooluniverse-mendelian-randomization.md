---
title: Mendelian Randomization (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-08-16
summary: ToolUniverse agent skill that uses genetic variants as instrumental variables to test whether an exposure causally affects a disease outcome.
---

# Mendelian Randomization (ToolUniverse Claude Skill)

A ToolUniverse agent skill that answers "does X actually cause Y, or is the association confounded?" using pre-computed and custom two-sample Mendelian randomization over IEU OpenGWAS and EpiGraphDB MR-EvE.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-mendelian-randomization/`) |
| **Pricing** | Free / OSS (Apache-2.0); IEU OpenGWAS and EpiGraphDB are free academic APIs |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-mendelian-randomization`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-mendelian-randomization ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the Mendelian randomization skill") rather than relying on automatic dispatch.

## What it does

Runs a five-step causal-inference workflow over four ToolUniverse tools:

1. **Trait resolution** — `EpiGraphDB_search_opengwas` maps the exposure and outcome you named onto exact OpenGWAS study labels, which is where most MR queries silently go wrong.
2. **MR execution** — `EpiGraphDB_get_mendelian_randomization` returns pre-computed exposure → outcome estimates from the MR-EvE graph; `OpenGWAS_get_mr_instruments` assembles instruments for a custom two-sample analysis when the pre-computed pair is missing.
3. **Interpretation** — effect direction and magnitude are read alongside instrument quality via the **MOE score**, so a large effect from weak instruments is not reported as a finding.
4. **Triangulation** — method agreement across IVW, MR-Egger and weighted median; bidirectional MR to rule out reverse causation; and `EpiGraphDB_get_genetic_correlations` to distinguish shared heritability from causation.
5. **Drug-target follow-up** — an optional step carrying a supported causal exposure into target work.

The skill is written to trigger on plain-language causal questions ("is LDL cholesterol actually causal for heart disease?", "does BMI cause type 2 diabetes or just correlate?") without the user naming MR at all.

**Primary use cases**: genetic validation of a drug target, testing whether a biomarker is a causal risk factor, triangulating an observational epidemiology result.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Two scope exclusions are explicit upstream: plain GWAS association lookups belong to the GWAS skills, and the skill will not fit your own instruments from raw summary statistics you supply — it works from OpenGWAS study identifiers.

Genetic correlation is deliberately reported as *not* causation; treat that output as context rather than evidence. For association-level questions use [GWAS Drug Discovery](tooluniverse-gwas-drug-discovery.html) or the [GWAS Catalog](gwas-database.html); for efficacy evidence assembly see [Drug Target Validation](tooluniverse-drug-target-validation.html). ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-mendelian-randomization/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-mendelian-randomization/SKILL.md)
- [IEU OpenGWAS](https://gwas.mrcieu.ac.uk/)
- [EpiGraphDB](https://epigraphdb.org/)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-mendelian-randomization&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-mendelian-randomization.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
