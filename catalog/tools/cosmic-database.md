---
title: COSMIC (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Translational Medicine, Molecular and Cellular Biology]
last_verified: 2026-06-11
summary: "Query COSMIC for cancer somatic mutations, gene census, mutational signatures, drug resistance variants."
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "skill provenance/CC BY 4.0 clear but COSMIC data is CC-BY-NC-SA-4.0 (non-commercial) and requires registration; note the data-use restriction"
---

# COSMIC (Claude Skill)

Query COSMIC for cancer somatic mutations, gene census, mutational signatures, drug resistance variants.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (CC-BY-NC-SA-4.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — skill CC BY 4.0 and provenance clear, but COSMIC data is CC-BY-NC-SA-4.0 (non-commercial, registration required) |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/genomics-bioinformatics/databases/cosmic-database ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Query COSMIC for cancer somatic mutations, gene census, mutational signatures, drug resistance variants. REST API v3.1 supports gene/sample/variant queries; free registration. For germline use clinvar-database; for drug-target data use opentargets-database or chembl-database-bioactivity.

**Primary use cases**: Query COSMIC for cancer somatic mutations, gene census, mutational signatures, drug resistance variants.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: CC-BY-NC-SA-4.0. The skill directory upstream is `skills/genomics-bioinformatics/databases/cosmic-database`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/genomics-bioinformatics/databases/cosmic-database/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/genomics-bioinformatics/databases/cosmic-database/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cosmic-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcosmic-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
