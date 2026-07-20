---
title: Biomni (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Stanford SNAP Lab
availability: GA
tool_categories: [All]
last_verified: 2026-06-11
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "provenance matches (snap-stanford/Biomni Apache-2.0 active, PyPI biomni 0.0.8, wrapper davila7/claude-code-templates MIT); the agent executes LLM-generated code with full system privileges — sandbox it"
summary: General-purpose biomedical AI agent that plans and runs multi-step research workflows across genomics, drug discovery, and clinical analysis.
---

# Biomni (Claude Skill)

A Claude Code skill that wraps the Stanford SNAP Lab Biomni agent so Claude can autonomously plan and execute multi-step biomedical research tasks across genomics, drug discovery, molecular biology, and clinical analysis.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Stanford SNAP Lab](https://github.com/snap-stanford/Biomni) |
| **Availability** | GA |
| **Pricing** | Free / OSS (Apache-2.0; some bundled tools/databases carry more restrictive commercial licenses) |
| **Capabilities** | Read/Write — generates and executes analysis code, retrieves from an integrated biomedical data lake |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — Apache-2.0 and provenance match, but the agent executes LLM-generated code with full system privileges; run sandboxed |

## How to install

The skill is distributed in the `davila7/claude-code-templates` collection.

- **Claude Code** — install the skill:
  ```
  npx skills add https://github.com/davila7/claude-code-templates --skill biomni
  ```
- **Prerequisite — install the Biomni package** the skill drives (the skill is a workflow wrapper; the agent itself is the `biomni` Python package):
  ```
  uv pip install biomni --upgrade
  ```
  (or `pip install biomni --upgrade`)
- **Prerequisite — API key**: set `ANTHROPIC_API_KEY` (recommended) or another supported provider key (OpenAI, Azure OpenAI, Google Gemini, Groq, AWS Bedrock).
- **First-run data lake**: ~11 GB of biomedical databases downloads automatically to your chosen data path on first agent initialization.

## What it does

Wraps the Biomni `A1` agent, which combines LLM reasoning with retrieval-augmented planning and code execution over an integrated biomedical data lake. Typical workflows:

- CRISPR screening design and gene prioritization
- Single-cell RNA-seq analysis with cell-type annotation
- Drug ADMET prediction and compound optimization
- GWAS variant interpretation and pathway enrichment
- Rare-disease diagnosis and clinical genomics
- Lab-protocol optimization

**Primary use cases**: Multi-step biomedical reasoning, autonomous analysis-pipeline generation, cross-domain research spanning genomics, drug discovery, and clinical analysis.

## Notes

The official `snap-stanford/Biomni` repo ships the agent as a Python package, not as a `SKILL.md`; the Claude Code skill is the community `davila7/claude-code-templates` wrapper, which is why both an `npx skills add` step and a `pip`/`uv` install of `biomni` are required.

Security: Biomni executes LLM-generated code with full system privileges and can access files, network, and system commands. Run it in an isolated/sandboxed environment and avoid exposing sensitive data or credentials. Apache-2.0 covers the framework, but some integrated tools and databases carry more restrictive commercial terms — check before commercial use.

## Sources

- [`snap-stanford/Biomni`](https://github.com/snap-stanford/Biomni)
- [biomni on PyPI](https://pypi.org/project/biomni/)
- [biomni skill — davila7/claude-code-templates](https://agentskills.so/skills/davila7-claude-code-templates-biomni)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=biomni&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbiomni.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
