---
title: MDAnalysis (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-06-11
summary: "Analyze MD trajectories from GROMACS, AMBER, NAMD, CHARMM, LAMMPS."
---

# MDAnalysis (Claude Skill)

Analyze MD trajectories from GROMACS, AMBER, NAMD, CHARMM, LAMMPS.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (GPL-2.0) |
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
  cp -r SciAgent-Skills/skills/structural-biology-drug-discovery/mdanalysis-trajectory ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Analyze MD trajectories from GROMACS, AMBER, NAMD, CHARMM, LAMMPS. Reads topology/trajectory into Universe objects; supports RMSD, RMSF, radius of gyration, contact maps, H-bonds, PCA, and custom distance/angle calculations. Use for post-simulation structural analysis; use OpenMM/GROMACS for running simulations.

**Primary use cases**: post-simulation structural analysis; use OpenMM/GROMACS for running simulations.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: GPL-2.0. The skill directory upstream is `skills/structural-biology-drug-discovery/mdanalysis-trajectory`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/structural-biology-drug-discovery/mdanalysis-trajectory/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/mdanalysis-trajectory/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=mdanalysis-trajectory&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmdanalysis-trajectory.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
