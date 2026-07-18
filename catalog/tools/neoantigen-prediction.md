---
title: Neoantigen Prediction (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Translational Medicine]
last_verified: 2026-07-18
summary: "Identify tumor neoantigens from somatic variants with pVACtools for personalized cancer vaccines and checkpoint biomarkers, centering clonality, HLA LOH, expression, and validation tiers"
---

# Neoantigen Prediction (bioSkills)

A Claude Code skill that builds a tumor-to-candidate neoantigen pipeline with pVACtools, emphasizing that binding prediction is the easy part and true positives live downstream.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |

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
  cp -r bioSkills/immunoinformatics/neoantigen-prediction ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). The skill declares its external dependencies (pVACtools, VEP, HLA typers, LOHHLA) in `SKILL.md`; install them when prompted on first use.

## What it does

Runs the full personalized-neoantigen discovery workflow with the **pVACtools** suite while enforcing the field's downstream filters:

- **pVACseq** — translates somatic SNVs/indels into mutant peptides via VEP annotation (Wildtype + Frameshift plugins).
- **pVACfuse** — handles fusion-junction neoantigens.
- **pVACbind** — scores arbitrary peptides without a wild-type comparison.
- **pVACview** — manual re-tiering and candidate selection.
- **Critical filters** — HLA loss-of-heterozygosity (LOHHLA, the silent invalidator), clonal cancer cell fraction (CCF), agretopicity/foreignness quality, and expression thresholds.

The skill centers the predicted → presented → immunogenic validation tiers, stressing that most confidently-predicted strong binders are never presented, and most presented peptides never elicit a T-cell response.

**Primary use cases**: cancer vaccine target nomination, neoantigen ranking, checkpoint-response biomarker discovery.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally via Bash/Python rather than as an MCP server. The upstream skill front-matter name is `bio-immunoinformatics-neoantigen-prediction`; if you invoke it as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/neoantigen-prediction`. Binding-affinity detail is delegated to the `mhc-binding-prediction` skill and ranking to `immunogenicity-scoring`. pVACtools and its dependencies (VEP, HLA typers) require separate installation. Upstream directory: `immunoinformatics/neoantigen-prediction`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`immunoinformatics/neoantigen-prediction/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/neoantigen-prediction/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=neoantigen-prediction&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fneoantigen-prediction.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
