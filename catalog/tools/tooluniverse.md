---
title: ToolUniverse
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Zitnik Lab (Harvard Medical School) · MIT Lincoln Laboratory
availability: GA
tool_categories: [All]
last_verified: 2026-05-24
summary: Harvard / MIT MCP server bundling 600+ vetted scientific tools — literature, chemistry, omics, clinical trials — for AI-scientist-style hypothesis exploration.
---

# ToolUniverse

MCP server developed by the Zitnik Lab at Harvard Medical School with MIT Lincoln Laboratory, exposing **600+ vetted scientific tools** spanning literature search, cheminformatics, omics, and clinical trial discovery. Designed as the tool backbone for AI-scientist workflows.

| | |
|---|---|
| **Type** | MCP server (also distributed as MCPB bundle and Claude.ai extension) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://zitniklab.hms.harvard.edu/); listed in `anthropics/life-sciences` marketplace |
| **Availability** | GA — PyPI `tooluniverse` 1.0.x, surfaced as an Anthropic Life Sciences connector at J.P. Morgan 2026 |
| **Pricing** | Free / OSS; some wrapped APIs require user-supplied keys (e.g., Azure OpenAI for AI-tool-search features) |
| **Capabilities** | Read/Write — most tools are read-only over public APIs; a few orchestrate analysis steps |

## How to install

- **Claude Code — direct stdio via `uvx`** (simplest; no environment to manage):
  ```
  claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
  ```
- **Claude Code — `anthropics/life-sciences` marketplace** (if you already use the marketplace):
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install tooluniverse@life-sciences
  ```
- **Claude Desktop — MCPB bundle**: download the `.mcpb` bundle from the [ToolUniverse releases page](https://github.com/mims-harvard/ToolUniverse/releases) and double-click to install via the Claude Desktop extensions UI.
- **Manual `uv` environment** (useful if you want a filtered tool subset or to pin a version):
  ```
  # 1) install uv (https://docs.astral.sh/uv/)
  # 2) create and populate a dedicated env (replace /abs/path/to/claude_toolu_env with a directory you choose — e.g., $HOME/.tooluniverse-env)
  mkdir -p /abs/path/to/claude_toolu_env
  uv --directory /abs/path/to/claude_toolu_env pip install tooluniverse
  # 3) register with Claude Code
  claude mcp add tooluniverse --scope local -- uv --directory /abs/path/to/claude_toolu_env run tooluniverse-smcp-stdio
  ```
  Filter to a research-focused subset with `--include-tools EuropePMC_search_articles,ChEMBL_search_similar_molecules,openalex_literature_search,search_clinical_trials` appended to the `tooluniverse-smcp-stdio` invocation.

## What it does

A single MCP surface that exposes 600+ tools covering:

- **Literature** — EuropePMC, OpenAlex, PubMed search and full-text retrieval
- **Chemistry / pharmacology** — ChEMBL, PubChem, drug-target lookups, similarity search
- **Omics & targets** — Open Targets, Ensembl, UniProt, gene/protein cross-references
- **Clinical trials & regulatory** — ClinicalTrials.gov search, FDA datasets
- **Knowledge graphs and ontologies** — disease, phenotype, pathway lookups

Includes an AI-powered tool-search facility that lets Claude pick the right tool from the catalogue at runtime rather than overwhelming the context window with 600 definitions at once.

**Primary use cases**: AI-scientist agents that need broad coverage; hypothesis generation and iterative refinement across literature → omics → chemistry → trials; comparing competing hypotheses by pulling evidence from multiple databases in one session.

## Notes

stdio transport when registered locally. Many wrapped APIs are public, but the AI-tool-search feature can be configured to use an LLM via environment variables (e.g., `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`). The MCPB bundle entry point is `tooluniverse-smcp-stdio`; the `uvx tooluniverse` shortcut is preferred for Claude Code because it doesn't require maintaining a separate env.

## Sources

- [ToolUniverse — Claude Code setup guide](https://zitniklab.hms.harvard.edu/bioagent/guide/building_ai_scientists/claude_code.html)
- [Anthropic tutorial — Using the ToolUniverse Extension in Claude](https://claude.com/resources/tutorials/using-the-tooluniverse-extension-in-claude)
- [`tooluniverse` on PyPI](https://pypi.org/project/tooluniverse/)
- [Democratizing AI scientists using ToolUniverse (arXiv:2509.23426)](https://arxiv.org/abs/2509.23426)
- [`anthropics/life-sciences` marketplace](https://github.com/anthropics/life-sciences)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
