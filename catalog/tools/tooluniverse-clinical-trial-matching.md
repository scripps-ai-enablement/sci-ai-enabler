---
title: Clinical Trial Matching (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-08-09
summary: ToolUniverse agent skill that turns a molecular profile into ranked trial matches across ClinicalTrials.gov, EU CTIS, and ISRCTN with evidence tiers.
verification: works
verified_on: 2026-08-13
reviewed_on: 2026-08-13
security: cleared
security_on: 2026-08-13
security_note: "mims-harvard/ToolUniverse Apache-2.0 confirmed this run, read-only over public sources, no external credentials"
---

# Clinical Trial Matching (ToolUniverse Claude Skill)

A ToolUniverse agent skill that takes a patient's molecular profile and clinical state and returns a ranked, evidence-tiered list of candidate trials — searching the U.S., EU, and UK registries rather than ClinicalTrials.gov alone.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-clinical-trial-matching/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public sources (ClinicalTrials.gov, EU CTIS, ISRCTN, CIViC, Open Targets, ChEMBL, DrugBank, MyGene, EFO/OLS, PharmGKB, FDA labels) |
| **Capabilities** | Read-only — registry and knowledge-base queries; produces a shortlist, not a clinical decision |
| **Verified** | works · 2026-08-13 |
| **Security** | cleared · 2026-08-13 — mims-harvard/ToolUniverse Apache-2.0, read-only public sources |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-clinical-trial-matching`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-clinical-trial-matching ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the clinical-trial-matching skill") rather than relying on automatic dispatch.

## What it does

Runs a ten-step matching workflow:

1. **Profile standardization** — resolve the disease to an ontology ID (`OpenTargets_get_disease_id_description_by_name`, `ols_search_efo_terms`), parse each alteration into gene + variant, normalize gene symbols via `MyGene_query_genes`.
2. **Broad discovery** — search by disease, biomarker, and intervention across `search_clinical_trials` (ClinicalTrials.gov), `CTIS_search_trials` (EU/EEA), and `ISRCTN_search_trials` (UK/international).
3. **Characterization** — batch-retrieve eligibility criteria, conditions and interventions, locations, status and dates, and outcome measures, **10 trials per batch**.
4. **Molecular eligibility matching** — parse free-text eligibility and score molecular fit.
5. **Drug–biomarker alignment** — the trial's drugs, their mechanisms, and FDA approval status for the biomarker combination.
6. **Evidence assessment** — cross-reference FDA approvals, published results, CIViC, and PharmGKB.
7. **Geography and feasibility** — site locations, enrollment status, proximity.
8. **Alternatives** — basket trials and expanded-access programs when no direct match exists.
9. **Scoring and ranking** — a composite Trial Match Score.
10. **Report synthesis** — an executive summary with ranked trials and a completeness checklist.

**Evidence tiers**: T1 FDA-approved or guideline-recommended biomarker–drug combination; T2 Phase III data; T3 Phase I/II data; T4 computational or preclinical only.

**Trial Match Score (0–100)** is the sum of four components — molecular match (0–40: exact variant 40, gene-level 30, pathway-level 20, none 10, explicitly excluded 0), clinical eligibility (0–25: all criteria met 25, most 18, some 10, ineligible 0), evidence strength (0–20: FDA-approved 20, Phase III 15, Phase II 10, Phase I 5), and trial phase (0–10).

**Primary use cases**: genotype-driven trial search for a precision-oncology or rare-disease case, biomarker-driven trial selection, eligibility triage across US/EU/UK registries.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail.

**This produces a shortlist for a clinician to review, not a clinical recommendation.** Eligibility is scored by parsing free-text criteria, which is exactly where registry entries are least structured — a "criteria met" call is a hypothesis to confirm against the trial's own screening process and the treating team. Registry records also lag reality: enrollment status, site activation, and cohort closures change faster than the postings. An `excluded` molecular call (score 0) is the one component worth trusting most, because exclusion criteria are usually stated explicitly.

Covering three registries is the distinguishing feature — a ClinicalTrials.gov-only search silently misses EU and UK trials for the same indication.

Complements [Precision Oncology](tooluniverse-precision-oncology.html) (interpretation of the same molecular profile) and [Clinical Trial Design](tooluniverse-clinical-trial-design.html) (the sponsor-side counterpart). The underlying registries and knowledge bases are catalogued separately: [ClinicalTrials.gov MCP](clinicaltrials-gov-mcp.html), [CIViC](civic.html), [Open Targets](open-targets.html), [ChEMBL](chembl.html), [DrugBank](drugbank.html), [MyGene](mygene.html), [ClinPGx / PharmGKB](clinpgx-database.html). ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-clinical-trial-matching/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-clinical-trial-matching/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-clinical-trial-matching&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-clinical-trial-matching.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
