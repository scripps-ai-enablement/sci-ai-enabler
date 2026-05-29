---
title: Estimate pharmacokinetic properties of a small molecule
parent: All recipes
grand_parent: Recipes
nav_order: 4
problem_class: Knowledge synthesis
subject_areas: [Chemistry, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-27
summary: Combine RDKit physchem descriptors, MedChem rule-based ADMET flags, and measured ChEMBL bioactivity / DMPK endpoints to build a defensible PK estimate for one compound without an ML predictor in the loop.
---

# Estimate pharmacokinetic properties of a small molecule

Hand Claude Code a SMILES; get back the rule-based, descriptor-based, and analog-based pharmacokinetic profile a medicinal chemist or DMPK scientist uses before committing to a chemotype — physicochemical descriptors, drug-likeness verdicts, ADMET-flag hits, and the closest measured ChEMBL endpoints.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

"What does the PK on this compound look like?" is one of the first questions asked after a hit comes off a screen. The honest answer for a single SMILES, with no animal data, sits in three layers:

1. **Physicochemical descriptors** that correlate with absorption and distribution — MW, cLogP, TPSA, HBA/HBD, rotatable bonds, fraction Csp3, aromatic-ring count.
2. **Rule-based ADMET flags** — Lipinski, Veber, Egan, Muegge, plus structural alerts (PAINS, BRENK) and reactive / promiscuity moieties that signal CYP or hERG liabilities.
3. **Measured endpoints on the same scaffold** — ChEMBL exposes assay data for CYP inhibition, hERG, microsomal stability, plasma protein binding, permeability, and aqueous solubility for hundreds of thousands of compounds; the nearest neighbours give the cleanest empirical anchor.

A working scientist doing this by hand opens four tabs (RDKit notebook, a filter library, ChEMBL web UI, and a paper) and ends up with a screenshot. Solved looks like: one prompt in, one structured PK card out, with every claim traceable to the descriptor that produced it, the rule that flagged it, or the ChEMBL document ID behind it.

## Recommended approach

This recipe uses three cataloged Claude Skills / connectors in sequence. Rung 3 of the simplicity ladder — `RDKit + MedChem + ChEMBL`.

1. **Install the skills and connector:**
   - [RDKit Cheminformatics Skill](../../catalog/tools/rdkit-skill.html) — physchem descriptors.
   - [MedChem (Claude Skill)](../../catalog/tools/medchem.html) — drug-likeness rules and ADMET-flag detection.
   - [ChEMBL Connector](../../catalog/tools/chembl.html) — measured bioactivity and DMPK endpoints.

   The two skills install from the K-Dense marketplace; the ChEMBL connector from the Anthropic life-sciences marketplace. Each catalog page owns the verbatim install commands.

2. **Pull the descriptor block.** A minimal prompt:

   ```
   Compound SMILES: <paste>

   Use the RDKit skill to compute and print, in a single markdown table:
     MW, cLogP (Crippen), TPSA, HBA, HBD, rotatable bonds, aromatic rings,
     fraction Csp3, formal charge, num heavy atoms, QED.

   Then briefly comment, descriptor by descriptor, on what each value
   implies for oral absorption and CNS penetration. Do not predict
   numeric clearance / Vd / F — only the qualitative implication.
   ```

   RDKit's Crippen LogP and TPSA are the standard inputs to both the Lipinski / Veber rule sets and to passive-permeability heuristics (TPSA < 90 Å² for oral, < 60 Å² for CNS).

3. **Apply the rule-based ADMET layer.** Next prompt:

   ```
   Using the MedChem skill on the same SMILES:
     1. Run Lipinski, Veber, Egan, and Muegge rule checks. Print
        a pass/fail table.
     2. Apply the PAINS, BRENK, and NIH alert catalogues. For any
        match, print the matched substructure SMARTS and the
        alert's typical implication (e.g., reactive, promiscuous,
        toxicophore).
     3. Compute the synthetic-accessibility score (SAScore) and
        flag if > 6.

   Synthesise: would this molecule clear a standard hit-to-lead
   triage gate? Name the rule(s) it fails, if any.
   ```

4. **Anchor with measured endpoints from ChEMBL.** Final prompt:

   ```
   Using the ChEMBL connector:
     1. compound_search on the SMILES. If an exact match exists,
        record its ChEMBL ID; if not, run a similarity search at
        Tanimoto >= 0.7 and keep the top 10 nearest neighbours.
     2. For each ChEMBL ID, pull bioactivity rows where
        target_pref_name contains any of:
          "Cytochrome P450", "hERG", "Microsomal stability",
          "Plasma protein binding", "Caco-2", "Aqueous solubility".
     3. Group by endpoint type. For each, report median value,
        n compounds, units, and the best (most relevant) assay
        description with its document_chembl_id.

   Emit a PK-anchor table:
     | Endpoint | Median | n | Units | Best ChEMBL doc |
   ```

5. **Assemble the PK card.** Ask Claude Code to merge the three blocks into a single page:

   ```
   Produce one self-contained markdown summary with sections:
     1. Compound — SMILES, canonical SMILES, InChIKey, ChEMBL ID if any.
     2. Physicochemistry — descriptor table + 2-sentence interpretation.
     3. Rule-based ADMET — pass/fail + alerts.
     4. Measured neighbour data — the PK-anchor table.
     5. Overall verdict — one paragraph naming the top three PK risks
        (e.g., "high cLogP suggests metabolic liability; PAINS match
        on the catechol ring; nearest 5 neighbours show CYP3A4 IC50
        < 1 µM") and the next experiment that would resolve each.

   Cite the ChEMBL document_chembl_id for every measured value
   and label everything else as "rule-based" or "descriptor-based".
   ```

   Save to `compounds/<name>_pk_card_<date>.md`.

## Why this assembly

Three components, three independent evidence layers, no overlap. RDKit alone (rung 2) gives descriptors but no rule decisions or empirical anchor — useful for a chemist who already knows the rules by heart, thin for anyone else. MedChem alone gives pass/fail without the underlying numbers a reviewer will ask to see. ChEMBL alone gives measured endpoints but only when the exact compound or a close analog exists in the literature. Stacking the three gets you a card that survives challenge: every number traces to either an RDKit descriptor, a named rule, or a ChEMBL document. The simplicity ladder forbids a rung-4 autonomous-science system here because no documented Biomni / Robin / ChemCrow workflow specifically targets single-compound PK profiling — and adding an unmotivated agent layer hides the provenance the chemist needs.

## Availability

Fully open. All three components are free and require no institutional access. The K-Dense skills are MIT-licensed wrappers around Apache-licensed libraries; the ChEMBL connector is Anthropic-packaged and uses CC-BY-SA-3.0 ChEMBL data. Any current Claude plan supports the marketplace installs.

## Compute requirements

Laptop. The full card for one compound returns in under a minute end-to-end. Descriptor calculation is sub-second; MedChem filter passes are sub-second per compound; the ChEMBL similarity search is the slowest step (~10–20 s for a well-known scaffold with hundreds of neighbours). No GPU, no local datasets to host.

## Evidence

`Proposed`. No documented end-to-end attempt of this exact three-component assembly inside Claude Code is known as of 2026-05-27. The closest analogues are:

- **AgentD** (Journal of Chemical Information and Modeling, 2025) — modular LLM framework that pipes RDKit descriptors and MedChem-style filters into an external Deep-PK predictor; the orchestration pattern is the same as this recipe, the predictor layer is different.
- **ChemCrow** (Bran et al., *Nature Machine Intelligence*, 2024, [doi:10.1038/s42256-024-00832-8](https://doi.org/10.1038/s42256-024-00832-8)) — established the pattern of an LLM calling RDKit and rule-based filters for property estimation; ChemCrow's tool list overlaps three of the four uses in this recipe.
- **PharmaBench** (Niu et al., *Scientific Data*, 2024, [doi:10.1038/s41597-024-03731-0](https://doi.org/10.1038/s41597-024-03731-0)) — multi-agent LLM extracts ADMET endpoints from ChEMBL assay descriptions, the same data layer this recipe leans on for the empirical anchor.

The component-level evidence is solid: the [ChEMBL Connector tutorial](https://claude.com/resources/tutorials/using-the-chembl-connector-in-claude) demonstrates compound resolution and bioactivity pulls; MedChem's rule sets trace to Lipinski 2001, Veber 2002, Baell 2010 (PAINS), and Brenk 2008; RDKit's Crippen LogP and TPSA implementations are the cheminformatics-standard reference. The assembly is rational from those components — but a peer-reviewed benchmark of *this* exact stack against a measured PK dataset has not been published. Treat the card as a hypothesis, not a measurement.

## Alternatives considered

- **Rung 2 — RDKit skill alone.** Adequate when the question is purely "is this molecule drug-like" and the chemist will read the rules themselves. Loses the empirical anchor and the structured ADMET-alert layer.
- **Rung 2 — ChEMBL connector alone.** Adequate when an exact ChEMBL hit exists; degrades fast for novel scaffolds (no neighbours within Tanimoto 0.7 means no anchor, and the card collapses to "no data").
- **Rung 4 — Biomni or a similar autonomous system.** No documented Biomni / Robin workflow exists for single-compound PK profiling; using one would obscure the per-claim provenance a working DMPK scientist needs. Revisit if such a workflow is published.
- **External ML predictor (ADMET-AI, AdmetLab 3.0, Deep-PK).** These would tighten the predictions substantially, particularly for non-Lipinski endpoints like CYP isoform inhibition and hERG IC50. None has a Claude-installable wrapper in [`catalog/tools/`](../../catalog/) today — see the Missing components note below.

## See also

- [RDKit Cheminformatics Skill](../../catalog/tools/rdkit-skill.html)
- [MedChem (Claude Skill)](../../catalog/tools/medchem.html)
- [ChEMBL Connector](../../catalog/tools/chembl.html)
- [Filter a virtual screening hit list with drug-likeness rules and structural alerts](filter-virtual-screening-hits.html) — upstream of this recipe; reach for it on a hit list, reach for this on a single compound earning deeper review.
- [Profile a compound's polypharmacology from ChEMBL bioactivity data](profile-compound-polypharmacology.html) — companion recipe; polypharmacology covers off-target *activity*, this one covers DMPK / safety endpoints.

## Sources

- [Anthropic tutorial — Using the ChEMBL Connector in Claude](https://claude.com/resources/tutorials/using-the-chembl-connector-in-claude) — verified 2026-05-27 (this run).
- [Bran A.M. et al., "Augmenting large language models with chemistry tools," *Nature Machine Intelligence* 2024](https://doi.org/10.1038/s42256-024-00832-8) — published 2024-05.
- [Niu Z. et al., "PharmaBench: Enhancing ADMET benchmarks with large language models," *Scientific Data* 2024](https://doi.org/10.1038/s41597-024-03731-0) — published 2024-08.
- [Baell J.B., Holloway G.A., "New substructure filters for removal of pan assay interference compounds (PAINS)," *J. Med. Chem.* 2010](https://doi.org/10.1021/jm901137j) — published 2010-04.
- [Brenk R. et al., "Lessons learnt from assembling screening libraries for drug discovery for neglected diseases," *ChemMedChem* 2008](https://doi.org/10.1002/cmdc.200700139) — published 2008-01.
- [Lipinski C.A. et al., "Experimental and computational approaches to estimate solubility and permeability in drug discovery and development settings," *Adv. Drug Deliv. Rev.* 2001](https://doi.org/10.1016/s0169-409x(00)00129-0) — published 2001-03.
- [Veber D.F. et al., "Molecular properties that influence the oral bioavailability of drug candidates," *J. Med. Chem.* 2002](https://doi.org/10.1021/jm020017n) — published 2002-06.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=estimate-pk-properties&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Festimate-pk-properties.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
