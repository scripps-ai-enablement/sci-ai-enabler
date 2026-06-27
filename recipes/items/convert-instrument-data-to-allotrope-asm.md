---
title: Convert raw analytical instrument data to Allotrope ASM JSON
parent: All recipes
grand_parent: Recipes
nav_order: 6
problem_class: Workflow automation
subject_areas: [Chemistry, Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-27
summary: Drop a raw instrument file (cell counter, plate reader, HPLC, qPCR) onto Claude Code and get back valid Allotrope Simple Model JSON, a flattened CSV for LIMS, and a standalone Python parser script.
---

# Convert raw analytical instrument data to Allotrope ASM JSON

Hand Claude Code a vendor-format file from a cell counter, plate reader, HPLC, mass spectrometer, or qPCR instrument; get back a strict-validated Allotrope Simple Model (ASM) JSON, a flattened 2D CSV ready for LIMS ingestion, and an exportable Python parser that a data engineer can put behind a pipeline.

| | |
|---|---|
| **Problem class** | Workflow automation |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Every analytical instrument writes its own file format — Beckman Vi-CELL counters emit one CSV layout; Agilent HPLCs emit another; Tecan and Molecular Devices plate readers each emit their own XML / Excel hybrids; NanoDrop spreadsheets, BMG OMEGA exports, Roche LightCycler `.ixo` packages, Bio-Rad CFX `.pcrd`. A pharma or biotech lab pipes those into LIMS, an ELN, or a data lake — and the glue is a long tail of one-off parsers that drift as vendors push firmware updates. The [Allotrope Foundation](https://www.allotrope.org/asm) standardised this with the Allotrope Simple Model (ASM): a JSON-LD schema per technique (flow cytometry, plate-reader, HPLC-DAD, qPCR, …) with ontology-anchored field names and explicit raw-vs-derived data separation.

The work that has to happen on every new file: identify the instrument and vendor, pick the right parser, map fields into the right ASM section (raw measurements into `measurement-document`; derived values into `calculated-data-aggregate-document` with `data-source-aggregate-document` traceability), validate against the ASM schema, and emit either ASM JSON (for an ASM-aware sink) or a flattened CSV (for everything else). Solved looks like: drop the file, get JSON + CSV + a re-usable parser script, no hand editing.

## Recommended approach

1. **Install the [instrument-data-to-allotrope skill](../../catalog/tools/instrument-data-to-allotrope.html)** — bundled in the Anthropic `life-sciences` marketplace and also inside the `bio-research` plugin:

   ```
   /plugin marketplace add anthropics/life-sciences
   /plugin install instrument-data-to-allotrope@life-sciences
   pip install allotropy
   ```

   Confirm with `/plugin list`. The skill bundles four scripts — `convert_to_asm.py`, `flatten_asm.py`, `export_parser.py`, `validate_asm.py` — plus references for the 40+ supported instruments.

2. **Drop the raw file and ask for auto-detection.** A minimal prompt:

   ```
   Convert raw/viCell_Results.csv to Allotrope ASM JSON. Auto-detect
   the instrument, report your detection confidence, run the native
   `allotropy` parser, and write:
     out/viCell_Results.asm.json   (full ASM JSON-LD)
     out/viCell_Results.flat.csv   (flattened 2D form for LIMS)
   Then run strict ASM schema validation on the JSON and print the
   validation result (pass / list of failed fields).
   ```

   The skill detects the vendor signature from the file header and reports a confidence score (the published Vi-CELL example reaches 95%). If confidence is low or the instrument is unsupported, the skill falls back to the flexible / PDF-table parser — flag this in your downstream metadata because field completeness drops.

3. **Pin the vendor explicitly for batch jobs.** Auto-detection is convenient for one-off files; for a directory of 50 plate-reader exports, pass the vendor enum directly so you do not pay the detection cost 50 times:

   ```
   For every *.xlsx under raw/plate_runs/2026-Q2/, call
   allotrope_from_file(path, Vendor.MOLDEV_SOFTMAX_PRO) and
   write the ASM JSON next to the source file (.asm.json suffix).
   On any parse failure, append a row to logs/parse_failures.csv with
   path, vendor, error class, error message. Print a final summary:
   N parsed / N failed.
   ```

   `Vendor` enums match the names in the `allotropy.parser_factory` module; see [`supported_instruments.md`](https://github.com/anthropics/life-sciences) in the skill bundle for the canonical list.

4. **Generate a stand-alone parser for production.** When a workflow stabilises, ask the skill to emit a self-contained script your data engineer can deploy without the skill in the loop:

   ```
   Generate a stand-alone Python parser for Beckman Vi-CELL BLU files.
   - Input: a Vi-CELL CSV path
   - Output: ASM JSON + flattened CSV, written next to the input
   - Include sample input and expected output as docstrings
   - Document all assumptions and the allotropy version used
   - Save to pipelines/parsers/vicell_blu_parser.py
   Also write a parallel notebook version at
   notebooks/vicell_blu_parser.ipynb that loads a sample file and
   shows the ASM structure.
   ```

5. **Validate the raw-vs-derived split before shipping.** The ASM model's single most-violated rule is mixing raw measurements with calculated values in the same document. Confirm before downstream ingestion:

   ```
   Run validate_asm on out/viCell_Results.asm.json with strict=True.
   Print any field that is in `calculated-data-aggregate-document`
   but lacks a `data-source-aggregate-document` traceability link,
   and any field in `measurement-document` that looks like a derived
   value (units of %, ratios, normalised values).
   ```

## Why this assembly

Rung 2 of the simplicity ladder. The work is mechanical — auto-detect vendor, dispatch to the right `allotropy` parser, emit JSON and CSV, validate — but every step needs vendor-specific knowledge of where fields live and the ASM-vs-vendor field-name map. The Anthropic-shipped skill bundles 40+ instrument mappings, the strict-validator, and the raw/derived field-classification reference. Plain Claude Code can write a parser from `allotropy` source, but it re-derives the field mapping every session and skips the ASM-validation step by default. A multi-tool harness or autonomous system adds nothing — there is no scientific decision to make, only a format transform.

## Availability

Fully open. The skill and its supporting `allotropy` Python library are MIT-licensed. The Allotrope Simple Model schemas themselves are open, ontology-anchored (Allotrope Foundation Ontologies, BAO, UO, IAO). No subscription, no cloud account; everything runs locally against your raw files.

## Compute requirements

Laptop. Per-file parse times are sub-second for typical instrument outputs (≤10 MB CSV / Excel). The strict-validator and the JSON-Schema check are similarly fast. RAM is the file size plus a few megabytes for the ASM in-memory representation. The only step that benefits from parallelism is batch conversion of large directories — use `n_jobs=-1` in the prompt.

## Evidence

Reported. The skill is shipped and documented by Anthropic as part of the [Claude for Life Sciences launch (October 2025)](https://www.anthropic.com/news/claude-for-life-sciences) and is bundled inside the [`bio-research` plugin](https://claude.com/plugins/bio-research). The Anthropic [Getting Started with Claude for Life Sciences](https://claude.com/resources/tutorials/getting-started-with-claude-for-life-sciences) tutorial walks through a worked Vi-CELL example end-to-end (detect → parse → flatten → validate → emit parser script), and the [GUVI step-by-step guide](https://www.guvi.in/blog/master-allotrope-skill-for-instrument/) reproduces the workflow on a public plate-reader CSV.

Underneath the skill, the [`allotropy`](https://github.com/Benchling-Open-Source/allotropy) library that does the parsing is the Benchling Open Source reference implementation that the Allotrope Foundation cites in its [ASM documentation](https://www.allotrope.org/asm); it is in production use across pharma data engineering, with 40+ vendor parsers maintained as of 2026. No peer-reviewed head-to-head benchmark of "Claude + this skill" against a hand-written parser is known — the agent loop adds discoverability, validation, and the emitted-parser handoff, not new parsing capability.

## Alternatives considered

- **Plain Claude Code + `allotropy` library, no skill.** Works for one-off files where you already know the vendor. Reach for it when a single CSV needs converting and you can name the `Vendor` enum yourself. The skill's value is the auto-detect, the strict-validation, and the parser-export step.
- **Vendor LIMS connectors (Benchling, LabVantage, Sapio).** Closed-source and tied to a LIMS contract. Use them when your sink is the same vendor's LIMS and you have the licence; the skill's value is the agent-driven ad-hoc workflow when no vendor connector exists or when you need to migrate between LIMS systems.
- **A hand-written Python parser per instrument.** Maintainable but a permanent maintenance debt as vendors push firmware updates. Pin to the skill's `export_parser.py` output and version-control the generated script — re-generate it when the skill bumps `allotropy` versions.

## See also

- [instrument-data-to-allotrope (Claude Skill)](../../catalog/tools/instrument-data-to-allotrope.html)
- [bio-research (Anthropic plugin)](../../catalog/tools/bio-research.html) — bundles this skill alongside the other Claude for Life Sciences components.
- [Draft a Phase 2/3 clinical-trial protocol from an indication brief](draft-phase23-clinical-trial-protocol.html) — sibling Anthropic Healthcare workflow recipe.

## Sources

- [Anthropic — Claude for Life Sciences launch](https://www.anthropic.com/news/claude-for-life-sciences) — published 2025-10-20; verified 2026-06-01 (this run).
- [Anthropic — Getting Started with Claude for Life Sciences (tutorial)](https://claude.com/resources/tutorials/getting-started-with-claude-for-life-sciences) — verified 2026-06-01 (this run).
- [`anthropics/life-sciences` marketplace — instrument-data-to-allotrope](https://github.com/anthropics/life-sciences) — verified 2026-06-01 (this run).
- [Skill listing — playbooks.com](https://playbooks.com/skills/anthropics/life-sciences/instrument-data-to-allotrope) — verified 2026-06-01 (this run).
- [Allotrope Foundation — ASM overview](https://www.allotrope.org/asm) — verified 2026-06-01 (this run).
- [`Benchling-Open-Source/allotropy`](https://github.com/Benchling-Open-Source/allotropy) — underlying parser library; verified 2026-06-01 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=convert-instrument-data-to-allotrope-asm&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fconvert-instrument-data-to-allotrope-asm.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
