---
title: Blatant-Why (BY) Protein Design Agent
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: 001TMF
availability: Beta
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology]
last_verified: 2026-08-15
verification: works
verified_on: 2026-08-17
reviewed_on: 2026-08-17
security: caution
security_on: 2026-08-17
security_note: "001TMF/blatant-why confirmed not archived, MIT, provenance matches; ships optional TAMARIND_API_KEY/RUNPOD_API_KEY/ADAPTYV_API_TOKEN credentials to third-party compute and wet-lab services"
summary: Scaffolds a Claude Code antibody and nanobody design campaign — 19 skills, 13 slash commands, and 11 MCP servers wired to design models and cloud compute.
---

# Blatant-Why (BY) Protein Design Agent

A Claude Code project scaffold that turns an antibody, nanobody, or de novo binder design campaign into a guided workflow, bundling design models (BoltzGen, PXDesign, Protenix), structure and antibody databases, screening, and optional cloud or local GPU compute.

| | |
|---|---|
| **Type** | Claude Code Plugin (project scaffold: skills + slash commands + bundled MCP servers) |
| **Supplier** | [001TMF](https://github.com/001TMF/blatant-why) |
| **Availability** | Beta — npm `blatant-why` at v0.1.0-beta, published 2026-04-03 |
| **Pricing** | Free / OSS (MIT). Compute is optional and billed by third parties: Tamarind Bio free tier of 10 jobs/month, RunPod GPU pods ~$0.40–$2.50/hr, Adaptyv Bio lab work priced by the vendor. Local GPU mode costs nothing beyond your hardware. |
| **Capabilities** | Read/Write — writes campaign state and design outputs to the project directory, submits compute jobs, and can submit designs for wet-lab expression (gated) |
| **Verified** | works · 2026-08-17 |
| **Security** | caution · 2026-08-17 — MIT and provenance confirmed; optional external compute/lab credentials (Tamarind, RunPod, Adaptyv) |

## How to install

Prerequisites: Node.js 18+, Python 3.11+, [`uv`](https://docs.astral.sh/uv/), and Claude Code. Claude Code supplies its own authentication, so no separate Anthropic API key is needed.

- **Claude Code** — scaffold a campaign directory, then open Claude Code inside it:
  ```
  mkdir my-campaign && cd my-campaign
  npx blatant-why init
  claude
  ```
  `init` writes a `CLAUDE.md` orchestration file plus a `.claude/` directory containing the agents, skills, slash commands, and MCP server definitions. Everything is **project-scoped** — the skills and `/by:…` commands exist only inside this directory, so run `claude` from the campaign folder rather than from your home directory.
- **Optional compute and lab credentials** — set in the project's `.env` after `init`:
  ```
  TAMARIND_API_KEY=…    # cloud fallback, free tier 10 jobs/month
  RUNPOD_API_KEY=…      # HPC pods, ~$0.40–$2.50/hr
  ADAPTYV_API_TOKEN=…   # wet-lab submission
  ```
- **Optional local GPU mode** — requires an NVIDIA CUDA GPU and local checkouts of the model repositories, pointed at by `.env` variables `PROTEUS_FOLD_DIR`, `PROTEUS_PROT_DIR`, and `PROTEUS_AB_DIR`; the scaffold auto-detects installed tools and offers local compute when present. No API keys are needed in this mode.
- **Claude Desktop** / **Claude.ai** — not supported. The scaffold depends on Claude Code's project-level skills, slash commands, and MCP wiring.

There is no plugin marketplace for this project — `npx blatant-why init` is the only install path, and it is a scaffold rather than a `/plugin install`. Do not expect `/plugin marketplace add` to find it.

## What it does

- **19 skills** — model drivers (`boltzgen`, `protenix`, `pxdesign`) plus workflow skills for campaign management, research and database lookup, epitope analysis, hypothesis debate, scoring, screening, failure diagnosis, experiment results, causal reasoning, campaign optimization, knowledge persistence, session handling, display, and compute deployment.
- **13 slash commands** — including `/by:setup`, `/by:welcome`, `/by:plan-campaign`, `/by:load`, `/by:screen`, `/by:results`, `/by:watch`, `/by:status`, `/by:resume`, `/by:set-profile`, and `/by:approve-lab`.
- **11 bundled MCP servers** — `pdb`, `uniprot`, `sabdab` (antibody structures), `screening`, `tamarind` and `cloud` (compute), `adaptyv` (lab submission), `campaign`, `research`, `local_compute`, and `knowledge`.
- **Models it drives** — BoltzGen for antibody and nanobody binder design, PXDesign for de novo binder design, and Protenix for structure prediction and confidence filtering. Screening covers ipSAE scoring, liability scanning, developability, and diversity selection.
- **Campaign memory** — each campaign writes to a JSON knowledge store queried through the `knowledge` MCP server, so past strategies for a target class are retrievable in later sessions.

**Primary use cases**: nanobody and antibody binder campaigns against a named target, de novo miniprotein binder design, developability and liability screening of candidate sequences.

## Notes

The underlying design models are research artifacts and are out of scope for this catalog on their own ([BoltzGen](https://github.com/HannesStark/boltzgen), [PXDesign](https://github.com/bytedance/PXDesign), Protenix); this entry covers the installable Claude Code layer that orchestrates them. Check each model's own license before using outputs commercially — the MIT license here covers the scaffold, not the weights.

Wet-lab submission through Adaptyv Bio is described upstream as triple-gated and fronted by `/by:approve-lab`; treat it as a spend-and-materials commitment, not a dry run. See the separate [Adaptyv](adaptyv.html) entry for that service. Related catalogued components: [PDB](pdb.html), [UniProt](uniprot.html), and [Boltz](boltz.html).

Still pre-1.0 (v0.1.0-beta), so expect interface churn. The project is MIT-licensed with 104 stars as of 2026-08-15, and its default branch is `master`. Cloud compute sends target sequences to third-party providers (Tamarind, RunPod) — use local GPU mode if your targets are confidential.

## Sources

- [`001TMF/blatant-why`](https://github.com/001TMF/blatant-why)
- [`blatant-why` on npm](https://www.npmjs.com/package/blatant-why)
- [BoltzGen](https://github.com/HannesStark/boltzgen)
- [PXDesign](https://github.com/bytedance/PXDesign)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=blatant-why&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fblatant-why.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
