---
title: ADMET Prediction (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-08-02
summary: ToolUniverse agent skill that profiles a compound's absorption, distribution, metabolism, excretion, and toxicity into a graded pass/warn/fail scorecard.
---

# ADMET Prediction (ToolUniverse Claude Skill)

A ToolUniverse agent skill that turns a drug name or SMILES into a structured ADMET scorecard, combining machine-learned predictions with experimental toxicity records.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-admet-prediction/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public services (PubChem, PubChemTox, ChEMBL, ADMET-AI, SwissADME) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-admet-prediction`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-admet-prediction ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the admet-prediction skill") rather than relying on automatic dispatch.

## What it does

Runs a five-phase profiling workflow:

1. **Identity resolution** — resolve a drug name to a PubChem CID and canonical SMILES before any prediction runs.
2. **Physicochemical and drug-likeness** — Lipinski rule-of-five compliance, TPSA, logP, solubility, and PAINS/Brenk structural alerts via ADMET-AI and SwissADME.
3. **ADME prediction** — blood-brain-barrier penetrance, oral bioavailability, CYP450 interactions, clearance, and distribution.
4. **Toxicity assessment** — predicted AMES mutagenicity, drug-induced liver injury (DILI), hERG cardiotoxicity, and carcinogenicity, cross-checked against experimental PubChemTox records (LD50/LC50, GHS classification, target organs) plus nuclear-receptor and stress-response assay panels.
5. **Scorecard** — aggregates into a 13-category scorecard with pass/warn/fail verdicts, evidence tiers (T1–T3), and recommended next steps; ChEMBL supplies clinical phase and regulatory context.

Operating rules the skill enforces: identity is resolved before analysis, experimental data outranks prediction, and a toxicity **FAIL** on hERG, AMES, or DILI is treated as program-limiting until wet-lab evidence refutes it.

**Primary use cases**: pre-screening a compound library before assay spend, drug-likeness triage, CNS-penetrance and hepatotoxicity risk assessment.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Every value in the scorecard other than the PubChemTox and ChEMBL rows is a **model prediction**, not a measurement — the evidence tiers exist so a reader can tell which is which.

Overlaps with the ADMET phase of the [Small Molecule Discovery](tooluniverse-small-molecule-discovery.html) skill but goes considerably deeper on toxicity and evidence grading; use that skill for end-to-end compound characterization and this one when ADMET is the question. For a self-hostable MCP alternative built on ADMETlab 3.0 rather than ADMET-AI, see [ADMETlab MCP Server](admetlab-mcp.html); [Inductive Bio](inductive-bio.html) is the enterprise-gated connector in the same space. ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-admet-prediction/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-admet-prediction/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-admet-prediction&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-admet-prediction.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
