---
title: Claude Desktop
parent: Claude surfaces
grand_parent: Guide
nav_order: 2
---

# Claude Desktop

> The native macOS/Windows app — the same chat as Claude.ai, plus local MCP servers and file access.

## What it is

Claude Desktop is the native counterpart to `claude.ai`. It shares your account, Projects, and history, and renders the same chat interface. Its differentiator is **local MCP**: you can register MCP servers that run on your machine and expose local files, databases, or scripts to Claude. Connectors enabled in Claude.ai also work here.

Claude Cowork — the sandboxed desktop agent for non-coding work — runs **inside** Claude Desktop, but is a separate experience from the chat. See [Claude Cowork](claude-cowork.html).

## When to use it

- Same use cases as Claude.ai, but you want local files in the conversation.
- Adding [MCP servers](../mcp-servers.html) that need filesystem or local-process access.
- When you want both chat and Cowork in one place.

## How to install / enable

- Download from `https://claude.ai/download`.
- Sign in with the same account you use on Claude.ai.
- Add a local MCP server by editing the config file:
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

  ```json
  {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/folder"]
      }
    }
  }
  ```

  Restart the app after editing.

## Common pitfalls

- Don't confuse Claude Desktop with Claude Code. Desktop is for chat-style use with local context; Code is for terminal/IDE coding.
- Don't confuse Claude Desktop with Cowork. Cowork is a sandboxed agent that lives inside the Desktop app's sidebar but is enabled separately.
- MCP server config changes require an app restart.
- Local MCP servers run with your user's permissions — don't expose folders or scripts you wouldn't run by hand.

## See also

- [MCP servers](../mcp-servers.html) — the protocol behind local tool access.
- [Connectors](../connectors.html) — Anthropic-managed integrations that also work here.
- [Claude Cowork](claude-cowork.html) — the sandboxed agent that lives inside this app.

## Sources

- [Claude Desktop download page](https://claude.ai/download) — Anthropic; verified 2026-05-21 (this run).
- [Model Context Protocol introduction](https://modelcontextprotocol.io/introduction) — MCP spec; verified 2026-05-21.
- [Use Connectors to extend Claude's capabilities](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities) — Anthropic help center; verified 2026-05-21.
