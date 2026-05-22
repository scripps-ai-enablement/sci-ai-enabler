---
title: Routines
parent: Advanced
grand_parent: Guide
nav_order: 4
---

# Routines

> Saved Claude Code automations that run unattended in Anthropic's cloud — fired on a schedule, by API call, or by a GitHub event — with MCP connectors and a repo attached.

## What it is

A routine packages a prompt, optional GitHub repo, and a set of connectors into a configuration you can fire by **schedule** (cron-style), **API** call, or **GitHub** event (PR opened, release published, …). Each firing spins up a fresh, isolated Claude Code session on Anthropic-managed cloud infrastructure — own VM, own git checkout, no memory of previous runs. Output is stored in a web transcript you can revisit any time.

Routines straddle two surfaces: you create and manage them from [Claude Code](../surfaces/claude-code.html) (`/schedule`) or at `claude.ai/code/routines`, and you view results in the same web UI. They launched in research preview 2026-04-14.

## When to use it

- Recurring digests, status reports, monitoring — anything you want fired on a clock.
- Reacting to GitHub events (a new PR, a tagged release) without standing up your own webhook handler.
- One-off scheduled runs: "do this tomorrow at 9am" — the form has a one-time option that auto-disables after firing.
- Programmatic triggers from your own systems via the API trigger.

## How to install / enable

The skill is bundled with Claude Code; no install needed. Routines require Claude Code on the web enabled on Pro, Max, Team, or Enterprise.

- In Claude Code, type `/schedule` and describe the task in plain language. Claude drafts the prompt, schedule, and MCP attachments, then creates the routine. For a non-preset cadence, run `/schedule update` to set a custom cron expression.
- Manage routines in the web UI:

  ```
  https://claude.ai/code/routines
  https://claude.ai/code/routines/<routine_id>
  ```

- API trigger requests must include the beta header `anthropic-beta: experimental-cc-routine-2026-04-01`.

## Common pitfalls

- **Schedules are local-timezone.** The web UI and `/schedule` interpret times in your local zone and auto-convert to UTC; verify the printed UTC equivalent in the routine config if you suspect drift. (Older guides that say "cron is UTC" describe an earlier behavior.)
- **Minimum interval is one hour.** `*/30 * * * *` is rejected.
- **Daily run caps.** Pro: 5 routines/day. Max: 15. Team / Enterprise: 25.
- **Each run is isolated.** No state carries between firings. Persist to a repo, an external store, or have the prompt re-derive state.
- **No email or push notification by default.** Wire a Slack / Gmail / etc. connector and ask the prompt to post results if you want active delivery.
- **Remote agents have no local context.** They cannot see files on your laptop, your local env vars, or local MCP servers. Use HTTP MCP connectors or have the agent clone a public repo.

## See also

- [Claude Code](../surfaces/claude-code.html) — where you create routines via `/schedule`.
- [Claude.ai](../surfaces/claude-ai.html) — where you view and edit them at `claude.ai/code/routines`.
- [MCP servers](../mcp-servers.html) and [Connectors](../connectors.html) — what you can attach to a routine.
- [Authentication](authentication.html) — how routines authenticate to MCP connectors via OAuth.

## Sources

- [Automate work with routines](https://code.claude.com/docs/en/routines) — Anthropic docs; verified 2026-05-22 (this run) — primary reference for schedule / API / GitHub triggers, plan availability, and local-timezone cron semantics.
- [Introducing routines in Claude Code](https://claude.com/blog/introducing-routines-in-claude-code) — Anthropic blog; published 2026-04-14 — launch announcement, daily limits (5 / 15 / 25), research-preview status.
- [Trigger a routine via API](https://platform.claude.com/docs/en/api/claude-code/routines-fire) — Anthropic API docs; verified 2026-05-22 — `experimental-cc-routine-2026-04-01` beta header.
- [Claude managed agents updates](https://claude.com/blog/claude-managed-agents-updates) — Anthropic blog; published 2026-05-19 — broader cloud-hosted agent infrastructure context.
- [Claude Code changelog](https://code.claude.com/docs/en/changelog) — Anthropic docs; verified 2026-05-22 — `/schedule update`, Stop-hook `session_crons` field.
