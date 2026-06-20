---
title: AlphaGenome Single-Variant Analysis (Claude Skill)
parent: All tools
grand_parent: Catalog
nav_order: 5
tool_type: Claude Skill
supplier: Google DeepMind
availability: Preview
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-20
summary: "Predict non-coding variant effects on expression, chromatin accessibility, histone marks, splicing, and TF binding via the AlphaGenome API."
---

# AlphaGenome Single-Variant Analysis (Claude Skill)

Predict how a non-coding genetic variant changes gene expression, chromatin accessibility, histone marks, splicing, and transcription-factor binding using the AlphaGenome API.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Google DeepMind](https://github.com/google-deepmind/science-skills) |
| **Availability** | Preview — AlphaGenome API is research-preview (signup-gated) |
| **Pricing** | Free / OSS skill (Apache-2.0 code, CC-BY-4.0 docs); AlphaGenome API free for non-commercial use, key required |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (`uv run`), calling the AlphaGenome API |

## How to install

The `google-deepmind/science-skills` collection follows the Agent Skills `SKILL.md` spec. The repo's primary `npx skills add` path targets Gemini/Antigravity; for Claude the followable path is a manual copy of the skill directory.

- **Claude Code / Claude Desktop** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/google-deepmind/science-skills
  cp -r science-skills/skills/alphagenome_single_variant_analysis ~/.claude/skills/
  cp -r science-skills/skills/scienceskillscommon ~/.claude/skills/
  ```
  (The skill imports shared helpers from `scienceskillscommon` — copy it too.)
- **Set the API key** — sign up at [deepmind.google.com/science/alphagenome](https://deepmind.google.com/science/alphagenome/), accept the terms, then:
  ```
  echo "ALPHAGENOME_API_KEY=<your-key>" >> ~/.env
  ```
  (replace `<your-key>` with the key from the AlphaGenome console).
- **Prerequisite** — the skill runs all Python via `uv run`; install `uv` first if absent: `curl -LsSf https://astral.sh/uv/install.sh | sh`. The skill installs its own Python deps (pandas, numpy, AlphaGenome client) into an isolated environment on first run.

## What it does

Evaluates a single variant (in `chr:pos:ref>alt` format) against AlphaGenome's predicted molecular phenotypes: RNA-seq expression, DNASE chromatin accessibility, ChIP histone marks, and transcription-factor binding. Helper scripts:

- `lookup_gene_info.py` — gene/transcript lookup via a local GTF (no external call)
- `resolve_ontology_terms.py` — map biological terms to UBERON/CL tissue and cell-type ontology IDs
- `visualize_variant_effects.py` — reference vs. alternate tracks and splicing visualizations
- `analyze_ism.py` — in-silico mutagenesis sequence logos
- `interpret_splicing.py` — quantitative splicing-disruption analysis

**Primary use cases**: non-coding variant effect prediction, regulatory/enhancer/promoter variant interpretation, splicing-disruption analysis.

## Notes

Requires an `ALPHAGENOME_API_KEY` and acceptance of the AlphaGenome terms before first use; the API is a research preview for non-commercial use. The skill resolves genes offline from a local GTF and prohibits direct external gene-lookup API calls. The `npx skills add google-deepmind/science-skills/` command documented upstream is oriented at Gemini/Antigravity (it writes to `~/.gemini/config/skills/`); for Claude, the manual copy into `~/.claude/skills/` shown above is the equivalent path. AlphaGenome the model itself (weights) is out of scope; this entry is the installable skill wrapper around its hosted API.

## Sources

- [`google-deepmind/science-skills`](https://github.com/google-deepmind/science-skills)
- [`skills/alphagenome_single_variant_analysis/SKILL.md`](https://github.com/google-deepmind/science-skills/blob/main/skills/alphagenome_single_variant_analysis/SKILL.md)
- [AlphaGenome (Google DeepMind)](https://deepmind.google.com/science/alphagenome/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=alphagenome&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Falphagenome.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
