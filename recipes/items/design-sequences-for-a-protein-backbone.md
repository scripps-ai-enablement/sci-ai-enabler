---
title: Design amino-acid sequences for a fixed protein backbone
parent: All recipes
grand_parent: Recipes
nav_order: 9
problem_class: Experimental design
subject_areas: [Integrative Structural and Computational Biology]
evidence_level: Reported
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-07-18
summary: Design sequences for a target backbone with ProteinMPNN, then refold each candidate with ESMFold and keep only those whose self-consistency RMSD recovers the backbone.
---

# Design amino-acid sequences for a fixed protein backbone

Hand Claude a backbone `.pdb`; get back a ranked FASTA of ProteinMPNN-designed sequences that fold to it, each filtered by an ESMFold refolding check (self-consistency RMSD + pLDDT) so you only order sequences the pipeline itself believes recover the target fold.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Integrative Structural and Computational Biology |
| **Evidence level** | Reported |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

You have a backbone but not a sequence. It might be an RFdiffusion-generated de novo scaffold, an existing protein you want to redesign for stability or expression, or a binder backbone whose interface you want to keep while reshaping the core. Rosetta fixed-backbone design is slow and force-field-limited; picking sequences by eye does not scale. ProteinMPNN solves the inverse-folding problem — given coordinates, sample sequences likely to fold to them — but a raw ProteinMPNN sample is only a hypothesis. The field-standard gate before spending DNA-synthesis budget is *self-consistency*: refold each designed sequence with a structure predictor and keep only those whose predicted structure superimposes on the input backbone (low Cα-RMSD) with high confidence (high pLDDT). Solved looks like: point at one backbone file and a few design settings, get a CSV of candidate sequences ranked by ProteinMPNN score *and* refolding self-consistency, with the throwaways already removed.

## Recommended approach

Rung 3 — a small two-model toolbelt: the [ProteinMPNN skill](../../catalog/tools/proteinmpnn.html) to design sequences and the [ESMFold skill](../../catalog/tools/esmfold.html) to refold them for the self-consistency gate. Both are Claude Science research skills that run local inference.

1. **Enable both skills.** In Claude Science, turn on the built-in **ProteinMPNN** and **ESMFold** research skills (install paths on the [ProteinMPNN](../../catalog/tools/proteinmpnn.html) and [ESMFold](../../catalog/tools/esmfold.html) catalog pages — do not run install steps from here). Put your backbone at `backbones/<name>.pdb`.

2. **Design sequences with ProteinMPNN.** Fix any positions that must not change (catalytic residues, an interface you want to preserve), and sample at a temperature that trades diversity against recovery:

   ```
   Use the ProteinMPNN skill on backbones/<name>.pdb.
     - Sample 32 sequences at sampling_temperature 0.1 and
       another 32 at 0.2 (lower T = higher recovery, less
       diversity).
     - Fix these positions (do not redesign): <chain/resid list,
       e.g. A:42,A:98 catalytic; leave blank for full redesign>.
     - Report per-sequence global score and sequence recovery
       vs the native sequence (if the backbone has one).
   Write all designs to designs/<name>_mpnn.fasta with the
   score in each header.
   ```

3. **Refold every design and compute self-consistency.** This is the gate that separates a real design from a plausible-looking string:

   ```
   For each sequence in designs/<name>_mpnn.fasta, use the
   ESMFold skill to predict its structure. Then, for each:
     - Superpose the predicted model onto backbones/<name>.pdb
       and compute Cα-RMSD over aligned residues (scRMSD).
     - Record mean pLDDT of the prediction.
   Write results/<name>_selfconsistency.csv with columns:
     seq_id, mpnn_score, scRMSD_A, mean_plddt, sequence.
   ```

4. **Apply the acceptance filter and rank.** Have Claude keep only designs that clear the standard self-consistency bar and rank the survivors, citing only rows in the CSV:

   ```
   From results/<name>_selfconsistency.csv, keep designs with
   scRMSD < 2.0 A AND mean_plddt > 80 (the common de-novo
   self-consistency cutoffs). Rank survivors by scRMSD ascending,
   breaking ties by mpnn_score. Print the top 10 as a table and
   state how many of the N designs passed. If none pass, say so
   and recommend loosening sampling_temperature or revisiting the
   backbone rather than lowering the cutoffs.
   ```

5. **Capture the pipeline as a versioned command + provenance.** Fold steps 2–4 into a committed `.claude/commands/mpnn-design.md` so the run is repeatable, and write `results/<name>_provenance.json`: ProteinMPNN model/version + sampling settings, ESMFold model/version, the scRMSD/pLDDT cutoffs used, the input backbone sha256, run date, and model/agent identity. See the [reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide.

The durable artifact is the committed `.claude/commands/mpnn-design.md`, the pinned skill environments, `designs/<name>_mpnn.fasta`, `results/<name>_selfconsistency.csv`, and `results/<name>_provenance.json`.

## Why this assembly

Rung 3, and it needs all three moving parts. Rung 1/2 cannot do it: neither plain Claude Code nor a single skill can *design* sequences for a backbone — that is ProteinMPNN's learned inverse-folding model. And a design pipeline that stops at ProteinMPNN alone is incomplete: raw samples include sequences that will not fold, so the ESMFold refolding gate is not optional polish but the step that makes the output orderable. Two models + one filter is the minimum. Rung 4 (an autonomous protein-design system) is overkill for a single backbone; escalate only when you are running an iterative design–predict–select loop over many backbones or optimizing against an experimental readout.

## Availability

Fully open. ProteinMPNN is MIT (Baker Lab); ESMFold code is MIT with model weights under Meta AI terms. Both are Anthropic-hosted Claude Science research skills — no separate accounts or API keys for the hosted path. If you run the upstream models yourself, you need the ProteinMPNN and ESM weights (freely downloadable). No subscription gate.

## Compute requirements

Workstation with GPU. ProteinMPNN sampling is cheap — dozens of sequences for a ~150-residue backbone in seconds to a minute on a single GPU. ESMFold is the heavier step: single-sequence folding of a ~150-residue protein runs in seconds to a couple of minutes on an 8–16 GB GPU; a 64-design batch is a few minutes to ~15 min wall-clock. Long chains (>700 aa) push ESMFold VRAM up — chunk the batch or use the ESM Atlas fold API for one-offs. CPU-only is impractical for the ESMFold step.

## Evidence

`Reported`. The components are validated and the design→refold→filter workflow is standard practice, but the specific Claude-skill assembly is not separately benchmarked.

- **ProteinMPNN** is the field-standard inverse-folding model — higher native sequence recovery than Rosetta with vastly lower compute, and extensively experimentally validated (Dauparas et al., [*Science* 2022](https://doi.org/10.1126/science.add2187)).
- **The refolding self-consistency gate** (design with an inverse-folding model, refold with a structure predictor, keep low-RMSD/high-confidence designs) is the routine in silico filter used across de novo design and redesign campaigns; ESMFold provides fast single-sequence refolding without an MSA (Lin et al., [*Science* 2023](https://doi.org/10.1126/science.ade2574)).
- **Wet-lab confirmation of ProteinMPNN redesign** exists for exactly this use case: a ProteinMPNN reengineering of a flavin-binding fluorescent protein (36–48 of 86 positions changed, 55–66% identity to WT) yielded three designs that all expressed and retained ligand binding, fluorescence, and thermal stability (Nikolaev et al., [*Protein Sci.* 2024](https://pubmed.ncbi.nlm.nih.gov/38501498/)).

Head-to-head studies also map the method's limits: for hard interfaces like TCR–pMHC, ProteinMPNN and ESM-IF fixed-backbone design need careful metric selection and still trail on low-affinity interfaces (Ribeiro-Filho et al., [*PLoS Comput. Biol.* 2024](https://pubmed.ncbi.nlm.nih.gov/39348412/)) — a reason to treat the self-consistency filter as necessary but not sufficient for binder work.

## Alternatives considered

- **Rung 2 — ProteinMPNN alone, no refolding gate.** Faster, but you order sequences the pipeline never checked can fold. Acceptable only when you will experimentally screen many candidates and can absorb the failures.
- **[LigandMPNN](../../catalog/tools/ligandmpnn.html) / [SolubleMPNN](../../catalog/tools/solublempnn.html).** Swap ProteinMPNN for LigandMPNN when the backbone binds a small molecule, metal, or nucleic acid whose context should shape the sequence; use SolubleMPNN when you need surfaces biased toward solubility. Same refolding gate applies.
- **AlphaFold2 instead of ESMFold for the gate.** [AlphaFold2](../../catalog/tools/alphafold2.html) refolding is more accurate but needs an MSA and is far slower; use it as a stricter second gate on the handful of designs that already pass the ESMFold filter, not on the whole batch.
- **Rung 4 — an autonomous design loop.** Warranted only for iterative multi-round campaigns or optimization against an experimental readout, not a single backbone.

## See also

- [ProteinMPNN (Claude Skill)](../../catalog/tools/proteinmpnn.html)
- [ESMFold (Claude Skill)](../../catalog/tools/esmfold.html)
- [LigandMPNN (Claude Skill)](../../catalog/tools/ligandmpnn.html) — ligand/metal/nucleic-acid-aware sequence design.
- [SolubleMPNN (Claude Skill)](../../catalog/tools/solublempnn.html) — solubility-biased sequence design.
- [Score point mutations for functional impact with a protein language model](score-protein-variants-with-esm.html) — pre-screen individual substitutions rather than redesign a whole backbone.
- [Triage an AlphaFold model for structure-based drug design](triage-alphafold-model-for-docking.html) — structure-quality checks for the models you feed in or get out.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md)

## Sources

- [Dauparas J. et al., "Robust deep learning-based protein sequence design using ProteinMPNN," *Science* 2022](https://doi.org/10.1126/science.add2187) — published 2022-09; verified 2026-07-18 (this run).
- [Lin Z. et al., "Evolutionary-scale prediction of atomic-level protein structure with a language model," *Science* 2023](https://doi.org/10.1126/science.ade2574) — published 2023-03.
- [Nikolaev A. et al., "Reengineering of a flavin-binding fluorescent protein using ProteinMPNN," *Protein Sci.* 2024](https://pubmed.ncbi.nlm.nih.gov/38501498/) — published 2024.
- [Ribeiro-Filho H.V. et al., "Exploring the potential of structure-based deep learning approaches for T cell receptor design," *PLoS Comput. Biol.* 2024](https://pubmed.ncbi.nlm.nih.gov/39348412/) — published 2024-09.
- [`dauparas/ProteinMPNN`](https://github.com/dauparas/ProteinMPNN) — verified 2026-07-18 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=design-sequences-for-a-protein-backbone&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdesign-sequences-for-a-protein-backbone.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
