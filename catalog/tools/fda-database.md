---
title: openFDA (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Translational Medicine, Drug Repurposing and Discovery]
last_verified: 2026-06-11
claude_science: true
summary: "Query openFDA REST API for adverse events (FAERS), labeling, product info, recalls, enforcement."
---

# openFDA (Claude Skill)

Query openFDA REST API for adverse events (FAERS), labeling, product info, recalls, enforcement.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (CC0-1.0) |
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
  cp -r SciAgent-Skills/skills/structural-biology-drug-discovery/fda-database ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Query openFDA REST API for adverse events (FAERS), labeling, product info, recalls, enforcement. Search by drug name, ingredient, MedDRA, or NDC. 1k req/day no key; 120k with free key. For trials use clinicaltrials-database-search; for structures use drugbank-database-access or chembl-database-bioactivity.

**Primary use cases**: Query openFDA REST API for adverse events (FAERS), labeling, product info, recalls, enforcement.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Drug Regulatory* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: CC0-1.0. The skill directory upstream is `skills/structural-biology-drug-discovery/fda-database`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/structural-biology-drug-discovery/fda-database/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/fda-database/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=fda-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ffda-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
