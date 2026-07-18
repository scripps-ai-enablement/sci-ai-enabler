---
title: Plan a synthetic route for a target molecule
parent: All recipes
grand_parent: Recipes
nav_order: 18
problem_class: Experimental design
subject_areas: [Chemistry, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Subscription required
compute_requirements: Laptop
last_verified: 2026-07-18
summary: Drive the CovaSyn MCP retrosynthesis suite from Claude Code to propose buyable-starting-material routes to a target SMILES and capture them as a reproducible route table.
---

# Plan a synthetic route for a target molecule

Hand Claude Code a target SMILES; get back one or more retrosynthetic routes back to purchasable starting materials, each disconnection recorded with its precursors — captured as a durable route table rather than a one-off chat answer.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Subscription required |
| **Compute** | Laptop |

## Problem

A medicinal chemist who has just designed or selected a compound — a virtual-screening hit, an enumerated analog, a de-novo idea — immediately faces the make question: *can this actually be synthesised, and from what?* Retrosynthetic analysis works backward from the target through plausible disconnections until every leaf is a commercially available (buyable) building block. Doing it by hand is slow and biased toward the reactions the chemist already knows; doing it in a generic chatbot invites plausible-looking but chemically invalid routes (unbalanced steps, non-existent reagents, precursors nobody sells).

Solved looks like: a target SMILES in, a small set of ranked routes out, each step naming precursor SMILES and the transform class, with the leaf building blocks flagged as buyable — reproducibly, on a laptop, so the route table can be handed to a synthetic chemist for a reality check and committed alongside the design that produced it.

## Recommended approach

1. **Install the [CovaSyn Chemistry MCP](../../catalog/tools/covasyn.html)** and set an API key. CovaSyn's `covaplatform` suite runs the retrosynthesis models cloud-side; a free-tier key (100 credits/week) covers a handful of targets.

   ```
   claude mcp add --transport stdio covasyn --env COVASYN_API_KEY=your_api_key_here --env COVASYN_API_BASE=https://api.covasyn.com -- npx -y @covasyn/mcp-client
   ```

   Confirm the server starts and the retrosynthesis tool is listed before running a target.

2. **(Optional, local) clean the target SMILES first with the [RDKit skill](../../catalog/tools/rdkit-skill.html) or [Datamol skill](../../catalog/tools/datamol.html).** Strip salts, keep the largest fragment, and canonicalize so the retrosynthesis call operates on a well-formed parent. Skip it for a hand-drawn, already-clean target.

3. **Write the route search to a versioned script.** Have Claude Code author `plan_route.py` — do not leave the workflow as an interactive chat. A minimal prompt:

   ```
   Input: targets.csv with columns id, smiles.

   Write plan_route.py that, for each row:
     1. (if rdkit available) canonicalize the SMILES: largest
        fragment, neutralize, canonical SMILES.
     2. Call the covasyn retrosynthesis tool (covaplatform suite)
        on the canonical SMILES, requesting up to N routes with a
        max depth (e.g. N=3 routes, depth<=5).
     3. For each returned route, record every step: step index,
        product SMILES, precursor SMILES, transform/reaction class,
        and whether each leaf precursor is flagged buyable.
     4. Score each route by (number of steps, count of non-buyable
        leaves) so shorter fully-buyable routes rank first.
   Emit routes.csv (one row per step, keyed by id + route_id) and
   route_summary.csv (one row per route: id, route_id, n_steps,
   n_nonbuyable_leaves, rank). Print id -> best route (n_steps,
   all-buyable?) per target.
   ```

   Cache retrieved routes by the target InChIKey so a re-run does not re-submit and re-spend credits.

4. **Record provenance.** Emit `provenance.json` capturing the CovaSyn MCP/registry version, the retrosynthesis model/suite identifier, the building-block catalog/snapshot the buyable flags came from, the request parameters (N routes, max depth), the run date, the sha256 of `targets.csv` and the output CSVs, and the model id driving the session. Cloud results are not byte-reproducible — the recorded version, catalog snapshot, and date make a later divergence visible.

5. **Hand off for a human reality check.** `route_summary.csv` + `routes.csv` are the durable artifacts; a synthetic chemist should sanity-check the top routes before anyone orders reagents. Commit `plan_route.py`, a pinned `requirements.txt`, both CSVs, and `provenance.json` to version control. This recipe pairs naturally downstream of [Enumerate analogs around a lead](enumerate-analogs-around-a-lead.html) (make-check the analogs you propose) and [Filter virtual-screening hits](filter-virtual-screening-hits.html). Follow the [reproducibility guide](../../guide/advanced/reproducibility.html) for the artifact layout.

## Why this assembly

Rung 2 of the simplicity ladder. Retrosynthetic route search needs a real transform/template model plus a buyable-building-block catalog — Claude-Code-alone (rung 1) can *narrate* a route but cannot check that each disconnection corresponds to a known reaction or that the leaves are actually purchasable, so it fabricates plausible-but-wrong routes. The [CovaSyn MCP](../../catalog/tools/covasyn.html) `covaplatform` retrosynthesis tool closes that gap in a single server. A rung-3 toolbelt adds nothing here — no second cataloged component contributes to the route search itself (the optional RDKit/Datamol clean is a pre-step, not a second essential tool). Rung 4 (a full autonomous chemist) is warranted only when the route must be *executed* and iterated in a closed loop, or when hard synthesis constraints must be enforced during search — see **Alternatives considered**.

## Availability

Subscription required. CovaSyn is freemium: a free account gives 100 credits/week (enough for a handful of targets); sustained use needs a paid plan (Pro €250/mo and up). SMILES are submitted to CovaSyn's servers (EU-hosted by default, US available), so for confidential structures treat this as a data-residency caveat and confirm your project's policy before submitting. The example MCP client is MIT-licensed but the CovaSyn service itself is commercial. The optional [RDKit skill](../../catalog/tools/rdkit-skill.html) / [Datamol skill](../../catalog/tools/datamol.html) pre-clean is free and local.

## Compute requirements

Laptop. All route search runs cloud-side on CovaSyn; your machine only submits and polls, and the optional RDKit/Datamol canonicalization is sub-second per molecule on a single CPU core. Budget credits, not hardware: a single-target retrosynthesis request typically returns in under a minute and consumes a few credits; a 20-target batch fits inside the free weekly allotment if you cache by InChIKey. No GPU, negligible local RAM.

## Evidence

Reported. LLM-agent-driven retrosynthesis under practical constraints has been benchmarked at approaching human-expert level: [LARC (Baker et al., *arXiv* 2508.11860, 2025-08-16)](https://arxiv.org/abs/2508.11860) — the first LLM-agentic constrained-retrosynthesis framework — reached a **72.9% success rate on 48 curated constrained-retrosynthesis tasks across 3 constraint types**, vastly outperforming LLM baselines and approaching expert success in substantially less time. The broader pattern — an LLM that plans and calls expert chemistry tools (including retrosynthesis) rather than answering from parametric memory — is the design validated by [ChemCrow (Bran et al., *Nat. Mach. Intell.* 2024)](https://doi.org/10.1038/s42256-024-00832-8), whose synthesis-planning tasks were graded by expert chemists above an unaugmented GPT-4 baseline. What is *not* separately benchmarked is this exact assembly: Claude Code driving the CovaSyn retrosynthesis tool. The evidence therefore supports the *pattern* (tool-grounded agentic retrosynthesis beats ungrounded LLM answers) and the *component* (CovaSyn's retrosynthesis suite), not a head-to-head on the specific pairing. Treat the route table as a ranked set of hypotheses for a synthetic chemist to vet, not a validated protocol.

## Alternatives considered

- **Plain Claude Code, no tool (rung 1).** It will happily narrate a retrosynthesis, but with no transform model or building-block catalog it cannot verify that each step is a real reaction or that the leaves are buyable. Use it only to *reason about* a route a tool already produced, never to generate one you will act on.
- **[ChemCrow](../../autonomous-science/systems/chemcrow.html) (rung 4).** A GPT-4-driven agent wrapping ~18 chemistry tools, including retrosynthesis and *reaction execution* on automated hardware. Reach for it when the route must be planned *and executed/iterated* in a closed loop, or when you want the agent to also handle property lookup and literature checks around the synthesis. It is heavier to set up and harder to audit per route than the single-MCP recipe; for planning-only, CovaSyn alone is the lower rung.
- **A constrained-retrosynthesis agent (LARC-style).** When routes must satisfy hard constraints (avoid a reagent class, stay within a reaction whitelist, meet a step-count ceiling), a framework with an in-loop constraint judge like [LARC](https://arxiv.org/abs/2508.11860) is the right tool. It is not currently a Claude-installable component in [`catalog/tools/`](../../catalog/); a note is filed for the catalog curator. Until then, enforce simple constraints by post-filtering the CovaSyn `routes.csv`.

## See also

- [CovaSyn Chemistry MCP](../../catalog/tools/covasyn.html)
- [ChemCrow](../../autonomous-science/systems/chemcrow.html) — the rung-4 autonomous alternative when routes must also be executed.
- [Enumerate analogs around a lead](enumerate-analogs-around-a-lead.html) — the upstream design step whose analogs this recipe make-checks.
- [Filter virtual-screening hits](filter-virtual-screening-hits.html) — another upstream source of the compounds you want to synthesise.
- [RDKit (Claude Skill)](../../catalog/tools/rdkit-skill.html) — the optional local SMILES canonicalization pre-clean.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the artifact + provenance pattern this recipe follows.

## Sources

- [CovaSyn Chemistry MCP catalog page](../../catalog/tools/covasyn.html) — documents the `covaplatform` retrosynthesis suite; verified 2026-07-18 (this run).
- [Baker et al., "LARC: Towards Human-level Constrained Retrosynthesis Planning through an Agentic Framework," *arXiv* 2508.11860 (2025)](https://arxiv.org/abs/2508.11860) — published 2025-08-16; verified 2026-07-18 (this run).
- [Bran et al., "Augmenting large language models with chemistry tools," *Nat. Mach. Intell.* (2024)](https://doi.org/10.1038/s42256-024-00832-8) — published 2024.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=plan-a-synthetic-route-for-a-target-molecule&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fplan-a-synthetic-route-for-a-target-molecule.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
