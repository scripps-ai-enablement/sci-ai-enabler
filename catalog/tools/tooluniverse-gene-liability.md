---
title: Gene Liability Evaluation (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-08-16
summary: ToolUniverse agent skill that scores the human safety liability of inhibiting or knocking out a gene across five evidence dimensions.
---

# Gene Liability Evaluation (ToolUniverse Claude Skill)

A ToolUniverse agent skill that answers "how dangerous is it to drug this target?" by scoring five independent safety dimensions into a single 0–100 liability figure and a recommended modulation strategy.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-gene-liability/`) |
| **Pricing** | Free / OSS (Apache-2.0); the underlying gnomAD, GTEx, Open Targets and DepMap queries are free public APIs |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-gene-liability`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-gene-liability ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

## What it does

Runs a five-phase target-safety assessment:

1. **Gene resolution** — `MyGene_query_genes` normalises whatever identifier you supplied (symbol, Ensembl, UniProt, Entrez) to a canonical gene.
2. **Evidence gathering across five dimensions** — human genetic constraint (`gnomad_get_gene_constraints`), mammalian knockout phenotype (`OpenTargets_get_biological_mouse_models_by_ensemblID`), critical-organ expression (`GTEx_get_median_gene_expression`), observed on-target clinical effects (`OpenTargets_get_target_safety_profile_by_ensemblID`), and cellular essentiality (`DepMap_get_gene_dependencies`). `OpenTargets_get_associated_drugs_by_target_ensemblID` supplies precedent from existing drugs against the target.
3. **Dimension scoring** — each dimension earns 0–25 points, graded by evidence tier T1–T4 so that direct human evidence outweighs inference.
4. **Score calculation** — liability is `100 × points earned / available weight`, so dimensions with no data are excluded from the denominator rather than silently scored as safe.
5. **Strategy translation** — the score maps to a concrete recommendation: full inhibition, partial modulation, transient dosing, tissue-specific delivery, or deprioritise the target.

Constraint scoring is anchored on gnomAD: **pLI ≥ 0.9 combined with LOEUF ≤ 0.35** takes the full 25 points for that dimension, and **embryonic lethality** in the mouse knockout takes the full 25 for phenotype.

**Primary use cases**: target triage before a discovery programme commits, on-target toxicity risk memos, deciding between a degrader and a partial inhibitor.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. The output is an *on-target* liability estimate — off-target chemical liabilities (hERG, AMES, DILI) are the domain of [ADMET Prediction](tooluniverse-admet-prediction.html) and [ADMETlab MCP Server](admetlab-mcp.html), and the skill does not attempt them.

Complements [Drug Target Validation](tooluniverse-drug-target-validation.html), which asks whether a target is *efficacious*, where this one asks whether it is *safe*. The individual evidence sources are catalogued separately if you want to query them directly: [gnomAD](gnomad-database.html), [GTEx](gtex-database.html), [Open Targets](open-targets.html), [DepMap](depmap.html), [MyGene.info](mygene.html). ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-gene-liability/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-gene-liability/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-gene-liability&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-gene-liability.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
