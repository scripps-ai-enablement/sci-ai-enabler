---
title: Rowan
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill, MCP server
supplier: K-Dense / Rowan
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-06-10
summary: Cloud-native molecular modeling and medicinal-chemistry workflow platform, installable as a Claude Skill or an MCP server.
---

# Rowan

Rowan is a cloud-native molecular modeling and medicinal-chemistry workflow platform, installable either as a K-Dense Claude Skill (local Python) or as a standalone MCP server.

| | |
|---|---|
| **Type** | Claude Skill (K-Dense) · MCP server (`k-yenko/rowan-mcp`) |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) · [Rowan](https://labs.rowansci.com) (community OSS wrappers) |
| **Availability** | GA — Skill is part of the actively maintained K-Dense collection; MCP published on PyPI as `rowan-mcp` |
| **Pricing** | Free / OSS wrappers; Rowan API key required (free tier at labs.rowansci.com) |
| **Capabilities** | Read/Write — submits cloud compute workflows to the Rowan platform |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/structural-biology-drug-discovery/rowan` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `rowan` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/rowan ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.
- **Claude Code / Claude Desktop** — MCP server (`k-yenko/rowan-mcp`): the server runs as a **long-lived local HTTP/SSE service** — keep it running in its own terminal while Claude is connected (it is *not* a stdio server the client launches for you). Get a free API key at [labs.rowansci.com](https://labs.rowansci.com), then in one terminal:
  ```
  export ROWAN_API_KEY="your_api_key_here"
  uvx --from rowan-mcp rowan-mcp
  ```
  This boots an SSE endpoint at `http://127.0.0.1:6276/sse`. Leave it running. Then register the endpoint with Claude Code:
  ```
  claude mcp add --transport sse rowan http://127.0.0.1:6276/sse
  ```
  For Claude Desktop (no native SSE transport), add an `mcp-remote` proxy entry to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "rowan": {
        "command": "npx",
        "args": ["mcp-remote", "http://127.0.0.1:6276/sse"]
      }
    }
  }
  ```

## What it does

Rowan is a cloud-native molecular modeling and medicinal-chemistry workflow platform with a Python API. Use for pKa and macropKa prediction, conformer and tautomer ensembles, docking and analogue docking, protein-ligand cofolding, MSA generation, molecular dynamics, permeability, descriptor workflows, and related small-molecule or protein modeling tasks. Ideal for programmatic batch screening, multi-step chemistry pipelines, and workflows that would otherwise require maintaining local HPC/GPU infrastructure.

**Primary use cases**: pKa and macropKa prediction, conformer and tautomer ensembles, docking and analogue docking, protein-ligand cofolding, MSA generation, molecular dynamics, permeability, descriptor workflows, and related small-molecule or protein modeling tasks.

The `rowan-mcp` server exposes ~45 MCP tools over the same Rowan platform — workflow submitters (e.g. `submit_pka_workflow`, `submit_docking_workflow`), `molecule_lookup`, workflow-management tools (`retrieve_workflow`), and protein-management tools — so an MCP user gets the same compute surface without writing Python.

## Notes

The **Skill** is distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server; the skill name to enable after install is `rowan`. The **MCP server** (`k-yenko/rowan-mcp`, PyPI `rowan-mcp`) is HTTP/SSE only, so it must stay running in a terminal for the duration of the session. Both paths require a Rowan API key (`ROWAN_API_KEY`; free tier at labs.rowansci.com). **Unverified —** the `rowan-mcp` repository does not publish a LICENSE file; confirm licensing before redistributing.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/rowan/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/rowan/SKILL.md)
- [`k-yenko/rowan-mcp`](https://github.com/k-yenko/rowan-mcp)
- [Rowan Labs](https://labs.rowansci.com)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=rowan&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Frowan.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
