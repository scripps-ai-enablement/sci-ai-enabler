# sci-ai-enabler

An agent-maintained catalog of AI ecosystem components — MCP servers, plugins, skills, agents, workflows, and related systems — for life-science applications.

A scheduled GitHub Action runs a Claude-based curator daily that researches, verifies, and updates entries across seven categories. All output lives as plain markdown under [`catalog/`](catalog/) and is also rendered as a [GitHub Pages site](https://goodb.github.io/sci-ai-enabler/).

## Browse the catalog

- [Chemistry](catalog/chemistry.md)
- [Immunology and Microbiology](catalog/immunology-microbiology.md)
- [Integrative Structural and Computational Biology](catalog/structural-computational-biology.md)
- [Molecular and Cellular Biology](catalog/molecular-cellular-biology.md)
- [Neuroscience](catalog/neuroscience.md)
- [Translational Medicine](catalog/translational-medicine.md)
- [Drug Repurposing and Discovery](catalog/drug-repurposing-discovery.md)

See [`CHANGELOG.md`](CHANGELOG.md) for the history of curator updates.

## How it works

- [`AGENT.md`](AGENT.md) — the curator's system prompt and schema. Single source of truth for entry structure and curator behavior.
- [`.github/workflows/curate.yml`](.github/workflows/curate.yml) — runs the curator daily at 13:00 UTC, or on demand. Uses the [Claude Code GitHub Action](https://github.com/anthropics/claude-code-base-action) on a GitHub-hosted runner with web search and web fetch enabled.
- Each run with substantive changes commits to `main` and posts a comment on the pinned **"Catalog updates"** issue, which is how update notifications land in your inbox.

## Triggering an on-demand run

From the browser: **Actions** → **Curate catalog** → **Run workflow**. You can optionally scope the run to a single category.

From the terminal:

```sh
gh workflow run curate.yml                       # all categories
gh workflow run curate.yml -f category=chemistry # one category
```

## One-time setup

1. Add an `ANTHROPIC_API_KEY` repository secret (**Settings → Secrets and variables → Actions**).
2. Enable GitHub Pages from the `main` branch root (**Settings → Pages → Source: Deploy from a branch → main / (root)**).
3. Watch the repo (or just the **Catalog updates** issue once the first run creates it) to receive email notifications on each update.
