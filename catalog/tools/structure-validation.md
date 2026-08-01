---
title: Structure Validation (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-08-01
summary: "Decide whether a structure or region is reliable enough to build on — resolution, R-free gap, B-factors, MolProbity geometry, and pLDDT/PAE for predicted models"
---

# Structure Validation (bioSkills)

A Claude Code skill that judges whether a macromolecular model — or one specific region of it — is trustworthy enough to dock against, measure, or reason about mechanistically.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — Biopython, Phenix/MolProbity and DSSP are separately installed (Phenix is free for academic use under its own licence) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |

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
  cp -r bioSkills/structural-biology/structure-validation ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone).

## What it does

Separates *global* model quality from *local, per-region* reliability, which is the distinction that actually determines whether a measurement is safe:

- **Experimental metadata** — pulls resolution, R-work, R-free and the experimental method from the mmCIF header (`MMCIF2Dict`), and reads the R-free-minus-R-work gap as an overfitting signal rather than looking at R-work alone.
- **B-factor screening** — flags high-B residues using within-structure statistics (median / MAD z-scoring) instead of an absolute cutoff, because B-factors are only comparable inside one structure.
- **Geometry outliers** — clashscore, Ramachandran and rotamer outliers, and cis non-proline peptides; coarse checks run in Bio.PDB, with `phenix.molprobity` as the authoritative validator.
- **Predicted models** — validates AlphaFold/ESMFold output through pLDDT confidence bands and PAE before docking or molecular replacement, and can trim low-confidence regions and split PAE domains with `phenix.process_predicted_model`.
- **Method-specific reading** — cryo-EM global vs local resolution (FSC 0.143 half-map vs 0.5 map-model) and NMR ensemble spread as a disorder signal.
- **Components** — Bio.PDB (primary), `phenix.molprobity` and `phenix.process_predicted_model` (CLI), DSSP/`mkdssp`, NumPy.

**Primary use cases**: pre-docking receptor triage, deciding whether a specific loop or side chain supports a mechanistic claim, vetting a predicted model before downstream use.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-structural-biology-structure-validation`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/structure-validation`. MolProbity-grade validation requires a local Phenix installation; without it the skill falls back to the Bio.PDB coarse geometry checks and says so. Natural upstream of the catalogued [Structure Preparation](structure-preparation.html) skill and of docking entries such as [AutoDock Vina](autodock-vina-docking.html) and [smina](smina-molecular-docking.html); pairs with [AlphaFold MCP Server](alphafold.html) for the predicted-model case. Upstream directory: `structural-biology/structure-validation`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`structural-biology/structure-validation/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/structure-validation/SKILL.md)
- [MolProbity / Phenix validation](https://phenix-online.org/documentation/reference/validation_summary.html)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=structure-validation&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fstructure-validation.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
