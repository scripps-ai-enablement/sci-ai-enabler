---
title: Scan adverse-event reports for a drug-safety signal
parent: All recipes
grand_parent: Recipes
nav_order: 30
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-19
summary: Use the OpenFDA MCP server to pull FAERS adverse-event reports and label warnings for a drug, rank the top reported reactions, and assemble a pharmacovigilance snapshot.
---

# Scan adverse-event reports for a drug-safety signal

Name a drug; get back its top reported adverse reactions from the FDA Adverse Event Reporting System (FAERS), its labeled warnings and contraindications, and a plain-language pharmacovigilance snapshot — without leaving the chat or writing a single API call.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Anyone evaluating a marketed drug — a clinical pharmacologist, a safety reviewer, a repurposing scientist eyeing an off-label use — needs a fast read on what goes wrong in the real world. The data is public (FAERS holds millions of spontaneous reports; the openFDA label endpoint holds structured warnings), but the openFDA query syntax is fiddly, the FAERS counts need careful framing (spontaneous reports are not incidence rates), and a manual portal session is slow and easy to do inconsistently across drugs. Solved looks like: name the drug, get the top reactions ranked by report count, the labeled warnings and contraindications, and a written caveat that report counts are not denominators — reproducibly, in one conversation.

## Recommended approach

1. **Get a free openFDA API key** at [open.fda.gov/apis/authentication](https://open.fda.gov/apis/authentication/) (raises the rate limit from 1,000 to 120,000 requests/hour), then **register the [OpenFDA MCP server](../../catalog/tools/openfda.html)** in Claude Code:

   ```
   claude mcp add-json openfda '{"command":"npx","args":["-y","@ythalorossy/openfda"],"env":{"OPENFDA_API_KEY":"your_api_key_here"}}'
   ```

   Restart Claude Code so it picks up the server. The seven tools (`get-drug-adverse-events`, `get-drug-safety-info`, `get-drug-by-generic-name`, `get-drug-by-ndc`, …) appear as callable MCP tools.

2. **Resolve the drug name first.** Brand and generic names hit different FAERS fields; resolve to the generic (active-ingredient) name so the report counts aggregate correctly.

   ```
   Use the openfda MCP. For "Eliquis", resolve the generic name first
   (get-drug-by-generic-name), then confirm which name returns the
   larger FAERS report set before counting reactions.
   ```

3. **Pull and rank the adverse-event reports.** Ask for the top reactions by report count and have Claude tabulate them:

   ```
   Call get-drug-adverse-events for apixaban. Return the top 20 reported
   reactions (MedDRA preferred terms) ranked by report count, as a table
   with counts and the share of total reports. Note the total report
   count for the drug.
   ```

4. **Layer in the structured label.** Pull warnings, contraindications, and interactions from the labeling endpoint and align them against the FAERS top reactions — flag any frequently reported reaction that is *not* on the label.

   ```
   Call get-drug-safety-info for apixaban. List boxed warnings,
   contraindications, and drug interactions. Then cross-check: which of
   the top-20 FAERS reactions are already labeled, and which are not?
   ```

5. **Frame the counts honestly.** Require the summary to state, in plain language, that FAERS counts are spontaneous-report tallies — subject to reporting bias and stimulated reporting, with no exposure denominator — so they signal *what is reported*, not incidence or causation.

6. **Hand off.** The ranked reaction table plus the label cross-check is a pharmacovigilance snapshot for a target dossier, a repurposing safety pre-screen, or a literature-review appendix. For formal disproportionality statistics (PRR, ROR, EBGM), export the counts and run them in a dedicated tool — see *Alternatives considered*.

## Why this assembly

Rung 2. The OpenFDA MCP turns the awkward openFDA query API into seven typed tools Claude calls directly; one server solves the whole problem. Plain Claude Code (rung 1) would have to hand-construct openFDA URLs from memory and parse the JSON — brittle and inconsistent across drugs, and prone to the brand-vs-generic field trap. There is no need for a multi-tool harness: a single drug-safety snapshot is one well-scoped knowledge-synthesis task. The one discipline the recipe enforces beyond the tool — framing FAERS counts as reports, not rates — is a prompt instruction, not a second component.

## Availability

Fully open. The OpenFDA MCP server is MIT-licensed (`@ythalorossy/openfda` on npm); the openFDA API is public U.S. government data. A free API key is required at startup (store it in the client config, not in a committed file). Any current Claude plan suffices. No institutional license or data-residency constraint — queries hit the public openFDA endpoint and return aggregate report data.

## Compute requirements

Laptop. Every step is a remote API call; there is no local computation beyond tabulating JSON. A full single-drug snapshot (name resolution + adverse-event ranking + label pull) is a handful of requests and completes in seconds. The API key's 120,000 requests/hour ceiling is far above what a single interactive session uses.

## Evidence

Proposed. No peer-reviewed paper documents this *exact* assembly (Claude Code + the ythalorossy OpenFDA MCP) producing a drug-safety snapshot. The component evidence is sound:

- **openFDA / FAERS as the public pharmacovigilance source** — the openFDA drug-event and labeling endpoints are the canonical programmatic access to FAERS and structured product labeling; the server wraps them faithfully (per the [catalog page](../../catalog/tools/openfda.html), verified 2026-06-06).
- **LLM-assisted FAERS / pharmacovigilance triage (analogous, method-level)** — a growing literature uses LLMs to read and structure adverse-event narratives and FAERS data; these validate the *task* (LLM-driven safety-signal triage) but not this specific MCP assembly. The recipe deliberately keeps the LLM on retrieval-and-framing, not causal inference.

No published comparison of this MCP assembly against a manual openFDA portal session is known. The server changes *how* the data is fetched (typed tools vs hand-built URLs), not the underlying FAERS data.

## Alternatives considered

- **Plain Claude Code with hand-built openFDA URLs (rung 1).** Possible but brittle: you re-derive query syntax each time and risk the brand-vs-generic field trap. Reach for it only if you cannot register an MCP server.
- **[BioMCP](../../catalog/tools/biomcp.html) (broader multi-source server).** BioMCP also wraps openFDA adverse events alongside PubMed, ClinicalTrials.gov, and MyVariant. Prefer it when the safety scan is one step in a larger multi-database dossier; prefer the focused OpenFDA MCP when you only need the drug-safety endpoints and want the smallest install.
- **Formal disproportionality analysis (PRR/ROR/EBGM).** The MCP returns counts, not disproportionality statistics. For a quantitative signal-detection study, export the counts and compute PRR/ROR in a dedicated pharmacovigilance package (e.g., R `PhViD` / `openEBGM`) — that is a different, statistics-grade workflow outside this recipe's scope.

## See also

- [OpenFDA MCP Server (ythalorossy)](../../catalog/tools/openfda.html)
- [BioMCP](../../catalog/tools/biomcp.html) — broader multi-source biomedical server that also wraps openFDA adverse events.
- [Scan approved drugs for repurposing candidates against a disease](scan-drug-repurposing-candidates.html) — the upstream repurposing scan whose shortlist this safety snapshot pre-screens.
- [Build a target dossier for a gene of interest](build-target-dossier.html) — drop the safety snapshot in as the tractability/safety section.

## Sources

- [OpenFDA MCP catalog page (this repo)](../../catalog/tools/openfda.html) — `last_verified` 2026-06-06.
- [`ythalorossy/openfda` (GitHub)](https://github.com/ythalorossy/openfda) — verified 2026-06-06 (this run).
- [openFDA API authentication / rate limits](https://open.fda.gov/apis/authentication/) — verified 2026-06-06 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=scan-adverse-events-for-drug-safety-signal&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fscan-adverse-events-for-drug-safety-signal.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
