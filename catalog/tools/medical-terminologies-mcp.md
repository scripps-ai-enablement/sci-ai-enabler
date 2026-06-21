---
title: Medical Terminologies MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Sidney Bissoli
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-06-21
summary: MIT-licensed MCP server giving Claude unified lookup and cross-mapping across ICD-11, SNOMED CT, LOINC, RxNorm, MeSH, and ATC.
---

# Medical Terminologies MCP

Community MCP server that exposes the major global medical terminologies — ICD-11, SNOMED CT, LOINC, RxNorm, MeSH, and ATC — through one install, with cross-terminology search and mapping.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Sidney Bissoli](https://github.com/SidneyBissoli/medical-terminologies-mcp) (open source) |
| **Availability** | GA — published to npm as `medical-terminologies-mcp` |
| **Pricing** | Free / OSS (MIT). WHO ICD-11 API credentials required for ICD-11 tools; SNOMED CT needs an IHTSDO/SNOMED International license for production use |
| **Capabilities** | Read-only — terminology lookup, hierarchy traversal, and cross-mapping |

## How to install

This server runs over stdio, so Claude Code / Claude Desktop launch the process themselves — there is no long-lived service to keep running. For ICD-11 tools, register first for free WHO ICD API credentials at [icd.who.int/icdapi](https://icd.who.int/icdapi); the LOINC, RxNorm, MeSH, and ATC tools need no auth.

- **Claude Code** — register the npm package directly (`npx` fetches it; replace the WHO placeholders with your credentials):

  ```
  claude mcp add-json medical-terminologies '{"command":"npx","args":["-y","medical-terminologies-mcp"],"env":{"WHO_CLIENT_ID":"your-who-client-id","WHO_CLIENT_SECRET":"your-who-client-secret"}}'
  ```

- **Claude Desktop** — add to `claude_desktop_config.json`:

  ```json
  {
    "mcpServers": {
      "medical-terminologies": {
        "command": "npx",
        "args": ["-y", "medical-terminologies-mcp"],
        "env": {
          "WHO_CLIENT_ID": "your-who-client-id",
          "WHO_CLIENT_SECRET": "your-who-client-secret"
        }
      }
    }
  }
  ```

  Restart Claude Desktop after editing the config.

## What it does

Exposes 31 tools by default (37 with SNOMED CT enabled) across the terminologies:

- **ICD-11** — search, lookup, hierarchy, chapters, post-coordination.
- **LOINC** — search, details, answers, panels.
- **RxNorm** — search, concept, ingredients, drug classes, NDC.
- **MeSH** — search, descriptor, tree, qualifiers.
- **SNOMED CT** (optional) — search, concept, hierarchy, descriptions, ECL expression queries.
- **ATC** — classify, lookup, members.

Includes built-in caching, rate limiting, and cross-terminology search/mapping.

**Primary use cases**: Map clinical terms across coding systems, resolve drug/lab/diagnosis codes, build terminology-validation steps for clinical documentation and trial-eligibility workflows.

## Notes

Complements the single-terminology Anthropic [`icd-10-codes`](icd-10-codes.html) connector: this server is broader (ICD-11 rather than ICD-10-CM/PCS, plus SNOMED/LOINC/RxNorm/MeSH/ATC) but is community-maintained and read-only. SNOMED CT content is reference-only unless you hold an IHTSDO license; RxNorm, LOINC, MeSH, and ATC are freely usable. Also installable via Smithery (`npx -y smithery mcp add sidneybissoli/medical-terminologies-mcp`). stdio transport.

## Sources

- [`SidneyBissoli/medical-terminologies-mcp`](https://github.com/SidneyBissoli/medical-terminologies-mcp)
- [npm `medical-terminologies-mcp`](https://www.npmjs.com/package/medical-terminologies-mcp)
- [WHO ICD API registration](https://icd.who.int/icdapi)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=medical-terminologies-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmedical-terminologies-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
