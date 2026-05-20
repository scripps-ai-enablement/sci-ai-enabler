---
title: fhir-developer (Anthropic Healthcare Plugin)
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Anthropic
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-05-20
summary: Anthropic Claude Code plugin for authoring FHIR R4 resources with LOINC, SNOMED, and RxNorm validation.
---

# fhir-developer

Anthropic-published Claude Code plugin from the `anthropics/healthcare` marketplace. Helps clinicians and developers translate prose into FHIR R4 resources with terminology validation built in.

| | |
|---|---|
| **Type** | Claude Code Plugin |
| **Supplier** | [Anthropic](https://github.com/anthropics/healthcare) |
| **Availability** | GA |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write — generates and validates FHIR R4 bundles |

## How to install

```
/plugin marketplace add anthropics/healthcare
/plugin install fhir-developer@healthcare
```

## What it does

A FHIR R4 authoring workflow that:

- Translates clinician text into structured FHIR resources (Patient, Observation, Condition, MedicationRequest, etc.).
- Validates codes against **LOINC** (observations / labs), **SNOMED CT** (conditions / procedures), and **RxNorm** (medications).
- Assembles validated resources into FHIR bundles.

**Primary use cases**: Convert clinician notes into coded FHIR resources, draft trial-eligibility queries, build sample bundles for integration testing.

## Notes

Distinct from the WSO2 FHIR MCP — that one *talks to* a FHIR server; this one *authors* the resources you send. The two are complementary.

## Sources

- [`anthropics/healthcare`](https://github.com/anthropics/healthcare)
- [Marketplace manifest](https://raw.githubusercontent.com/anthropics/healthcare/main/.claude-plugin/marketplace.json)
