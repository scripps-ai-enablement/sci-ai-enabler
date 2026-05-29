---
title: Triage a stack of new preprints in your field
parent: All recipes
grand_parent: Recipes
nav_order: 15
problem_class: Literature triage
subject_areas: [All]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-29
summary: Use the bio-research plugin in Claude Code to pull last-week bioRxiv and PubMed hits, rank by relevance, and produce a one-paragraph readout per paper.
---

# Triage a stack of new preprints in your field

Pull last-week bioRxiv and PubMed hits in a defined topic area, rank by relevance to the user's stated interests, and produce a one-paragraph readout per paper that calls out methods, claims, and obvious limitations.

| | |
|---|---|
| **Problem class** | Literature triage |
| **Subject areas** | All |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Most working life scientists drown in new literature. bioRxiv alone posts ~200 preprints a day across the life sciences; PubMed indexes thousands of newly-published papers weekly. The cost of triage isn't reading — it's deciding what to read. Solved looks like: a weekly digest, scoped to your topic, with a one-paragraph readout per paper that lets you decide in one minute whether to open the PDF.

This is the canonical entry-level use of an LLM in a scientific workflow. Doing it well end-to-end — fresh sources, faithful summaries, no hallucinated citations — is the value the recipe delivers.

## Recommended approach

1. **Install the [bio-research plugin](../../catalog/tools/bio-research.html)** in Claude Code. One install gives you the bioRxiv connector, the [Anthropic PubMed Connector](../../catalog/tools/pubmed.html), and several others you'll want later. Run `/bio-research:start` once to confirm the bundled tools loaded.
2. **Define your topic in a system prompt** at the top of the session. Be specific:

   ```
   I work on cryptic splicing in neurodegeneration. I want a weekly
   digest of last-week bioRxiv and PubMed hits that touch any of:
   TDP-43, STMN2, UNC13A, cryptic exons, RNA-seq evidence for
   mis-splicing in ALS/FTD/AD. Skip review articles unless they cite
   2026 primary work.
   ```

3. **Ask for the digest** with explicit recency and ranking:

   ```
   Pull bioRxiv + PubMed hits posted in the last 7 days matching the
   topic above. Rank by relevance to my interests (be honest about
   ones you're uncertain about). For each, give me: 1-line title, 1-2
   sentence claim, methods in 1 sentence, 1 obvious limitation, and
   the DOI. Cap at 15 papers. If two papers cover the same finding,
   keep the one with stronger methods.
   ```

4. **Open the DOIs for the ones you flag.** The recipe stops at triage; reading is yours.

5. **Save the prompt** as a Claude Code custom slash command (e.g., `/triage-preprints`) so the next weekly run is one command.

## Why this assembly

Rung 2 of the simplicity ladder (Claude Code + one plugin) is the right answer here. Plain Claude Code can answer questions about preprints but cannot reliably pull *fresh* ones — and "fresh" is the entire point of triage. The bio-research plugin bundles bioRxiv + PubMed in a single install, which is cheaper than `claude mcp add` for each separately. There is no need to escalate to a multi-tool harness or an autonomous-science system; a chat session driving two read-only MCPs is sufficient and stays fully under the user's control.

## Availability

Fully open. The bio-research plugin is Apache 2.0; bioRxiv and PubMed access is free and requires no institutional license. You need an Anthropic account to use Claude Code, and any current Claude plan (including the free tier, subject to its rate limits) is enough for a weekly digest.

## Compute requirements

Laptop-sufficient. The entire workflow is a chat session driving two HTTP-MCP servers; nothing runs locally beyond Claude Code itself.

## Evidence

Reported. The bio-research plugin's README ([anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins/tree/main/bio-research)) documents this exact use case as one of the bundled "Literature Review" skill's primary flows. Anthropic's tutorial for the [PubMed Connector](https://claude.com/resources/tutorials/using-the-pubmed-connector-in-claude) covers ranked-summary outputs with cited DOIs.

No peer-reviewed benchmark of this exact assembly is known. The closest quantitative point of comparison is Stanford's Biomni LAB-Bench DbQA result (74.4%, matching expert baselines) on biomedical Q&A — a harder problem than literature triage and a different harness, but a useful upper-bound reference for what an LLM-driven biomedical-lookup workflow can achieve. See [Biomni](../../autonomous-science/systems/biomni.html).

A known issue (`anthropics/claude-code#40106`, March 2026) reports that plugin-bundled MCP tools sometimes return "Session not found" in Claude Code while working in Claude.ai Cowork. If the digest comes back empty, verify the tool loaded by running `/mcp` and re-running.

## Alternatives considered

- **Plain Claude Code, no MCP.** Fails the freshness test: the model's training cutoff means "last-week preprints" cannot be answered from memory. Rejected.
- **Two separate MCP installs (`pubmed` + a standalone bioRxiv MCP).** Equivalent capability but slightly more setup. Reach for this if you don't want the rest of the bio-research bundle and prefer minimal install footprint.
- **An autonomous-science system (Robin, Biomni, OpenScientist).** Overkill. These are designed for hypothesis generation and wet-lab follow-up; using them for plain triage wastes a lot of agent loop on a problem that doesn't need it.

## See also

- [bio-research (Claude Code Plugin)](../../catalog/tools/bio-research.html)
- [Anthropic PubMed Connector](../../catalog/tools/pubmed.html)
- [Biomni](../../autonomous-science/systems/biomni.html) — what the same problem class looks like one rung up, when triage gives way to active hypothesis generation.

## Sources

- [bio-research plugin README](https://github.com/anthropics/knowledge-work-plugins/tree/main/bio-research) — last updated 2026-05; verified 2026-05-21 (this run).
- [Anthropic PubMed Connector tutorial](https://claude.com/resources/tutorials/using-the-pubmed-connector-in-claude) — published 2025-10; verified 2026-05-21 (this run).
- [`anthropics/claude-code` issue #40106](https://github.com/anthropics/claude-code/issues/40106) — opened March 2026; tracking the "Session not found" bundled-MCP issue noted under Evidence.

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=triage-new-preprints&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftriage-new-preprints.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
