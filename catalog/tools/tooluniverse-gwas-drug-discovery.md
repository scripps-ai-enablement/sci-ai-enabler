---
title: GWAS Drug Discovery (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-05
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches Zitnik Lab (mims-harvard/ToolUniverse), Apache-2.0, skills/tooluniverse-gwas-drug-discovery confirmed present, no OSV advisories"
summary: ToolUniverse agent skill that turns GWAS-significant loci into druggable targets and repurposing candidates via fine-mapping, tractability scoring, and drug matching.
---

# GWAS Drug Discovery (ToolUniverse Claude Skill)

A ToolUniverse agent skill that connects genome-wide association signals to causal genes, ranks the druggable candidates, and matches them to existing drugs for repurposing.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-gwas-drug-discovery/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (GWAS Catalog, Open Targets, DGIdb, ChEMBL, openFDA, PubMed, ClinicalTrials.gov) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches Zitnik Lab, Apache-2.0, skill dir confirmed, no OSV advisories |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-gwas-drug-discovery`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-gwas-drug-discovery ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the gwas-drug-discovery skill") rather than relying on automatic dispatch.

## What it does

Runs a six-phase workflow from GWAS signal to actionable drug hypothesis:

1. **GWAS gene discovery** — identify disease-associated variants and map them to causal genes (`gwas_get_associations_for_trait`, `gwas_search_associations`, `OpenTargets_get_variant_credible_sets` for fine-mapping/eQTL).
2. **Druggability assessment** — evaluate target tractability and safety (`OpenTargets_get_target_tractability_by_ensemblID`, `_get_target_classes_by_ensemblID`, `_get_target_safety_profile_by_ensemblID`).
3. **Target prioritisation** — composite score (GWAS 40%, druggability 30%, clinical evidence 20%, novelty 10%).
4. **Existing drug search** — approved compounds and clinical candidates (`OpenTargets_get_associated_drugs_by_disease_efoId`, `ChEMBL_get_target_activities`, `DGIdb_get_drug_gene_interactions`).
5. **Clinical evidence and safety** — adverse-reaction and warning data (`FDA_get_adverse_reactions_by_drug_name`, `OpenTargets_get_drug_warnings_by_chemblId`).
6. **Repurposing opportunities** — match existing drugs to new disease indications, supported by literature and trial evidence (`PubMed_search_articles`, `ClinicalTrials_search_studies`).

**Primary use cases**: post-GWAS target triage, genetics-anchored repurposing, prioritising loci for follow-up given druggability and clinical precedent.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Phases 1–5 lean heavily on Open Targets `OpenTargets_*` tools — if the ToolUniverse Open Targets surface is degraded (see the [Open Targets](open-targets.html) flag), tractability and drug-association steps may be incomplete. Complements the [Drug Repurposing](drug-repurposing.html) and [Drug Target Validation](tooluniverse-drug-target-validation.html) skills. ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-gwas-drug-discovery/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-gwas-drug-discovery/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-gwas-drug-discovery&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-gwas-drug-discovery.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
