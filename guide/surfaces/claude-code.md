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
- **Web** — `claude.ai/code` runs the agent in an Anthropic-managed cloud VM that clones your GitHub repo and opens PRs. Use `--teleport` from the CLI to hand off a cloud session into your terminal, or `claude --bg` to run a session in the background and reattach later via `/resume` or `claude agents` (a single-screen view of every running, blocked, and finished session).

Claude Code is where Skills, MCP servers, Plugins, Hooks, and slash commands all install.

## When to use it

- Multi-step coding against files in a real repo.
- Anything you'd want to leave running unattended — long migrations, refactors, test runs.
- Async work via `claude.ai/code` — kick off jobs from the iOS app or web and check back later.
- Setting up [Routines](../advanced/routines.html) (`/schedule`) for recurring tasks.

## How to install / enable

- macOS/Linux: native installer.

  ```bash
  curl -fsSL https://claude.ai/install.sh | bash
  claude
  ```

- Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`, or `winget upgrade Anthropic.ClaudeCode`.
- Homebrew: `brew install --cask claude-code` (stable) or `claude-code@latest` (newest).
- Linux distros: `apt`, `dnf`, `apk` packages also available.
- npm package still works and wraps the same native binary.
- Web: `https://claude.ai/code` (Pro, Max, Team, or premium Enterprise seats).

## Common pitfalls

- Claude Code on the web runs in a sandboxed VM with network restrictions; local-only MCP servers won't work there.
- Skills/plugins/MCP installed in `~/.claude/` (user scope) are global; `.claude/` in a repo (project scope) is per-repo.
- Background sessions accumulate — list with `claude agents` and clean up.

## See also

- [Skills](../skills.html), [MCP servers](../mcp-servers.html), [Plugins](../plugins.html), [Marketplaces](../marketplaces.html)
- [Hooks](../advanced/hooks.html), [Slash commands and subagents](../advanced/slash-commands.html), [Routines](../advanced/routines.html), [Authentication](../advanced/authentication.html)

## Sources

- [Claude Code product landing](https://claude.com/product/claude-code) — Anthropic; verified 2026-05-22 (this run) — canonical install command and OS-specific options.
- [Set up Claude Code](https://code.claude.com/docs/en/setup) — Anthropic docs; verified 2026-05-22.
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) — Anthropic docs; verified 2026-05-19.
- [Redesigning Claude Code on desktop for parallel agents](https://claude.com/blog/claude-code-desktop-redesign) — Anthropic blog; published 2026-04-14 — session sidebar, drag-and-drop panes, SSH on macOS, per-session Git worktrees.
- [Claude Code changelog (v2.1.139–v2.1.146)](https://code.claude.com/docs/en/changelog) — `claude agents`, `/goal`, `/code-review` (renamed from `/simplify`), `claude --bg`, `/resume`; verified 2026-05-22.
