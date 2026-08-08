---
title: Rank the conformers and tautomers of a small molecule with semi-empirical QM
parent: All recipes
grand_parent: Recipes
nav_order: 20
problem_class: Data analysis
subject_areas: [Chemistry, Integrative Structural and Computational Biology, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-08
summary: Drive the ChemGraph MCP server to optimize and free-energy-rank enumerated tautomers and conformers at GFN2-xTB, emitting a populations table instead of one guessed structure.
---

# Rank the conformers and tautomers of a small molecule with semi-empirical QM

Enumerate the plausible tautomers and conformers of a compound, optimize each one with semi-empirical quantum chemistry through [ChemGraph](../../catalog/tools/chemgraph.html), and get back a Boltzmann-population table — so the 3D structure you carry into docking, descriptor calculation, or spectral assignment is the one the energetics actually support.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Chemistry, Integrative Structural and Computational Biology, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A SMILES string drawn in a paper, pulled from a vendor catalog, or emitted by a generative model encodes *one* tautomer and *no* conformation. Both are choices, and both are usually made by whoever typed the string rather than by the molecule. Hydroxypyridines, amidines, guanidines, 2-aminothiazoles, and almost any ring with an exocyclic N or O have tautomers that differ by a few kcal/mol — small enough that the drawn form is often not the dominant one, large enough to change hydrogen-bond donor/acceptor counts, formal charge distribution, and therefore every docking pose, every ADMET descriptor, and every predicted NMR shift downstream.

Force fields cannot arbitrate this. A tautomer shift is a change in bond topology, so MMFF or UFF are comparing two different molecules with two different parameter sets — the relative energies are meaningless. DFT can arbitrate it, but a realistic candidate set is 3–6 tautomers × 20–100 conformers each, and optimizing several hundred structures at DFT is a cluster job. "Solved" here means: a ranked, free-energy-based table of candidate states with populations and an explicit statement of which ones are too close to call, produced cheaply enough that you run it on every compound rather than on the one that later turned out to matter.

## Recommended approach

1. **Install [ChemGraph](../../catalog/tools/chemgraph.html)** with the `[calculators]` extra — that pulls in TBLite, the xTB backend, which is the one that works without a separate engine install. The catalog page owns the verbatim `pip install` and `claude mcp add` commands, including the absolute-venv-python detail that the registration needs. Work in a scratch directory: `run_ase` executes real calculations and writes coordinate and JSON files to disk.

2. **Enumerate candidate states in a committed script, tautomers before conformers.** Ask Claude Code to write `enumerate_states.py` using RDKit (see **Dependencies**): `rdMolStandardize.TautomerEnumerator` over the input SMILES, then `AllChem.EmbedMultipleConfs` with ETKDGv3 and a fixed `randomSeed` on *each* tautomer separately, MMFF pre-optimization, and RMSD pruning. The ordering is load-bearing — a tautomer has a different bond topology and therefore a different conformer space, so conformers generated for the drawn form do not transfer. Output `candidates.csv` (one row per `state_id`, carrying tautomer SMILES, conformer index, and the path to an XYZ file) plus the XYZ files themselves.

   ```
   Write enumerate_states.py. Read input.smi. For each input SMILES:
   enumerate tautomers with rdMolStandardize.TautomerEnumerator, then for each
   tautomer embed conformers with ETKDGv3 (randomSeed=0xC0FFEE), MMFF-optimize,
   prune at 0.5 A heavy-atom RMSD. Write candidates.csv and one XYZ per state.
   Print the tautomer and conformer counts per input compound.
   ```

3. **Optimize and run frequencies on every candidate at GFN2-xTB.** Have Claude drive ChemGraph's `run_ase` over `candidates.csv` — geometry optimization first, then a vibrational-frequency job on the optimized geometry, with `extract_output_json` reading the results back. **Gate on the frequency calculation.** A structure the optimizer declared converged but that carries imaginary frequencies is a saddle point, not a minimum, and it will otherwise sit in your table looking like a real state. Declare the solvation model explicitly (ALPB/GBSA with a named solvent, or gas phase) and record it: tautomer orderings routinely invert between gas phase and water, so an undeclared solvation choice silently decides the answer.

4. **Rank on free energy, not electronic energy.** Write `rank_states.py` to assemble `state_energies.csv` — `state_id`, tautomer SMILES, electronic energy, ZPE, thermal correction, G(298.15 K), ΔG relative to the global minimum in kcal/mol, Boltzmann population, and the imaginary-frequency count. ZPE and entropy differ enough between tautomers that the electronic-energy ordering and the free-energy ordering disagree more often than people expect; the free energy is what a population is defined on.

5. **Emit rejections and ties as first-class outputs.** `rejected_states.csv` takes every candidate with `n_imag > 0`, a failed SCF, or a non-converged optimization, each with a reason string. And treat the top of the table honestly: GFN2-xTB is a semi-empirical method, so any two states within roughly 1 kcal/mol of each other are **not** resolved by this calculation. Have the script set a `too_close_to_call` flag on that group rather than reporting a single winner, and carry every flagged state into whatever comes next — docking two tautomers is cheap; docking the wrong one is not.

6. **Record provenance.** Write `provenance.json` with the `chemgraph` and TBLite/xtb versions, the Hamiltonian (`GFN2-xTB`), the solvation model and solvent, the optimizer and its convergence thresholds, the temperature used for the thermochemistry, the RDKit version and the ETKDG random seed, the sha256 of `input.smi`, and the model id that authored the scripts. Commit `enumerate_states.py`, `rank_states.py`, `requirements.txt`, and `provenance.json`; the seed and the solvation model are the two fields that make the run re-derivable. See the [reproducibility guide](../../guide/advanced/reproducibility.html) for the pattern.

## Dependencies

Libraries this recipe's script installs and imports directly. Claude Code installs these into your project environment — they are not available in Claude.ai chat. ChemGraph itself is a catalogued MCP server and is installed from its own page, not here.

| Package | Registry | Pinned | License | Import | Source (fetched 2026-08-08) |
|---|---|---|---|---|---|
| rdkit | PyPI | `2026.3.5` | BSD-3-Clause | `rdkit` | [rdkit on PyPI](https://pypi.org/project/rdkit/) |

```
pip install rdkit==2026.3.5
python3 -c "import rdkit"
```

No first-run downloads — RDKit ships its own data tables in the wheel.

## Why this assembly

Rung 2. The hard part is not the chemistry decision, it is that running a few hundred xTB jobs by hand means writing a few hundred input decks and parsing a few hundred outputs, and that is exactly what [ChemGraph](../../catalog/tools/chemgraph.html)'s `run_ase` / `extract_output_json` pair removes — Claude issues the calculations as tool calls and reads structured JSON back, so the loop lives in a committed script rather than in a shell-history archaeology exercise.

Rung 1 does not reach: plain Claude Code can shell out to `xtb`, but it re-derives the deck format each session, and the failure mode is quiet — a mis-set `--gfn` flag or a dropped `--opt` still produces numbers. Rung 3 adds nothing: enumeration is a single RDKit call inside the recipe's own script, which is what the **Dependencies** mechanism is for. Rung 4 is unwarranted for a single-compound calculation.

## Availability

Fully open, and fully local. ChemGraph is Apache-2.0, TBLite/xTB is LGPL-3.0, RDKit is BSD-3-Clause; no subscription, no registration, no institutional licence. Structures never leave the machine, which matters for unpublished chemistry — this is the contrast with the cloud-side path in [prepare-protonation-states-for-docking](prepare-protonation-states-for-docking.html). One exception: ChemGraph's `molecule_name_to_smiles` resolves names against PubChem, so skip that tool and supply SMILES directly if the structure is confidential. ChemGraph is Beta.

## Compute requirements

Laptop. A GFN2-xTB optimization on a 40-heavy-atom drug-like molecule is seconds on one core; the frequency job is the expensive half and is typically a few times the optimization. A realistic set — 5 tautomers × 40 conformers, optimization plus frequencies — runs in tens of minutes on a modern laptop and parallelizes trivially across cores, since every state is independent. Disk, not CPU, is the surprise: `run_ase` writes coordinate and JSON files per job, so a multi-compound sweep leaves thousands of files behind. Keep it in a scratch directory and archive only `state_energies.csv`, `rejected_states.csv`, and the XYZ files of the surviving states.

Escalating the top few states to DFT for a publication-grade number is a different tier — a workstation or cluster — and is out of scope here. ChemGraph reaches NWChem and ORCA for exactly that, but a DFT job "requested casually in conversation" can consume real wall time, so drive it from an explicit script with an explicit candidate list.

## Evidence

Proposed. No documented attempt at this specific assembly — Claude Code driving the ChemGraph MCP server over an enumerated tautomer/conformer set — is known. The closest evidence is component-level:

- **ChemGraph itself was benchmarked across 13 tasks** spanning structure generation, single-point energies, geometry optimization, vibrational analysis, and thermochemistry. Smaller models handled simple workflows; more complex tasks benefited from larger models, and decomposing a complex task into subtasks let smaller models match or exceed the larger one ([Pham, Tanikanti & Keçeli, arXiv 2506.06363, 2025-06-03](https://arxiv.org/abs/2506.06363)). The evaluation used GPT-4o-class and Qwen models, not Claude Code, and the task decomposition finding is the direct argument for step 2's "commit a script" framing over a single open-ended request.
- **GFN2-xTB is the canonical method for this job.** Its authors designed it for fast structures and noncovalent interaction energies on systems of roughly 1000 atoms, report lower errors than prior semi-empirical methods on off-target properties including barrier heights and dipole moments, and describe it as "well-suited to explore the conformational space of molecular systems" ([Bannwarth, Ehlert & Grimme, *J Chem Theory Comput* 2019](https://pubmed.ncbi.nlm.nih.gov/30741547/)). That is a statement about *exploring* and narrowing, which is why step 5 refuses to resolve sub-kcal/mol gaps.
- **LLM agents orchestrating real electronic-structure calculations is a documented pattern, not a speculation.** An LLM-agent-driven workflow planned and coordinated AIMD sampling and DFT spectral calculations alongside robotic IR/Raman measurement for bridged azobenzene isomerization ([Shen et al., *Chem Sci* 2026](https://doi.org/10.1039/d5sc08794e)); a separate pipeline used LLM agents for electronic-structure code selection, input preparation, and output conversion when generating MLIP training data ([Lahouari, Rogal & Tuckerman, *J Chem Theory Comput* 2026](https://doi.org/10.1021/acs.jctc.5c01610)). Both keep the numerical work in conventional codes and use the agent for setup and orchestration — the same division of labour this recipe uses.

## Alternatives considered

**The [RDKit skill](../../catalog/tools/rdkit-skill.html) or [RDKit MCP](../../catalog/tools/rdkit-mcp.html) alone.** If all you need is a reasonable 3D conformer of a single drawn tautomer — for a figure, or as a docking input where the tautomer is not in question — ETKDG plus MMFF is sufficient and instant. Reach for this recipe only when the *ranking* is the deliverable.

**The [XTB MCP Server](../../catalog/tools/xtb-mcp-server.html).** It generates and validates xtb control decks but does not execute them, so it is the right tool when you have your own submission harness (an HPC queue, a workflow engine) and want the input files written correctly. It also covers setups ChemGraph does not expose — ONIOM partitions, metadynamics, spectroscopy. For the end-to-end "give me the ranked table" loop, ChemGraph's execute-and-parse pair is the shorter path.

**[Rowan](../../catalog/tools/rowan.html), via [prepare-protonation-states-for-docking](prepare-protonation-states-for-docking.html).** That recipe answers the adjacent question — which *protonation* state dominates at physiological pH — with a cloud-side macro-pKa workflow. Run it when the question is charge; run this one when the question is tautomer or conformer. They compose, and the sibling recipe is the one to use if you would rather not maintain a local QM install; the tradeoff is that SMILES leave your machine.

## See also

- [ChemGraph (MCP server)](../../catalog/tools/chemgraph.html)
- [XTB MCP Server](../../catalog/tools/xtb-mcp-server.html)
- [Prepare the correct protonation state of a ligand before docking](prepare-protonation-states-for-docking.html)
- [Dock a ligand library with DiffDock](dock-ligand-library-with-diffdock.html)
- [Set up a protein MD simulation in GROMACS](set-up-protein-md-simulation-in-gromacs.html)
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [ChemGraph: An Agentic Framework for Computational Chemistry Workflows](https://arxiv.org/abs/2506.06363) — published 2025-06-03; verified 2026-08-08 (this run).
- [GFN2-xTB — An Accurate and Broadly Parametrized Self-Consistent Tight-Binding Quantum Chemical Method](https://pubmed.ncbi.nlm.nih.gov/30741547/) — published 2019; canonical method reference, verified 2026-08-08 (this run).
- [Unlocking azobenzene isomerization mechanisms via an LLM agent-driven workflow](https://doi.org/10.1039/d5sc08794e) — published 2026; verified 2026-08-08 (this run).
- [Automated Machine Learning Pipeline: LLM-Assisted Automated Data set Generation for Training MLIPs](https://doi.org/10.1021/acs.jctc.5c01610) — published 2026; verified 2026-08-08 (this run).
- [rdkit on PyPI](https://pypi.org/project/rdkit/) — version 2026.3.5, BSD-3-Clause; fetched 2026-08-08 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=rank-conformers-and-tautomers-with-xtb&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Frank-conformers-and-tautomers-with-xtb.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
