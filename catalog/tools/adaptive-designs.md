---
title: Adaptive Designs (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-02
summary: "Plan group-sequential, sample-size re-estimation, seamless Phase 2/3 and enrichment trials with rpact/gsDesign, against FDA and ICH E20 adaptive-design guidance"
verification: works
verified_on: 2026-08-03
reviewed_on: 2026-08-03
security: cleared
security_on: 2026-08-03
security_note: "GPTomics/bioSkills root LICENSE confirmed MIT this run, not archived, 1.1k stars, skill dir current"
---

# Adaptive Designs (bioSkills)

A Claude Code skill for planning adaptive clinical trials — interim analyses, sample-size re-estimation, arm selection, population enrichment — with the boundary maths done in `rpact`/`gsDesign` and the design choices anchored to current regulatory guidance.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — `rpact`, `gsDesign`, `gsDesign2`, `adaptr`, `simtrial`, `BOIN`, `dfcrm`, `trialr` and `escalation` are separately installed OSS R packages. The commercial alternatives the skill names (FACTS, East/EastHorizon, ADDPLAN) are licensed products and are not installed. |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (R), not as an MCP tool |
| **Verified** | works · 2026-08-03 |
| **Security** | cleared · 2026-08-03 — GPTomics/bioSkills MIT confirmed, provenance matches, no advisories |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "clinical-biostatistics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/clinical-biostatistics/adaptive-designs ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the R packages on first use, e.g. `install.packages(c("rpact", "gsDesign", "gsDesign2"))`.

## What it does

Walks a five-stage design process and picks the machinery to match:

- **Design selection** — group-sequential (O'Brien–Fleming, Pocock, Lan–DeMets alpha spending), blinded sample-size re-estimation (Friede–Kieser), unblinded SSR (Cui–Hung–Wang weighted statistics, Mehta–Pocock promising zone), combination tests, seamless Phase 2/3 with treatment-arm selection, adaptive population enrichment, and response-adaptive randomisation.
- **Pre-specification** — encoding boundaries, spending functions, interim timing, the SSR rule and the IDMC firewall in the Statistical Analysis Plan before any data are seen.
- **Interim analysis** — computing the test statistic, conditional power or interim effect estimate for IDMC review of unblinded data.
- **Adaptation decision** — applying the pre-specified rule: stop for efficacy or futility, increase n, drop or select arms, restrict the population.
- **Final analysis** — combining stages with the pre-specified weights or combination test, and reporting bias-corrected estimates where the adaptation induces bias.

Software the skill drives: `rpact` 4.2+ (primary — group-sequential, SSR, combination tests, enrichment), `gsDesign` 3.6+ and `gsDesign2` 1.1+ (boundaries and spending), `adaptr` (enrichment, RAR), `simtrial` (simulated operating characteristics), and for dose-finding `BOIN` (FDA Fit-for-Purpose designation, December 2021), `dfcrm` (CRM), `trialr` (EffTox) and `escalation`.

**Primary use cases**: sizing a trial with interim looks, choosing a sample-size re-estimation rule, planning a master or platform protocol.

## Notes

Regulatory anchors cited in the skill: the **FDA 2019 Final Adaptive Designs Guidance** (Federal Register 2019-25986, 2 December 2019), the **FDA 2022 Final Master Protocols Guidance** (March 2022), the **ICH E20 draft** at Step 2b (25 June 2025) — which the skill is explicit is **not final** — and an FDA CDER Bayesian methodology draft (January 2026). Treat the draft guidances as drafts when writing an SAP.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-clinical-biostatistics-adaptive-designs`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/adaptive-designs`. Upstream directory: `clinical-biostatistics/adaptive-designs`.

Complements [Trial Reporting](trial-reporting.html) (analysis and CONSORT-conformant write-up) and [Clinical Trial Protocol](clinical-trial-protocol.html) (protocol document generation). Sample-size work for fixed designs and the missing-data handling that follows an interim are covered by sibling skills in the same category.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-biostatistics/adaptive-designs/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/adaptive-designs/SKILL.md)
- [FDA Adaptive Designs for Clinical Trials of Drugs and Biologics (2019)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/adaptive-design-clinical-trials-drugs-and-biologics-guidance-industry)
- [`rpact` on CRAN](https://cran.r-project.org/package=rpact)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=adaptive-designs&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fadaptive-designs.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
