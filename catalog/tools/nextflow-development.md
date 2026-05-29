---
title: nextflow-development
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Anthropic
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine]
last_verified: 2026-05-19
summary: Runs nf-core rnaseq, sarek, and atacseq pipelines on local FASTQ or GEO/SRA inputs.
---

# nextflow-development

Configures and runs nf-core pipelines on local FASTQ inputs or public GEO/SRA accessions, writing pipeline outputs to a user-specified directory.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Anthropic](https://github.com/anthropics/life-sciences) |
| **Availability** | GA — distributed via `anthropics/life-sciences` (Oct 2025); positioned by Anthropic as a prototype / educational example |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install nextflow-development@life-sciences
  ```
- **Claude.ai** — **Settings → Capabilities → Skills → Upload skill**, using the skill bundle from the `anthropics/life-sciences` repo.

## What it does

Skill instructions for nf-core `rnaseq` (v3.22.2), `sarek` (v3.7.1), and `atacseq` (v2.1.2) — including the standard `-profile test,docker` smoke commands and pointers to expand support to other nf-core pipelines.

**Primary use cases**: Bench-scientist orchestration of bulk RNA-seq, germline/somatic variant calling, and ATAC-seq analyses without bespoke bioinformatics tooling.

## Notes

Requires Nextflow and Docker (or another supported container engine) on the host. Users are responsible for compute capacity and result validation — Anthropic flags this skill as not production-ready without domain validation.

## Sources

- [Skill listing (agent-skills.md)](https://agent-skills.md/skills/anthropics/life-sciences/nextflow-development)
- [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences)
- [nf-core pipelines](https://nf-co.re/pipelines)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=nextflow-development&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fnextflow-development.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
