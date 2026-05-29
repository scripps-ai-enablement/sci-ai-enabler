---
title: RDKit MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: TandemAI
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-05-20
summary: MCP server exposing the full RDKit API as discrete tool calls so Claude can run cheminformatics without executing Python locally.
---

# RDKit MCP Server (TandemAI)

MCP server that exposes the full RDKit 2025.3.1 surface as discrete tool calls — useful when local Python execution is disabled or undesirable.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [TandemAI Inc.](https://github.com/tandemai-inc/rdkit-mcp-server) |
| **Availability** | GA — targets RDKit 2025.3.1, actively developed |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write |

Clone, install dependencies, and verify the server starts:

```
git clone https://github.com/tandemai-inc/rdkit-mcp-server
cd rdkit-mcp-server
pip install -r requirements.txt
python run_server.py --settings settings.yaml   # Ctrl-C once you confirm it boots
```

Then register with Claude Code (replace `/path/to/rdkit-mcp-server` with the absolute path — e.g., `$(pwd)` if still in that directory):

```
claude mcp add --transport stdio rdkit -- python /path/to/rdkit-mcp-server/run_server.py --settings /path/to/rdkit-mcp-server/settings.yaml
```

Or for Claude Desktop, add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rdkit": {
      "command": "python",
      "args": ["/path/to/rdkit-mcp-server/run_server.py", "--settings", "/path/to/rdkit-mcp-server/settings.yaml"]
    }
  }
}
```

Enumerate the available tools with `python list_tools.py` from inside the clone.

## What it does

Auto-generated MCP wrappers around RDKit modules — descriptors, fingerprints, reactions, substructure matching, conformer generation, and more. `settings.yaml` controls which RDKit surface is exposed.

**Primary use cases**: Agent-driven cheminformatics where Claude calls RDKit as tools (not code execution), molecule manipulation pipelines, retrosynthesis support.

## Notes

stdio transport. Differs from the K-Dense RDKit Skill: this exposes RDKit as discrete MCP tools (model calls them like any other function), while the skill instructs Claude to write and run Python locally. Pick the server if your environment forbids Bash/Python execution; pick the skill if it allows them and you want maximum flexibility.

## Sources

- [`tandemai-inc/rdkit-mcp-server`](https://github.com/tandemai-inc/rdkit-mcp-server)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=rdkit-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Frdkit-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
