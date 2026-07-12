---
title: Adverse Event Detection (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-07-12
summary: ToolUniverse agent skill that detects adverse-drug-event signals from FDA FAERS with disproportionality statistics (PRR, ROR, IC) and a 0–100 safety signal score.
---

# Adverse Event Detection (ToolUniverse Claude Skill)

A ToolUniverse agent skill for pharmacovigilance signal detection — it mines FDA FAERS reports, drug labels, and disproportionality statistics to produce a quantitative safety-signal score with evidence grading.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-adverse-event-detection/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public APIs (openFDA FAERS + labels, OpenTargets, ChEMBL, DrugBank, PubMed/OpenAlex/EuropePMC) |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-adverse-event-detection`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-adverse-event-detection ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the adverse-event-detection skill") rather than relying on automatic dispatch.

## What it does

Executes a nine-phase pharmacovigilance pipeline:

1. **Drug disambiguation** — ChEMBL/DrugBank IDs, mechanism of action, approved indications.
2. **FAERS profiling** — frequency, seriousness, demographics, outcomes.
3. **Disproportionality analysis** — PRR, ROR, IC with 95% CIs; a signal is flagged when `PRR >= 2.0 AND lower CI > 1.0 AND N >= 3`.
4. **FDA label extraction** — boxed warnings, contraindications, interactions, special populations.
5. **Mechanism-based context** — target safety profiles, ADMET predictions, off-target effects.
6. **Comparative safety** — analysis across drug classes.
7. **Interactions** — drug-drug interactions and pharmacogenomic risk factors.
8. **Literature synthesis** — PubMed, OpenAlex, EuropePMC.
9. **Safety Signal Score** — 0–100 with evidence grading (T1–T4) and a report.

**Primary use cases**: post-market drug safety surveillance, disproportionality signal triage, comparative safety review of a drug class.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. FAERS disproportionality statistics are hypothesis-generating signals, not confirmed causal associations. ToolUniverse ships ~150 such skills; other drug-discovery and pharmacovigilance workflows (e.g. [Pharmacovigilance](tooluniverse-pharmacovigilance.html)) are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-adverse-event-detection/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-adverse-event-detection/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-adverse-event-detection&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-adverse-event-detection.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
