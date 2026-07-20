---
title: MOFA+ (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-11
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches jaechang-hits, root LICENSE is CC BY 4.0, no OSV/GitHub advisories, read-only local MOFA+ analysis skill"
summary: "Multi-Omics Factor Analysis v2 (MOFA+) with mofapy2."
---

# MOFA+ (Claude Skill)

Multi-Omics Factor Analysis v2 (MOFA+) with mofapy2.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (LGPL-3.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches jaechang-hits, CC BY 4.0, no advisories |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/systems-biology-multiomics/mofaplus-multi-omics ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Multi-Omics Factor Analysis v2 (MOFA+) with mofapy2. Jointly decompose omics layers (scRNA, ATAC, proteomics, methylation) into latent factors capturing major variation. Multi-group designs. AnnData views → MOFA object → train → variance explained → correlate factors with metadata → visualize/cluster → enrich top loadings.

**Primary use cases**: Multi-Omics Factor Analysis v2 (MOFA+) with mofapy2.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: LGPL-3.0. The skill directory upstream is `skills/systems-biology-multiomics/mofaplus-multi-omics`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/systems-biology-multiomics/mofaplus-multi-omics/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/systems-biology-multiomics/mofaplus-multi-omics/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=mofaplus-multi-omics&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmofaplus-multi-omics.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
