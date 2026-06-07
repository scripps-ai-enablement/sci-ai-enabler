---
title: Enumerate analogs around a lead compound for SAR expansion
parent: All recipes
grand_parent: Recipes
nav_order: 10
problem_class: Hypothesis generation
subject_areas: [Chemistry, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
summary: Use the Datamol skill in Claude Code to enumerate standardized, drug-like analogs around a lead SMILES — tautomers, stereoisomers, and fragment-substituted variants — as a ranked SAR-expansion table.
last_verified: 2026-06-07
---

# Enumerate analogs around a lead compound for SAR expansion

Hand Claude Code a lead SMILES; get back a deduplicated, standardized set of close-in analogs — tautomer and stereoisomer variants plus fragment-substituted neighbors — each scored for drug-likeness and similarity to the parent, ready for the medicinal chemist to triage into the next synthesis round.

| | |
|---|---|
| **Problem class** | Hypothesis generation |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Once a project has a confirmed hit or a lead, the recurring question is *what should we make next?* The medicinal chemist wants a structured set of close neighbors — the same scaffold with single-point modifications (a methyl walk, a halogen scan, a bioisosteric ring swap), plus the tautomers and stereoisomers that a single drawn SMILES silently collapses. Doing this by hand is slow and inconsistent: the enumeration order, the standardization rules, and the similarity cut-offs vary run to run, so two chemists expanding the same lead produce different sets. The output also has to be clean — salts stripped, charges neutralized, duplicates removed — before any of it is worth scoring or ordering.

Solved looks like: one lead SMILES in, a deduplicated table of candidate analogs out, each row carrying its Tanimoto similarity to the parent, a QED drug-likeness score, and the transformation that produced it, in a few minutes on a laptop. This is a *hypothesis-generation* step — the table is a menu of testable structures, not a ranked list of predicted winners.

## Recommended approach

1. **Install the [Datamol skill](../../catalog/tools/datamol.html)** — it bundles the standardization, enumeration, and featurization recipes:

   ```
   /plugin marketplace add K-Dense-AI/claude-scientific-skills
   /plugin install datamol@claude-scientific-skills
   ```

   Confirm with `/plugin list`. The [RDKit skill](../../catalog/tools/rdkit-skill.html) is implicitly available (Datamol is RDKit-built); install it explicitly only if you want raw reaction-SMARTS enumeration beyond what Datamol exposes.

2. **Standardize and expand the stereo/tautomer space first.** A minimal prompt:

   ```
   Lead: CC(=O)Oc1ccccc1C(=O)O  (or paste your SMILES)

   Use the Datamol skill:
     1. Standardize the lead (dm.fix_mol, dm.sanitize_mol,
        dm.standardize_smiles); keep the largest fragment and
        neutralize charges. Print the standardized canonical SMILES.
     2. Enumerate tautomers (dm.enumerate_tautomers) and
        stereoisomers (dm.enumerate_stereoisomers), capping at
        32 forms each. Deduplicate by InChIKey.
   Report the parent plus each enumerated form as a table:
   smiles | inchikey | relation (tautomer/stereoisomer) | n_atoms.
   ```

3. **Generate fragment-substituted neighbors.** Add a follow-up that walks single-point modifications around the core:

   ```
   Now generate close analogs of the standardized lead:
     - For each aromatic H position, enumerate substitution with a
       small fragment set: -F, -Cl, -CH3, -OCH3, -CF3, -CN, -OH.
     - Use RDKit reaction SMARTS or dm scaffold tools; standardize
       each product and drop anything that fails to parse.
     - Deduplicate the full set by InChIKey against the parent and
       against each other.
   ```

   Keep the fragment set small and chemically sensible for the chemotype — a kinase hinge-binder warrants a different substituent palette than a GPCR amine. The point is breadth of single-point ideas, not exhaustive combinatorics.

4. **Score and rank the analog set.** Drive Datamol's featurization plus a drug-likeness pass:

   ```
   For every analog (and the parent), compute with the Datamol skill:
     - ECFP4 (Morgan radius 2, 2048-bit) fingerprint
     - Tanimoto similarity to the standardized parent
     - QED drug-likeness score
     - molecular weight, logP, HBD, HBA, rotatable bonds
   Write analogs/<lead>_expansion.csv with columns:
   smiles | inchikey | transformation | tanimoto_to_parent | qed |
   mw | logp | hbd | hba | rotb.
   Sort by tanimoto_to_parent descending, then qed descending.
   Print the top 20 rows and the total count.
   ```

5. **Hand off to filtering and bioactivity.** The enumeration deliberately stops at "plausible neighbors" — it does not judge developability. Pipe `analogs/<lead>_expansion.csv` straight into the [Filter a virtual screening hit list](filter-virtual-screening-hits.html) recipe (Lipinski / Veber / PAINS / BRENK cascade via the MedChem skill) to strip non-drug-like and alert-bearing structures, then look up any analog that already exists in ChEMBL with the [Profile a compound's polypharmacology](profile-compound-polypharmacology.html) recipe before committing synthesis effort.

## Why this assembly

Rung 2 of the simplicity ladder. The whole problem — standardize, enumerate tautomers/stereoisomers, walk single-point substitutions, featurize, and score similarity — is exactly the surface the [Datamol skill](../../catalog/tools/datamol.html) bundles (its catalog page lists "analog generation in lead optimisation" and "similarity searching" as primary use cases, with parallel batch operations on top of RDKit). Plain Claude Code with raw RDKit (rung 1) can do it, but every session re-derives the standardization order and the enumeration caps, and the InChIKey-deduplication step is easy to forget — which is precisely what makes hand-rolled analog sets irreproducible. A multi-tool harness (rung 3) adds nothing here: there is no second data source and no orchestration across heterogeneous APIs, only one cheminformatics library applied in sequence. Generative-model or autonomous-chemist escalation (rung 4) is reserved for de-novo scaffold design and synthesis planning — a different, larger problem than expanding the immediate neighborhood of a known lead.

## Availability

Fully open. The [Datamol](../../catalog/tools/datamol.html) and [RDKit](../../catalog/tools/rdkit-skill.html) skills ship via the `K-Dense-AI/claude-scientific-skills` marketplace under MIT (skills) / Apache-2.0 and BSD-3-Clause (underlying libraries). No subscription, no institutional licence, no account beyond a Claude plan.

## Compute requirements

Laptop. Enumerating tautomers, stereoisomers, and a single-point substitution scan for one lead produces hundreds to low-thousands of analogs and runs in well under a minute on a single CPU core. Fingerprinting and similarity scoring scale linearly; even a 50 000-analog combinatorial expansion fits in <2 GB RAM with Datamol parallelism (`n_jobs=-1`). No GPU.

## Evidence

Proposed. No published benchmark of an LLM-driven Datamol analog-enumeration workflow is known. The closest documented analogue is the K-Dense [lead-optimisation workflow](https://github.com/K-Dense-AI/scientific-agent-skills), which positions Datamol (standardization, enumeration, featurization) immediately upstream of the MedChem filtering step this recipe hands off to — the same rdkit → datamol → medchem ordering. The underlying enumeration and similarity primitives are textbook medicinal cheminformatics: ECFP/Morgan fingerprints and Tanimoto similarity ([Rogers & Hahn, *J. Chem. Inf. Model.* 50:742, 2010](https://doi.org/10.1021/ci100050t)); the QED drug-likeness score ([Bickerton et al., *Nature Chemistry* 4:90, 2012](https://doi.org/10.1038/nchem.1243)); and the matched-molecular-pair concept that motivates single-point SAR expansion ([Griffen et al., *J. Med. Chem.* 54:7739, 2011](https://doi.org/10.1021/jm200452d)). Each component has independent validation; the agent-orchestrated assembly does not. Treat the output as a hypothesis menu to be confirmed by filtering, bioactivity lookup, and ultimately synthesis and assay.

## Alternatives considered

- **Plain Claude Code, no skill (rung 1).** Fine for enumerating a handful of analogs you can eyeball, but Claude re-derives the standardization and enumeration boilerplate each session and the dedup-by-InChIKey step is easy to drop. Reach for it only for one-off, sub-dozen expansions.
- **RDKit skill alone.** The [RDKit skill](../../catalog/tools/rdkit-skill.html) gives reaction-SMARTS enumeration and fingerprints but not Datamol's higher-level standardization and batch helpers. Use it when you need bespoke reaction transforms Datamol does not wrap; otherwise Datamol is the lower-friction rung.
- **A generative chemistry model or autonomous chemist (rung 4).** De-novo generators (and synthesis-planning agents such as [ChemCrow](../../autonomous-science/systems/chemcrow.html)) propose *new* scaffolds and routes rather than close neighbors of a known lead. Reach for them when the project needs scaffold hopping or retrosynthesis, not single-point SAR expansion. They are heavier to set up and harder to audit per structure.

## See also

- [Datamol (Claude Skill)](../../catalog/tools/datamol.html)
- [RDKit Cheminformatics Skill](../../catalog/tools/rdkit-skill.html)
- [Filter a virtual screening hit list with drug-likeness rules and structural alerts](filter-virtual-screening-hits.html) — the downstream developability gate for the enumerated set.
- [Profile a compound's polypharmacology from ChEMBL bioactivity data](profile-compound-polypharmacology.html) — check whether an analog already has measured activity before making it.
- [ChemCrow](../../autonomous-science/systems/chemcrow.html) — the autonomous-system option one rung up, for de-novo design and synthesis planning.

## Sources

- [`K-Dense-AI/scientific-agent-skills` — datamol skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/datamol/SKILL.md) — verified 2026-06-07 (this run).
- [Datamol library — datamol.io](https://datamol.io/) — verified 2026-06-07 (this run).
- [Rogers D., Hahn M. — Extended-Connectivity Fingerprints, *J. Chem. Inf. Model.* 50:742 (2010)](https://doi.org/10.1021/ci100050t) — published 2010-04.
- [Bickerton G.R. et al. — Quantifying the chemical beauty of drugs (QED), *Nature Chemistry* 4:90 (2012)](https://doi.org/10.1038/nchem.1243) — published 2012-01.
- [Griffen E. et al. — Matched Molecular Pairs as a Medicinal Chemistry Tool, *J. Med. Chem.* 54:7739 (2011)](https://doi.org/10.1021/jm200452d) — published 2011-10.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=enumerate-analogs-around-a-lead&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fenumerate-analogs-around-a-lead.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
