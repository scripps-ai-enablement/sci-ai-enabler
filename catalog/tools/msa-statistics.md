---
title: MSA Statistics (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
last_verified: 2026-08-15
summary: "Compute percent identity, conservation scores, gap profiles and substitution-matrix statistics over a multiple alignment with BioPython, and read them correctly"
---

# MSA Statistics (bioSkills)

A Claude Code skill for measuring an alignment rather than eyeballing it — percent identity by an explicitly named definition, per-column conservation, gap profiles, and the substitution-matrix scores behind them.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT); BioPython is BSD-style, NumPy BSD-3-Clause |
| **Capabilities** | Read/Write — Claude runs the skill's Python workflow locally, not as an MCP tool |

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
  cp -r bioSkills/alignment/msa-statistics ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites — pure Python, no external CLI:**
  ```
  pip install "biopython>=1.83" "numpy>=1.26"
  ```
  Confirm with `pip show biopython numpy`. The skill imports `Bio.AlignIO`, `Bio.Align.substitution_matrices`, `collections.Counter`, `numpy` and `math`; `primary_tool` is `Bio.Align`.
- **Optional, only for the tree-based conservation route** — ConSurf / rate4site needs a phylogenetic tree as input and is not installed by the commands above. (**Unverified —** upstream names rate4site without an install path; see the ConSurf documentation.)

## What it does

- **Percent identity, with the denominator named** — four definitions that are not interchangeable: **PID1** over aligned positions including internal gaps (general screening), **PID2** over aligned residue pairs only (motif/domain detection), **PID3** over the shorter sequence's ungapped length (fragment comparison), **PID4** over the mean ungapped length (structural similarity; the skill's recommendation for orthologs).
- **Conservation scoring** — majority fraction and Shannon entropy for quick screening and DNA/RNA logos; Capra–Singh Jensen–Shannon divergence for catalytic-residue prediction (reported AUC ≈ **0.94**, Top-30 ≈ **0.75**); ConSurf/rate4site when the goal is mapping rates onto a PDB surface.
- **Information content** — uniform background for DNA (`IC = log₂(4) − H`), Kullback–Leibler divergence against Robinson & Robinson background frequencies for protein.
- **Gap profiles** — per-column gap fraction plus aggregate statistics (total gaps, gap-free column count, gappiest sequence and column).
- **Pairwise identity matrices** — the naive double loop is O(N² × L), fine for hundreds of sequences; vectorise with NumPy broadcasting for thousands, and switch to k-mer methods past ~10,000.

**Quality thresholds**: more than **50% gaps in more than 30% of columns** → drop outlier sequences and re-align; average protein pairwise identity **< 25%** → validate with GUIDANCE2 or move to structural alignment; conservation collapsing in a region expected to be functional → re-check homology with BLAST rather than trusting the alignment.

**Primary use cases**: quantifying how good an alignment actually is, ranking residues by conservation before mutagenesis, reporting a defensible identity figure in a manuscript.

## Notes

The single most useful fact on this page is that **"percent identity" is not one number**. The four denominators produce up to **11.5% variation** on the *same* alignment, and once different alignment algorithms are also in play the spread reaches **22%**. The worked example makes the trap concrete: 80 matches between a 500-residue protein and a 100-residue domain fragment gives PID2 ≈ **84%** but PID4 ≈ **27%** — both correct, answering different questions. Any reported identity that does not state its denominator is not reproducible.

A second reproducibility caveat applies to bit scores: tools calibrate the Karlin–Altschul lambda differently — NCBI BLAST tabulates **0.3176**, FASTA/SSEARCH recomputes per query, HMMER `phmmer` derives it by Forward calibration, and `Bio.Align` does not implement Karlin–Altschul at all — so expect roughly **2% bit-score variation** across tools on one alignment.

There is also a silent-failure API trap worth knowing before you write code against it: `substitution_matrices.load('BLOSUM62')` returns a NumPy-backed `Array` indexed by residue characters, **not a dict**. The correct accessor is `matrix[c1, c2]`; calling `.get((c1, c2), 0)` on it always returns **0** without raising, which produces plausible-looking all-zero scores. Non-standard residues such as `U` and `J` raise `IndexError` and must be skipped or scored zero explicitly.

Upstream skill front-matter name is `bio-alignment-msa-statistics`; upstream directory `alignment/msa-statistics`. Third step of the alignment chain, after [Multiple Sequence Alignment](multiple-alignment.html) and [Alignment Trimming](alignment-trimming.html); for RNA alignments the evolutionary test is [Covariation Analysis](covariation-analysis.html) rather than a conservation score, and below the identity floor use [Structural Alignment](structural-alignment.html). General sequence-object handling lives in [Biopython](biopython.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`alignment/msa-statistics/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/alignment/msa-statistics/SKILL.md)
- [BioPython `Bio.Align` documentation](https://biopython.org/docs/latest/api/Bio.Align.html)
- [Capra & Singh, *Bioinformatics* 23:1875 (2007) — JSD conservation](https://doi.org/10.1093/bioinformatics/btm270)
- [ConSurf](https://consurf.tau.ac.il/)
- [Raghava & Barton, *BMC Bioinformatics* 7:415 (2006) — percent-identity definitions](https://doi.org/10.1186/1471-2105-7-415)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=msa-statistics&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmsa-statistics.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
