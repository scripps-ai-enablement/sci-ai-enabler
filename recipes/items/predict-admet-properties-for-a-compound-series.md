---
title: Predict ADMET properties for a compound series with an ML predictor
parent: All recipes
grand_parent: Recipes
nav_order: 41
problem_class: Data analysis
subject_areas: [Chemistry, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-26
summary: Drive the ADMETlab MCP server to batch-predict ~119 ML ADMET endpoints (with uncertainty) for a SMILES series, then commit a triaged CSV, pinned client env, and a provenance record.
---

# Predict ADMET properties for a compound series with an ML predictor

Hand Claude Code a CSV of SMILES; get back a per-compound table of machine-learned ADMET predictions — CYP inhibition, hERG, microsomal clearance, solubility, permeability, and ~110 more endpoints, each with an uncertainty flag — so lead optimization has a defensible ML layer, not just rule-based flags.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Rule-based ADMET filters (Lipinski, Veber, PAINS, BRENK) tell you whether a molecule looks drug-like, but they say nothing quantitative about the endpoints that actually kill programs: CYP isoform inhibition, hERG liability, metabolic clearance, aqueous solubility, oral bioavailability. For those, a medicinal chemist wants a trained model's prediction — ideally with a confidence estimate so borderline calls get flagged rather than trusted blindly.

Doing this by hand means pasting SMILES one at a time into a web form and screenshotting the result — no batch, no provenance, no re-run. Solved looks like: one prompt, a SMILES CSV in, a wide predictions CSV out, with the model version and query date recorded so next quarter's re-run is comparable and every number traces to the endpoint that produced it.

## Recommended approach

Rung 2 of the simplicity ladder — one MCP server. The [ADMETlab MCP server](../../catalog/tools/admetlab-mcp.html) fronts the peer-reviewed ADMETlab 3.0 API (multi-task DMPNN, 119 endpoints, per-prediction uncertainty).

1. **Start the ADMETlab MCP server and register it.** Follow the [catalog page](../../catalog/tools/admetlab-mcp.html) verbatim — it is a long-lived HTTP server you launch with `uvicorn` in its own terminal, then register with `claude mcp add --transport http admetlab http://127.0.0.1:8200/mcp`. Confirm it appears in `/mcp`. No API key is required; predictions are computed by the upstream ADMETlab 3.0 service.

2. **Wash the structures first.** Consistent standardization is what makes the predictions reproducible:

   ```
   I have hits/series_2026Q3.csv with columns: id, smiles.
   Use the ADMETlab MCP wash_molecule tool on each SMILES to
   standardize/clean it. Write the washed set to
   hits/series_2026Q3_washed.csv (columns: id, smiles, washed_smiles);
   drop and report any rows that fail to wash.
   ```

3. **Batch-predict ADMET endpoints.** Drive `predict_admet` over the washed series (batches of up to ~1000 SMILES, ≤5 rps):

   ```
   Using the ADMETlab MCP predict_admet tool on the washed_smiles
   column of hits/series_2026Q3_washed.csv:
     - Predict the full ADMET panel for each compound.
     - Retrieve results as CSV (fetch_admet_csv) and merge back on id.
     - Keep, at minimum, these endpoints as named columns:
         CYP1A2/2C9/2C19/2D6/3A4 inhibition, hERG, HIA, F(20%)/F(30%),
         Caco-2, logS (solubility), CL (clearance), t1/2, PPB, BBB, Ames.
     - Carry through the per-endpoint uncertainty/confidence value
       ADMETlab returns, as <endpoint>_unc columns.
   Write hits/series_2026Q3_admet.csv.
   ```

4. **Capture the analysis as a committed script.** Ask Claude to write the wash→predict→merge flow to a durable artifact, not leave it in chat:

   ```
   Write predict_admet.py that takes an input CSV of id,smiles,
   calls the ADMETlab MCP wash + predict + fetch-CSV steps, and
   emits <input>_admet.csv. Add a triage summary: for each compound,
   flag red/amber/green per endpoint using ADMETlab's documented
   optimal/medium/poor cut-offs, and a rollup "n_red" column.
   Pin the client dependencies in requirements.txt.
   Emit provenance.json recording: ADMETlab MCP server commit/version,
   the ADMETlab 3.0 model version string returned by the API, the
   query date (UTC), input CSV sha256, output row count, and the
   model id used to author the script.
   ```

   Commit `predict_admet.py`, `requirements.txt`, `series_2026Q3_admet.csv`, and `provenance.json`. Because predictions come from a live external service, the recorded query date + model-version string are what make later divergence visible rather than silent — see the [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide.

5. **Interpret only from the saved table.** Any narrative ("compound 7 is the cleanest — green on all five CYPs, amber hERG") must cite the emitted CSV columns, not the model's memory.

## Why this assembly

Rung 2. The prediction is a single MCP call per batch; the value is that ADMETlab 3.0 is a peer-reviewed, widely-used multi-task model with per-prediction uncertainty, so you get ML endpoints (CYP, hERG, clearance) that rule-based filters cannot produce. Plain Claude Code cannot predict these — there is no local model. A multi-tool harness or autonomous system adds nothing: there is one prediction step and no branching decision. The only reason to escalate would be a need for *local* prediction on confidential structures (ADMETlab runs cloud-side), which this recipe cannot satisfy.

## Availability

Fully open. The [ADMETlab MCP server](../../catalog/tools/admetlab-mcp.html) is Apache-2.0, install-from-source (Beta), and requires no registration; it depends on the free public ADMETlab 3.0 API. Data-residency caveat: SMILES are sent to the upstream ADMETlab service — do not use this recipe for structures that cannot leave your network. No local ML-ADMET predictor is catalogued today (see the curator note); until one is, confidential series need a different path.

## Compute requirements

Laptop. The client is I/O-bound: predictions are computed upstream. A 1000-compound batch returns in a few minutes at the ≤5 rps rate limit; larger series scale linearly. No GPU, no local datasets. Expect occasional 5xx/404 passthroughs from the upstream service — the recipe's retry/backoff (built into the MCP server) handles transient failures.

## Evidence

`Reported`. ADMETlab 3.0 is peer-reviewed: Fu et al. (*Nucleic Acids Research* 2024, [doi:10.1093/nar/gkae236](https://doi.org/10.1093/nar/gkae236)) document a multi-task DMPNN over >400,000 entries covering 119 endpoints, with reported accuracy/robustness gains over the prior version and per-prediction uncertainty estimates. The MCP server (`ToxMCP/admetlab-mcp`) wraps that API's wash / predict / CSV endpoints. No peer-reviewed head-to-head benchmark of "Claude + ADMETlab MCP" against a hand-written API client is known; the agent loop adds reproducibility and provenance, not new predictive capability. The predictor itself is the evidence — treat predictions as model estimates with the uncertainty flag attached, not measurements.

## Alternatives considered

- **Rule-based triage first — [Filter a virtual screening hit list](filter-virtual-screening-hits.html).** Cheaper and offline; catches gross liabilities. Run it upstream to shrink the series, then use this recipe for the ML endpoints rules cannot produce.
- **Descriptor / analog anchoring — [Estimate PK properties of a small molecule](estimate-pk-properties.html).** No ML predictor in the loop; every number traces to a descriptor, a named rule, or a measured ChEMBL neighbour. Reach for it on a single compound earning deep, fully-traceable review, or when structures cannot leave your network.
- **Benchmarking rather than predicting — [Benchmark an ADMET property with PyTDC](benchmark-admet-property-with-pytdc.html).** Use PyTDC when you are training/comparing your *own* ADMET model against a leaderboard, not scoring your compounds.
- **Enterprise-hosted ADMET.** The [Inductive Bio ADMET connector](../../catalog/tools/inductive-bio.html) offers a zero-install, hosted path in Claude.ai for teams that need managed governance; it is not fully open.

## See also

- [ADMETlab MCP Server](../../catalog/tools/admetlab-mcp.html)
- [Filter a virtual screening hit list with drug-likeness rules and structural alerts](filter-virtual-screening-hits.html)
- [Estimate pharmacokinetic properties of a small molecule](estimate-pk-properties.html)
- [Benchmark an ADMET property with PyTDC](benchmark-admet-property-with-pytdc.html)

## Sources

- [Fu L. et al., "ADMETlab 3.0: an updated comprehensive online ADMET prediction platform," *Nucleic Acids Research* 2024](https://doi.org/10.1093/nar/gkae236) — published 2024; verified 2026-07-26 (this run).
- [`ToxMCP/admetlab-mcp`](https://github.com/ToxMCP/admetlab-mcp) — per catalog page, verified 2026-07-26.
- [ADMETlab 3.0 web server](https://admetlab3.scbdd.com/) — verified 2026-07-26 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=predict-admet-properties-for-a-compound-series&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fpredict-admet-properties-for-a-compound-series.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
