---
title: Drug Target Validation (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-06-21
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches Zitnik Lab (mims-harvard/ToolUniverse), Apache-2.0, skills/tooluniverse-drug-target-validation confirmed present, no OSV advisories"
summary: ToolUniverse agent skill that scores a drug target 0–100 across genetic, druggability, safety, and clinical-precedent gates with a GO/NO-GO recommendation.
---

# Drug Target Validation (ToolUniverse Claude Skill)

A ToolUniverse agent skill that validates a drug-target hypothesis with multi-dimensional computational evidence and returns a quantitative Target Validation Score, priority tier, and GO/NO-GO recommendation before any experimental commitment.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-drug-target-validation/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (Open Targets, ChEMBL, UniProt, Ensembl, HGNC, expression atlases) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches Zitnik Lab, Apache-2.0, skill dir confirmed, no OSV advisories |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-drug-target-validation`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-drug-target-validation ~/.claude/skills/
  ```

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the drug-target-validation skill") rather than relying on automatic dispatch.

## What it does

Runs a four-gate sequential validation model — failure at an early gate makes later gates irrelevant, and negative results are documented rather than hidden:

1. **Disease association** — genetic evidence (GWAS, rare/Mendelian variants), literature, and pathway support.
2. **Druggability** — structure and binding-pocket assessment, available chemical matter, and target class.
3. **Safety in normal tissue** — expression across critical organs, mouse-knockout lethality, known ADRs.
4. **Competitive landscape** — approved drugs, late-stage trials, and the differentiation bar.

It produces a 0–100 score (Disease Association 30 + Druggability 25 + Safety 20 + Clinical Precedent 15 + Validation Evidence 10) mapped to priority tiers: 80–100 Tier 1 (GO), 60–79 Tier 2 (conditional GO), 40–59 Tier 3 (caution), 0–39 Tier 4 (NO-GO). It resolves all identifiers (Ensembl, UniProt, ChEMBL, HGNC) first and computes statistics in Python rather than narrating hypothetical steps.

**Primary use cases**: target prioritisation before experimental work, GO/NO-GO triage of candidate targets, portfolio ranking by genetic and druggability evidence.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. The genetic-evidence and competitive-landscape gates lean on Open Targets `OpenTargets_*` tools — if the ToolUniverse Open Targets surface is degraded (see the [Open Targets](open-targets.html) flag), scores in those dimensions may be incomplete. ToolUniverse ships ~68 such skills; the research, repurposing, and synergy workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-drug-target-validation/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-target-validation/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-drug-target-validation&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-drug-target-validation.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
