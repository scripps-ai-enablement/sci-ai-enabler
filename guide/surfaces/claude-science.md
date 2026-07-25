---
title: Claude Science
parent: Claude surfaces
grand_parent: Guide
nav_order: 6
---

# Claude Science

> A standalone research workbench app — the non-coding-but-technical counterpart to Claude Code, aimed at running analyses, searching scientific databases, and keeping a reproducible trail from data to manuscript.

## What it is

Claude Science is a desktop app for researchers that you download from `claude.com/science`. One lead agent plans your work, spawns specialist and reviewer sub-agents, and calls curated skills and database connectors on your behalf. It ships with 60+ skills for genomics, single-cell, proteomics, structural biology, and cheminformatics, and connectors to databases like UniProt, PDB, Ensembl, ClinVar, ChEMBL, and GEO. It runs the same general-purpose models everyone else uses (the current Opus and Sonnet lines) — no special biology model or gating. Every figure carries the exact code, environment, and message history that produced it.

## When to use it

- Literature review, multi-step analysis, or figure generation over scientific data.
- Computational biology / drug-discovery workflows that touch curated databases.
- Work that must be reproducible and citation-checked, not a scrolling chat.
- You want the [Claude Code](claude-code.html) working style but for science, not software.
- You need native rendering of proteins, structures, alignments, or genomic tracks.

## How to install / enable

- Download from `https://claude.com/science`:
  - **Mac (Apple Silicon)** or **Mac (Intel)** — DMG installer
  - **Linux** — downloadable executable
  - Windows is not supported.
- Sign in with your Claude account. Beta is open to **Pro, Max, Team, and Enterprise** plans — no enterprise vetting.
- You can also run it remotely over SSH or on an HPC login node.

## Common pitfalls

- It's a separate app, not a mode inside Claude.ai or Claude Code — download it explicitly.
- The reviewer/fact-checker agent is the same model checking itself, not an independent source of truth — verify important citations and numbers yourself.
- Beta: features and skill sets are still changing.
- Windows users have no native client yet; use SSH into a Mac/Linux host.

## See also

- [Skills](../skills.html) and [Connectors](../connectors.html) — the components Claude Science orchestrates.
- [Slash commands and subagents](../advanced/slash-commands.html) — the specialist/reviewer agent pattern.
- [Reproducible, provenance-tracked AI analysis](../advanced/reproducibility.html) — the discipline Claude Science bakes in.
- [Claude Code](claude-code.html) — the software-engineering sibling surface.

## Sources

- [Claude Science app landing](https://claude.com/science) — Anthropic product page; verified 2026-07-11 (this run) — DMG / Linux downloads, macOS + Linux only (no Windows), beta status, reproducibility tracking, native rendering.
- [Claude Science, an AI workbench for scientists](https://www.anthropic.com/news/claude-science-ai-workbench) — Anthropic news; published 2026-06-30; verified 2026-07-11 (this run) — standalone app at `claude.com/science`, beta on macOS/Linux for Pro/Max/Team/Enterprise, 60+ skills, database connectors (UniProt/PDB/Ensembl/Reactome/ClinVar/ChEMBL/GEO), specialist + reviewer agents, BioNeMo integration, per-figure code+environment+history reproducibility.
- [Anthropic releases Claude Science](https://www.statnews.com/2026/06/30/anthropic-release-claude-science-ceo-dario-amodei/) — STAT News; published 2026-06-30 — beta July 1 for all paid subscribers, same underlying models (no biology-specific model), builds on Claude for Life Sciences.
