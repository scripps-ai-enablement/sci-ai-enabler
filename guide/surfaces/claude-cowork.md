---
title: Claude Cowork
parent: Claude surfaces
grand_parent: Guide
nav_order: 4
---

# Claude Cowork

> The non-developer counterpart to Claude Code — a sandboxed desktop agent for file-heavy work (spreadsheets, slide decks, document wrangling), available inside the Claude desktop app.

## What it is

Cowork runs Claude as an agent inside a sandboxed VM with permission-gated access to local folders. It's aimed at non-coding workflows: editing spreadsheets, generating slide decks, reformatting reports, batching file operations. You interact with it from the Claude desktop app's sidebar; Anthropic manages the VM.

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

## Common pitfalls

- Cowork is not Claude Desktop chat and not Claude Code — it's a third surface that happens to live inside the desktop app.
- Sandboxed VM means local-only command-line tools and arbitrary binaries don't run; use [Claude Code](claude-code.html) for that.
- Folder access is permission-gated — grant access deliberately, not blanket.

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
