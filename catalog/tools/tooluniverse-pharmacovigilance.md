---
title: Pharmacovigilance (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-07-05
summary: ToolUniverse agent skill that mines FAERS adverse-event reports and FDA labels, computes disproportionality signals (PRR, ROR, IC), and assesses pharmacogenomic risk.
---

# Pharmacovigilance (ToolUniverse Claude Skill)

A ToolUniverse agent skill that analyzes drug safety by mining FDA adverse-event reports, computing disproportionality signals, checking label warnings and pharmacogenomic risk, and synthesizing a prioritized safety report.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-pharmacovigilance/`) |
| **Pricing** | Free / OSS (Apache-2.0); reasoning runs locally, database calls go through the ToolUniverse MCP server |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-pharmacovigilance`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-pharmacovigilance ~/.claude/skills/
  ```

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the pharmacovigilance skill") rather than relying on automatic dispatch.

## What it does

Runs a multi-phase drug-safety analysis, executing Python (pandas/scipy/statsmodels) for the quantitative steps rather than describing them:

- **Drug disambiguation** — `DailyMed_search_spls`, `ChEMBL_search_drugs` resolve the drug to canonical identifiers.
- **Adverse-event profiling** — `FAERS_count_reactions_by_drug_event`, `FAERS_filter_serious_events`, `FAERS_stratify_by_demographics` mine FDA spontaneous reports, with MedDRA British-spelling conventions in queries.
- **Label warnings** — `DailyMed_get_spl_by_setid`, `OpenFDA_search_drug_labels` pull black-box warnings and label-change history.
- **Pharmacogenomics** — `PharmGKB_search_drugs`, `CPIC_list_guidelines` assess genotype-dependent risk.
- **Clinical trials & literature** — `search_clinical_trials`, `PubMed_search_articles`, plus KEGG drug-metabolism queries and OpenAlex citation analysis.
- **Signal prioritization & report** — computes disproportionality measures (PRR, ROR, IC), classifies dose-dependent vs. idiosyncratic reactions, and writes a markdown report plus CSV data files.

**Primary use cases**: post-marketing safety-signal detection, FAERS disproportionality analysis, label/black-box warning review, pharmacogenomic risk assessment.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Disproportionality measures from spontaneous-report data (FAERS) indicate signals, not confirmed causality, and are subject to reporting bias. Outputs are decision-support reasoning, not clinical advice. Closely related to the `tooluniverse-adverse-event-detection` skill (also FAERS/PRR/ROR-based). ToolUniverse ships ~68 such skills; the research, repurposing, target-validation, synergy, drug-drug-interaction, and precision-oncology workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-pharmacovigilance/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-pharmacovigilance/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-pharmacovigilance&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-pharmacovigilance.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
