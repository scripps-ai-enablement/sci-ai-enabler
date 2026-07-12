---
title: Adverse Outcome Pathway (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-07-12
summary: ToolUniverse agent skill that maps chemicals to adverse outcome pathways using AOPWiki, GHS/IARC classification, LD50 data, and toxicogenomics.
---

# Adverse Outcome Pathway (ToolUniverse Claude Skill)

A ToolUniverse agent skill that maps environmental and industrial chemicals to adverse outcome pathways — from molecular initiating event to organ-level toxicity — using AOPWiki, GHS classification, IARC carcinogen status, LD50 data, and toxicogenomics.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-adverse-outcome-pathway/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (AOPWiki, PubChem, PubChemTox, CTD) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-adverse-outcome-pathway`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-adverse-outcome-pathway ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the adverse-outcome-pathway skill") rather than relying on automatic dispatch.

## What it does

Runs a four-phase chemical hazard assessment:

1. **Compound identity resolution** — chemical names to PubChem CIDs (`PubChem_get_CID_by_compound_name`).
2. **AOP discovery** — search AOPWiki by organ, mechanism, or receptor; retrieve full pathway details including molecular initiating events, key events, and stressor lists (`AOPWiki_list_aops`, `AOPWiki_get_aop`).
3. **Hazard quantification** — parallel PubChemTox queries for GHS classification, IARC carcinogen status, and LD50/LC50 values (`PubChemTox_get_ghs_classification`, `_get_carcinogen_classification`, `_get_toxicity_values`).
4. **Toxicogenomics integration** — map chemicals to gene targets and disease associations via CTD, cross-referenced with AOP key-event genes (`CTD_get_chemical_gene_interactions`, `CTD_get_chemical_diseases`).

**Primary use cases**: mechanistic toxicity assessment, regulatory hazard screening, off-target/safety triage for candidate compounds.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Aimed at environmental/industrial chemical toxicology, but the AOP + GHS/IARC + toxicogenomics surface is also useful for safety filtering in drug discovery. ToolUniverse ships ~150 such skills; other chemical-safety and drug-discovery workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-adverse-outcome-pathway/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-adverse-outcome-pathway/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-adverse-outcome-pathway&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-adverse-outcome-pathway.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
