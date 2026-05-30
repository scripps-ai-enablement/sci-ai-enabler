---
title: Match a patient summary to recruiting clinical trials
parent: All recipes
grand_parent: Recipes
nav_order: 11
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-23
summary: Use BioMCP (or the standalone ClinicalTrials.gov MCP) to take a free-text patient summary and return a ranked list of currently-recruiting trials with eligibility rationale.
---

# Match a patient summary to recruiting clinical trials

Hand Claude a de-identified one-paragraph patient summary; get back a short list of actively-recruiting trials on ClinicalTrials.gov with a per-criterion eligibility rationale for each.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Clinical-trial pre-screening is the single most time-consuming step in patient recruitment. A clinician or research coordinator reads a case summary, mentally lists the relevant trials, then opens ClinicalTrials.gov and reads eligibility blocks one by one. For a single advanced-disease patient with multiple co-morbidities, this is 30–90 minutes of clerical work per encounter. Solved looks like: paste the patient paragraph, get a ranked short list of trials with the inclusion/exclusion criteria already scored against the patient's known attributes, including which criteria need follow-up because the paragraph doesn't say. The agent is not making the enrollment decision — it is collapsing the screen-out step so the clinician can spend their time on the borderline cases.

## Recommended approach

1. **Install one MCP server.** The simplest path is [BioMCP](../../catalog/tools/biomcp.html) (covers trials, variants, PubMed, OpenFDA in one server):

   ```
   uv tool install biomcp-cli
   claude mcp add --transport stdio biomcp -- biomcp run
   ```

   If you only need trial matching (no variant or literature lookups), the [ClinicalTrials.gov MCP Server](../../catalog/tools/clinicaltrials-gov-mcp.html) is lighter-weight and has a hosted public instance — no install at all:

   ```
   claude mcp add --transport http clinicaltrials https://clinicaltrials.caseyjhand.com/mcp
   ```

2. **Prompt Claude with the patient summary and the matching task.** A minimal version:

   ```
   I have a de-identified patient summary. Use the clinicaltrials MCP
   (or BioMCP trial_searcher) to find currently RECRUITING trials that
   may fit. Steps:

   1. Extract from the summary: primary condition, disease stage / line
      of therapy, key prior treatments, key biomarkers/variants, age,
      ECOG/performance status, and any disqualifying co-morbidities.
   2. Search recruiting trials with conditions and intervention terms
      derived from step 1. Expand condition synonyms.
   3. For the top 10 matches by relevance, fetch the full eligibility
      criteria. Score each criterion as MET / NOT MET / UNKNOWN against
      the patient summary. Cite the NCT ID and the exact criterion
      text for each.
   4. Rank trials by (count of MET criteria) - (count of NOT MET) and
      return the top 5 with a one-paragraph rationale and the list of
      UNKNOWN criteria the clinician still needs to check.

   Patient summary:
   <paste paragraph here>
   ```

3. **Sanity-check the locations.** Trials list multiple sites; for a usable shortlist, follow up with the MCP's `trial_locations_getter` (cyanheads server) or `trial_searcher`'s location filter (BioMCP) to keep only sites within the patient's catchment.

4. **Save as a slash command.** Once a prompt works on a few cases, register it as `/match-trials` and parameterize on the patient summary.

## Why this assembly

Rung 2 of the simplicity ladder. The whole task is structured retrieval and per-criterion reasoning against a single API (ClinicalTrials.gov v2). One MCP server is enough; no skill chaining, no autonomous-science loop. Escalating to a rung-4 system (Biomni) would technically work but adds orchestration overhead for a problem one tool can solve. Claude Code alone (rung 1) is not enough — without an MCP, the model cannot query the live ClinicalTrials.gov database and will hallucinate NCT IDs.

## Availability

Fully open. ClinicalTrials.gov v2 API is public and unauthenticated. Both BioMCP and the cyanheads ClinicalTrials.gov MCP are OSS (MIT and Apache-2.0 respectively). The cyanheads hosted instance is free; for PHI-adjacent workflows, self-host (local stdio or Cloudflare Workers deploy) rather than using the public endpoint.

## Compute requirements

Laptop-sufficient. Both servers are thin API wrappers; per-query latency is dominated by ClinicalTrials.gov itself (typically < 2 s). A 10-trial scoring pass usually fits in a single Claude turn.

## Evidence

Reported. The TrialGPT framework ([Jin et al., *Nature Communications* 2024](https://www.nature.com/articles/s41467-024-53081-z)) is the closest validated reference for the assembly *class*: an LLM scoring patient–criterion pairs against ClinicalTrials.gov. TrialGPT-Matching achieved 87.3% accuracy on 1,015 patient-criterion pairs (vs human experts at 88.7–90%), recalled ≥ 90% of relevant trials while reading < 6% of the corpus, and reduced clinician screening time by 42.6% in a user study. TrialGPT used a bespoke GPT-4 pipeline, not BioMCP, but the underlying data source (ClinicalTrials.gov) and the per-criterion scoring pattern are the same. MatchMiner-AI ([Dana-Farber, *arXiv* 2024](https://arxiv.org/abs/2412.17228)) reports 0.94–0.98 AUROC for cancer patient-trial eligibility classification using a similar LLM-over-ClinicalTrials.gov design. No published benchmark is known for the BioMCP or cyanheads MCP servers specifically; treat the assembly as evidence-backed by analogy.

## Alternatives considered

- **Claude Code alone (rung 1).** Will not work end-to-end — without an MCP the model has no access to live trial records and will fabricate NCT IDs. Useful only for re-formatting an already-fetched JSON.
- **Biomni (rung 4).** [Biomni](../../autonomous-science/systems/biomni.html) bundles ClinicalTrials.gov-class tools alongside dozens of other biomedical databases. Reach for it when the trial match is one step of a larger autonomous workflow (e.g., variant interpretation → drug-target mapping → trial lookup). For one-shot trial matching, the rung-2 MCP is simpler and easier to audit.
- **TrialGPT directly.** [`ncbi-nlp/TrialGPT`](https://github.com/ncbi-nlp/TrialGPT) is publicly available code. Reach for it if you want the exact pipeline from the paper (retrieval, matching, ranking modules separately wired) and are running large batch jobs. For interactive case-by-case work inside Claude Code, the MCP path is lower-friction.

## See also

- [BioMCP](../../catalog/tools/biomcp.html)
- [ClinicalTrials.gov MCP Server (cyanheads)](../../catalog/tools/clinicaltrials-gov-mcp.html)
- [clinical-trial-protocol plugin](../../catalog/tools/clinical-trial-protocol.html) — the upstream task: drafting a protocol that defines the eligibility criteria scored here.
- [Biomni](../../autonomous-science/systems/biomni.html) — autonomous-system alternative.
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — pairs naturally when a variant drives trial eligibility.

## Sources

- [Jin et al., "Matching patients to clinical trials with large language models," *Nature Communications* 15:9074](https://www.nature.com/articles/s41467-024-53081-z) — published 2024-11-18; verified 2026-05-23 (this run).
- [`cyanheads/clinicaltrialsgov-mcp-server`](https://github.com/cyanheads/clinicaltrialsgov-mcp-server) — verified 2026-05-23 (this run).
- [biomcp.org `trial_searcher` docs](https://biomcp.org/) — verified 2026-05-23 (this run).
- [MatchMiner-AI preprint](https://arxiv.org/abs/2412.17228) — published 2024-12; analogous benchmark.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=match-patient-to-clinical-trials&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fmatch-patient-to-clinical-trials.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
