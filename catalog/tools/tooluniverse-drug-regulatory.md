---
title: Drug Regulatory Research (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-08-09
summary: ToolUniverse agent skill for jurisdiction-aware approval status — UNII identity, ATC/EPC class, Orange Book patents and exclusivity, generic availability, label parsing.
---

# Drug Regulatory Research (ToolUniverse Claude Skill)

A ToolUniverse agent skill that answers "is this drug approved, where, and when can a generic enter?" — FDA substance identity, therapeutic classification, Orange Book patent and exclusivity records, therapeutic-equivalence codes, and label content, always reported against a named market.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-drug-regulatory/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public sources (FDA GSRS, RxClass, FDA Orange Book, DailyMed, ClinicalTrials.gov, FAERS, PubMed) |
| **Capabilities** | Read-only — regulatory database and label queries |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-drug-regulatory`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-drug-regulatory ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the drug-regulatory skill") rather than relying on automatic dispatch.

## What it does

Runs eight sequential phases:

1. **Substance identification** — the official FDA UNII plus DrugBank / CAS / ATC cross-references (`FDAGSRS_search_substances`, `FDAGSRS_get_substance`, `FDAGSRS_get_structure`).
2. **Classification** — ATC, Established Pharmacologic Class, mechanism-of-action class and peer drugs in the same class (`RxClass_get_drug_classes`, `RxClass_find_classes`, `RxClass_get_class_members`).
3. **Approval and generic status** — approval pathway and whether a generic exists (`FDA_OrangeBook_search_drug`, `FDA_OrangeBook_check_generic_availability`, `FDA_OrangeBook_get_te_code`, `FDA_OrangeBook_get_approval_history`).
4. **Patent and exclusivity** — listed patents and data-protection periods with expiry dates (`FDA_OrangeBook_get_patent_info`, `FDA_OrangeBook_get_exclusivity`).
5. **Label parsing** — adverse reactions, dosing, contraindications, interactions and clinical pharmacology pulled from DailyMed SPLs (`DailyMed_parse_*`, `DailyMed_search_spls`).
6. **Clinical trials** — active and completed trials for the drug.
7. **Pharmacovigilance** — aggregated post-market adverse-event reports.
8. **Literature and history** — approval timeline and peer-reviewed evidence.

Rules the skill applies:

- **Approval pathways** — 505(b)(1) NDA (sponsor's own full safety/efficacy package), 505(b)(2) NDA (partial reliance on published literature or prior FDA findings), ANDA (generic, bioequivalence only).
- **Therapeutic equivalence** — an `AB` code means therapeutically equivalent and substitutable; `BX` or a missing code means substitutability is *not* established.
- **Exclusivity durations** — NCE (new chemical entity) 5 years, ODE (orphan drug) 7 years, PED (pediatric) adds 6 months to existing protection, NP/M (new product or formulation) variable.
- **The load-bearing heuristic** — generic availability needs *both* patent expiry *and* an approved ANDA, and an exclusivity code can block generic entry even after every listed patent has expired. Reading a patent expiry date as a generic-entry date is the error this rule exists to prevent.

Reports must name the jurisdiction (FDA vs EMA), give approval dates and application numbers, list every active exclusivity with its expiry, and keep clinical-trial adverse-event rates separate from post-market signals.

**Primary use cases**: loss-of-exclusivity and generic-entry timing, regulatory pathway selection for a new application, jurisdiction-aware approval status, drug class and peer-drug lookup.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail.

Upstream scopes several adjacent questions **out** of this skill: drug–drug interactions, pharmacogenomics, mechanism of action, and drug repurposing each route to a sibling skill. Orange Book and DailyMed reflect the U.S. market; the EMA side of a "where is this approved" question is thinner here than the FDA side, so verify non-U.S. status against the relevant national register before relying on it. Patent and exclusivity records are the FDA's listing, not a freedom-to-operate opinion.

Complements [Drug Mechanism Research](tooluniverse-drug-mechanism-research.html), [Pharmacovigilance](tooluniverse-pharmacovigilance.html), and [Clinical Trial Design](tooluniverse-clinical-trial-design.html) (which reuses the Orange Book and approval-history tools for pathway strategy). The underlying sources are catalogued separately: [openFDA](openfda.html), [FDA drug databases](fda-database.html), [DailyMed](dailymed-database.html), [DrugBank](drugbank.html). For a standalone MCP server over the Orange Book and Purple Book specifically, see [FDA MCP Server (OpenPharma)](fda-mcp.html). ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-drug-regulatory/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-regulatory/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)
- [FDA Orange Book](https://www.accessdata.fda.gov/scripts/cder/ob/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-drug-regulatory&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-drug-regulatory.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
