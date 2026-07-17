---
title: Generate falsification-tested drug-repurposing hypotheses across corpora
parent: All recipes
grand_parent: Recipes
problem_class: Hypothesis generation
subject_areas: [Drug Repurposing and Discovery, Neuroscience, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: Autonomous system
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-17
summary: Use the Hypothesis Crucible plugin to mine typed knowledge fragments from literature, Open Targets/ChEMBL/ClinicalTrials, and raw experimental data (GEO), bridge them Swanson-style into candidate drug-disease connections, then aggressively reject the non-novel, ungrounded, contradicted, and implausible — surfacing only survivors with a fragment-cited mechanism and a falsifiable experiment.
---

# Generate falsification-tested drug-repurposing hypotheses across corpora

Point the Hypothesis Crucible plugin at a disease and get back a short list of repurposing candidates that no single source proposes, each assembled from fragments spanning multiple bodies of evidence, screened by a falsification gauntlet, and delivered with the citations, the proof that the connection is novel, and the experiment that would kill it.

| | |
|---|---|
| **Problem class** | Hypothesis generation |
| **Subject areas** | Drug Repurposing and Discovery, Neuroscience, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | Autonomous system |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

The hard part of computational hypothesis generation is not producing ideas — an LLM will produce a plausible-sounding drug–disease link for almost any pair — but producing ideas that are simultaneously **novel** (not already in the literature), **grounded** (every mechanistic step traceable to real evidence), and **not already falsified** (no failed trial, no contradicting data, no pharmacological showstopper). Naïve prompting fails all three: it confabulates mechanisms, re-proposes approved indications as if new, and ignores the Phase III graveyard. What you want instead: hand over a disease, get back a handful of candidates where each one arrives with a mechanistic chain whose every link cites a real fragment (a PMID, a GEO series, a ChEMBL mechanism, an Open Targets association), a record of the searches that confirm no one has published the direct claim, the disconfirming evidence that was sought and did not sink it, and a discriminating experiment — plus a full log of everything that was rejected and why.

## Recommended approach

1. **Install the [Hypothesis Crucible plugin](../../catalog/tools/hypothesis-crucible.html)** and connect the bio-research MCP servers it drives:

   ```
   /plugin marketplace add scripps-ai-enablement/sci-ai-enabler
   /plugin install crucible
   ```

   Connect `pubmed`, `ot`, `chembl`, `c-trials`, `biorxiv`, `consensus`, `biomcp`, and `tooluniverse` via `/mcp`; GEO is reached through the `gget` skill / `tooluniverse`.

2. **Run the forge command with your goal:**

   ```
   /crucible:forge "repurposable approved drugs for Alzheimer's disease"
   ```

   The skill frames the goal to an EFO/MONDO id, mines typed fragments across the three source tiers, discovers Swanson-style A–C bridges (no direct edge, ≥2 independent B-paths across ≥2 corpora), and runs each candidate through the falsification gauntlet.

3. **Read the kill tally, not just the survivors.** The run streams how many candidates each gate removed — G1 novelty (already published), G2 groundedness (a hallucinated mechanistic step), G3 contradiction (a failed trial or opposing signature), G4 plausibility (e.g. no blood–brain-barrier penetration). A healthy run kills most of what it considers; that aggressive rejection is the point, and the `kill-log.jsonl` is the audit trail.

4. **Take delivery of the run bundle.** The durable artifact is a directory (`./crucible-runs/<goal>-<date>/`) holding `hypotheses.json` (survivors, each with a fragment-cited chain + novelty evidence + falsification record + a discriminating test), `kill-log.jsonl`, `fragments.jsonl`, `provenance.json`, and an IEEE-2791 `run.bco.json`. This is what you commit and share — not the chat.

5. **Hand a survivor downstream.** Pass a candidate to the [composer](../../catalog/tools/composer.html) to design its wet-lab experiment, or export the top candidates as the input to an experimental validation loop. Crucible is a high-precision *filter* that sits upstream of validation.

6. **For a time-sliced sanity check, run the evaluation.** The [worked example](../examples/hypothesis-crucible/) ships a deterministic scorer and gold fixtures (`eval/score.py`, `eval/gold/`) that measure rediscovery recall, planted-negative kill rate, per-gate attribution, and groundedness against a captured run — the protocol for deciding whether the gauntlet actually earns its place before trusting a run.

## Why this assembly

Rung 4 of the simplicity ladder, and it earns it. Rung 1 (plain Claude) confabulates mechanisms and novelty; rung 2 (a single hypothesis-generation skill) produces ungrounded ideas with no rejection stage; rung 3 (a toolbelt of literature + database MCPs) gets you the fragments but not the bridge discovery, the aggressive falsification gauntlet, or the provenance-bound capture. The distinctive work here — Swanson-style cross-corpus bridging, four independent veto gates that log every kill, and an auditable run bundle — is an orchestrated multi-agent loop, which is what rung 4 is for. It is deliberately narrower than an end-to-end autonomous scientist: it generates and *filters* candidates rather than validating them experimentally.

## Availability

Fully open. The plugin ships in this repository's marketplace; the MCP servers it drives are the open `bio-research` set (PubMed, Open Targets, ChEMBL, ClinicalTrials.gov, bioRxiv, Consensus, BioMCP, ToolUniverse). No subscription. GEO access is via the OSS `gget` library / public NCBI endpoints. Some literature full text may sit behind publisher access, in which case the skill falls back to abstracts.

## Compute requirements

Laptop. The workflow is API/MCP calls and model reasoning; no GPU, no large downloads. Wall-clock is dominated by the number of candidates run through the gauntlet and any tournament rounds, typically minutes to tens of minutes for a single disease goal.

## Evidence

Proposed. This is a freshly composed assembly, screened but not yet validated by a surfaced hypothesis being confirmed in the lab. The design draws on published patterns: Swanson's literature-based discovery / ABC model of undiscovered public knowledge; the generation–reflection–ranking–evolution tournament of Google DeepMind's [AI co-scientist](../../autonomous-science/systems/co-scientist-google.html) ([Gottweis et al., 2025, arXiv:2502.18864](https://arxiv.org/abs/2502.18864)); provenance-bound literature-grounded generation (HypER, [arXiv:2506.12937](https://arxiv.org/abs/2506.12937)); groundedness/hallucination filtering (TruthHypo/KnowHD, [arXiv:2505.14599](https://arxiv.org/abs/2505.14599)); and novelty-optimized retrieval (SciMON, [arXiv:2305.14259](https://arxiv.org/abs/2305.14259)). Its differentiator is the falsification-first control structure — optimizing precision by aggressive rejection with logged kills — which the evaluation harness in the worked example is built to test.

## Alternatives considered

- **[Co-Scientist](https://arxiv.org/abs/2502.18864) / [Robin](https://www.futurehouse.org/research-announcements/demonstrating-end-to-end-scientific-discovery-with-robin-a-multi-agent-system) / OpenScientist directly.** These are broader end-to-end systems (Co-Scientist ranks proposals; Robin closes a wet-lab loop; OpenScientist runs computational experiments). Reach for them when you want a full discovery loop rather than a high-precision candidate filter, or when you can execute experiments. Crucible is complementary — it can feed candidates into any of them.
- **[Hypothesis Generation skill](../../catalog/tools/hypothesis-generation.html) (K-Dense).** A single skill for structured hypothesis formulation from observations. Lighter (rung 2) and good for ideation, but it has no cross-corpus fragment mining, no Swanson bridge discovery, and no falsification gauntlet — it will not reject aggressively or emit provenance.
- **Plain Claude + literature/database MCPs (rung 3 toolbelt).** Gets you fragments and manual reasoning; use it for a one-off look. You lose the systematic bridge search, the four-gate rejection, and the reproducible run bundle.

## See also

- [Hypothesis Crucible (Claude Plugin)](../../catalog/tools/hypothesis-crucible.html) — the tool this recipe installs.
- [Worked example + evaluation harness](../examples/hypothesis-crucible/) — a captured Alzheimer's run bundle plus the deterministic scorer and gold fixtures.
- [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) — the self-grounding / verification pattern the gauntlet's G2 gate generalizes.
- [Map a disease to its implicated genes and pathways](map-disease-to-genes-and-pathways.html) — a good way to seed the anchor gene space in Stage 0.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the doctrine the run bundle satisfies.

## Sources

- [Gottweis J. et al., "Towards an AI co-scientist," arXiv:2502.18864, 2025](https://arxiv.org/abs/2502.18864) — the tournament/evolution pattern reused in Stage 4.
- [HypER: Literature-grounded Hypothesis Generation and Distillation with Provenance, arXiv:2506.12937, 2025](https://arxiv.org/abs/2506.12937) — provenance-bound generation.
- [Toward Reliable Scientific Hypothesis Generation (TruthHypo / KnowHD), arXiv:2505.14599, 2025](https://arxiv.org/abs/2505.14599) — groundedness filtering that G2 adapts.
- [Wang Q. et al., "SciMON: Scientific Inspiration Machines Optimized for Novelty," arXiv:2305.14259, 2023](https://arxiv.org/abs/2305.14259) — novelty optimization.
- Swanson D.R., "Undiscovered public knowledge," *Library Quarterly* 56(2):103–118, 1986 — the ABC model behind Stage 2.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=generate-cross-corpus-drug-repurposing-hypotheses&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fgenerate-cross-corpus-drug-repurposing-hypotheses.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
