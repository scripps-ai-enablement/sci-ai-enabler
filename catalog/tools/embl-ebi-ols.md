---
title: EMBL-EBI OLS (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Google DeepMind
availability: GA
tool_categories: [All]
last_verified: 2026-06-27
summary: "Resolve and navigate biomedical ontology terms (GO, MONDO, HP, CHEBI, CL, UBERON, EFO, …) across 250+ ontologies via the EMBL-EBI Ontology Lookup Service."
---

# EMBL-EBI OLS (Claude Skill)

Look up biomedical ontology terms, definitions, and hierarchies across 250+ ontologies through the EMBL-EBI Ontology Lookup Service — resolve a label to an ID, walk parent/child relationships, and find the canonical term for a concept.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Google DeepMind](https://github.com/google-deepmind/science-skills) |
| **Availability** | GA |
| **Pricing** | Free / OSS skill (Apache-2.0 code, CC-BY-4.0 docs); the OLS API is a public EMBL-EBI web service, no key |
| **Capabilities** | Read-only — Claude runs the skill's Python locally (`uv run`) and queries the public OLS4 API |

## How to install

The `google-deepmind/science-skills` collection follows the Agent Skills `SKILL.md` spec. The repo's primary `npx skills add` path targets Gemini/Antigravity; for Claude the followable path is a manual copy of the skill directory.

- **Claude Code / Claude Desktop** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/google-deepmind/science-skills
  cp -r science-skills/skills/embl_ebi_ols ~/.claude/skills/
  cp -r science-skills/skills/scienceskillscommon ~/.claude/skills/
  ```
  (The skill imports shared helpers from `scienceskillscommon` — copy it too.)
- **Prerequisite** — the skill runs its utility script via `uv run`; install `uv` first if absent: `curl -LsSf https://astral.sh/uv/install.sh | sh`. Python deps install into an isolated environment on first run.

## What it does

Queries the [EMBL-EBI Ontology Lookup Service (OLS4)](https://www.ebi.ac.uk/ols4/) and interprets the results:

- **Term resolution** — retrieve a term's label, definition, synonyms, IRI, and OBO ID from a query, OBO ID, or IRI.
- **Hierarchy navigation** — parents, children, ancestors, and descendants of a term.
- **Property and individual lookups** within an ontology.
- **Autocomplete** suggestions for partial terms.
- **Ontology metadata and statistics** — version, term counts, and coverage per ontology.
- **Cross-ontology search** with filtering by ontology and relation type.

Covers 250+ ontologies including GO (Gene Ontology), MONDO, DOID (Disease Ontology), HP (Human Phenotype), CHEBI, CL (Cell Ontology), UBERON (anatomy), and EFO. Outputs are JSON.

**Primary use cases**: normalizing free-text concepts to ontology IDs, building controlled vocabularies, mapping phenotypes/diseases/anatomy/cell-types to canonical terms, enriching annotations with ontology hierarchy.

## Notes

The skill mandates use of its bundled utility script for all OLS API interactions — it instructs Claude never to call the API with raw `curl` or ad-hoc requests, which keeps queries within the skill's validated paths. It calls the public OLS4 service, so results depend on EMBL-EBI availability. The upstream `npx skills add google-deepmind/science-skills/` command is oriented at Gemini/Antigravity (it writes to `~/.gemini/config/skills/`); for Claude, the manual copy into `~/.claude/skills/` shown above is the equivalent path. Tagged `All`: ontology resolution is a cross-cutting need spanning every life-science domain.

## Sources

- [`google-deepmind/science-skills`](https://github.com/google-deepmind/science-skills)
- [`skills/embl_ebi_ols/SKILL.md`](https://github.com/google-deepmind/science-skills/blob/main/skills/embl_ebi_ols/SKILL.md)
- [EMBL-EBI Ontology Lookup Service](https://www.ebi.ac.uk/ols4/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=embl-ebi-ols&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fembl-ebi-ols.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
