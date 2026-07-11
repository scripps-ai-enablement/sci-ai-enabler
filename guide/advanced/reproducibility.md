---
title: Reproducible, provenance-tracked AI analysis
parent: Advanced
grand_parent: Guide
nav_order: 5
---

# Reproducible, provenance-tracked AI analysis

> Why the durable record of an AI-assisted analysis should be committed **code** plus a pinned environment and a provenance record — not a chat transcript — and how to make that the default.

## The principle

Using Claude with Skills and MCP servers is a fast, legitimate way to *do* an analysis. But a conversation is not a method. Six months on, a reviewer, a collaborator, or your future self needs to know exactly what was run, against which data and tool versions, and to be able to run it again and get the same answer. A scrolling chat — full of model choices that vary run to run — cannot carry that weight.

So treat the assistant as the author, not the record. **The chat produces an artifact; the artifact is what you keep, cite, and re-run.** Concretely, every analysis should leave behind three things under version control:

1. **Code** — a script (`analysis.py`) or notebook (`analysis.ipynb`) that performs the workflow end to end.
2. **A pinned environment** — `requirements.txt`, `environment.yml`, or a lockfile, with exact versions.
3. **A provenance record** — what ran, against what, when: tool/library/MCP-server versions, the external-database release or snapshot date, the model identity, the exact inputs, and a hash of the outputs.

## The pattern

A practical recipe for getting there from an interactive session:

- **Ask for the script, not just the answer.** "Write this as `analysis.py` that takes the input file and writes the outputs and a `provenance.json`" — then commit it. The result of running *that file* is the deliverable; the conversation was scaffolding.
- **Pin what you can.** Capture exact versions: `pip freeze > requirements.lock.txt`, or pin the specific Skill/MCP-server version. Record the model id you used.
- **Record what you can't.** Calls to live external services — Enrichr, Open Targets, UniProt, an MCP server, the model itself — are **not** byte-reproducible: libraries, indexes, and weights move. You cannot pin them, so capture the **release or snapshot date** and an accession or content hash. The goal is not to freeze the world; it is to make any divergence *visible* instead of silent.
- **Snapshot the outputs.** The saved tables/figures are the audit trail. Any written interpretation must cite only what appears in them — so the narrative can't drift from the data.
- **Make re-runnable the easy path.** A `.claude/commands/<verb-noun>.md` wrapper is a fine convenience, but understand what it is: it re-invokes the agent and can produce different code next time. It is a shortcut to *regenerate or re-run* the artifact — not the reproducible record itself.

## What you can and can't guarantee

| Layer | Reproducible? | How you handle it |
|---|---|---|
| Your analysis code | Yes | Commit it; it is the source of truth. |
| Python/R libraries | Yes | Pin exact versions in a lockfile. |
| A Skill or MCP server | Mostly | Pin the version; record it in provenance. |
| A live external database | No (it evolves) | Record the release/snapshot **date** + accession/hash. |
| The model's free-form output | No (stochastic) | Don't depend on it for the record — depend on the saved outputs and code. |

Full byte-for-byte reproducibility ends at the network boundary. The honest, achievable standard is **"pin what you can, record the rest"** — which is exactly what lets a colleague understand, trust, and re-attempt your work.

[Claude Science](../surfaces/claude-science.html) builds this discipline in: every figure it produces carries the exact code, environment, and message history that generated it. Working there gives you much of the pattern below for free — but the principle applies on any surface.

## A worked reference

The cookbook ships a complete example: [`recipes/examples/functional-enrichment/`](https://github.com/scripps-ai-enablement/sci-ai-enabler/tree/main/recipes/examples/functional-enrichment). It pairs the recipe [Run functional enrichment on a gene list](../../recipes/items/run-functional-enrichment-on-a-gene-list.html) with:

- `enrichment.py` — the analysis, with a deterministic offline replay and a live `gget`/Enrichr mode;
- `requirements.txt` — the pinned environment;
- `fixtures/enrichr_response.json` — a recorded external response carrying its snapshot date;
- `provenance.json` — emitted by every run (versions, source date, input hash, output hashes);
- a CI test that runs the script twice and asserts the output is **byte-identical** — reproducibility enforced as a check, not promised in prose.

Model your own analyses on it.
