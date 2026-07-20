---
title: Chemical Safety (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-07-19
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches Zitnik Lab (mims-harvard/ToolUniverse), Apache-2.0, skills/tooluniverse-chemical-safety confirmed present, no OSV advisories"
summary: ToolUniverse agent skill for chemical hazard and toxicology assessment via ADMET-AI, CTD toxicogenomics, AOPWiki, GHS/IARC classification, and regulatory safety data.
---

# Chemical Safety (ToolUniverse Claude Skill)

A ToolUniverse agent skill that assesses a compound's toxicological risk by combining predictive toxicology, toxicogenomics, structural alerts, and regulatory safety data into a graded risk profile.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-chemical-safety/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (ADMET-AI, CTD, PubChem/PubChemTox, AOPWiki, ChEMBL, STITCH, FDA, DrugBank) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches Zitnik Lab, Apache-2.0, skill dir confirmed, no OSV advisories |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-chemical-safety`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-chemical-safety ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the chemical-safety skill") rather than relying on automatic dispatch.

## What it does

Runs an eight-phase toxicology pipeline:

0. **Compound disambiguation** — resolve identity to SMILES, PubChem CID, ChEMBL ID.
1. **Predictive toxicology** — ADMET-AI endpoints (AMES mutagenicity, DILI, LD50, carcinogenicity, hERG).
2. **ADMET properties** — absorption, distribution, metabolism, excretion, CYP interactions.
3. **Toxicogenomics** — CTD chemical-gene-disease mapping; PubChemTox experimental data; AOPWiki adverse-outcome pathways.
4. **Regulatory safety** — FDA boxed warnings, contraindications, adverse reactions (pharmaceuticals only).
5. **Drug safety profile** — DrugBank toxicity, contraindications, interactions (pharmaceuticals only).
6. **Chemical-protein interactions** — STITCH binding networks, off-target effects.
7. **Structural alerts** — ChEMBL PAINS/Brenk/Glaxo alerts.

It synthesizes an integrated risk classification (Critical/High/Medium/Low) with T1–T4 evidence grading.

**Primary use cases**: hazard identification, occupational/consumer-product toxicity screening, dose-response evaluation, acute vs. chronic toxicity assessment, and safety triage of drug candidates.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Distinct from the [Small Molecule Discovery](tooluniverse-small-molecule-discovery.html) skill (identity/activity/sourcing) and the [Adverse Outcome Pathway](tooluniverse-adverse-outcome-pathway.html) and [Adverse Event Detection](tooluniverse-adverse-event-detection.html) skills — this one is a compound-level toxicology profile. ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-chemical-safety/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-chemical-safety/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-chemical-safety&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-chemical-safety.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
