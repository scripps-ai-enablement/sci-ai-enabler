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
- **Web** — `claude.ai/code` runs the agent in an Anthropic-managed cloud VM that clones your repo and opens PRs. Use `--teleport` from the CLI to hand off a cloud session into your terminal, or `claude --bg` to run a session in the background and reattach later via `/resume` or `claude agents` (a single-screen view of every running, blocked, and finished session; accepts `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--model`, `--effort`). Inside `claude agents`, prefix any shell command with `!` to spin it up as a detachable background job — equivalent to `claude --bg --exec '<command>'` from your shell. `--worktree` and the `claude agents` view now also recognize GitLab merge requests (shown as `!N`), alongside GitHub PRs (v2.1.233, 2026-08-14). Run `/fork` (v2.1.212, 2026-07-17) to copy your current conversation into its own background-session row and keep working in the original. Background sessions on different machines can message each other with `SendMessage` and discover each other with `ListAgents` (macOS/Linux, v2.1.224, 2026-08-07); type `@` plus a session name in any prompt to message one directly, and manage inbound requests from `/config` (v2.1.232, 2026-08-13). Team/Enterprise can also run `claude self-hosted-runner` to host web/mobile/desktop sessions on their own machines instead of Anthropic's cloud VMs (v2.1.224).

**Claude in Chrome** (browser extension, generally available 2026-07-01) pairs with Claude Code for a build-test-verify loop: build in your terminal, then have Claude drive the browser to test. All paid plans; Pro is limited to Haiku 4.5. Not a Claude Code form itself, but it interoperates with one.

The Desktop app form also has two features shared with Claude Cowork: toggle **computer use** (Settings → General) to let Claude click and type directly on your screen when no connector covers a task, and pair the mobile app with a Desktop session via **Dispatch** to hand off a task from your phone. Both are Research Preview, Pro/Max only. See [cross-cutting features](../claude-surfaces.html#cross-cutting-features).

Claude Code is where Skills, MCP servers, Plugins, Hooks, and slash commands all install.

## When to use it

- Multi-step coding against files in a real repo.
- Anything you'd want to leave running unattended — long migrations, refactors, test runs.
- Async work via `claude.ai/code` — kick off jobs from the iOS app or web and check back later.
- Setting up [Routines](../advanced/routines.html) (`/schedule`) for recurring tasks.
- Letting Claude grind on a measurable goal across many turns — `/goal "<completion condition>"` (v2.1.139+, May 2026) keeps Claude working until a separate evaluator model confirms the condition holds (e.g., `npm test exits 0`).
- Tackling a migration or audit too large for one session — include the keyword `ultracode` in your prompt (renamed from `workflow` in v2.1.160 — the bare word `workflow` no longer fires), or set `/effort ultracode` to auto-orchestrate the whole session, to fan the job out across up to 1,000 parallel subagents (research preview, requires v2.1.154+; see [Dynamic Workflows](../claude-surfaces.html#cross-cutting-features) on the surfaces page).
- Reviewing a GitHub PR without installing the GitHub App. From a checked-out PR branch, run `/code-review` to print findings in the terminal, `/code-review --comment` to post them as inline PR comments (≥ 80-confidence, deduped), or `/code-review --fix` to apply them to the working tree. Originally absorbed `/simplify` in v2.1.146 (2026-05-21); since v2.1.154 (2026-05-28), `/simplify` is back as a separate **cleanup-only** review (reuse, simplification, efficiency, altitude — no bug-hunting). If you want bug-hunting plus apply-fixes, use `/code-review --fix`.

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
- Pick a model with `/model` (or `--model` at launch). **Claude Opus 5 is the default** as of v2.1.219 (2026-07-24) — a step-change agentic-coding model with a 1M-token context window, priced identically to Opus 4.8 ($5 / $25 per million tokens). Sonnet 5 (cheaper, also 1M context) and Opus 4.8 remain selectable; a request that trips a safety classifier falls back to Opus 4.8 automatically. **Claude Fable 5** is available again after its export-control suspension was lifted (redeployed globally 2026-07-01), so it appears in the picker for all users. (Mythos 5 is restricted to approved U.S. organizations.)

## Common pitfalls

- Claude Code on the web runs in a sandboxed VM with network restrictions; local-only MCP servers won't work there.
- Skills/plugins/MCP installed in `~/.claude/` (user scope) are global; `.claude/` in a repo (project scope) is per-repo.
- Background sessions accumulate — list with `claude agents` and clean up. Pin one with Ctrl+T in that view if you want it kept alive when idle and restarted in place on updates; un-pinned sessions are shed first under memory pressure.
- **The planned Agent SDK billing split was paused.** Anthropic had announced that `claude -p` (headless mode), Claude Code GitHub Actions, and any third-party harness using the Agent SDK would move to a separate credit pool on 2026-06-15. On that date Anthropic shelved the change: for now, `claude -p` and the Agent SDK still draw from your normal subscription, same as interactive `claude` in the terminal. Anthropic says it will give notice before any future change. See [Claude API](claude-api.html).

## See also

- [Skills](../skills.html), [MCP servers](../mcp-servers.html), [Plugins](../plugins.html), [Marketplaces](../marketplaces.html)
- [Hooks](../advanced/hooks.html), [Slash commands and subagents](../advanced/slash-commands.html), [Routines](../advanced/routines.html), [Authentication](../advanced/authentication.html)

## Sources

- [Claude Code product landing](https://claude.com/product/claude-code) — Anthropic; verified 2026-05-29 (this run, via search summary) — canonical install command (`curl -fsSL https://claude.ai/install.sh | bash`) and OS-specific options, including `winget install Anthropic.ClaudeCode`.
- [Set up Claude Code](https://code.claude.com/docs/en/setup) — Anthropic docs; verified 2026-05-26 (this run).
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) — Anthropic docs; verified 2026-05-19.
- [Redesigning Claude Code on desktop for parallel agents](https://claude.com/blog/claude-code-desktop-redesign) — Anthropic blog; published 2026-04-14 — session sidebar, drag-and-drop panes, SSH on macOS, per-session Git worktrees.
- [Claude Code changelog (v2.1.139–v2.1.162)](https://code.claude.com/docs/en/changelog) — `claude agents` config flags, `/code-review` (absorbed `/simplify` in v2.1.146 on 2026-05-21; gained `--fix` in v2.1.152 on 2026-05-27; gained `--comment` for inline PR comments in v2.1.161, 2026-06-02). In v2.1.154 (2026-05-28) `/simplify` returned as a distinct cleanup-only command (reuse / simplification / efficiency / altitude — no bug-hunting), so it is no longer an alias for `/code-review --fix`. Also: `claude --bg`, `claude --bg --exec '<command>'`, and the `!` prefix inside `claude agents` to spin background jobs; `/resume` (also covers background sessions as of v2.1.161); Ctrl+T pinned background sessions; `/goal` (v2.1.139, 2026-05-12); `/reload-skills` + `disallowed-tools` frontmatter (v2.1.152); Opus 4.8 + Dynamic Workflows + `/effort ultracode` (v2.1.154, 2026-05-28); verified 2026-06-05 (this run).
- [Code review](https://code.claude.com/docs/en/code-review) — Anthropic docs; verified 2026-06-03 (this run) — `/code-review`, `--fix`, `--comment` flag semantics; 80-confidence threshold; parallel review subagents.
- [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal) — Anthropic docs; verified 2026-05-27 — `/goal` completion-condition loop with separate evaluator model, 4,000-char limit, requires v2.1.139+.
- [Introducing dynamic workflows in Claude Code](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code) — Anthropic blog; published 2026-05-28 — research preview, 1,000-agent cap, 16 concurrent, plan availability (Max/Team on by default, Enterprise admin-gated, Pro toggle in `/config`).
- [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows) — Anthropic docs; verified 2026-06-06 (this run) — single-task keyword renamed `workflow` → `ultracode` in v2.1.160; `/effort ultracode` session setting (xhigh + auto-orchestration); v2.1.154 requirement; `CLAUDE_CODE_DISABLE_WORKFLOWS` env var.
- [Install Claude Code the Right Way in 2026](https://vanja.io/install-claude-code/) — secondary; npm-deprecation banner and native-installer migration path; verified 2026-05-25.
- [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) — Anthropic help center; verified 2026-06-20 (this run) — opening notice confirms the planned Agent SDK / `claude -p` billing split is paused as of 2026-06-15; usage still draws from subscription limits.
- [Anthropic puts Claude agents on a meter across its subscriptions](https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html) — InfoWorld; published 2026-05-14 — the (now-paused) plan to move `claude -p` and the Agent SDK onto a separate credit pool on 2026-06-15.
- [Introducing Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5) — Anthropic news; published 2026-06-30; verified 2026-07-04 (this run) — Sonnet 5 (`claude-sonnet-5`) is the default for Free / Pro and the default in Claude Code, 1M-token context, intro pricing through 2026-08-31; Opus 4.8 still selectable.
- [Redeploying Claude Fable 5](https://www.anthropic.com/news/redeploying-fable-5) — Anthropic news; published 2026-06-30; verified 2026-07-04 (this run) — export controls lifted 2026-06-30; Fable 5 redeployed globally 2026-07-01 on Claude Platform / Claude.ai / Claude Code / Cowork; Mythos 5 restricted to approved U.S. orgs.
- [Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome) — Anthropic help center; verified 2026-07-04 (this run) — Chrome extension GA 2026-07-01, build-test-verify pairing with Claude Code, all paid plans, Pro limited to Haiku 4.5.
- [Claude Code changelog (v2.1.196–v2.1.220)](https://code.claude.com/docs/en/changelog) — Anthropic docs; verified 2026-07-25 (this run) — Sonnet 5 default (v2.1.197, 2026-06-30); Claude in Chrome GA + subagents background-by-default + `/dataviz` skill + background agents auto-open draft PRs (v2.1.198, 2026-07-01); permission dialogs require manual approval by default (v2.1.200, 2026-07-03); screen-reader mode `--ax-screen-reader` (v2.1.208, 2026-07-14); `/fork` now copies the conversation into a background session and the in-session subagent launcher becomes `/subtask` (v2.1.212, 2026-07-17); EndConversation tool (v2.1.214, 2026-07-18); `/verify` and `/code-review` no longer auto-run — manual invocation required (v2.1.215, 2026-07-19); `sandbox.filesystem.disabled` setting (v2.1.216, 2026-07-20); `/code-review` runs as a background subagent (v2.1.218, 2026-07-22); **Claude Opus 5 becomes the default** (v2.1.219, 2026-07-24). Latest release v2.1.220 (2026-07-25).
- [Introducing Claude Opus 5](https://www.anthropic.com/news/claude-opus-5) — Anthropic news; published 2026-07-24; verified 2026-07-25 — `claude-opus-5`, $5 / $25 per Mtok (same as Opus 4.8), 1M context, available on Claude API / Bedrock / Vertex / Foundry / claude.ai / Claude Code / Cowork, new default on Max and strongest on Pro, flagged requests fall back to Opus 4.8.
- [Let Claude use your computer in Cowork](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork) — Anthropic help center; verified 2026-08-01 (this run) — confirms computer use is available in both Cowork and Claude Code, Desktop app only, Pro/Max, macOS + Windows.
- [Put Claude to work on your computer](https://claude.com/blog/dispatch-and-computer-use) — Anthropic blog; published 2026-03-23; verified 2026-08-01 (this run) — Dispatch + computer use launch, Cowork and Claude Code.
- [Claude Code product landing](https://claude.com/product/claude-code) — re-verified 2026-08-15 (this run); install command (`curl -fsSL https://claude.ai/install.sh | bash`) and launch surfaces (Terminal, Desktop, VS Code, JetBrains, web, iOS/Android, Slack, GitHub Actions) unchanged.
- [Claude Code changelog (v2.1.221–v2.1.224, 2026-08-03 to 2026-08-07)](https://code.claude.com/docs/en/changelog) — Anthropic docs; verified 2026-08-08 — `claude self-hosted-runner` and cross-session `SendMessage`/`ListAgents` (v2.1.224); `archive` plugin source (zip + SHA-256, v2.1.224); 200-subagent-per-session spawn cap removed (v2.1.224); Focus view chat-menu toggle (v2.1.221); permission/sandbox hardening (v2.1.222–223).
- [Claude Code changelog (v2.1.225–v2.1.233, 2026-08-08 to 2026-08-14)](https://code.claude.com/docs/en/changelog) — Anthropic docs; verified 2026-08-15 (this run) — `@`-mention of another session by name plus `/config` rows for "Dialog expiry" / "Messages from your other sessions" (v2.1.232); GitLab support in plugin marketplaces (v2.1.232); `--worktree` and `claude agents` recognize GitLab merge requests as `!N` (v2.1.233). Latest release v2.1.233.
