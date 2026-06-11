---
title: MACS3 (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-11
summary: "Poisson-model peak caller for ChIP-seq/ATAC-seq BAMs."
---

# MACS3 (Claude Skill)

Poisson-model peak caller for ChIP-seq/ATAC-seq BAMs.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (BSD-3-Clause) |
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
  cp -r SciAgent-Skills/skills/genomics-bioinformatics/macs3-peak-calling ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Poisson-model peak caller for ChIP-seq/ATAC-seq BAMs. MACS3 callpeak finds enriched regions (TF sites or histone marks) vs input/IgG; outputs BED narrowPeak/broadPeak for motif analysis, annotation, and differential binding. Use narrow peaks for TF ChIP-seq and ATAC-seq; broad for H3K27me3, H3K9me3, and other broad marks.

**Primary use cases**: Poisson-model peak caller for ChIP-seq/ATAC-seq BAMs.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: BSD-3-Clause. The skill directory upstream is `skills/genomics-bioinformatics/macs3-peak-calling`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/genomics-bioinformatics/macs3-peak-calling/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/genomics-bioinformatics/macs3-peak-calling/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=macs3-peak-calling&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmacs3-peak-calling.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
