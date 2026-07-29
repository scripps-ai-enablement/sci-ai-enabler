---
title: AMR / Resistome Detection (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-11
verification: works
verified_on: 2026-07-29
security: cleared
security_on: 2026-07-29
security_note: "GPTomics/bioSkills MIT (GitHub API, pushed 2026-07-18), metagenomics/amr-detection SKILL.md confirmed via contents API; provenance matches, read-only local workflow, no credential requests"
summary: "Profile the antimicrobial-resistance gene content (resistome) of shotgun metagenomes with RGI, AMR++/MEGARes, deepARG, and AMRFinderPlus/ABRicate"
---

# AMR / Resistome Detection (bioSkills)

A Claude Code skill for detecting and quantifying antimicrobial-resistance genes in microbial communities from shotgun metagenomic reads, contigs, or MAGs.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-29 |
| **Security** | cleared · 2026-07-29 — GPTomics/bioSkills MIT, amr-detection SKILL.md confirmed, provenance matches, read-only local workflow |

## How to install

bioSkills is **not** an npm package — clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "metagenomics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `--list` to preview and `--dry-run` to see what would be copied.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/metagenomics/amr-detection ~/.claude/skills/
  ```
  (run from inside your clone; otherwise replace `bioSkills/` with the absolute path of your clone). Install the resistome tools referenced by the skill (`RGI`, `AMRFinderPlus`, `ABRicate`, etc., via bioconda) and their databases (CARD, MEGARes, ResFinder) when prompted on first use.

## What it does

Profiles the resistome — the antibiotic-resistance gene content of a community — via two complementary routes:

- **Read-based quantification** — `RGI bwt` (CARD homolog mapping), `AMR++`/`MEGARes` (gene-fraction-filtered profiling), `ARGs-OAP`/`SARG` (normalized to copies per 16S / per cell), `deepARG` (deep-learning detection of divergent ARGs), `GROOT` (variation-graph typing of SNP-bearing alleles).
- **Presence calling on assemblies** — `AMRFinderPlus` (curated per-gene thresholds) and `ABRicate` (rapid 80/80 contig screening) on contigs or MAGs.

The skill stresses a key caveat: an ARG hit is a sequence match, not a phenotype, and a metagenomic ARG has no host or genomic context until assembly — so breadth-of-coverage filtering is used to reject partial-domain false positives.

**Primary use cases**: community resistome quantification, ARG presence calling on contigs/MAGs, cross-sample ARG normalization, false-positive control.

## Notes

Distributed as a `SKILL.md` in the bioSkills collection — Claude executes the workflow locally via Bash rather than as an MCP server. Upstream front-matter name: `bio-metagenomics-amr-detection`. Reference databases (CARD, MEGARes, ResFinder) are separate downloads. This is the first Claude-installable AMR/resistome wrapper the catalog has surfaced (previously a tracked gap). Upstream directory: `metagenomics/amr-detection`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`metagenomics/amr-detection/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/metagenomics/amr-detection/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=amr-detection&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Famr-detection.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
