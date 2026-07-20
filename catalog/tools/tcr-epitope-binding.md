---
title: TCR-Epitope Binding (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-18
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches GPTomics/bioSkills MIT, skill dir + SKILL.md confirmed via contents API, read-only local workflow"
summary: "Infer or annotate TCR antigen specificity via unsupervised clustering (tcrdist3, GLIPH2, clusTCR, GIANA) and database lookup (VDJdb, IEDB, McPAS-TCR), with honest caveats on supervised prediction"
---

# TCR-Epitope Binding (bioSkills)

A Claude Code skill that infers or annotates TCR antigen specificity through clustering and database lookup, with supervised predictors framed under explicit reliability caveats.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches GPTomics/bioSkills, MIT, no advisories |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "immunoinformatics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/immunoinformatics/tcr-epitope-binding ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). The skill declares its external dependencies (tcrdist3, GLIPH2, clusTCR, GIANA, ERGO-II, NetTCR, pMTnet) in `SKILL.md`; install them when prompted on first use.

## What it does

Assigns TCR antigen specificity through a two-tier approach:

- **Clustering & lookup (the defensible task)** — groups TCRs likely sharing specificity using distance-based methods (`tcrdist3`, `GLIPH2`, `clusTCR`, `GIANA`) and matches against curated databases (VDJdb, IEDB, McPAS-TCR) with confidence filtering, operating within single cohorts to avoid HLA and background confounds.
- **Caveated supervised prediction** — ranks candidates with `ERGO-II`, `NetTCR-2.x`, and `pMTnet`, under the explicit warning that "general TCR-epitope prediction for unseen epitopes essentially does not work" (training data dominated by immunodominant epitopes, absence of true negatives).

The skill is emphatic that clustering is the defensible discovery task while per-pair predictions on novel epitopes require wet-lab validation (e.g., tetramer assays) and should never substitute for functional experiments.

**Primary use cases**: TCR specificity annotation, antigen-specific clonotype discovery via clustering, ranking TCR-epitope candidates for validation.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally via Bash/Python rather than as an MCP server. The upstream skill front-matter name is `bio-immunoinformatics-tcr-epitope-binding`; if you invoke it as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/tcr-epitope-binding`. Complements the single-cell/bulk repertoire skills (`scirpy-analysis`, `mixcr-analysis`, `immcantation-analysis`). Several bundled predictors and databases require separate download/registration from their vendors. Upstream directory: `immunoinformatics/tcr-epitope-binding`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`immunoinformatics/tcr-epitope-binding/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/tcr-epitope-binding/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tcr-epitope-binding&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftcr-epitope-binding.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
