---
title: clinical-trial-protocol (Anthropic Healthcare Plugin)
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Anthropic
availability: GA
tool_categories: [Translational Medicine, Drug Repurposing and Discovery]
last_verified: 2026-05-23
summary: Anthropic Claude Code plugin that drafts FDA/NIH-compliant Phase 2/3 clinical-trial protocols for drugs or devices via a waypoint-based workflow.
---

# clinical-trial-protocol

Anthropic-published Claude Code plugin from the `anthropics/healthcare` marketplace. Drafts a full Phase 2/3 clinical-trial protocol document from a minimal indication / endpoint brief, following FDA and NIH templates.

| | |
|---|---|
| **Type** | Claude Code Plugin (Agent Skill) |
| **Supplier** | [Anthropic](https://github.com/anthropics/healthcare) |
| **Availability** | GA — shipped 2026-01 alongside the Claude for Healthcare launch |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write — researches regulatory landscape, generates protocol document |

## How to install

- **Claude Code** — plugin marketplace:

  ```
  /plugin marketplace add anthropics/healthcare
  /plugin install clinical-trial-protocol@healthcare
  ```

- **Claude.ai** — download the skill ZIP from the `anthropics/healthcare` repo and upload via **Settings → Capabilities → Skills** (Team / Enterprise admin).

## What it does

A waypoint-based, four-step workflow that:

1. **Regulatory classification** — searches FDA guidance documents to identify the relevant pathway (IND for drugs, IDE/IVD for devices).
2. **Competitive landscape** — queries ClinicalTrials.gov for similar prior or active trials.
3. **Sample-size calculation** — runs power calculations against the supplied endpoints and effect sizes.
4. **Protocol drafting** — emits an initial full protocol document conforming to the FDA/NIH IND / IVD template.

**Primary use cases**: Early-stage protocol drafting at biotech and medical-device companies; regulatory-affairs first-drafts; medical-writing acceleration; trial-design exploration in academic labs.

## Notes

Anthropic explicitly markets this as a **sample / starting point** — not production-ready. Review and adapt the SKILL.md and templates to your organization's workflow before clinical use. Output is a draft for human review, not a submission-ready document.

## Sources

- [`anthropics/healthcare`](https://github.com/anthropics/healthcare)
- [How to use the Clinical Trial Protocol Draft Generation sample skill with Claude](https://claude.com/resources/tutorials/how-to-use-the-clinical-trial-protocol-draft-generation-sample-skill-with-claude)
- [Advancing Claude in healthcare and the life sciences](https://www.anthropic.com/news/healthcare-life-sciences)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=clinical-trial-protocol&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fclinical-trial-protocol.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
