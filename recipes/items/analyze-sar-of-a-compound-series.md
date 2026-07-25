---
title: Analyze the SAR of a measured compound series
parent: All recipes
grand_parent: Recipes
nav_order: 1
problem_class: Data analysis
subject_areas: [Chemistry, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-19
summary: Drive the SAR Analysis skill over a CSV of assayed analogs to decompose the common scaffold, tabulate R-group vs potency, and surface activity cliffs for the next lead-optimization round.
---

# Analyze the SAR of a measured compound series

You have a table of analogs with measured potencies. Drive the [SAR Analysis skill](../../catalog/tools/sar-analysis.html) to find the shared scaffold, decompose each molecule into core + R-groups, map substituent to activity, and flag the activity cliffs that should steer the next synthesis round.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A medicinal-chemistry project accumulates a series of close analogs with measured IC50 / Ki / EC50 values, and the recurring question is *which structural change moved potency, and in which direction?* Answering it by eye across dozens of SMILES is slow and inconsistent: the shared scaffold has to be identified, each molecule split into a common core plus its variable substituents, the substituents lined up at matching R-positions, and the potency deltas read off — the same maximum-common-substructure and R-group-decomposition logic every time. The high-value output is the **activity cliff**: a pair of near-identical structures with a large potency gap, which pinpoints the substituent position worth exploiting. Solved looks like: a CSV of analogs in, a scaffold + R-group-vs-activity table out, activity cliffs flagged, in a few minutes on a laptop — reproducibly, so two chemists analyzing the same series get the same decomposition.

This is the retrospective, *analyze-what-you-measured* counterpart to the forward [enumerate-analogs](enumerate-analogs-around-a-lead.html) recipe, which proposes new structures to make.

## Recommended approach

1. **Install the [SAR Analysis skill](../../catalog/tools/sar-analysis.html)** (SciAgent-Skills; runs its Python locally via RDKit). Clone the collection and load it as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   /plugin install sciagent-skills
   ```

   It declares its own dependencies (RDKit, pandas) in `SKILL.md`; install them when prompted, and pin them (`rdkit`, `pandas`) in a `requirements.txt` you commit.

2. **Prepare an input CSV** with one row per compound — a `smiles` column, a compound `id`, and a numeric activity column (IC50/Ki in nM, or pIC50). Standardize the structures first if they came from mixed sources (the [datamol skill](../../catalog/tools/datamol.html) strips salts and neutralizes charges); a clean, deduplicated table makes the scaffold detection robust.

3. **Have the assistant author a versioned analysis script**, not an interactive chat. A prompt that lands a durable artifact:

   ```
   Use the sar-analysis skill on series.csv (columns: id, smiles, ic50_nM).
   Write the analysis to a committed script sar_analysis.py that:
     1. Converts ic50_nM to pIC50 for the activity scale.
     2. Finds the maximum common substructure (rdFMCS, threshold 0.8)
        and reports the shared scaffold as SMARTS.
     3. Runs R-group decomposition against that core; emits a table of
        core + R1/R2/... substituents per compound.
     4. Joins substituents to pIC50 and, for each R-position, tabulates
        substituent -> mean pIC50 so the SAR trend at each position is
        explicit.
     5. Flags activity cliffs: pairs differing at a single R-position
        with |delta pIC50| >= 1.0 (>=10x potency change).
   Save sar_table.csv, activity_cliffs.csv, and the skill's HTML report
   to results/. Do not summarize beyond what those files contain.
   ```

4. **Run the script and read the outputs.** `sar_table.csv` is the core-plus-R-group decomposition; `activity_cliffs.csv` is the shortlist of single-change pairs with large potency swings — those are the transformations to prioritize or avoid next. The HTML report gives aligned 2D structures with the activity heatmap for a figure. Any written SAR narrative must cite only rows in those tables.

5. **Record provenance.** Emit a `provenance.json` capturing the RDKit and pandas versions, the SAR-skill commit, the MCS threshold and cliff cutoff you used, the input CSV's sha256, the run date, and the model id — so the decomposition can be re-run and audited. Commit `sar_analysis.py`, `requirements.txt`, `results/`, and `provenance.json`. See the [reproducibility guide](../../guide/advanced/reproducibility.md) for the artifact pattern.

## Why this assembly

Rung 2 of the simplicity ladder. The whole task — MCS detection, R-group decomposition, activity alignment, cliff flagging — is exactly what the one SAR Analysis skill wraps over RDKit, so a single skill solves it. Rung 1 (Claude Code alone) loses RDKit's validated `rdFMCS`/`rdRGroupDecomposition` and risks a scaffold the model eyeballs incorrectly, which corrupts every downstream R-group column. Rung 3+ (adding a QSAR model or an autonomous system) answers a different question — *predict* the potency of an unmade analog — and is overkill for reading the SAR of a series you already measured. Start here; escalate only when you want quantitative prediction of new compounds.

## Availability

Fully open. The SAR Analysis skill ships in the CC-BY-4.0 SciAgent-Skills collection and runs entirely locally over RDKit and pandas — your structures and assay data never leave the machine, so there is no subscription or data-residency gate. Any current Claude plan suffices.

## Compute requirements

Laptop. MCS and R-group decomposition over a series of tens to a few hundred analogs is CPU-only and completes in seconds to a minute; runtime is dominated by the skill's reasoning, not the RDKit calls. No GPU. Very large series (thousands of compounds) with an expensive MCS threshold can take longer — subset to one chemotype at a time if so.

## Evidence

Reported. No published paper documents this exact Claude + SAR-Analysis-skill assembly, but its two layers are both grounded. (1) The underlying methods are field-standard for lead optimization: R-group decomposition and matched-pair-style single-substituent comparison are the canonical way to read SAR and detect activity cliffs, established across the medicinal-chemistry literature and reaffirmed in current work — context-based matched-pair analysis of a ChEMBL CYP1A2 set to guide lead optimization ([Raut & Dixit, *RSC Med. Chem.* 2025](https://pubmed.ncbi.nlm.nih.gov/40438290/)), matched-pair/matched-series bioactivity models reaching R² ≈ 0.83 for potency change ([Ding et al., *Curr. Med. Chem.* 2020](https://pubmed.ncbi.nlm.nih.gov/32338210/)), and the "retro-optimization" matched-pair-network framing of optimization logic ([Kombo & LaMarche, *J. Med. Chem.* 2025](https://pubmed.ncbi.nlm.nih.gov/40418162/)). (2) The skill is part of the SciAgent-Skills collection evaluated on BixBench, and it calls RDKit's validated `rdFMCS`/`rdRGroupDecomposition` — so the assembly inherits those routines' correctness. What is not separately benchmarked is the Claude-driven path versus a hand-coded RDKit script; they call the same functions.

## Alternatives considered

- **Hand-coded RDKit script.** The same `rdFMCS` + `rdRGroupDecomposition` in a notebook works for a one-off. Reach for it when you are scripting a batch pipeline across many series. The skill's value is doing the decomposition, alignment, and cliff-flagging conversationally and emitting the aligned-structure HTML report without boilerplate.
- **Enumerate new analogs instead of analyzing measured ones.** If the question is *what should we make next* rather than *what did our measurements tell us*, use the [enumerate-analogs](enumerate-analogs-around-a-lead.html) recipe (forward, hypothesis-generation) — these are siblings.
- **Property-focused medicinal-chemistry filtering.** To flag structural-alert / drug-likeness liabilities across the series rather than potency SAR, the [medchem](../../catalog/tools/medchem.html) skill and the [filter-virtual-screening-hits](filter-virtual-screening-hits.html) recipe are the better fit.
- **True matched-molecular-pair transformation networks with search-time rules.** The skill does single-position R-group comparison, not a full MMP transformation database (e.g., `mmpdb`). For systematic transformation-rule mining across a large corpus, a dedicated MMP tool is the right escalation — none is catalogued as a Claude-installable component today.

## See also

- [SAR Analysis (Claude Skill)](../../catalog/tools/sar-analysis.html)
- [datamol (Claude Skill)](../../catalog/tools/datamol.html) — standardize the input series first.
- [medchem (Claude Skill)](../../catalog/tools/medchem.html) — structural-alert / drug-likeness companion.
- [Enumerate analogs around a lead compound for SAR expansion](enumerate-analogs-around-a-lead.html) — forward sibling: propose new analogs to make.
- [Train a QSAR model from your own assay data and predict untested compounds](train-qsar-model-from-assay-data.html) — predictive sibling: score the next batch once you understand the series.
- [Filter a virtual screening hit list with drug-likeness rules and structural alerts](filter-virtual-screening-hits.html)

## Sources

- [SAR Analysis catalog page (this repo)](../../catalog/tools/sar-analysis.html) — `last_verified` 2026-06-11.
- [`skills/structural-biology-drug-discovery/sar-analysis/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/sar-analysis/SKILL.md) — verified 2026-07-19 (this run).
- [Raut & Dixit, "A context-based matched molecular pair analysis identifies structural transformations that reduce CYP1A2 inhibition," *RSC Med. Chem.* (2025)](https://pubmed.ncbi.nlm.nih.gov/40438290/) — published 2025.
- [Ding et al., "Bioactivity Prediction Based on Matched Molecular Pair and Matched Molecular Series Methods," *Curr. Med. Chem.* (2020)](https://pubmed.ncbi.nlm.nih.gov/32338210/) — published 2020.
- [Kombo & LaMarche, "The Logic of Chemical Optimization," *J. Med. Chem.* (2025)](https://pubmed.ncbi.nlm.nih.gov/40418162/) — published 2025.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=analyze-sar-of-a-compound-series&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fanalyze-sar-of-a-compound-series.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
