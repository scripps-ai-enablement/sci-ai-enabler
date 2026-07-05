---
title: Rare Disease Diagnosis (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-05
summary: ToolUniverse agent skill for rare-disease differential diagnosis — HPO phenotype matching to Orphanet/OMIM, gene-panel prioritization, and ACMG variant interpretation.
---

# Rare Disease Diagnosis (ToolUniverse Claude Skill)

A ToolUniverse agent skill that builds a rare-disease differential diagnosis from a patient's phenotype and genetic data by matching HPO terms to candidate diseases, prioritizing genes, and interpreting variants under ACMG criteria.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-rare-disease-diagnosis/`) |
| **Pricing** | Free / OSS (Apache-2.0); reasoning runs locally, database calls go through the ToolUniverse MCP server |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-rare-disease-diagnosis`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-rare-disease-diagnosis ~/.claude/skills/
  ```

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the rare-disease-diagnosis skill") rather than relying on automatic dispatch.

## What it does

Runs a phenotype-driven differential-diagnosis workflow, grading evidence by tier and writing a progressively-updated report:

- **Clinical reasoning** — forms an initial 3–5 candidate differential from the presentation.
- **Phenotype matching** — `HPO_search_terms` maps symptoms to Human Phenotype Ontology terms.
- **Candidate diseases** — `Orphanet_search_diseases`, `Orphanet_get_genes`, `OMIM_search`, `DisGeNET_search_gene` identify candidate diseases and associated genes.
- **Gene prioritization** — `MARRVEL_get_gene`, `MARRVEL_get_omim_phenotypes`, ClinGen validation, `GTEx_get_expression_summary`, plus CELLxGENE/ChIP-Atlas and KEGG/IntAct pathway context.
- **Variant interpretation** — `FAVOR_annotate_variant`, `ClinVar_get_variant_details`, `gnomad_get_variant`, with EVE and SpliceAI for missense/splice effects; AlphaFold2 + InterPro for structure-based analysis.
- **Literature & synthesis** — PubMed, bioRxiv/medRxiv, and OpenAlex evidence, synthesized into a tiered (T1–T4) diagnostic report.

**Primary use cases**: undiagnosed-disease-program support, phenotype-to-gene-panel prioritization, ACMG variant classification, differential-diagnosis review.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. The skill operates on **user-supplied phenotype and variant data** rather than raw sequencing files, and OMIM access may require a user account/license for full content. Outputs are decision-support reasoning, not a clinical diagnosis. ToolUniverse ships ~68 such skills; the research, repurposing, precision-oncology, pharmacovigilance, and drug-drug-interaction workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-rare-disease-diagnosis/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-rare-disease-diagnosis/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-rare-disease-diagnosis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-rare-disease-diagnosis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
