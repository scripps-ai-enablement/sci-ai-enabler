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
- **Web** — `claude.ai/code` runs the agent in an Anthropic-managed cloud VM that clones your GitHub repo and opens PRs. Use `--teleport` from the CLI to hand off a cloud session into your terminal, or `claude --bg` to run a session in the background and reattach later via `/resume` or `claude agents` (a single-screen view of every running, blocked, and finished session; accepts `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--model`, `--effort`). Inside `claude agents`, prefix any shell command with `!` to spin it up as a detachable background job — equivalent to `claude --bg --exec '<command>'` from your shell.

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
- Pick a model with `/model` (or `--model` at launch). **Claude Fable 5** — a "Mythos-class" tier above Opus — is selectable as of v2.1.170 (2026-06-09); it's included free on Pro / Max / Team / Enterprise through 2026-06-22, then needs usage credits from 2026-06-23. Cybersecurity, biology / chemistry, and distillation prompts are auto-routed to Opus 4.8 (under ~5% of sessions). Opus 4.8 remains the default.

## Common pitfalls

- Claude Code on the web runs in a sandboxed VM with network restrictions; local-only MCP servers won't work there.
- Skills/plugins/MCP installed in `~/.claude/` (user scope) are global; `.claude/` in a repo (project scope) is per-repo.
- Background sessions accumulate — list with `claude agents` and clean up. Pin one with Ctrl+T in that view if you want it kept alive when idle and restarted in place on updates; un-pinned sessions are shed first under memory pressure.
- **`claude -p` (headless / non-interactive mode) moves to a separate Agent SDK credit on 2026-06-15.** Interactive `claude` in the terminal still draws from your subscription. `claude -p`, Claude Code GitHub Actions, and any third-party harness that auths via the Agent SDK draw from a new dollar-denominated credit pool billed at standard API rates (one-time opt-in, no rollover). See [Claude API](claude-api.html) for the per-plan credit amounts.

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
- [Anthropic puts Claude agents on a meter across its subscriptions](https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html) — InfoWorld; published 2026-05-14 — `claude -p` and Agent SDK move off subscription limits onto a separate credit pool 2026-06-15; verified 2026-06-02 (this run).
- [Claude Fable 5 and Claude Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5) — Anthropic news; published 2026-06-09 — Mythos-class tier; Fable 5 selectable in Claude Code v2.1.170; subscription-free through 2026-06-22 then credit-gated; Opus-4.8 safety fallback (<5% of sessions). Verified 2026-06-10 (this run).
