---
title: Drug Repurposing (Claude Skill)
parent: All tools
grand_parent: Catalog
nav_order: 80
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-06-14
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier Zitnik Lab (mims-harvard org), repo Apache-2.0 and actively maintained (pushed 2026-07-20), read-only over public APIs, no OSV advisories"
summary: ToolUniverse agent skill that finds drug-repurposing candidates via target-, compound-, and disease-driven strategies with mechanism and feasibility scoring.
---

# Drug Repurposing (Claude Skill)

A ToolUniverse agent skill that systematically identifies and prioritises drug-repurposing candidates by combining target-, compound-, and disease-driven reasoning with mechanism rationale, clinical-trial precedent, and regulatory feasibility.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-drug-repurposing/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (Open Targets, ChEMBL, UniProt, Reactome, STRING) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches Zitnik Lab, Apache-2.0 maintained, read-only, no OSV advisories |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-drug-repurposing`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-drug-repurposing ~/.claude/skills/
  ```

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the drug-repurposing skill") rather than relying on automatic dispatch.

## What it does

Guides a five-phase workflow — disease/target analysis, drug discovery, safety assessment, literature review, and composite scoring — across three strategies:

- **Target-based** — identify disease-associated targets via genetic evidence (GWAS/rare variants), then find approved drugs that modulate them.
- **Compound-based** — start from an approved drug, map its full primary/off-target profile via ChEMBL bioactivity, then search for new indications where secondary targets are relevant.
- **Disease-driven** — start from a disease, derive associated targets/pathways via Reactome/STRING, then match to existing drugs.

Representative ToolUniverse tools called: `OpenTargets_get_disease_id_description_by_name`, `OpenTargets_get_associated_targets_by_disease_efoId`, `UniProt_get_entry_by_accession`, plus ChEMBL bioactivity and clinical-trial lookups.

**Primary use cases**: hypothesis-generating repurposing for orphan diseases, finding existing drugs for new indications, prioritising candidates by evidence and feasibility.

## Notes

The skill emphasises mechanistic validation — each link (target involvement, drug potency, pathway overlap) must be verified with a tool call rather than assumed. It is a thin reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. ToolUniverse ships ~68 such skills (drug research, target validation, drug-drug interaction, pharmacovigilance, precision oncology, rare-disease diagnosis); this entry covers the repurposing workflow specifically.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-drug-repurposing/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-repurposing/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=drug-repurposing&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdrug-repurposing.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
