---
title: Chemical Sourcing (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-08-02
verification: works
verified_on: 2026-08-06
reviewed_on: 2026-08-06
verification_note: "mims-harvard/ToolUniverse repo and skills/tooluniverse-chemical-sourcing dir confirmed live this run, install instructions match the current upstream layout"
security: cleared
security_on: 2026-08-06
security_note: "mims-harvard/ToolUniverse Apache-2.0, wraps public PubChem/ChEMBL/ZINC/Enamine/eMolecules/Mcule read-only catalogs, places no orders, no credential requirements, no OSV advisories"
summary: ToolUniverse agent skill that finds commercial suppliers for a compound across ZINC, Enamine, eMolecules, and Mcule, with purchasable-analog fallback.
---

# Chemical Sourcing (ToolUniverse Claude Skill)

A ToolUniverse agent skill that answers "where can I buy this compound, and at what purity and price?" — and, when the exact compound is unavailable, what to buy instead.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-chemical-sourcing/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public and vendor catalogs (PubChem, ChEMBL, ZINC, Enamine, eMolecules, Mcule) |
| **Capabilities** | Read-only — searches catalogs and compares listings; places no orders |
| **Verified** | works · 2026-08-06 |
| **Security** | cleared · 2026-08-06 — ToolUniverse Apache-2.0, public read-only catalogs, no credentials |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-chemical-sourcing`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-chemical-sourcing ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the chemical-sourcing skill") rather than relying on automatic dispatch.

## What it does

Runs a five-phase procurement workflow over ten ToolUniverse tools — `PubChem_get_CID_by_compound_name`, `PubChem_get_compound_properties_by_CID`, `ChEMBL_get_molecule`, `ZINC_search_compounds`, `ZINC_get_compound`, `Enamine_search_catalog`, `Enamine_get_compound`, `eMolecules_search`, `eMolecules_get_compound`, and `Mcule_get_compound`:

1. **Identity resolution** — confirm the structure via PubChem CID and canonical SMILES before searching any catalog.
2. **Vendor search** — query ZINC (230M+ compounds), Enamine (~4M in stock plus make-on-demand), eMolecules (8M+ across multiple vendors), and Mcule (40M+).
3. **Price and availability comparison** — collate pricing, purity grade, stock status, and delivery timelines.
4. **Analog search** — when nothing exact is purchasable, find structurally similar in-stock alternatives at Tanimoto ≥ 0.7.
5. **Decision summary** — a vendor recommendation with ChEMBL bioactivity context for the compound and any proposed analog.

Purchasing rules the skill applies: in-stock beats cheaper (make-on-demand runs 2–4 weeks); purity floors of ≥ 95% for screening, ≥ 98% for dose-response, and ≥ 99% for reference standards; a listing priced above 5× the median usually signals a different salt form or purity grade, so costs are normalized per mg; and SMILES searches are preferred over name searches because names are ambiguous. Missing purity data, a 4-week "in stock" lead time, or a SMILES mismatch are flagged for vendor confirmation before ordering.

**Primary use cases**: procuring screening compounds, curating a purchasable virtual library, sourcing analogs for a SAR series.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. Prices and stock status are whatever the vendor catalogs report at query time — treat them as a shortlist to confirm with the supplier, not a quote.

Deeper on procurement than the commercial-availability phase of [Small Molecule Discovery](tooluniverse-small-molecule-discovery.html), which covers the same vendors in one step as part of a broader compound workup. Complements the standalone [ZINC](zinc-database.html), [PubChem](pubchem.html), and [ChEMBL](chembl.html) entries, and pairs with [SAR Analysis](sar-analysis.html) when the goal is buying out an analog series. ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-chemical-sourcing/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-chemical-sourcing/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-chemical-sourcing&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-chemical-sourcing.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
