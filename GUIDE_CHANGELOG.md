# Guide changelog

A reverse-chronological log of guide updates produced by the guide curator agent. The newest entry is at the top.

<!-- Curator appends new dated entries directly below this line. -->

## 2026-05-19

### Updated
- **[claude-surfaces] Re-verify install commands against product landing pages** — replaced the deprecated `npm install -g @anthropic-ai/claude-code` with the canonical native installer `curl -fsSL https://claude.ai/install.sh | bash`, added the Windows PowerShell variant `irm https://claude.ai/install.ps1 | iex` and Homebrew option, and added [`claude.com/product/claude-code`](https://claude.com/product/claude-code) and [`code.claude.com/docs/en/setup`](https://code.claude.com/docs/en/setup) to the Sources section. No other guide page contained the stale npm command.

## 2026-05-19

### Added
- **[all] Sources sections to all guide pages** — every topic page (claude-surfaces, skills, mcp-servers, plugins, marketplaces, connectors, hooks, slash-commands, authentication) now lists the dated URLs that ground its claims, per the per-page grounding rule introduced in `GUIDE_AGENT.md`.

### Updated
- **[claude-surfaces] Added Claude Code on the web** — `claude.ai/code` launched 2025-10-20 on Anthropic-managed cloud VMs; previously omitted. Reframed the surfaces list and added the `--teleport` hand-off note ([source](https://www.anthropic.com/news/claude-code-on-the-web)).
- **[plugins] Corrected install flow** — `claude-plugins-official` is pre-registered when Claude Code starts; reworked the example to install from it directly instead of `anthropics/claude-code` (the demo marketplace).
- **[marketplaces] Clarified pre-registered marketplace** — noted that `claude-plugins-official` ships pre-added; updated examples to install from `anthropics/life-sciences` and the community marketplace.

## 2026-05-19 (initial)

### Added
- **[claude-surfaces] First-run content** — beginner orientation across Claude.ai, Claude Desktop, Claude Code, and the Claude API ([source](https://code.claude.com/docs/)).
- **[skills] First-run content** — install paths under `~/.claude/skills/` and `.claude/skills/`, format pointers ([source](https://code.claude.com/docs/en/skills)).
- **[mcp-servers] First-run content** — canonical `claude mcp add` examples for HTTP and stdio transports, with scopes ([source](https://code.claude.com/docs/en/mcp)).
- **[plugins] First-run content** — `/plugin marketplace add` and `/plugin install <name>@<marketplace>` flow ([source](https://code.claude.com/docs/en/plugins)).
- **[marketplaces] First-run content** — supported source forms and the Anthropic life-sciences/cross-domain marketplaces ([source](https://code.claude.com/docs/en/discover-plugins)).
- **[connectors] First-run content** — Claude.ai Settings → Connectors flow, custom remote MCP connectors, Team/Enterprise admin path ([source](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)).
- **[advanced/hooks] First-run content** — `PreToolUse`/`PostToolUse` events, `.claude/settings.json` schema, exit-code-2 guardrail ([source](https://code.claude.com/docs/en/hooks)).
- **[advanced/slash-commands] First-run content** — `.claude/commands/` vs. `.claude/agents/`, convergence with Skills ([source](https://code.claude.com/docs/en/slash-commands)).
- **[advanced/authentication] First-run content** — Anthropic credential precedence, `claude setup-token`, MCP OAuth 2.1 ([source](https://code.claude.com/docs/en/authentication)).

