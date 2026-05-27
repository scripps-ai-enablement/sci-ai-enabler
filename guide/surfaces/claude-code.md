---
title: Claude Code
parent: Claude surfaces
grand_parent: Guide
nav_order: 3
---

# Claude Code

> The agentic coding tool — a CLI you install locally, a redesigned desktop app, an IDE extension, and a browser interface at `claude.ai/code` that runs tasks on Anthropic-managed cloud VMs.

## What it is

Claude Code is where Claude takes multi-step actions against code: reading files, running commands, editing, running tests, opening PRs. It has four forms that share the same underlying engine.

- **CLI** — install on your machine, run `claude` in any repo, work in your terminal.
- **Desktop app** — redesigned 2026-04-14 around parallel sessions: a session sidebar across repos, drag-and-drop panes (terminal / preview / diff / chat), an in-app file editor and diff viewer, SSH on macOS (already supported on Linux), and one Git worktree per session.
- **IDE extension** — VS Code and JetBrains, surfacing the same engine in your editor.
- **Web** — `claude.ai/code` runs the agent in an Anthropic-managed cloud VM that clones your GitHub repo and opens PRs. Use `--teleport` from the CLI to hand off a cloud session into your terminal, or `claude --bg` to run a session in the background and reattach later via `/resume` or `claude agents` (a single-screen view of every running, blocked, and finished session; accepts `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--model`, `--effort`).

Claude Code is where Skills, MCP servers, Plugins, Hooks, and slash commands all install.

## When to use it

- Multi-step coding against files in a real repo.
- Anything you'd want to leave running unattended — long migrations, refactors, test runs.
- Async work via `claude.ai/code` — kick off jobs from the iOS app or web and check back later.
- Setting up [Routines](../advanced/routines.html) (`/schedule`) for recurring tasks.
- Letting Claude grind on a measurable goal across many turns — `/goal "<completion condition>"` (v2.1.139+, May 2026) keeps Claude working until a separate evaluator model confirms the condition holds (e.g., `npm test exits 0`).

## How to install / enable

- macOS/Linux: native installer.

  ```bash
  curl -fsSL https://claude.ai/install.sh | bash
  claude
  ```

- Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`, or `winget install Anthropic.ClaudeCode` (use `winget upgrade Anthropic.ClaudeCode` to bump an existing install).
- Homebrew: `brew install --cask claude-code` (stable) or `claude-code@latest` (newest).
- Linux distros: `apt`, `dnf`, `apk` packages also available.
- npm install (`npm install -g @anthropic-ai/claude-code`) still works but Anthropic now prints a yellow "npm installation is deprecated" banner. Use the native installer for new setups.
- Web: `https://claude.ai/code` (Pro, Max, Team, or premium Enterprise seats).

## Common pitfalls

- Claude Code on the web runs in a sandboxed VM with network restrictions; local-only MCP servers won't work there.
- Skills/plugins/MCP installed in `~/.claude/` (user scope) are global; `.claude/` in a repo (project scope) is per-repo.
- Background sessions accumulate — list with `claude agents` and clean up. Pin one with Ctrl+T in that view if you want it kept alive when idle and restarted in place on updates; un-pinned sessions are shed first under memory pressure.

## See also

- [Skills](../skills.html), [MCP servers](../mcp-servers.html), [Plugins](../plugins.html), [Marketplaces](../marketplaces.html)
- [Hooks](../advanced/hooks.html), [Slash commands and subagents](../advanced/slash-commands.html), [Routines](../advanced/routines.html), [Authentication](../advanced/authentication.html)

## Sources

- [Claude Code product landing](https://claude.com/product/claude-code) — Anthropic; verified 2026-05-27 (this run, via search summary) — canonical install command (`curl -fsSL https://claude.ai/install.sh | bash`) and OS-specific options, including `winget install Anthropic.ClaudeCode`.
- [Set up Claude Code](https://code.claude.com/docs/en/setup) — Anthropic docs; verified 2026-05-26 (this run).
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) — Anthropic docs; verified 2026-05-19.
- [Redesigning Claude Code on desktop for parallel agents](https://claude.com/blog/claude-code-desktop-redesign) — Anthropic blog; published 2026-04-14 — session sidebar, drag-and-drop panes, SSH on macOS, per-session Git worktrees.
- [Claude Code changelog (v2.1.139–v2.1.150)](https://code.claude.com/docs/en/changelog) — `claude agents` config flags, `/code-review` (renamed from `/simplify` in v2.1.147, 2026-05-21) with `--comment` for inline PR comments, `claude --bg`, `/resume`, Ctrl+T pinned background sessions, fast mode now Opus 4.7 by default, `/goal` introduced in v2.1.139 (2026-05-12); verified 2026-05-27 (this run).
- [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal) — Anthropic docs; verified 2026-05-27 (this run) — `/goal` completion-condition loop with separate evaluator model, 4,000-char limit, requires v2.1.139+.
- [Install Claude Code the Right Way in 2026](https://vanja.io/install-claude-code/) — secondary; npm-deprecation banner and native-installer migration path; verified 2026-05-25 (this run).
