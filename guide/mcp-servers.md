---
title: MCP servers
parent: Guide
nav_order: 3
---

# MCP servers

> External tools and data sources Claude can call, packaged behind the Model Context Protocol.

## What it is

An MCP server exposes tools, resources, and prompts over the Model Context Protocol so Claude can call them. The server runs as a local subprocess (stdio transport) or as a remote HTTP service (streamable HTTP transport). MCP is an open spec, so the same server works with Claude Code, Claude Desktop, the Claude.ai connector directory, and other MCP-aware clients.

You install one MCP server per data source — PubMed, ClinicalTrials.gov, your filesystem, your issue tracker — and Claude picks tools from it as needed.

## When to use it

- You need Claude to query a database or API (PubMed, ChEMBL, your internal services).
- You want Claude to read or write files on your machine.
- A vendor publishes a hosted MCP endpoint you want to point Claude at.
- You're building a shared team integration committed to a repo via `.mcp.json`.

## How to install / enable

Use `claude mcp add` from your shell. Flags go **before** the server name; `--` separates stdio commands.

```bash
# Remote HTTP server
claude mcp add --transport http pubmed https://pubmed.mcp.claude.com/mcp

# Local stdio server (default transport)
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/Documents

# Share with your team (commits .mcp.json at repo root)
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

Inside a session, run `/mcp` to see status and trigger OAuth login for servers that require it.

## Common pitfalls

- Putting flags after the server name — they're silently ignored.
- Forgetting `--` before the stdio command and its arguments.
- Committing `~/.claude.json` (it holds local-scope credentials). Use `--scope project` for `.mcp.json` instead.
- Using `--transport sse` — deprecated; use `--transport http`.
- Assuming static API keys work for remote MCP. Remote servers use OAuth 2.1; pass bearer tokens via `--header` when supported.
- Trying to expose an MCP server inside a private network. Don't poke firewall holes — request access to **MCP tunnels** (Research Preview, May 2026), which run a `cloudflared` agent outbound from your network. Console-managed only; not yet exposed as claude.ai connectors.

## See also

- [Plugins](plugins.md) — bundle an MCP server with skills and slash commands
- [Connectors](connectors.md) — Anthropic-managed remote MCP servers exposed in Claude.ai
- [Authentication](advanced/authentication.md)
- [MCP reference for Claude Code](https://code.claude.com/docs/en/mcp) — canonical docs
- [Model Context Protocol spec](https://modelcontextprotocol.io/)
- Catalog example: [PubMed MCP](../catalog/translational-medicine.md)

## Sources

- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) — Anthropic docs; verified 2026-05-19.
- [Model Context Protocol specification](https://modelcontextprotocol.io/) — verified 2026-05-19.
- [MCP donated to Linux Foundation Agentic AI Foundation](https://www.anthropic.com/news) — December 2025 announcement; verified 2026-05-19.
- [New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels](https://claude.com/blog/claude-managed-agents-updates) — Anthropic blog; published 2026-05-19 — MCP tunnels (Research Preview), `cloudflared`-based.
- [Anthropic Introduces MCP Tunnels for Private Agent Access to Internal Systems](https://www.infoq.com/news/2026/05/claude-mcp-tunnels/) — InfoQ; published 2026-05-19.
- [MCP tunnels (API docs)](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview) — Anthropic docs; verified 2026-05-20.
