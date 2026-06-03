---
title: Dock a ligand library into a target structure with DiffDock
parent: All recipes
grand_parent: Recipes
nav_order: 8
problem_class: Data analysis
subject_areas: [Integrative Structural and Computational Biology, Drug Repurposing and Discovery, Chemistry]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-06-03
summary: Drive DiffDock from Claude Code to generate per-ligand binding poses against a PDB or AlphaFold target, filter by confidence, and emit a ranked pose set ready for MM/PBSA rescoring or visualization.
---

# Dock a ligand library into a target structure with DiffDock

Hand Claude Code a target structure (PDB ID or local PDB file) and a CSV of ligand SMILES; get back per-ligand DiffDock poses with confidence scores, a confidence-filtered shortlist, and SDF / PDB exports ready for downstream rescoring or visualization.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Integrative Structural and Computational Biology, Drug Repurposing and Discovery, Chemistry |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

A computational chemist with a triaged target — either a crystal structure or an AlphaFold model that passed pocket-pLDDT triage — needs to dock dozens to thousands of candidate ligands without specifying a binding box or running a per-ligand Vina configuration. Classical docking (Vina, GNINA, Glide) requires a pocket box and rigid-receptor geometry; for AlphaFold models or large allosteric targets that is a real headache. DiffDock is a diffusion model that predicts binding poses directly from PDB + SMILES, no box required, and ranks each pose by a confidence model that correlates with pose validity. The work that still has to happen — staging the protein, batching SMILES, running diffusion sampling, applying a confidence cutoff, sanity-checking with PoseBusters-style geometry checks, exporting SDF/PDB for the next step — is mechanical and easy to get wrong by hand.

Solved looks like: one prompt referencing a target and a SMILES file; one ranked poses directory out with a confidence-filtered shortlist, a top-K SDF per ligand, and a markdown card stating which ligands cleared the confidence > 0 bar.

## Recommended approach

Rung 2 of the simplicity ladder — one Claude skill, the [DiffDock skill](../../catalog/tools/diffdock.html), wraps the GitHub `gcorso/DiffDock` model and ships the batch CSV templates, the confidence-aware analysis script, and pose-export helpers. The skill does not ship the model weights; the catalog page documents the conda environment install.

1. **Install the skill and the DiffDock environment.** Verbatim commands are on the [catalog page](../../catalog/tools/diffdock.html); the short version is `/plugin marketplace add K-Dense-AI/claude-scientific-skills` then `/plugin install diffdock@claude-scientific-skills`, plus a separate `git clone https://github.com/gcorso/DiffDock` and `conda env create --file environment.yml`. The skill's `setup_check.py` verifies PyTorch + CUDA, PyTorch Geometric, RDKit, and ESM before any run.

2. **Stage the target.** If using a triaged AlphaFold model from the [AlphaFold triage recipe](triage-alphafold-model-for-docking.html), point at the local `.pdb` file the triage step exported; otherwise pull a PDB:

   ```
   Target: PDB 7L11 (or local file structures/P38398_alphafold.pdb).

   Using the diffdock skill:
     1. Confirm the target file exists. If it is an AlphaFold
        model, restate the pocket-pLDDT verdict from the triage
        card and refuse to proceed if the verdict was "not
        docking-ready".
     2. Strip waters, ions, and non-cofactor ligands from a
        copy of the file. Keep a backup of the original.
   ```

3. **Prepare the ligand batch CSV.** The skill's `prepare_batch_csv.py` builds the DiffDock-expected `complex_name, protein_path, ligand_description` schema from a SMILES table:

   ```
   Ligand input: data/hits.csv (columns: id, smiles).
   Protein: structures/target_clean.pdb.

   Run prepare_batch_csv.py to emit data/diffdock_batch.csv
   with one row per ligand. Reject any SMILES that RDKit
   cannot sanitize and write the failures to data/rejects.csv.
   ```

4. **Run diffusion sampling.** Default DiffDock samples 10–40 poses per ligand; 20 is a reasonable starting point for screening, 40 for lead optimization:

   ```
   Run DiffDock inference on data/diffdock_batch.csv:
     samples_per_complex = 20
     batch_size = 10        (lower if VRAM constrained)
     inference_steps = 20
     output_dir = results/diffdock_run_<date>/

   Stream the per-complex confidence scores to a CSV
   results/diffdock_run_<date>/confidences.csv with columns
   ligand_id, pose_rank, confidence.
   ```

5. **Filter by confidence and inspect.** Apply the rule-of-thumb cutoff from the upstream `confidence_and_limitations.md`:

   ```
   Using analyze_results.py on results/diffdock_run_<date>/:
     - Keep poses with confidence > 0 as "trustworthy".
     - Flag poses with confidence between -1.5 and 0 as
       "inspect visually before use".
     - Drop poses with confidence < -1.5.
     - For each ligand, emit the top-3 trustworthy poses as
       a numbered SDF in results/.../top_poses/<ligand_id>/.

   Print a summary table: ligand_id, n_trustworthy, best_conf,
   pocket_overlap (fraction of pose atoms within 5 Å of the
   pocket residue centroid — pocket residues from the triage
   card, or supplied separately).
   ```

6. **Hand off downstream.** Confidence-filtered SDFs are the input to:

   - [MedChem](../../catalog/tools/medchem.html) — drug-likeness / PAINS / BRENK rescue cascade across the ligand list before any further compute (see the [virtual-screening hit filter recipe](filter-virtual-screening-hits.html)).
   - [DeepChem](../../catalog/tools/deepchem.html) — neural-network rescoring of the top-K poses if a binding-affinity proxy is needed.
   - [molecular-dynamics](../../catalog/tools/molecular-dynamics.html) / [molecule-mcp](../../catalog/tools/molecule-mcp.html) — short MM/PBSA or full MD relaxation to upgrade pose quality and produce an affinity estimate (see the [GROMACS MD setup recipe](set-up-protein-md-simulation-in-gromacs.html)).
   - PyMOL / ChimeraX via `molecule-mcp` — visual inspection of the top trustworthy pose per ligand.

7. **Persist the run card.** Ask Claude Code to write `results/diffdock_run_<date>/RUN.md` capturing the target identifier, the ligand-count in / kept / rejected, the confidence-filtering rule, the wall-clock per ligand, and links to the downstream rescore steps that ran.

## Why this assembly

Rung 2 of the simplicity ladder. The [DiffDock skill](../../catalog/tools/diffdock.html) is exactly one skill, and it bundles the batch CSV preparation, the confidence-aware result analyzer, and the pose export — the three steps that would otherwise be hand-written glue around a GitHub repo. Rung 1 (plain Claude Code calling DiffDock via raw Python) is possible but throws away the skill's hard-won understanding of which DiffDock command-line flags actually matter and where the confidence-thresholding conventions come from. Rung 3 (chaining MedChem + DeepChem + MD rescoring) is the right next step after the docking run, but each tool stands alone — wrapping them into one harness now is premature optimization for a workflow that is iterative by nature.

## Availability

Fully open. The DiffDock skill is MIT-licensed; the underlying [`gcorso/DiffDock`](https://github.com/gcorso/DiffDock) model and weights are MIT. No subscription, no auth, no quota. The model is shipped on Hugging Face and pinned by the upstream conda environment.

## Compute requirements

Workstation with GPU. DiffDock diffusion sampling is GPU-bound; on a single RTX 4090 / A100, a 20-sample-per-complex run averages around 30–60 s per ligand depending on protein size and inference steps. A 1000-ligand screen at 20 samples/complex therefore runs in roughly 8–17 hours on a single GPU; batch_size > 10 is feasible on 24 GB+ VRAM. CPU-only inference is supported but ~10–20× slower and not recommended past dozens of ligands. The skill's `setup_check.py` checks CUDA visibility before any run.

## Evidence

`Proposed`. No documented end-to-end LLM-orchestrated DiffDock virtual-screen workflow is known as of 2026-06-03. The component pieces are independently well-validated:

- **DiffDock itself** — published at [ICLR 2023 (Corso et al., arXiv:2210.01776)](https://arxiv.org/abs/2210.01776); DiffDock-L follow-up at [ICLR 2024](https://arxiv.org/abs/2402.18396) achieves 38% → 80% RMSD < 2 Å success when filtering to the top one-third by confidence on PDBBind. DiffDock-L produced ≥1 physically valid pose for 95.53% of active compounds on DUDE-Z.
- **PoseBusters benchmarking** — [Buttenschoen, Morris & Deane, *Chem. Sci.* 15:3130–3139 (2024), DOI:10.1039/D3SC04185A](https://doi.org/10.1039/D3SC04185A) — established that DiffDock produces the most physically valid poses among deep-learning dockers but underperforms classical methods on out-of-distribution targets; gating by DiffDock confidence is what closes the gap.
- **DiffDock on AlphaFold models** — the AF2-target performance is materially worse than on crystallographic targets ([Scardino et al. and follow-ups, ~21% RMSD < 2 Å vs ~10% for other deep learners on AF2 targets, pocket-RMSD-sensitive](https://doi.org/10.1021/acs.jcim.3c00601)); this recipe addresses that risk by chaining onto the upstream AlphaFold triage and refusing to proceed when the pocket-pLDDT verdict is poor.
- **LLM-orchestrated docking frameworks more broadly** — [AgentD (arXiv:2507.02925, 2025)](https://arxiv.org/abs/2507.02925) and [MADD (Solovev et al., EMNLP Findings 2025)](https://aclanthology.org/2025.findings-emnlp/) demonstrate that LLM agents can coordinate docking + property-prediction stacks end-to-end, but neither documents DiffDock specifically as the docking backbone.

A peer-reviewed benchmark of "Claude + DiffDock skill" against a hand-built notebook is the missing link; the component-level evidence behind every claim — the confidence-filtering rule of thumb, the AlphaFold caveat, the conda environment — is well-established.

## Alternatives considered

- **Classical docking (AutoDock Vina / GNINA / Glide).** Faster per ligand, decades of validation, and a binding-affinity score out of the box. The right escalation when the target has a well-defined pocket box and a crystal structure; DiffDock's advantage is the no-box, geometry-driven setup that fits AlphaFold models and allosteric or cryptic sites.
- **Rung 3 with MM/PBSA rescoring inline.** Worth it only when the trustworthy-pose count is small (≤ 50 ligands) and binding-affinity ranking matters for the decision. For first-pass library triage, confidence-filtered DiffDock + drug-likeness filter is the cheap path.
- **Rung 4 autonomous-science systems.** [Biomni](../../autonomous-science/systems/biomni.html) and [ChemCrow](../../autonomous-science/systems/chemcrow.html) cover broader drug-discovery workflows but neither documents DiffDock as the primary docker; an autonomous system here over-constrains a workflow the chemist usually wants to iterate on.
- **Co-folding (AlphaFold-Multimer, Boltz-2, RoseTTAFold All-Atom).** Better than docking when the ligand is large enough that induced fit matters. Not yet wrapped as a Claude-installable component — see Missing components in the curator state.

## See also

- [DiffDock skill](../../catalog/tools/diffdock.html)
- [AlphaFold MCP server](../../catalog/tools/alphafold.html)
- [MedChem skill](../../catalog/tools/medchem.html)
- [DeepChem skill](../../catalog/tools/deepchem.html)
- [molecular-dynamics skill](../../catalog/tools/molecular-dynamics.html)
- [Triage an AlphaFold model for structure-based drug design](triage-alphafold-model-for-docking.html) — the upstream pre-flight; this recipe assumes the target has already passed pocket-pLDDT triage.
- [Filter a virtual screening hit list with drug-likeness rules and structural alerts](filter-virtual-screening-hits.html) — the natural downstream filter on the kept ligands.
- [Set up a protein molecular dynamics simulation in GROMACS from a PDB ID](set-up-protein-md-simulation-in-gromacs.html) — the MD-refinement / MM-PBSA rescoring step for the top-K poses.

## Sources

- [`K-Dense-AI/claude-scientific-skills` — diffdock SKILL.md](https://github.com/K-Dense-AI/claude-scientific-skills/blob/main/scientific-skills/diffdock/SKILL.md) — verified 2026-06-03 (this run).
- [`gcorso/DiffDock`](https://github.com/gcorso/DiffDock) — verified 2026-06-03 (this run).
- [Corso G. et al., "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking," ICLR 2023, arXiv:2210.01776](https://arxiv.org/abs/2210.01776) — published 2022-10.
- [Corso G. et al., "Deep confident steps to new pockets: strategies for docking generalization," ICLR 2024, arXiv:2402.18396](https://arxiv.org/abs/2402.18396) — published 2024-02.
- [Buttenschoen M. et al., "PoseBusters: AI-based docking methods fail to generate physically valid poses or generalise to novel sequences," *Chem. Sci.* 15:3130–3139 (2024)](https://doi.org/10.1039/D3SC04185A) — published 2024-01.
- [Karelina M. et al., "How accurately can one predict drug binding modes using AlphaFold models?" *J. Chem. Inf. Model.* 63:6219 (2023)](https://doi.org/10.1021/acs.jcim.3c00601) — published 2023-09.
- [AgentD: Multi-Agent Drug Discovery, arXiv:2507.02925](https://arxiv.org/abs/2507.02925) — published 2025-07.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=dock-ligand-library-with-diffdock&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdock-ligand-library-with-diffdock.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
