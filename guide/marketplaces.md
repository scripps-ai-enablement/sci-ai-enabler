# Marketplaces

> Curated catalogs of plugins (and the skills/MCP servers inside them) that Claude Code can install from.

_Last updated: 2026-05-19_

## What it is

A marketplace is a `marketplace.json` index — usually in a GitHub repo — listing plugins available for `/plugin install`. Once you register a marketplace, its plugins are discoverable in the `/plugin` browser and addressable as `<plugin-name>@<marketplace-name>`. Sources can be GitHub `owner/repo`, any Git URL, a local directory, or a direct URL to a hosted `marketplace.json`.

Anthropic ships the `claude-plugins-official` marketplace pre-registered — it's available the first time you open Claude Code. Other Anthropic-managed marketplaces (community, life-sciences, knowledge-work) and any third-party marketplace must be added explicitly.

## When to use it

- You want one command to make a vendor's plugins discoverable.
- Your team maintains internal plugins and wants to install them with a single source-of-truth URL.
- You want to pull a domain bundle (e.g., life sciences) without picking plugins one at a time.

## How to install / enable

Inside a Claude Code session, add a marketplace by GitHub `owner/repo`:

```bash
/plugin marketplace add anthropics/life-sciences
/plugin install pubmed@life-sciences
```

Other source forms:

```bash
/plugin marketplace add anthropics/claude-plugins-community
/plugin marketplace add https://github.com/your-org/your-marketplace.git
/plugin marketplace add ~/projects/local-marketplace
```

List, remove, or update with `/plugin marketplace list`, `/plugin marketplace remove <name>` (or `rm`), and `/plugin marketplace update <name>`.

## Common pitfalls

- Skipping `/plugin marketplace add` before `/plugin install` — installs need a registered source.
- Adding a private repo without authentication — Claude Code uses your local Git credentials.
- Forgetting to `/plugin marketplace update` after the upstream marketplace changes.
- Trusting marketplaces blindly. Marketplaces are arbitrary repos; review the plugins they list.

## See also

- [Plugins](plugins.md) — what marketplaces distribute
- [Discover plugins reference](https://code.claude.com/docs/en/discover-plugins) — canonical docs
- [`anthropics/life-sciences`](https://github.com/anthropics/life-sciences) — domain marketplace
- [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) — cross-domain marketplace (pre-registered)
- Catalog examples that install via this marketplace: [Translational Medicine](../catalog/translational-medicine.md)

## Sources

- [Discover and install prebuilt plugins through marketplaces](https://code.claude.com/docs/en/discover-plugins) — Anthropic docs; verified 2026-05-19 (this run).
- [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) — verified 2026-05-19.
- [`anthropics/life-sciences`](https://github.com/anthropics/life-sciences) — verified 2026-05-19.
- [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community) — verified 2026-05-19.
