---
title: GPCR Structural Pharmacology (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-08-16
summary: ToolUniverse agent skill for GPCR drug discovery — ligand classification, GPCRdb structures, mutation effects, and antibody-antigen interface analysis.
---

# GPCR Structural Pharmacology (ToolUniverse Claude Skill)

A ToolUniverse agent skill that walks a GPCR target from receptor identification through its ligand landscape, active/inactive structures, mutational pharmacology, and antibody interfaces.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-gpcr-structural-pharmacology/`) |
| **Pricing** | Free / OSS (Apache-2.0); GPCRdb, PDBePISA and SAbDab are free academic resources |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-gpcr-structural-pharmacology`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-gpcr-structural-pharmacology ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the GPCR structural pharmacology skill") rather than relying on automatic dispatch.

## What it does

Runs a five-phase receptor-pharmacology workflow:

1. **Receptor identification** — `GPCRdb_list_proteins` browses GPCRs by family or protein class; `GPCRdb_get_protein` pulls the receptor's annotations once the entry name is fixed.
2. **Ligand landscape** — `GPCRdb_get_ligands` classifies every known ligand by pharmacological type (agonist, antagonist, inverse agonist, biased agonist) with affinities, optionally cross-referenced against ChEMBL or PubChem.
3. **Structural data** — `GPCRdb_get_structures` filtered by conformational state (active / inactive / intermediate), with `PDBePISA_get_interfaces` and `PDBePISA_get_assemblies` for interface and biological-assembly analysis.
4. **Mutation and pharmacology** — `GPCRdb_get_mutations` extracts the functional and binding consequences of point mutations and maps them onto the ligand binding site, which is how orthosteric and allosteric pockets get told apart.
5. **Antibody structures** — `SAbDab_search_structures` and `SAbDab_get_structure` retrieve antibody entries with CDR annotations, with `PDBePISA_get_interfaces` again used for the antibody–antigen interface.

**Primary use cases**: GPCR drug discovery, biased-agonism analysis, receptor subtype selectivity, orthosteric vs allosteric pocket characterisation.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Coverage is bounded by GPCRdb — receptors with few solved structures return a thin phase 3, and the skill reports the ligand landscape from curated GPCRdb records rather than a fresh literature sweep.

For the chemistry side of a GPCR programme, pair with [Small Molecule Discovery](tooluniverse-small-molecule-discovery.html) and [ADMET Prediction](tooluniverse-admet-prediction.html); for the safety side, [Gene Liability Evaluation](tooluniverse-gene-liability.html). ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-gpcr-structural-pharmacology/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-gpcr-structural-pharmacology/SKILL.md)
- [GPCRdb](https://gpcrdb.org/)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-gpcr-structural-pharmacology&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-gpcr-structural-pharmacology.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
