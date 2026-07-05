---
title: Binder Discovery (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-07-05
summary: ToolUniverse agent skill that discovers small-molecule binders for a target via known-ligand mining, similarity expansion, docking, and ADMET filtering into a ranked shortlist.
---

# Binder Discovery (ToolUniverse Claude Skill)

A ToolUniverse agent skill that runs a seven-phase small-molecule discovery workflow — from druggability assessment through docking and ADMET filtering — to hand back a ranked shortlist of candidate binders for a protein target.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-binder-discovery/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (ChEMBL, BindingDB, PubChem, PDB, AlphaFold) plus NVIDIA NIM generative/docking endpoints |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-binder-discovery`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-binder-discovery ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the binder-discovery skill") rather than relying on automatic dispatch.

## What it does

Executes seven sequential phases to identify and prioritise drug-like compounds:

1. **Target validation** — resolve IDs, assess druggability and binding sites (`UniProt_search`, `MyGene_query_genes`, `OpenTargets_get_target_tractability_by_ensemblID`, `DGIdb_*`).
2. **Known-ligand mining** — extract bioactivity from curated databases (`ChEMBL_get_target_activities`, `BindingDB_get_ligands_by_uniprot`, `GtoPdb_search_ligands`, `PubChem_search_assays_by_target_gene`).
3. **Structure analysis** — retrieve PDB/cryo-EM structures or predict them (`PDB_search_similar_structures`, `get_binding_affinity_by_pdb_id`, `EMDB_search_structures`, `alphafold_get_prediction`, `InterPro_get_protein_domains`).
4. **Docking validation** — validate pocket geometry with a reference inhibitor (`get_diffdock_info` — NVIDIA NIM DiffDock; `NvidiaNIM_boltz2`).
5. **Compound expansion** — similarity/substructure search and de novo generation (`ChEMBL_search_similar_molecules`, `PubChem_search_compounds_by_similarity`, `NvidiaNIM_genmol` scaffold hopping, `NvidiaNIM_molmim` analog generation).
6. **ADMET filtering** — eliminate poor compounds on physicochemical/toxicity rules (`ADMETAI_predict_physicochemical_properties`, `_predict_bioavailability`, `_predict_toxicity`, `_predict_CYP_interactions`, `ChEMBL_search_compound_structural_alerts`).
7. **Docking, ranking, and report** — score and prioritise the top ~20 candidates with literature-graded evidence.

**Primary use cases**: hit finding for a validated target, virtual-screening triage, generative analog design with ADMET gating.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Several tools in phases 4–5 route to **NVIDIA NIM** generative/docking endpoints (DiffDock, Boltz-2, GenMol, MolMIM) — those calls need ToolUniverse's NVIDIA NIM access configured, and may be rate-limited or unavailable without appropriate credentials; the ChEMBL/BindingDB/PubChem mining and ADMET-AI steps run against public APIs. ToolUniverse ships ~68 such skills; other drug-discovery workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-binder-discovery/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-binder-discovery/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-binder-discovery&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-binder-discovery.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
