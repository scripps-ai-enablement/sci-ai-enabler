---
title: Draft a Phase 2/3 clinical-trial protocol from an indication brief
parent: All recipes
grand_parent: Recipes
nav_order: 5
problem_class: Manuscript prep
subject_areas: [Translational Medicine, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-30
summary: Use the Anthropic clinical-trial-protocol plugin to expand a short indication / endpoint brief into an FDA/NIH-compliant Phase 2/3 protocol draft, with regulatory pathway, competitive landscape, and sample-size calculation already wired in.
---

# Draft a Phase 2/3 clinical-trial protocol from an indication brief

Hand Claude a one-paragraph brief naming the indication, intervention, target population, and the primary endpoint; get back a draft Phase 2/3 protocol that already cites the relevant FDA guidance, surveys prior ClinicalTrials.gov entries in the space, and includes a sample-size calculation the medical writer can sanity-check.

| | |
|---|---|
| **Problem class** | Manuscript prep |
| **Subject areas** | Translational Medicine, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Protocol drafting is the bottleneck between a promising IND-enabling result and an active trial. A medical writer or clinician-investigator typically spends 2–8 weeks producing a first draft: pulling the right FDA guidance documents, surveying prior trials in the indication, picking primary and secondary endpoints consistent with the regulatory pathway, running power calculations, and stitching the result into the FDA/NIH IND template. Solved looks like: drop a paragraph that names the drug or device, the indication, the trial phase, and the expected effect size, and get back a structured draft with the four core scaffolding sections already populated — regulatory pathway, competitive landscape, sample-size justification, and the first pass at the protocol body. The output is a starting point for human review, not a submission-ready document.

## Recommended approach

1. **Install the [`clinical-trial-protocol`](../../catalog/tools/clinical-trial-protocol.html) plugin from the `anthropics/healthcare` marketplace.**

   ```
   /plugin marketplace add anthropics/healthcare
   /plugin install clinical-trial-protocol@healthcare
   ```

   The plugin ships as a Claude Code Agent Skill with a four-step waypoint workflow: regulatory classification, competitive landscape, sample-size calculation, protocol drafting.

2. **Invoke the skill with the brief.** The skill is namespaced; from Claude Code call it with the brief inline:

   ```
   /clinical-trial-protocol:start

   Indication: moderate-to-severe ulcerative colitis in adults with
     inadequate response to TNF inhibitors.
   Intervention: <drug name>, <route>, <dose>, <schedule>.
   Phase: 2b.
   Primary endpoint: clinical remission at Week 12
     (Mayo score <= 2, no subscore > 1).
   Expected effect: 25% absolute increase in remission rate
     over placebo (placebo ~10%, treatment ~35%).
   Population: adults 18-75, biopsy-confirmed UC, prior TNF failure.
   Comparator: placebo, 2:1 randomization.
   ```

3. **Review each waypoint before the skill emits the protocol body.** The plugin pauses between waypoints. At each pause, check:
   - **Regulatory pathway** — does the cited FDA guidance match the actual product class (drug vs biologic vs combination product)?
   - **Competitive landscape** — are the ClinicalTrials.gov references current, and are the cited comparator-arm designs correct?
   - **Sample-size calculation** — does the assumed dropout rate, alpha, and power match your statistical plan? A common failure mode is an over-optimistic placebo response rate; correct it before the protocol body is generated.

4. **Pair with [`/match-patient-to-clinical-trials`](match-patient-to-clinical-trials.html) as a sanity check.** Once the draft includes eligibility criteria, run the trial-matching recipe with a synthetic patient summary in your target population to see whether the criteria actually admit the people you intend to enroll.

5. **Export and hand off to medical writing for the regulatory-affairs polish.** The plugin's output is a draft scaffold — protocol synopsis, schedule of activities, statistical analysis plan stubs — that medical writing extends into the submission-ready document.

## Why this assembly

Rung 2 of the simplicity ladder. The entire workflow lives inside a single Anthropic-published Claude Code plugin that already federates ClinicalTrials.gov lookups, FDA guidance retrieval, and templated drafting into one waypoint sequence. Rung 1 (Claude Code alone with a long prompt) under-delivers in two specific ways: the model cannot pull live FDA guidance documents or ClinicalTrials.gov competitors without tool calls, and the four-waypoint pause-and-review structure that makes the plugin auditable does not exist in a bare-prompt approach. A rung-3 toolbelt (BioMCP for trials + a separate FDA-guidance MCP + a stats skill) would replicate the plugin's federation without the templated drafting, which is the slow step.

## Availability

Fully open. The plugin ships free / OSS from `anthropics/healthcare`. ClinicalTrials.gov and FDA guidance documents are public. The sample-size calculation runs locally. The plugin is GA as of January 2026 (Claude for Healthcare launch). Anthropic explicitly markets it as a sample / starting point — review and adapt the SKILL.md and templates to your organization's regulatory workflow before any clinical use.

## Compute requirements

Laptop-sufficient. The plugin's heavy steps are API calls (ClinicalTrials.gov, FDA guidance) and local statistical calculations; wall-clock per full draft is typically 5–15 minutes including the human review pauses. No GPU. The plugin streams the protocol body as it generates, so the long final waypoint can be cancelled mid-emission if an earlier waypoint needs to be revised.

## Evidence

Reported. Anthropic published the plugin alongside the [Claude for Healthcare launch](https://www.anthropic.com/news/healthcare-life-sciences) (January 2026), with a dedicated [tutorial](https://claude.com/resources/tutorials/how-to-use-the-clinical-trial-protocol-draft-generation-sample-skill-with-claude) documenting the four-waypoint flow on a worked Phase 2/3 example. Independent validation of the LLM-driven protocol-drafting *class* is now substantial:

- [Markey et al. *Clinical Trials* (2025)](https://journals.sagepub.com/home/ctj) report that an off-the-shelf LLM achieved ~80% content relevance and >99% medical-terminology accuracy on protocol section generation, with RAG augmentation substantially improving clinical reasoning. The Anthropic plugin's regulatory-classification + competitive-landscape waypoints implement exactly this RAG pattern over FDA guidance and ClinicalTrials.gov.
- [Shin et al. *Clinical Pharmacology & Therapeutics* (2026)](https://ascpt.onlinelibrary.wiley.com/journal/15326535) used GPT-4o to assess statistical-analysis plans and PK-PD protocol components and reached 100% accuracy on disease / intervention / comparator extraction and 14/15 trials on sample-size identification — the same fields the plugin's sample-size waypoint computes.
- [Hauptman et al. *JMIR Dermatology* (2026)](https://derma.jmir.org/) compared 10 LLMs on dermatology research-proposal generation; reasoning-tuned models (ChatGPT-o1, o3-mini) scored highest on physician-assessed accuracy and comprehensiveness — a peer for Claude in the protocol-drafting class.
- [Maleki, *arXiv* 2404.05044 (2024)](https://arxiv.org/abs/2404.05044) trained T5 / BioBart / GPT-3.5/4 on Type-II diabetes protocols from ClinicalTrials.gov and reported per-section generation quality, establishing the modern baseline.

No published head-to-head benchmark of the Anthropic plugin specifically against these alternatives is yet known; the `Reported` label reflects that the assembly is documented and shipped by the vendor with a worked example but not yet independently benchmarked. Treat outputs as drafts for medical-writing and regulatory review.

## Alternatives considered

- **Claude Code alone with a hand-written prompt (rung 1).** Possible for a synopsis-level scaffold, but cannot pull live FDA guidance or current ClinicalTrials.gov competitors without MCP / plugin tool calls, and lacks the waypoint structure that makes a regulatory-affairs review tractable. Reach for it only when you need a one-page synopsis and have the regulatory context already in the system prompt.
- **A rung-3 toolbelt of [BioMCP](../../catalog/tools/biomcp.html) + a stats skill.** BioMCP covers the ClinicalTrials.gov competitive-landscape step well, but does not ship the FDA guidance retrieval or the IND-template drafting that the Anthropic plugin includes. Pick this path only if your organization's regulatory documents are not the FDA / NIH templates the plugin emits.
- **An autonomous-science system (rung 4).** No documented autonomous loop currently drafts regulatory protocols end-to-end; protocol drafting is a human-in-the-loop activity by design. Do not escalate.

## See also

- [clinical-trial-protocol plugin](../../catalog/tools/clinical-trial-protocol.html)
- [Match a patient summary to recruiting clinical trials](match-patient-to-clinical-trials.html) — natural pairing to sanity-check the draft eligibility criteria.
- [Scan approved drugs for repurposing candidates against a disease](scan-drug-repurposing-candidates.html) — upstream step when the protocol covers a repurposing hypothesis.
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — upstream step when the protocol covers a novel target.

## Sources

- [`anthropics/healthcare`](https://github.com/anthropics/healthcare) — plugin source; verified 2026-05-30 (this run).
- [How to use the Clinical Trial Protocol Draft Generation sample skill with Claude](https://claude.com/resources/tutorials/how-to-use-the-clinical-trial-protocol-draft-generation-sample-skill-with-claude) — Anthropic tutorial; verified 2026-05-30 (this run).
- [Advancing Claude in healthcare and the life sciences](https://www.anthropic.com/news/healthcare-life-sciences) — launch announcement, January 2026.
- [Markey et al., "Off-the-shelf large language models for clinical trial protocol section generation," *Clinical Trials* 2025](https://journals.sagepub.com/home/ctj) — class-level evidence on RAG-augmented LLM protocol drafting.
- [Shin et al., "Large Language Models for Clinical Trial Protocol Assessments," *Clinical Pharmacology & Therapeutics* 2026](https://ascpt.onlinelibrary.wiley.com/journal/15326535) — quantitative validation of LLM extraction of trial-design fields.
- [Maleki, "Clinical Trials Protocol Authoring using LLMs," *arXiv* 2404.05044 (2024-04-08)](https://arxiv.org/abs/2404.05044) — earliest methods baseline.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=draft-phase23-clinical-trial-protocol&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdraft-phase23-clinical-trial-protocol.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
