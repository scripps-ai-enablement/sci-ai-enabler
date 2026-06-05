---
title: Set up a protein molecular dynamics simulation in GROMACS from a PDB ID
parent: All recipes
grand_parent: Recipes
nav_order: 24
problem_class: Experimental design
subject_areas: [Chemistry, Integrative Structural and Computational Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-06-01
summary: Drive the GROMACS Copilot component of molecule-mcp to take a PDB ID through topology, solvation, ion neutralisation, minimisation, NVT/NPT equilibration, and a short production MD, with RMSD/RMSF/Rg analysis on the resulting trajectory.
---

# Set up a protein molecular dynamics simulation in GROMACS from a PDB ID

Hand Claude Code a PDB ID and a target production length; get back a GROMACS-ready workspace — topology built with the chosen force field, the protein solvated and neutralised, energy-minimised, NVT and NPT equilibrated, and a production trajectory with RMSD, RMSF, and radius-of-gyration analysis — without ever typing `pdb2gmx` or `genion` by hand.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Chemistry, Integrative Structural and Computational Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

A wet-lab structural biologist or a computational chemist looking at a new target wants a quick MD sanity check: pull the PDB structure, run a short MD, see whether the loop near the binding pocket is genuinely flexible or whether the crystal lattice was holding it still, look at RMSF per residue, and decide whether to commit to a microsecond-scale production run. The mechanical work to get there — `pdb2gmx` with the right force field, `editconf` for a properly-sized box, `solvate`, `genion` with the matching neutral-pH counter-ion budget, `grompp` + `mdrun` × 3 stages (minimisation / NVT / NPT) before production — is exactly the kind of multi-step CLI plumbing where one wrong group index ("which is `Protein`? which is `SOL`?") silently produces nonsense.

Solved looks like: one natural-language prompt, a workspace directory with each stage's outputs, and a final RMSD/RMSF/Rg report — close enough to run yourself when something fails, automated enough to skip when nothing does.

## Recommended approach

1. **Install the [molecule-mcp bundle](../../catalog/tools/molecule-mcp.html)** — register the GROMACS Copilot server alongside the PyMOL and ChimeraX visualisation servers:

   ```
   pip install "mcp[cli]" chatmol
   git clone https://github.com/chatmol/molecule-mcp
   claude mcp add --transport stdio gromacs_copilot \
     -- python /path/to/molecule-mcp/mcp_server.py
   ```

   The Copilot itself sits behind the MCP server; install it once:

   ```
   pip install git+https://github.com/ChatMol/gromacs_copilot.git
   conda install -c conda-forge gromacs        # if not already
   ```

   GROMACS itself must be on `PATH` (`gmx` resolvable). Confirm with `gmx --version` and `claude mcp list`.

2. **Pick a workspace, fetch the structure, declare your defaults.** Prompt:

   ```
   Create workspace md/1pga_2026_q2/ and set:
     - force field: charmm36-jul2022
     - water model: tip3p
     - box: cubic, 1.2 nm padding
     - salt: 0.15 M NaCl, neutralise charge
     - integrator timestep: 2 fs (with H-bond constraints)
   Download PDB 1PGA into the workspace as protein.pdb.
   Strip crystallographic waters and ligands; keep one biological
   chain. Stop and ask me to confirm before any topology generation.
   ```

   The "stop and confirm" step is important: the LLM occasionally picks the wrong selection group index when GROMACS prompts interactively, and confirming the chosen chain and residue range catches this before topology is built.

3. **Run the four-stage prep.** A single prompt covers it:

   ```
   In md/1pga_2026_q2/, build topology with pdb2gmx (CHARMM36, TIP3P),
   solvate to the declared padding, neutralise with NaCl, then run:
     - energy minimisation (steep, Fmax < 1000 kJ/mol/nm)
     - NVT equilibration, 100 ps, V-rescale @ 300 K
     - NPT equilibration, 100 ps, Parrinello-Rahman @ 1 bar
   For each stage, dump the .mdp file used, the final .gro, and the
   energy / temperature / pressure plot. Stop if any stage fails to
   converge.
   ```

4. **Production MD with explicit GPU offload.** Keep the production prompt small enough that a re-run is cheap:

   ```
   Run 50 ns production MD from the NPT-equilibrated state:
     - dt 2 fs, 25 000 000 steps
     - trajectory output every 10 ps
     - GPU offload: nonbonded + PME on GPU 0
     - LINCS for H-bonds, PME for electrostatics, 1.2 nm cutoffs
   Save md.xtc, md.gro, md.edr. Print the wall-clock and ns/day.
   ```

   `gmx mdrun -nb gpu -pme gpu -update gpu` is the canonical flag set on a single GPU; let the Copilot pick threads/pinning but verify the printed command line.

5. **RMSD / RMSF / Rg analysis.** Closing prompt:

   ```
   On md.xtc + md.gro:
     - Backbone RMSD vs the starting NPT frame
     - Per-residue RMSF averaged over the last 40 ns
     - Radius of gyration time series
     - PCA on backbone coordinates (first 3 PCs, scree plot)
   Save plots to md/1pga_2026_q2/analysis/*.png and a summary.md
   with: mean Rg, mean RMSD over last 40 ns, top-5 residues by RMSF.
   Flag any RMSF > 0.5 nm region as a candidate flexible loop.
   ```

   Hand the resulting workspace and `summary.md` off to a structural biologist for the actual scientific call.

## Why this assembly

Rung 2 of the simplicity ladder. The MD setup is mechanical but unforgiving: pick the wrong group index in `genion`, get a topology that minimises but blows up in NPT; forget `LINCS`, lose the 2 fs timestep; mis-pin GPU offload, run at 1/5 the throughput. The [molecule-mcp](../../catalog/tools/molecule-mcp.html) bundle exposes the GROMACS Copilot agent over MCP so Claude can drive `gmx` end-to-end with named-stage outputs and stop-on-failure. Plain Claude Code can call `gmx` directly via Bash, but it re-derives the workflow every session and the group-index issue resurfaces. A multi-tool harness adds nothing here — the agent loop is *inside* the Copilot. Rung 4 (a full autonomous-science system like MDCrow or DynaMate) is overkill for the single-target workflow this recipe targets, but is the right escalation if you need broader tool coverage (PCA-driven analysis, RG-based clustering, batch over many PDBs) — see Alternatives.

## Availability

Fully open. The [molecule-mcp](../../catalog/tools/molecule-mcp.html) bundle is MIT-licensed; [GROMACS Copilot](https://github.com/ChatMol/gromacs_copilot) is MIT-licensed; GROMACS itself is LGPL-2.1. CHARMM36 force-field parameters are free for academic use (registration with the MacKerell lab). No subscription or institutional licence required, but the LLM backend the Copilot calls (OpenAI, DeepSeek, or your own) does carry inference cost — the Copilot is model-agnostic.

## Compute requirements

Workstation with GPU. A 50 ns production MD of a ~60-residue protein in a ~5 nm cubic TIP3P box runs at ~80–150 ns/day on a single RTX 4090 / A6000 with `-nb gpu -pme gpu -update gpu`, so the production run above completes in 8–16 hours of wall-clock. Setup and equilibration are <30 min total on the same hardware. RAM budget: 16 GB system + 12–16 GB VRAM. CPU-only is feasible but ~10× slower and not recommended past 10 ns. Disk: ~500 MB per ns of trajectory at 10 ps stride; budget 25 GB for a 50 ns run. For an HPC cluster, the same prompts work via `mdrun -ntomp/-ntmpi` settings; let the Copilot emit the command and edit the thread/MPI counts before submission.

## Evidence

Proposed. No documented end-to-end attempt of "Claude Code + molecule-mcp GROMACS Copilot" on a published benchmark is known. The closest class-level evidence:

- **MDCrow** ([Campbell et al., *Machine Learning: Science and Technology* 2025, DOI:10.1088/2632-2153/ae4b07](https://iopscience.iop.org/article/10.1088/2632-2153/ae4b07); [arXiv:2502.09565](https://arxiv.org/abs/2502.09565)) — assessed an LLM agent across 25 MD tasks of varying complexity; with GPT-4o it completes complex multi-step setups with low variance, significantly outperforming a plain LLM (t-test p=1×10⁻³) and ReAct (p=4×10⁻⁴). Uses OpenMM, not GROMACS — but the architecture (chain-of-thought over named MD tools, file-based hand-off between stages) is the same shape the Copilot uses.
- **DynaMate** ([arXiv:2512.10034](https://arxiv.org/abs/2512.10034), 2025) — multi-agent extension that supports both AmberTools and GROMACS and handles protein-ligand complexes, demonstrating the GROMACS path is tractable for LLM agents.
- **NAMD-Agent** ([arXiv:2507.07887](https://arxiv.org/abs/2507.07887), 2025) — protein-system setup via CHARMM-GUI web automation, showing LLM agents can manage force-field-aware setup choices reliably.
- **MDGym benchmark** ([arXiv:2605.08941](https://arxiv.org/abs/2605.08941), 2026) — 169 expert-curated MD simulations spanning LAMMPS and GROMACS evaluated across Claude Code, Codex, and OpenHands. All agents perform poorly (≤21% on easy tier, <10% at higher difficulties). Read as a caution: do not expect autonomous reliability past the workflow above; keep a human in the loop for the production-length choice and the analysis call.

[GROMACS Copilot](https://github.com/ChatMol/gromacs_copilot) itself is presented by ChatMol as a v0.2 community project with protein-ligand support and DeepSeek / OpenAI / Anthropic backends; no peer-reviewed benchmark of the Copilot is published as of 2026-06-01.

## Alternatives considered

- **Plain Claude Code, no MCP.** Claude can call `gmx` via Bash directly, and for a single PDB an experienced user can shepherd it through. Reach for plain Claude when you only need to re-run a known workflow or when you would rather inspect every `gmx` command line yourself. The MCP wrapper adds the stage-by-stage memory and the failure-handling loop.
- **MDCrow / DynaMate (autonomous-science rung).** Neither is currently in [`autonomous-science/systems/`](../../autonomous-science/) as a wrapped component this cookbook can recommend. Use them directly from their repos when you need an agent that *plans* across a wider tool surface — for example, deciding between OpenMM and GROMACS, choosing the production length from the user-stated scientific question, or doing PCA-clustering-driven sampling. The recipe above stops short of that planning.
- **A full free-energy / FEP workflow.** Out of scope. The molecule-mcp bundle does not wrap an FEP engine; pair this recipe with a dedicated FEP tool when you need ΔG, not just trajectory analysis.

## See also

- [Molecule-MCP (MCP server bundle)](../../catalog/tools/molecule-mcp.html)
- [Triage an AlphaFold model for structure-based drug design](triage-alphafold-model-for-docking.html) — natural upstream step if you do not have an experimental PDB.

## Sources

- [`ChatMol/gromacs_copilot`](https://github.com/ChatMol/gromacs_copilot) — verified 2026-06-01 (this run).
- [`chatmol/molecule-mcp`](https://github.com/chatmol/molecule-mcp) — verified 2026-06-01 (this run).
- [Campbell, Cox, Medina, Cox, Sun, Lin, Wang, Cox, Diaz, White — MDCrow, *Mach. Learn. Sci. Technol.* 2025, DOI:10.1088/2632-2153/ae4b07](https://iopscience.iop.org/article/10.1088/2632-2153/ae4b07) — published 2025; verified 2026-06-01.
- [MDCrow arXiv preprint — arXiv:2502.09565](https://arxiv.org/abs/2502.09565) — published 2025-02-13.
- [DynaMate — arXiv:2512.10034](https://arxiv.org/abs/2512.10034) — published 2025-12.
- [NAMD-Agent — arXiv:2507.07887](https://arxiv.org/abs/2507.07887) — published 2025-07.
- [MDGym — arXiv:2605.08941](https://arxiv.org/abs/2605.08941) — published 2026-05.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=set-up-protein-md-simulation-in-gromacs&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fset-up-protein-md-simulation-in-gromacs.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
