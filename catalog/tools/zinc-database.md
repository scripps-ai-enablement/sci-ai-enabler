---
title: ZINC (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-06-11
claude_science: true
summary: "Query ZINC15/ZINC22 virtual compound libraries (1.4B compounds, 750M purchasable)."
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches jaechang-hits/SciAgent-Skills, skill code CC BY 4.0, ZINC data free for research, no OSV advisories"
---

# ZINC (Claude Skill)

Query ZINC15/ZINC22 virtual compound libraries (1.4B compounds, 750M purchasable).

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (CC-BY-4.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches supplier, skill code CC BY 4.0, ZINC data free for research, no OSV advisories |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/structural-biology-drug-discovery/zinc-database ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Query ZINC15/ZINC22 virtual compound libraries (1.4B compounds, 750M purchasable). Search lead/fragment/drug-like compounds by MW, logP, reactivity, or SMILES similarity; download 3D sets for docking. For bioactivity use chembl-database-bioactivity; for approved drugs use drugbank-database-access.

**Primary use cases**: Query ZINC15/ZINC22 virtual compound libraries (1.4B compounds, 750M purchasable).

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *ZINC* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: CC-BY-4.0. The skill directory upstream is `skills/structural-biology-drug-discovery/zinc-database`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/structural-biology-drug-discovery/zinc-database/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/zinc-database/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=zinc-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fzinc-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
