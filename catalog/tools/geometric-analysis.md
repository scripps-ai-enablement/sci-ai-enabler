---
title: Geometric Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-08-08
summary: "Measure static protein structures with Bio.PDB — distances, dihedrals, superposition and RMSD, radius of gyration, and SASA — with the caveats stated"
verification: works
verified_on: 2026-08-10
reviewed_on: 2026-08-10
security: cleared
security_on: 2026-08-10
security_note: "GPTomics/bioSkills MIT root confirmed, provenance matches, Biopython BSD and DSSP now Boost/BSD-2 (confirmed this run)"
---

# Geometric Analysis (bioSkills)

A Claude Code skill for taking careful measurements on a static structure: how far apart two atoms are, what the backbone dihedrals do, how much surface is buried, and what an RMSD number actually means.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — Biopython (BSD-style) and the DSSP binary are installed separately |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |
| **Verified** | works · 2026-08-10 |
| **Security** | cleared · 2026-08-10 — MIT, provenance matches, Biopython BSD, DSSP now Boost/BSD-2 |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "structural-biology"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/structural-biology/geometric-analysis ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites**:
  ```
  pip install "biopython>=1.83" "numpy>=1.26"
  conda install -c conda-forge -c bioconda dssp
  ```
  The DSSP v4 binary (`mkdssp`) is only needed for secondary-structure and some SASA workflows; the distance, dihedral and superposition paths are pure Biopython.

## What it does

- **Parsing and selection** — `PDBParser` into a structure, then atom/residue filtering; the hetflag test (`residue.id[0] == ' '`) is used to drop waters and heteroatoms before measuring, which is where most silently-wrong numbers come from.
- **Distances** — interatomic distances and full distance matrices.
- **Angles** — bond angles and dihedrals, including backbone phi/psi (Ramachandran) and side-chain chi.
- **Superposition and RMSD** — Kabsch/SVD alignment via `Superimposer`, or `QCPSuperimposer` when speed matters.
- **Bulk descriptors** — center of mass, radius of gyration.
- **Surface** — solvent-accessible surface area, reported alongside the probe radius used.
- **Reporting discipline** — every metric is reported with its context: which atoms were selected, which probe radius, which algorithm.

Reference values the skill treats as rules of thumb rather than laws: relative SASA **< 0.20** as a common buried-residue heuristic, a rigid-core RMSD cutoff around **2.0 Å**, **TM-score > 0.5** for "same fold" (length-normalized and asymmetric), and Ramachandran outliers in disallowed regions read as refinement errors rather than biology.

**Primary use cases**: measuring a specific contact or dihedral to support a mechanistic claim, comparing two conformations of the same protein, quantifying burial of a residue of interest.

## Notes

The headline warning is worth internalizing: **RMSD is not a property of a structure**. It depends jointly on the superposition and the atom selection, and a global all-atom RMSD is dominated by the worst-fitting atoms — it will hide a near-perfect core behind a couple of flexible loops. Related trap: `Superimposer` requires equal-length, ordered atom lists and does *not* solve the correspondence problem; feeding it mismatched lists produces a number rather than an error.

This skill measures **static structures**. For the same quantities computed over a molecular-dynamics trajectory, use [MDTraj](mdtraj-trajectory-analysis.html) or [MDAnalysis](mdanalysis-trajectory.html) instead; for fold-level comparison across a database rather than a pairwise measurement, see [Foldseek](foldseek-structural-search.html). Within the bioSkills structural set it sits downstream of [Structure Preparation](structure-preparation.html) and alongside [Structure Validation](structure-validation.html) (which judges reliability) and [Interface Analysis](interface-analysis.html) (which applies the same SASA machinery to buried surface between chains); [Biopython](biopython.html) is the underlying library as its own catalog entry.

Upstream skill front-matter name is `bio-structural-biology-geometric-analysis`; upstream directory `structural-biology/geometric-analysis`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`structural-biology/geometric-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/geometric-analysis/SKILL.md)
- [Biopython `Bio.PDB` documentation](https://biopython.org/docs/latest/api/Bio.PDB.html)
- [DSSP v4 (`mkdssp`)](https://github.com/PDB-REDO/dssp)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=geometric-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fgeometric-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
