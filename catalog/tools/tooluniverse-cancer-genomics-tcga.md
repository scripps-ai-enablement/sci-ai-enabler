---
title: Cancer Genomics TCGA (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-19
summary: ToolUniverse agent skill for TCGA/GDC cancer genomics — cohort construction, clinical metadata, somatic mutation frequencies, CNV, survival analysis, and OncoKB variant interpretation.
---

# Cancer Genomics TCGA (ToolUniverse Claude Skill)

A ToolUniverse agent skill that runs cancer-type-specific TCGA/GDC analyses from cohort selection through somatic mutation frequencies, copy-number changes, survival, and clinically actionable variant annotation.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-cancer-genomics-tcga/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (GDC/TCGA, Progenetix, OncoKB) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-cancer-genomics-tcga`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-cancer-genomics-tcga ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the cancer-genomics-tcga skill") rather than relying on automatic dispatch.

## What it does

Runs a six-phase cancer-genomics workflow:

1. **Study selection** — identify and confirm TCGA projects (`GDC_list_projects`, `GDC_search_cases`).
2. **Clinical data** — patient demographics, diagnoses, treatments (`GDC_get_clinical_data`).
3. **Somatic mutations** — mutation frequencies and specific variants (`GDC_get_ssm_by_gene`, `GDC_get_mutation_frequency`).
4. **CNV analysis** — copy-number amplifications/deletions (`Progenetix_cnv_search`, `Progenetix_search_biosamples`).
5. **Survival analysis** — Kaplan-Meier curves and log-rank p-values split by mutation status (`GDC_get_survival`).
6. **Variant interpretation** — oncogenicity and FDA-approved therapies (`OncoKB_annotate_variant`).

The skill emphasizes cancer-type-specific cohorts and warns against uncontextualized pan-cancer queries.

**Primary use cases**: cohort-based somatic-mutation profiling, biomarker survival stratification, actionable-variant triage, and evidence for oncology target/repurposing hypotheses.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Complements the [Precision Oncology](tooluniverse-precision-oncology.html) and [Cancer Variant Interpretation](tooluniverse-cancer-variant-interpretation.html) skills — this one is the TCGA/GDC cohort-analysis workflow specifically. ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-cancer-genomics-tcga/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-cancer-genomics-tcga/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-cancer-genomics-tcga&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-cancer-genomics-tcga.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
