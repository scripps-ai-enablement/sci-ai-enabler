---
title: Map a disease to its implicated genes and pathways
parent: All recipes
grand_parent: Recipes
nav_order: 14
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine, Drug Repurposing and Discovery, Molecular and Cellular Biology]
evidence_level: Reported
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-20
summary: Chain Open Targets target ranking into gget/Enrichr functional enrichment to turn a disease name or EFO/MONDO ID into a cited genes-and-pathways readout.
---

# Map a disease to its implicated genes and pathways

Start from a disease (a name, or an EFO/MONDO ID) and end with two cited tables: the genes most strongly associated with it, and the biological pathways those genes implicate — a two-step chain of Open Targets ranking into Enrichr over-representation analysis.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine, Drug Repurposing and Discovery, Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A recurring "where do I even start" question in target biology: given a disease, *which genes drive it, and what processes do those genes sit in?* The first half is a target-association lookup; the second is functional enrichment. Each half is a solved problem on its own, but the join is where time goes — exporting a ranked gene list from one tool, reshaping it into the symbol list the enrichment tool wants, and keeping the provenance straight so the final summary cites real terms rather than the model's prior. Solved looks like: disease in, two CSVs out (ranked associated genes; enriched GO/KEGG/Reactome/disease terms at adjusted p<0.05), plus a short synthesis that names only terms present in those CSVs — runnable on a laptop in a couple of minutes.

## Recommended approach

This recipe chains two existing recipes; follow each for the prompt-level detail.

1. **Rank the disease's associated genes.** Follow [Prioritize targets within a disease via Open Targets](prioritize-targets-within-a-disease.html), but for this chain you only need the association ranking, not the full four-pillar panel. Resolve the disease to its EFO/MONDO ID, then pull the top ~30 targets by **overall** association score (GraphQL `disease.associatedTargets(orderByScore: "score")`). Save the gene symbols.

   > The hosted Open Targets MCP endpoint is currently failing its handshake (see the known-issue note on the linked recipe). Until it's fixed, drive the query against the direct GraphQL API (`https://api.platform.opentargets.org/api/v4/graphql`) from plain Claude Code, or use the [ToolUniverse](../../catalog/tools/tooluniverse.html) `OpenTargets_*` tools. For overall-score ranking the GraphQL path is preferred — ToolUniverse exposes per-datasource scores only.

2. **Enrich the gene list.** Hand the top ~30 symbols to [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html). Run `gget enrichr` across `GO_Biological_Process_2023`, `KEGG_2021_Human`, `Reactome_2022`, `MSigDB_Hallmark_2020`, and `DisGeNET`, saving one CSV per library.

3. **Use DisGeNET as a positive control.** The disease you started from should resurface as a top DisGeNET term — if it does not, suspect a symbol-mapping or species mismatch before trusting the rest. (In the field test, knee OA recovered "Osteoarthritis, Knee" as expected.)

4. **Write the grounded synthesis.** Ask Claude to write a one-paragraph-per-library summary citing only terms that appear in the saved CSVs with adjusted p<0.05, then run the verification pass from the enrichment recipe (re-read the summary, confirm every named term is in the corresponding CSV, rewrite any claim that isn't).

## Why this assembly

Rung 3 — a small two-tool chain (Open Targets ranking + gget/Enrichr). It is genuinely two components because the question spans two databases: association evidence lives in Open Targets, pathway membership in Enrichr's libraries. Rung 1 (plain Claude) cannot supply either ranking or enrichment without fabricating; rung 2 (one tool) answers only half the question — Open Targets alone gives genes but not pathway context, gget/Enrichr alone needs a gene list you don't yet have. The chain stops at rung 3: no autonomous loop is needed because the data flow is a single linear hand-off, and the verification pass (not an agent) is what controls hallucination.

## Availability

Fully open. Open Targets data is CC0; the GraphQL API and ToolUniverse `OpenTargets_*` tools are unauthenticated. The gget skill is OSS (`K-Dense-AI/scientific-agent-skills`); `gget`/`pachterlab/gget` is BSD-2-Clause; Enrichr is free for academic and non-profit use (commercial users should review the [Enrichr terms](https://maayanlab.cloud/Enrichr/help#terms) and KEGG-library licences). No subscription or institutional account.

## Compute requirements

Laptop. Both legs are HTTP calls. A 30-gene chain across five Enrichr libraries plus the Open Targets ranking returns in roughly 1–2 minutes end-to-end; the field report clocked under one minute. No GPU; the CSV outputs are a few hundred KB.

## Evidence

Reported. A composition report ([#43, 2026-06-20](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/43)) documents this exact two-recipe chain run end-to-end on knee osteoarthritis (EFO_0004616): top associated genes NGF, GDF5, ACAN, COL27A1, PTGS2, SMAD3, FGF18, ALDH1A2; enriched pathways included Reactome ECM Organization / Collagen Formation, GO Cartilage Development, and KEGG TGF-β + Hippo signaling, with DisGeNET "Osteoarthritis, Knee" recovered as a positive control. Each leg inherits its own evidence: Open Targets association ranking is the peer-reviewed framework of [Buniello et al., *NAR* 53(D1):D1467 (2025)](https://doi.org/10.1093/nar/gkae1128); the database-grounded enrichment-plus-verification pattern is benchmarked by GeneAgent ([Wang et al., *Nature Methods* 22:1677 (2025)](https://doi.org/10.1038/s41592-025-02748-6), 84% of claims database-supported). No peer-reviewed benchmark of the *composed* chain against a manual disease→pathway workflow is known; the field report is a single documented success with a built-in positive control.

## Alternatives considered

- **Stop at Open Targets (rung 2).** If you only need the gene shortlist — not pathway context — use [Prioritize targets within a disease](prioritize-targets-within-a-disease.html) directly and skip the enrichment leg.
- **Start from your own gene list (rung 2).** If the genes come from a DE run or CRISPR screen rather than a disease association, skip step 1 and go straight to [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html).
- **Drill into one gene (rung 3, different shape).** When the goal is a deep readout on a single target rather than a disease-wide map, use [Build a target dossier](build-target-dossier.html).
- **An autonomous system (Biomni).** Overkill for a linear two-step hand-off; reach for it only when this map is one node inside a larger autonomous hypothesis loop.

## See also

- [Prioritize targets within a disease via Open Targets](prioritize-targets-within-a-disease.html) — step 1 of this chain.
- [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) — step 2 of this chain.
- [Build a target dossier](build-target-dossier.html) — gene-in, evidence-out, when you want depth on one target instead of a disease-wide map.
- [Open Targets Plugin](../../catalog/tools/open-targets.html)
- [gget (Claude Skill)](../../catalog/tools/gget.html)
- [ToolUniverse](../../catalog/tools/tooluniverse.html)

## Sources

- [Composition report #43 — knee-OA disease→genes→pathways chain](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/43) — filed 2026-06-20; verified 2026-06-20 (this run).
- [Buniello et al., "Open Targets Platform," *Nucleic Acids Research* 53(D1):D1467–D1475 (2025)](https://doi.org/10.1093/nar/gkae1128) — published 2025.
- [Wang Z. et al., "GeneAgent," *Nature Methods* 22:1677–1685 (2025)](https://doi.org/10.1038/s41592-025-02748-6) — published 2025-07.
- [gget documentation — `gget enrichr`](https://pachterlab.github.io/gget/en/enrichr.html) — verified 2026-06-20 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=map-disease-to-genes-and-pathways&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fmap-disease-to-genes-and-pathways.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
