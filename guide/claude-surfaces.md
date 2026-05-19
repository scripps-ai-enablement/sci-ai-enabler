# Claude surfaces

> The four products that share the Claude name: Claude.ai, Claude Desktop, Claude Code, and the Claude API.

_Last updated: 2026-05-19_

## What it is

Four ways to talk to the same Anthropic models. **Claude.ai** is the web chat at `claude.ai`. **Claude Desktop** is the native macOS/Windows app — same chat, plus local MCP servers and Connectors. **Claude Code** is the agentic CLI (and an in-desktop GUI view) that edits files and runs commands in your terminal. **Claude API** is the developer endpoint you call from your own code.

Your account, Projects, and conversation history are shared across Claude.ai and Claude Desktop. Claude Code is billed either through your Pro/Max subscription or via API.

## When to use it

- **Claude.ai** — chat, document upload, one-click Connectors.
- **Claude Desktop** — the same chat plus local files via MCP and screen awareness.
- **Claude Code** — multi-step coding, editing files, running commands, scripted workflows.
- **Claude API** — building your own product, agent, or backend integration.

## How to install / enable

- Claude.ai: sign in at `https://claude.ai`.
- Claude Desktop: download from `https://claude.ai/download`.
- Claude Code: install the CLI, then sign in.

  ```bash
  npm install -g @anthropic-ai/claude-code
  claude
  ```

- Claude API: create a key at `https://console.anthropic.com` and call the REST endpoint or an Anthropic SDK.

## Common pitfalls

- Confusing Claude Desktop with Claude Code — they're different apps. The desktop app now embeds a Claude Code GUI view; the CLI is still its own binary.
- Components don't all install everywhere. Skills, MCP servers, and Plugins work in Claude Code; Connectors work in Claude.ai/Desktop. A few tools (e.g., PubMed) ship in both.
- API usage is metered separately from a Pro subscription.

## See also

- [Skills](skills.md), [MCP servers](mcp-servers.md), [Plugins](plugins.md), [Connectors](connectors.md)
- [Decision tree](decision-tree.md)
- [Claude Code overview](https://code.claude.com/docs/) — canonical docs
- [Claude.ai help center](https://support.claude.com/) — canonical docs
