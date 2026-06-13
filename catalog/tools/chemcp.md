---
title: ChemCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Scott Reed
availability: GA
tool_categories: [Chemistry]
last_verified: 2026-06-13
summary: MCP App that renders interactive 2D molecular structures from SMILES and computes basic properties inside Claude conversations via RDKit.js.
---

# ChemCP

MCP App that draws interactive 2D molecular structure diagrams from SMILES strings — using RDKit.js — and reports basic computed properties directly inside a Claude conversation.

| | |
|---|---|
| **Type** | MCP server (MCP App) |
| **Supplier** | [Scott Reed](https://github.com/scottmreed/ChemCP) |
| **Availability** | GA — installable via npm |
| **Pricing** | Free / OSS (license not declared upstream) |
| **Capabilities** | Read-only — renders and describes molecules you supply |

## How to install

Requires Node.js 18+.

- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "chemcp": {
        "command": "npx",
        "args": ["chemcp"]
      }
    }
  }
  ```

- **Claude Code** — direct MCP add (stdio):
  ```
  claude mcp add --transport stdio chemcp -- npx chemcp
  ```

- **Claude.ai** — run the HTTP server and expose it through a tunnel, then add it as a custom connector:
  ```
  npm install -g chemcp
  chemcp --http            # long-lived service: keep this terminal open (serves http://localhost:3001/mcp)
  npx cloudflared tunnel --url http://localhost:3001
  ```
  In **Settings → Connectors → Add custom connector**, paste the tunnel URL with `/mcp` appended.

## What it does

Exposes a single `render_molecule` tool that accepts a SMILES string, draws the 2D structure with RDKit.js, and computes molecular weight, LogP, H-bond donors/acceptors, TPSA, rotatable bonds, and ring counts.

**Primary use cases**: quick in-chat molecule visualization, sanity-checking SMILES, lightweight property readouts.

## Notes

For Claude Desktop the `npx chemcp` entry runs over stdio (Claude launches it). For Claude.ai the `chemcp --http` server is long-lived — keep that terminal open while the connector is in use. Interactive visual rendering depends on MCP Apps support: Claude.ai custom connectors have experimental MCP Apps support and CSP restrictions may block RDKit.js, so Claude Desktop is the more reliable surface; Claude Code (CLI) clients without MCP Apps still receive the SMILES/property data as text but no rendered diagram. **Unverified —** no license file is declared in the repository; pricing is listed as Free / OSS on the basis of the public npm package but the redistribution terms are not stated upstream.

## Sources

- [`scottmreed/ChemCP`](https://github.com/scottmreed/ChemCP)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=chemcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fchemcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
