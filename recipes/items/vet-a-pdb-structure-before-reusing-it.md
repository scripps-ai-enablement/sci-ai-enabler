---
title: Vet a PDB structure before you build on it
parent: All recipes
grand_parent: Recipes
nav_order: 33
problem_class: Data analysis
subject_areas: [Integrative Structural and Computational Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-01
summary: Judge whether a deposited structure — or one specific loop or side chain in it — is reliable enough to dock against, measure, or build a mechanism on.
---

# Vet a PDB structure before you build on it

Hand Claude Code a PDB entry and the residues you actually care about; get back the global quality metrics, a per-region reliability verdict, and an explicit answer to "can I trust these atoms" — before the measurement goes in a figure.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Integrative Structural and Computational Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A structure is not uniformly good. A 1.8 Å entry can have a disordered surface loop modelled on wishful density; a 3.4 Å entry can have a rock-solid active site. The number in the paper is a global average, and the question you have is local: *is the side chain I am about to measure a distance from actually placed by the data?* Getting this wrong is quiet and expensive — a docking run against a mis-rotamered pocket, a mechanistic claim resting on a hydrogen bond that is a model artifact, a mutagenesis panel designed around a residue that was never resolved.

The checks are standard and published — resolution, the R-free-minus-R-work gap, B-factor distribution, MolProbity clashscore, Ramachandran and rotamer outliers, occupancy and alternate conformations, cryo-EM local versus global resolution — but running them means a Phenix install, a mmCIF header you have to parse, and knowing which of those numbers matters for *your* region. Most people look at the resolution and stop. Solved looks like a committed script that takes a PDB ID plus a residue selection and writes a short verdict file: global metrics, per-residue reliability flags for the selection, and a go / use-with-caveats / don't verdict with the reason attached.

## Recommended approach

Rung 2 — one Claude Skill, [Structure Validation](../../catalog/tools/structure-validation.html), which reads the mmCIF header with Bio.PDB, runs `phenix.molprobity` where available, and separates global model quality from local, per-region reliability.

1. **Install the skill.** Verbatim steps are on the [catalog page](../../catalog/tools/structure-validation.html) (clone `GPTomics/bioSkills`, install the `structural-biology` category or copy the single skill directory). MolProbity-grade geometry needs a local Phenix install — free for academic use under its own licence. Without Phenix the skill falls back to coarse Bio.PDB geometry checks **and says so**; do not let that fallback go unrecorded in your verdict file.

2. **Choose the entry, don't inherit it.** If you have a UniProt accession rather than a specific PDB ID, enumerate the candidates first with the [PDB MCP server](../../catalog/tools/pdb.html) (`search_by_uniprot`) and compare on the axes that matter for reuse — resolution, chain coverage of *your* region, apo versus ligand-bound, deposition year, and whether the construct carries mutations or a fusion tag. The best entry for a docking study is frequently not the highest-resolution one.

3. **Read global quality as a pair, not a single number.** Ask for the header metrics together:

   ```
   Entry: 1ABC (X-ray).

   Using the structure-validation skill, report:
     - experimental method, resolution, R-work, R-free,
       and the R-free minus R-work gap
     - MolProbity clashscore and its percentile, Ramachandran
       favoured / allowed / outlier counts, rotamer outliers,
       cis non-proline peptides
     - whether phenix.molprobity ran or the Bio.PDB fallback
       was used
   Flag the R-free gap explicitly: a gap much larger than
   typical for this resolution is an overfitting signal, and
   R-work alone must not be reported as the quality measure.
   ```

4. **Then ask the local question — this is the step that matters.** Global metrics do not license a specific measurement:

   ```
   Region of interest: chain A residues 145-152 (catalytic loop)
   and the His201 / Asp57 pair.

   For every residue in the selection report:
     - occupancy (flag anything < 1.0 and any altloc)
     - is the side chain modelled at all, or truncated to CB
     - B-factor, plus its z-score against the within-structure
       median/MAD distribution (NOT an absolute cutoff --
       B-factors are only comparable inside one structure)
     - local Ramachandran / rotamer status
     - DSSP secondary structure assignment
   Emit a per-residue table and a one-line verdict per residue:
     reliable | use with caveats | do not build on this.
   ```

   Missing side chains and partial occupancies are the failures most often missed, because nothing in a cartoon render shows them.

5. **Switch the reading for the method.** For a cryo-EM entry, global resolution (FSC 0.143 half-map) and map-model agreement (FSC 0.5) are different numbers and your region's *local* resolution may be far worse than either — ask for both and treat the global figure as an upper bound. For an NMR entry, ask for the per-residue spread across the ensemble; wide spread is a disorder signal, not noise to average away. For a predicted model, this is the wrong recipe — use [Triage an AlphaFold model](triage-alphafold-model-for-docking.html), or have the skill run `phenix.process_predicted_model` to trim low-confidence regions and split PAE domains before anything else touches it.

6. **Commit the artifact.** Version `validate_structure.py` (the selection, the thresholds you applied, the table emission) with `validation_<pdbid>.csv`, a short `verdict.md`, and `provenance.json` recording: the PDB ID **and the mmCIF file sha256**, the PDB release/download date, Phenix and Bio.PDB/DSSP versions, whether the MolProbity path or the fallback ran, and the model id. Entries are re-refined and re-versioned; a verdict without the file hash cannot be reproduced later. See [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html).

## Why this assembly

Rung 2, and no further. The work is running two or three well-defined validators and reading them correctly for one region — the skill's contribution is the *reading*: within-structure B-factor z-scoring rather than an absolute cutoff, the R-free gap rather than R-work, local versus global cryo-EM resolution. Rung 1 can fetch a wwPDB validation report PDF, but that report is global, does not answer the per-residue question, and Claude Code with no skill will happily average B-factors across structures — a category error the skill explicitly avoids. Rung 3 would mean bundling preparation and docking into the same run; those are separate recipes with separate artifacts, and conflating them is how an unvalidated receptor ends up in a screen. Rung 4 is not remotely warranted for a single-entry check.

## Availability

Fully open. The skill is MIT-licensed; Bio.PDB, DSSP and the PDB archive are free. Phenix — which provides the authoritative `phenix.molprobity` and `phenix.process_predicted_model` — is free for academic use under its own licence but requires registration and is **not** freely licensed for commercial use; commercial users either license Phenix or accept the Bio.PDB fallback (and must record that they did). Everything runs locally; no structure leaves your machine.

## Compute requirements

Laptop. Header parsing and Bio.PDB checks on a single entry are seconds. A full `phenix.molprobity` run is typically well under a minute for a normal-sized protein, longer for a large ribosome- or virus-scale assembly. Disk is trivial — an mmCIF is a few megabytes. Batch-validating a few hundred candidate entries is a coffee break on one core, which is what makes step 2 worth doing properly instead of taking the first hit.

## Evidence

`Proposed`. No documented attempt at an agent-driven, region-scoped validation workflow using this skill is known as of 2026-08-01. The underlying criteria are the field's standard and are current:

- **MolProbity is the reference all-atom validator.** Its Ramachandran and rotamer criteria were rebuilt from a million quality-filtered residues, it introduced CaBLAM for backbone assessment in cryo-EM and low-resolution X-ray, and its all-atom clashscore is used in wwPDB deposition — the authors note that deposited structures "have continued to improve greatly" as measured by it ([Williams et al., *Protein Sci.* 2018](https://doi.org/10.1002/pro.3330)). The thresholds in steps 3–4 are these criteria, not house rules.
- **The clashscore responds to real model quality.** Automated QM/MM refinement of 80 Astex Diverse Set protein–ligand structures produced a 4.5-fold improvement in MolProbity clashscore and a 3.5-fold reduction in ligand strain ([Borbulevych et al., *Acta Cryst. D* 2018](https://doi.org/10.1107/S2059798318012913)) — evidence that the metric tracks something fixable rather than being a formality.
- **Validation-before-reuse is the archive's own position, and it is expanding.** The wwPDB continues to formalize per-entry assessment of data quality, local geometry, and model-to-data fit; the 2026 IHMValidation pipeline extends that to integrative/hybrid models with explicit positional-uncertainty estimates, on the stated premise that "rigorous interpretation of a structure model requires assessment of underlying data quality" ([Zalevsky et al., *J. Mol. Biol.* 2026](https://doi.org/10.1016/j.jmb.2025.169598)).

What is missing is a benchmark of agent-produced verdicts against structural biologists' judgements on the same regions. Treat the output as a well-organized pre-flight that surfaces the right numbers, not as a substitute for looking at the density.

## Alternatives considered

**The wwPDB validation report.** Every PDB entry ships one, free, no install. Read it first — it is authoritative and takes thirty seconds. Reach for this recipe when the report's global summary does not answer your local question, when you need the check scripted across many entries, or when you need the verdict in a version-controlled file next to the analysis it justifies.

**Skip validation and prepare the structure directly.** The [Structure Preparation skill](../../catalog/tools/structure-preparation.html) will add hydrogens, assign protonation states and strip additives whether or not the underlying atoms are trustworthy. Preparation on an unvalidated model launders a bad structure into a clean-looking input file, which is the failure this recipe exists to prevent. Validate, then prepare.

**Compare structures instead of validating one.** When two entries disagree about a loop, superposition often settles it faster than metrics — [Superpose two protein structures](superpose-two-protein-structures.html). That is complementary: use this recipe to decide which of the two deserves to be the reference.

## See also

- [Structure Validation (Claude Skill)](../../catalog/tools/structure-validation.html)
- [PDB MCP Server](../../catalog/tools/pdb.html) — enumerate candidate entries for a UniProt accession.
- [Structure Preparation (Claude Skill)](../../catalog/tools/structure-preparation.html) — the next step, once the verdict is favourable.
- [Triage an AlphaFold model for structure-based drug design](triage-alphafold-model-for-docking.html) — the predicted-model counterpart to this recipe.
- [Detect and rank druggable pockets on a protein structure](detect-and-rank-druggable-pockets.html) — downstream; pockets are only as real as the atoms lining them.
- [Superpose two protein structures](superpose-two-protein-structures.html) — when two entries disagree.

## Sources

- [Williams C.J. et al., "MolProbity: More and better reference data for improved all-atom structure validation," *Protein Sci.* 2018](https://doi.org/10.1002/pro.3330) — published 2018; verified 2026-08-01 (this run).
- [Zalevsky A.O. et al., "IHMValidation: Assessment of Integrative Structure Models Deposited to the Protein Data Bank," *J. Mol. Biol.* 2026](https://doi.org/10.1016/j.jmb.2025.169598) — published 2026; verified 2026-08-01 (this run).
- [Borbulevych O. et al., "High-throughput quantum-mechanics/molecular-mechanics (ONIOM) macromolecular crystallographic refinement with PHENIX/DivCon," *Acta Cryst. D* 2018](https://doi.org/10.1107/S2059798318012913) — published 2018.
- [MolProbity / Phenix validation documentation](https://phenix-online.org/documentation/reference/validation_summary.html) — per the catalog page, last verified 2026-08-01.
- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills) — install path per the catalog page, last verified 2026-08-01.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=vet-a-pdb-structure-before-reusing-it&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fvet-a-pdb-structure-before-reusing-it.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
