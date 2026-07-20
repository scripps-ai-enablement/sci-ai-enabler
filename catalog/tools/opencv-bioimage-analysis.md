---
title: OpenCV (Bio-image) (Claude Skill)
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
security_note: "provenance matches jaechang-hits/SciAgent-Skills, CC BY 4.0 skill collection, no OSV/GitHub advisories, read-only local computer vision with no credential requests"
summary: "Computer vision for bio-image preprocessing, feature detection, real-time microscopy."
---

# OpenCV (Bio-image) (Claude Skill)

Computer vision for bio-image preprocessing, feature detection, real-time microscopy.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (Apache-2.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches jaechang-hits/SciAgent-Skills, CC BY 4.0 collection, no advisories, read-only local computer vision |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/cell-biology/opencv-bioimage-analysis ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Computer vision for bio-image preprocessing, feature detection, real-time microscopy. Color conversion, morphology, contour/blob detection, template matching, optical flow on fluorescence/brightfield. 10-100× faster than pure Python via C++. Use scikit-image for scientific morphometry/regionprops; OpenCV for real-time, video, classical feature extraction.

**Primary use cases**: Computer vision for bio-image preprocessing, feature detection, real-time microscopy.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: Apache-2.0. The skill directory upstream is `skills/cell-biology/opencv-bioimage-analysis`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/cell-biology/opencv-bioimage-analysis/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/cell-biology/opencv-bioimage-analysis/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=opencv-bioimage-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fopencv-bioimage-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
