---
title: Drug Mechanism Research (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-08-09
summary: ToolUniverse agent skill that traces a drug's mechanism from primary target through off-targets, pathways, FDA label, and pharmacogenomics.
verification: works
verified_on: 2026-08-13
reviewed_on: 2026-08-13
security: cleared
security_on: 2026-08-13
security_note: "mims-harvard/ToolUniverse Apache-2.0 confirmed this run, read-only over public sources, no external credentials"
---

# Drug Mechanism Research (ToolUniverse Claude Skill)

A ToolUniverse agent skill that answers "how does this drug actually work?" — chaining primary target, off-target binding, pathway context, the FDA label's own mechanism language, and pharmacogenomic modifiers into one evidence-tiered report.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-drug-mechanism-research/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public sources (Open Targets, ChEMBL, KEGG, Reactome, WikiPathways, STRING, DailyMed, PharmGKB, PubMed, Europe PMC) |
| **Capabilities** | Read-only — database and literature queries; runs no computation on your data |
| **Verified** | works · 2026-08-13 |
| **Security** | cleared · 2026-08-13 — mims-harvard/ToolUniverse Apache-2.0, read-only public sources |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-drug-mechanism-research`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-drug-mechanism-research ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the drug-mechanism-research skill") rather than relying on automatic dispatch.

## What it does

Runs an eight-step investigation:

1. **Drug resolution** — name to canonical IDs (ChEMBL ID via `OpenTargets_get_drug_id_description_by_name`, PharmGKB ID via `PharmGKB_search_drugs`) before any downstream query.
2. **Primary target** — the bound protein and the action type (inhibition, agonism, antagonism) via `OpenTargets_get_drug_mechanisms_of_action_by_chemblId` and `ChEMBL_get_drug_mechanisms`.
3. **Off-target assessment** — additional proteins bound at clinical concentrations, via `ChEMBL_get_target_activities` and `STRING_get_interaction_partners`, as the explanation for side effects and interactions.
4. **Pathway mapping** — the target's position in KEGG / Reactome / WikiPathways, distinguishing an *upstream* target (broad downstream effects) from a *downstream* one (narrow effects).
5. **Regulatory view** — the FDA label's own mechanism narrative parsed out of DailyMed, kept alongside the molecular detail rather than replaced by it.
6. **Pharmacogenomics** — variants that modify response, focused on CPIC Level A/B gene–drug pairs and FDA-labeled biomarkers.
7. **Literature evidence** — PubMed and Europe PMC support for each claimed mechanism.
8. **Integration** — a structured report ordered by an explicit evidence hierarchy.

Rules the skill applies: nanomolar binding affinity marks a **primary** target while micromolar affinity marks an **off-target** effect at clinical dose; when several targets converge on one pathway, that pathway is reported as the true mechanism, and targets in genuinely different pathways are reported separately rather than merged.

Findings are graded on a four-tier hierarchy — **T1** FDA labels, CPIC Level A guidelines, FDA PGx biomarkers; **T2** ChEMBL mechanisms with literature references and binding-affinity data; **T3** database MOA entries and pathway databases; **T4** PubMed / Europe PMC articles.

**Primary use cases**: explaining how an approved drug works, rationalizing an unexpected side effect as off-target binding, mechanism-based combination design, drafting the mechanism section of a report.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail.

The tier system is doing real work here — a mechanism supported only by a T3 database MOA entry is a database assertion, not a measurement, and the skill is designed to say so rather than flatten everything into one narrative. Binding-affinity calls depend on ChEMBL's assay records, which mix assay types and conditions; treat a nanomolar-vs-micromolar split as a triage heuristic, not a measured selectivity ratio.

Complements [Drug Research](tooluniverse-drug-research.html) (broader profile of one drug), [Drug-Target Validation](tooluniverse-drug-target-validation.html) (evidence that a target is worth pursuing), and [Drug-Drug Interaction](tooluniverse-drug-drug-interaction.html) (the interaction surface this skill's off-target step feeds). The individual sources are catalogued separately: [Open Targets](open-targets.html), [ChEMBL](chembl.html), [KEGG](kegg-database.html), [Reactome](reactome-database.html), [STRING](string-database-ppi.html), [DailyMed](dailymed-database.html), [ClinPGx / PharmGKB](clinpgx-database.html). ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-drug-mechanism-research/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-mechanism-research/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-drug-mechanism-research&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-drug-mechanism-research.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
