---
title: BCFtools (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-11
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "provenance matches jaechang-hits SciAgent-Skills, repo resolves and active 2026-06, but GitHub reports license as NOASSERTION (non-standard), no OSV advisories"
summary: "CLI for VCF/BCF: filter, merge, annotate, query, normalize, compute stats."
---

# BCFtools (Claude Skill)

CLI for VCF/BCF: filter, merge, annotate, query, normalize, compute stats.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — SciAgent-Skills repo active but GitHub license is NOASSERTION, no OSV advisories |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/genomics-bioinformatics/variant/bcftools-variant-manipulation ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

CLI for VCF/BCF: filter, merge, annotate, query, normalize, compute stats. Core post-variant-calling: quality filtering, multi-sample merging, rsID annotation, genotype extraction. Samtools companion in HTSlib. Use GATK for complex indel realignment during calling; use VCFtools for population genetics stats.

**Primary use cases**: CLI for VCF/BCF: filter, merge, annotate, query, normalize, compute stats.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/genomics-bioinformatics/variant/bcftools-variant-manipulation`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/genomics-bioinformatics/variant/bcftools-variant-manipulation/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/genomics-bioinformatics/variant/bcftools-variant-manipulation/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=bcftools-variant-manipulation&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbcftools-variant-manipulation.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
