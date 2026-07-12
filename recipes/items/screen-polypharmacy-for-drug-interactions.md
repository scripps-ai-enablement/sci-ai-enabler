---
title: Screen a polypharmacy medication list for drug-drug interactions
parent: All recipes
grand_parent: Recipes
nav_order: 24
problem_class: Knowledge synthesis
subject_areas: [Drug Repurposing and Discovery, Translational Medicine]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-12
summary: Ground Claude in the DDInter skill to screen a multi-drug medication list for pairwise interactions with severity and mechanism, instead of asking the model from memory.
---

# Screen a polypharmacy medication list for drug-drug interactions

Hand Claude Code a patient's or candidate-regimen's medication list; get back a cited pairwise drug-drug-interaction table with severity, mechanism, and management note — sourced from the curated DDInter database, not the model's memory.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Drug Repurposing and Discovery, Translational Medicine |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A patient on five or more drugs, or a repurposing regimen that stacks a candidate onto standard-of-care, raises an immediate question: which pairs interact, how badly, and what to do about it. The combinatorics are unforgiving — a 10-drug list has 45 pairs — and the answer must be sourced, severity-graded, and mechanism-aware, not a confident guess. The tempting shortcut is to paste the list into a chatbot and ask. The published failure mode of that shortcut is well documented: bare LLMs over-flag (low precision, alert fatigue) and hallucinate clinically inaccurate interactions, so their output cannot stand without a curated reference behind it.

Solved looks like: one prompt, one medication list in, one cited table out — every flagged pair traceable to a DDInter record with a severity grade (major / moderate / minor) and a management recommendation, and an explicit "no interaction found in DDInter" line for the pairs that are clean.

## Recommended approach

1. **Install the [DDInter skill](../../catalog/tools/ddinter-database.html)** — it wraps the DDInter REST API (1.7M+ interactions, 2,400+ drugs, no auth):

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then run `/plugin install sciagent-skills` in Claude Code and confirm it under `/plugin` → Installed.

2. **Drive the pairwise screen with one prompt.** Give Claude the full list and force it to enumerate every pair through DDInter rather than reason from memory:

   ```
   Use the ddinter-database skill to screen this medication list for
   drug-drug interactions. Do NOT answer from prior knowledge — every
   interaction you report must come from a DDInter query.

   Medications: warfarin, amiodarone, simvastatin, metformin,
   omeprazole, sertraline.

   For each drug, resolve its DDInter ID, then query interactions for
   every unique pair. Render a Markdown table:
   drug A | drug B | DDInter severity (major/moderate/minor) |
   mechanism | management note | DDInter source ID.
   Sort by severity (major first). At the end, list every pair that
   returned NO interaction in DDInter as an explicit "clean" line.
   ```

3. **(Optional, rung 3) Overlay FDA labeling and pharmacogenomic phenoconversion.** For pairs DDInter grades major, pull the structured product label with the [DailyMed skill](../../catalog/tools/dailymed-database.html) to confirm the boxed-warning / contraindication language, and — if the patient has a known metabolizer phenotype — check the [ClinPGx skill](../../catalog/tools/clinpgx-database.html) for phenoconversion that could turn a moderate interaction into a major one (e.g., a CYP2D6 inhibitor in a CYP2D6 intermediate metabolizer). Keep these to the flagged pairs; running them across all 45 is wasted latency.

4. **Read the table as a triage queue, not a verdict.** DDInter severity is a population-level grade; it does not know the patient's dose, renal function, or timing. Hand the major/moderate rows to a pharmacist or prescriber for the clinical call.

5. **Save the prompt as a slash command.** Parameterize on the drug list — `/ddi-screen <comma-separated drugs>` — and reuse for every new regimen or repurposing stack.

## Why this assembly

Rung 2 of the simplicity ladder, and it stops there. The entire task is a curated-database lookup plus a pairwise enumeration that Claude orchestrates; one skill (DDInter) supplies the evidence and Claude supplies the loop and the write-up. Rung 1 (Claude Code alone, from memory) is the explicitly-discouraged path — the literature shows bare LLMs over-flag and hallucinate DDIs, which is exactly the precision failure DDInter prevents. The optional DailyMed + ClinPGx overlay (step 3) is a rung-3 escalation reserved for confirming or up-grading the major pairs; most screens never need it. Rung 4 (an autonomous system) buys nothing for a bounded ranked-join over one database.

## Availability

Fully open. DDInter, DailyMed, and ClinPGx are all distributed as OSS Claude skills (CC-BY-4.0 / CC0) wrapping public, no-auth REST APIs. No subscription, account, or institutional access required. Note the data caveat: DDInter is a research database, not a regulated clinical decision-support product — use it to triage, and route the clinical decision through a licensed professional.

## Compute requirements

Laptop. All three skills are read-only REST lookups; no GPU, no large downloads. Wall-clock is dominated by Claude's tool-calling latency — a 6-drug list (15 pairs) typically screens in 1–3 minutes; a 12-drug list (66 pairs) in 3–8 minutes. The optional DailyMed/ClinPGx overlay adds a few seconds per flagged pair.

## Evidence

Reported. Domián et al. (*Exploratory Research in Clinical and Social Pharmacy*, Sept 2025) compared three general-purpose LLMs (ChatGPT, Gemini, Copilot) against established DDI databases on real-world medication records from 57 rheumatology patients (204 reference interactions). The LLMs over-flagged badly — Copilot returned 1,813 candidate interactions and Gemini 1,556 against a 204-interaction reference — with uniformly low precision and the authors attributing errors to hallucination, concluding LLM output "must always undergo professional validation." That study is the direct evidence that the ungrounded shortcut fails and that screening must be anchored to a curated DDI database — which is precisely the assembly this recipe recommends (Claude + DDInter rather than Claude alone). The DDInter database itself is the peer-reviewed reference (Xiong et al., *Nucleic Acids Research* 50:D1200, 2022, [doi:10.1093/nar/gkab880](https://doi.org/10.1093/nar/gkab880)); no published benchmark of the Claude-plus-DDInter-skill composition specifically is known, so this is `Reported` rather than `Validated`.

## Alternatives considered

- **Claude Code alone, from memory (rung 1).** The discouraged path. Use it only for a throwaway sanity check on one or two famous pairs (warfarin + NSAID); never for a real medication list — the precision is too low and the failure mode is silent.
- **DailyMed-only by drug label (rung 2 variant).** Each FDA structured product label lists known interactions in its own warnings section. Reach for this when you have a single drug and want the regulator's view rather than a pairwise matrix; it does not scale to enumerating all pairs in a long list.
- **The [pharmacogenomic dosing recipe](build-pharmacogenomic-dosing-report.html).** Reach for that when the question is "given this patient's diplotypes, how should I dose" rather than "do these drugs interact." The two compose — phenoconversion (step 3 here) is the bridge — but they answer different questions.
- **An autonomous system (rung 4).** Overkill. The task is a bounded database join, not an open-ended discovery loop.

## See also

- [DDInter (Claude Skill)](../../catalog/tools/ddinter-database.html)
- [DailyMed (Claude Skill)](../../catalog/tools/dailymed-database.html) — FDA label overlay for flagged pairs.
- [ClinPGx (Claude Skill)](../../catalog/tools/clinpgx-database.html) — phenoconversion overlay.
- [Build a pharmacogenomic dosing report from a patient's diplotypes](build-pharmacogenomic-dosing-report.html) — the genotype-driven dosing companion.
- [Scan adverse-event reports for a drug-safety signal](scan-adverse-events-for-drug-safety-signal.html) — population safety signal, complementary lens.

## Sources

- [Domián BM et al., "Comparative evaluation of artificial intelligence platforms and drug interaction screening databases using real-world patient data," *Explor. Res. Clin. Soc. Pharm.* 2025, doi:10.1016/j.rcsop.2025.100655](https://pubmed.ncbi.nlm.nih.gov/41425735/) — published 2025-09; verified 2026-06-14 (this run).
- [Xiong G et al., "DDInter: an online drug-drug interaction database," *Nucleic Acids Research* 50:D1200, doi:10.1093/nar/gkab880](https://doi.org/10.1093/nar/gkab880) — published 2022.
- [`jaechang-hits/SciAgent-Skills` — ddinter-database SKILL.md](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/ddinter-database/SKILL.md) — verified 2026-06-14 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=screen-polypharmacy-for-drug-interactions&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fscreen-polypharmacy-for-drug-interactions.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
