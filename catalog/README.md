# Catalog

A curated catalog of installable Claude components for life-science applications — Claude Skills, MCP servers, Claude Code Plugins, and Claude.ai Connectors. Each entry must be a discrete unit a Claude.ai or Claude Code user can install or enable today.

Maintained by a scheduled Claude curator. See the top-level [README](../README.md) and [`AGENT.md`](../AGENT.md) for how this is produced, and [`CHANGELOG.md`](../CHANGELOG.md) for the history.

**New to Claude Skills, MCP servers, or Plugins?** Start with the [guide](../guide/) — short pages that explain what each component is and how to install it.

_Last refreshed: 2026-05-19_

## How this catalog is organized

- [`entries.md`](entries.md) holds the **full content for every entry** — one canonical block per tool. Browse it directly to scan everything, or jump to a specific tool by name.
- The seven category files below are **index views**. Each lists short cards for every entry tagged with that category, linking back to the canonical entry. Tools tagged `Categories: All` appear in every category index.

| Category | Index | Entries |
|---|---|---|
| Chemistry | [chemistry.md](chemistry.md) | 4 |
| Immunology and Microbiology | [immunology-microbiology.md](immunology-microbiology.md) | 7 |
| Integrative Structural and Computational Biology | [structural-computational-biology.md](structural-computational-biology.md) | 6 |
| Molecular and Cellular Biology | [molecular-cellular-biology.md](molecular-cellular-biology.md) | 7 |
| Neuroscience | [neuroscience.md](neuroscience.md) | 6 |
| Translational Medicine | [translational-medicine.md](translational-medicine.md) | 7 |
| Drug Repurposing and Discovery | [drug-repurposing-discovery.md](drug-repurposing-discovery.md) | 7 |

Distinct tools currently catalogued: **7**. Cross-cutting tools (PubMed Connector, BioMCP, BioRender Connector) use `Categories: All` and appear in every index; tools with a defined subset (10x Genomics Cloud MCP, single-cell-rna-qc, nextflow-development, instrument-data-to-allotrope) enumerate their categories explicitly.

## Entry schema

Each entry in `entries.md` includes a `Categories` tag list, type, supplier, availability, pricing, capabilities, install paths (`Available in`), tools/resources exposed, primary use cases, integration notes, sources, and verification timestamps. See [`AGENT.md`](../AGENT.md) for the canonical schema.
