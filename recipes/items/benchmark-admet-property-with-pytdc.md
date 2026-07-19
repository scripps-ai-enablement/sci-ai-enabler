---
title: Benchmark an ADMET property with PyTDC
parent: All recipes
grand_parent: Recipes
nav_order: 2
problem_class: Data analysis
subject_areas: [Drug Repurposing and Discovery, Chemistry]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-19
summary: Drive the PyTDC Claude skill to load a Therapeutics Data Commons ADMET dataset with its leaderboard split, train or score a baseline model, and emit the standard TDC metrics so a new method can be compared head-to-head against the leaderboard.
---

# Benchmark an ADMET property with PyTDC

For a single ADMET endpoint (e.g., Caco-2 permeability, hERG inhibition, CYP3A4 inhibition, AMES mutagenicity, microsomal clearance), load the canonical Therapeutics Data Commons dataset with the leaderboard split, fit a baseline, and emit the official TDC metric — so a new model has a comparable number to report.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Drug Repurposing and Discovery, Chemistry |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

ADMET prediction is the front-line filter for any virtual library — but every paper reports on a different split of a different dataset with a different metric, and head-to-head comparison is impossible without re-running the canonical benchmark. Therapeutics Data Commons (TDC) fixed this with 22 ADMET datasets, frozen scaffold splits, and per-task metric definitions. The hard part is no longer the benchmark — it's the boilerplate: which dataset object, which split mode, which metric, which leaderboard group. A working medicinal chemist or ML researcher should be able to say *"give me the Caco-2 benchmark, scaffold split, with a Morgan-fingerprint + random-forest baseline, report the official metric"* and get a number that's directly comparable to the published leaderboard. Solved looks like: one prompt, one number, in the same row format as the [TDC leaderboard](https://tdcommons.ai/benchmark/admet_group/overview/), in under ten minutes of wall-clock.

## Recommended approach

1. **Install the PyTDC Claude skill** ([catalog page](../../catalog/tools/pytdc.html)).

   ```
   /plugin marketplace add K-Dense-AI/claude-scientific-skills
   /plugin install pytdc@claude-scientific-skills
   pip install pytdc
   ```

   For a fingerprint+RF baseline, also install RDKit and scikit-learn locally (`pip install rdkit scikit-learn`). For a featurizer-rich baseline, add the [molfeat](../../catalog/tools/molfeat.html) or [datamol](../../catalog/tools/datamol.html) skills.

2. **Drive the benchmark with a single prompt.** A minimal version:

   ```
   Using the pytdc skill, run the official TDC ADMET_Group
   benchmark for "caco2_wang":
     1. Load the dataset via `ADMET_Group(path='./tdc_data')`.
     2. Use the official benchmark seeds (1, 2, 3, 4, 5).
     3. For each seed, get train/valid/test via group.get(...).
     4. Featurize SMILES with Morgan ECFP4 (2048 bits, radius 2).
     5. Fit a RandomForestRegressor (n_estimators=500,
        max_features='sqrt') on train.
     6. Predict on test and record MAE (the official metric for
        Caco-2 per the TDC leaderboard).
     7. Report mean +/- std across the 5 seeds in the standard
        leaderboard row format: dataset, metric, mean, std.
   Save the per-seed predictions to results/caco2_wang.csv.
   ```

3. **Sanity-check against the leaderboard.** The expected metric for a Morgan+RF baseline on Caco-2 lives on the [TDC ADMET_Group leaderboard](https://tdcommons.ai/benchmark/admet_group/overview/) — if your number is dramatically better or worse, you're probably using the wrong metric direction (regression vs classification) or the wrong split. The skill's `load_and_split_data.py` reference covers the canonical splits.

4. **Swap in your method.** Once the baseline reproduces a leaderboard-comparable number, replace the fingerprint+RF block with the model you want to benchmark — keep everything else (dataset name, seeds, split, metric) identical. That preserves apples-to-apples comparability with everything else on the leaderboard.

## Why this assembly

Rung 2 of the simplicity ladder. PyTDC itself owns the dataset loaders, splits, and metric definitions — the whole benchmark fits inside one Claude skill. Dropping to rung 1 (Claude Code alone) loses access to TDC's frozen splits, and any "I'll just download the CSV" path lands at a non-comparable result. Escalating to rung 3 (PyTDC + datamol + molfeat) is a fine choice when the question is *"which featurizer gives the best score"* — but for the basic "give me one comparable benchmark number" task, the skill alone is sufficient. Rung 4 (a full autonomous system like Biomni) is overkill for a single benchmark run.

## Availability

Fully open. PyTDC is MIT-licensed; the skill is an MIT-collection community skill; the TDC datasets are CC0 or per-dataset-licensed but free for academic use. Some datasets auto-download on first use (a few GB total across the full suite); ADMET_Group fits in a few hundred MB. No subscription.

## Compute requirements

Laptop. A Morgan+RF baseline on any single ADMET_Group dataset runs in a few minutes on a modern laptop CPU. The full ADMET_Group suite (22 tasks × 5 seeds) runs in a few hours of CPU time. GPU is only needed for neural baselines (graph nets, message-passing models, foundation models like Tx-LLM); for those, an 8–16 GB consumer GPU is typically sufficient for the ADMET datasets, which are small (≤ a few thousand molecules per task).

## Evidence

Reported. The canonical benchmark itself is established in [Huang et al., *NeurIPS Datasets and Benchmarks* 2021 (arXiv:2102.09548)](https://arxiv.org/abs/2102.09548), with the ADMET_Group leaderboard documented at [tdcommons.ai/benchmark/admet_group/overview/](https://tdcommons.ai/benchmark/admet_group/overview/). The framework extension is [Velez-Arce et al., "Signals in the Cells: Multimodal and Contextualized ML Foundations for Therapeutics," NeurIPS 2024 (TDC-2)](https://openreview.net/forum?id=kL8dlYp6IM). Recent LLM-driven ADMET workflows that follow the same benchmark protocol include [Hao et al., "PharmaBench: Enhancing ADMET benchmarks with large language models," *Scientific Data* 11:864 (2024)](https://doi.org/10.1038/s41597-024-03793-0) and [Yuan et al., "Tx-LLM: A Large Language Model for Therapeutics," arXiv:2406.06316 (2024)](https://arxiv.org/abs/2406.06316), both of which report TDC leaderboard numbers as their headline metric. The skill's `SKILL.md` is documentation plus Python recipes — the actual computation is the published TDC code path, so the assembly inherits the benchmark's validation. No published head-to-head benchmark of the *Claude-driven* path against a hand-coded script is known — they call the same `ADMET_Group` API.

## Alternatives considered

- **Hand-coded Python script.** The same `ADMET_Group` API in a notebook works fine for a one-off benchmark. Reach for it when you don't want a chat-driven workflow at all. The skill's value is in (a) Claude knowing the metric direction per dataset without you having to remember and (b) emitting the leaderboard row in the expected format.
- **PyTDC + molfeat + datamol toolbelt.** Add the [molfeat](../../catalog/tools/molfeat.html) skill when you want to sweep featurizers (Mordred descriptors, neural fingerprints, language-model embeddings); add [datamol](../../catalog/tools/datamol.html) when you need preprocessing (standardization, salt stripping). Rung 3 — reach for it when the question is featurizer selection, not benchmark reporting.
- **DeepChem.** A natural ML stack for ADMET prediction; flagged in [`catalog/curator-state.md`](../../catalog/curator-state.html) as the next Chemistry pass. Today there is no Claude-installable DeepChem skill in the catalog, so DeepChem-based ADMET is deferred until that lands.
- **ADMET-AI / AdmetLab 3.0 / Deep-PK.** Published ML predictors that report against TDC. None has a Claude-installable wrapper today — surfaced as a Missing component in `recipes/curator-state.md`. Reach for them via their web servers when you need a ready-made model and don't want to fit your own; reach for the PyTDC recipe when you want a comparable benchmark number for *your* model.

## See also

- [PyTDC (Claude Skill)](../../catalog/tools/pytdc.html)
- [molfeat (Claude Skill)](../../catalog/tools/molfeat.html) — featurizer sweep companion.
- [datamol (Claude Skill)](../../catalog/tools/datamol.html) — preprocessing companion.
- [Estimate pharmacokinetic properties of a small molecule](estimate-pk-properties.html) — sibling recipe that answers *"what's the predicted ADMET profile for this molecule"* rather than *"how does my model score on the benchmark"*.
- [Filter a virtual screening hit list with drug-likeness rules and structural alerts](filter-virtual-screening-hits.html) — downstream use of an ADMET model.

## Sources

- [Therapeutics Data Commons home](https://tdcommons.ai/) — verified 2026-06-21 (this run).
- [TDC ADMET_Group leaderboard](https://tdcommons.ai/benchmark/admet_group/overview/) — verified 2026-06-21 (this run).
- [Huang et al., "Therapeutics Data Commons: Machine Learning Datasets and Tasks for Drug Discovery and Development," *NeurIPS Datasets and Benchmarks* 2021 (arXiv:2102.09548)](https://arxiv.org/abs/2102.09548).
- [Velez-Arce et al., "Signals in the Cells: Multimodal and Contextualized ML Foundations for Therapeutics," NeurIPS 2024 (TDC-2)](https://openreview.net/forum?id=kL8dlYp6IM).
- [Hao et al., "PharmaBench: Enhancing ADMET benchmarks with large language models," *Scientific Data* 11:864 (2024)](https://doi.org/10.1038/s41597-024-03793-0).
- [Yuan et al., "Tx-LLM: A Large Language Model for Therapeutics," arXiv:2406.06316 (2024)](https://arxiv.org/abs/2406.06316).
- [`mims-harvard/TDC`](https://github.com/mims-harvard/TDC) — verified 2026-06-21 (this run).
- [`K-Dense-AI/scientific-agent-skills` (`scientific-skills/pytdc/SKILL.md`)](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/pytdc/SKILL.md) — verified 2026-06-21 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=benchmark-admet-property-with-pytdc&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fbenchmark-admet-property-with-pytdc.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
