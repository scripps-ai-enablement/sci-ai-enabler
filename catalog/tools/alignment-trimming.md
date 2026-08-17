---
title: Alignment Trimming (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
last_verified: 2026-08-15
verification: works
verified_on: 2026-08-17
reviewed_on: 2026-08-17
security: caution
security_on: 2026-08-17
security_note: "upstream GPTomics/bioSkills repo confirmed archived on GitHub 2026-08-15; MIT root license and skill directory still intact, no further upstream maintenance expected"
summary: "Trim multiple sequence alignments with ClipKIT, trimAl, BMGE, Divvier or HMMcleaner, choosing the mode by downstream goal rather than by habit"
---

# Alignment Trimming (bioSkills)

A Claude Code skill for the step between alignment and inference: remove the columns that are noise without removing the signal, and check afterwards whether the trimming changed the answer.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT). The trimmers install separately and are all free: ClipKIT (MIT), trimAl (GPL-3.0), BMGE, Divvier, HMMcleaner (`Bio::MUST::Apps::HmmCleaner`, CPAN) |
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
  cp -r bioSkills/alignment/alignment-trimming ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites — the trimmers are CLI tools the skill drives, none are bundled.** Four of the five are on bioconda (versions checked 2026-08-15, each satisfying the skill's stated minimum):
  ```
  conda install -c conda-forge -c bioconda clipkit trimal bmge divvier
  ```
  `clipkit` 2.14.0 (skill wants 2.1+), `trimal` 1.5.1 (1.4+), `bmge` 1.12 (1.12+), `divvier` 1.01 (1.01). Verify with `clipkit --version`, `trimal --version`, `BMGE --help`, `Divvier --help`.
- **HMMcleaner** is a Perl distribution rather than a conda package — install the current CPAN release:
  ```
  cpanm Bio::MUST::Apps::HmmCleaner
  ```
  (**Unverified —** upstream names the CPAN release but gives no pinned version or install command; adapt if `cpanm` is unavailable on your system.)
- **Python side** — BioPython 1.83+ for reading the trimmed alignments back and keeping column indices:
  ```
  pip install "biopython>=1.83"
  ```

## What it does

Five stages, in order: characterise the dataset (divergence depth, gap structure) → pick the tool by *downstream goal* rather than by default → trim with mode-specific parameters → run a sensitivity analysis comparing tree topology and support before and after → keep the column index mapping so site-specific results can be traced back to the untrimmed alignment.

Working parameters the skill carries:

| Parameter | Value | Meaning |
|---|---|---|
| BMGE `-h` (entropy) | **0.5** default | Lower is more aggressive; **0.4** for deep phylogenomics, **0.6** for shallow datasets |
| BMGE `-g` (gap rate) | **0.2** | Gap-fraction threshold per column |
| BMGE `-b` (block size) | **5** | Minimum retained block length |
| trimAl `-gt` | set manually | Drop columns above the specified gap fraction |
| ClipKIT retention | **> 60%** | If a trimmer removes more than **40%** of columns, the mode is too aggressive |
| T-Coffee TCS | retain **≥ 5** | Column confidence on a 0–9 scale; 5–7 is the usable band |

Tool routing follows the destination: ClipKIT (the `primary_tool`) for phylogenetics where the goal is retaining parsimony-informative sites, trimAl for gap- and similarity-threshold trimming, BMGE for entropy-based trimming of deep phylogenomic matrices, Divvier for partitioned/divergence-aware filtering, HMMcleaner for removing individual mis-aligned sequence segments rather than whole columns.

**Primary use cases**: preparing a concatenated phylogenomic matrix, cleaning an alignment before HMM building, filtering before dN/dS or selection analysis.

## Notes

The rule that keeps this honest is the **> 60% retention check**: if trimming removes more than 40% of columns, the mode is wrong for the dataset, not the dataset wrong for the mode. Paired with the mandated sensitivity analysis — compare the tree topology and support values with and without trimming — it turns trimming from an unexamined default step into something with a reported effect. A phylogeny that only appears with aggressive trimming is a result about the trimmer.

The tools are not interchangeable in kind. Column-based trimmers (trimAl, BMGE, ClipKIT) delete positions across all sequences; HMMcleaner removes *segments within individual sequences*, which is the right instrument when one or two taxa carry annotation or assembly errors and column trimming would throw away good data from everyone else. Divvier likewise filters on alignment uncertainty rather than on gap counts.

Keeping the column index map is not optional if any downstream claim is site-specific — a positively selected site or a conserved catalytic residue reported at a trimmed-alignment coordinate is unreadable against the original sequence.

Upstream skill front-matter name is `bio-alignment-trimming`; upstream directory `alignment/alignment-trimming`; `primary_tool` is ClipKIT. Sits between [Multiple Sequence Alignment](multiple-alignment.html) and [MSA Statistics](msa-statistics.html), and feeds [Phylogenetics](phylogenetics.html). For RNA alignments, note that trimming interacts with structure annotation — see [Covariation Analysis](covariation-analysis.html), which needs the paired columns intact.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`alignment/alignment-trimming/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/alignment/alignment-trimming/SKILL.md)
- [ClipKIT](https://github.com/JLSteenwyk/ClipKIT)
- [trimAl](https://github.com/inab/trimal)
- [BMGE (bioconda)](https://anaconda.org/bioconda/bmge)
- [Divvier](https://github.com/simonwhelan/Divvier)
- [`Bio::MUST::Apps::HmmCleaner` (CPAN)](https://metacpan.org/pod/Bio::MUST::Apps::HmmCleaner)
- [`bioconda::clipkit`](https://anaconda.org/bioconda/clipkit)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=alignment-trimming&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Falignment-trimming.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
