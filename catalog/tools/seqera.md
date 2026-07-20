---
title: Seqera MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Seqera Labs
availability: GA
tool_categories: [Molecular and Cellular Biology, Immunology and Microbiology, Integrative Structural and Computational Biology]
last_verified: 2026-07-04
verification: works
verified_on: 2026-07-20
verification_note: "official Seqera docs confirm the hosted endpoint mcp.seqera.io/mcp as current; functional connect is OAuth/account-gated so verified via primary-source docs not a live tool call"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier Seqera Labs (official docs.seqera.io documents the endpoint), hosted vendor service; write-capable (launches compute) so treat runs as cost-incurring"
summary: Hosted MCP server for launching and managing Nextflow/nf-core pipelines on the Seqera Platform and retrieving public SRA/ENA/GEO sequencing data.
---

# Seqera MCP

Official hosted MCP server from Seqera Labs (the team behind Nextflow) that lets Claude launch and manage Nextflow pipelines, search nf-core modules, and pull public sequencing data — all from natural language.

| | |
|---|---|
| **Type** | MCP server (hosted, HTTP) |
| **Supplier** | [Seqera Labs](https://seqera.io/) |
| **Availability** | GA — endpoint live at `https://mcp.seqera.io/mcp` |
| **Pricing** | Free / OSS client access; a Seqera Platform account is required (Seqera has a free Cloud/Community tier; paid Pro/Enterprise tiers for larger compute) |
| **Capabilities** | Read/Write — launches and manages compute workflows on your Seqera account |
| **Verified** | works · 2026-07-20 — official docs confirm mcp.seqera.io/mcp endpoint (OAuth-gated) |
| **Security** | cleared · 2026-07-20 — provenance matches Seqera Labs official docs, hosted vendor service, write-capable |

## How to install

- **Claude Code** — direct MCP add (HTTP transport; OAuth login opens in your browser on first connect):
  ```
  claude mcp add --scope=user --transport=http seqera https://mcp.seqera.io/mcp
  ```
  This is a hosted HTTP server — you do **not** run any local process. Claude Code connects to the remote endpoint directly. On first use a browser window opens for the Seqera OAuth 2.1 login.

- **Claude Desktop** — Claude Desktop has no native remote-HTTP transport, so add it as a custom connector: **Settings → Connectors → Add custom connector**, enter URL `https://mcp.seqera.io/mcp`, and select **OAuth** as the authentication method. (If your Desktop build lacks the custom-connector UI, register a proxy stdio entry with `mcp-remote` instead: add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "seqera": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://mcp.seqera.io/mcp"]
      }
    }
  }
  ```
  )

- **Alternative auth (clients without OAuth)** — use a Seqera Platform Personal Access Token as a Bearer token instead of the interactive OAuth flow. Generate the token in the Seqera Platform UI (**Your tokens**), then pass it via the `--header` flag:
  ```
  claude mcp add --scope=user --transport=http seqera https://mcp.seqera.io/mcp --header "Authorization: Bearer <YOUR_SEQERA_TOKEN>"
  ```
  (replace `<YOUR_SEQERA_TOKEN>` with the personal access token from your Seqera Platform account.)

## What it does

Three tool groups:

- **Seqera Platform tools** — launch, monitor, and manage Nextflow pipeline runs; create/inspect compute environments; provision containers via Wave.
- **nf-core tools** — search the nf-core module library (1000+ standardized bioinformatics modules) and get analysis recommendations.
- **SRA tools** — search and retrieve public sequencing data from NCBI SRA, EBI ENA, and GEO.

**Primary use cases**: Natural-language launching of nf-core pipelines (rnaseq, sarek, atacseq, etc.), managing Seqera compute environments, discovering public sequencing datasets to feed into a workflow.

## Notes

Requires a Seqera Platform account. Because the server can launch compute workflows, treat it as a write-capable tool — pipeline runs may incur compute costs on your configured environment. Complements the `nextflow-development` skill (`anthropics/life-sciences`): that skill teaches Claude how to author and run nf-core pipelines locally, while this MCP drives runs and data retrieval through the hosted Seqera Platform.

The third-party Composio "Tool Router" integration exposes the same toolkit via a Composio-generated URL and an `X-API-Key` header; the official `https://mcp.seqera.io/mcp` endpoint above is the direct route and is preferred.

## Sources

- [Seqera MCP overview (official docs)](https://docs.seqera.io/platform-cloud/seqera-mcp/overview)
- [Seqera MCP integration with Claude Code (Composio)](https://composio.dev/toolkits/seqera/framework/claude-code)
- [Seqera Labs](https://seqera.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=seqera&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fseqera.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
