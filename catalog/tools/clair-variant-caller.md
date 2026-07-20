---
title: Clair Variant Caller (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: HKU-BAL
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-27
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "HKU-BAL/Clair-skills resolves (GitHub API, pushed 2026-04-16) and provenance matches, but the skill repo publishes no SPDX LICENSE (page already notes this) and is single-maintainer/6-star; no GitHub advisories"
summary: "Agent skill for the Clair suite — germline, somatic, mosaic, and long-read RNA variant calling with Clair3/ClairS/Clair-Mosaic."
---

# Clair Variant Caller (Claude Skill)

An agent skill that teaches Claude how to run the Clair suite of deep-learning variant callers for germline, somatic, mosaic, and long-read RNA variant detection.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [HKU-BAL](https://github.com/HKU-BAL/Clair-skills) |
| **Availability** | GA |
| **Pricing** | Free / OSS — Clair tools are BSD-3-Clause; skill wrapper distributed as-is (**Unverified —** no explicit SPDX license file on the skill repo) |
| **Capabilities** | Read/Write — Claude invokes the Clair CLIs locally (Bash) over BAM/CRAM inputs and writes VCFs |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — HKU-BAL/Clair-skills resolves, provenance matches, but no SPDX LICENSE on the skill repo, single-maintainer; no advisories |

## How to install

The skill is a `SKILL.md` (plus helper docs) that Claude reads; the underlying Clair callers must be installed separately (see Notes).

- **Claude Code** — global install:
  ```
  git clone https://github.com/HKU-BAL/Clair-skills.git ~/.claude/skills/clair-variant-caller
  ```
- **Claude Code** — project-level install (clone into the repo you are working in):
  ```
  git clone https://github.com/HKU-BAL/Clair-skills.git .claude/skills/clair-variant-caller
  ```

The skill resolves as `/clair-variant-caller` once cloned into a skills directory. No registration command is needed for skills — Claude loads them from the skills folder on the next session.

## What it does

Wraps five tools from the Clair suite:

- **Clair3** — germline variant calling (DNA)
- **Clair3-RNA** — variant calling from long-read RNA-seq
- **ClairS** — somatic variant calling (paired tumor/normal)
- **ClairS-TO** — somatic variant calling (tumor-only)
- **Clair-Mosaic** — mosaic variant calling

The skill guides input preparation (BAM/CRAM + reference), model/platform selection (ONT, PacBio HiFi, Illumina), and command construction for each caller.

**Primary use cases**: germline SNP/indel calling, somatic variant calling (tumor/normal and tumor-only), mosaic variant detection, long-read RNA variant calling.

## Notes

This skill provides procedural know-how only — the Clair binaries (Clair3, ClairS, etc.) and their model files must be installed on the host (typically via the per-tool conda/Docker instructions in the upstream Clair repos). The skill repo states it is "provided as-is for use with the Clair suite"; the Clair tools themselves are BSD-3-Clause licensed by HKU-BAL. For short-read germline calling via GATK see `gatk-variant-calling.md`; for variant annotation see `snpeff-variant-annotation.md`.

## Sources

- [`HKU-BAL/Clair-skills`](https://github.com/HKU-BAL/Clair-skills)
- [`GoekeLab/awesome-genomic-skills`](https://github.com/GoekeLab/awesome-genomic-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=clair-variant-caller&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fclair-variant-caller.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
