---
title: ViennaRNA (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Molecular and Cellular Biology, Integrative Structural and Computational Biology]
last_verified: 2026-06-11
verification: works
verified_on: 2026-07-29
verification_note: "repo jaechang-hits/SciAgent-Skills resolves (CC BY 4.0 root, pushed 2026-07-24) and the skills/molecular-biology/viennarna-structure-prediction dir install path is current; local ViennaRNA Python bindings, no network"
security: cleared
security_on: 2026-07-29
security_note: "provenance matches jaechang-hits, root LICENSE is CC BY 4.0, no OSV/GitHub advisories, read-only local ViennaRNA analysis"
summary: "Predict RNA secondary structure, MFE folding, base-pair probabilities, RNA-RNA interactions via ViennaRNA Python bindings."
---

# ViennaRNA (Claude Skill)

Predict RNA secondary structure, MFE folding, base-pair probabilities, RNA-RNA interactions via ViennaRNA Python bindings.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-29 |
| **Security** | cleared · 2026-07-29 — provenance matches jaechang-hits, CC BY 4.0, no advisories |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/molecular-biology/viennarna-structure-prediction ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Predict RNA secondary structure, MFE folding, base-pair probabilities, RNA-RNA interactions via ViennaRNA Python bindings. Pipeline: sequence → MFE → partition function and pair-probability matrix → dot-bracket → duplex. Use for siRNA/sgRNA targeting, ribozyme design, RNA accessibility. Use RNAfold CLI for batch use without Python.

**Primary use cases**: siRNA/sgRNA targeting, ribozyme design, RNA accessibility.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/molecular-biology/viennarna-structure-prediction`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/molecular-biology/viennarna-structure-prediction/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/molecular-biology/viennarna-structure-prediction/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=viennarna-structure-prediction&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fviennarna-structure-prediction.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
