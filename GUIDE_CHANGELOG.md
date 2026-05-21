---
title: Guide updates
parent: Updates
nav_order: 2
permalink: /updates/guide.html
---

# Guide updates

Reverse-chronological log of changes to the [guide](guide/). Newest at the top.

<!-- Curator appends new dated entries directly below this line. -->

## 2026-05-21

### Added
- **[surfaces/*, advanced/routines] Surfaces section now has one sub-page per surface, and routines is documented as a cross-cutting feature.** Restructured `guide/claude-surfaces.md` into a thin parent index (`has_children: true`) with a comparison table, and added `guide/surfaces/{claude-ai, claude-desktop, claude-code, claude-cowork, claude-api}.md` for surface-specific install and feature detail. Added `guide/advanced/routines.md` covering scheduled remote Claude Code agents (created via `/schedule`, viewed at `claude.ai/code/routines`, cron in UTC with 1-hour minimum, MCP-connector-aware, fully isolated per firing). The routines page is cross-linked from the Claude Code and Claude.ai sub-pages — first formal example of the "cross-cutting features" pattern described in GUIDE_AGENT.md.
- **[GUIDE_AGENT] "Cross-cutting features" section and ongoing-discovery directive.** Curator now maintains a single page per cross-cutting feature in `guide/advanced/` and cross-links from each relevant surface sub-page; on every run, scans Anthropic news / Claude Code changelog / named secondary commentary for newly-shipped cross-surface features (routines, background sessions, MCP tunnels, Cowork plugins, `--teleport`) that beginners would otherwise miss, and adds them. Topics table updated to include the five surface sub-pages and `advanced/routines.md`. Page schema updated with `parent: Claude surfaces` / `grand_parent: Guide` convention for surface sub-pages.

### Updated
- **[claude-surfaces] Expanded install methods and added background-session note** — `claude.com/product/claude-code` now documents `winget upgrade Anthropic.ClaudeCode`, Homebrew `claude-code@latest` for the latest channel, and `apt`/`dnf`/`apk` packages alongside the canonical `curl …/install.sh`. Removed "npm is deprecated" wording since the npm package now wraps the same native binary. Added `claude --bg` / `/resume` / `claude agents` for background sessions per the May 18–19 changelog (v2.1.144–v2.1.145). Then refactored this page into a parent index (see Added).
- **[guide/README] Surfaces now has sub-pages; advanced section now mentions routines** — added the Cowork surface to the top-line description, noted that each surface has its own sub-page with install and feature detail, and added routines to the advanced one-liner.
- **[advanced/README] Routines added to the advanced index.**
- **[plugins] `/plugin` Discover/Browse component previews and Claude for Small Business example** — noted that the Discover and Browse panes now preview a plugin's commands/agents/skills/hooks/MCP/LSP servers before install (May 2026 changelog), and added Claude for Small Business (2026-05-13) as the canonical example of a single-toggle Cowork plugin bundling connectors + workflows.
- **[connectors] Corrected directory size estimate** — replaced "past 375" with Anthropic's own most-recent count of "over 200" since July 2025 launch (per `claude.com/blog/connectors-for-everyday-life`); the 375 figure was sourced from secondary commentary only. Kept the May 12 legal push (20+ connectors, 12 practice-area plugins). Added a pitfall pointer to the Claude for Small Business Cowork bundle for users hunting SMB connectors.

### Verified (no changes)
- skills.md — `~/.claude/skills/` layout, open-standard claim, `/skills` picker unchanged this run.
- mcp-servers.md — `claude mcp add --transport http` syntax, MCP tunnels (Research Preview), and `--scope` semantics unchanged.
- marketplaces.md — source forms and seed-managed read-only behavior unchanged.
- decision-tree.md — table unchanged; Cowork row covers the SMB scenario adequately at this granularity.
- advanced/hooks.md, advanced/slash-commands.md, advanced/authentication.md — unchanged this run.

### Flagged for review
- WebFetch remained unavailable (model 404 for `claude-3-5-haiku-20241022`) — all source verification this run went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `claude.com/blog/connectors-for-everyday-life`, `anthropic.com/news/claude-for-small-business`, and `github.com/anthropics/claude-plugins-official`. A human should occasionally check the actual connector count on `claude.ai/directory/connectors`; Anthropic's blog says "over 200" but third-party trackers list far more.
- **New surface sub-pages and `advanced/routines.md` were drafted in-session without a fresh per-page source fetch.** The content draws on existing claude-surfaces.md (already source-grounded), direct observation of the Anthropic routines API in this session (the `claude.ai/code/routines/<id>` URL and create-body shape were returned live by `RemoteTrigger`), and the curator's prior research. Each new page lists candidate sources, but the next scheduled run should fetch them per `GUIDE_AGENT.md`'s per-page grounding rule and tighten any claim that doesn't survive verification. Specific items to re-verify on the next run: (1) the exact local-MCP config path on Windows for Claude Desktop, (2) current Anthropic SDK install commands and example, (3) presence and naming of an Anthropic-published "routines" or "managed agents" doc page suitable as a primary source.

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

