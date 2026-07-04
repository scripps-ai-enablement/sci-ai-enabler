---
title: Claude surfaces
parent: Guide
nav_order: 1
has_children: true
---

# Claude surfaces

> The places you can use Claude: Claude.ai, Claude Desktop, Claude Code (terminal, IDE, and web), Claude Cowork, and the Claude API.

## What it is

Ways to talk to the same Anthropic models. Each surface has different strengths and different component support. Pick the surface that matches your work, then read its sub-page for install and feature detail.

| Surface | Best for | Components supported |
|---|---|---|
| [Claude.ai](surfaces/claude-ai.html) | Chat, document upload, one-click Connectors | Connectors, Projects |
| [Claude Desktop](surfaces/claude-desktop.html) | The same chat plus local files via MCP | Connectors, MCP servers |
| [Claude Code](surfaces/claude-code.html) | Multi-step coding (CLI, IDE, web) | Skills, MCP servers, Plugins, Hooks, Routines |
| [Claude Cowork](surfaces/claude-cowork.html) | Non-coding desktop automation in a sandboxed VM | Connectors, Plugins |
| [Claude API](surfaces/claude-api.html) | Building your own product, agent, or backend | SDKs, Managed Agents, MCP |

Your account, Projects, and conversation history are shared across Claude.ai and Claude Desktop. Claude Code and Cowork are billed through your Pro/Max/Team/Enterprise subscription or via API.

## Cross-cutting features

Some features span more than one surface — you start them in one place and view or extend them in another. Read the linked page for detail.

- **[Routines](advanced/routines.html)** — scheduled remote Claude Code agents. Created via the `/schedule` skill in [Claude Code](surfaces/claude-code.html), viewed and edited at `claude.ai/code/routines` (a [Claude.ai](surfaces/claude-ai.html) surface), execute on Anthropic cloud infrastructure with MCP connectors attached.
- **Background sessions** — `claude --bg` starts a long-running Claude Code task; reattach later via `/resume` or `claude agents`. Spans CLI and `claude.ai/code`.
- **MCP tunnels (Research Preview)** — outbound-only `cloudflared` tunnels that expose private MCP servers to Claude.ai. Bridges Claude.ai / Claude Desktop and MCP servers running inside private networks. See [MCP servers](mcp-servers.html).
- **Channels (Research Preview)** — inverts MCP from pull to push: an allowlisted MCP server can inject events into a running [Claude Code](surfaces/claude-code.html) session so Claude reacts to outside happenings (CI failures, monitoring alerts, an iMessage). Start a session with `claude --channels discord,telegram,imessage`; bundled plugins are Telegram, Discord, iMessage, and `fakechat`. Requires a `claude.ai` login (no API-key auth); Team / Enterprise admins must set `channelsEnabled: true` and curate `allowedChannelPlugins`. Custom channels need `--dangerously-load-development-channels`. Bridges Claude Code and [MCP servers](mcp-servers.html). Shipped 2026-03-20 in v2.1.80.
- **Claude Security (Enterprise public beta)** — vulnerability scanning at `claude.ai/security` (sidebar icon in [Claude.ai](surfaces/claude-ai.html)). Launched 2026-05-04 on Opus 4.7. Each finding has a remediation button that opens a [Claude Code on the web](surfaces/claude-code.html) session, drafts a patch, and opens a PR. Enterprise plans only; Team / Max coming.
- **Dynamic Workflows (Research Preview)** — spans CLI, Desktop, and the VS Code extension of [Claude Code](surfaces/claude-code.html). Claude writes an orchestration script on the fly and runs up to 1,000 parallel subagents (16 concurrent) to tackle migrations, audits, and other large jobs. Trigger one task by including the keyword `ultracode` in a prompt (renamed from `workflow` in v2.1.160 — the bare word `workflow` no longer fires), or set `/effort ultracode` to auto-orchestrate every substantive task in the session. Launched 2026-05-28 alongside Opus 4.8; requires Claude Code v2.1.154+. On by default on Max and Team; admin-gated on Enterprise; off by default on Pro (toggle in `/config`). Burns substantially more tokens than a normal session.
- **Claude Tag (Team / Enterprise beta)** — a Slack-native Claude you add to channels and `@Claude` to delegate tasks. It's a fifth place to reach Claude — one shared "multiplayer" agent per channel that remembers channel context, works async, and can schedule its own follow-ups; admins scope its tools/data/memory per channel and set token-spend caps. Uses Opus 4.8. Launched 2026-06-23 in beta; it **replaces the old Claude-in-Slack app**, and admins have a 30-day window to opt in to migrate. Anthropic frames it as an evolution of [Claude Code](surfaces/claude-code.html) into Slack, so the tag-a-task workflow will feel familiar.
- **Claude in Chrome (generally available 2026-07-01)** — a browser extension that reads, clicks, and navigates sites in a Chrome side panel. It's a sixth place to reach Claude, and it pairs with [Claude Code](surfaces/claude-code.html) for a build-test-verify loop (build in the terminal, drive the browser to test). All paid plans; Pro is limited to Haiku 4.5. Chrome only — no other Chromium browsers, no mobile.
- **Sandboxing differs by surface** — useful to know when reasoning about what Claude can touch on your machine. Per [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) (Anthropic engineering, late May 2026): [Claude.ai](surfaces/claude-ai.html) runs tools inside gVisor; [Claude Code](surfaces/claude-code.html) running locally uses macOS Seatbelt or Linux Bubblewrap (reads allowed, writes inside the workspace, network denied by default); [Claude Cowork](surfaces/claude-cowork.html) runs a full VM (Apple Virtualization on macOS, HCS on Windows). Local MCP servers you wire into [Claude Desktop](surfaces/claude-desktop.html) run with your user's permissions, not inside a sandbox — review folders and scripts before exposing them.

## Common pitfalls

- Confusing Claude Desktop, Claude Code, and Claude Cowork — three different apps that all live near `claude.ai`.
- Components don't all install everywhere. Skills, MCP servers, and Plugins work in Claude Code and Cowork; Connectors work in Claude.ai / Desktop / Cowork. A few tools (e.g., PubMed) ship in multiple places.
- API usage is metered separately from a Pro subscription.

## See also

- [Decision tree](decision-tree.html)
- [Skills](skills.html), [MCP servers](mcp-servers.html), [Plugins](plugins.html), [Connectors](connectors.html)
- [Claude Code overview](https://code.claude.com/docs/) — canonical docs
- [Claude.ai help center](https://support.claude.com/) — canonical docs

## Sources

- [Claude Code product landing](https://claude.com/product/claude-code) — Anthropic product page; verified 2026-05-26 (this run) — canonical install command and Windows/WinGet/Linux package options.
- [Set up Claude Code](https://code.claude.com/docs/en/setup) — Anthropic docs; verified 2026-05-26 (this run).
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) — Anthropic docs; verified 2026-05-19.
- [Claude Code on the web (announcement)](https://www.anthropic.com/news/claude-code-on-the-web) — published 2025-10-20.
- [Anthropic announces Claude Cowork](https://www.infoq.com/news/2026/01/claude-cowork/) — published 2026-01-13.
- [Cowork and plugins for teams across the enterprise](https://claude.com/blog/cowork-plugins-across-enterprise) — Anthropic blog; published 2026-02-24.
- [Claude Code changelog (v2.1.144 / v2.1.145, May 18–19 2026)](https://code.claude.com/docs/en/changelog) — `claude --bg`, `/resume`, `claude agents --json`; verified 2026-05-26.
- [Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome) — Anthropic help center; verified 2026-07-04 (this run) — Chrome extension GA 2026-07-01, build-test-verify pairing with Claude Code, all paid plans, Pro limited to Haiku 4.5, Chrome-only.
- [Claude Security is now in public beta](https://claude.com/blog/claude-security-public-beta) — Anthropic blog; published 2026-05-04 — `claude.ai/security`, Opus 4.7, remediation opens Claude Code on the web, Enterprise public beta.
- [Getting started with Claude Security](https://claude.com/resources/tutorials/getting-started-with-claude-security) — Anthropic tutorial; verified 2026-05-26 — sidebar location and remediation-session flow.
- [Introducing dynamic workflows in Claude Code](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code) — Anthropic blog; published 2026-05-28 — research preview, 1,000-agent cap, 16 concurrent, plan availability and defaults.
- [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows) — Anthropic docs; verified 2026-06-06 (this run) — single-task keyword renamed `workflow` → `ultracode` in v2.1.160 (bare `workflow` no longer triggers); `/effort ultracode` is a session setting (sends xhigh + auto-orchestration), not a model effort level; effort ladder remains low/medium/high/xhigh/max; v2.1.154 requirement.
- [Introducing Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8) — Anthropic news; published 2026-05-28 — Opus 4.8 ship date, paired Dynamic Workflows + effort-control launch.
- [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) — Anthropic engineering blog; published late May 2026 (verified 2026-05-31 this run) — per-surface sandbox stack: gVisor for Claude.ai, Seatbelt (macOS) / Bubblewrap (Linux) for Claude Code local with default-deny network, full VM (Apple Virtualization / HCS) for Cowork.
- [How we contain Claude across products (link blog)](https://simonwillison.net/2026/May/30/how-we-contain-claude/) — Simon Willison; published 2026-05-30 — independent summary of the same engineering post.
- [Channels reference](https://code.claude.com/docs/en/channels-reference) — Anthropic docs; verified 2026-06-03 — `--channels`, bundled plugins, `claude.ai` OAuth-only auth, Team / Enterprise `channelsEnabled` + `allowedChannelPlugins` managed settings, `--dangerously-load-development-channels`.
- [Introducing Claude Tag](https://www.anthropic.com/news/introducing-claude-tag) — Anthropic news; published 2026-06-23; verified 2026-06-27 (this run) — Slack-native `@Claude`, beta on Team / Enterprise, Opus 4.8, replaces the Claude-in-Slack app, 30-day admin opt-in window, per-channel tool/data/memory scoping and token caps.
- [Claude Code 2.1.80: --channels Lets MCP Servers Push Messages Into Your Session](https://www.vibesparking.com/en/blog/ai/claude-code/changelog/2026-03-20-claude-code-2180-channels-mcp-push-messages/) — Vibe Sparking AI; published 2026-03-20 — research-preview launch context, Telegram / Discord initial channels.
