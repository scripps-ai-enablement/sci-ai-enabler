---
title: Adaptyv (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Immunology and Microbiology, Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-29
verification_note: "repo and skills/adaptyv dir resolve on K-Dense-AI/scientific-agent-skills; wet-lab submission half needs a gated Adaptyv API key (in-silico half runs unauthenticated)"
security: caution
security_on: 2026-07-29
security_note: "provenance matches supplier K-Dense-AI, MIT collection, but skill writes to a paid external wet-lab platform and handles an ADAPTYV_API_KEY — review submissions before approval"
summary: K-Dense skill that submits designed protein and antibody sequences to the Adaptyv cloud lab for wet-lab binding, expression, thermostability, and activity assays, with NetSolP/SoluProt/SolubleMPNN/ESM/ipTM/pSAE pre-screening.
---

# Adaptyv (Claude Skill)

Claude skill that closes the design–build–test loop for proteins and antibodies — pre-screens sequences in silico (solubility, expression, stability, interface, aggregation), then submits them to the Adaptyv cloud laboratory for wet-lab binding, expression, thermostability, and enzyme-activity assays.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) |
| **Availability** | GA — distributed via the K-Dense `scientific-agent-skills` collection. The Adaptyv platform itself is in alpha/beta and API access is request-gated by Adaptyv. |
| **Pricing** | Free / OSS (skill source). Adaptyv wet-lab assays are paid per-experiment via Adaptyv; pricing is quoted by Adaptyv on API onboarding. |
| **Capabilities** | Read/Write — local in-silico pre-screening, plus authenticated API calls that **submit experiments to a wet lab** (the skill writes to the Adaptyv platform on the user's behalf). |
| **Verified** | works · 2026-07-29 |
| **Security** | caution · 2026-07-29 — provenance matches K-Dense-AI, MIT collection, but skill writes to a paid external wet-lab platform and handles an API key |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/proteomics-protein-engineering/adaptyv-bio` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `adaptyv` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
  This installs the full K-Dense `scientific-skills` plugin, which bundles the `adaptyv` skill alongside ~170 sibling skills.
- **Claude Code / Claude Desktop** — manual clone (single-skill install):
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/adaptyv ~/.claude/skills/
  ```
  (Replace `~/.claude/skills/` with your user-level Claude skills directory if you've relocated it.) The skill uses `uv` to install its Python dependencies on first invocation; install `uv` first (`pipx install uv` or per the [uv install docs](https://docs.astral.sh/uv/getting-started/installation/)) so the skill can resolve its environment.
- **Authentication** — Adaptyv requires an API key. Email `[email protected]` to request access while the platform is in alpha/beta, then set:
  ```
  export ADAPTYV_API_KEY=<your-key>
  ```
  in the environment Claude Code (or Claude Desktop) launches the skill from.

## What it does

- **Submits and tracks wet-lab experiments** on the Adaptyv cloud platform via authenticated API calls:
  - **Binding assays** — biolayer interferometry for protein–target K_D / k_on / k_off
  - **Expression testing** — E. coli, mammalian, yeast, or insect cell systems
  - **Thermostability** — DSF and CD for T_m and stability profiling
  - **Enzyme activity** — kinetic parameters, substrate specificity, inhibitor screens
- **Pre-screens sequences in silico** before submission so users don't waste wet-lab cycles on candidates that will fail expression or solubility:
  - **NetSolP / SoluProt** — solubility prediction
  - **SolubleMPNN** — sequence redesign to improve expression
  - **ESM** — sequence-likelihood scoring
  - **ipTM (AlphaFold-Multimer)** — interface-stability estimate for designed binders
  - **pSAE** — aggregation-risk quantification
- Supports **batch submission** for library screening and **webhook callbacks** for experiment completion (Adaptyv turnaround is ~21 days).
- Returns kinetic parameters, confidence metrics, and raw assay data alongside the original sequence metadata so subsequent design iterations can be conditioned on real wet-lab feedback.

**Primary use cases**: antibody affinity maturation, therapeutic-protein developability assessment, enzyme engineering, AI-driven protein-design validation loops, library-scale expression screens, lead optimization with experimental ground truth.

## Notes

- **The skill writes to a wet lab.** Review submitted sequences and experiment configurations carefully before approval — each call spends Adaptyv credits and consumes platform-side wet-lab resources.
- **Adaptyv API is gated.** Access is alpha/beta as of 2026-06-02; without an issued API key the in-silico pre-screening half is still usable, but the submission tools will fail.
- **K-Dense skill path migration.** The canonical K-Dense `scientific-agent-skills` repo moved skill directories from `skills/<name>/` to `skills/<name>/` in v2.43.0 to match the Agent Skills CLI layout. The published marketplace repo (`K-Dense-AI/scientific-agent-skills`) still uses `skills/<name>/` paths at the time of verification; the manual-clone snippet above matches that layout. If the marketplace path migrates, update the `cp` source path accordingly.
- Pairs with the [AlphaFold (Claude Skill)](alphafold.html), [PDB (Claude Skill)](pdb.html), and [Glycoengineering (Claude Skill)](glycoengineering.html) entries for an antibody-design workflow that runs from sequence → structure → glycan profile → in-silico screen → wet-lab validation.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills) — canonical skill repository (170+ skills; Adaptyv at `skills/adaptyv/SKILL.md` post-v2.43.0 migration)
- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills) — Claude Code plugin marketplace publishing the `scientific-skills` plugin
- [`skills/adaptyv/reference/examples.md`](https://github.com/K-Dense-AI/claude-skills/blob/main/skills/adaptyv/reference/examples.md) — usage examples shipped with the skill
- [Adaptyv Bio](https://www.adaptyvbio.com/) — wet-lab platform documentation and API onboarding (`[email protected]`)
- [Playbooks: adaptyv skill](https://playbooks.com/skills/k-dense-ai/claude-skills/adaptyv) — third-party skill catalog mirror

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=adaptyv&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fadaptyv.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
