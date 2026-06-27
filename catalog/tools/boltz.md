---
title: Boltz (Claude Code Plugin)
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Boltz
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology]
last_verified: 2026-06-27
summary: Skills that drive the hosted Boltz API to predict biomolecular structures, screen and design small molecules, and design protein/antibody binders.
---

# Boltz (Claude Code Plugin)

Plugin of agent skills that let Claude run Boltz biomolecular workflows — 3D structure and binding prediction, small-molecule and protein/antibody screening, and de novo binder design — by submitting jobs to the hosted Boltz API.

| | |
|---|---|
| **Type** | Claude Code Plugin (skills) — also a Claude Desktop `.mcpb` extension |
| **Supplier** | [Boltz](https://boltz.bio/) (`boltz-bio/boltz-api-skills`) |
| **Availability** | GA — listed in `anthropics/claude-plugins-official` |
| **Pricing** | Usage-based — Boltz API account required; agent shows a cost estimate before submitting each job (per-job pricing not published) |
| **Capabilities** | Read/Write — submits compute jobs to the Boltz API and retrieves results |

## How to install

- **Claude Code** — official marketplace:
  ```
  /plugin install boltz@claude-plugins-official
  ```
  (the `claude-plugins-official` marketplace is available by default; if not found, run `/plugin marketplace add anthropics/claude-plugins-official` first)
- **Claude Code** — upstream marketplace (alternative):
  ```
  claude plugin marketplace add boltz-bio/boltz-api-skills
  claude plugin install boltz@boltz-marketplace --scope user
  ```
- **Claude Desktop** — download the latest `.mcpb` bundle from the project's [Releases](https://github.com/boltz-bio/boltz-api-skills/releases) and install via **Settings → Extensions → Advanced settings → Install Extension**.
- **Install the `boltz-api` CLI** (the skills call it; required on macOS/Linux):
  ```
  curl -fsSL https://install.boltz.bio/boltz-api/install.sh | sh
  ```
  Windows PowerShell: `irm https://install.boltz.bio/boltz-api/install.ps1 | iex`
- **Authenticate** the CLI before running any skill (one-time):
  ```
  boltz-api auth login --device-code
  ```
  or set `export BOLTZ_API_KEY="<your-api-key>"` in the shell that launches Claude Code.

## What it does

Eight skills wrap the `boltz-api` CLI (they orchestrate job submission and result retrieval — the computation runs server-side):

- **`boltz-cli-setup`** — CLI installation and authentication.
- **`boltz-structure-and-binding`** — 3D structure prediction with optional binding-affinity scoring.
- **`boltz-small-molecule-screen`** — rank a SMILES library against a target.
- **`boltz-small-molecule-design`** — generate novel small-molecule binders.
- **`boltz-small-molecule-adme`** — estimate ADME properties.
- **`boltz-protein-screen`** — rank proteins, peptides, and antibodies.
- **`boltz-protein-design`** — generate novel peptide/protein binders.
- **`boltz-check-status`** — monitor jobs and recover results.

**Primary use cases**: target structure prediction, virtual screening, de novo binder/antibody design, early-stage hit-to-lead triage.

## Notes

The Boltz model weights themselves are a separate research artifact (out of scope as a catalog entry); this plugin is in scope because it is an installable Claude component that calls the hosted Boltz API rather than running weights locally — no GPU is required on the user's machine. Jobs incur API usage cost; the agent surfaces a cost estimate before submitting. Anthropic lists the plugin in the official marketplace but does not control or guarantee third-party plugin behavior. Outputs are for research use; validate predictions experimentally.

## Sources

- [`boltz-bio/boltz-api-skills`](https://github.com/boltz-bio/boltz-api-skills)
- [`anthropics/claude-plugins-official` marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json)
- [Boltz](https://boltz.bio/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=boltz&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fboltz.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
