---
title: Validate a drug target with a GO/NO-GO score before committing bench work
parent: All recipes
grand_parent: Recipes
nav_order: 33
problem_class: Knowledge synthesis
subject_areas: [Drug Repurposing and Discovery, Translational Medicine, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-05
summary: Drive the ToolUniverse Drug Target Validation skill to score one hypothesized target 0–100 across genetics, druggability, safety, and clinical precedent, emitting a cited GO/NO-GO card.
---

# Validate a drug target with a GO/NO-GO score before committing bench work

You already have a target in mind — a gene a screen or a paper pointed you at. Before you spend a year making tools against it, get a structured, weighted, cited verdict: genetic support, druggability, normal-tissue safety, and competitive landscape, rolled into one 0–100 score with a GO/NO-GO recommendation.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Drug Repurposing and Discovery, Translational Medicine, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A screen, a knockout phenotype, or a review hands you a *single* candidate target and the question is not "which of these hundred genes" — it is "should I commit to *this* one?" The honest answer weighs four axes that live in different databases: is there human genetic evidence tying the gene to the disease (Open Targets, GWAS, rare-variant), is the protein actually druggable (pocket, target class, existing chemical matter), is it safe to hit (expression in critical organs, knockout lethality, known ADRs), and is the field already crowded (approved drugs, late-stage trials). Done by hand, each axis is a separate database session and the "verdict" ends up as an unweighted paragraph that the next reviewer re-litigates.

Solved looks like: a gene symbol in, a single card out — a 0–100 score with the four sub-scores broken out, a priority tier, a GO/NO-GO line, and every claim traceable to the tool call that produced it — in a few minutes on a laptop. This is a *triage* verdict, not a substitute for the wet-lab validation the score is meant to gate.

## Recommended approach

Rung 2 of the simplicity ladder — one Claude Skill over one MCP server. The [Drug Target Validation skill](../../catalog/tools/tooluniverse-drug-target-validation.html) runs the four-gate model and computes the composite score; it calls the [ToolUniverse MCP server](../../catalog/tools/tooluniverse.html) for every underlying lookup.

1. **Register the MCP server and add the skill.** The skill is inert without the server (see both catalog pages for the authoritative install):

   ```
   claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
   npx skills add mims-harvard/ToolUniverse
   ```

   The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly by name.

2. **Run the validation on your target.** A minimal prompt:

   ```
   Use the drug-target-validation skill to validate SOAT1 as a target
   for familial hypercholesterolemia.

   Resolve identifiers first (HGNC, Ensembl, UniProt, ChEMBL), then run
   all four gates and score them:
     - Disease association (30): OpenTargets genetic + literature + pathway.
     - Druggability (25): target class, pocket/structure, existing chemistry.
     - Safety in normal tissue (20): critical-organ expression, mouse-KO
       lethality, known ADRs.
     - Clinical precedent (15): approved drugs, late-stage trials, the
       differentiation bar.
     - Validation evidence (10).
   Print each gate's sub-score with the specific tool call and value that
   justified it. Give the composite 0-100, the priority tier, and the
   GO / NO-GO line. Document negative findings; do not hide a failed gate.
   ```

   Repeat for each candidate target you want compared head-to-head — the score is designed to be portfolio-ranked.

3. **Capture the run as a durable artifact.** Do not leave the verdict in the chat. Have Claude write a parameterized command file and a scored table so the run is re-executable and auditable:

   ```
   Write .claude/commands/validate-target.md — a slash command
   /validate-target <gene> <disease_efo> that runs the prompt above and
   appends one row to targets/validation_scores.csv:
     gene | disease_efo | assoc_score | druggability_score | safety_score |
     precedent_score | evidence_score | composite | tier | recommendation.
   Also write targets/<gene>_validation_<date>.md with the full cited
   gate-by-gate card.
   ```

   Commit `.claude/commands/validate-target.md`, `targets/validation_scores.csv`, and the per-target cards to version control.

4. **Record provenance.** Live databases move, so pin what you can and date-stamp what you cannot. Have Claude emit `targets/provenance.json` capturing: the `tooluniverse` package version (`uvx tooluniverse --version`), the skill commit/tag from `npx skills`, the Open Targets / ChEMBL data-release labels returned by the tool calls, the run date, the resolved identifiers (Ensembl/UniProt/ChEMBL accessions), and the model id. The saved `validation_scores.csv` and per-target cards are the audit trail — any prose summary must cite only the sub-scores and tool values that appear in them.

5. **Drill down on the survivors.** A Tier-1/Tier-2 target earns a deeper look. Pipe it into the [Build a target dossier](build-target-dossier.html) recipe for the free-form structure/dependency/expression context, check cancer-context selectivity with [Find selective cancer dependencies with DepMap](find-selective-cancer-dependencies-with-depmap.html), and design knockouts with [Design CRISPR sgRNAs for a gene knockout](design-crispr-sgrnas-for-a-gene-knockout.html) to actually test it.

## Why this assembly

Rung 2. The four-gate scoring, identifier resolution, and composite arithmetic are exactly the surface the [Drug Target Validation skill](../../catalog/tools/tooluniverse-drug-target-validation.html) bundles — a thin, auditable reasoning layer that drives ToolUniverse's `OpenTargets_*`, `UniProt_*`, and ChEMBL tool calls and computes the score in Python rather than narrating it. Plain Claude Code hitting the raw GraphQL/REST APIs (rung 1) can reach the same data, but re-derives the gate weights and the identifier-reconciliation boilerplate every session, which is precisely what makes hand-built "GO/NO-GO" verdicts irreproducible. A multi-tool harness (rung 3) adds nothing: this is one skill over one MCP, not an orchestration across heterogeneous servers. A rung-4 autonomous system is unjustified — the workflow is shallow and one-shot, and the value is the per-gate provenance an opaque agent would bury.

## Availability

Fully open. ToolUniverse and its skills are Apache-2.0; the wrapped data sources (Open Targets CC0, ChEMBL CC-BY-SA-3.0, UniProt CC-BY-4.0, Ensembl, HGNC) are free with no auth. `uvx` and Node are the only local prerequisites; no subscription, no institutional license, no account beyond a Claude plan.

## Compute requirements

Laptop. Every step is a read-only API lookup plus in-process scoring; the ToolUniverse stdio server uses on the order of 100–300 MB RAM. Wall-clock for one target is dominated by Claude's tool-calling latency across the four gates — expect roughly 2–5 minutes per target. No GPU, no local datasets.

## Evidence

`Proposed`. No published benchmark of this exact skill-driven target-validation score against an expert GO/NO-GO panel is known. The closest documented evidence is the ToolUniverse ecosystem paper itself ([Gao et al., *Democratizing AI scientists using ToolUniverse*, arXiv:2509.23426, 2025-09-27](https://arxiv.org/abs/2509.23426)), whose hypercholesterolemia case study used ToolUniverse to build an AI scientist that identified a potent analog with favorable predicted properties — demonstrating the same tool-composition pattern (Open Targets + ChEMBL + UniProt over the ToolUniverse MCP) that this skill drives, though not the validation-score workflow specifically. The four gates themselves are the field-standard target-assessment axes: human genetic evidence as the dominant predictor of clinical success ([Nelson et al., *Nat. Genet.* 2015, 47:856](https://doi.org/10.1038/ng.3314); [Minikel et al., *Nature* 2024, 629:624](https://doi.org/10.1038/s41586-024-07316-0)), and the precedence/tractability/doability/safety framework that Open Targets operationalizes ([Ochoa et al., *Nucleic Acids Res.* 2023, 51:D1353](https://doi.org/10.1093/nar/gkac1046)). Each component has independent validation; the agent-orchestrated composite score does not. Treat the tier and GO/NO-GO line as a structured triage hypothesis, not a decision.

## Alternatives considered

- **Prioritize targets within a disease (rung 2, Open Targets).** Reach for the [prioritize-targets recipe](prioritize-targets-within-a-disease.html) when the question is inverted — disease in, a *ranked shortlist* of candidate genes out. This recipe is the complement: you already have one gene and want a weighted verdict on it, not a ranking.
- **Build a target dossier (rung 3).** The [target-dossier recipe](build-target-dossier.html) assembles a richer free-form gene → structure → dependency profile across four lookups, but it does not produce a single weighted score or a GO/NO-GO tier. Use the dossier for narrative depth on a target that already passed this score; use this recipe for the fast, comparable triage that decides whether the dossier is worth writing.
- **Plain Claude Code + raw Open Targets GraphQL (rung 1).** Viable if you cannot install the ToolUniverse MCP, but you re-implement the gate weights and identifier reconciliation each session, and the composite becomes hand-derived and irreproducible. Prefer it only as a fallback.
- **A rung-4 autonomous system (Biomni, Robin).** Justified only when target validation is one step inside a larger autonomous discovery loop that also runs experiments. For a standalone, auditable GO/NO-GO on one target, the single skill is more transparent per gate.

## See also

- [Drug Target Validation (ToolUniverse Claude Skill)](../../catalog/tools/tooluniverse-drug-target-validation.html)
- [ToolUniverse](../../catalog/tools/tooluniverse.html)
- [Prioritize targets within a disease via Open Targets](prioritize-targets-within-a-disease.html) — the disease-in, ranked-list complement.
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — the free-form drill-down for a target that passes this score.
- [Find selective cancer dependencies for a cancer context with DepMap](find-selective-cancer-dependencies-with-depmap.html) — context-specific dependency evidence for the druggability/selectivity gate.
- [Design CRISPR sgRNAs for a gene knockout](design-crispr-sgrnas-for-a-gene-knockout.html) — how to actually test a GO target at the bench.

## Sources

- [Drug Target Validation skill — `skills/tooluniverse-drug-target-validation/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-target-validation/SKILL.md) — verified 2026-07-05 (this run).
- [Gao S. et al., "Democratizing AI scientists using ToolUniverse," arXiv:2509.23426](https://arxiv.org/abs/2509.23426) — published 2025-09-27; verified 2026-07-05 (this run).
- [Nelson M.R. et al., "The support of human genetic evidence for approved drug indications," *Nat. Genet.* 47:856 (2015)](https://doi.org/10.1038/ng.3314) — published 2015-06.
- [Minikel E.V. et al., "Refining the impact of genetic evidence on clinical success," *Nature* 629:624 (2024)](https://doi.org/10.1038/s41586-024-07316-0) — published 2024-04.
- [Ochoa D. et al., "The next-generation Open Targets Platform," *Nucleic Acids Res.* 51:D1353 (2023)](https://doi.org/10.1093/nar/gkac1046) — published 2022-11.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=validate-a-drug-target-with-a-go-no-go-score&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fvalidate-a-drug-target-with-a-go-no-go-score.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
