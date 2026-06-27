---
title: Foldseek Structural Search (Claude Skill)
parent: All tools
grand_parent: Catalog
nav_order: 95
tool_type: Claude Skill
supplier: Google DeepMind
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-06-27
summary: "Submit a 3D protein structure (.pdb/.cif) and find structurally similar proteins across AFDB, PDB100, SwissProt, and more via the Foldseek API."
---

# Foldseek Structural Search (Claude Skill)

Take a protein 3D coordinate file and find structurally similar proteins across large structure databases, returning ranked matches with probability, coverage, E-value, and identity scores.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Google DeepMind](https://github.com/google-deepmind/science-skills) |
| **Availability** | GA |
| **Pricing** | Free / OSS skill (Apache-2.0 code, CC-BY-4.0 docs); Foldseek Search API is a public web service, no key |
| **Capabilities** | Read-only — Claude runs the skill's Python locally (`uv run`) and submits your structure to the Foldseek web API |

## How to install

The `google-deepmind/science-skills` collection follows the Agent Skills `SKILL.md` spec. The repo's primary `npx skills add` path targets Gemini/Antigravity; for Claude the followable path is a manual copy of the skill directory.

- **Claude Code / Claude Desktop** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/google-deepmind/science-skills
  cp -r science-skills/skills/foldseek_structural_search ~/.claude/skills/
  cp -r science-skills/skills/scienceskillscommon ~/.claude/skills/
  ```
  (The skill imports shared helpers from `scienceskillscommon` — copy it too.)
- **Prerequisite** — the skill runs its `scripts/search.py` via `uv run`; install `uv` first if absent: `curl -LsSf https://astral.sh/uv/install.sh | sh`. Python deps install into an isolated environment on first run.

## What it does

Submits a structure to the [Foldseek](https://search.foldseek.com/) web search API and interprets the hits:

- Accepts a physical coordinate file (`.cif`, `.mmcif`, or `.pdb`) — it will **not** accept a bare sequence, gene name, or accession.
- Searches a chosen target database from the allowlist: `afdb50`, `afdb-swissprot`, `pdb100`, `BFVD`, `mgnify_esm30`, `cath50`, `gmgcl_id`, `bfmd`, `afdb-proteome`.
- Writes two outputs: a JSON file with the full API results for downstream analysis and a Markdown file with a formatted match table.
- Interprets matches via probability, query coverage, E-value, and sequence identity to infer likely function from target annotations.

**Primary use cases**: structural-homology search for an uncharacterized model (e.g., an AlphaFold prediction), function inference from structure, finding remote homologs that sequence search misses.

## Notes

Requires a real 3D structure file as input — pair it with [AlphaFold](alphafold.html) or the [RCSB PDB](pdb.html) skill to obtain coordinates first. The skill validates inputs strictly and halts on sequence-only input or an unsupported database. It calls the public Foldseek web service, so results depend on that service's availability; large queries are subject to its server-side limits. The `npx skills add google-deepmind/science-skills/` command documented upstream is oriented at Gemini/Antigravity (it writes to `~/.gemini/config/skills/`); for Claude, the manual copy into `~/.claude/skills/` shown above is the equivalent path. Foldseek itself is GPLv3 ([`steineggerlab/foldseek`](https://github.com/steineggerlab/foldseek)); this skill uses the hosted search API rather than a local Foldseek install.

## Sources

- [`google-deepmind/science-skills`](https://github.com/google-deepmind/science-skills)
- [`skills/foldseek_structural_search/SKILL.md`](https://github.com/google-deepmind/science-skills/blob/main/skills/foldseek_structural_search/SKILL.md)
- [Foldseek Search](https://search.foldseek.com/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=foldseek-structural-search&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ffoldseek-structural-search.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
