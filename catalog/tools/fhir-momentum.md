---
title: Momentum FHIR MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Momentum
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-06-21
summary: MIT-licensed FHIR R4 MCP server with full CRUD, document ingestion/chunking, and Pinecone-backed semantic search over clinical records.
---

# Momentum FHIR MCP Server

Open-source MCP server that connects Claude to any HL7 FHIR R4 server, adding document ingestion and semantic search on top of full FHIR CRUD.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Momentum](https://github.com/the-momentum/fhir-mcp-server) (open source) |
| **Availability** | GA |
| **Pricing** | Free / OSS (MIT). A Pinecone account is needed for the semantic-search / document tools |
| **Capabilities** | Read/Write — full FHIR R4 CRUD plus document ingestion and vector search |

## How to install

Not published to PyPI — source install only. Clone, configure `.env`, and build with either Docker or `uv`:

```
git clone https://github.com/the-momentum/fhir-mcp-server
cd fhir-mcp-server
cp config/.env.example config/.env
make uv
```

(Edit `config/.env` to set your FHIR server base URL and, for the semantic-search tools, your Pinecone credentials.)

The server runs over stdio, so Claude launches the process itself — there is no long-lived service to keep running.

- **Claude Code** — register the `uv` launch command (replace `/path/to/fhir-mcp-server` with the absolute path of your clone — e.g., `$(pwd)` if you're still inside it from the clone step):

  ```
  claude mcp add --transport stdio fhir-momentum -- uv run --frozen --directory /path/to/fhir-mcp-server start
  ```

- **Claude Desktop** — add to `claude_desktop_config.json` (replace `<your-project-path>` with the absolute path of your clone, and `<uv-bin-folder-path>` with the directory containing the `uv` binary — find it with `dirname $(which uv)`):

  ```json
  {
    "mcpServers": {
      "fhir-momentum": {
        "command": "uv",
        "args": ["run", "--frozen", "--directory", "<your-project-path>", "start"],
        "env": { "PATH": "<uv-bin-folder-path>" }
      }
    }
  }
  ```

  A Docker launch is also documented upstream (`make build`, then a `docker run … mcp-server:latest` stdio entry) — see the README if you prefer containers. Restart Claude Desktop after editing the config.

## What it does

Exposes FHIR resource handlers plus document and terminology tools:

- **FHIR resources** — Patient, Observation, Condition, Medication, Immunization, Encounter, AllergyIntolerance, FamilyMemberHistory, and a generic resource handler, with full CRUD.
- **Document management** — DocumentReference handling, AI-powered ingestion and chunking of multiple formats, and Pinecone-backed semantic search over ingested clinical documents.
- **Terminology** — LOINC code retrieval.

**Primary use cases**: Natural-language search and retrieval over EHR/FHIR records, drafting and writing back FHIR resources, semantic search across clinical documents.

## Notes

Distinct from the [WSO2 FHIR MCP](fhir-wso2.html) (a CRUD bridge to any FHIR server) and the Anthropic [`fhir-developer`](fhir-developer.html) authoring plugin: Momentum adds document ingestion/chunking and Pinecone vector search, so it targets retrieval-augmented clinical workflows rather than bare resource CRUD. The semantic-search and document tools require Pinecone; the plain FHIR CRUD tools do not. stdio transport.

## Sources

- [`the-momentum/fhir-mcp-server`](https://github.com/the-momentum/fhir-mcp-server)
- [Momentum: Introducing the FHIR MCP Server](https://www.themomentum.ai/blog/introducing-fhir-mcp-server-natural-language-interface-for-healthcare-data)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=fhir-momentum&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ffhir-momentum.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
