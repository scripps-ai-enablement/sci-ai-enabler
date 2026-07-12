---
title: Immunotherapy Response Prediction (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Translational Medicine]
last_verified: 2026-07-12
summary: ToolUniverse agent skill that predicts immune-checkpoint-inhibitor response by integrating TMB, MSI, PD-L1, HLA, and immune gene expression into a 0–100 score.
---

# Immunotherapy Response Prediction (ToolUniverse Claude Skill)

A ToolUniverse agent skill that predicts a patient's response to immune checkpoint inhibitors by integrating tumor mutational burden, microsatellite instability, PD-L1 expression, HLA status, and immune-related gene expression into a scored, evidence-graded report.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-immunotherapy-response-prediction/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (OpenTargets, CIViC, FDA pharmacogenomics, Human Protein Atlas, IEDB, Enrichr, ClinicalTrials.gov, PubMed) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-immunotherapy-response-prediction`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-immunotherapy-response-prediction ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the immunotherapy-response-prediction skill") rather than relying on automatic dispatch.

## What it does

Transforms a tumor profile into an ICI Response Score across eleven phases:

1. **Phases 1–4** — input standardization, TMB classification, neoantigen estimation, and MMR/MSI assessment with cancer-type-specific thresholds.
2. **Phases 5–7** — PD-L1 expression analysis, immune-microenvironment profiling, and mutation-based predictor evaluation (resistance vs. sensitivity mutations).
3. **Phases 8–11** — clinical-evidence synthesis, resistance risk stratification, multi-biomarker score integration (0–100), and drug-specific recommendations.

Key integrations: OpenTargets / MyGene / Ensembl (disease/gene), FDA pharmacogenomics + HPA cancer prognostics (biomarker validation), CIViC / UniProt / EnsemblVEP (mutation analysis), IEDB + Enrichr (immune profiling), FDA indications + trial search + PubMed (clinical evidence).

**Primary use cases**: checkpoint-inhibitor eligibility triage, multi-biomarker immunotherapy scoring, resistance-factor review.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Output is report-first with evidence-graded (T1–T4) component scoring and cancer-specific thresholds; it is a research aid, not a clinical decision tool. ToolUniverse ships ~150 such skills; other oncology and drug-discovery workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-immunotherapy-response-prediction/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-immunotherapy-response-prediction/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-immunotherapy-response-prediction&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-immunotherapy-response-prediction.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
