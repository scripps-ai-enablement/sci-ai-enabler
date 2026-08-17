---
title: Structural Alignment (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-08-15
verification: works
verified_on: 2026-08-17
reviewed_on: 2026-08-17
security: caution
security_on: 2026-08-17
security_note: "upstream GPTomics/bioSkills repo confirmed archived on GitHub 2026-08-15; MIT root license and skill directory still intact, no further upstream maintenance expected"
summary: "Superpose and score protein structures with Foldseek, TM-align, US-align, DALI or FoldMason when sequence identity is too low to align reliably"
---

# Structural Alignment (bioSkills)

A Claude Code skill for the case where sequence alignment has run out of signal: pick the right structural aligner, run it, and read TM-score, DALI Z-score, RMSD and lDDT against the cutoffs that actually mean something.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT). The aligners are installed separately and are individually free: Foldseek and FoldMason (GPL-3.0, Steinegger Lab), TM-align / US-align (Zhang Lab, free for academic use), open-source PyMOL. DALI is used as a web server or via DaliLite from the Holm lab |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |
| **Verified** | works · 2026-08-17 |
| **Security** | caution · 2026-08-17 — GPTomics/bioSkills is now archived upstream; MIT and skill dir confirmed unchanged |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "alignment"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/alignment/structural-alignment ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites — the aligners are CLI tools the skill drives, none are bundled.** All four are on bioconda (versions checked 2026-08-15, and each satisfies the skill's stated minimum):
  ```
  conda install -c conda-forge -c bioconda foldseek tmalign usalign foldmason
  ```
  `foldseek` 8.ef4e960 (skill wants 8+), `tmalign` 20240303 (20220412+), `usalign` 20241201 (20231222+), `foldmason` 2.7bd21ed (1+). Confirm with `foldseek version`, `TMalign` (prints usage), `USalign -h`, `foldmason version`.
- **Python side** — BioPython 1.83+ for `Bio.PDB.Superimposer`, plus open-source PyMOL 3.0+ if you want to render the superposition:
  ```
  pip install "biopython>=1.83"
  conda install -c conda-forge pymol-open-source
  ```
- **DALI** — not a conda package. It is reached through the [Dali server](http://ekhidna2.biocenter.helsinki.fi/dali/) (free, submit-and-wait) or the standalone DaliLite distribution from the Holm lab. Treat it as an external service: uploading an unpublished structure sends it off your machine.

## What it does

Routes a structure-comparison question to the tool that answers it, then interprets the score:

- **Database-scale search** — Foldseek's 3Di alphabet indexes backbone geometry as sequence, giving structural search at ~10³–10⁶ structures/second; Foldseek-Multimer extends this to complexes.
- **Pairwise superposition** — TM-align for single chains where the residue correspondence is unknown; US-align for multi-chain complexes, RNA and DNA (`-mm 1 -ter 0`); `Bio.PDB.Superimposer` (Kabsch/SVD) when the atom correspondence is already known and you just need the transform.
- **Flexible and distance-matrix methods** — FATCAT for alignments needing twists and chain breaks, CE for combinatorial extension, DALI for distance-matrix alignment and its Z-score.
- **Structural MSA** — FoldMason for multiple structure alignment at scale; T-Coffee Expresso / 3D-Coffee for hybrid sequence–structure alignment when only some members have structures.

**Score cutoffs the skill carries**: TM-score **> 0.5** = same fold, **> 0.8** = equivalent topology, **< 0.2** = random similarity — and for chains under **60 residues** a length-aware Gumbel p-value instead of the raw TM-score. DALI Z-score **> 20** definitely homologous, **8–19** probable, **2–8** candidate (confirm with TM-score), **< 2** not significant. RMSD **< 2 Å over > 100 residues** is a strong superposition, **< 1.5 Å** excellent. lDDT **> 0.6** for a correctly modelled residue.

**Primary use cases**: remote-homology detection below the sequence twilight zone, deciding whether two folds are the same, superposing predicted against experimental models, building a structural MSA.

## Notes

The skill's organising idea is a **sequence-identity ladder that tells you when to stop aligning sequences**: at **≥ 40%** identity ordinary sequence dynamic programming is sufficient; **25–40%** calls for sensitive sequence methods (MMseqs2, jackhmmer, HHsearch); **15–25%** for profile–profile methods, or Foldseek if structures exist; **below 15%** sequence alignment is noise and structural or protein-language-model aligners are required. The stated exception is families under strong structural or functional constraint, which can stay reliable down to roughly **12–15%** identity when confirmed by a profile–profile search.

The most consequential practical warning concerns predicted models: **mask residues with pLDDT < 70 before Foldseek indexing** — their backbone coordinates encode as effectively random 3Di letters and contaminate hits below about TM-score 0.4. Feeding a full-length AlphaFold model with long disordered tails into a structural search is the standard way to generate confident-looking nonsense.

Two boundaries worth keeping straight. RMSD is not a property of a structure pair — it depends on the superposition *and* the atom selection — so TM-score, which is length-normalised, is the comparable number; and `Bio.PDB.Superimposer` does **not** solve the correspondence problem, so it is the wrong tool the moment you do not already know which atom pairs with which.

Upstream skill front-matter name is `bio-alignment-structural`; upstream directory `alignment/structural-alignment`; `primary_tool` is Foldseek. Complements [Foldseek Structural Search](foldseek-structural-search.html) (the standalone Foldseek surface), [Protein MCP Server](protein-mcp-server.html) (TM-align/jFATCAT and Foldseek reachable as MCP tools rather than local CLIs), [Geometric Analysis](geometric-analysis.html) (RMSD, SASA and dihedrals on a single structure), [Structure Validation](structure-validation.html) (pLDDT and PAE interpretation before you index a model), and [Multiple Sequence Alignment](multiple-alignment.html) for the sequence-side step this skill takes over from.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`alignment/structural-alignment/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/alignment/structural-alignment/SKILL.md)
- [Foldseek (Steinegger Lab)](https://github.com/steineggerlab/foldseek)
- [FoldMason](https://github.com/steineggerlab/foldmason)
- [US-align / TM-align (Zhang Lab)](https://zhanggroup.org/US-align/)
- [Dali server (Holm lab)](http://ekhidna2.biocenter.helsinki.fi/dali/)
- [Zhang & Skolnick, *Nucleic Acids Res* 33:2302 (2005) — TM-align](https://doi.org/10.1093/nar/gki524)
- [Zhang et al., *Nat Methods* 19:1109 (2022) — US-align](https://doi.org/10.1038/s41592-022-01585-1)
- [Mariani et al., *Bioinformatics* 29:2722 (2013) — lDDT](https://doi.org/10.1093/bioinformatics/btt473)
- [`bioconda::foldseek`](https://anaconda.org/bioconda/foldseek)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=structural-alignment&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fstructural-alignment.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
