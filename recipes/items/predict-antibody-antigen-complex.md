---
title: Predict an antibody–antigen complex to map an epitope
parent: All recipes
grand_parent: Recipes
nav_order: 18
problem_class: Experimental design
subject_areas: [Immunology and Microbiology, Integrative Structural and Computational Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Subscription required
compute_requirements: Laptop
last_verified: 2026-07-25
summary: Use the Boltz plugin to predict an antibody/nanobody–antigen complex and read off a candidate epitope — with explicit handling of the field's low success rate and unreliable confidence ranking.
---

# Predict an antibody–antigen complex to map an epitope

Hand Claude an antibody (or nanobody) sequence plus its antigen, submit a co-folding job through the hosted Boltz API, and get back a ranked set of complex models you can mine for the candidate epitope — with the model's known failure modes surfaced so you treat the answer as a hypothesis, not ground truth.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Immunology and Microbiology, Integrative Structural and Computational Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Subscription required |
| **Compute** | Laptop |

## Problem

You have an antibody or nanobody that binds a target and you want to know *where* — which antigen residues make up the epitope — before committing to crystallography, cryo-EM, HDX-MS, or an escape-mutant screen. A computational epitope hypothesis tells you which surface to mutate for affinity maturation, whether two antibodies compete for the same patch, and where engineered liabilities sit relative to the paratope. The hard part: antibody–antigen interfaces are the *worst* case for current co-folding models. The CDR-H3 loop is hypervariable and poorly templated, nanobody (VHH) complexes are harder still, and — critically — a model's own confidence score does **not** reliably pick the correct pose even when one exists in the ensemble. "Solved" here is honest: a small ranked set of plausible complexes, a residue-level epitope readout for each, an interface-confidence number, and a clear statement that this is a prioritization aid that must be confirmed experimentally.

## Recommended approach

1. **Install the [Boltz plugin](../../catalog/tools/boltz.html)** (official marketplace) and authenticate the CLI:

   ```
   /plugin install boltz@claude-plugins-official
   ```

   Then, in the shell that launches Claude Code, install and log in to the `boltz-api` CLI per the catalog page (`boltz-api auth login --device-code`). Jobs run server-side on Boltz's hosted API — no GPU on your machine — and incur usage cost; the agent shows an estimate before submitting.

2. **Assemble the inputs.** You need the antibody chains (VH + VL, or the single VHH domain for a nanobody) and the antigen sequence as FASTA. If you only have a UniProt accession for the antigen, fetch the canonical sequence first with the [gget skill](../../catalog/tools/gget.html). Decide up front whether you want a full Fab or just the variable domains — trimming to the variable region reduces irrelevant chain mass without losing the paratope.

3. **Submit the complex prediction and sample widely.** Drive the `boltz-structure-and-binding` skill. Because confidence ranking is weak, ask for many samples per target rather than one — the correct pose is far more likely to appear *somewhere* in a large ensemble than to be ranked first:

   ```
   Use the boltz-structure-and-binding skill to predict the complex of
   this antibody with its antigen.

   - Antibody: VH and VL chains below (treat as a paired Fv).
   - Antigen: sequence below.
   - Generate a large sample ensemble (request the maximum samples the
     job allows; we will rank ourselves, not trust a single top pose).
   - Return, for every model: the per-interface confidence (ipTM /
     interface-PAE), the antigen residues within 4.5 Å of any antibody
     CDR atom (the candidate epitope), and which CDR loops contact them.

   Antibody VH: >VH  <paste>
   Antibody VL: >VL  <paste>
   Antigen:     >AG  <paste>
   ```

4. **Capture the run as a durable artifact, not a chat.** Have Claude write a parameterized command file `.claude/commands/predict-epitope.md` (the prompt above, with the sequences as fill-in fields) plus a small `epitope_from_boltz.py` that reads the returned model files, recomputes the 4.5 Å antigen-contact set per model with a pinned `biopython`/`numpy`, and emits `epitope.csv` (`model_id, iptm, interface_pae, antigen_residue, cdr_loop`) and a consensus column (how many of the top-N models share each contact). Pin the environment in `requirements.txt`. Commit the command file, the script, and the env.

5. **Rank by consensus, not by the model's confidence.** The trustworthy signal is *agreement*: antigen residues that recur across the highest-confidence models are your candidate epitope; a single high-confidence pose is not enough. Record provenance to `provenance.json`: Boltz plugin version, `boltz-api` job IDs and submission date, the Boltz model identity returned by the API, library versions, and the antigen accession. These pin the otherwise-unreproducible hosted call.

## Why this assembly

Rung 2. One plugin's skill submits the co-folding job and returns the models; the only local code is a deterministic contact-distance recomputation that belongs in the artifact for auditability. Claude Code alone (rung 1) cannot run a structure-prediction model. A multi-tool harness (rung 3) or an autonomous system (rung 4) is unjustified: this is a single prediction step feeding a manual interpretation, and adding orchestration would not raise the (model-limited) accuracy. The honest constraint is the *model*, not the assembly — so the right move is to stay at rung 2 and spend the saved effort on wide sampling and consensus ranking, which the literature shows is the tractable lever.

## Availability

Subscription required. The Boltz plugin is free and GA in the official marketplace, but it submits jobs to the **hosted Boltz API**, which needs an account and bills usage-based (per-job pricing not published; the agent surfaces an estimate before each submit). gget is free/OSS. No institutional data agreement is needed for public antigen sequences — but do not submit confidential therapeutic sequences to a third-party API without clearing it with your organization.

## Compute requirements

Laptop-sufficient on your side: the heavy computation runs server-side on the Boltz API, so you need only network access and the `boltz-api` CLI. Wall-clock is dominated by queue + server time, not your hardware; a large multi-sample ensemble for one complex is minutes-to-tens-of-minutes of API time and proportional cost. The local contact-recomputation over a handful of model PDBs is instantaneous. Budget API spend, not VRAM.

## Evidence

Reported. Boltz is one of the leading co-folding models and has been independently benchmarked on exactly this problem — antibody/nanobody–antigen complexes — but the *Claude-plugin convenience layer* is not separately benchmarked, so this is `Reported`, not `Validated`, and the realistic accuracy is sobering.

- **Gupta et al. (*Protein Science* 2026), SNAC-DB**, benchmarked seven leading models (including Boltz-2 and Boltz-1x) on post-May-2024 PDB antibody/VHH–antigen complexes: success rates **rarely exceed 25%**, all models "consistently struggle with therapeutically relevant" nanobody VHHs, and confidence-based ranking "fails to identify best predictions even when accurate structures exist in ensembles." Crucially for the recipe's design: generating **1000 samples per target raised oracle success from 11.9% to 50.5%**, while confidence-based ranking stayed nearly flat (10.9–14.9%) — direct support for "sample wide, rank by consensus, distrust the top-1 confidence." ([doi:10.1002/pro.70655](https://doi.org/10.1002/pro.70655))
- **Ünsal et al. (*Briefings in Bioinformatics* 2026)** evaluated nine methods (AF2, Boltz-1/1x/2, Chai-1, Protenix variants, OpenFold3, ESMFold) on 200 curated Ab–Ag complexes, found Boltz variants did *not* benefit from added recycling cycles (unlike AF2/Chai-1/Protenix), and introduced **AntiConf** (combining pDockQ2 + pTM) as a better post-prediction confidence metric than the native scores. ([doi:10.1093/bib/bbag137](https://doi.org/10.1093/bib/bbag137))

No documented attempt of this exact Claude/Boltz-plugin assembly on epitope mapping is known; the evidence above is component-level (the model on the task), and the recipe's sampling-and-consensus strategy is built directly on the SNAC-DB findings.

## Alternatives considered

- **[Triage an AlphaFold model before docking](triage-alphafold-model-for-docking.html) (rung 2).** Reach for that when you have a *single-chain* target and want a monomer structure quality check, not a complex. This recipe is the complex/interface counterpart; the two share the "treat the prediction as a hypothesis, check confidence locally" discipline.
- **Local AlphaFold-Multimer / other co-folders.** AF2-multimer ranked competitively with Boltz in both benchmarks above and Chai-1/Protenix-1 edged ahead in the Ünsal study — but none is catalogued as a Claude-installable component today (a co-folding wrapper is an open [missing-component note](../curator-state.html)). If you already run AF-Multimer on your own GPU, the *interpretation* steps here (wide sampling, consensus epitope, AntiConf-style rescoring) transfer directly.
- **Experimental epitope mapping (HDX-MS, alanine scan, escape mutants).** The ground truth. Given the ≤25% success rate, the computational epitope is a *prioritization* aid that tells you which residues to perturb first — not a replacement. Escalate to the bench as soon as the decision cost exceeds the experiment cost.

## See also

- [Boltz (Claude Code Plugin)](../../catalog/tools/boltz.html)
- [gget (Claude Skill)](../../catalog/tools/gget.html) — fetches the canonical antigen sequence for the input step.
- [Triage an AlphaFold model before docking](triage-alphafold-model-for-docking.html) — single-chain structure-quality counterpart.
- [Scan a therapeutic antibody for glycosylation sites](scan-antibody-glycosylation-sites.html) — sequence-level developability pre-flight on the same antibody.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [Gupta et al., "SNAC-DB: An ML-ready database for antibody and NANOBODY VHH-antigen complexes…" (*Protein Science* 2026)](https://pubmed.ncbi.nlm.nih.gov/42252708/) — Boltz-2/Boltz-1x benchmark, ≤25% success, 1000-sample oracle 50.5%, flat confidence ranking; published 2026; verified 2026-06-27 (this run).
- [Ünsal et al., "Confidence scoring for deep learning-predicted antibody-antigen complexes: AntiConf…" (*Briefings in Bioinformatics* 2026)](https://pubmed.ncbi.nlm.nih.gov/41903187/) — nine-method Ab–Ag benchmark incl. Boltz-1/1x/2, recycling effects, AntiConf metric; published 2026; verified 2026-06-27 (this run).
- [`boltz-bio/boltz-api-skills`](https://github.com/boltz-bio/boltz-api-skills) — `boltz-structure-and-binding` / `boltz-protein-screen` skills; verified 2026-06-27 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=predict-antibody-antigen-complex&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fpredict-antibody-antigen-complex.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
