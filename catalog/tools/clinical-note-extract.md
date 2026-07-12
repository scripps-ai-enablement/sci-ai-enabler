---
title: Clinical Note Extract (Anthropic Healthcare Plugin)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Anthropic
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-07-12
summary: Anthropic Claude skill that extracts structured, validated records from unstructured clinical notes with span-level provenance and explicit null handling.
---

# Clinical Note Extract (Anthropic Healthcare Plugin)

Anthropic-published skill from the `anthropics/healthcare` plugin marketplace that turns unstructured clinical text into structured, validated records where every value is traced back to its source span.

| | |
|---|---|
| **Type** | Claude Skill (shipped inside the `healthcare` Claude Code plugin) |
| **Supplier** | [Anthropic](https://github.com/anthropics/healthcare) |
| **Availability** | GA |
| **Pricing** | Free / OSS — provided under Anthropic's terms of service |
| **Capabilities** | Read/Write — reads clinical notes, writes structured records |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/healthcare
  /plugin install healthcare@healthcare
  ```
  The `clinical-note-extract` skill is bundled inside the consolidated `healthcare` plugin (the older standalone plugins are now deprecated in favor of `healthcare@healthcare`). Invoke it as `/healthcare:clinical-note-extract` (namespaced by the plugin — not a bare `/clinical-note-extract`).
- **Claude.ai / Claude Desktop** — the healthcare plugin's skills load wherever the marketplace plugin is enabled.

## What it does

Processes one or many notes through a four-step pipeline — schema definition, extraction, validation, reporting — and emits per-value records with:

- `value` — the extracted data.
- `span` — the verbatim source text supporting it.
- `presence` / `temporality` / `experiencer` — assertion metadata.
- `null_reason` — an explanation whenever a field is absent (nulls are documented, not omitted).
- `unit` — measurement units where applicable.

Validation is deterministic (terminology lookups, range checks, date validation) and appends verification status; any span that cannot be confirmed against the source note is explicitly flagged.

**Primary use cases**: Auditable chart abstraction, clinical registry building, structured EHR data extraction with provenance.

## Notes

Its SKILL.md front-matter names the skill `clinical-note-extract-skill`, but the directory and plugin command are `clinical-note-extract`. Distinct from the K-Dense `clinical-reports` skill (report authoring) — this one is a structured-extraction/abstraction tool with span-level citations. Pairs with `icd10-cm` and `procedure-coding` for coding downstream of extraction.

## Sources

- [`anthropics/healthcare`](https://github.com/anthropics/healthcare)
- [`plugins/healthcare/skills/clinical-note-extract/SKILL.md`](https://github.com/anthropics/healthcare/blob/main/plugins/healthcare/skills/clinical-note-extract/SKILL.md)
- [Marketplace manifest](https://raw.githubusercontent.com/anthropics/healthcare/main/.claude-plugin/marketplace.json)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=clinical-note-extract&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fclinical-note-extract.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
