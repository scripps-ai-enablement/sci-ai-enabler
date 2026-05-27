---
title: Filter a virtual screening hit list with drug-likeness rules and structural alerts
parent: All recipes
grand_parent: Recipes
nav_order: 3
problem_class: Data analysis
subject_areas: [Chemistry, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-25
summary: Use the MedChem skill in Claude Code to cascade Lipinski / Veber / PAINS / BRENK filters over a SMILES hit list and emit a triaged CSV with per-rule flags and a final keep/drop column.
---

# Filter a virtual screening hit list with drug-likeness rules and structural alerts

Hand Claude Code a CSV of SMILES from a docking run, similarity search, or generative-model output; get back a per-molecule table with drug-likeness rule violations, PAINS / BRENK / NIH structural-alert hits, and a recommended keep/drop column so the medicinal chemist's review queue collapses from thousands to dozens.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A virtual-screening run, a generative-model batch, or a similarity-expanded hit list routinely produces 10³–10⁶ SMILES that nobody can inspect by eye. Most will fail downstream: oral bioavailability falls off the Lipinski / Veber cliff; pan-assay interference compounds (PAINS) produce false positives across every assay platform; BRENK and NIH alerts catch reactive electrophiles, unstable groups, and known toxicophores that any medicinal chemist would reject on sight. The work that has to happen before a chemist looks at the list is mechanical: standardize the structures, compute properties, apply each rule set, record *which* rule each compound failed, and rank what survives.

Solved looks like: one prompt, one CSV in, one CSV out, with the rule cascade and the cut-offs written down so the same triage is reproducible next quarter. Cascading the filters in published order — Lipinski → Veber → PAINS → BRENK — typically retains <1% of an unbiased library, but most of the discarded structures should never have entered the docking pipeline.

## Recommended approach

1. **Install the [MedChem skill](../../catalog/tools/medchem.html)** — it bundles the filter recipes and the configurable cut-offs:

   ```
   /plugin marketplace add K-Dense-AI/claude-scientific-skills
   /plugin install medchem@claude-scientific-skills
   ```

   Confirm with `/plugin list`. Install the sibling [Datamol skill](../../catalog/tools/datamol.html) too — MedChem operates on standardized molecules and Datamol is what produces them. The [RDKit skill](../../catalog/tools/rdkit-skill.html) is implicitly available because both are RDKit-built; install it explicitly only if you also want descriptor work outside the filter cascade.

2. **Pre-standardize the SMILES before filtering.** A minimal prompt:

   ```
   I have hits/screen_2026Q2.csv with columns: id, smiles, dock_score.
   Use the Datamol skill to:
     - load the CSV into a pandas dataframe
     - standardize each SMILES (dm.fix_mol, dm.sanitize_mol,
       dm.standardize_smiles); drop rows that fail to parse
     - keep the largest covalent fragment (dm.keep_largest_fragment)
     - neutralize charges and canonicalize tautomers
   Write the cleaned set to hits/screen_2026Q2_clean.parquet and
   print the row count before and after.
   ```

   Skipping standardization is the most common reason filter results disagree across runs — salt forms and tautomers change descriptor values and alert matches.

3. **Cascade the filters with explicit cut-offs and per-rule columns.** Drive MedChem with a single, explicit prompt:

   ```
   Use the MedChem skill on hits/screen_2026Q2_clean.parquet:
     - Apply rule_of_five (Lipinski) — record pass/fail in col ro5_pass
     - Apply rule_of_veber                — col veber_pass
     - Apply rule_of_egan                 — col egan_pass
     - Run PAINS filter (NIH variant)     — col pains_hits (count)
     - Run BRENK structural alerts        — col brenk_hits  (count)
     - Run NIH undesirable-substructure filter — col nih_hits
     - Compute SAScore                    — col sa_score
     - Compute QED (drug-likeness score)  — col qed

   Add a final "keep" column = (ro5_pass AND veber_pass AND
   pains_hits == 0 AND brenk_hits == 0 AND sa_score <= 6).

   Save to hits/screen_2026Q2_triaged.csv, then print:
     - rows in, rows surviving each step
     - top-25 keep=True rows sorted by dock_score, descending.
   ```

   The cut-offs above are the defaults documented in the MedChem repo; tune them per project (kinase chemotypes routinely fail Lipinski but are still tractable).

4. **Sanity-check the cascade.** Ask Claude to emit a one-page summary plot:

   ```
   Make figures/triage_funnel.png — a horizontal bar chart of rows
   surviving Lipinski, +Veber, +PAINS, +BRENK, +SAScore in order.
   Also write a 3-column markdown table of the top 5 most-common
   alert SMARTS strings hit, with example structures.
   ```

   If >99% of the input is dropped at the PAINS step, the input was already PAINS-heavy and the generative or docking step needs fixing upstream — not the filter.

5. **Hand off the survivors.** The triaged CSV slots into downstream analog enumeration, MD scoring via the [Molecule MCP](../../catalog/tools/molecule-mcp.html), or bioactivity look-up via the [ChEMBL connector](../../catalog/tools/chembl.html). Keep `hits/screen_2026Q2_triaged.csv` under version control — it is the project's audit trail of "what was on the table before we picked".

## Why this assembly

Rung 2 of the simplicity ladder. The filter cascade is mechanical, but the right cut-offs, the right alert catalogues (PAINS-A/B/C, BRENK, NIH, Glaxo), and the standardization-first ordering are easy to get wrong from scratch. The [MedChem skill](../../catalog/tools/medchem.html) bundles all of this with named functions and cut-offs that match the published medicinal-chemistry literature, and Datamol enforces the pre-standardization. Plain Claude Code can drive RDKit and reimplement the rules, but every run reinvents the boilerplate. A multi-tool harness or autonomous system adds nothing — there is no decision-making here, only rule application.

## Availability

Fully open. The [MedChem](../../catalog/tools/medchem.html) and [Datamol](../../catalog/tools/datamol.html) skills ship via the `K-Dense-AI/claude-scientific-skills` marketplace under MIT (skills) / Apache-2.0 (underlying libraries). RDKit is BSD-3-Clause. No subscription or institutional licence required.

## Compute requirements

Laptop. A 10 000-compound triage runs in under a minute on a single CPU core; 1 M compounds take ~20 min if Datamol parallelism is enabled (`n_jobs=-1`). RAM scales linearly with library size — budget 8 GB for libraries up to 5 M SMILES. No GPU needed.

## Evidence

Reported. The K-Dense [lead-optimisation workflow](https://github.com/K-Dense-AI/scientific-agent-skills) documents this exact rdkit → datamol → medchem cascade as the canonical pre-screening step, and the underlying filters all have peer-reviewed quantitative anchors: PAINS by Baell & Holloway ([*J. Med. Chem.* 2010, 53:2719](https://doi.org/10.1021/jm901137j)); BRENK by Brenk et al. ([*ChemMedChem* 2008, 3:435](https://doi.org/10.1002/cmdc.200700139)); Lipinski's Rule of Five ([Lipinski et al., *Adv. Drug Deliv. Rev.* 2001, 46:3](https://doi.org/10.1016/S0169-409X(00)00129-0)); Veber rules ([Veber et al., *J. Med. Chem.* 2002, 45:2615](https://doi.org/10.1021/jm020017n)).

For the size of the funnel, the KNIME comparative analysis ([Lagorce et al., reproduced in the FrogScout tutorial and replicated in 2024 KNIME teaching material](https://pubmed.ncbi.nlm.nih.gov/35775847/)) applied Lipinski + Ghose + Veber + REOS + PAINS + Brenk to BindingDB compounds and reported ~50% surviving Lipinski alone but only ~0.6% surviving all filters combined — the same order of magnitude readers should expect.

No peer-reviewed head-to-head benchmark of "Claude + MedChem skill" against a hand-written RDKit pipeline is known. The agent loop adds reproducibility, not new analytical capability.

## Alternatives considered

- **Plain Claude Code, no skill.** Works for small lists and one-off questions, but Claude has to re-derive the alert catalogues every session and the PAINS / BRENK SMARTS strings are long, easy to typo, and version-dependent. Reach for plain Claude only when filtering ≤100 compounds you can spot-check by eye.
- **RDKit-MCP server alone.** The [RDKit MCP](../../catalog/tools/rdkit-mcp.md) exposes raw RDKit tools but does not bundle the filter catalogues; you would re-implement PAINS / BRENK on top of it. Use it when you need stateless RDKit calls but not the medchem cascade.
- **A chemistry-agent system (ChemCrow).** [ChemCrow](../../autonomous-science/systems/chemcrow.html) is designed for synthesis planning and reaction execution, not hit-list triage. Overkill and out of scope.
- **Wait for ADMET-AI integration.** ML-based ADMET predictors (ADMET-AI 2024; PharmaBench 2024) outperform rule-based filters on aqueous solubility and clearance, but are not yet wrapped as a catalogued component. If solubility is critical, run them downstream of this triage rather than instead of it.

## See also

- [MedChem (Claude Skill)](../../catalog/tools/medchem.html)
- [Datamol (Claude Skill)](../../catalog/tools/datamol.html)
- [RDKit Cheminformatics Skill](../../catalog/tools/rdkit-skill.html)
- [Scan approved drugs for repurposing candidates against a disease](scan-drug-repurposing-candidates.html) — upstream step that produces the candidate list this recipe triages.

## Sources

- [`K-Dense-AI/scientific-agent-skills` — medchem](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/medchem/SKILL.md) — verified 2026-05-25 (this run).
- [MedChem documentation — medchem.datamol.io](https://medchem.datamol.io/) — verified 2026-05-25 (this run).
- [Baell J.B., Holloway G.A. — PAINS, *J. Med. Chem.* 2010](https://doi.org/10.1021/jm901137j) — published 2010-04-08.
- [Brenk R. et al. — BRENK, *ChemMedChem* 2008](https://doi.org/10.1002/cmdc.200700139) — published 2008-03.
- [Lipinski C.A. et al. — Rule of Five, *Adv. Drug Deliv. Rev.* 2001](https://doi.org/10.1016/S0169-409X(00)00129-0) — published 2001-03.
- [Veber D.F. et al. — Veber rules, *J. Med. Chem.* 2002](https://doi.org/10.1021/jm020017n) — published 2002-06.

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=filter-virtual-screening-hits&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ffilter-virtual-screening-hits.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
