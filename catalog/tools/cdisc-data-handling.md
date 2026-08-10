---
title: CDISC Data Handling (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-09
summary: "Read SDTM XPT files, derive ADaM datasets with traceability, apply TEAE conventions, and validate for FDA submission with Pinnacle 21 or CORE"
verification: works
verified_on: 2026-08-10
reviewed_on: 2026-08-10
security: caution
security_on: 2026-08-10
security_note: "GPTomics/bioSkills MIT skill code clean, but CDISC standards/Pinnacle 21 Enterprise are commercially licensed, data-use restriction only"
---

# CDISC Data Handling (bioSkills)

A Claude Code skill for taking raw CDISC SDTM tabulation data through to analysis-ready ADaM datasets and a Define-XML 2.1 submission package, with the conformance rules and traceability requirements stated at each layer.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — `pyreadstat`, `pandas`, `numpy` and the R packages `admiral`, `metacore`, `metatools`, `xportr` are separately installed OSS. **CDISC standards themselves require a CDISC membership or licence for some deliverables**, and **Pinnacle 21 Enterprise is a commercial product** (the free Community validator is a separate, more limited tool). CDISC **CORE** is the open-source rules engine. |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python and R), not as an MCP tool |
| **Verified** | works · 2026-08-10 |
| **Security** | caution · 2026-08-10 — MIT skill code clean, CDISC/Pinnacle 21 Enterprise data-use restriction only |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "clinical-biostatistics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/clinical-biostatistics/cdisc-data-handling ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the Python side on first use with `pip install "pyreadstat>=1.2" "pandas>=2.1" "numpy>=1.26"`; the ADaM-derivation route additionally needs R with `install.packages(c("admiral", "metacore", "metatools", "xportr"))`.

## What it does

Bridges raw CRF data → SDTM tabulation → ADaM analysis datasets → submission package:

- **Read submission formats** — parse SAS XPORT (`.xpt`) files with `pyreadstat` 1.2+ so variable labels and formats survive the round trip, plus plain CSV clinical extracts.
- **Join SDTM domains** — attach event-level domains (AE, EX, VS, LB, DS) to the subject-level DM spine, and handle SUPPQUAL / non-standard variables rather than silently dropping them.
- **Derive ADaM** — build the ADaM architecture (ADSL subject-level, BDS basic data structure, OCCDS occurrence data, ADTTE time-to-event) with baseline derivation, change-from-baseline, and analysis flags, preserving variable-level traceability back to SDTM.
- **Apply TEAE logic** — treatment-emergent adverse event windows per ICH E2A.
- **Validate and document** — run conformance checks and generate Define-XML 2.1 metadata for the submission.

Conventions and constraints the skill pins down:

| Item | Value |
|---|---|
| SAS XPT v5 variable name limit | 8 characters |
| SAS XPT v5 text value limit | 200 characters |
| Study day convention | first dose = Day 1; `ADY = (ADT − TRTSDT) + 1` (no day zero) |
| TEAE window, small molecules | 28–30 days post-treatment (ICH E2A; sponsor-defined) |
| TEAE window, biologics / mAbs | 60–90 days, for the extended half-life |
| TEAE window, cell and gene therapy | indefinite — lifelong monitoring expected |
| Define-XML | 2.1, required for studies starting on or after 15 March 2023 |
| Dataset-JSON | v1.1 (December 2024), the modern alternative to XPT v5 |
| Validation engines | Pinnacle 21 4.0+; CDISC **CORE** (open-source, YAML rule definitions) |

**Primary use cases**: preparing an analysis-ready ADaM package, validating SDTM conformance before submission, writing Define-XML metadata.

## Notes

The TEAE window is a **sponsor-defined** choice, not a fixed rule — the skill gives the modality-dependent ranges above as the defensible starting points and expects the choice to be stated in the SAP. Getting it wrong shifts events in and out of the safety analysis set.

**XPT v5 is still the FDA submission format, but not the only one.** The skill notes that FDA issued a notice in April 2025 regarding Dataset-JSON v1.1 as a modern replacement. Confirm the current requirement against the FDA Study Data Technical Conformance Guide for your submission date rather than relying on this page.

The 8-character variable-name and 200-character value limits of XPT v5 are the most common source of silent truncation when exporting derived ADaM datasets from Python or R — `xportr` exists specifically to enforce them at export time.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-clinical-biostatistics-cdisc-data`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/cdisc-data-handling`. Upstream directory: `clinical-biostatistics/cdisc-data-handling`.

**No MCP server over the CDISC Library is catalogued yet** — the skill works from files you already hold, and does not query CDISC controlled terminology over the network.

Complements [Trial Reporting](trial-reporting.html) (CONSORT-conformant analysis write-up), [Adaptive Designs](adaptive-designs.html), and [Missing Data Sensitivity](missing-data-sensitivity.html) (the estimand and imputation layer that consumes ADaM datasets).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-biostatistics/cdisc-data-handling/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/cdisc-data-handling/SKILL.md)
- [CDISC ADaM](https://www.cdisc.org/standards/foundational/adam) and [SDTM](https://www.cdisc.org/standards/foundational/sdtm)
- [CDISC CORE (open-source rules engine)](https://www.cdisc.org/core)
- [`pharmaverse/admiral`](https://pharmaverse.github.io/admiral/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cdisc-data-handling&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcdisc-data-handling.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
