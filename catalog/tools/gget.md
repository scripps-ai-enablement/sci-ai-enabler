---
title: gget (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology]
last_verified: 2026-07-25
verification: works
verified_on: 2026-07-20
verification_note: "repo and skills/gget dir resolve on K-Dense-AI/scientific-agent-skills"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier K-Dense-AI, MIT repo wrapping the gget library, maintained (pushed 2026-07-15), no OSV advisories"
summary: Claude skill wrapping the gget command-line / Python tool for fast unified queries against Ensembl, UniProt, NCBI, PDB, COSMIC, and other genomics databases.
---

# gget (Claude Skill)

Claude skill that teaches the gget unified API for querying 20+ genomics databases from a single Python or command-line interface.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only — queries public databases via gget |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches K-Dense-AI, MIT repo, maintained, no OSV advisories |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/genomics-bioinformatics/databases/gget-genomic-databases` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
<!-- alt-install:gget-mcp -->
- **Also available as an MCP server** ([`longevity-genie/gget-mcp`](https://github.com/longevity-genie/gget-mcp), MIT, PyPI `gget-mcp`) — exposes gget's functions as discrete MCP tools rather than as a skill; no API key. Register with Claude Code (stdio — Claude Code launches the process itself, so don't run it separately):
  ```
  claude mcp add --transport stdio gget-mcp -- uvx --from gget-mcp@latest stdio
  ```
  Or with Claude Desktop, add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "gget-mcp": { "command": "uvx", "args": ["--from", "gget-mcp@latest", "stdio"] }
    }
  }
  ```
  (Requires [uv](https://docs.astral.sh/uv/); use `uvx --from gget-mcp@latest server` instead of `stdio` for streamable-HTTP transport.)
<!-- /alt-install:gget-mcp -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `gget` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/gget ~/.claude/skills/
  pip install gget
  ```

## What it does

Recipes for gget commands against:

- Ensembl — gene information, sequences, orthologs, variants
- UniProt — protein sequences and annotations
- NCBI — BLAST searches, gene information
- RCSB PDB — protein structures
- COSMIC — cancer mutations
- Other curated databases through a single Python/CLI interface

Includes batch-query support, pandas DataFrame integration, and result formatting.

**Primary use cases**: Quick gene lookups, sequence retrieval, variant annotation, orthology checks, protein structure access without per-database API setup.

## Notes

Useful when a workflow needs heterogeneous lookups (gene → sequence → ortholog → structure) without orchestrating separate database clients. For dedicated UniProt or PDB workflows, the standalone MCP servers expose more specialised tooling.

Two packagings of the same underlying gget library are offered above: the K-Dense/SciAgent **skills** (procedural recipes Claude follows in local Python) and the `longevity-genie/gget-mcp` **MCP server** (gget functions exposed as discrete tools — `gget_search`, `gget_info`, `gget_seq`, `gget_ref`, `gget_blast`, `gget_blat`, `gget_muscle`, `gget_archs4`, `gget_enrichr`, `gget_pdb`, `gget_alphafold`, `gget_cosmic`, `gget_cellxgene`). Pick the MCP path if you want Claude to call gget mid-conversation; pick a skill if you prefer scripted, reproducible runs.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/gget/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/gget/SKILL.md)
- [`longevity-genie/gget-mcp`](https://github.com/longevity-genie/gget-mcp)
- [gget documentation](https://pachterlab.github.io/gget/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=gget&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fgget.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
