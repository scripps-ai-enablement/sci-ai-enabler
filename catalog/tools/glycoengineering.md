---
title: Glycoengineering (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Immunology and Microbiology, Drug Repurposing and Discovery]
last_verified: 2026-05-26
summary: Claude skill for protein-glycosylation analysis — N-glycosylation sequon scanning, O-glycosylation hotspot prediction, and access to NetOGlyc/GlycoShield/GlycoWorkbench for therapeutic antibody and vaccine design.
---

# Glycoengineering (Claude Skill)

Claude skill that analyzes and engineers protein glycosylation — scans sequences for N-glycosylation sequons, predicts O-glycosylation sites, and orchestrates established glycan-analysis tools for therapeutic antibody and vaccine work.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) |
| **Availability** | GA — distributed via the K-Dense `claude-scientific-skills` plugin marketplace |
| **Pricing** | Free / OSS (skill source); some third-party tools it calls (e.g., NetOGlyc, NetNGlyc) have their own academic-use licences |
| **Capabilities** | Read/Write — local sequence scanning and orchestration of external glycan-prediction tools |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install glycoengineering@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/glycoengineering ~/.claude/skills/
  ```
  The skill uses `uv` to install its Python dependencies on first invocation; install `uv` first (`pipx install uv` or per the [uv install docs](https://docs.astral.sh/uv/getting-started/installation/)) so the skill can resolve its environment.

## What it does

- Scans protein sequences for **N-glycosylation sequons** (N-X-S/T, X ≠ P)
- Predicts **O-glycosylation** hotspots (Ser/Thr-rich regions)
- Wraps and orchestrates external glycan-analysis utilities:
  - **NetNGlyc / NetOGlyc** — N- and O-linked site prediction (DTU Health Tech)
  - **GlycoShield** — glycan-shielding analysis on glycoprotein structures
  - **GlycoWorkbench** — glycan-structure drawing and annotation
- Suggests sequence edits to add or remove glycosylation sites (e.g., for Fc-region effector tuning, mucin-domain redesign)
- Outputs annotated sequence reports usable as inputs to downstream protein-design or AlphaFold-Multimer runs

**Primary use cases**: therapeutic-antibody Fc engineering, glycoprotein developability assessment, vaccine-immunogen glycan-shield design, host-cell-line glyco-optimization for biologics manufacturing.

## Notes

- **External-tool licences vary.** NetNGlyc / NetOGlyc are free for academic use but require separate registration with DTU Health Tech for commercial use — the skill calls them but does not redistribute them.
- Pure-Python orchestration; no API keys required for the core sequon-scanning paths.
- Pairs naturally with the [AlphaFold (Claude Skill)](alphafold.html) and [PDB (Claude Skill)](pdb.html) entries when assessing how engineered glycan changes affect structure.

## Sources

- [`scientific-skills/glycoengineering/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/glycoengineering/SKILL.md)
- [`K-Dense-AI/claude-scientific-skills` marketplace](https://github.com/K-Dense-AI/claude-scientific-skills)
- [K-Dense scientific-skills catalog](https://github.com/K-Dense-AI/claude-scientific-skills/blob/main/docs/scientific-skills.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=glycoengineering&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fglycoengineering.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
