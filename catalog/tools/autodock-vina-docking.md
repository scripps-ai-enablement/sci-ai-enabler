---
title: AutoDock Vina (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-06-11
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches jaechang-hits SciAgent-Skills, committed root LICENSE is CC BY 4.0 (GitHub classifier NOASSERTION), maintained (pushed 2026-06-15), public read-only docking skill, no OSV advisories"
summary: "Molecular docking with AutoDock Vina (Python API)."
---

# AutoDock Vina (Claude Skill)

Molecular docking with AutoDock Vina (Python API).

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (CC-BY-4.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — SciAgent-Skills root LICENSE is CC BY 4.0, maintained, public read-only docking skill, no OSV advisories |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/structural-biology-drug-discovery/autodock-vina-docking ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Molecular docking with AutoDock Vina (Python API). Receptor/ligand prep (Meeko + RDKit), grid box, docking, pose and binding energy analysis, and batch virtual screening.

**Primary use cases**: Molecular docking with AutoDock Vina (Python API).

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: CC-BY-4.0. The skill directory upstream is `skills/structural-biology-drug-discovery/autodock-vina-docking`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/structural-biology-drug-discovery/autodock-vina-docking/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/autodock-vina-docking/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=autodock-vina-docking&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fautodock-vina-docking.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
