---
title: Drug-Drug Interaction (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-06-28
summary: ToolUniverse agent skill that assesses drug-drug interactions via CYP/transporter pharmacokinetics, pharmacodynamic overlap, and 0-100 clinical risk scoring.
---

# Drug-Drug Interaction (ToolUniverse Claude Skill)

A ToolUniverse agent skill that evaluates a drug pair for interaction risk by reasoning through CYP metabolic pathways, transporter effects, and pharmacodynamic mechanisms, then grading the evidence and producing a clinical risk score.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-drug-drug-interaction/`) |
| **Pricing** | Free / OSS (Apache-2.0); reasoning runs locally, database calls go through the ToolUniverse MCP server |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-drug-drug-interaction`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-drug-drug-interaction ~/.claude/skills/
  ```

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the drug-drug-interaction skill") rather than relying on automatic dispatch.

## What it does

Runs a structured interaction assessment that combines local pharmacology reference data with live database queries:

- **Pharmacokinetic analysis** — `ChEMBL_get_drug_mechanisms` (substrate/inhibitor/inducer classification), `KEGG_get_drug` (metabolic pathways), and `drugbank_get_drug_interactions_by_drug_name_or_id` (P-gp/OATP/OAT/OCT transporter effects). A local `scripts/pharmacology_ref.py` is consulted first for instant CYP/UGT enzyme roles and known critical interactions.
- **Pharmacodynamic analysis** — identifies receptor overlap and shared organ-toxicity pathways.
- **Evidence grading** — `DailyMed_get_spl_by_setid` (FDA label warnings) and `PubMed_search_articles` (clinical evidence), graded FDA label > clinical study > theoretical.
- **Risk scoring** — combines mechanism, severity, and evidence into a 0-100 score, with bidirectional (A→B and B→A) analysis and management recommendations (alternatives, dose adjustments, monitoring).

**Primary use cases**: pre-prescription interaction screening, polypharmacy review, mechanistic interpretation of a flagged drug pair.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. The skill emphasizes Phase II UGT/glucuronidation interactions in addition to CYP, and explicitly documents null results in its report. Outputs are decision-support reasoning, not clinical advice. ToolUniverse ships ~68 such skills; the research, repurposing, target-validation, synergy, and precision-oncology workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-drug-drug-interaction/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-drug-interaction/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-drug-drug-interaction&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-drug-drug-interaction.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
