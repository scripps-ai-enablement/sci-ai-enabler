# Autonomous science

A tracker of **autonomous AI scientist systems** — named software agents that, with meaningful autonomy, perform the core work of science: **hypothesis generation, experiment design, and analysis**. Manuscript writing is treated as a downstream subcomponent, not a peer stage; systems whose only function is to draft papers are out of scope.

Maintained by a scheduled Claude curator. See the top-level [README](../README.md) and [`COSCIENTIST_AGENT.md`](../COSCIENTIST_AGENT.md) for how this is produced, and [`COSCIENTIST_CHANGELOG.md`](../COSCIENTIST_CHANGELOG.md) for the history.

_Last refreshed: pending first run._

## What's here

- [`summary.md`](summary.md) — a state-of-the-field synthesis (≤ 1200 words). Start here for the landscape view.
- [`entries.md`](entries.md) — the canonical listing of named systems, one block per system, with affiliation, lifecycle stages, autonomy level, validation, availability, and citations.

## Entry schema (in brief)

Each entry in `entries.md` records: affiliation, first-introduced date, lifecycle stages covered (Hypothesis / Experiment design / Analysis / Multi-stage, optionally + Writing as a secondary tag), autonomy level, domain focus, architectural approach, availability, validation, notable results, primary paper, code repo, and the local source PDF in [`../sources/`](../sources/). See [`COSCIENTIST_AGENT.md`](../COSCIENTIST_AGENT.md) for the canonical schema.

## Sources archive

PDFs of papers cited by entries live in [`../sources/`](../sources/) alongside `pdftotext`-generated `.txt` sidecars. [`../sources/manifest.json`](../sources/manifest.json) is the DOI-keyed dedup registry — the agent checks it before downloading anything new.
