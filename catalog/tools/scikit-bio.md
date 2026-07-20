---
title: scikit-bio (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-20
verification_note: "repo and skills/scikit-bio dir resolve on K-Dense-AI/scientific-agent-skills; smoke clone failed on sandbox missing git (environmental, not tool)"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier K-Dense-AI, MIT repo wrapping BSD-3 scikit-bio, maintained (pushed 2026-07-15), no OSV advisories"
summary: Skill for microbiome ecology — reads BIOM/FASTA, computes alpha/beta diversity (UniFrac), PCoA, PERMANOVA, and builds phylogenetic trees.
---

# scikit-bio (Claude Skill)

Claude skill wrapping the scikit-bio library for community ecology and microbiome analysis — diversity metrics, ordination, statistical tests, and phylogenetics.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (wraps the BSD-3 scikit-bio library) |
| **Availability** | GA |
| **Pricing** | Free / OSS (BSD-3-Clause) |
| **Capabilities** | Read/Write — local computation on user-supplied sequence and community data |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches K-Dense-AI, MIT repo, maintained, no OSV advisories |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/genomics-bioinformatics/scikit-bio` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
Install via the Skills CLI (recommended): `npx skills add K-Dense-AI/scientific-agent-skills`, then enable the `scikit-bio` skill. Or clone the repo manually:

```
git clone https://github.com/K-Dense-AI/scientific-agent-skills
cp -r scientific-agent-skills/skills/scikit-bio ~/.claude/skills/
uv pip install scikit-bio
```

## What it does

Recipes covering:

- BIOM, FASTA, FASTQ, and GenBank I/O
- Alpha diversity: Shannon, Simpson, Faith's PD
- Beta diversity: Bray-Curtis, Jaccard, weighted / unweighted UniFrac
- Ordination: PCoA, RDA, CCA
- Statistics: PERMANOVA, ANOSIM, Mantel
- Phylogenetics: neighbor-joining, UPGMA

**Primary use cases**: 16S and shotgun microbiome diversity workflows, QIIME 2-style OTU/ASV analyses, community-ecology statistics.

## Notes

Pure-Python, runs locally; no auth or external services. Pairs cleanly with QIIME 2 outputs via BIOM.

## Sources

- [`skills/scikit-bio/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scikit-bio/SKILL.md)
- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=scikit-bio&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fscikit-bio.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
