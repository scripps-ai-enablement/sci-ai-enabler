---
title: Target Research (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-05
summary: ToolUniverse agent skill that profiles a drug target across nine parallel research paths — expression, pathways, interactions, variants, druggability — into a cited report.
---

# Target Research (ToolUniverse Claude Skill)

A ToolUniverse agent skill that assembles a comprehensive intelligence dossier on a protein target by running nine parallel research paths and grading every finding with an evidence tier.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-target-research/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (Open Targets, UniProt, GTEx, HPA, STRING, ClinVar, gnomAD, ChEMBL, DGIdb) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-target-research`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-target-research ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the target-research skill") rather than relying on automatic dispatch.

## What it does

Runs a report-first, evidence-graded workflow: it first resolves all target identifiers (UniProt accession, Ensembl ID, gene symbol, Entrez ID, ChEMBL target ID, with GPCR detection), then executes nine parallel research paths:

- **Path 0** — Open Targets foundation (baseline across all dimensions)
- **Path 1** — Core identity (names, sequences, subcellular location)
- **Path 2** — Structure and domains (PDB, AlphaFold, InterPro; GPCRdb for GPCRs)
- **Path 3** — Function and pathways (GO, Reactome, KEGG, WikiPathways)
- **Path 4** — Protein interactions (STRING, IntAct, BioGRID, HPA)
- **Path 5** — Expression profiling (GTEx, HPA, single-cell via CELLxGENE)
- **Path 6** — Variants and disease (gnomAD constraints, ClinVar, DisGeNET, CIViC)
- **Path 7** — Druggability and safety (Pharos TDL, BindingDB, DepMap, Open Targets safety)
- **Path 8** — Literature (PubMed, EuropePMC, collision-aware filtering)

It synthesises the results into a 15-section markdown report with T1–T4 evidence grading and a GO/NO-GO recommendation.

**Primary use cases**: target dossier assembly before program commitment, novelty and safety assessment, competitive-landscape review for a candidate target.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Several paths lean on Open Targets `OpenTargets_*` tools — if the ToolUniverse Open Targets surface is degraded (see the [Open Targets](open-targets.html) flag), those dimensions may be incomplete. Complementary to the ToolUniverse [Drug Target Validation](tooluniverse-drug-target-validation.html) skill, which scores a target GO/NO-GO rather than profiling it. ToolUniverse ships ~68 such skills; other drug-discovery workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-target-research/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-target-research/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-target-research&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-target-research.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
