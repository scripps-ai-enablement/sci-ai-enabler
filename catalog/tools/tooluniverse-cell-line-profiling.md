---
title: Cell Line Profiling (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-08-02
verification: works
verified_on: 2026-08-06
reviewed_on: 2026-08-06
verification_note: "mims-harvard/ToolUniverse repo and skills/tooluniverse-cell-line-profiling dir confirmed live this run, install instructions match the current upstream layout"
security: cleared
security_on: 2026-08-06
security_note: "mims-harvard/ToolUniverse Apache-2.0, wraps public DepMap/Cellosaurus/COSMIC/PharmacoDB read-only APIs, no credential requirements, no OSV advisories"
summary: ToolUniverse agent skill that ranks cancer cell lines for an experiment by cross-referencing DepMap, Cellosaurus, COSMIC, and PharmacoDB.
---

# Cell Line Profiling (ToolUniverse Claude Skill)

A ToolUniverse agent skill that answers "which cancer cell line should I use to study gene X?" with a ranked, evidence-backed shortlist.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-cell-line-profiling/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public resources (DepMap, Cellosaurus, COSMIC, cBioPortal CCLE, Human Protein Atlas, CellMarker, PharmacoDB, SYNERGxDB) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |
| **Verified** | works · 2026-08-06 |
| **Security** | cleared · 2026-08-06 — ToolUniverse Apache-2.0, public read-only APIs, no credentials |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-cell-line-profiling`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-cell-line-profiling ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the cell-line-profiling skill") rather than relying on automatic dispatch.

## What it does

Runs a five-phase selection workflow:

1. **Identity verification** — check the line against Cellosaurus for STR profile and misidentification/contamination flags, and DepMap for tissue, cancer type, and MSI status. Given only a cancer type, it pulls candidate lines and narrows them in later phases.
2. **Molecular profiling** — mutations from COSMIC and cBioPortal CCLE, expression from the Human Protein Atlas (which covers only 10 lines), and lineage markers from CellMarker.
3. **Gene dependencies** — CRISPR essentiality from DepMap Chronos scores, with **< −0.5** as the essentiality cut-off.
4. **Drug sensitivity** — IC50 and AAC from PharmacoDB across GDSC, CCLE, and PRISM, plus combination synergy (ZIP scores) from SYNERGxDB.
5. **Ranking** — weighted scoring out of 27 (mutation match ×3, co-mutation simplicity ×2, gene dependency ×2, drug data ×1, practical growth factors ×1), returned as ranked recommendations with biological rationale, growth characteristics, and known pitfalls.

**Primary use cases**: picking a model line for a target-validation experiment, sanity-checking a line already in use, finding lines with a specific mutation background for a drug-sensitivity study.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail.

**Known limitation the skill states upstream**: the DepMap API returns metadata only, so per-cell-line Chronos dependency scores come from a bundled `depmap_gene_dependency.py` script or the depmap.org portal rather than from a live tool call. Expect that phase to need a local script run or a manual portal lookup.

The Cellosaurus identity check in phase 1 is the part worth not skipping — a large fraction of published cancer cell-line work uses misidentified or cross-contaminated lines. Complements the standalone [DepMap](depmap.html), [cBioPortal](cbioportal.html), and [COSMIC](cosmic-database.html) entries, and pairs with [Drug Synergy](tooluniverse-drug-synergy.html) and [Drug Target Validation](tooluniverse-drug-target-validation.html). ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-cell-line-profiling/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-cell-line-profiling/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-cell-line-profiling&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-cell-line-profiling.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
