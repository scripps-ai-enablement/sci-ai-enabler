---
title: PDBe MCP Servers
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: PDBe (EMBL-EBI)
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Drug Repurposing and Discovery]
last_verified: 2026-07-04
claude_science: true
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches PDBeurope/pdbe-mcp-servers Apache-2.0 + PyPI pdbe-mcp-server 1.1.5, read-only API/Search servers keyless"
summary: First-party PDBe Europe MCP servers giving Claude access to protein structure data via REST API, Solr search, and an optional Neo4j graph.
---

# PDBe MCP Servers

First-party MCP servers from the Protein Data Bank in Europe (PDBe) that let Claude query structural data through the PDBe REST API, run advanced Solr searches, and optionally traverse the PDBe knowledge graph.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [PDBe (EMBL-EBI)](https://github.com/PDBeurope/pdbe-mcp-servers) |
| **Availability** | GA — `pdbe-mcp-server` on PyPI (v1.1.4, 2026-06-15) |
| **Pricing** | Free / OSS (Apache-2.0) |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches PDBe EMBL-EBI, Apache-2.0, keyless read-only |

## How to install

The package ships three servers selected by a `--server-type` flag. The **API** and **Search** servers need no accounts, API keys, or extra infrastructure; the **Graph** server additionally requires a self-hosted Neo4j instance.

**Prerequisite**: `uvx` requires [uv](https://docs.astral.sh/uv/) installed — `pip install uv` or the official installer.

- **Claude Code** — direct MCP add over stdio (Claude launches the process itself via `uvx`; no separate terminal needed):
  ```
  claude mcp add --transport stdio pdbe-api -- uvx pdbe-mcp-server --server-type pdbe_api_server
  claude mcp add --transport stdio pdbe-search -- uvx pdbe-mcp-server --server-type pdbe_search_server
  ```
- **Claude Desktop** — add the equivalent stdio entries to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "PDBe API Server": {
        "command": "uvx",
        "args": ["pdbe-mcp-server", "--server-type", "pdbe_api_server"]
      },
      "PDBe Search Server": {
        "command": "uvx",
        "args": ["pdbe-mcp-server", "--server-type", "pdbe_search_server"]
      }
    }
  }
  ```
- **Graph server (optional, requires Neo4j)** — set `NEO4J_URL`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD` for a running Neo4j instance, then register:
  ```
  claude mcp add --transport stdio pdbe-graph --env NEO4J_URL=bolt://localhost:7687 --env NEO4J_USERNAME=neo4j --env NEO4J_PASSWORD=<your-password> -- uvx pdbe-mcp-server --server-type pdbe_graph_server
  ```
  (Replace `<your-password>` with your Neo4j password. PDBe does not host a public graph endpoint, so the Graph server is only useful if you stand up your own Neo4j mirror of the PDBe graph.)

To confirm a server boots before registering, run the `uvx …` command directly and Ctrl-C after it starts — Claude Code/Desktop will launch the process on demand via stdio, so you do not keep it running in a separate terminal.

## What it does

Three complementary servers over PDBe resources:

- **PDBe API Server** (`pdbe_api_server`) — tools auto-generated from the PDBe REST API OpenAPI spec: entries, assemblies, molecules, ligands, publications, and structure validation data.
- **PDBe Search Server** (`pdbe_search_server`) — `get_pdbe_search_schema` and `run_pdbe_search_query` for advanced Solr-based faceted searches across structural data.
- **PDBe Graph Server** (`pdbe_graph_server`) — `pdbe_graph_nodes`, `pdbe_graph_edges`, `pdbe_graph_node_relationships`, `pdbe_graph_example_queries`, and `pdbe_run_cypher_query` for exploring the PDBe knowledge-graph schema and running Cypher queries (against a local Neo4j).

**Primary use cases**: Retrieve PDBe structure metadata and validation into Claude workflows, run faceted Solr queries over the archive, explore structural relationships via the PDBe graph.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Structures & Interactions* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Apache-2.0. The API and Search servers are keyless and run out of the box; the Graph server needs a self-hosted Neo4j (PDBe does not expose a public graph endpoint), so most users should start with the API and Search servers. All servers are read-only. This is a **PDBe Europe** resource (EMBL-EBI), distinct from the RCSB-focused servers on the [PDB MCP Server](pdb.html) page — PDBe and RCSB are separate wwPDB partner sites with different APIs, search backends, and graph infrastructure; catalogued separately as one entry per data source.

## Sources

- [`PDBeurope/pdbe-mcp-servers`](https://github.com/PDBeurope/pdbe-mcp-servers)
- [PyPI: `pdbe-mcp-server`](https://pypi.org/project/pdbe-mcp-server/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pdbe&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpdbe.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
