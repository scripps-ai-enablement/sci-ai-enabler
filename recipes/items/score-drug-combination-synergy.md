---
title: Score a drug-combination screen for synergy
parent: All recipes
grand_parent: Recipes
nav_order: 30
problem_class: Data analysis
subject_areas: [Drug Repurposing and Discovery, Chemistry]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-19
summary: Drive the ToolUniverse Drug Synergy skill to pick the right reference model (Bliss / HSA / Loewe / ZIP / Chou-Talalay) for your combination data and classify a two-drug pairing as synergistic, additive, or antagonistic.
---

# Score a drug-combination screen for synergy

You ran a two-drug combination assay and have effect measurements — now you need a defensible synergy call. Drive the ToolUniverse Drug Synergy skill to select the correct reference model for the data you actually have and return a Bliss/HSA/Loewe/ZIP/CI score with the standard interpretation.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Drug Repurposing and Discovery, Chemistry |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You measured single-drug and combination effects in a cell-viability or inhibition assay — maybe a single dose pair, maybe a full dose × dose matrix — and you need to say whether the combination is synergistic, additive, or antagonistic. The trap is the reference model: Bliss (multiplicative independence), HSA (highest single agent), Loewe (dose additivity), and ZIP each define "expected combined effect" differently, and they can legitimately disagree for the same data. Picking the wrong model for your data shape (e.g., Loewe with only one combo point, or mixing fractional-inhibition and viability-percentage scales) produces a confident but wrong call. "Solved" looks like: the right model chosen for the data you have, the score computed on a consistent scale, and a synergy/additive/antagonism classification you can put in a figure caption — in a few minutes, on a laptop.

## Recommended approach

1. **Install the ToolUniverse MCP server, then the Drug Synergy skill** ([catalog page](../../catalog/tools/tooluniverse-drug-synergy.html)). The skill is a reasoning layer over ToolUniverse tool calls, so the MCP server must be registered first:

   ```
   claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
   npx skills add mims-harvard/ToolUniverse
   ```

   The skill sets `disable-model-invocation: true`, so invoke it explicitly.

2. **Hand the skill your effect data on a single consistent scale.** Use fractional inhibition (0–1) for Bliss/HSA/Loewe/CI, or viability percentages (0–100) for ZIP — never both in one call. A minimal prompt:

   ```
   Use the drug-synergy skill on this combination assay.
   Drug A (erlotinib) single-agent fractional inhibition: 0.30
   Drug B (trametinib) single-agent fractional inhibition: 0.25
   Combination fractional inhibition: 0.72
   I have only this one dose pair.
     1. Tell me which reference model is valid for a single dose
        pair and why the others are not.
     2. Compute the synergy score with that model.
     3. Classify as synergy / additive / antagonism using the
        standard +10 / -10 thresholds, noting the score is on a
        0-100 scale.
   ```

   For a full dose-response matrix, ask for ZIP and request the synergistic *regions*, not a single summary number:

   ```
   Use the drug-synergy skill. I have a 6x6 dose-response matrix
   of viability percentages (attached). Compute the ZIP synergy
   landscape, report the mean ZIP score and flag the dose region
   with the strongest synergy. Warn me about ceiling effects.
   ```

3. **Let the skill pick the model from the data shape.** It maps `DrugSynergy_calculate_bliss` (single dose pair), `_hsa` (multiple dose points), `_loewe` (dose-response curves + combo point), `_zip` (full matrix), and `_calculate_ci` (Chou-Talalay Combination Index). Ask it to state the model's additivity baseline so the call is auditable.

4. **Read the classification with the standard thresholds.** On the 0–100 scale: score > +10 synergy, −10 to +10 additive, < −10 antagonism. For Combination Index the direction inverts: CI < 1 synergy, CI = 1 additive, CI > 1 antagonism. Report a synergistic region for matrix data rather than a single value — synergy is dose-dependent.

## Why this assembly

Rung 2 of the simplicity ladder. The synergy calculators ship as ToolUniverse tools and the skill is the reasoning layer that selects the right one and applies the thresholds — one skill plus its MCP server fully solves the problem. Rung 1 (Claude Code alone) loses the validated calculators and risks an arithmetic baseline the model improvises; the recurring real-world failure here is scale-mixing and model-selection bias, exactly what the skill is built to guard against. Rung 3+ (a toolbelt or an autonomous system) adds nothing for a single combination call. If you need batch analysis across hundreds of combinations with outlier detection and consensus scoring, the SynergyFinder web tool (see Alternatives) is the better fit — but for a defensible call on one combination from your own data, the skill alone is sufficient.

## Availability

Fully open. ToolUniverse is Apache-2.0; the synergy calculators run locally over your own effect data — no combination database is queried, so there is no subscription or data-residency gate. You supply the measurements.

## Compute requirements

Laptop. The reference-model calculations are closed-form arithmetic over a small effect table; runtime is dominated by the skill's reasoning, not computation. No GPU. A single combination or a modest dose × dose matrix returns in seconds of compute.

## Evidence

Proposed. No documented attempt of this specific Claude-driven ToolUniverse Drug Synergy assembly on a real combination screen is known. The grounding is two-layer: (1) the reference models themselves are the field standard — Bliss, HSA, Loewe, and ZIP with the ±10 interpretation thresholds are exactly those implemented and validated in [Ianevski et al., "SynergyFinder 3.0," *Nucleic Acids Research* 50(W1):W739–W743 (2022)](https://doi.org/10.1093/nar/gkac382), the most widely used combination-synergy tool; and (2) the skill's `SKILL.md` documents the same five `DrugSynergy_calculate_*` tool calls, the same scale requirements, and the same thresholds. The assembly inherits the calculators' correctness; what is unbenchmarked is the Claude-driven path versus running SynergyFinder or a hand-coded `synergyfinder` R/Python script directly.

## Alternatives considered

- **SynergyFinder web app / R package.** The canonical tool for combination synergy; reach for it when you have many combinations, need consensus scoring across models, outlier detection, or publication-grade landscape plots across multiple samples. It is not in `catalog/tools/` as a Claude-installable component, so it is an external alternative, not a recipe. Use the skill when you want a quick, conversational, single-combination call inside Claude Code.
- **Hand-coded `synergyfinder`/`synergy` Python.** Same math in a notebook; choose it when you are scripting a batch pipeline. The skill's value is choosing the right model for your data shape and flagging scale-mixing without you having to remember each model's input contract.
- **Quantifying multi-target promiscuity instead of pairwise synergy.** If your question is "what targets does one compound hit" rather than "do two drugs synergize," see the [polypharmacology recipe](profile-compound-polypharmacology.html).

## See also

- [Drug Synergy (ToolUniverse Claude Skill)](../../catalog/tools/tooluniverse-drug-synergy.html)
- [ToolUniverse (MCP server)](../../catalog/tools/tooluniverse.html)
- [Profile a compound's polypharmacology](profile-compound-polypharmacology.html) — single-compound multi-target view.
- [Scan a disease for drug-repurposing candidates](scan-drug-repurposing-candidates.html) — upstream: where a combination hypothesis comes from.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse) — verified 2026-06-21 (this run).
- [`skills/tooluniverse-drug-synergy/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-synergy/SKILL.md) — verified 2026-06-21 (this run).
- [Ianevski et al., "SynergyFinder 3.0: an interactive analysis and consensus interpretation of multi-drug synergies across multiple samples," *Nucleic Acids Research* 50(W1):W739–W743 (2022)](https://doi.org/10.1093/nar/gkac382) — published 2022-05-17.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=score-drug-combination-synergy&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fscore-drug-combination-synergy.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
