---
title: Precision Oncology (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-06-28
summary: ToolUniverse agent skill that maps a tumor molecular profile to matched FDA-approved/investigational therapies, resistance mechanisms, and clinical trials.
---

# Precision Oncology (ToolUniverse Claude Skill)

A ToolUniverse agent skill that turns a tumor molecular profile (mutations, fusions, biomarkers) into actionable treatment recommendations by integrating variant-interpretation databases, drug-target evidence, resistance mechanisms, and matching clinical trials.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-precision-oncology/`) |
| **Pricing** | Free / OSS (Apache-2.0); database calls go through the ToolUniverse MCP server |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-precision-oncology`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-precision-oncology ~/.claude/skills/
  ```

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the precision-oncology skill") rather than relying on automatic dispatch.

## What it does

Runs a six-phase analysis over a supplied molecular profile:

- **Profile validation** — `MyGene_query_genes`, `UniProt_search`, `ChEMBL_search_targets` resolve gene/protein/target identifiers.
- **Variant interpretation** — `civic_search_variants` / `civic_get_variant`, `COSMIC_get_mutations_by_gene`, `GDC_get_mutation_frequency` / `_get_gene_expression` / `_get_survival`, `OncoKB_annotate_variant`, `cBioPortal_get_mutations`, `HPA_search_genes_by_query`.
- **Treatment options** — `OpenTargets_get_associated_drugs_by_target_ensemblID`, `DGIdb_get_drug_gene_interactions`, `DailyMed_search_spls`, `ChEMBL_get_drug_mechanisms`, mapped to FDA-approved therapies under a strict evidence hierarchy.
- **Resistance analysis** — `civic_search_evidence_items`, `PubMed_search_articles`, `alphafold_get_prediction`.
- **Clinical trials & safety** — `search_clinical_trials`, `get_clinical_trial_eligibility_criteria`, `FAERS_search_adverse_event_reports`, `FDA_get_warnings_and_cautions_by_drug_name`, `CPIC_list_guidelines`.
- **Literature** — `PubMed_search_articles`, `openalex_search_works`.

**Primary use cases**: molecular-tumor-board support, biomarker-to-therapy matching, resistance-mechanism review, trial eligibility screening.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. The skill operates on a **user-supplied molecular profile** rather than ingesting raw sequencing data, and several of its data sources (OncoKB, COSMIC) may themselves require user accounts/licenses for full access. Outputs are decision-support reasoning, not clinical advice. ToolUniverse ships ~68 such skills; the research, repurposing, target-validation, synergy, and drug-drug-interaction workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-precision-oncology/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-precision-oncology/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-precision-oncology&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-precision-oncology.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
