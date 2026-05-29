---
title: Claude.ai
parent: Claude surfaces
grand_parent: Guide
nav_order: 1
---

# Claude.ai

> The web app at `claude.ai` — chat, document upload, Projects, and one-click Connectors.

## What it is

The browser-based Claude. You sign in at `https://claude.ai`, pick a model, and chat. Beyond chat, Claude.ai is where you manage your Anthropic-managed integrations (Connectors), organize long-running context in Projects, and view the results of remote agents you started elsewhere.

Account, Projects, and history are shared with Claude Desktop. Connectors enabled here also light up in Claude Desktop and Cowork.

## When to use it

- Quick chat, brainstorming, document Q&A.
- Browsing and toggling [Connectors](../connectors.html) from the Settings panel.
- Viewing scheduled [Routines](../advanced/routines.html) you created from Claude Code, at `claude.ai/code/routines`.
- Resuming a [Claude Code on the web](claude-code.html) session at `claude.ai/code`.
- (Enterprise) Running vulnerability scans from the **Security** sidebar icon at `claude.ai/security` — see Claude Security under cross-cutting features on [Claude surfaces](../claude-surfaces.html).
- Generating quick visuals — prototypes, slides, one-pagers — via **Claude Design** at `claude.ai/design` (Anthropic Labs research preview launched 2026-04-17; included with Pro / Max / Team / Enterprise; off by default on Enterprise until an admin enables it).
- Anything where you do not need filesystem or terminal access.

## How to install / enable

- Sign in at `https://claude.ai`. No install needed.
- Enable Connectors: Settings → Connectors → Browse Directory (`claude.ai/directory/connectors`). Toggle a connector and complete OAuth if prompted.
- For Team/Enterprise admins, custom remote MCP connectors are added from the admin console.

## Common pitfalls

- File uploads here are not the same as local filesystem access. For real local-file work, use Claude Desktop (Connectors with file access) or Claude Code.
- Connector availability depends on your plan tier. Some Healthcare/Legal connectors require Team or Enterprise.
- A Connector enabled in Claude.ai is also available in Claude Desktop on the same account — it's not a per-surface toggle.

## See also

- [Connectors](../connectors.html) — the integration model behind one-click toggles here.
- [Claude Code (on the web)](claude-code.html) — the cloud-VM coding surface, accessed at `claude.ai/code`.
- [Routines](../advanced/routines.html) — scheduled remote agents, viewable at `claude.ai/code/routines`.

## Sources

- [Claude.ai product page](https://claude.com/product/claude) — Anthropic product page; verified 2026-05-26 (this run).
- [Use Connectors to extend Claude's capabilities](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities) — Anthropic help center; verified 2026-05-26.
- [Claude Code on the web (announcement)](https://www.anthropic.com/news/claude-code-on-the-web) — published 2025-10-20.
- [Claude Security is now in public beta](https://claude.com/blog/claude-security-public-beta) — Anthropic blog; published 2026-05-04 — Security sidebar icon at `claude.ai/security`, Enterprise public beta.
- [Introducing Claude Design by Anthropic Labs](https://www.anthropic.com/news/claude-design-anthropic-labs) — Anthropic news; published 2026-04-17 — `claude.ai/design`, research preview, Pro/Max/Team/Enterprise availability, Enterprise admin-enable.
