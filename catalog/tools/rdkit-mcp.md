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

## How to install

```
git clone https://github.com/tandemai-inc/rdkit-mcp-server
cd rdkit-mcp-server
pip install -r requirements.txt
python run_server.py --settings settings.yaml
```

Register with Claude Desktop via a standard `claude_desktop_config.json` stdio entry pointing at `run_server.py`. Enumerate available tools with `python list_tools.py`.

## What it does

Auto-generated MCP wrappers around RDKit modules — descriptors, fingerprints, reactions, substructure matching, conformer generation, and more. `settings.yaml` controls which RDKit surface is exposed.

**Primary use cases**: Agent-driven cheminformatics where Claude calls RDKit as tools (not code execution), molecule manipulation pipelines, retrosynthesis support.

## Notes

stdio transport. Differs from the K-Dense RDKit Skill: this exposes RDKit as discrete MCP tools (model calls them like any other function), while the skill instructs Claude to write and run Python locally. Pick the server if your environment forbids Bash/Python execution; pick the skill if it allows them and you want maximum flexibility.

## Sources

- [`tandemai-inc/rdkit-mcp-server`](https://github.com/tandemai-inc/rdkit-mcp-server)
