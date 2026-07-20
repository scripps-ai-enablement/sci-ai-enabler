---
title: Rare Disease Genomics (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-19
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches Zitnik Lab (mims-harvard/ToolUniverse), Apache-2.0, skills/tooluniverse-rare-disease-genomics confirmed present, no OSV advisories"
summary: ToolUniverse agent skill for rare-disease investigation — Orphanet characterization, HPO phenotypes, causative genes, GenCC validity, ClinVar variants, trials, and repurposing.
---

# Rare Disease Genomics (ToolUniverse Claude Skill)

A ToolUniverse agent skill that works a rare disease from name disambiguation through phenotype mapping, causative-gene discovery, variant interpretation, and translational leads including trials and drug repurposing.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-rare-disease-genomics/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (Orphanet, GenCC, ClinVar, OLS, HMDB, ClinicalTrials.gov, Europe PMC) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches Zitnik Lab, Apache-2.0, skill dir confirmed, no OSV advisories |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-rare-disease-genomics`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-rare-disease-genomics ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the rare-disease-genomics skill") rather than relying on automatic dispatch.

## What it does

Runs a nine-phase (plus disambiguation) rare-disease workflow:

0. **Disambiguation** — resolve disease names to ORPHA codes.
1. **Disease characterization** — official definitions and classifications (Orphanet).
2. **Phenotype mapping** — HPO phenotypes with frequency labels.
3. **Causative gene discovery** — genes with association types.
4. **Gene-disease validity** — confidence via GenCC submitter consensus.
5. **Pathogenic variant lookup** — ClinVar with review-status context.
6. **Epidemiology** — prevalence and incidence.
7. **Clinical trials** — recruiting and completed studies.
8. **Literature** — supporting publications (Europe PMC).
9. **Report** — synthesized findings with evidence grading.

**Primary use cases**: rare-disease gene/variant triage, phenotype-driven diagnosis support, and translational-lead discovery (trials, repurposing candidates).

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Distinct from the [Rare Disease Diagnosis](tooluniverse-rare-disease-diagnosis.html) skill — this one is genomics-anchored (Orphanet→gene→variant), with translational repurposing leads. ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-rare-disease-genomics/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-rare-disease-genomics/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-rare-disease-genomics&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-rare-disease-genomics.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
