---
title: RDKit Agent
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: scottmreed
availability: Alpha
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-07-11
summary: WASM-based cheminformatics CLI, Node library, and MCP server that validates, converts, and analyzes SMILES/SMIRKS/InChI with no Python runtime.
---

# RDKit Agent

Agent-first cheminformatics toolkit powered by RDKit compiled to WebAssembly — validate, repair, convert, and analyze chemical notation with structured JSON output and no Python runtime.

| | |
|---|---|
| **Type** | MCP server (also ships as a CLI, Node library, and Claude Code skill/plugin) |
| **Supplier** | [scottmreed](https://github.com/scottmreed/rdkit-agent) |
| **Availability** | Alpha — npm `rdkit-agent` v0.1.1, published 2026-03-16 |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — read-only chemistry analysis; writes SVG/PNG images and edited structures |

## How to install

Prerequisite: Node.js ≥ 16. RDKit runs as WebAssembly, so there is no native build step or Python dependency.

- **Claude Code — MCP server (stdio).** Install the CLI globally, then register it. Claude Code launches the process itself via stdio — you do not need to keep `rdkit-agent mcp` running in a separate terminal.
  ```
  npm install -g rdkit-agent
  claude mcp add --transport stdio rdkit-agent -- rdkit-agent mcp
  ```
  To verify the server boots before registering, run `rdkit-agent mcp` once and Ctrl-C after it starts.
- **Claude Desktop — MCP server (stdio).** After `npm install -g rdkit-agent`, add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "rdkit-agent": {
        "command": "rdkit-agent",
        "args": ["mcp"]
      }
    }
  }
  ```
- **Claude Code — as a skill** (auto-invoked for cheminformatics tasks):
  ```
  npx skills add scottmreed/rdkit-agent -g
  ```
  The upstream README shows the skill shortcut as bare `/rdkit-agent`. When installed as a plugin, plugin skills resolve as `/<plugin>:<skill>` — invoke `/rdkit-agent:rdkit-agent` if the bare form does not resolve.
- **Claude Code — as a plugin:**
  ```
  claude plugin install scottmreed/rdkit-agent
  ```

## What it does

Exposes 20+ cheminformatics subcommands as MCP tools:

- `check` — validate SMILES / SMIRKS / reactions
- `repair-smiles` — reconstruct malformed SMILES
- `convert` — format conversion (SMILES ↔ InChI / InChIKey / MOL / SDF)
- `descriptors` — molecular properties (MW, LogP, TPSA, HBD, HBA, …)
- `similarity` — Tanimoto similarity
- `filter` — descriptor-based filtering (e.g., Lipinski rules)
- `draw` — SVG / PNG rendering with atom/bond highlighting
- `react` — apply reaction SMIRKS to reactants
- `stereo` — stereocenter analysis
- `atom-map` — manage atom mapping
- `balance`, `fg`, `subsearch`, `fingerprint`, `scaffold`, `rings`, `stats`, `edit`, `schema`, `version`

**Primary use cases**: SMILES validation and repair, notation interconversion, descriptor calculation, reaction manipulation and atom mapping — without executing Python locally.

## Notes

stdio transport. RDKit runs as WebAssembly (`@rdkit/rdkit ≥ 2022.03` for reaction support), so there is no Python runtime — the author reports ~1 ms warm-path latency. Distinct from the [TandemAI RDKit MCP Server](rdkit-mcp.html) (Python-based, exposes RDKit modules) and the K-Dense [RDKit Skill](rdkit-skill.html) (writes and runs Python locally): this one is Node/WASM and adds SMILES repair, reaction balancing, and atom-mapping tools not present in those. Same author as [ChemCP](chemcp.html) (interactive molecule rendering), but a separate package.

Early-stage (v0.1.x) → `availability: Alpha`. Community project, not vendor-affiliated.

## Sources

- [`scottmreed/rdkit-agent`](https://github.com/scottmreed/rdkit-agent)
- [npm `rdkit-agent`](https://registry.npmjs.org/rdkit-agent) (v0.1.1, MIT, published 2026-03-16)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=rdkit-agent&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Frdkit-agent.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
