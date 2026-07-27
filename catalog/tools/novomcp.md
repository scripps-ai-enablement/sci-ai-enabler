---
title: NovoMCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Quant NexusAI
availability: Preview
tool_categories: [Chemistry, Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-07-18
verification: degraded
verified_on: 2026-07-27
verification_note: "novomcp.com now points to a self-host repo NovoMCP/novomcp (pushed 2026-07-26) with a local localhost:8018/mcp endpoint, but its README launch command is not yet confirmed and the hosted FAVES tier stays application-gated, so still not functionally resolved this run"
security: unknown
security_on: 2026-07-27
security_note: "new NovoMCP/novomcp repo appeared but GitHub reports license NOASSERTION (site claims Apache-2.0) and it is 2-star day-old, so provenance/license not yet assessable"
summary: Hosted computational-chemistry engine MCP — ADMET, GFN2-xTB QM, GPU GROMACS MD, and AutoDock-GPU docking over a precomputed compound layer.
---

# NovoMCP

Hosted MCP server that gives Claude a computational-chemistry engine — molecular profiling and ADMET on a precomputed compound layer, plus GPU-backed quantum chemistry, molecular dynamics, and docking through a paid compute tier.

| | |
|---|---|
| **Type** | MCP server (remote, HTTP) |
| **Supplier** | [Quant NexusAI](https://www.novomcp.com/) |
| **Availability** | Preview — research-preview access; the platform describes an application process for full access |
| **Pricing** | Freemium — free tier (molecular profiling, ADMET, compliance screening); paid Core / Scale / Enterprise plans unlock **Novo Compute** (QM, MD, docking). Specific prices not published. |
| **Capabilities** | Read/Write — read-only property/ADMET lookups; compute tools launch GPU simulation jobs |
| **Verified** | degraded · 2026-07-27 — new self-host repo NovoMCP/novomcp appeared but launch not yet confirmed; hosted tier still gated |
| **Security** | unknown · 2026-07-27 — NovoMCP/novomcp license NOASSERTION vs Apache-2.0 claim, day-old 2-star, not yet assessable |

## How to install

An API key (format `nmcp_…`) from [app.novomcp.com](https://app.novomcp.com/) is required for authentication.

- **Claude Code** — direct MCP add (base engine, free-tier tools):
  ```
  claude mcp add --transport http novo https://ai.novomcp.com/mcp
  ```
- **Claude Code** — direct MCP add (Novo Compute, paid QM / MD / docking):
  ```
  claude mcp add --transport http novo-compute https://compute.novomcp.com/mcp
  ```
- **Claude Desktop** — **Settings → Connectors → Add custom connector**, URL `https://ai.novomcp.com/mcp` (or `https://compute.novomcp.com/mcp` for compute), then authenticate with your `nmcp_…` API key. Claude Desktop supports remote connectors natively for Pro/Max/Team/Enterprise accounts; on plans without native remote-connector support, use an `mcp-remote` proxy entry in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "novo": {
        "command": "npx",
        "args": ["mcp-remote", "https://ai.novomcp.com/mcp", "--header", "Authorization: Bearer nmcp_YOUR_KEY"]
      }
    }
  }
  ```
  (replace `nmcp_YOUR_KEY` with your API key from app.novomcp.com.)

## What it does

**Base engine (`ai.novomcp.com`, free tier)** — a precomputed molecular-intelligence layer over ~122M compounds:

- Molecular profiling and physicochemical property calculation.
- ADMET prediction via ~31 ML models spanning absorption, distribution, metabolism, excretion, and toxicity.
- Regulatory / compliance screening (FAVES assessment across multiple jurisdictions).
- Literature, patent, and clinical-trial search; target discovery from omics data.

**Novo Compute (`compute.novomcp.com`, paid)** — GPU / quantum simulation:

- Quantum chemistry via GFN2-xTB semi-empirical QM; conformer generation and strain-energy calculations.
- GPU molecular dynamics via GROMACS (e.g. protein–ligand binding stability over nanosecond timescales); a QM-to-force-field bridge (MCPB.py) for metalloprotein MD.
- GPU-accelerated molecular docking via AutoDock-GPU.
- Lead optimization via scaffold hopping; pharmacogenomic patient stratification.

**Primary use cases**: ADMET / property triage of candidate molecules, GPU MD of protein–ligand complexes, semi-empirical QM and docking without local HPC.

## Notes

Commercial, closed-source hosted service maintained by Quant NexusAI Inc.; no client-side source or license is published — treat it as a proprietary SaaS connector rather than an OSS tool. Access is gated: the marketing site describes a **research preview open to a small group of PIs, postdocs, and research engineers** with an application step, while the docs describe a self-serve free tier and paid compute plans — confirm your access path at app.novomcp.com before relying on it. The free tier covers profiling / ADMET / compliance; QM, MD, and docking require a paid Novo Compute plan and hit a separate `compute.novomcp.com` endpoint. Pricing figures for the paid tiers are not published — contact the vendor. The ADMET / property and literature-search surfaces overlap dedicated catalog entries (e.g. [pyTDC](pytdc.html), [PubMed](pubmed.html)); NovoMCP's distinct value is the bundled GPU QM / MD / docking behind one connector.

## Sources

- [NovoMCP](https://www.novomcp.com/)
- [NovoMCP docs — Novo](https://www.novomcp.com/docs/novo)
- [app.novomcp.com (API keys / access)](https://app.novomcp.com/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=novomcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fnovomcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
