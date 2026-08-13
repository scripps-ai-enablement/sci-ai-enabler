---
title: Clinical Trial Design (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-08-09
summary: ToolUniverse agent skill that scores trial feasibility across endpoint, population, comparator, effect size, duration, and regulatory pathway using precedent trials.
verification: works
verified_on: 2026-08-13
reviewed_on: 2026-08-13
security: cleared
security_on: 2026-08-13
security_note: "mims-harvard/ToolUniverse Apache-2.0 confirmed this run, read-only over public sources, no external credentials"
---

# Clinical Trial Design (ToolUniverse Claude Skill)

A ToolUniverse agent skill that stress-tests a proposed trial before a statistician is engaged — sizing the eligible population, checking whether the FDA has previously accepted the endpoint, sourcing a comparator, and scoring overall feasibility from precedent.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-clinical-trial-design/`) |
| **Pricing** | Free / OSS (Apache-2.0); wraps public sources (Open Targets, ClinicalTrials.gov, ClinVar, gnomAD, COSMIC, DrugBank, FDA Orange Book, openFDA, FAERS, PubMed) |
| **Capabilities** | Read-only — evidence gathering and scoring; runs no statistical computation |
| **Verified** | works · 2026-08-13 |
| **Security** | cleared · 2026-08-13 — mims-harvard/ToolUniverse Apache-2.0, read-only public sources |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-clinical-trial-design`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-clinical-trial-design ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the clinical-trial-design skill") rather than relying on automatic dispatch.

## What it does

Assesses **six design dimensions** — endpoint (OS, PFS, ORR, or biomarker-based), population (unselected vs biomarker-enriched), comparator (placebo, active control, or historical), effect size, duration, and regulatory pathway — via **six parallel research paths**:

1. Patient-population sizing from disease prevalence and biomarker frequency, through an eligibility funnel to an enrollment projection.
2. Biomarker testing logistics — assay availability, cost, reimbursement.
3. Standard-of-care identification and comparator sourcing.
4. Endpoint precedent — has the FDA accepted this endpoint in this indication before?
5. Safety monitoring — dose-limiting toxicity definitions and organ-specific surveillance, informed by FAERS signals for the class.
6. Regulatory precedent — breakthrough designations, prior approval pathways, Orange Book approval history.

Scoring rules it applies:

- **Feasibility score ≥ 75** = HIGH (proceed); **50–74** = MODERATE (additional validation needed); **< 50** = LOW (de-risk before committing).
- Component weights: patient availability **30%**, endpoint precedent **25%**, regulatory clarity **20%**, comparator feasibility **15%**, safety monitoring **10%**.
- Effect-size sizing rules of thumb: a 20% improvement in objective response rate needs roughly **100 patients per arm**; a 50% improvement roughly **30 per arm**.
- Endpoints are graded **A** (regulatory acceptance, multiple precedents) through **D** (novel, unvalidated).

Output is a 14-section markdown report covering executive summary, disease background, population, biomarker strategy, endpoint, comparator, safety monitoring, study design, enrollment strategy, regulatory pathway, budget, risk, and success criteria.

**Primary use cases**: go/no-go feasibility on a proposed indication, endpoint selection defensible by precedent, enrollment projection and site-count sanity check, comparator and pathway strategy.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail.

**Upstream states plainly that this is precedent-based reasoning, not first-principles math** — the per-arm numbers above are order-of-magnitude anchors drawn from what comparable trials did, not a power calculation. Do not put them in a protocol. Run the actual sample-size calculation with [Power and Sample Size](power-and-sample-size.html), and take group-sequential or adaptive features to [Adaptive Designs](adaptive-designs.html). The 30/25/20/15/10 weighting is likewise a convention the skill imposes, not a validated instrument; a feasibility score is a way to compare two candidate designs, not an absolute probability of success.

Prevalence figures inherited from Open Targets and biomarker frequencies from gnomAD/COSMIC/ClinVar carry their own ascertainment biases, which propagate straight into the enrollment funnel — the eligible-population number is usually the most optimistic figure in the report.

Complements [Clinical Trial Protocol](clinical-trial-protocol.html) (the Anthropic plugin that drafts the protocol document once the design is settled), [Clinical Trial Matching](tooluniverse-clinical-trial-matching.html) (the patient-side counterpart), [Drug Regulatory Research](tooluniverse-drug-regulatory.html), and [Trial Reporting](trial-reporting.html). ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-clinical-trial-design/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-clinical-trial-design/SKILL.md)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-clinical-trial-design&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-clinical-trial-design.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
