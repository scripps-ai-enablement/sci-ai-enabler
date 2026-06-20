---
title: CovaSyn Chemistry MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: CovaSyn
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-06-20
summary: Hosted deterministic cheminformatics MCP with 130+ tools spanning ADMET, docking, retrosynthesis, ICH M7 toxicology, NMR/MS, and biologics design.
---

# CovaSyn Chemistry MCP

Hosted MCP server that gives Claude a broad, deterministic drug-discovery toolbox — cheminformatics, ADMET, retrosynthesis, docking, and regulatory toxicology — over a single API.

| | |
|---|---|
| **Type** | MCP server (hosted, streamable-HTTP) |
| **Supplier** | [CovaSyn](https://github.com/oliverkraft93-ops/covasyn-mcp-examples) |
| **Availability** | GA — registry version 1.27.2, last updated 2026-06-02 |
| **Pricing** | Freemium — free tier 100 credits/week; Pro €250/mo; Unlimited €750/mo; Enterprise (contact, GxP validation) |
| **Capabilities** | Read/Write — molecular computation and analysis; no persistent state |

## How to install

An API key is required. Create a free account at [covasyn.com](https://covasyn.com/en/pricing) to obtain `COVASYN_API_KEY`.

- **Claude Code** — direct MCP add (remote streamable-HTTP):
  ```
  claude mcp add --transport http covasyn https://mcp.covasyn.com/mcp --header "Authorization: Bearer YOUR_COVASYN_API_KEY"
  ```
  (replace `YOUR_COVASYN_API_KEY` with the key from your CovaSyn account. **Unverified —** the upstream repo documents the `@covasyn/mcp-client` stdio proxy below rather than a header-auth HTTP form; if the remote endpoint rejects the header, use the Desktop/stdio proxy entry instead.)
- **Claude Desktop** — stdio via the published npm proxy client, in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "covasyn": {
        "command": "npx",
        "args": ["-y", "@covasyn/mcp-client"],
        "env": {
          "COVASYN_API_KEY": "your_api_key_here",
          "COVASYN_API_BASE": "https://api.covasyn.com"
        }
      }
    }
  }
  ```
- **Claude Code** — equivalent stdio proxy (mirror of the Desktop entry):
  ```
  claude mcp add --transport stdio covasyn --env COVASYN_API_KEY=your_api_key_here --env COVASYN_API_BASE=https://api.covasyn.com -- npx -y @covasyn/mcp-client
  ```

The hosted endpoint is a long-lived remote service maintained by CovaSyn — there is nothing to keep running locally; the `npx` proxy launches on demand via stdio when Claude starts.

## What it does

Exposes 130+ deterministic tools grouped into suites, including:

- **covabasic** — core cheminformatics: canonicalization, fingerprints, druglikeness
- **covachem** — ADME, pKa, chemical profiling
- **covatox** — toxicology with ICH M7 assessment and CYP450 analysis
- **covams** / **covanmr** — mass-spectrometry and 1D/2D/batch NMR analysis
- **covafold** — protein and RNA folding
- **covabio** — antibody, peptide, ADC, and biologics tools
- **covaplatform** — stability, design of experiments, docking, chromatography, retrosynthesis

**Primary use cases**: ADMET profiling, molecular docking, retrosynthetic analysis, ICH M7 regulatory toxicology, lipid-nanoparticle and biologics design.

## Notes

Streamable-HTTP transport; EU-hosted (Hetzner Leipzig) by default with US hosting available. API key required; usage is metered in credits against the chosen plan. The example client snippets in the repo are MIT-licensed, but the CovaSyn service itself is commercial. Covers two open catalog gaps (a Claude-installable retrosynthesis and an ADMET tool) in a single hosted server.

## Sources

- [`oliverkraft93-ops/covasyn-mcp-examples`](https://github.com/oliverkraft93-ops/covasyn-mcp-examples)
- [MCP Registry — `com.covasyn/chemistry`](https://registry.modelcontextprotocol.io/)
- [CovaSyn](https://covasyn.com/en)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=covasyn&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcovasyn.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
