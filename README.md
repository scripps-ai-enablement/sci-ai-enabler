# sci-ai-enabler

Four agent-maintained resources for Claude users working in life science:

- **[Catalog](catalog/)** — what Claude Skills, MCP servers, Plugins, and Claude.ai Connectors are available for life-science work, organized into seven research areas plus a General-Purpose Utilities shelf.
- **[Guide](guide/)** — short, beginner-facing pages that explain what those components are and how to install them.
- **[Autonomous science](autonomous-science/)** — a tracker of AI co-scientist systems: named agents that perform hypothesis generation, experiment design, or analysis with meaningful autonomy. Manuscript writing is treated as a downstream subcomponent.
- **[Recipes](recipes/)** — a cookbook pairing concrete life-science problems with recommended assemblies of the cataloged components, with explicit evidence labels and availability/compute metadata.

All four are rendered as a [GitHub Pages site](https://scripps-ai-enablement.github.io/sci-ai-enabler/) and refreshed by separate scheduled GitHub Actions.

## Browse the catalog

- [Chemistry](catalog/chemistry.md)
- [Immunology and Microbiology](catalog/immunology-microbiology.md)
- [Integrative Structural and Computational Biology](catalog/structural-computational-biology.md)
- [Molecular and Cellular Biology](catalog/molecular-cellular-biology.md)
- [Neuroscience](catalog/neuroscience.md)
- [Translational Medicine](catalog/translational-medicine.md)
- [Drug Repurposing and Discovery](catalog/drug-repurposing-discovery.md)
- [General-Purpose Utilities](catalog/general-purpose-utilities.md) — cross-cutting shelf

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

## Browse recipes

A cookbook pairing real problems with recommended assemblies of the cataloged components. Each recipe carries an evidence label (Validated / Reported / Proposed), an explicit availability tag, and a compute-requirements tag so you can decide if it fits your situation.

- [Recipes landing page](recipes/) — section overview, simplicity ladder, evidence labels.
- [Landscape](recipes/summary.md) — coverage by problem class, where the gaps are.
- [All recipes](recipes/items/) — every recipe, one page each.

See [`RECIPES_CHANGELOG.md`](RECIPES_CHANGELOG.md) for the cookbook's update history.

## How it works

Independent scheduled agents, each a [Claude Code GitHub Action](https://github.com/anthropics/claude-code-base-action) run on a GitHub-hosted runner with web search and fetch enabled. Each posts to its own pinned tracking issue when a run produced changes — that's how update notifications land in your inbox. Runs are staggered across the weekend so no two agents edit the same files at once.

| Resource | Prompt | Workflow | Schedule (UTC) | Tracking issue |
|---|---|---|---|---|
| Catalog | [`AGENT.md`](AGENT.md) | [`curate.yml`](.github/workflows/curate.yml) | Weekends — 7 slots, one category per slot (Sat 00/06/12/18, Sun 00/06/12) | "Catalog updates" |
| Guide | [`GUIDE_AGENT.md`](GUIDE_AGENT.md) | [`guide.yml`](.github/workflows/guide.yml) | Weekly, Sat 01:00 | "Guide updates" |
| Autonomous science | [`COSCIENTIST_AGENT.md`](COSCIENTIST_AGENT.md) | [`coscientist.yml`](.github/workflows/coscientist.yml) | Weekly, Sat 02:00 | "AI co-scientist updates" |
| Recipes | [`RECIPE_AGENT.md`](RECIPE_AGENT.md) | [`recipes.yml`](.github/workflows/recipes.yml) | Weekends — 7 slots, one subject area per slot (Sat 03/09/15/21, Sun 03/09/15) | "Recipes updates" |
| Verifier | [`VERIFIER_AGENT.md`](VERIFIER_AGENT.md) | [`verify.yml`](.github/workflows/verify.yml) | Mon/Wed/Fri 08:00 | "Verification updates" |

The **Verifier** keeps the catalog trustworthy rather than adding tools. Each run it takes a batch of catalog entries, confirms they still work (statically via registries/repos, plus a quarantined sandbox smoke-test job that never hands untrusted code to the agent), runs a security assessment, fixes broken entries (dead install commands, moved repos, stale availability), and stamps each page with graded `verification` and `security` badges. See [`VERIFIER_AGENT.md`](VERIFIER_AGENT.md) and [`VERIFIER_CHANGELOG.md`](VERIFIER_CHANGELOG.md).

Two supporting workflows run on their own schedules: [`index.yml`](.github/workflows/index.yml) rebuilds the searchable knowledge-base index (daily 10:30 and on every content push), and [`digest.yml`](.github/workflows/digest.yml) posts a single weekly summary (Sun 18:00) to the **Weekly digest** issue.

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
gh workflow run recipes.yml                      # whole cookbook
gh workflow run recipes.yml -f scope=chemistry   # one subject area
gh workflow run recipes.yml -f scope=literature-triage  # one problem class
gh workflow run verify.yml                        # re-verify aging catalog entries
gh workflow run verify.yml -f scope=bootstrap     # verify unstamped entries first
gh workflow run digest.yml                        # post a weekly digest now
gh workflow run index.yml                          # rebuild the knowledge-base index
```

## One-time setup

1. Add an `ANTHROPIC_API_KEY` repository secret (**Settings → Secrets and variables → Actions**).
2. Enable GitHub Pages from the `main` branch root (**Settings → Pages → Source: Deploy from a branch → main / (root)**).
3. Subscribe to the **Weekly digest** issue (opened by the `digest.yml` workflow on its first run) for one weekly summary email — or watch the repo, or the per-section **Catalog updates**, **Guide updates**, **AI co-scientist updates**, **Recipes updates**, and **Verification updates** issues, for finer-grained notifications.
