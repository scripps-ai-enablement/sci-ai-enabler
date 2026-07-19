---
title: Small Molecule Discovery (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-07-19
summary: ToolUniverse agent skill for compound identification, analog search, bioactivity, ADMET, target prediction, and commercial sourcing across PubChem, ChEMBL, BindingDB, and vendor catalogs.
---

# Small Molecule Discovery (ToolUniverse Claude Skill)

A ToolUniverse agent skill that takes a small molecule from identity resolution through bioactivity, drug-likeness, predicted targets, and commercial availability.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-small-molecule-discovery/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (PubChem, ChEMBL, BindingDB, ADMET-AI, SwissADME, SwissTargetPrediction, eMolecules, Enamine) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-small-molecule-discovery`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-small-molecule-discovery ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the small-molecule-discovery skill") rather than relying on automatic dispatch.

## What it does

Runs a six-phase compound-research workflow:

1. **Compound identification** — resolve chemical identity via PubChem CID, ChEMBL ID, and canonical SMILES.
2. **Structure-based search** — find analogs through similarity and substructure queries.
3. **Bioactivity and binding** — retrieve potency data (IC50, Ki) from ChEMBL and BindingDB (with a ChEMBL fallback).
4. **Drug-likeness and ADMET** — physicochemical rules and drug-likeness via SwissADME; ML-based toxicity, bioavailability, BBB penetrance, and CYP interactions via ADMET-AI.
5. **Target prediction** — infer likely protein targets for novel compounds (SwissTargetPrediction).
6. **Commercial availability** — check sourcing via eMolecules and Enamine catalogs (returns URLs when APIs are unavailable).

**Primary use cases**: hit characterization, analog scouting, ADMET triage, target deconvolution, and procurement of purchasable compounds.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Overlaps but is distinct from the [Chemical Safety](tooluniverse-chemical-safety.html) skill (which centers hazard/toxicology) — this one centers identification, activity, and sourcing. Complements the standalone [ChEMBL](chembl.html), [PubChem](pubchem.html), and [BindingDB](bindingdb.html) entries. ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-small-molecule-discovery/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-small-molecule-discovery/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-small-molecule-discovery&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-small-molecule-discovery.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
