---
title: NCBI GEO
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent / MCPmed
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-27
summary: "NCBI GEO access — keyword/series search, GSE matrices, GPL/GSM metadata — as a SciAgent skill or the MCPmed GEO MCP server."
---

# NCBI GEO

NCBI Gene Expression Omnibus access — search series/samples/platforms, download expression matrices, and parse annotations — available as a SciAgent Claude Skill or the MCPmed `geo-mcp` MCP server.

| | |
|---|---|
| **Type** | Claude Skill · MCP server |
| **Supplier** | [jaechang-hits / SciAgent](https://github.com/jaechang-hits/SciAgent-Skills) (skill) · [MCPmed](https://github.com/MCPmed/GEOmcp) (MCP) |
| **Availability** | GA |
| **Pricing** | Free / OSS — skill MIT; `geo-mcp` BSD-3-Clause |
| **Capabilities** | Read/Write — skill runs Python locally (Bash); MCP exposes GEO search/download tools over stdio or HTTP |

## How to install

### Option A — MCPmed GEO MCP server (`geo-mcp`)

First-class MCP server (BSD-3-Clause) over the NCBI E-utilities GEO endpoints.

- **Install:**
  ```
  pip install geo-mcp
  ```
- **Claude Code** — register the stdio server:
  ```
  which geo-mcp   # note the absolute path printed
  claude mcp add geo-mcp /path/to/geo-mcp
  ```
  (replace `/path/to/geo-mcp` with the absolute path that `which geo-mcp` printed — e.g. `/Users/you/.local/bin/geo-mcp`.) NCBI requires an email; set `GEOMCP_EMAIL` (and optionally `GEOMCP_API_KEY` for higher rate limits) in the environment, or run `geo-mcp --init` once to write a config file.
- **Claude Desktop** — in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "geo-mcp": {
        "command": "/path/to/geo-mcp",
        "env": { "GEOMCP_EMAIL": "you@example.org" }
      }
    }
  }
  ```
  Fully quit and relaunch Claude Desktop after editing. This is a long-lived stdio server launched by Claude itself — do not run `geo-mcp` separately (running it once in a terminal only verifies it boots; Ctrl-C after).

MCP tools: `search_geo`, `search_geo_profiles`, `search_geo_datasets`, `search_geo_series`, `search_geo_samples`, `search_geo_platforms`, `download_geo_data`.

### Option B — SciAgent NCBI GEO skill

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/genomics-bioinformatics/databases/geo-database ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

NCBI GEO access via GEOparse and E-utilities. Search by keyword/organism/platform, download GSE series matrices, parse GPL annotations, extract GSM metadata, load expression matrices into pandas. For single-cell use cellxgene-census; for multi-DB access use gget-genomic-databases.

**Primary use cases**: NCBI GEO access via GEOparse and E-utilities.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/genomics-bioinformatics/databases/geo-database`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/genomics-bioinformatics/databases/geo-database/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/genomics-bioinformatics/databases/geo-database/SKILL.md)
- [`MCPmed/GEOmcp`](https://github.com/MCPmed/GEOmcp) (`geo-mcp` MCP server, BSD-3-Clause)
- [MCPmed (Briefings in Bioinformatics 2026, bbag076)](https://academic.oup.com/bib/article/27/1/bbag076/8495038)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=geo-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fgeo-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
