---
title: Source purchasable compounds for a hit list
parent: All recipes
grand_parent: Recipes
nav_order: 25
problem_class: Knowledge synthesis
subject_areas: [Chemistry, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-02
summary: Drive the ToolUniverse Chemical Sourcing skill to turn a shortlist of SMILES into a per-listing procurement table with purity, lead time, and analog fallbacks.
---

# Source purchasable compounds for a hit list

Your virtual screen produced forty compounds worth testing. Drive the ToolUniverse Chemical Sourcing skill to find out which ones you can actually buy, at what purity and lead time, and what to order instead when the answer is nothing.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Between a ranked hit list and a plate of compounds sits a procurement problem that quietly decides what the experiment actually tests. Some hits are in stock and arrive in a week. Some are make-on-demand and arrive in a month, or never. Some are listed by three vendors at prices differing tenfold because two of them are shipping a different salt form. Some have no purity figure at all. And doing this by hand — vendor site by vendor site, compound by compound — is the step where a computational hit list goes stale for six weeks.

The failure mode is not "we couldn't find a vendor." It is buying the wrong thing and not knowing: a name-matched compound that is a different stereoisomer, a 90%-pure lot used for a dose-response assay, or an analog silently swapped in for the compound the model actually scored. "Solved" looks like a committed procurement table where every row is a *listing* with its vendor, price per mg, purity, and stock status; a separate list of compounds nothing can be bought for; and analogs kept in their own file so nobody mistakes a substitution for the original hypothesis.

## Recommended approach

1. **Install the ToolUniverse MCP server, then the Chemical Sourcing skill** ([catalog page](../../catalog/tools/tooluniverse-chemical-sourcing.html)). The skill drives ToolUniverse tool calls, so register the server first:

   ```
   claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
   npx skills add mims-harvard/ToolUniverse
   ```

   The skill sets `disable-model-invocation: true`, so invoke it explicitly.

2. **Commit the hit list as `hits.csv`, keyed on SMILES rather than name.** One row per compound: `compound_id`, `smiles`, `intended_assay`, `mg_needed`, `rank`. Search by SMILES, not by name — names map ambiguously onto salt forms, stereoisomers, and tautomers, and a name-matched purchase is the most common way to receive the wrong molecule. If your upstream step produced only names, resolve them to canonical SMILES first and keep both columns so the resolution is auditable.

3. **Declare the purity floor from the intended assay, not from the price.** The skill applies ≥ 95% for screening, ≥ 98% for dose-response, and ≥ 99% for reference standards; put `intended_assay` in the input so the floor is derived per compound rather than applied globally. This is not a formality: analytical QC of the 8,900-compound Tox21 library found that of the samples that could be graded, only **76% exceeded 90% purity**, and on retest after four months in DMSO **11% showed evidence of loss or degradation** ([Richard et al., *Chem. Res. Toxicol.* 2025](https://doi.org/10.1021/acs.chemrestox.4c00330)). A curated, heavily used public library is that noisy; a cheap vendor lot with no purity figure is worse.

4. **Commit the query as `.claude/commands/source-compounds.md`** so the whole list gets one rule set:

   ```markdown
   Use the chemical-sourcing skill on $ARGUMENTS (a CSV: compound_id,
   smiles, intended_assay, mg_needed, rank).

   For each row:
     1. Resolve identity from the SMILES (PubChem CID + canonical
        SMILES). Record the canonical SMILES you got back.
     2. Search ZINC, Enamine, eMolecules, and Mcule.

   Write sourcing.csv with ONE ROW PER LISTING, not per compound:
     compound_id, vendor, vendor_catalog_id, listed_smiles, price,
     currency, pack_size_mg, price_per_mg, purity_pct,
     availability (in_stock | make_on_demand | unknown),
     lead_time_weeks, purity_floor_required, meets_purity_floor.

   Do not collapse in_stock and make_on_demand into one
   "available" value. Do not average prices across listings.

   Write these as separate files, each a first-class result:
     - no_source.csv    - compound_id with no listing anywhere
     - smiles_mismatch.csv - listed_smiles differs from the query
       canonical SMILES (report both strings)
     - missing_purity.csv  - listings with no purity figure
     - price_outliers.csv  - listings above 5x the median
       price_per_mg for that compound (probable different salt
       form or purity grade)
     - analogs.csv - only where the exact compound is not
       purchasable: query compound_id, analog SMILES, Tanimoto
       (>= 0.7), vendor, availability, and any ChEMBL bioactivity
       context for the analog.

   Never merge analogs.csv into sourcing.csv.

   Cite only values you retrieved from a catalog. Do not state a
   price, purity, or stock status you did not read back from a
   tool call.
   ```

   Run it as `/source-compounds hits.csv`.

5. **Treat the in-stock / make-on-demand split as a fork in the experiment, not a shipping detail.** Make-on-demand libraries are where the novel chemistry lives — over **97% of the core Bemis–Murcko scaffolds in make-on-demand collections are unavailable from in-stock collections**, and an 88-fold increase in molecules over in-stock sets rests on a 16-fold increase in distinct scaffolds ([Irwin et al., *J. Chem. Inf. Model.* 2020](https://doi.org/10.1021/acs.jcim.0c00675)). So a hit list that filters to in-stock only is systematically restricted to well-trodden scaffolds; a hit list that ignores lead times will sit idle for a month. Decide explicitly, per compound, and record the decision in an `order_decision` column.

6. **Read the four exception files before the main table.** `smiles_mismatch.csv` is the one that costs a whole experiment — a vendor listing whose structure does not round-trip to your query SMILES is a different compound until the supplier confirms otherwise. `no_source.csv` is a legitimate result to publish: it is the reason a top-ranked docking hit was never tested, and reviewers ask. Confirm anything in `missing_purity.csv` or `price_outliers.csv` with the vendor before ordering.

7. **Timestamp everything, because this is the most perishable data in the cookbook.** Prices, stock status, and lead times are whatever the catalogs said at query time and can change within days. Write `provenance.json` with the **UTC query date**, ToolUniverse version, the repo commit SHA the skill came from, the sha256 of `hits.csv`, the purity floors and Tanimoto floor used, and the model id. Commit `.claude/commands/source-compounds.md`, `hits.csv`, `sourcing.csv`, the exception files, and `provenance.json` together; re-run the command rather than editing the table when a quote goes stale. See [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html).

8. **Get a written quote before you buy.** The table is a shortlist to confirm, not an order. Treat vendor-reported purity and delivery as claims to verify, especially for anything going into a dose-response assay.

## Why this assembly

Rung 2 of the simplicity ladder. Four vendor catalogs, identity resolution, price normalization per mg, and the analog fallback all ship as ToolUniverse tool calls, and the skill is the layer that sequences them and applies the purchasing rules — one skill plus its MCP server solves the problem, so stop here. Rung 1 (Claude Code alone) has no catalog access at all and would have to be told prices, which is how hallucinated availability gets into a procurement decision. Rung 3 would add a structure-cleanup tool such as [Datamol](../../catalog/tools/datamol.html) for standardizing messy input SMILES; add it only if your hit list comes in dirty, and keep it upstream of this recipe rather than inside it.

## Availability

Fully open with one caveat that matters more than the licence. ToolUniverse is Apache-2.0 and the vendor catalogs it queries (ZINC, Enamine, eMolecules, Mcule) are publicly searchable, so there is no subscription gate.

The caveat is disclosure: **your query SMILES leave the machine.** Searching a commercial catalog for an unpublished hit tells a vendor which structures you are interested in. For confidential chemistry, confirm your organization's policy before running this against a proprietary hit list — this is a different risk from the compute-local recipes in this section, and there is no offline substitute in the catalog because the data you need lives in the vendors' inventories.

## Compute requirements

Laptop. Every step is an API call; nothing is computed locally and no GPU is involved. Wall-clock scales with the number of compounds times four catalogs, so a forty-compound list is minutes and a five-hundred-compound list is long enough to hit rate limits — batch it in chunks of a few dozen and append to `sourcing.csv` incrementally so a mid-run failure does not lose the work.

## Evidence

Proposed. No documented attempt of this specific Claude-driven ToolUniverse Chemical Sourcing assembly on a real hit list is known, and the skill is not benchmarked. The grounding is that each rule the recipe enforces exists because a measured failure motivates it:

- **The purity floor.** Analytical QC across the Tox21 10K library (LC-MS, GC-MS, NMR on >13,000 sample identifiers) graded 92% of baseline samples, of which only 76% exceeded 90% purity; 11% of retested samples showed loss or degradation after four months in DMSO at ambient conditions, and structural features enriched in unstable compounds were identifiable ([Richard et al., *Chem. Res. Toxicol.* 2025](https://doi.org/10.1021/acs.chemrestox.4c00330)). Poor-quality samples produce both false positives and false negatives in screening, which is the reason purity is a gate and not a footnote.
- **The in-stock / make-on-demand split.** Quantified in the ZINC20 analysis: >97% of core Bemis–Murcko scaffolds in make-on-demand libraries are absent from in-stock collections, and make-on-demand sets are more structurally diverse in shape space ([Irwin et al., *J. Chem. Inf. Model.* 60(12):6065–6073, 2020](https://doi.org/10.1021/acs.jcim.0c00675)). Restricting to in-stock is a chemical-space decision, not a logistics one.
- **The identity-first, SMILES-not-name rule and the 5×-median price flag** are documented behaviours of the skill itself, in its `SKILL.md`, along with the ≥ 95 / 98 / 99% purity tiers and the Tanimoto ≥ 0.7 analog fallback.

What is unvalidated is the agent-driven path specifically: nobody has published a comparison of this assembly against a chemist working through the vendor sites by hand, and vendor catalog coverage through ToolUniverse may lag the vendors' own search interfaces.

## Alternatives considered

- **Searching the vendor sites or ZINC directly.** For one or two compounds this is faster than installing anything, and it is what you should do to confirm a quote. The recipe earns its keep from about ten compounds upward, where the per-compound cost of four catalog lookups plus price normalization plus the mismatch check stops being worth a human's afternoon.
- **The [Small Molecule Discovery skill](../../catalog/tools/tooluniverse-small-molecule-discovery.html).** It covers commercial availability as one phase of a broader compound workup. Reach for it when procurement is a detail inside a larger question about a molecule; reach for this recipe when procurement *is* the question and you need a per-listing table.
- **Buying out an analog series instead of individual hits.** If the goal is SAR rather than testing specific predictions, run [Enumerate analogs around a lead](enumerate-analogs-around-a-lead.html) first and source the enumerated set, using `analogs.csv` as the primary output rather than the exception file.
- **Skipping procurement entirely.** If the hit list has not yet been filtered for chemical plausibility, source *after* filtering, not before — see [Filter virtual screening hits](filter-virtual-screening-hits.html). Sourcing a list you are about to cut is wasted API calls and wasted attention.

## See also

- [Chemical Sourcing (ToolUniverse Claude Skill)](../../catalog/tools/tooluniverse-chemical-sourcing.html)
- [ToolUniverse (MCP server)](../../catalog/tools/tooluniverse.html)
- [ZINC (database)](../../catalog/tools/zinc-database.html)
- [Filter virtual screening hits](filter-virtual-screening-hits.html) — the upstream cut that should happen first.
- [Enumerate analogs around a lead](enumerate-analogs-around-a-lead.html) — when the analog file is the point.
- [Fit a dose-response curve and report a defensible IC50](fit-dose-response-curve-to-ic50.html) — the assay whose ≥ 98% purity floor step 3 is protecting.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse) — component facts deferred to the catalog page, `last_verified` 2026-08-02.
- [`skills/tooluniverse-chemical-sourcing/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-chemical-sourcing/SKILL.md) — via catalog page, verified 2026-08-02 (this run).
- [Richard AM et al. "Analytical Quality Evaluation of the Tox21 Compound Library." *Chemical Research in Toxicology* (2025)](https://doi.org/10.1021/acs.chemrestox.4c00330) — published 2025; retrieved 2026-08-02 (this run).
- [Irwin JJ et al. "ZINC20 — A Free Ultralarge-Scale Chemical Database for Ligand Discovery." *J. Chem. Inf. Model.* 60(12):6065–6073 (2020)](https://doi.org/10.1021/acs.jcim.0c00675) — published 2020; retrieved 2026-08-02 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=source-purchasable-compounds-for-a-hit-list&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fsource-purchasable-compounds-for-a-hit-list.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
