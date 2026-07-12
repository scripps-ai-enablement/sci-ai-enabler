---
title: Cancer Variant Interpretation (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-12
summary: ToolUniverse agent skill that turns a gene + somatic variant + cancer type into an evidence-graded precision-oncology report with therapies, resistance, and matching trials.
---

# Cancer Variant Interpretation (ToolUniverse Claude Skill)

A ToolUniverse agent skill that interprets a somatic cancer mutation — gene, variant, and cancer type — into an actionable precision-oncology report with clinical evidence tiers, therapeutic options, resistance mechanisms, prognosis, and matching clinical trials.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-cancer-variant-interpretation/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (CIViC, OncoKB, cBioPortal, OpenTargets, ChEMBL, DrugBank, ClinicalTrials.gov) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-cancer-variant-interpretation`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-cancer-variant-interpretation ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the cancer-variant-interpretation skill") rather than relying on automatic dispatch.

## What it does

Runs an eight-phase somatic-mutation interpretation pipeline:

1. **Gene disambiguation** — resolve symbols to Ensembl/UniProt/Entrez IDs (`MyGene_query_genes`, `UniProt_search`, `ensembl_lookup_gene`).
2. **Clinical variant evidence** — query CIViC for curated evidence items and tiers.
3. **Mutation prevalence** — cBioPortal hotspot status and cancer-type distribution.
4. **Therapeutic associations** — FDA-approved and investigational drugs via OpenTargets, ChEMBL, DrugBank.
5. **Resistance mechanisms** — known on-target and bypass-pathway resistance variants.
6. **Clinical trials** — match to active trials via ClinicalTrials.gov.
7. **Prognostic impact** — survival and pathway context (Reactome, GTEx).
8. **Report synthesis** — prioritized, evidence-graded (T1–T4) treatment recommendations, each citing its database origin.

**Primary use cases**: precision-oncology variant reporting, therapy matching for a somatic mutation, resistance-mechanism review.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Output is report-first (creates the output file before populating data) and cancer-type specific. It surfaces clinical evidence but is a research aid, not a clinical decision tool — recommendations should be reviewed against primary sources. ToolUniverse ships ~150 such skills; other drug-discovery and oncology workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-cancer-variant-interpretation/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-cancer-variant-interpretation/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-cancer-variant-interpretation&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-cancer-variant-interpretation.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
