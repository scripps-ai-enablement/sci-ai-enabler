---
title: Claude surfaces
parent: Guide
nav_order: 1
has_children: true
---

# Claude surfaces

> The places you can use Claude: Claude.ai, Claude Desktop, Claude Code (terminal, IDE, and web), Claude Cowork, and the Claude API.

## What it is

Ways to talk to the same Anthropic models. Each surface has different strengths and different component support. Pick the surface that matches your work, then read its sub-page for install and feature detail.

| Surface | Best for | Components supported |
|---|---|---|
| [Claude.ai](surfaces/claude-ai.html) | Chat, document upload, one-click Connectors | Connectors, Projects |
| [Claude Desktop](surfaces/claude-desktop.html) | The same chat plus local files via MCP | Connectors, MCP servers |
| [Claude Code](surfaces/claude-code.html) | Multi-step coding (CLI, IDE, web) | Skills, MCP servers, Plugins, Hooks, Routines |
| [Claude Cowork](surfaces/claude-cowork.html) | Non-coding desktop automation in a sandboxed VM | Connectors, Plugins |
| [Claude API](surfaces/claude-api.html) | Building your own product, agent, or backend | SDKs, Managed Agents, MCP |

Your account, Projects, and conversation history are shared across Claude.ai and Claude Desktop. Claude Code and Cowork are billed through your Pro/Max/Team/Enterprise subscription or via API.

## Cross-cutting features

Some features span more than one surface — you start them in one place and view or extend them in another. Read the linked page for detail.

- **[Routines](advanced/routines.html)** — scheduled remote Claude Code agents. Created via the `/schedule` skill in [Claude Code](surfaces/claude-code.html), viewed and edited at `claude.ai/code/routines` (a [Claude.ai](surfaces/claude-ai.html) surface), execute on Anthropic cloud infrastructure with MCP connectors attached.
- **Background sessions** — `claude --bg` starts a long-running Claude Code task; reattach later via `/resume` or `claude agents`. Spans CLI and `claude.ai/code`.
- **MCP tunnels (Research Preview)** — outbound-only `cloudflared` tunnels that expose private MCP servers to Claude.ai. Bridges Claude.ai / Claude Desktop and MCP servers running inside private networks. See [MCP servers](mcp-servers.html).

## Common pitfalls

- Confusing Claude Desktop, Claude Code, and Claude Cowork — three different apps that all live near `claude.ai`.
- Components don't all install everywhere. Skills, MCP servers, and Plugins work in Claude Code and Cowork; Connectors work in Claude.ai / Desktop / Cowork. A few tools (e.g., PubMed) ship in multiple places.
- API usage is metered separately from a Pro subscription.

## See also

- [Decision tree](decision-tree.html)
- [Skills](skills.html), [MCP servers](mcp-servers.html), [Plugins](plugins.html), [Connectors](connectors.html)
- [Claude Code overview](https://code.claude.com/docs/) — canonical docs
- [Claude.ai help center](https://support.claude.com/) — canonical docs

## Sources

- [Claude Code product landing](https://claude.com/product/claude-code) — Anthropic product page; verified 2026-05-21 (this run) — canonical install command and Windows/WinGet/Linux package options.
- [Set up Claude Code](https://code.claude.com/docs/en/setup) — Anthropic docs; verified 2026-05-21 (this run).
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) — Anthropic docs; verified 2026-05-19.
- [Claude Code on the web (announcement)](https://www.anthropic.com/news/claude-code-on-the-web) — published 2025-10-20.
- [Anthropic announces Claude Cowork](https://www.infoq.com/news/2026/01/claude-cowork/) — published 2026-01-13.
- [Cowork and plugins for teams across the enterprise](https://claude.com/blog/cowork-plugins-across-enterprise) — Anthropic blog; published 2026-02-24.
- [Claude Code changelog (v2.1.144 / v2.1.145, May 18–19 2026)](https://code.claude.com/docs/en/changelog) — `claude --bg`, `/resume`, `claude agents --json`; verified 2026-05-21 (this run).
