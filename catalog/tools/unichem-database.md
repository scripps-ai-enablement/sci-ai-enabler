---
title: UniChem (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-06-11
summary: "Cross-reference compound IDs across 20+ databases (ChEMBL, DrugBank, PubChem, ChEBI, PDB, SureChEMBL, HMDB, DrugCentral, BindingDB) via UniChem REST API."
---

# UniChem (Claude Skill)

Cross-reference compound IDs across 20+ databases (ChEMBL, DrugBank, PubChem, ChEBI, PDB, SureChEMBL, HMDB, DrugCentral, BindingDB) via UniChem REST API.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (Apache-2.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/structural-biology-drug-discovery/unichem-database ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Cross-reference compound IDs across 20+ databases (ChEMBL, DrugBank, PubChem, ChEBI, PDB, SureChEMBL, HMDB, DrugCentral, BindingDB) via UniChem REST API. Resolve InChIKeys to source IDs, translate between source-specific IDs, find structurally related compounds by connectivity. POST with a JSON body for all cross-reference queries; only /sources is GET. No auth required.

**Primary use cases**: Cross-reference compound IDs across 20+ databases (ChEMBL, DrugBank, PubChem, ChEBI, PDB, SureChEMBL, HMDB, DrugCentral, BindingDB) via UniChem REST API.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: Apache-2.0. The skill directory upstream is `skills/structural-biology-drug-discovery/unichem-database`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/structural-biology-drug-discovery/unichem-database/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/unichem-database/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=unichem-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Funichem-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
