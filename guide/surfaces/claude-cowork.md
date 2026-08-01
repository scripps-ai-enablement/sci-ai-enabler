---
title: Claude Cowork
parent: Claude surfaces
grand_parent: Guide
nav_order: 4
---

# Claude Cowork

> The non-developer counterpart to Claude Code — an agent for file-heavy work (spreadsheets, slide decks, document wrangling), available in the Claude desktop app and, in beta, on the web and mobile.

## What it is

Cowork runs Claude as an agent with permission-gated access to your files. It's aimed at non-coding workflows: editing spreadsheets, generating slide decks, reformatting reports, batching file operations. It started as a sandboxed-VM app inside Claude Desktop; since 2026-07-07 it's also in beta on the web (`claude.ai`) and mobile (iOS/Android), where sessions run on Anthropic's servers and follow you across devices — start a task at your desk, check it from your phone. The full desktop experience (local files, browser, [computer use](../claude-surfaces.html#cross-cutting-features)) stays desktop-only.

Cowork supports **Plugins** — packaged bundles that combine Connectors and workflow templates. Anthropic ships department-specific Cowork plugins (e.g., Claude for Small Business) that pre-wire a set of connectors for a use case.

## When to use it

- File and document automation that doesn't require coding.
- Workflows that need a desktop agent with controlled local-folder access.
- Trying a packaged Cowork plugin (e.g., Claude for Small Business) instead of wiring connectors yourself.

## How to install / enable

- Install [Claude Desktop](claude-desktop.html) on macOS or Windows. Cowork went generally available on both platforms on 2026-04-09; no Linux desktop client.
- Open the app and enable Cowork from the sidebar.
- Available on all paid plans (Pro, Max, Team, Enterprise). Max 5x or higher is recommended for daily use; Cowork tasks consume substantially more tokens than chat.
- Install a Cowork plugin from the Plugins surface in the app, or via the Claude.ai directory (`claude.ai/directory`).
- To try the web/mobile beta instead: on Max, start a Cowork session from the `claude.ai` home screen, or open Cowork from the sidebar in the Claude iOS/Android app.

## Common pitfalls

- Cowork is not Claude Desktop chat and not Claude Code — it's a distinct surface, now reachable from the desktop app, `claude.ai`, or mobile.
- Local-only command-line tools and arbitrary binaries don't run in Cowork; use [Claude Code](claude-code.html) for that. The desktop app's [computer use](../claude-surfaces.html#cross-cutting-features) toggle gets you screen control instead, not a real shell.
- Folder access is permission-gated — grant access deliberately, not blanket.
- Web/mobile Cowork is beta and Max-first; other plans roll out over the following weeks with no fixed date.

## See also

- [Plugins](../plugins.html) — bundles that ship Cowork workflows.
- [Connectors](../connectors.html) — the integrations Cowork plugins wire together.
- [Claude Desktop](claude-desktop.html) — the host app.

## Sources

- [Anthropic announces Claude Cowork](https://www.infoq.com/news/2026/01/claude-cowork/) — published 2026-01-13.
- [Cowork and plugins for teams across the enterprise](https://claude.com/blog/cowork-plugins-across-enterprise) — Anthropic blog; published 2026-02-24.
- [Anthropic Opens Claude Cowork to All Paid Plans on macOS, Windows](https://www.eweek.com/news/claude-cowork-general-availability-enterprise-controls/) — eWeek; covers 2026-04-09 GA on macOS and Windows; verified 2026-05-25 (this run).
- [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork) — Anthropic help center; verified 2026-05-25.
- [Claude for Small Business](https://www.anthropic.com/news/claude-for-small-business) — Anthropic news; published 2026-05-13.
- [Claude Cowork on web and mobile: hand off work anywhere](https://claude.com/blog/cowork-web-mobile) — Anthropic blog; published 2026-07-07; verified 2026-08-01 (this run) — beta web (`claude.ai`) and mobile (iOS/Android) access, cross-device continuity, background execution, Max-first rollout, doubled usage limits through 2026-08-05.
- [Let Claude use your computer in Cowork](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork) — Anthropic help center; verified 2026-08-01 (this run) — computer use toggle, Pro/Max only, macOS + Windows, research preview.
