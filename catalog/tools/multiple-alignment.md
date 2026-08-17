---
title: Multiple Sequence Alignment (bioSkills)
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
summary: "Build multiple sequence alignments with MAFFT, MUSCLE5, Clustal Omega or T-Coffee, choosing the algorithm by dataset size and divergence"
---

# Multiple Sequence Alignment (bioSkills)

A Claude Code skill that picks the alignment algorithm from the two facts that determine it — how many sequences and how diverged — instead of running the same default on every dataset.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT). The aligners install separately and are all free/OSS: MAFFT (BSD), MUSCLE5 (GPL-3.0), Clustal Omega (GPL-2.0), T-Coffee (GPL-3.0) |
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
  cp -r bioSkills/alignment/multiple-alignment ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites — the aligners are CLI tools the skill drives, none are bundled.** All are on bioconda (versions checked 2026-08-15, each satisfying the skill's stated minimum):
  ```
  conda install -c conda-forge -c bioconda mafft muscle clustalo t-coffee
  ```
  `mafft` 7.525 (skill wants 7.520+), `muscle` 5.3 (5.1+), `clustalo` 1.2.4 (1.2.4+), `t-coffee` 13.46.0 (13+). Confirm with `mafft --version`, `muscle -version`, `clustalo --version`, `t_coffee -version`.
- **Codon-alignment extras**, only if you are heading for dN/dS:
  ```
  conda install -c conda-forge -c bioconda pal2nal prank macse
  ```
  (**Unverified —** bioconda versions for these three were not checked on this pass; run `conda search` before relying on them.)
- **Python side** — BioPython 1.83+:
  ```
  pip install "biopython>=1.83"
  ```
  Note the API change the skill flags: **`Bio.Align.Applications` was removed in BioPython 1.86**, so wrapper classes no longer exist and the aligners must be invoked with `subprocess` directly.

## What it does

- **Algorithm selection by size** — reproduces MAFFT's `--auto` decision boundaries explicitly so you can see which branch you are on: **< 200** sequences → L-INS-i (local pairwise iterative, the accuracy option); **200–500** → FFT-NS-i truncated to `--maxiterate 2`; **500–2,000** → FFT-NS-2 progressive; **2,000–50,000** → single-pass FFT-NS-2; **> 50,000** → PartTree.
- **Tool capacity** — MAFFT L-INS-i tops out around **200** sequences at highest accuracy; MUSCLE5 PPP (`-align`) handles about **1,000** at highest accuracy; MUSCLE5 `-super5` scales past **100,000**; Clustal Omega has a published benchmark at **190,000**.
- **Confidence assessment** — per-column reliability with GUIDANCE2 or T-Coffee TCS *before* anything downstream consumes the alignment, then masking rather than silent acceptance.
- **Codon-aware alignment** — protein-first with MAFFT then threading nucleotides back with PAL2NAL for clean orthologs; PRANK `+F` codon for indel-rich paralogs; MACSE v2 where frameshifts or pseudogenes are present; HyPhy's `pre-msa.bf` / `post-msa.bf` for BUSTED/MEME-grade input.
- **Six-stage workflow** — homology check (BLAST E-value **< 1e-5**, drop non-homologous sequences) → algorithm selection → alignment → confidence scoring → low-confidence masking → downstream analysis.

**Primary use cases**: building a defensible alignment for phylogenetics or selection analysis, choosing between MAFFT modes on a large family, preparing codon alignments for dN/dS.

## Notes

The load-bearing threshold is the **twilight zone**, stated as a table: above **40%** protein identity any MSA tool will do; **25–40%** requires iterative methods with GUIDANCE2 validation; **20–25%** calls for profile–profile methods; and below **15–20%** the sequence signal is dominated by noise and the correct move is to switch to structural alignment altogether. That last row is the one most often ignored — a low-identity alignment is not merely imprecise, it is a different alignment on every rerun.

The sharpest warning concerns codon work: standard nucleotide MSA tools break reading frames and produce **systematically incorrect dN/dS estimates and false-positive selection signals even on clean simulated data** (Fletcher & Yang 2010). If the destination is PAML or HyPhy, a nucleotide-level MAFFT run is not an acceptable input, which is why the skill routes through protein alignment plus PAL2NAL, PRANK codon mode, or MACSE.

Upstream skill front-matter name is `bio-alignment-multiple`; upstream directory `alignment/multiple-alignment`; `primary_tool` is MAFFT. This is the first step of a four-part chain: build here, then [Alignment Trimming](alignment-trimming.html), then [MSA Statistics](msa-statistics.html), with [Structural Alignment](structural-alignment.html) taking over below the identity floor. Trees are built in [Phylogenetics](phylogenetics.html) (which bundles its own MAFFT + IQ-TREE 2 path for the simple case), covariation testing of RNA alignments in [Covariation Analysis](covariation-analysis.html), and profile-HMM/covariance-model search in [ncRNA Search](ncrna-search.html) and [BLAST](blast.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`alignment/multiple-alignment/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/alignment/multiple-alignment/SKILL.md)
- [MAFFT](https://mafft.cbrc.jp/alignment/software/)
- [MUSCLE v5](https://drive5.com/muscle/)
- [Clustal Omega](http://www.clustal.org/omega/)
- [T-Coffee](https://tcoffee.org/)
- [PAL2NAL](https://www.bork.embl.de/pal2nal/)
- [Fletcher & Yang, *Mol Biol Evol* 27:2257 (2010)](https://doi.org/10.1093/molbev/msq115)
- [`bioconda::mafft`](https://anaconda.org/bioconda/mafft)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=multiple-alignment&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmultiple-alignment.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
