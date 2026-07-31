---
title: ARCHS4 (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-11
summary: "Query ARCHS4 REST API for uniformly processed RNA-seq expression, tissue patterns, co-expression across 1M+ human/mouse samples."
verification: works
verified_on: 2026-07-29
reviewed_on: 2026-07-29
verification_note: "skills/genomics-bioinformatics/databases/archs4-database dir resolves, unchanged since 2026-05-28"
security: cleared
security_on: 2026-07-29
security_note: "provenance matches jaechang-hits; GitHub license classifier reports NOASSERTION but root LICENSE fetched this run is verbatim CC BY 4.0; public ARCHS4 REST queries, no risky patterns"
---

# ARCHS4 (Claude Skill)

Query ARCHS4 REST API for uniformly processed RNA-seq expression, tissue patterns, co-expression across 1M+ human/mouse samples.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (CC-BY-4.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-29 |
| **Security** | cleared · 2026-07-29 — provenance matches supplier, CC BY 4.0 repo LICENSE, public ARCHS4 queries, no OSV advisories |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/genomics-bioinformatics/databases/archs4-database ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Query ARCHS4 REST API for uniformly processed RNA-seq expression, tissue patterns, co-expression across 1M+ human/mouse samples. Retrieve z-scores, co-expressed genes, samples by metadata, HDF5 matrices. For variant population genetics use gnomad-database; for pathway enrichment use gget-genomic-databases (Enrichr).

**Primary use cases**: Query ARCHS4 REST API for uniformly processed RNA-seq expression, tissue patterns, co-expression across 1M+ human/mouse samples.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: CC-BY-4.0. The skill directory upstream is `skills/genomics-bioinformatics/databases/archs4-database`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/genomics-bioinformatics/databases/archs4-database/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/genomics-bioinformatics/databases/archs4-database/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=archs4-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Farchs4-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
