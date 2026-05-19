# Plugins

> Installable bundles for Claude Code that can ship skills, MCP servers, hooks, and slash commands together.

_Last updated: 2026-05-19_

## What it is

A Claude Code plugin is a distribution unit. One install can register multiple skills (`skills/`), MCP servers (`.mcp.json`), hooks (`hooks/`), and slash commands (`commands/` or `agents/`) at once. Plugins live in a marketplace — a repository or local directory with a `marketplace.json` index — and you install from there.

Plugins are a Claude Code feature only. They don't apply to Claude.ai or Claude Desktop chat; if you want that, see [Connectors](connectors.md).

## When to use it

- You want to install several related components with one command.
- You want to distribute a workflow to teammates and have everyone end up on the same version.
- A vendor or open-source project ships their offering as a plugin (e.g., the Anthropic Life Sciences plugins).
- You want enable/disable controls per project without uninstalling.

## How to install / enable

The Anthropic-managed marketplace `claude-plugins-official` is registered automatically when you start Claude Code. Install from it directly:

```bash
# inside a Claude Code session
/plugin install <plugin-name>@claude-plugins-official
```

For other marketplaces (community, vendor, your own), add the source first, then install:

```bash
/plugin marketplace add anthropics/life-sciences
/plugin install pubmed@life-sciences
```

Manage installs with `/plugin list`, `/plugin enable <name>`, `/plugin disable <name>`, `/plugin uninstall <name>`. Open the tabbed manager with `/plugin`. Run `/reload-plugins` after editing files in a local marketplace.

## Common pitfalls

- Forgetting the `@marketplace-name` suffix on `/plugin install` — Claude Code needs to know the source.
- Installing into the wrong scope. The CLI may prompt for project vs. user; choose deliberately.
- Treating plugins as runtime sandboxes — they bring along whatever the author shipped (skills, hooks, MCP). Review before installing.
- Expecting plugins to work in Claude.ai. They don't.

## See also

- [Marketplaces](marketplaces.md) — where plugins live
- [Skills](skills.md), [MCP servers](mcp-servers.md), [Hooks](advanced/hooks.md), [Slash commands](advanced/slash-commands.md)
- [Plugins reference](https://code.claude.com/docs/en/plugins) — canonical docs
- [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) — Anthropic's cross-domain marketplace

## Sources

- [Discover and install prebuilt plugins through marketplaces](https://code.claude.com/docs/en/discover-plugins) — Anthropic docs; verified 2026-05-19 (this run).
- [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) — verified 2026-05-19.
- [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community) — verified 2026-05-19.
- [`anthropics/claude-code` plugins README](https://github.com/anthropics/claude-code/blob/main/plugins/README.md) — verified 2026-05-19.
