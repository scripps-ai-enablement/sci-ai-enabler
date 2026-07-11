---
title: Predict a protein–protein complex to map the binding interface
parent: All recipes
grand_parent: Recipes
nav_order: 27
problem_class: Hypothesis generation
subject_areas: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Subscription required
compute_requirements: Laptop
summary: Use the Boltz plugin to co-fold two proteins into a complex and read off the candidate binding interface — sampling widely and ranking by consensus rather than trusting the top-1 confidence.
---

# Predict a protein–protein complex to map the binding interface

Hand Claude two protein sequences you believe interact, submit a co-folding job through the hosted Boltz API, and get back a ranked set of complex models you can mine for the candidate interface — with the field's confidence-ranking caveats surfaced so you treat the answer as a hypothesis, not ground truth.

| | |
|---|---|
| **Problem class** | Hypothesis generation |
| **Subject areas** | Integrative Structural and Computational Biology, Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Subscription required |
| **Compute** | Laptop |

## Problem

You have two proteins you think interact — a kinase and its putative substrate adaptor, a pathogen effector and its host target, two subunits of a complex you pulled down by co-IP — and you want to know *where* they touch before designing an interface mutant, a competing peptide, or a disruption assay. Which residues form the interface tells you which contact to perturb to test the interaction, whether a disease mutation sits at the binding surface, and where to place a crosslinker. The hard part: classical docking needs a good guess at the binding mode and struggles with induced fit, and a co-folding model's own confidence score does **not** reliably rank the correct pose even when one exists in the sampled ensemble. "Solved" here is honest: a small ranked set of plausible complexes, a residue-level interface readout for each, an interface-confidence number, and a clear statement that this is a prioritization aid to confirm experimentally.

## Recommended approach

Rung 2 — one plugin, the [Boltz plugin](../../catalog/tools/boltz.html), whose `boltz-structure-and-binding` skill submits a multi-chain co-folding job to the hosted Boltz API and returns ranked complex models. The only local code is a deterministic interface-contact recomputation that belongs in the durable artifact.

1. **Install the [Boltz plugin](../../catalog/tools/boltz.html)** (official marketplace):

   ```
   /plugin install boltz@claude-plugins-official
   ```

   Then, in the shell that launches Claude Code, install and log in to the `boltz-api` CLI per the [catalog page](../../catalog/tools/boltz.html) (`boltz-api auth login --device-code`). Jobs run server-side — no GPU on your machine — and incur usage cost; the agent shows an estimate before submitting.

2. **Assemble the inputs.** Both partner sequences as FASTA. If you only have UniProt accessions, fetch the canonical sequences first with the [gget skill](../../catalog/tools/gget.html), and confirm residue numbering matches the canonical isoform (position 1 = first residue) so the interface residues you read out map back to your construct. For large multidomain proteins, consider trimming to the domain you expect to mediate binding — irrelevant chain mass dilutes the signal and costs more.

3. **Submit the complex prediction and sample widely.** Because confidence ranking is weak, request many samples rather than one — the correct pose is far likelier to appear *somewhere* in a large ensemble than to be ranked first:

   ```
   Use the boltz-structure-and-binding skill to predict the complex of
   protein A with protein B.

   - Chain A: sequence below.
   - Chain B: sequence below.
   - Generate a large sample ensemble (request the maximum samples the
     job allows; we will rank ourselves, not trust a single top pose).
   - Return, for every model: the interface confidence (ipTM /
     interface-PAE), and the chain-A and chain-B residues within 5 A of
     any atom of the other chain (the candidate interface).

   Chain A: >A  <paste>
   Chain B: >B  <paste>
   ```

4. **Capture the run as a durable artifact, not a chat.** Have Claude write a parameterized command file `.claude/commands/predict-ppi-interface.md` (the prompt above, sequences as fill-in fields) plus a small `interface_from_boltz.py` that reads the returned model files, recomputes the 5 Å inter-chain contact set per model with a pinned `biopython`/`numpy`, and emits `interface.csv` (`model_id, iptm, interface_pae, chain, residue, partner_residue`) and a consensus column (how many of the top-N models share each contact). Pin the environment in `requirements.txt`. Commit the command file, the script, and the env.

5. **Rank by consensus, not by the model's confidence.** The trustworthy signal is *agreement*: interface residues that recur across the highest-confidence models are your candidate binding site; a single high-confidence pose is not enough. Also read the global ipTM as a coarse "is there a real interface at all" gate — very low ipTM across the whole ensemble is a signal the two proteins may not form a stable direct complex under these inputs. Record provenance to `provenance.json`: Boltz plugin version, `boltz-api` job IDs and submission date, the Boltz model identity returned by the API, library versions, and the two input accessions/sha256. These pin the otherwise-unreproducible hosted call. See the [reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) guide for the pattern.

The durable artifact is the committed `.claude/commands/predict-ppi-interface.md`, the `interface_from_boltz.py` script, the pinned `requirements.txt`, and the saved `interface.csv` + `provenance.json` per complex.

## Why this assembly

Rung 2, and it stops here. Predicting a two-chain complex and reading off the interface is a single co-folding-then-interpret step; one plugin skill submits the job and returns the models, and the only local code is a deterministic contact recomputation that belongs in the artifact for auditability. Claude Code alone (rung 1) cannot run a structure-prediction model and will confabulate coordinates. A multi-tool harness (rung 3) or an autonomous system (rung 4) is unjustified: the accuracy ceiling here is the *model*, not the orchestration, so the right move is to stay at rung 2 and spend the saved effort on wide sampling and consensus ranking — the tractable lever the literature identifies.

## Availability

Subscription required. The Boltz plugin is free and GA in the official marketplace, but it submits jobs to the **hosted Boltz API**, which needs an account and bills usage-based (per-job pricing not published; the agent surfaces an estimate before each submit). gget is free/OSS. No institutional data agreement is needed for public sequences — but do not submit confidential or proprietary sequences to a third-party API without clearing it with your organization (a data-residency caveat).

## Compute requirements

Laptop-sufficient on your side: the heavy computation runs server-side on the Boltz API, so you need only network access and the `boltz-api` CLI. Wall-clock is dominated by queue + server time, not your hardware; a large multi-sample ensemble for one complex is minutes-to-tens-of-minutes of API time and proportional cost. The local contact-recomputation over a handful of model files is instantaneous. Budget API spend, not VRAM.

## Evidence

Reported. Boltz is one of the leading open co-folding models and has been benchmarked on exactly this problem — general multi-chain complex structure — but the *Claude-plugin convenience layer* is not separately benchmarked, so this is `Reported`, not `Validated`.

- **Passaro et al., Boltz-2 (2025)** benchmarked complex structure prediction against Boltz-1, Chai-1, Protenix, and AlphaFold3 on PDB complexes deposited in 2024–2025 that were significantly different from training structures, and reported that Boltz-2 matches or moderately improves over Boltz-1 across modalities; all code and weights are MIT-licensed ([bioRxiv 2025.06.14.659707](https://www.biorxiv.org/content/10.1101/2025.06.14.659707v1)).
- **Hou et al. (*Nat. Commun.* 2025)** quantify the strong AlphaFold-Multimer / AlphaFold3 baselines for protein-complex modeling on CASP15 multimer targets (their DeepSCFold improves TM-score by 11.6% over AF-Multimer and 10.3% over AF3), confirming co-folding as the field-standard route to a complex-interface hypothesis ([doi:10.1038/s41467-025-65090-7](https://doi.org/10.1038/s41467-025-65090-7)).

No documented attempt of this exact Claude/Boltz-plugin assembly on general PPI interface mapping is known; the evidence above is component-level (the model on the task). The recipe's sample-wide-and-rank-by-consensus discipline is carried over from the closely related [antibody–antigen complex recipe](predict-antibody-antigen-complex.html), whose benchmarks show confidence-based top-1 ranking is unreliable and wide sampling raises oracle success substantially.

## Alternatives considered

- **[Predict an antibody–antigen complex](predict-antibody-antigen-complex.html) (rung 2).** Reach for that when one partner is an antibody or nanobody — antibody interfaces are the hardest co-folding case (≤25% success in recent benchmarks) and that recipe carries the specific paratope/epitope readout and failure-mode warnings. This recipe is the general non-antibody PPI counterpart; the two share the wide-sampling, consensus-ranking discipline.
- **[Triage an AlphaFold model before docking](triage-alphafold-model-for-docking.html) (rung 2).** Reach for that for a *single-chain* target quality check, not a complex. Use it upstream if you first need to confirm each monomer is well-modelled before co-folding.
- **Local AlphaFold-Multimer / other co-folders.** AF-Multimer and AF3 are competitive baselines (see Evidence), but none is catalogued as a Claude-installable component today (a local co-folding wrapper is an open [missing-component note](../curator-state.html)). If you already run AF-Multimer on your own GPU, the interpretation steps here (wide sampling, consensus interface, ipTM gating) transfer directly.
- **Experimental interface mapping (crosslinking-MS, alanine scan, HDX-MS).** The ground truth. The computational interface is a *prioritization* aid that tells you which residues to perturb first — escalate to the bench as soon as the decision cost exceeds the experiment cost.

## See also

- [Boltz (Claude Code Plugin)](../../catalog/tools/boltz.html)
- [gget (Claude Skill)](../../catalog/tools/gget.html) — fetches the canonical partner sequences for the input step.
- [Predict an antibody–antigen complex to map an epitope](predict-antibody-antigen-complex.html) — antibody-specific sibling with harder-case caveats.
- [Triage an AlphaFold model before docking](triage-alphafold-model-for-docking.html) — single-chain structure-quality counterpart.
- [Superpose two protein structures](superpose-two-protein-structures.html) — compare the predicted complex against a reference.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [Passaro et al., "Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction" (*bioRxiv* 2025)](https://www.biorxiv.org/content/10.1101/2025.06.14.659707v1) — complex-structure benchmark vs AF3/Chai-1/Protenix on PDB 2024–2025; published 2025-06-14; verified 2026-07-11 (this run).
- [Hou et al., "High-accuracy protein complex structure modeling based on sequence-derived structure complementarity" (*Nat. Commun.* 2025)](https://pubmed.ncbi.nlm.nih.gov/41261173/) — AF-Multimer/AF3 multimer baselines on CASP15; published 2025; verified 2026-07-11 (this run).
- [`boltz-bio/boltz-api-skills`](https://github.com/boltz-bio/boltz-api-skills) — `boltz-structure-and-binding` skill for multi-chain co-folding; verified 2026-07-11 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=predict-protein-protein-complex-interface&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fpredict-protein-protein-complex-interface.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
