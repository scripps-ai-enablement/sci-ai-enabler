---
title: DrugBank MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: openpharma-org (community)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Chemistry, Translational Medicine]
last_verified: 2026-07-26
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "openpharma-org/drugbank-mcp-server repo resolves (not archived, pushed 2026-05-07), no OSV advisories, but it is an unofficial community wrapper (not affiliated with DrugBank), GitHub license classifier is null, and it requires user-supplied license-gated DrugBank data"
summary: Community MCP server exposing a local DrugBank SQLite (17k+ drugs) with 16 query methods for repurposing, target lookup, interactions, and structural similarity.
---

# DrugBank MCP Server

Community MCP server that loads the DrugBank database into a local SQLite store and exposes 16 query methods for drug repurposing, drug-drug interactions, and structural similarity search.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [openpharma-org](https://github.com/openpharma-org/drugbank-mcp-server) (community, **unofficial**) |
| **Availability** | GA — stable single-commit release |
| **Pricing** | MIT-licensed server; **DrugBank data requires a separate user-supplied license** (academic or commercial) |
| **Capabilities** | Read-only — local SQLite over 17,430 drugs (small molecules plus biologics) |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — repo resolves, no OSV advisories, but unofficial community wrapper, license classifier null, license-gated DrugBank data |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/structural-biology-drug-discovery/drugbank-database-access` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
```
git clone https://github.com/openpharma-org/drugbank-mcp-server
cd drugbank-mcp-server
npm install
npm run download:db   # requires you to have obtained the DrugBank XML separately
npm run build
```

Then add to `claude_desktop_config.json` (replace `/path/to/drugbank-mcp-server` with the absolute path of your clone — e.g., `/Users/you/repos/drugbank-mcp-server`):

```json
{
  "mcpServers": {
    "drugbank": { "command": "node", "args": ["/path/to/drugbank-mcp-server/build/index.js"] }
  }
}
```

For Claude Code, the equivalent registration is:

```
claude mcp add --transport stdio drugbank -- node /path/to/drugbank-mcp-server/build/index.js
```

## What it does

16 query methods including:

- `search_by_name`, `get_drug_details`
- `search_by_indication`, `search_by_target`
- `get_drug_interactions`
- `search_by_atc_code`
- `get_pathways`
- `search_by_structure`, `get_similar_drugs`

**Primary use cases**: Drug repurposing by indication / target lookup, drug-drug interaction screening, structure / ATC similarity search.

## Notes

Unofficial — verify against DrugBank's current terms before use. The user must independently obtain the DrugBank XML (license-gated). Local stdio MCP; sub-10ms queries; ~50-100 MB RAM. DrugBank also ships an **official hosted MCP** ([go.drugbank.com/mcp](https://go.drugbank.com/mcp)) querying its curated knowledge graph directly, but it is gated behind a paid DrugBank OS account with MCP access enabled (contact your account manager); the community server above is the only free/self-hosted path.

## Sources

- [`openpharma-org/drugbank-mcp-server`](https://github.com/openpharma-org/drugbank-mcp-server)
- [DrugBank official MCP](https://go.drugbank.com/mcp)
- [LobeHub listing](https://lobehub.com/mcp/openpharma-org-drugbank-mcp-server)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=drugbank&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdrugbank.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
