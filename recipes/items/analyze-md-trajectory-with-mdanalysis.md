---
title: Analyze an existing MD trajectory for stability, flexibility, and contacts
parent: All recipes
grand_parent: Recipes
nav_order: 1
problem_class: Data analysis
subject_areas: [Chemistry, Integrative Structural and Computational Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-06-13
summary: Drive the MDAnalysis skill (MDTraj as backup) to take a finished GROMACS/AMBER/NAMD trajectory through RMSD/RMSF/Rg, contact maps, H-bonds, and PCA without writing the analysis script by hand.
---

# Analyze an existing MD trajectory for stability, flexibility, and contacts

You already have a trajectory — from GROMACS, AMBER, NAMD, CHARMM, or a collaborator — and need the standard post-simulation readout: did it equilibrate, which residues move, what contacts persist, and what the dominant motions are. This recipe drives the [MDAnalysis skill](../../catalog/tools/mdanalysis-trajectory.html) to do all of it from one prompt.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Chemistry, Integrative Structural and Computational Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

The simulation finished overnight. You have a topology and a multi-gigabyte `.xtc`/`.dcd`/`.nc` trajectory, and now you need the analysis that decides whether the run is usable: backbone RMSD to confirm the structure equilibrated, per-residue RMSF to find the flexible loops, radius of gyration to check for unfolding, a residue-residue contact map to see which interactions survived, hydrogen-bond occupancy across a binding interface, and PCA to extract the dominant collective motions. None of this requires running MD — it requires getting the atom selections right, aligning frames before RMSF, skipping the equilibration window, and not running out of RAM on a long trajectory. Writing that script from scratch each time, looking up MDAnalysis's selection grammar and the `align.AlignTraj`-before-RMSF gotcha, is exactly the boilerplate an agent should absorb.

Solved looks like: point Claude at the topology and trajectory, state the selections and the analysis window, and get back labelled plots plus a numeric summary you can paste into a figure or a methods section.

## Recommended approach

1. **Install the [MDAnalysis skill](../../catalog/tools/mdanalysis-trajectory.html)** from the SciAgent-Skills collection (clone the repo and `/plugin install sciagent-skills`, or copy the `mdanalysis-trajectory` skill into `~/.claude/skills/`). The skill declares its own Python deps (`MDAnalysis`, `numpy`, `matplotlib`); let it install them on first use. Keep the [MDTraj skill](../../catalog/tools/mdtraj-trajectory-analysis.html) installed too as a fallback for DSSP secondary structure and Ramachandran torsions.

2. **Load the trajectory and sanity-check it before any analysis.** Prompt:

   ```
   Load topology md/prod.gro and trajectory md/prod.xtc with MDAnalysis.
   Report: number of frames, time per frame, total simulated time,
   number of atoms, number of protein residues, and whether the box
   is present. Do NOT analyze yet — just confirm the Universe loaded
   and tell me the frame stride so I can choose an analysis window.
   ```

   This catches the common mismatch (topology atom count != trajectory atom count) before you waste a pass over a large file.

3. **RMSD / RMSF / Rg over the production window.** Specify the equilibration cutoff explicitly:

   ```
   On the loaded Universe, using frames from t = 10 ns onward
   (drop equilibration):
     - Backbone RMSD vs the first analyzed frame, after RMSD-fitting
       on backbone atoms (use align.AlignTraj first).
     - Per-residue RMSF on CA atoms, computed on the aligned trajectory.
     - Radius of gyration time series for the protein selection.
   Save plots to md/analysis/{rmsd,rmsf,rg}.png and write the mean
   RMSD over the window, mean Rg, and the top-5 residues by RMSF to
   md/analysis/summary.md. Flag any CA RMSF > 0.3 nm as a flexible
   region.
   ```

   The `align.AlignTraj`-before-RMSF instruction matters: RMSF on an un-aligned trajectory measures overall tumbling, not internal flexibility.

4. **Contacts and hydrogen bonds across the interface you care about.** Name the two selections:

   ```
   Selection A = "protein and resid 50-70" (the loop)
   Selection B = "protein and resid 120-140" (the partner helix)
   Over the same t >= 10 ns window:
     - Residue-residue minimum-distance contact frequency map between
       A and B (contact if any heavy-atom pair < 4.5 A), save as a
       heatmap.
     - Hydrogen bonds between A and B with the HydrogenBondAnalysis
       module; report each donor-acceptor pair and its % occupancy,
       sorted descending.
   Save to md/analysis/contacts.png and md/analysis/hbonds.csv.
   ```

5. **PCA on the backbone for the dominant motions.** Closing prompt:

   ```
   Run PCA on backbone coordinates over t >= 10 ns:
     - Scree plot of the first 10 PCs (variance explained).
     - Project the trajectory onto PC1 and PC2; save the 2D
       projection scatter coloured by time.
     - Report the cumulative variance captured by PC1-3.
   Save to md/analysis/pca_*.png. If PC1-3 capture < 60% of variance,
   note that the motion is diffuse rather than dominated by a single mode.
   ```

   For 8-state DSSP secondary-structure timelines or Gly/Pro-aware Ramachandran plots, switch to the [MDTraj skill](../../catalog/tools/mdtraj-trajectory-analysis.html) — it wraps DSSP and the torsion helpers directly.

## Why this assembly

Rung 2 of the simplicity ladder, and it stops there. The analysis is pure post-processing of a file you already have, and the [MDAnalysis skill](../../catalog/tools/mdanalysis-trajectory.html) already encodes the selection grammar, the multi-format readers (GROMACS/AMBER/NAMD/CHARMM/LAMMPS), and the analysis modules (RMSD/RMSF/Rg/contacts/H-bonds/PCA). One skill covers every step above. Plain Claude Code with no skill *can* import MDAnalysis via Bash, but it re-derives the align-before-RMSF idiom and the selection syntax each session and tends to compute RMSF on an un-fitted trajectory. A multi-tool harness adds nothing — there is a single library doing the work; MDTraj is a complementary fallback (DSSP, Ramachandran), not a third coordinating layer. Rung 4 (an autonomous MD agent like MDCrow) is for *planning* across simulation and analysis, not for running a fixed analysis battery on a finished trajectory.

## Availability

Fully open. The [MDAnalysis skill](../../catalog/tools/mdanalysis-trajectory.html) is community OSS (skill content CC BY 4.0; MDAnalysis itself GPL-2.0). The [MDTraj skill](../../catalog/tools/mdtraj-trajectory-analysis.html) fallback is LGPL-2.1. No subscription, account, or institutional licence is required. The only cost is the Claude inference that drives the skill.

## Compute requirements

Workstation, GPU optional. The analysis itself is CPU-bound NumPy, not GPU work — the "GPU" tier reflects that the trajectories you analyze typically come from GPU MD runs, not that analysis needs one. A 50 ns trajectory of a ~300-residue protein at 10 ps stride (~5000 frames) runs the full RMSD/RMSF/Rg/contacts/PCA battery in 2–10 minutes on a laptop with 16 GB RAM. The memory ceiling is the binding constraint: MDAnalysis streams frames so it stays modest, but PCA and contact maps that materialise full coordinate arrays can spike — for trajectories above ~50k frames, analyze in a `transformations`/in-memory slice of the production window rather than loading everything. Disk: outputs are a handful of PNGs and CSVs, <10 MB.

## Evidence

Proposed. No documented end-to-end attempt of "Claude Code + the MDAnalysis skill" on a published benchmark is known. The closest evidence is at the component and the agent-class level:

- **MDAnalysis** ([Michaud-Agrawal et al., *J. Comput. Chem.* 32:2319 (2011), DOI:10.1002/jcc.21787](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.21787); [Gowers et al., *SciPy* 2016](https://doi.org/10.25080/Majora-629e541a-00e)) is the canonical, decade-validated analysis library underneath the skill — the analysis steps above are its documented core use, tested on systems of millions of particles.
- **MDTraj** ([McGibbon et al., *Biophys. J.* 109:1528 (2015), DOI:10.1016/j.bpj.2015.08.015](https://doi.org/10.1016/j.bpj.2015.08.015)) backs the fallback path (DSSP, contacts, torsions).
- **MDCrow** ([Campbell et al., *Mach. Learn. Sci. Technol.* 2025, DOI:10.1088/2632-2153/ae4b07](https://iopscience.iop.org/article/10.1088/2632-2153/ae4b07); [arXiv:2502.09565](https://arxiv.org/abs/2502.09565)) showed an LLM agent reliably driving MD *analysis* tools (RMSD, RMSF, Rg, PCA over named modules with file-based hand-off) as part of its 25-task suite — the same analysis shape this recipe automates.
- **MDGym** ([arXiv:2605.08941](https://arxiv.org/abs/2605.08941), 2026) is the caution: agents are weak at autonomous end-to-end MD *setup*. This recipe deliberately scopes to analysis of an already-finished trajectory, where the work is deterministic library calls, not the open-ended setup MDGym found hard.

## Alternatives considered

- **Plain Claude Code, no skill.** Workable for a one-off if you are happy to inspect every MDAnalysis call. The skill earns its place by encoding the align-before-RMSF idiom and the selection grammar so the first pass is correct; reach for bare Claude only when you want to hand-write the analysis yourself.
- **Do the analysis inside the GROMACS Copilot.** The [Set up a protein MD simulation in GROMACS](set-up-protein-md-simulation-in-gromacs.html) recipe already produces RMSD/RMSF/Rg as a closing step. Use that when you are running the simulation in the same session. Use *this* recipe when the trajectory already exists, came from a non-GROMACS engine, or needs analysis the Copilot's closing step does not cover (contact maps, H-bond occupancy, interface-specific selections).
- **MDCrow (autonomous rung).** Not currently wrapped in [`autonomous-science/systems/`](../../autonomous-science/) as a recommendable component. Reach for it directly from its repo when you need an agent that *decides which* analyses to run from a scientific question, rather than running the fixed battery above.

## See also

- [MDAnalysis (Claude Skill)](../../catalog/tools/mdanalysis-trajectory.html)
- [MDTraj (Claude Skill)](../../catalog/tools/mdtraj-trajectory-analysis.html)
- [Set up a protein MD simulation in GROMACS](set-up-protein-md-simulation-in-gromacs.html) — the upstream recipe that produces the trajectory this one analyzes.
- [Triage an AlphaFold model for structure-based drug design](triage-alphafold-model-for-docking.html) — for static-structure quality checks before you ever simulate.

## Sources

- [`jaechang-hits/SciAgent-Skills` — mdanalysis-trajectory](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/mdanalysis-trajectory/SKILL.md) — verified 2026-06-13 (this run).
- [Michaud-Agrawal, Denning, Woolf, Beckstein — MDAnalysis, *J. Comput. Chem.* 32:2319 (2011)](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.21787) — published 2011; verified 2026-06-13.
- [McGibbon et al. — MDTraj, *Biophys. J.* 109:1528 (2015)](https://doi.org/10.1016/j.bpj.2015.08.015) — published 2015.
- [Campbell et al. — MDCrow, *Mach. Learn. Sci. Technol.* 2025, DOI:10.1088/2632-2153/ae4b07](https://iopscience.iop.org/article/10.1088/2632-2153/ae4b07) — published 2025; verified 2026-06-13.
- [MDGym — arXiv:2605.08941](https://arxiv.org/abs/2605.08941) — published 2026-05.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=analyze-md-trajectory-with-mdanalysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fanalyze-md-trajectory-with-mdanalysis.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
