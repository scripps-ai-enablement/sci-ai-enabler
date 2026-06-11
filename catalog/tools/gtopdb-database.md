---
title: Guide to Pharmacology (GtoPdb) (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Drug Repurposing and Discovery, Chemistry]
last_verified: 2026-06-11
summary: "Query IUPHAR/BPS Guide to Pharmacology (GtoPdb) for receptor-ligand interactions, target/ligand metadata, families, and approved drugs."
---

# Guide to Pharmacology (GtoPdb) (Claude Skill)

Query IUPHAR/BPS Guide to Pharmacology (GtoPdb) for receptor-ligand interactions, target/ligand metadata, families, and approved drugs.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (ODbL-1.0) |
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
  cp -r SciAgent-Skills/skills/structural-biology-drug-discovery/gtopdb-database ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Query IUPHAR/BPS Guide to Pharmacology (GtoPdb) for receptor-ligand interactions, target/ligand metadata, families, and approved drugs. Affinities (pKi/pIC50/pKd), action (Agonist/Antagonist/etc.), species, structures (SMILES/InChI). No auth. Always resolve targets via geneSymbol/accession; most metadata lives in sub-resources (/databaseLinks, /structure, /synonyms).

**Primary use cases**: Query IUPHAR/BPS Guide to Pharmacology (GtoPdb) for receptor-ligand interactions, target/ligand metadata, families, and approved drugs.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: ODbL-1.0. The skill directory upstream is `skills/structural-biology-drug-discovery/gtopdb-database`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/structural-biology-drug-discovery/gtopdb-database/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/gtopdb-database/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=gtopdb-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fgtopdb-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
