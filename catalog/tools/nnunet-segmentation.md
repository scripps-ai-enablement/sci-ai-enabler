---
title: nnU-Net (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-06-11
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches jaechang-hits, root LICENSE is CC BY 4.0, no OSV/GitHub advisories, read-only local nnU-Net analysis skill"
summary: "Medical image segmentation with nnU-Net's self-configuring framework — auto-selects architecture, preprocessing, training for any modality."
---

# nnU-Net (Claude Skill)

Medical image segmentation with nnU-Net's self-configuring framework — auto-selects architecture, preprocessing, training for any modality.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (Apache-2.0) |
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
  cp -r SciAgent-Skills/skills/medical-imaging/nnunet-segmentation ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Medical image segmentation with nnU-Net's self-configuring framework — auto-selects architecture, preprocessing, training for any modality. CT, MRI, microscopy, ultrasound in 2D, 3D full-res, 3D low-res, cascade. Pipeline: convert → plan/preprocess → train (5-fold CV) → best config → predict → ensemble. Use when classical segmentation fails and annotated data exists.

**Primary use cases**: classical segmentation fails and annotated data exists.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: Apache-2.0. The skill directory upstream is `skills/medical-imaging/nnunet-segmentation`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/medical-imaging/nnunet-segmentation/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/medical-imaging/nnunet-segmentation/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=nnunet-segmentation&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fnnunet-segmentation.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
