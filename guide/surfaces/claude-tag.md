---
title: Claude Tag
parent: Claude surfaces
grand_parent: Guide
nav_order: 7
---

# Claude Tag

> Claude inside Slack — tag `@Claude` in a channel and delegate a task. A multiplayer surface where one Claude serves a whole channel, builds context from the conversation, and works asynchronously. Replaces the older "Claude in Slack" app.

## What it is

Claude Tag brings Claude into Slack as a collaborative team member. You invite Claude into a channel and mention `@Claude` with a request; Claude breaks the task into stages and executes them using the tools and data sources it's been granted. Because one Claude instance serves the entire channel, everyone can watch progress and jump into the same shared thread — it's a multiplayer surface rather than a private 1:1 chat.

Claude remembers relevant information from the channels it's in, so context carries across requests, and tasks run asynchronously — you delegate and keep working while Claude follows up on unresolved items when proactive updates are enabled. It runs on Opus 4.8 and replaces the earlier Claude in Slack app.

## When to use it

- Delegating work where your team already lives — triage, drafting, lookups, and follow-ups in a Slack channel.
- Multiplayer tasks where several teammates need to see and contribute to the same Claude thread.
- Asynchronous, longer-running work you want to hand off and check back on.
- Giving a channel a scoped Claude "identity" with its own access and memory for a specific workflow.

## How to install / enable

- Available in beta for **Claude Enterprise and Team** customers (launched 2026-06-23).
- An admin connects Claude Tag to the Slack workspace, grants Claude access to specific tools and data, and sets monthly spending limits (organization-wide and per-channel).
- Test in a private channel first, then invite Claude into the channels where you want it.
- Admins already running the older Claude in Slack app have a 30-day window to migrate to Claude Tag.

## Common pitfalls

- One Claude per channel is shared — treat the thread as team-visible, not a private conversation.
- Tool and data access is scoped per channel by an admin; if Claude can't reach a source, check the channel's grants rather than re-asking.
- Spending is metered; watch the org- and channel-level limits an admin has set.
- It's a distinct surface from [Claude Cowork](claude-cowork.html) and [Claude Code](claude-code.html) — same models, different place and interaction model.

## See also

- [Claude surfaces](../claude-surfaces.html) — the full surface comparison.
- [Connectors](../connectors.html) — the integrations an admin can wire into a channel.
- [Decision tree](../decision-tree.html) — pick the right surface for a task.

## Sources

- [Introducing Claude Tag](https://www.anthropic.com/news/introducing-claude-tag) — Anthropic news; published 2026-06-23 — Slack `@Claude` mention, multiplayer per-channel model, channel memory, asynchronous tasks and proactive updates, Opus 4.8, Enterprise/Team beta, admin tool/data scoping, org- and channel-level spending limits, per-channel Claude identities, replaces Claude in Slack with a 30-day migration window.
