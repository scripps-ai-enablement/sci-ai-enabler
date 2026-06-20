---
title: GTEx Expression Database (Claude Skill)
parent: All tools
grand_parent: Catalog
nav_order: 110
tool_type: Claude Skill
supplier: Google DeepMind
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-20
summary: "Query the GTEx Portal for median RNA expression (TPM) across 54 human tissues and eQTLs linking variants to gene expression."
---

# GTEx Expression Database (Claude Skill)

Retrieve quantitative tissue-level RNA expression and expression-QTL data from the GTEx (Genotype-Tissue Expression) Project across 54 non-diseased human tissues.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Google DeepMind](https://github.com/google-deepmind/science-skills) |
| **Availability** | GA |
| **Pricing** | Free / OSS skill (Apache-2.0 code, CC-BY-4.0 docs); GTEx Portal API is public, no key |
| **Capabilities** | Read-only — Claude runs the skill's Python locally (`uv run`) against the GTEx Portal API |

## How to install

The `google-deepmind/science-skills` collection follows the Agent Skills `SKILL.md` spec. The repo's primary `npx skills add` path targets Gemini/Antigravity; for Claude the followable path is a manual copy of the skill directory.

- **Claude Code / Claude Desktop** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/google-deepmind/science-skills
  cp -r science-skills/skills/gtex_database ~/.claude/skills/
  cp -r science-skills/skills/scienceskillscommon ~/.claude/skills/
  ```
  (The skill imports shared helpers from `scienceskillscommon` — copy it too.)
- **Prerequisite** — the skill runs its `scripts/gtex_cli.py` via `uv run`; install `uv` first if absent: `curl -LsSf https://astral.sh/uv/install.sh | sh`. Python deps install into an isolated environment on first run.

## What it does

Queries the GTEx Portal API V2 for transcriptomics across 54 tissue sites:

- Gene symbol → GENCODE ID mapping
- Median TPM expression retrieval across tissues
- Top-tissue identification by expression level
- eQTL discovery for a specific gene
- Regional eQTL queries within a chromosomal window

**Primary use cases**: tissue-specific expression lookup, eQTL annotation of variants, prioritizing candidate regulatory variants by tissue.

## Notes

No API key required, but users must acknowledge the GTEx Portal license terms before first use; built-in rate limiting is enforced by the wrapper scripts. Covers non-diseased adult tissues and mRNA abundance only — not protein expression. The `npx skills add google-deepmind/science-skills/` command documented upstream is oriented at Gemini/Antigravity (it writes to `~/.gemini/config/skills/`); for Claude, the manual copy into `~/.claude/skills/` shown above is the equivalent path.

## Sources

- [`google-deepmind/science-skills`](https://github.com/google-deepmind/science-skills)
- [`skills/gtex_database/SKILL.md`](https://github.com/google-deepmind/science-skills/blob/main/skills/gtex_database/SKILL.md)
- [GTEx Portal](https://www.gtexportal.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=gtex-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fgtex-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
