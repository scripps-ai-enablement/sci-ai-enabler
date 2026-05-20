# Connectors

> Anthropic-managed integrations you toggle on inside the Claude.ai web, desktop, and mobile apps.

_Last updated: 2026-05-20_

## What it is

A Connector is a remote MCP server exposed through the Claude.ai UI. Anthropic (or a vendor partner) hosts the server and handles OAuth so you don't run anything yourself. You enable a connector once; it then appears as a toggle in the chat composer. Connectors inherit your permissions in the source system — Claude can only see what your account can.

Since March 2026 the Connectors directory lives at `claude.ai/directory/connectors` (alongside Skills and Plugins tabs in a unified Directory). The catalog has grown past 375 prebuilt integrations across productivity, design, finance, healthcare, legal, creative, and everyday-life categories — the May 12 "Claude for Legal" launch alone added 20+ connectors (DocuSign, LexisNexis, Westlaw, Everlaw, iManage, Harvey, Ironclad, …). Custom connectors are also supported: point Claude.ai at a remote MCP URL and it walks you through OAuth.

## When to use it

- You want a one-click integration inside Claude.ai chat (Google Drive, Slack, Notion, Microsoft 365, etc.).
- You're not using Claude Code and don't want to manage a local MCP server.
- You're on Team or Enterprise and want admin-controlled, org-wide access.
- You have a remote MCP server you want to expose to Claude.ai users.

## How to install / enable

Open `https://claude.ai/directory/connectors` (or `claude.ai/settings/connectors`), browse the directory, click **Connect**, and complete OAuth. Inside a chat, click the **+** button (or type **/**) → **Connectors** to toggle which ones are active for that conversation.

Add a custom connector:

```text
claude.ai → Settings → Connectors → Add custom connector
# Enter the remote MCP URL; optionally an OAuth client ID/secret.
```

On Team/Enterprise, an Owner enables the connector for the org first (Organization settings → Connectors), then each member authenticates individually.

## Common pitfalls

- Confusing connectors with Claude Code MCP servers. Same protocol underneath, different surface and install path.
- Forgetting to toggle the connector on for the specific conversation.
- Free-tier limit: one custom connector per account.
- Adding a custom connector that hasn't been vetted by Anthropic — review the source.
- Org-level enable doesn't grant access; each user still has to authenticate.

## See also

- [MCP servers](mcp-servers.md) — the underlying protocol
- [Claude surfaces](claude-surfaces.md)
- [Use connectors](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities) — canonical docs
- [Custom connectors with remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) — canonical docs
- Catalog example: [PubMed Connector](../catalog/translational-medicine.md)

## Sources

- [Use connectors to extend Claude's capabilities](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities) — Anthropic help center; verified 2026-05-19 (this run).
- [Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) — Anthropic help center; verified 2026-05-19.
- [Connectors directory](https://claude.com/docs/connectors/directory) — canonical directory listing; verified 2026-05-20.
- [Claude AI Connectors directory overview](https://www.claude.com/connectors) — verified 2026-05-20.
- [New connectors in Claude for everyday life](https://claude.com/blog/connectors-for-everyday-life) — Anthropic blog; AllTrails/Uber/Spotify/etc. added May 2026.
- [Anthropic Goes All-In on Legal](https://www.lawnext.com/2026/05/anthropic-goes-all-in-on-legal-releasing-more-than-20-connectors-and-12-practice-area-plugins-for-claude.html) — LawSites; published 2026-05-12 — 20+ legal connectors and 12 practice-area plugins.
- [Anthropic Expands Claude for Legal](https://www.technology.org/2026/05/13/anthropic-claude-legal-plugins-mcp-connectors/) — published 2026-05-13.
