---
title: Routines
parent: Advanced
grand_parent: Guide
nav_order: 4
---

# Routines

> Scheduled remote Claude Code agents — cron-style jobs that run unattended in Anthropic's cloud, attach MCP connectors, and post their output to a web UI you can read later.

## What it is

A routine is a recurring (or one-time) Claude Code session that fires on a schedule. Each firing spins up a fresh, isolated cloud session — own VM, own git checkout, no memory of previous runs. You give the routine a prompt, a schedule, optional MCP connectors, and an optional GitHub repo to clone; Anthropic runs it and stores the transcript at a URL you can visit any time.

Routines straddle two surfaces: you create and manage them from [Claude Code](../surfaces/claude-code.html), and you view results at `claude.ai/code/routines` (a [Claude.ai](../surfaces/claude-ai.html) page).

## When to use it

- Weekly literature digests, status reports, monitoring jobs — anything you want fired on a clock.
- Polling external systems (a CI run, a deploy, a queue) you can't be notified about otherwise.
- One-time scheduled runs: "do this tomorrow at 9am" — set `run_once_at` and the routine auto-disables after firing.

## How to install / enable

The skill is bundled with Claude Code; no install needed.

- In Claude Code, type `/schedule` and describe the task in plain language. Claude will draft the prompt, schedule, and MCP attachments, then create the routine.
- View, edit, or run a routine on demand:

  ```
  https://claude.ai/code/routines/<routine_id>
  ```

- Or list every routine on your account: `https://claude.ai/code/routines`.
- To rerun via the API, the `run` action on the routine triggers an immediate execution outside the schedule.

## Common pitfalls

- **Cron is UTC.** Always convert your local time before pasting an expression. Claude Code will do the conversion if you say "every Monday at 8am Pacific" — verify the printed UTC equivalent.
- **Minimum interval is one hour.** `*/30 * * * *` is rejected.
- **Each run is isolated.** No state carries between firings. If you need continuity ("don't re-show last week's hits"), build it into the prompt or persist to a repo / external store.
- **No email or push notification by default.** You go look at the routine page. Wire a Slack connector and ask the prompt to post results if you want active delivery.
- **Cannot delete via API.** Delete from the web UI at `claude.ai/code/routines`. Disabling (`enabled: false`) is API-supported.
- **Remote agents have no local context.** They cannot see files on your laptop, your local env vars, or local MCP servers. Use HTTP MCP connectors or have the agent clone a public repo.

## See also

- [Claude Code](../surfaces/claude-code.html) — where you create routines via `/schedule`.
- [Claude.ai](../surfaces/claude-ai.html) — where you view and edit them at `claude.ai/code/routines`.
- [MCP servers](../mcp-servers.html) and [Connectors](../connectors.html) — what you can attach to a routine.
- [Authentication](authentication.html) — how routines authenticate to MCP connectors via OAuth.

## Sources

- `claude.ai/code/routines` — Anthropic routine management UI; observed in-session 2026-05-21 (this run).
- [Claude managed agents updates](https://claude.com/blog/claude-managed-agents-updates) — Anthropic blog covering cloud-hosted agent infrastructure; verified 2026-05-21.
- [Claude Code changelog](https://code.claude.com/docs/en/changelog) — Anthropic docs; verified 2026-05-21.
