---
title: ncRNA Search (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Find non-coding RNA homologs and assign Rfam families with Infernal covariance models, scoring sequence and secondary structure together"
verification: works
verified_on: 2026-08-13
reviewed_on: 2026-08-13
security: cleared
security_on: 2026-08-13
security_note: "GPTomics/bioSkills root LICENSE confirmed MIT this run, not archived, 1.2k stars, no external credentials"
---

# ncRNA Search (bioSkills)

A Claude Code skill that runs Infernal covariance-model searches against Rfam properly — clan de-overlapping, curated bit-score cutoffs, and the E-value-depends-on-database-size trap handled rather than ignored.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — Infernal (BSD) and the Rfam database (CC0) are downloaded separately |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |
| **Verified** | works · 2026-08-13 |
| **Security** | cleared · 2026-08-13 — GPTomics/bioSkills MIT, no external credentials |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "rna-structure"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/rna-structure/ncrna-search ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites** — Infernal 1.1.4+ plus the Python helpers the skill's examples use:
  ```
  conda install -c conda-forge -c bioconda infernal
  pip install "biopython>=1.83" "pandas>=2.2"
  ```
  bioconda ships `infernal` 1.1.5 (checked 2026-08-08). Confirm with `cmscan -h`.
- **Rfam database** — download and index it once (this is the skill's own documented setup step):
  ```
  wget https://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/Rfam.cm.gz && gunzip Rfam.cm.gz
  wget https://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/Rfam.clanin
  cmpress Rfam.cm
  ```
  `Rfam.cm` ships **pre-calibrated** — run `cmpress` on it, and do **not** run `cmcalibrate`.

## What it does

- **Search** — `cmscan` for one sequence against the whole CM database, `cmsearch` for one covariance model against a sequence database; both score sequence *and* consensus secondary structure jointly, which is what a covariance model buys over an HMM.
- **De-overlap** — resolves the redundant hits Rfam clans produce, using `--fmt 2 --clanin Rfam.clanin` and filtering the marked lines (`grep -v ' = '`).
- **Threshold choice** — explains the three curated per-family cutoffs and when each applies: **GA** (gathering, the curated membership threshold and the default choice for Rfam), **TC** (trusted cutoff, the lowest known true-positive score, most conservative), **NC** (noise cutoff, the highest false-positive score, most permissive).
- **Structure recovery** — `cmalign` to fold hits back against the model and recover the consensus secondary structure, which is the handoff into covariation testing or restrained folding.
- **Custom models** — `cmbuild` → `cmcalibrate` → `cmpress` for a family not in Rfam, plus `cmfetch` to pull individual models out of the flatfile.
- **Specialized alternatives** the skill routes to when a general CM search is the wrong tool: tRNAscan-SE 2.0 (tRNAs), barrnap and RNAmmer (rRNA), snoscan and snoReport 2.0 (snoRNAs), miRDeep2 (miRNAs).

**Primary use cases**: annotating structured ncRNAs in a new genome or contig set, assigning an unknown transcript to an Rfam family, recovering a consensus fold for a set of homologs.

## Notes

The skill leads with a scoping rule that saves wasted runtime: a **covariance model offers no advantage when there is little conserved secondary structure to exploit**, and a CM built from a structure-free alignment (no real `#=GC SS_cons` pairs) collapses to an HMM — all the cost, none of the benefit. Long lncRNAs are the usual case where this bites.

Two reporting rules follow. First, a CM **E-value scales linearly with the searched database size** (`Z`), so the same hit gets a different E-value depending on what you searched; for reproducibility use `--cut_ga` or pin `-Z <Mb>` explicitly, and prefer bit scores (database-size independent) when working with a custom uncalibrated model. Second, a significant hit means the locus has sequence plus structure consistent with the family — it does **not** establish that the RNA is expressed, processed, or functional.

Upstream skill front-matter name is `bio-rna-structure-ncrna-search`; upstream directory `rna-structure/ncrna-search`. The natural next step after a hit is [Covariation Analysis](covariation-analysis.html) to test whether the recovered structure has evolutionary support, or [ViennaRNA](viennarna-structure-prediction.html) for thermodynamic folding of individual hits; [Rfam](rfam.html) is the same database as a hosted Claude connector if you want interactive family lookups without a local download, and [RNA Structure Probing](structure-probing.html) supplies the experimental complement.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`rna-structure/ncrna-search/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/rna-structure/ncrna-search/SKILL.md)
- [Infernal 1.1 documentation](http://eddylab.org/infernal/)
- [Nawrocki & Eddy, *Bioinformatics* 29:2933–2935 (2013)](https://doi.org/10.1093/bioinformatics/btt509)
- [Rfam CURRENT release downloads](https://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/)
- [`bioconda::infernal`](https://anaconda.org/bioconda/infernal)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=ncrna-search&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fncrna-search.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
