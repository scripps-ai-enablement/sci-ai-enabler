---
title: Reactome (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-11
claude_science: true
summary: "Query Reactome pathways via REST: pathway queries, entity lookup, keyword search, gene list enrichment, hierarchy, cross-refs."
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches jaechang-hits/SciAgent-Skills, skill code CC BY 4.0, Reactome data CC BY 4.0, no OSV advisories"
---

# Reactome (Claude Skill)

Query Reactome pathways via REST: pathway queries, entity lookup, keyword search, gene list enrichment, hierarchy, cross-refs.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (CC-BY-4.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches supplier, skill code CC BY 4.0, Reactome data CC BY 4.0, no OSV advisories |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/systems-biology-multiomics/reactome-database ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Query Reactome pathways via REST: pathway queries, entity lookup, keyword search, gene list enrichment, hierarchy, cross-refs. Content + Analysis services. Python wrapper: reactome2py. For KEGG use kegg-database; for PPIs use string-database-ppi.

**Primary use cases**: Query Reactome pathways via REST: pathway queries, entity lookup, keyword search, gene list enrichment, hierarchy, cross-refs.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Genes & Ontologies* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: CC-BY-4.0. The skill directory upstream is `skills/systems-biology-multiomics/reactome-database`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/systems-biology-multiomics/reactome-database/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/systems-biology-multiomics/reactome-database/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=reactome-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Freactome-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
