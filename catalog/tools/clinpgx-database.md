---
title: ClinPGx (PharmGKB) (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Translational Medicine, Drug Repurposing and Discovery]
last_verified: 2026-06-11
summary: "Query the ClinPGx (formerly PharmGKB) REST API plus the CPIC PostgREST companion API for pharmacogenomic clinical annotations, CPIC/DPWG dosing guidelines, gene-drug pairs, variant-drug associations …"
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches jaechang-hits SciAgent-Skills (CC BY 4.0 repo LICENSE); public ClinPGx/CPIC REST queries, no risky patterns"
---

# ClinPGx (PharmGKB) (Claude Skill)

Query the ClinPGx (formerly PharmGKB) REST API plus the CPIC PostgREST companion API for pharmacogenomic clinical annotations, CPIC/DPWG dosing guidelines, gene-drug pairs, variant-drug associations, FDA/EMA drug labels, and PGx pathways.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (CC-BY-SA-4.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches supplier, CC BY 4.0 repo LICENSE, public ClinPGx/CPIC queries, no OSV advisories |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/genomics-bioinformatics/databases/clinpgx-database ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Query the ClinPGx (formerly PharmGKB) REST API plus the CPIC PostgREST companion API for pharmacogenomic clinical annotations, CPIC/DPWG dosing guidelines, gene-drug pairs, variant-drug associations, FDA/EMA drug labels, and PGx pathways. Two-host architecture: api.clinpgx.org for annotation records, api.cpicpgx.org for genotype→recommendation lookups. No auth. For germline pathogenicity use clinvar-database; for somatic cancer PGx use cosmic-database or opentargets-database; for drug bioactivity use chembl-database-bioactivity.

**Primary use cases**: Query the ClinPGx (formerly PharmGKB) REST API plus the CPIC PostgREST companion API for pharmacogenomic clinical annotations, CPIC/DPWG dosing guidelines, gene-drug pairs, variant-drug associations, FDA/EMA drug labels, and PGx pathways.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: CC-BY-SA-4.0. The skill directory upstream is `skills/genomics-bioinformatics/databases/clinpgx-database`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/genomics-bioinformatics/databases/clinpgx-database/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/genomics-bioinformatics/databases/clinpgx-database/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=clinpgx-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fclinpgx-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
