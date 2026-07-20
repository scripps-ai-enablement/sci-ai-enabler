---
title: UniBind TF Binding Sites (Claude Skill)
parent: All tools
grand_parent: Catalog
nav_order: 290
tool_type: Claude Skill
supplier: Google DeepMind
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-20
claude_science: true
verification: degraded
verified_on: 2026-07-20
verification_note: "repo + unibind_database skill dir resolve on google-deepmind/science-skills; replaced a stale scienceskillscommon copy line (that dir no longer exists) with the uv skill the SKILL.md actually requires"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier google-deepmind, Apache-2.0 code, maintained (pushed 2026-07-07, 2458 stars), keyless public UniBind API, no OSV advisories"
summary: "Query UniBind for experimentally validated transcription-factor binding sites; download BED/FASTA coordinates by species, cell line, or TF."
---

# UniBind TF Binding Sites (Claude Skill)

Query UniBind for experimentally validated, ChIP-seq-derived transcription-factor binding sites and download their coordinates for local analysis.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Google DeepMind](https://github.com/google-deepmind/science-skills) |
| **Availability** | GA |
| **Pricing** | Free / OSS skill (Apache-2.0 code, CC-BY-4.0 docs); UniBind API is public, no key |
| **Capabilities** | Read-only — Claude runs the skill's Python locally (`uv run`) against the UniBind REST API |
| **Verified** | degraded · 2026-07-20 — dir resolves; fixed a stale scienceskillscommon copy line |
| **Security** | cleared · 2026-07-20 — provenance matches google-deepmind, Apache-2.0, maintained, keyless public API, no OSV advisories |

## How to install

The `google-deepmind/science-skills` collection follows the Agent Skills `SKILL.md` spec. The repo's primary `npx skills add` path targets Gemini/Antigravity; for Claude the followable path is a manual copy of the skill directory.

- **Claude Code / Claude Desktop** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/google-deepmind/science-skills
  cp -r science-skills/skills/unibind_database ~/.claude/skills/
  cp -r science-skills/skills/uv ~/.claude/skills/
  ```
  (The `SKILL.md` requires the bundled `uv` skill for its setup — copy it too.)
- **Prerequisite** — the skill runs its Python helpers via `uv run`; install `uv` first if absent: `curl -LsSf https://astral.sh/uv/install.sh | sh`. `jq` is recommended for parsing large JSON responses. Python deps install into an isolated environment on first run.

## What it does

Wraps the UniBind REST API — a curated repository of direct TF–DNA interactions across 9 species, integrating ChIP-seq peaks with JASPAR profiles via the DAMO framework:

- List species, collections, cell lines, and transcription factors
- Filter/retrieve datasets by organism, TF name, cell line, or data source
- Download binding-site coordinates in BED or FASTA
- Retrieve dataset metadata

It is for dataset discovery and bulk coordinate download, not for querying specific intervals, genes, or motif models.

**Primary use cases**: retrieving validated TF binding-site sets, downstream peak/enrichment analysis, building TF-regulation datasets.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Regulation* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

No API key required, but users must review the UniBind terms at [unibind.uio.no](https://unibind.uio.no/) before use. Complements the catalogued JASPAR skill (`jaspar-database.md`), which provides the motif models UniBind integrates. The `npx skills add google-deepmind/science-skills/` command documented upstream is oriented at Gemini/Antigravity (it writes to `~/.gemini/config/skills/`); for Claude, the manual copy into `~/.claude/skills/` shown above is the equivalent path.

## Sources

- [`google-deepmind/science-skills`](https://github.com/google-deepmind/science-skills)
- [`skills/unibind_database/SKILL.md`](https://github.com/google-deepmind/science-skills/blob/main/skills/unibind_database/SKILL.md)
- [UniBind](https://unibind.uio.no/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=unibind-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Funibind-database.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
