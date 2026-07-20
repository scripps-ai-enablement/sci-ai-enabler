---
title: PyMOL (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Google DeepMind
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-06-27
verification: degraded
verified_on: 2026-07-20
verification_note: "removed a stale copy of skills/scienceskillscommon (404 in repo, not imported by SKILL.md); pymol skill dir resolves on google-deepmind/science-skills"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier google-deepmind, Apache-2.0 code, maintained (pushed 2026-07-07), no OSV advisories"
summary: "Visualize, align, and render protein/molecular structures with PyMOL — headless, GPU-free, producing publication-quality PNGs and editable .pse sessions."
---

# PyMOL (Claude Skill)

Render and analyze 3D protein and small-molecule structures with PyMOL from inside Claude, producing publication-quality images, alignments, and interaction measurements without a display server or GPU.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Google DeepMind](https://github.com/google-deepmind/science-skills) |
| **Availability** | GA |
| **Pricing** | Free / OSS skill (Apache-2.0 code, CC-BY-4.0 docs); PyMOL itself is licensed separately — review [pymol.org](https://www.pymol.org/) |
| **Capabilities** | Read/Write — Claude writes and runs PyMOL Python scripts locally (`uv run`) over structure files in your project, writing PNG/`.pse`/stdout outputs |
| **Verified** | degraded · 2026-07-20 — removed stale scienceskillscommon copy line; pymol skill dir resolves |
| **Security** | cleared · 2026-07-20 — provenance matches google-deepmind, Apache-2.0, maintained, no OSV advisories |

## How to install

The `google-deepmind/science-skills` collection follows the Agent Skills `SKILL.md` spec. The repo's primary `npx skills add` path targets Gemini/Antigravity; for Claude the followable path is a manual copy of the skill directory.

- **Claude Code / Claude Desktop** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/google-deepmind/science-skills
  cp -r science-skills/skills/pymol ~/.claude/skills/
  ```
- **Prerequisite** — the skill runs PyMOL via `uv run` with PEP 723 dependency headers; install `uv` first if absent: `curl -LsSf https://astral.sh/uv/install.sh | sh`. PyMOL (open-source build, headless via OSMesa) installs into an isolated environment on first run — no GPU, X11, or display server required.

## What it does

Generates and executes PyMOL Python scripts headlessly, then interprets the results:

- **Visualization** — renders publication-quality PNG images of structures with custom representations and coloring.
- **Alignment / superposition** — overlays structures and reports RMSD.
- **Measurements** — distances, atom counts, and other stdout metrics.
- **Coloring schemes** — by B-factor / pLDDT confidence, binding-site highlighting, and protein–ligand interaction views.
- **Outputs** — PNG renders, editable `.pse` session files (openable in a local PyMOL), and stdout numeric metrics.

Inputs are structure files (`.pdb`, `.cif`, etc.) that already exist locally in your project directory.

**Primary use cases**: publication figures of protein structures, structure superposition and RMSD, pLDDT/B-factor coloring of predicted models, binding-site and protein–ligand interaction inspection.

## Notes

The skill operates on local coordinate files — pair it with [AlphaFold](alphafold.html) or the [RCSB PDB](pdb.html) servers to obtain structures first. It is **not** for AlphaFold prediction, docking, molecular dynamics, or sequence-only analysis. Rendering is headless via OSMesa, so it works on machines without a GPU or display. PyMOL is open-source under its own license (Schrödinger maintains both open-source and commercial Incentive builds) — review the PyMOL license before use; the skill itself is Apache-2.0 (code) / CC-BY-4.0 (docs). The upstream `npx skills add google-deepmind/science-skills/` command is oriented at Gemini/Antigravity (it writes to `~/.gemini/config/skills/`); for Claude, the manual copy into `~/.claude/skills/` shown above is the equivalent path.

## Sources

- [`google-deepmind/science-skills`](https://github.com/google-deepmind/science-skills)
- [`skills/pymol/SKILL.md`](https://github.com/google-deepmind/science-skills/blob/main/skills/pymol/SKILL.md)
- [PyMOL](https://www.pymol.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pymol&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpymol.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
