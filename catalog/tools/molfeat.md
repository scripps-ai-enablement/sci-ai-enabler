---
title: Molfeat (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-20
verification_note: "repo and skills/molfeat dir resolve on K-Dense-AI/scientific-agent-skills; smoke clone failed on sandbox missing git (environmental, not tool)"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier K-Dense-AI, MIT repo wrapping Apache-2.0 Molfeat, maintained (pushed 2026-07-15), no OSV advisories"
summary: Claude skill wrapping Molfeat — a unified API over 100+ molecular featurizers spanning classical fingerprints, descriptors, and pre-trained chemical foundation-model embeddings.
---

# Molfeat (Claude Skill)

Claude skill providing Python recipes for [Molfeat](https://molfeat.datamol.io/), a featurizer hub that unifies 100+ molecular representations — ECFP / MACCS / RDKit fingerprints, 2D/3D descriptors, molecular graphs, and pretrained embeddings (ChemBERTa, MolBERT, Uni-Mol) — behind a single scikit-learn-compatible transformer API.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS skill (MIT collection); Molfeat itself is Apache-2.0 |
| **Capabilities** | Read/Write — Claude executes Molfeat via the Bash/Python tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches K-Dense-AI, MIT repo, maintained, no OSV advisories |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/structural-biology-drug-discovery/molfeat-molecular-featurization` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `molfeat` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/molfeat ~/.claude/skills/
  pip install molfeat
  ```

Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- Classical fingerprints — ECFP / Morgan, MACCS, RDKit, pharmacophore
- 2D/3D descriptors — constitutional, topological, electronic
- Graph-based representations — molecular graphs, line graphs
- Pre-trained embeddings — ChemBERTa, MolBERT, Uni-Mol via the Molfeat hub
- Unified transformer API for `fit` / `transform` use in scikit-learn / PyTorch pipelines
- Caching and parallel processing for virtual-screening-scale compound sets

**Primary use cases**: Featurization for QSAR / property-prediction models, virtual screening, molecular similarity search, preparing input tensors for deep-learning chemistry models.

## Notes

Skill is documentation plus Python recipes — Claude executes Molfeat locally via Bash/Python. Pairs naturally with the catalog's `rdkit-skill` and `datamol` pages for end-to-end lead-optimisation pipelines. Pretrained-model featurizers may download weights on first use; expect a one-off network hop.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/molfeat/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/molfeat/SKILL.md)
- [Molfeat documentation — molfeat.datamol.io](https://molfeat.datamol.io/)
- [`datamol-io/molfeat`](https://github.com/datamol-io/molfeat)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=molfeat&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmolfeat.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
