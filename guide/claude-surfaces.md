# Claude surfaces

> The places you can use Claude: Claude.ai, Claude Desktop, Claude Code (terminal, IDE, and web), Claude Cowork, and the Claude API.

_Last updated: 2026-05-19_

## What it is

Ways to talk to the same Anthropic models. **Claude.ai** is the web chat at `claude.ai`. **Claude Desktop** is the native macOS/Windows app — same chat, plus local MCP servers and Connectors. **Claude Code** is the agentic coding tool: a CLI you install locally, an IDE extension, and a browser interface at `claude.ai/code` that runs tasks on Anthropic-managed cloud VMs. **Claude Cowork** is the non-developer counterpart to Claude Code: a sandboxed desktop agent for file-heavy work, available inside the Claude desktop app. **Claude API** is the developer endpoint you call from your own code.

Your account, Projects, and conversation history are shared across Claude.ai and Claude Desktop. Claude Code and Cowork are billed through your Pro/Max/Team/Enterprise subscription or via API.

## When to use it

- **Claude.ai** — chat, document upload, one-click Connectors.
- **Claude Desktop** — the same chat plus local files via MCP.
- **Claude Code (CLI / IDE)** — multi-step coding against files on your machine.
- **Claude Code on the web** (`claude.ai/code`) — async coding agents that clone your GitHub repo into an Anthropic-managed VM and open PRs; monitor from the Claude iOS app.
- **Claude Cowork** — non-coding desktop automation (file wrangling, spreadsheets, slide decks); runs in a sandboxed VM with permission-gated access to local folders.
- **Claude API** — building your own product, agent, or backend integration.

## How to install / enable

- Claude.ai: sign in at `https://claude.ai`.
- Claude Desktop: download from `https://claude.ai/download`.
- Claude Code CLI: install with the native installer, then sign in. (npm is deprecated.)

  ```bash
  curl -fsSL https://claude.ai/install.sh | bash
  claude
  ```

  Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`. Homebrew: `brew install --cask claude-code`.

- Claude Code on the web: go to `https://claude.ai/code` and sign in (Pro, Max, Team, or premium Enterprise seats). Use `--teleport` from the CLI to pull a cloud session into your terminal.
- Claude Cowork: open the Claude desktop app on macOS (Windows in preview) and enable Cowork from the sidebar. Available on all paid plans.
- Claude API: create a key at `https://console.anthropic.com` and call the REST endpoint or an Anthropic SDK.

## Common pitfalls

- Confusing Claude Desktop, Claude Code, and Claude Cowork — three different apps that all live near `claude.ai`.
- Components don't all install everywhere. Skills, MCP servers, and Plugins work in Claude Code and Cowork; Connectors work in Claude.ai / Desktop / Cowork. A few tools (e.g., PubMed) ship in multiple places.
- Claude Code on the web runs in a sandboxed VM with network restrictions; local-only tools won't work there.
- API usage is metered separately from a Pro subscription.

## See also

- [Skills](skills.md), [MCP servers](mcp-servers.md), [Plugins](plugins.md), [Connectors](connectors.md)
- [Decision tree](decision-tree.md)
- [Claude Code overview](https://code.claude.com/docs/) — canonical docs
- [Claude.ai help center](https://support.claude.com/) — canonical docs

## Sources

- [Claude Code product landing](https://claude.com/product/claude-code) — Anthropic product page; verified 2026-05-19 (this run) — canonical install command.
- [Set up Claude Code](https://code.claude.com/docs/en/setup) — Anthropic docs; verified 2026-05-19 (this run) — confirms native installer is recommended, npm is deprecated.
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) — Anthropic docs; verified 2026-05-19 (this run).
- [Claude Code on the web (announcement)](https://www.anthropic.com/news/claude-code-on-the-web) — published 2025-10-20.
- [Anthropic announces Claude Cowork](https://www.infoq.com/news/2026/01/claude-cowork/) — published 2026-01-13; covers Cowork's launch as the non-developer counterpart to Claude Code.
- [Cowork and plugins for teams across the enterprise](https://claude.com/blog/cowork-plugins-across-enterprise) — Anthropic blog; published 2026-02-24.
- [Claude Code overview](https://code.claude.com/docs/en/overview) — Anthropic docs; verified 2026-05-19.
