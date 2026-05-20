# Guide changelog

A reverse-chronological log of guide updates produced by the guide curator agent. The newest entry is at the top.

<!-- Curator appends new dated entries directly below this line. -->

## 2026-05-20

### Updated
- **[connectors] Directory size and "Claude for Legal" launch** — bumped catalog estimate from "past 200" to "past 375" prebuilt integrations and called out the May 12 legal push (DocuSign, LexisNexis, Westlaw, Everlaw, iManage, Harvey, Ironclad, …) which added 20+ connectors and 12 practice-area plugins ([LawSites 2026-05-12](https://www.lawnext.com/2026/05/anthropic-goes-all-in-on-legal-releasing-more-than-20-connectors-and-12-practice-area-plugins-for-claude.html); awesome-claude-connectors enumerates ~398 entries as of 2026-05-15).
- **[plugins] Surfaced `claude-code-setup`** — added the official onboarding plugin as a recommended first install from `claude-plugins-official` (project-scanning helper that suggests hooks, skills, MCP servers, and subagents).
- **[mcp-servers] MCP tunnels (Research Preview)** — added a pitfall pointer for exposing MCP servers inside private networks, with the new `cloudflared`-based outbound-only tunnels announced 2026-05-19 at Code with Claude London ([Anthropic blog](https://claude.com/blog/claude-managed-agents-updates), [InfoQ 2026-05-19](https://www.infoq.com/news/2026/05/claude-mcp-tunnels/)).
- **[advanced/hooks] `terminalSequence` JSON field** — noted that any hook can now emit desktop notifications, set window titles, or ring the bell without a controlling terminal (May 2026 Claude Code changelog).

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`), Cowork, Claude Code on the web all still current per `claude.com/product/claude-code` and surrounding May 2026 coverage.
- skills.md — `~/.claude/skills/` layout and open-standard claim unchanged this run.
- marketplaces.md — source forms and seed-managed read-only behavior unchanged this run.
- advanced/slash-commands.md, advanced/authentication.md — unchanged this run.

### Flagged for review
- WebFetch was again unavailable this run (the model name it shells out to returns 404). All primary-source verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `claude.com/blog/claude-managed-agents-updates`, and `github.com/anthropics/claude-plugins-official`. A human should occasionally double-check the directory-size figure on `claude.ai/directory/connectors` directly, since the 375+ number is corroborated only by secondary commentary (Anthropic's directory page itself doesn't publish a count).

## 2026-05-19

### Updated
- **[claude-surfaces] Added Claude Cowork as a surface** — Cowork launched 2026-01-13 as the non-developer counterpart to Claude Code (sandboxed desktop agent for file/spreadsheet/slide work); expanded across paid plans by 2026-01-23 and gained department-specific plugins on 2026-02-24. Previously omitted ([source](https://www.infoq.com/news/2026/01/claude-cowork/), [Cowork plugins](https://claude.com/blog/cowork-plugins-across-enterprise)).
- **[skills] Open-standard adoption and Claude Code UX** — noted `SKILL.md` is now used by Codex CLI, Cursor, Gemini CLI, and GitHub Copilot, and `/skills` has type-to-filter search ([Claude Code changelog](https://code.claude.com/docs/en/changelog)).
- **[plugins] New install flags and dependency management** — documented `claude --plugin-dir <dir-or-zip>`, `claude --plugin-url`, dependency-aware `/plugin disable`, and `claude plugin prune` (May 2026 changelog).
- **[marketplaces] Seed-managed marketplaces and unified Directory pointer** — noted read-only seed marketplaces (containerized deployments) and the `claude.ai/directory` Plugins tab on the Claude.ai side, separate from the Claude Code marketplace mechanism.
- **[connectors] Unified Directory URL and 200+ catalog growth** — pointed canonical install path at `claude.ai/directory/connectors`; added everyday-life connectors (AllTrails, Uber, Spotify, …) per the May 2026 blog post.
- **[advanced/hooks] PostToolUse `updatedToolOutput` for all tools** — added the May 2026 generalization (previously MCP-only), the `Stop`-hook loop cap, and the `$CLAUDE_EFFORT` environment variable.
- **[decision-tree] Cowork row, current date** — added a row for non-coding desktop automation and replaced the "pending first guide run" date.

### Verified (no changes)
- mcp-servers.md — `claude mcp add --transport http` syntax and `--scope` semantics unchanged; sources re-verified.
- advanced/slash-commands.md — frontmatter and `.claude/agents/` schema unchanged this run.
- advanced/authentication.md — credential precedence and `claude setup-token` flow unchanged this run.

### Flagged for review
- WebFetch was unavailable this run (model error), so all primary-source verification went through WebSearch. Landing-page text (`claude.com/product/claude-code`) was last directly fetched on 2026-05-19 (previous run); install command is corroborated by multiple May 2026 secondary sources.

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

