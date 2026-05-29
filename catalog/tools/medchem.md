---
title: MedChem (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-05-25
summary: Claude skill wrapping MedChem — drug-likeness filters (Lipinski, Veber, Egan, Muegge), ADMET-flag detection, and medicinal-chemistry alerts on top of RDKit.
---

# MedChem (Claude Skill)

Claude skill providing Python recipes for [MedChem](https://medchem.datamol.io/), a medicinal-chemistry filtering library built on RDKit — drug-likeness rules, structural alerts, complexity metrics, and synthetic-accessibility scoring for compound-library triage.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS skill (MIT collection); MedChem itself is Apache-2.0 |
| **Capabilities** | Read/Write — Claude executes MedChem via the Bash/Python tool |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install medchem@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/medchem ~/.claude/skills/
  pip install medchem
  ```

Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- Drug-likeness rule sets — Lipinski's Rule of Five, Veber, Egan, Muegge
- Structural alerts — PAINS, BRENK, NIH, and other medicinal-chemistry filter catalogues
- Molecular-complexity metrics and synthetic-accessibility scoring (SAScore)
- ADMET-flag detection on compound libraries
- Parallel filter application across large screening sets

**Primary use cases**: Triage and prioritisation of virtual-screening hit lists, drug-likeness assessment for lead-optimisation analog sets, removal of pan-assay interference and reactive moieties before in-vitro follow-up.

## Notes

Skill is documentation plus Python recipes — Claude executes MedChem locally via Bash/Python. Designed to slot in after the `rdkit-skill` / `datamol` / `molfeat` steps in K-Dense's lead-optimisation example workflow. Rule cut-offs are configurable — defaults match the published medicinal-chemistry literature but should be tuned per project.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`scientific-skills/medchem/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/medchem/SKILL.md)
- [MedChem documentation — medchem.datamol.io](https://medchem.datamol.io/)
- [`datamol-io/medchem`](https://github.com/datamol-io/medchem)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=medchem&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmedchem.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
