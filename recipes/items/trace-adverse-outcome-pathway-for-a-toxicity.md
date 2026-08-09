---
title: Trace an adverse outcome pathway from a molecular initiating event to an organ finding
parent: All recipes
grand_parent: Recipes
nav_order: 28
problem_class: Knowledge synthesis
subject_areas: [Chemistry, Drug Repurposing and Discovery, Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-09
summary: Drive the ToolUniverse Adverse Outcome Pathway skill to assemble candidate MIE-to-endpoint pathways for an observed toxicity, with weight of evidence recorded per link.
---

# Trace an adverse outcome pathway from a molecular initiating event to an organ finding

You have a compound and an organ-level finding, and you need a mechanistic account you can act on: which molecular initiating event plausibly starts it, which key events sit between there and the finding, and how well-evidenced each link actually is.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery, Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A tox study comes back with a finding — hepatic steatosis, reduced anogenital distance, thyroid follicular hypertrophy — and the next meeting asks *why*. The answer determines what happens next: a receptor-binding assay if the mechanism runs through a nuclear receptor, a mitochondrial panel if it runs through bioenergetics, a read-across argument if the pathway is shared across an analog series, and nothing at all if the finding is a species-specific artifact. Getting this wrong is expensive in both directions: chasing the wrong mechanism burns a quarter, and dismissing a real one shows up in a regulatory filing.

The adverse outcome pathway framework is the structured form of this reasoning — molecular initiating event, an ordered chain of measurable key events, an adverse outcome, with a weight-of-evidence call on each link ([Tanabe et al. 2025](https://doi.org/10.1093/etojnl/vgaf173)). AOP-Wiki holds 595 AOPs, 1,939 key events and 3,168 key-event relationships (fetched 2026-08-09), but the content is uneven: some pathways are OECD-endorsed and quantitatively supported, others are one group's draft, and progress toward fully endorsed AOPs has been slow ([Holmer et al. 2024](https://doi.org/10.1016/j.reprotox.2024.108662)). "Solved" here means a committed table where each candidate pathway is named with its OECD status, each link carries its own evidence grade, and the chemical-specific evidence connecting *your* compound to the pathway is a separate column from the pathway's own biology — because those two things are almost always at different strengths.

## Recommended approach

1. **Install the [Adverse Outcome Pathway skill](../../catalog/tools/tooluniverse-adverse-outcome-pathway.html)**, which needs the [ToolUniverse](../../catalog/tools/tooluniverse.html) MCP server first — the catalog pages own both install commands. The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly ("use the adverse-outcome-pathway skill") rather than relying on automatic dispatch.

2. **Write the query from the finding, not from the compound.** AOP discovery searches by organ, mechanism, or receptor keyword (`AOPWiki_list_aops`) — the pathway index is organized around biology, not chemistry. Put the observed endpoint, the target organ, the species, and the study type into `finding.yaml`, along with the exact search terms you intend to use. Commit that file first. A pathway list generated from remembered search terms cannot be re-derived, and the term choice is the single largest determinant of which pathways come back.

3. **Commit the workflow as a slash command.** Have Claude Code write `.claude/commands/trace-aop.md` capturing the instruction, the output schema, and the gates below, so the next finding is traced by the same text. Run it with `/trace-aop`.

4. **Record OECD status per candidate pathway before reading any of its content.** `aop_candidates.csv` carries `aop_id`, `title`, `oecd_status` (endorsed / under review / in the workplan / under development), `mie`, `adverse_outcome`, and `retrieved_utc`. An AOP under development is a hypothesis one group wrote down; an endorsed one has been through the OECD review process that exists precisely to make its links usable for decisions ([Tanabe et al. 2025](https://doi.org/10.1093/etojnl/vgaf173)). Sorting by status before you read titles keeps you from anchoring on a well-written draft.

5. **Emit one row per key-event relationship, never one per pathway.** `key_events.csv` carries `aop_id`, `upstream_ke`, `downstream_ke`, `adjacency`, `weight_of_evidence`, and `quantitative_understanding` as reported by `AOPWiki_get_aop`. The KER is the unit of causal knowledge, and it is the unit that gets developed and reviewed on its own ([Holmer et al. 2024](https://doi.org/10.1016/j.reprotox.2024.108662)). A pathway summarized as "moderate evidence" hides whether the weak link is the one you were planning to assay. Report the **weakest** link alongside the pathway, not the average.

6. **Make stressor absence an explicit value, not a blank.** AOP-Wiki lists 871 prototypical stressors across 595 AOPs (fetched 2026-08-09) — most AOPs name a handful of exemplar chemicals or none, so your compound being absent is the ordinary case and carries almost no information. Record `stressor_match` as one of `listed`, `not_listed`, or `aop_lists_no_stressors`. Collapsing the last two into one blank cell is the mistake that turns a sparse curation field into a false negative.

7. **Keep chemical-specific evidence in its own table, and split direct from inferred.** `chemical_evidence.csv` holds the CTD gene and disease hits (`CTD_get_chemical_gene_interactions`, `CTD_get_chemical_diseases`) with an `association_type` column that is either `direct_curated` or `inferred`. CTD's inferred chemical-disease links are transitive constructs assembled through a shared gene, and they outnumber the directly curated ones by orders of magnitude — enough that CTD itself had to build a network-topology score to rank them ([King et al. 2012](https://doi.org/10.1371/journal.pone.0046524)). An inferred link is a hypothesis generator; presented next to a curated one without a label, it reads as corroboration.

8. **Put the hazard layer in a third table and do not let it validate the mechanism.** GHS classification, IARC status and LD50 values (`PubChemTox_*`) tell you the compound is hazardous; they say nothing about which pathway produced your finding. Keep them in `hazard_context.csv` for the reader's orientation.

9. **Grade each candidate pathway three ways, defaulting to the middle.** In `aop_report.md`, label every candidate `supported`, `plausible_unsupported`, or `not_supported`, defaulting to `plausible_unsupported`. Reserve `supported` for pathways that are OECD-endorsed *and* have your compound as a listed stressor or a direct curated CTD interaction with an MIE gene. Every verdict must cite the specific `key_events.csv` and `chemical_evidence.csv` rows behind it; a graded pathway with no row references is a model opinion. Then state the **one assay that would discriminate** between the surviving candidates — that is what the reader came for.

10. **Record provenance.** `provenance.json` carries the AOP-Wiki release version (2.8, released 2026-03-08) with the UTC query timestamp, the ToolUniverse version, the skill commit SHA, the sha256 of `finding.yaml`, and the model id. These are live APIs and nothing here is byte-reproducible; the release version plus timestamp is what makes divergence visible. Commit `.claude/commands/trace-aop.md`, `finding.yaml`, all four tables, `aop_report.md`, and `provenance.json`. See the [reproducibility guide](../../guide/advanced/reproducibility.html) for the pattern.

**An AOP is dose- and kinetics-free by construction.** It describes the biology once the MIE is engaged; it does not tell you whether your exposure reaches the MIE at the concentration your study used. Anything in the report that reads as a potency claim is not coming from AOP-Wiki.

## Why this assembly

Rung 2. The work is retrieval and structured assembly across AOP-Wiki, PubChemTox and CTD, and the [Adverse Outcome Pathway skill](../../catalog/tools/tooluniverse-adverse-outcome-pathway.html) already encodes the four-phase ordering, the tool names, and an evidence-grading frame. Rung 1 fails on grounding, and it fails invisibly: plain Claude Code will produce a confident, plausibly-ordered key-event chain from pre-training, complete with pathway-sounding names that do not correspond to any AOP-Wiki key event, and nothing about the prose reveals which links were retrieved. Rung 3 would add a second mechanistic source, but every additional retrieval layer widens the report rather than sharpening the verdict, and the verdict is the deliverable.

## Availability

Fully open on licence. ToolUniverse is Apache-2.0; AOP-Wiki, PubChem/PubChemTox and CTD are free public APIs with no account or subscription.

The access bar is **disclosure**. The compound identity and the observed finding are sent to third-party public services, which rules this out for confidential chemistry or an unpublished safety signal. There is no offline substitute — the pathway and toxicogenomics content *is* the databases, so a local mode is not merely absent but not constructible. If the compound cannot leave your machine, you can search AOP-Wiki by endpoint alone (steps 2 and 4–5, which are chemical-agnostic) and simply omit steps 6–8, recording their omission in the report so that a missing chemical-evidence table does not read as a negative result.

## Compute requirements

Laptop. Everything is API-bound and the wall clock is network round-trips: budget a few minutes per finding across the four phases. A broad search term ("liver") returns dozens of candidate pathways and each `AOPWiki_get_aop` call is a separate request, so narrow the term before widening the batch. This recipe takes one finding at a time by design — it is not a screening tool.

## Evidence

Proposed. No documented attempt at this assembly — Claude Code driving the ToolUniverse Adverse Outcome Pathway skill over an observed toxicity — is known, and the skill has not been benchmarked end-to-end. The catalog records it as `verified: works` (2026-07-20), which establishes that the tool calls resolve, not that the graded pathway is correct. The closest evidence is framework- and component-level, and each gate traces to a specific result:

- **Step 4's status gate** reflects the OECD AOP Programme's own position that structured, reviewed development is what builds confidence in an AOP's applicability to decisions, and the fact that the programme runs a coaching effort and "gardening" of redundant key events precisely because AOP-Wiki content quality is uneven ([Tanabe et al. 2025](https://doi.org/10.1093/etojnl/vgaf173)).
- **Step 5's per-KER rule** follows the pragmatic development approach now used in the field, in which the key-event relationship — not the whole pathway — is the essential unit of knowledge from which causality is inferred, and is developed and systematically evidenced on its own ([Holmer et al. 2024](https://doi.org/10.1016/j.reprotox.2024.108662)).
- **Step 6's three-value stressor field** is arithmetic from the current AOP-Wiki metrics: 871 prototypical stressors against 595 AOPs and 1,939 key events (fetched 2026-08-09) means stressor lists are exemplars, not coverage.
- **Step 7's direct-vs-inferred split** is CTD's own distinction. Inferred chemical-disease relationships are generated by chaining a curated chemical-gene statement to a curated gene-disease statement, they grow superlinearly with curation, and CTD built a local-network-topology metric to rank them because their raw volume is not usable as evidence ([King et al. 2012](https://doi.org/10.1371/journal.pone.0046524); [Davis et al. 2009](https://doi.org/10.1093/nar/gkn580)).

## Alternatives considered

**Profile the compound instead of the finding.** If the question is "what is known about this compound's liabilities" rather than "why did this happen", use [triage-a-compound-toxicology-and-hazard-profile](triage-a-compound-toxicology-and-hazard-profile.html), which drives the Chemical Safety skill over a shortlist and touches AOP-Wiki as one retrieval among eight. That recipe is compound-keyed and produces a dossier; this one is finding-keyed and produces a mechanism with a next assay. Run that one first if you have a shortlist and no findings yet.

**Predict endpoint values instead.** [predict-admet-properties-for-a-compound-series](predict-admet-properties-for-a-compound-series.html) gives calibrated per-endpoint predictions across a series and will rank compounds on predicted liability far faster. It cannot tell you *how* — reach for it upstream, when you are choosing which compounds to run, not downstream when one of them has already surprised you.

**Off-target explanations for a clinical signal.** If the finding came from patients rather than a tox study, [scan-adverse-events-for-drug-safety-signal](scan-adverse-events-for-drug-safety-signal.html) and [profile-compound-polypharmacology](profile-compound-polypharmacology.html) address the disproportionality and target-engagement halves of that question respectively; an AOP trace is the mechanistic layer you add after one of those produces a candidate target.

## See also

- [Adverse Outcome Pathway (ToolUniverse Claude Skill)](../../catalog/tools/tooluniverse-adverse-outcome-pathway.html)
- [ToolUniverse](../../catalog/tools/tooluniverse.html)
- [Triage a compound's toxicology and hazard profile](triage-a-compound-toxicology-and-hazard-profile.html)
- [Predict ADMET properties for a compound series](predict-admet-properties-for-a-compound-series.html)
- [Profile compound polypharmacology](profile-compound-polypharmacology.html)
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [AOP-Wiki metrics summary](https://aopwiki.org/metrics_summary) — 595 AOPs, 1,939 key events, 3,168 key-event relationships, 871 prototypical stressors; fetched 2026-08-09 (this run).
- [AOP-Wiki](https://aopwiki.org/) — release 2.8, 2026-03-08; verified 2026-08-09 (this run).
- [Adverse Outcome Pathway (AOP) Coaching Program — how it functions and contributes to a more harmonized approach to AOP development](https://doi.org/10.1093/etojnl/vgaf173) — published 2025; verified 2026-08-09 (this run).
- [Methodology for developing data-rich Key Event Relationships for Adverse Outcome Pathways](https://doi.org/10.1016/j.reprotox.2024.108662) — published 2024; verified 2026-08-09 (this run).
- [Ranking transitive chemical-disease inferences using local network topology in the Comparative Toxicogenomics Database](https://doi.org/10.1371/journal.pone.0046524) — published 2012; canonical statement of CTD's inferred-vs-direct distinction, verified 2026-08-09 (this run).
- [Comparative Toxicogenomics Database: a knowledgebase and discovery tool for chemical-gene-disease networks](https://doi.org/10.1093/nar/gkn580) — published 2009; verified 2026-08-09 (this run).
- [`skills/tooluniverse-adverse-outcome-pathway/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-adverse-outcome-pathway/SKILL.md) — four-phase workflow and tool names confirmed by fetch 2026-08-09 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=trace-adverse-outcome-pathway-for-a-toxicity&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftrace-adverse-outcome-pathway-for-a-toxicity.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
