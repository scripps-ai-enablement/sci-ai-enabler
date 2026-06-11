---
title: MaxQuant (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-11
summary: "MaxQuant + Perseus proteomics pipeline: run MaxQuant for LFQ and SILAC; parse proteinGroups.txt in Python; filter contaminants/decoys; log2 + median-normalize; impute MNAR; t-test with …"
---

# MaxQuant (Claude Skill)

MaxQuant + Perseus proteomics pipeline: run MaxQuant for LFQ and SILAC; parse proteinGroups.txt in Python; filter contaminants/decoys; log2 + median-normalize; impute MNAR; t-test with FDR; volcano plot; GO/pathway enrichment.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (Apache-2.0) |
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
  cp -r SciAgent-Skills/skills/proteomics-protein-engineering/maxquant-proteomics ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

MaxQuant + Perseus proteomics pipeline: run MaxQuant for LFQ and SILAC; parse proteinGroups.txt in Python; filter contaminants/decoys; log2 + median-normalize; impute MNAR; t-test with FDR; volcano plot; GO/pathway enrichment. Use Proteome Discoverer for Thermo-native processing; FragPipe/MSFragger for GPU-accelerated DB search.

**Primary use cases**: MaxQuant + Perseus proteomics pipeline: run MaxQuant for LFQ and SILAC; parse proteinGroups.txt in Python; filter contaminants/decoys; log2 + median-normalize; impute MNAR; t-test with FDR; volcano plot; GO/pathway enrichment.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: Apache-2.0. The skill directory upstream is `skills/proteomics-protein-engineering/maxquant-proteomics`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/proteomics-protein-engineering/maxquant-proteomics/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/proteomics-protein-engineering/maxquant-proteomics/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=maxquant-proteomics&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmaxquant-proteomics.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
