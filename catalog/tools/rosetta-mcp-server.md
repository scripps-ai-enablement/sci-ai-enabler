---
title: Rosetta MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Ariel Ben-Sasson (community OSS)
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-08-01
summary: "MCP server for Rosetta, PyRosetta and Biotite — run and validate RosettaScripts, score structures, translate protocols between the three APIs"
---

# Rosetta MCP Server

An MCP server that gives Claude working knowledge of the Rosetta protein-modeling stack: it runs and validates RosettaScripts XML, scores structures with PyRosetta, and translates protocols between Rosetta, PyRosetta and Biotite.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Ariel Ben-Sasson](https://github.com/Arielbs/rosetta-mcp-server) (community OSS) |
| **Availability** | GA — npm `rosetta-mcp-server` 1.3.1; last upstream push 2026-04-05; written up by [RosettaCommons](https://rosettacommons.org/2025/10/20/rosetta-cursor-simplifying-protein-design-with-ai-assistance/) 2025-10-20 |
| **Pricing** | Free / OSS — MIT per the npm package manifest (**Unverified —** no `LICENSE` file is committed to the GitHub repo, so redistribution terms are declared only in `package.json`). Rosetta and PyRosetta themselves require a separate licence from the University of Washington (free for non-commercial academic use). |
| **Capabilities** | Read/Write — reads and writes structure/XML files, executes local Rosetta and PyRosetta runs |

## How to install

The server is a Node wrapper around a Python process, so both runtimes are needed: **Node 14+** and **Python 3.8+**.

1. Install the server:
   ```
   npm install -g rosetta-mcp-server
   ```
2. Create the Python environment it drives, and install PyRosetta into it:
   ```
   uv venv ~/.venvs/rosetta-mcp
   ~/.venvs/rosetta-mcp/bin/pip install pyrosetta-installer biotite
   ~/.venvs/rosetta-mcp/bin/python -c "import pyrosetta_installer as I; I.install_pyrosetta()"
   ```
   (If you skip this, the PyRosetta-backed tools report "not available"; the server also exposes `install_pyrosetta_installer` to do it on first use.)
3. **Claude Code** — register it as a stdio server, passing the two paths it needs:
   ```
   claude mcp add --transport stdio rosetta \
     --env PYTHON_BIN=$HOME/.venvs/rosetta-mcp/bin/python \
     --env ROSETTA_BIN=/path/to/rosetta_scripts.default.macosclangrelease \
     -- rosetta-mcp-server
   ```
   Replace `/path/to/rosetta_scripts.default.macosclangrelease` with the absolute path to your compiled `rosetta_scripts` executable — the binary name encodes your platform and build (e.g. `rosetta_scripts.default.linuxgccrelease` on Linux), and it lives under `<rosetta>/source/bin/`. Omit `ROSETTA_BIN` if you only want the documentation, translation, validation and PyRosetta-scoring tools; `run_rosetta_scripts` and `find_rosetta_scripts` need it.
4. **Claude Desktop** — add the equivalent stdio entry to `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "rosetta": {
         "command": "rosetta-mcp-server",
         "args": [],
         "env": {
           "PYTHON_BIN": "/Users/you/.venvs/rosetta-mcp/bin/python",
           "ROSETTA_BIN": "/path/to/rosetta_scripts.default.macosclangrelease"
         }
       }
     }
   }
   ```
   Use absolute paths here — Claude Desktop does not expand `$HOME` or `~`.

You do not need to start the server yourself: Claude Code and Claude Desktop launch it over stdio. (The repo also ships `rosetta_mcp_http.js` for an HTTP deployment; that path is **Unverified —** the README documents only the stdio wrapper.)

## What it does

18 tools, grouped by what they are for:

- **Documentation and discovery** — `get_rosetta_info`, `get_rosetta_help` (accepts a mover name like `FastRelax`, a concept like `constraints` or `docking`, or a score function like `ref2015`, fetching live docs from rosettacommons.org), `pyrosetta_introspect`, `search_rosetta_web_docs`, `get_rosetta_web_doc`, `get_cached_docs`.
- **Execution and scoring** — `run_rosetta_scripts` (runs a RosettaScripts XML protocol), `pyrosetta_score` (total or `per_residue` energy breakdown).
- **Translation** — `xml_to_pyrosetta`, `rosetta_to_biotite` and `biotite_to_rosetta` (paired lookups across ~21 mappings covering structure I/O, SASA, RMSD, superimposition, secondary structure, contacts, hydrogen bonds, B-factors and angles), `translate_rosetta_script_to_biotite` (whole XML or PyRosetta script). Design and optimization operations are flagged as Rosetta-only rather than silently mistranslated.
- **Validation** — `validate_xml` (optionally `validate_against_schema`, checking element names against the Rosetta XSD), `rosetta_scripts_schema`.
- **Environment** — `python_env_info`, `check_pyrosetta`, `install_pyrosetta_installer`, `find_rosetta_scripts`.

**Primary use cases**: writing and debugging RosettaScripts protocols, scoring and relaxing structures with PyRosetta, porting Rosetta analysis code to the OSS Biotite stack.

## Notes

The upstream README documents registration for Cursor; the snippets above are the Claude Code and Claude Desktop equivalents of that same stdio entry. Two environment variables carry all the configuration — `PYTHON_BIN` (the interpreter holding PyRosetta and Biotite) and `ROSETTA_BIN` (the compiled `rosetta_scripts` executable) — and getting either wrong is the usual cause of tools reporting the software as unavailable; `python_env_info` and `check_pyrosetta` exist to diagnose exactly that.

Rosetta itself is **not** bundled and is not free software: it is distributed under licence from the University of Washington (no cost for academic and non-commercial use, paid for commercial). The `rosetta_to_biotite` translation tools exist partly to give a licence-free path for the analysis half of a workflow — [Biotite](https://www.biotite-python.org/) is BSD-3-Clause.

Complements the catalogued design-model wrappers [ProteinMPNN](proteinmpnn.html), [LigandMPNN](ligandmpnn.html) and [SolubleMPNN](solublempnn.html) (sequence design), and the analysis-side [PyMOL](pymol.html) and [MDAnalysis](mdanalysis-trajectory.html) skills. No `LICENSE` file is committed upstream — see the pricing row.

## Sources

- [`Arielbs/rosetta-mcp-server`](https://github.com/Arielbs/rosetta-mcp-server)
- [`rosetta-mcp-server` on npm](https://www.npmjs.com/package/rosetta-mcp-server)
- [RosettaCommons — "Rosetta + Cursor: Simplifying Protein Design with AI Assistance"](https://rosettacommons.org/2025/10/20/rosetta-cursor-simplifying-protein-design-with-ai-assistance/)
- [PyRosetta licensing](https://www.pyrosetta.org/home/licensing-pyrosetta)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=rosetta-mcp-server&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Frosetta-mcp-server.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
