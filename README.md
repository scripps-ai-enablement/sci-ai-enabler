# sci-ai-enabler

Three agent-maintained resources for Claude users working in life science:

- **[Catalog](catalog/)** — what Claude Skills, MCP servers, Plugins, and Claude.ai Connectors are available for life-science work, organized into seven research areas.
- **[Guide](guide/)** — short, beginner-facing pages that explain what those components are and how to install them.
- **[Autonomous science](autonomous-science/)** — a tracker of AI co-scientist systems: named agents that perform hypothesis generation, experiment design, or analysis with meaningful autonomy. Manuscript writing is treated as a downstream subcomponent.

All three are rendered as a [GitHub Pages site](https://goodb.github.io/sci-ai-enabler/) and refreshed by separate scheduled GitHub Actions.

## Browse the catalog

- [Chemistry](catalog/chemistry.md)
- [Immunology and Microbiology](catalog/immunology-microbiology.md)
- [Integrative Structural and Computational Biology](catalog/structural-computational-biology.md)
- [Molecular and Cellular Biology](catalog/molecular-cellular-biology.md)
- [Neuroscience](catalog/neuroscience.md)
- [Translational Medicine](catalog/translational-medicine.md)
- [Drug Repurposing and Discovery](catalog/drug-repurposing-discovery.md)

See [`CHANGELOG.md`](CHANGELOG.md) for the catalog's update history.

## Read the guide

Start here if you're new to Claude Skills, MCP servers, or Plugins.

- [Claude surfaces](guide/claude-surfaces.md) — which Claude product is which.
- [Skills](guide/skills.md), [MCP servers](guide/mcp-servers.md), [Plugins](guide/plugins.md), [Marketplaces](guide/marketplaces.md), [Connectors](guide/connectors.md) — one short page per concept.
- [Decision tree](guide/decision-tree.md) — "I want to do X — which should I use?"
- [Advanced](guide/advanced/) — hooks, custom slash commands, authentication.

See [`GUIDE_CHANGELOG.md`](GUIDE_CHANGELOG.md) for the guide's update history.

## Track autonomous AI scientists

A separate track focused on the emerging field of AI co-scientists — systems that semi- or fully-autonomously perform hypothesis generation, experiment design, or analysis. Manuscript writing is welcome as a secondary capability but is not the focus; writing-only systems are out of scope.

- [Summary](autonomous-science/summary.md) — landscape view of the field.
- [Entries](autonomous-science/entries.md) — one block per named system (Google AI co-scientist, FutureHouse Aviary, ChemCrow, etc.).
- [`sources/`](sources/) — archived PDFs the curator has read, with `pdftotext` sidecars; [`sources/manifest.json`](sources/manifest.json) is the dedup registry.

See [`COSCIENTIST_CHANGELOG.md`](COSCIENTIST_CHANGELOG.md) for the autonomous-science update history.

## How it works

Three independent scheduled agents, each a [Claude Code GitHub Action](https://github.com/anthropics/claude-code-base-action) run on a GitHub-hosted runner with web search and fetch enabled. Each posts to its own pinned tracking issue when a run produced changes — that's how update notifications land in your inbox.

| Resource | Prompt | Workflow | Schedule | Tracking issue |
|---|---|---|---|---|
| Catalog | [`AGENT.md`](AGENT.md) | [`curate.yml`](.github/workflows/curate.yml) | Daily 13:00 UTC | "Catalog updates" |
| Guide | [`GUIDE_AGENT.md`](GUIDE_AGENT.md) | [`guide.yml`](.github/workflows/guide.yml) | Daily 14:30 UTC | "Guide updates" |
| Autonomous science | [`COSCIENTIST_AGENT.md`](COSCIENTIST_AGENT.md) | [`coscientist.yml`](.github/workflows/coscientist.yml) | Daily 16:00 UTC | "AI co-scientist updates" |

## Triggering an on-demand run

From the browser: **Actions** → choose the workflow → **Run workflow**. You can optionally scope to a single category or topic.

From the terminal:

```sh
gh workflow run curate.yml                       # whole catalog
gh workflow run curate.yml -f category=chemistry # one category
gh workflow run guide.yml                        # whole guide
gh workflow run guide.yml -f topic=skills        # one topic
gh workflow run coscientist.yml                  # daily autonomous-science update
gh workflow run coscientist.yml -f scope=bootstrap  # re-seed from sources/
```

## One-time setup

1. Add an `ANTHROPIC_API_KEY` repository secret (**Settings → Secrets and variables → Actions**).
2. Enable GitHub Pages from the `main` branch root (**Settings → Pages → Source: Deploy from a branch → main / (root)**).
3. Watch the repo (or the **Catalog updates**, **Guide updates**, and **AI co-scientist updates** issues once the first runs create them) to receive email notifications.
