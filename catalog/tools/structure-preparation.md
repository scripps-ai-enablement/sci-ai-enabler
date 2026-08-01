---
title: Structure Preparation (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-08-01
summary: "Make a deposited or predicted structure docking- or MD-ready with PDBFixer, reduce, PROPKA and PDB2PQR — hydrogens, tautomers, missing atoms, short loops"
---

# Structure Preparation (bioSkills)

A Claude Code skill that turns a deposited or predicted structure into one you can actually dock, simulate, or run electrostatics on — adding hydrogens, assigning protonation and tautomer states, and filling in what the experiment never resolved.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — PDBFixer, OpenMM, PROPKA 3 and PDB2PQR are separately installed OSS; `reduce`/Reduce2 ships with CCTBX/Phenix (free for academic use under its own licence) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python) and writes prepared structure files, not as an MCP tool |

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
  cp -r bioSkills/structural-biology/structure-preparation ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). The skill checks its own dependencies with `pip show <package>` and `<tool> --version` before running.

## What it does

Runs the preparation sequence and — the part that matters downstream — records what was *built* rather than observed:

- **Hydrogens** — adds the hydrogens an X-ray model never resolved, with `reduce`/Reduce2 for optimized placement.
- **Protonation and tautomers** — assigns His HID/HIE/HIP tautomers, Asn/Gln/His 180° flips, and pKa-shifted Cys/Lys/Asp/Glu states at a **stated pH and local microenvironment** using PROPKA 3, instead of assuming standard pKa values at pH 7.
- **Missing atoms and loops** — finds gaps by comparing SEQRES to modelled atoms, replaces nonstandard residues (MSE, PTR, other modified forms) with their standard parents, fills missing side-chain atoms, and models short missing loops explicitly as *disorder hypotheses* rather than as data.
- **Predicted models** — the prep path for an AlphaFold/ESMFold model after low-pLDDT regions have been trimmed.
- **Electrostatics output** — writes a PQR file with PDB2PQR 3.0 for Poisson–Boltzmann calculations.
- **Components** — PDBFixer 1.9+ (primary), OpenMM 8.1+, plus the separately installed CLI tools `reduce`/Reduce2, PROPKA 3 and PDB2PQR 3.0 (conda-forge or pip).

**Primary use cases**: docking receptor prep, MD system setup, Poisson–Boltzmann electrostatics input, cleaning up a predicted model.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-structural-biology-structure-preparation`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/structure-preparation`. The three CLI dependencies are not installed by the skill and are the usual friction point — `reduce` in particular normally arrives via a CCTBX or Phenix installation rather than pip. Sits between the catalogued [Structure Validation](structure-validation.html) skill (decide whether the model is usable, trim low-pLDDT regions) and the downstream simulation and docking entries [OpenMM MCP Server](openmm-mcp.html), [GROMACS MCP Server](gromacs-mcp.html), [AutoDock Vina](autodock-vina-docking.html) and [smina](smina-molecular-docking.html). Upstream directory: `structural-biology/structure-preparation`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`structural-biology/structure-preparation/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/structure-preparation/SKILL.md)
- [PDBFixer](https://github.com/openmm/pdbfixer)
- [PROPKA 3](https://github.com/jensengroup/propka)
- [PDB2PQR](https://github.com/Electrostatics/pdb2pqr)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=structure-preparation&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fstructure-preparation.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
