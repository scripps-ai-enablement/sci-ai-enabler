---
title: Drug Research (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-06-21
summary: ToolUniverse agent skill that compiles a comprehensive drug dossier — mechanism, targets, ADMET, trials, FAERS safety, pharmacogenomics, and approval history.
---

# Drug Research (ToolUniverse Claude Skill)

A ToolUniverse agent skill that assembles a comprehensive, citation-backed drug profile by querying chemistry, target, clinical-trial, safety, pharmacogenomic, and regulatory sources in a fixed research sequence.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-drug-research/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (PubChem, ChEMBL, DailyMed, PharmGKB, ClinicalTrials.gov, FDA FAERS/Orange Book, PubMed) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-drug-research`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-drug-research ~/.claude/skills/
  ```

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the drug-research skill") rather than relying on automatic dispatch.

## What it does

Enforces a 12-step, report-first research cycle that builds a structured markdown dossier before querying, then fills each section from a primary source with a documented fallback:

- **Identifier disambiguation** — resolve the compound via PubChem → ChEMBL → DailyMed → PharmGKB.
- **Chemistry & ADMET** — physicochemical properties from PubChem; ADMET predictions from the ADMET-AI suite.
- **Mechanism & targets** — FDA mechanism-of-action text validated against ChEMBL bioactivity (pChEMBL ≥ 6.0).
- **Clinical trials** — ClinicalTrials.gov search with phase distribution and outcomes.
- **Post-marketing safety** — FDA FAERS adverse-event patterns cross-referenced with label warnings.
- **Pharmacogenomics** — PharmGKB dosing guidance and annotations.
- **Regulatory history** — FDA Orange Book approval dates, exclusivity, and patents.
- **Literature synthesis & cross-source validation** — PubMed real-world evidence; reconcile conflicting values across databases with inline citations.

Representative ToolUniverse tools called: `PubChem_get_CID_by_compound_name`, `PubChem_get_compound_properties_by_CID`, `ChEMBL_search_drugs`, DailyMed mechanism/clinical-pharmacology lookups, and ClinicalTrials.gov / FAERS / PharmGKB queries.

**Primary use cases**: due-diligence drug dossiers, competitive-landscape profiling, mechanism-and-safety briefs for a single agent or compound.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. The skill is deliberate about provenance — it tracks the source and any fallback for every value and reconciles conflicts rather than averaging them. ToolUniverse ships ~68 such skills; the repurposing, target-validation, and synergy workflows are catalogued separately ([Drug Repurposing](drug-repurposing.html), [Drug Target Validation](tooluniverse-drug-target-validation.html), [Drug Synergy](tooluniverse-drug-synergy.html)).

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-drug-research/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-research/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-drug-research&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-drug-research.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
