---
title: CDXML Toolkit
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Hiu Fung Kevin Lee
availability: Beta
tool_categories: [Chemistry]
last_verified: 2026-07-25
summary: MCP server that draws molecules and reaction schemes to publication-ready ChemDraw CDXML, parses ELN/LCMS/NMR files, and reads structures from images.
---

# CDXML Toolkit

MCP server and Python toolkit that lets a Claude agent draw molecules and reaction schemes as publication-ready ChemDraw CDXML, extract structures from images, and parse reaction/analysis files — with tool-grounded chemistry to avoid SMILES hallucination.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Hiu Fung Kevin Lee](https://github.com/leehiufung911/cdxml-toolkit) |
| **Availability** | Beta — PyPI `cdxml-toolkit` v0.5.17 (2026) |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — resolves and renders structures, writes CDXML/PNG files, reads/writes ChemDraw objects in Office documents |

## How to install

**Prerequisites:** **Windows only** — requires ChemDraw / ChemOffice 2015+ installed (CDXML rendering, `render_to_png`, and Office OLE tools call ChemDraw via COM). Python 3.10–3.13 (3.14 is unsupported by TensorFlow/DECIMER).

Install into a dedicated conda environment:

```
conda create -n cdxml python=3.12 pip -y
conda activate cdxml
pip install cdxml-toolkit
cdxml-doctor --no-tests
```

(`cdxml-doctor --no-tests` is a one-shot setup check — it prints diagnostics and exits; it is not a long-lived service.)

- **Claude Desktop** — add to `%APPDATA%\Claude\claude_desktop_config.json`, pointing `command` at the Python interpreter inside the `cdxml` conda env (replace `YOUR_USERNAME`; run `where python` inside the activated env to find the exact path):
  ```json
  {
    "mcpServers": {
      "cdxml-toolkit": {
        "command": "C:\\Users\\YOUR_USERNAME\\miniconda3\\envs\\cdxml\\python.exe",
        "args": ["-m", "cdxml_toolkit.mcp_server"]
      }
    }
  }
  ```
  Claude Desktop launches this over stdio — you do **not** keep a terminal open.

- **Claude Code** — direct MCP add (stdio), using the same env Python interpreter:
  ```
  claude mcp add --transport stdio cdxml-toolkit -- "C:\Users\YOUR_USERNAME\miniconda3\envs\cdxml\python.exe" -m cdxml_toolkit.mcp_server
  ```
  (Upstream documents only the Claude Desktop JSON form; the `claude mcp add` equivalent above mirrors it — replace the interpreter path with your env's `python.exe`.) The package also installs a `cdxml-mcp` console entry point, so `claude mcp add --transport stdio cdxml-toolkit -- cdxml-mcp` works if the `cdxml` env is on your `PATH`.

Upstream also ships a `CLAUDE.md` in the repository root with anti-hallucination rules; copy it into your agent's working directory so the agent always resolves structures through tools rather than writing SMILES from memory or vision.

## What it does

Exposes **15 grounded chemistry tools** so the model reasons about chemistry while the tools handle structure resolution, 2D layout, and CDXML:

- **Resolution** — `resolve_name` (name/abbreviation/CAS/formula → molecule JSON), `modify_molecule` (6 edit operations with 162 named-reaction templates, returns MCS diffs to verify the change).
- **Rendering** — `draw_molecule` (single molecule → CDXML), `render_scheme` (YAML/text/reaction JSON → publication-ready CDXML), `render_to_png` (CDXML → PNG via ChemDraw COM).
- **Perception** — `parse_reaction` (ELN export → semantic JSON with species, roles, SMILES), `summarize_reaction`, `extract_structures_from_image` (image → validated SMILES via the DECIMER OCR neural network), `parse_scheme` (CDXML → species/steps/topology JSON).
- **Analysis** — `parse_analysis_file` (LCMS/NMR PDF → structured peak data), `format_lab_entry`.
- **Office integration** — `extract_cdxml_from_office` / `embed_cdxml_in_office` (pull/inject editable ChemDraw OLE objects in PPTX/DOCX), `convert_cdx_cdxml`, `search_compound` (SMILES-similarity search across directories).

**Primary use cases**: drawing publication-ready reaction schemes, digitizing structures from figures/screenshots, ELN and LCMS/NMR parsing, ChemDraw office-document automation.

## Notes

Grounding is the design goal: the bundled `CLAUDE.md` instructs the agent to never write SMILES from memory or vision — every structure must come from `resolve_name`, `modify_molecule`, or `extract_structures_from_image` (which runs DECIMER OCR and returns validated SMILES), and edits go through `modify_molecule` so an MCS diff confirms the transformation. Large CDXML/JSON outputs are written to files (the tool returns a path) to keep them out of the model's context window.

The Windows + ChemDraw requirement is a hard dependency for CDXML rendering, `render_to_png`, and the Office OLE tools; the toolkit is not usable on macOS/Linux or without a ChemDraw install. Distinct from the RDKit-based servers catalogued here (`chemcp`, `rdkit-mcp`, `rdkit-skill`, `rdkit-agent`), which render SVG/PNG offline via RDKit but do not produce editable ChemDraw CDXML or automate Office documents.

## Sources

- [`leehiufung911/cdxml-toolkit`](https://github.com/leehiufung911/cdxml-toolkit)
- [cdxml-toolkit on PyPI](https://pypi.org/project/cdxml-toolkit/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cdxml-toolkit&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcdxml-toolkit.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
