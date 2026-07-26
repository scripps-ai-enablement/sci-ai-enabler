---
title: Rank a compound library against a target by predicted binding affinity
parent: All recipes
grand_parent: Recipes
nav_order: 20
problem_class: Data analysis
subject_areas: [Drug Repurposing and Discovery, Chemistry, Integrative Structural and Computational Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Subscription required
compute_requirements: Laptop
summary: Use the Boltz plugin's hosted small-molecule screen to rank a SMILES library against a target by predicted binding affinity — no local GPU — and treat the score as a binder/non-binder enrichment filter, not a quantitative ranker.
last_verified: 2026-07-26
---

# Rank a compound library against a target by predicted binding affinity

Hand Claude a target (sequence or PDB) and a CSV of candidate SMILES, submit a structure-and-affinity screen through the hosted Boltz API, and get back a ranked shortlist — with the model's known weakness (good at separating binders from non-binders, weak at quantitatively ordering close analogs) surfaced so you use it as an enrichment filter, not a final ranking.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Drug Repurposing and Discovery, Chemistry, Integrative Structural and Computational Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Subscription required |
| **Compute** | Laptop |

## Problem

You have a target and a few hundred to a few thousand candidate compounds — a repurposing set, a similarity-expanded hit list, a generative-model batch — and you want to know which ones are worth the bench time *before* you commit to docking, MD, or an assay. Classical structure-based screening (Vina, GNINA, Glide) needs a prepared receptor, a defined pocket box, and per-ligand setup; the deep-learning docker [DiffDock](dock-ligand-library-with-diffdock.html) needs a local GPU and produces poses, not an affinity number. Many groups have neither a GPU farm nor a crystal pocket box on hand. What they want is a cheap, no-infrastructure first pass that takes SMILES in and returns an affinity-ranked shortlist out.

"Solved" here is deliberately honest: a ranked table that **enriches** the front of the list for true binders, plus a clear statement that the score is a binder/non-binder classifier — not a tool for finely ordering close analogs — and a durable artifact that records exactly which model version and job IDs produced the ranking.

## Recommended approach

1. **Install the [Boltz plugin](../../catalog/tools/boltz.html)** (official marketplace) and authenticate the CLI:

   ```
   /plugin install boltz@claude-plugins-official
   ```

   Then install and log in to the `boltz-api` CLI per the catalog page (`boltz-api auth login --device-code`). Jobs run server-side on the hosted Boltz API — no GPU on your machine — and bill usage-based; the agent shows a cost estimate before submitting.

2. **Pre-filter and standardize the library first.** Screening compute is wasted on un-drug-like or alerting structures. Run the SMILES through the [virtual-screening hit filter recipe](filter-virtual-screening-hits.html) (Datamol standardize → MedChem Lipinski/Veber/PAINS/BRENK cascade) and carry only the survivors forward. This keeps API spend on compounds worth ranking.

3. **Assemble the target.** You need the target sequence as FASTA (or a PDB/UniProt accession). If you only have an accession, fetch the canonical sequence with the [gget skill](../../catalog/tools/gget.html). Name the binding region if you know it — Boltz can take a pocket constraint, which sharpens enrichment.

4. **Submit the screen.** Drive the `boltz-small-molecule-screen` skill on the filtered library:

   ```
   Use the boltz-small-molecule-screen skill to rank this library
   against the target below.

   - Target: sequence (or PDB ID) below.
   - Library: data/hits_filtered.csv (columns: id, smiles).
   - Return, per compound: predicted binding affinity, the binding
     probability / classifier score, and the structure confidence
     (ipTM / complex confidence) for the predicted pose.
   - Do NOT collapse to a single ranking yet — return all three
     columns so we rank ourselves.

   Target: >TGT  <paste sequence or PDB id>
   ```

5. **Capture the run as a durable artifact, not a chat.** Have Claude write a parameterized command file `.claude/commands/boltz-affinity-screen.md` (the prompt above with fill-in fields) plus a small `rank_screen.py` that reads the returned per-compound results, joins them back to the filtered library, and emits `screen_ranked.csv` (`id, smiles, affinity, binder_prob, confidence, rank`) with a pinned `pandas`. Pin the environment in `requirements.txt`. Commit the command file, the script, and the env.

6. **Rank by classifier score for triage, not by fine affinity differences.** The trustworthy signal is the *binder/non-binder* separation: sort by `binder_prob` (and structure confidence as a tie-break) to pull a top-N shortlist, and treat small affinity gaps between neighbors as noise. Record provenance to `provenance.json`: Boltz plugin version, the Boltz model identity the API returns, `boltz-api` job IDs and submission date, library versions, input SMILES-file sha256, and the target accession. These pin the otherwise-unreproducible hosted call.

7. **Hand off the shortlist.** The top-N survivors are the input to pose-level work — [DiffDock](dock-ligand-library-with-diffdock.html) for poses against a structure, or [GROMACS MM/PBSA](set-up-protein-md-simulation-in-gromacs.html) on the handful you most believe in — and to bioactivity look-up via the [ChEMBL connector](../../catalog/tools/chembl.html).

## Why this assembly

Rung 2. One plugin's skill submits the screen and returns affinity + classifier + confidence; the only local code is a deterministic join-and-sort that belongs in the artifact for auditability. Claude Code alone (rung 1) cannot run a structure-and-affinity model. A multi-tool harness (rung 3) or autonomous system (rung 4) is unjustified for a single ranking pass — the honest constraint is the *model's* quantitative-ranking precision, not the assembly, so the right move is to stay at rung 2, gate on the classifier score, and spend pose-level compute only on the enriched shortlist. The GPU-free hosted path is also what distinguishes this from the [DiffDock recipe](dock-ligand-library-with-diffdock.html), which needs local CUDA.

## Availability

Subscription required. The Boltz plugin is free and GA in the official marketplace, but it submits jobs to the **hosted Boltz API**, which needs an account and bills usage-based (per-job pricing not published; the agent surfaces an estimate before each submit). gget, MedChem, and Datamol are free/OSS. Public target sequences are fine; do not submit confidential targets or proprietary chemistry to a third-party API without clearing it with your organization.

## Compute requirements

Laptop-sufficient on your side: the heavy computation runs server-side on the Boltz API, so you need only network access and the `boltz-api` CLI. Wall-clock is dominated by queue + server time and scales with library size; budget API spend, not VRAM. The local pre-filter (MedChem/Datamol) and the join-and-sort are instantaneous on a single CPU core. A library worth screening should already be filtered to the hundreds–low-thousands; submit in batches and monitor with `boltz-check-status`.

## Evidence

Reported. Boltz-2 — the model behind the hosted screen skill — has been benchmarked on exactly this task, but the *Claude-plugin convenience layer* is not separately benchmarked, and the realistic use is enrichment, not precise ranking.

- **Passaro, Corso, Wohlwend et al. (Boltz-2, bioRxiv 2025-06-14)** report that Boltz-2 is the first AI model to *approach FEP accuracy* on small-molecule binding affinity (avg Pearson **0.62** on the held-out FEP+/OpenFE benchmark, comparable to OpenFE) while being **>1000× faster**; it **outperformed all submitted methods** on the CASP16 affinity challenge (140 protein–ligand pairs) out-of-the-box, and in retrospective hit-discovery screens (MF-PCBA) it **roughly doubled average precision** versus ML and docking baselines — direct support for using it as a screening enrichment filter. ([doi:10.1101/2025.06.14.659707](https://doi.org/10.1101/2025.06.14.659707))
- **Wan, Zhang, Xue & Coveney (UCL, arXiv:2603.05532, 2026-03-02)** independently evaluated Boltz-2 on 16,780 (3CLPro) and 21,702 (TNKS2) compounds against physics-based ESMACS free energies: only weak-to-moderate global correlation (Pearson **0.24** and **0.45**), and **no correlation** within the top-100 high-confidence set. Their conclusion — Boltz-2 "may be effective for classification (identifying binders), but does not provide accurate binding free energies compared to simulation-based approaches" — is exactly why this recipe ranks by the classifier score and treats neighboring affinity gaps as noise.

No documented attempt of this exact Claude/Boltz-plugin assembly on library screening is known; the evidence above is component-level (the model on the task), and the recipe's "gate on classifier score, distrust fine ranking" strategy is built directly on the Wan et al. findings.

## Alternatives considered

- **[Dock a ligand library with DiffDock](dock-ligand-library-with-diffdock.html) (rung 2).** Reach for that when you have (or can get) a local GPU and you need *binding poses* against a structure for visual inspection or MM/PBSA rescoring, not an affinity-ranked shortlist. The two are complementary: this recipe enriches the library cheaply with no GPU; DiffDock then poses the survivors.
- **[Filter a virtual screening hit list](filter-virtual-screening-hits.html) (rung 2).** That is property/alert triage (Lipinski/PAINS/BRENK), not target-aware affinity. It is the *upstream* step here, not a substitute — run it first to cut API spend.
- **Classical docking (Vina / GNINA / Glide).** Decades of validation and a binding-affinity score out of the box, but needs a prepared receptor and pocket box, and is per-ligand fiddly. The right escalation when you have a crystal pocket and want physics-grounded scoring; this recipe's edge is zero local infrastructure.
- **Physics-based FEP / ESMACS.** The accuracy ceiling for ranking close analogs, and the only reliable way to order neighbors that Boltz cannot separate — but orders of magnitude more compute and setup. Reserve it for the handful of compounds the cheap screen enriched, where quantitative ranking actually drives the decision.

## See also

- [Boltz (Claude Code Plugin)](../../catalog/tools/boltz.html)
- [gget (Claude Skill)](../../catalog/tools/gget.html) — fetches the canonical target sequence for the input step.
- [Filter a virtual screening hit list with drug-likeness rules and structural alerts](filter-virtual-screening-hits.html) — the upstream pre-filter that cuts API spend.
- [Dock a ligand library into a target structure with DiffDock](dock-ligand-library-with-diffdock.html) — GPU pose-level counterpart for the enriched shortlist.
- [Predict an antibody–antigen complex to map an epitope](predict-antibody-antigen-complex.html) — the macromolecular-complex Boltz recipe.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [Passaro, Corso, Wohlwend et al., "Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction" (bioRxiv 2025)](https://www.biorxiv.org/content/10.1101/2025.06.14.659707v1) — FEP+ Pearson 0.62, CASP16 win, MF-PCBA average-precision doubling; published 2025-06-14; verified 2026-06-28 (this run).
- [Wan, Zhang, Xue & Coveney, "On the Reliability of AI Methods in Drug Discovery: Evaluation of Boltz-2…" (arXiv:2603.05532)](https://arxiv.org/abs/2603.05532) — independent eval: weak global correlation, no top-100 correlation, classifier-not-ranker conclusion; published 2026-03-02; verified 2026-06-28 (this run).
- [`boltz-bio/boltz-api-skills`](https://github.com/boltz-bio/boltz-api-skills) — `boltz-small-molecule-screen` skill; verified 2026-06-28 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=rank-compound-library-by-predicted-affinity&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Frank-compound-library-by-predicted-affinity.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
