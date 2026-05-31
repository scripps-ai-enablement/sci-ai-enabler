---
title: Prioritize targets within a disease via Open Targets
parent: All recipes
grand_parent: Recipes
nav_order: 19
problem_class: Knowledge synthesis
subject_areas: [Drug Repurposing and Discovery, Translational Medicine, Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-31
summary: Drive the Open Targets MCP plugin to rank candidate targets within a disease across the four prioritisation pillars (precedence, tractability, doability, safety) and emit a cited target shortlist.
---

# Prioritize targets within a disease via Open Targets

For a disease (EFO or MONDO ID, or plain name), produce a ranked target shortlist using the Open Targets target-prioritisation framework — one prompt, one cited table, all four pillars (precedence, tractability, doability, safety) attached.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Drug Repurposing and Discovery, Translational Medicine, Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Drug-discovery teams routinely have to walk into a new indication and ask: *of the hundreds of genes associated with this disease, which 5–20 are the best candidates to actually drug?* The answer is not the top of the association-score list — it has to weigh precedence (do clinical compounds already exist?), tractability (is there a ligandable pocket or a precedent modality?), doability (does the right assay or model system exist?), and safety (is there evidence of essentiality or adverse-event signal?). All four pillars live inside the Open Targets Platform, but assembling them by hand across the GraphQL schema is tedious. Solved looks like: one prompt — disease in, ranked target table out, with each cell traceable to the GraphQL field that produced it, in under five minutes.

## Recommended approach

1. **Install the Open Targets plugin** ([catalog page](../../catalog/tools/open-targets.html)).

   ```
   /plugin marketplace add anthropics/life-sciences
   /plugin install open-targets@life-sciences
   ```

2. **Drive the prioritisation with a single prompt.** A minimal version:

   ```
   For disease EFO_0000676 (psoriasis), use the open-targets MCP to:
     1. Resolve the disease and confirm the EFO ID.
     2. Pull the top 30 associated targets by overallAssociationScore.
     3. For each target, fetch the prioritisation panel:
        - precedence pillar: maxClinicalTrialPhase, drugApprovals
        - tractability pillar: smallMoleculeTractability,
          antibodyTractability, otherModalitiesTractability
        - doability pillar: knownDrugs count, mouseKO availability
        - safety pillar: hasSafetyEvent, geneticConstraint (LOEUF),
          mouse_lethal phenotype
     4. Score each target 0–4 per pillar (sum = 0–16) and rank.
     5. Output a Markdown table with columns: rank, gene symbol,
        ENSG, overall association score, the four pillar scores,
        and a one-line rationale per row.
   Cite the GraphQL field that produced each value.
   ```

3. **Inspect the schema before assuming field names.** Open Targets evolves; ask the agent to call `get_open_targets_graphql_schema` first so the field names in step 2 match the live API. The `target.prioritisation` field on a `Target` object exposes the prioritisation data points named in the [public docs](https://platform-docs.opentargets.org/target-prioritisation).

4. **Iterate, then parameterize.** Once the first disease works, save the prompt as a slash command (e.g., `/prioritize-targets <EFO_ID>`) and reuse it across the rest of the portfolio.

## Why this assembly

Rung 2 of the simplicity ladder. The whole prioritisation framework lives inside a single MCP server (Open Targets), so a single plugin solves it. Stepping down to Claude-Code-alone (rung 1) loses the GraphQL access entirely — Claude would have to either scrape the web UI or fabricate scores. Stepping up to a toolbelt (rung 3) — adding UniProt, AlphaFold, DepMap — produces a richer dossier but answers a different question; that's the [Build a target dossier](build-target-dossier.html) recipe. For pure within-disease target ranking, the Open Targets plugin alone is the right rung.

## Availability

Fully open. Open Targets data is CC0 ([Buniello et al., 2025](https://doi.org/10.1093/nar/gkae1128)); the MCP server is Apache-2.0 and unauthenticated. No subscription or institutional account.

## Compute requirements

Laptop. Pure HTTP GraphQL calls; nothing local. A 30-target prioritisation call typically runs in under a minute. The streamable HTTP MCP transport adds no setup beyond `claude mcp add` or the plugin install.

## Evidence

Reported. The Open Targets target-prioritisation framework is the canonical, peer-reviewed framework for this task — [Buniello et al., *Nucleic Acids Research* 53(D1):D1467–D1475 (2025)](https://doi.org/10.1093/nar/gkae1128) documents the four-pillar approach and its data sources. The framework itself is informed by [Minikel et al., *Nature* 629:624–629 (2024)](https://doi.org/10.1038/s41586-024-07316-0), which quantifies how human-genetics evidence improves clinical-success rates ~2× and underpins the precedence pillar. The Open Targets MCP server (release 2026.03.1, April 2026) exposes the same prioritisation fields used in the platform's web UI, so the Claude assembly inherits the framework's validation. No published head-to-head benchmark of the *MCP-driven* prioritisation against the *web UI* prioritisation is known — they call the same API, so the comparison is identity by construction. Closest documented LLM application: the agentic drug-repurposing literature cites Open Targets as a primary evidence source ([Zunzunegui Sanz et al., *bioRxiv* 2025-06-13](https://doi.org/10.1101/2025.06.13.659527); [More et al., *npj Precision Oncology* 10:95 (2025)](https://doi.org/10.1038/s41698-025-01265-1)).

## Alternatives considered

- **gget alone** ([catalog page](../../catalog/tools/gget.html)). gget has a wrapper for Open Targets associations but does not expose the prioritisation panel directly. Use gget when the question is just "what diseases is this gene linked to" — for ranking within a disease, the MCP plugin is required.
- **Open Targets web UI.** Equivalent for one-off lookups but does not produce a cited table or compose with downstream agent steps (writing a dossier, generating a slide, drafting a target-rationale section of a grant). Reach for the UI when interactivity matters more than reproducibility.
- **Biomni** ([system page](../../autonomous-science/systems/biomni.html)). Wires Open Targets in as one of many tools. Reach for Biomni when target prioritisation is one step in a larger autonomous loop (generate candidate gene set → prioritise → propose validation experiments). For one-shot prioritisation, the single-plugin recipe is simpler.
- **Multi-tool dossier**. The [Build a target dossier](build-target-dossier.html) recipe goes in the opposite direction — gene-in, evidence-out — and adds UniProt / AlphaFold / DepMap. Reach for that when you already have a target and want the full readout; reach for *this* recipe when you have a disease and need the gene shortlist.

## See also

- [Open Targets Plugin](../../catalog/tools/open-targets.html)
- [Build a target dossier](build-target-dossier.html) — the natural next step once the shortlist is ranked.
- [Scan approved drugs for repurposing candidates against a disease](scan-drug-repurposing-candidates.html) — drug-out-of-disease version of the same problem.
- [gget (Claude Skill)](../../catalog/tools/gget.html) — lower-rung alternative when prioritisation pillars are not required.

## Sources

- [Open Targets target-prioritisation docs](https://platform-docs.opentargets.org/target-prioritisation) — verified 2026-05-31 (this run).
- [Buniello et al., "Open Targets Platform: facilitating therapeutic hypotheses building in drug discovery," *Nucleic Acids Research* 53(D1):D1467–D1475 (2025)](https://doi.org/10.1093/nar/gkae1128).
- [Minikel et al., "Refining the impact of genetic evidence on clinical success," *Nature* 629:624–629 (2024)](https://doi.org/10.1038/s41586-024-07316-0).
- [Open Targets blog: official MCP](https://blog.opentargets.org/official-open-targets-mcp/) — release 2026.03.1 (April 2026); verified 2026-05-31 (this run).
- [`opentargets/open-targets-platform-mcp`](https://github.com/opentargets/open-targets-platform-mcp) — verified 2026-05-31 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=prioritize-targets-within-a-disease&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fprioritize-targets-within-a-disease.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
