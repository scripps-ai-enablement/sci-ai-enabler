---
title: smina (Claude Skill)
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
security_note: "provenance matches jaechang-hits/SciAgent-Skills, CC BY 4.0 skill collection, no OSV/GitHub advisories, local docking CLI wrapper with no credential requests"
summary: "Smina molecular docking CLI."
---

# smina (Claude Skill)

Smina molecular docking CLI.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (GPL-2.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches jaechang-hits/SciAgent-Skills, CC BY 4.0 collection, no advisories, local docking CLI wrapper |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/structural-biology-drug-discovery/smina-molecular-docking ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

smina molecular docking CLI. AutoDock Vina fork with customizable scoring functions, native SDF/MOL2/PDB ligand input, autoboxing, local energy minimization, and per-atom score breakdowns. Pipeline: receptor PDBQT prep -> ligand prep (RDKit/OpenBabel) -> dock via autobox or explicit grid -> rescore/minimize with custom scoring -> rank poses by affinity. Choose smina over Vina when you need custom scoring terms (--custom_scoring), local optimization of an existing pose (--local_only), per-atom contributions (--atom_term_data), or SDF/MOL2 ligands without manual PDBQT conversion. For unknown binding sites use diffdock; for the Python-bindings/Vinardo workflow use autodock-vina-docking.

**Primary use cases**: Smina molecular docking CLI.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: GPL-2.0. The skill directory upstream is `skills/structural-biology-drug-discovery/smina-molecular-docking`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/structural-biology-drug-discovery/smina-molecular-docking/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/smina-molecular-docking/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=smina-molecular-docking&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fsmina-molecular-docking.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
