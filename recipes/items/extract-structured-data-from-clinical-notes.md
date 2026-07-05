---
title: Extract structured variables from free-text clinical notes
parent: All recipes
grand_parent: Recipes
nav_order: 11
problem_class: Data analysis
subject_areas: [Translational Medicine]
evidence_level: Validated
complexity: Claude Code alone
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-05
summary: Use Claude Code alone to extract predefined variables from de-identified clinical notes into a reviewable, provenance-tracked registry table.
---

# Extract structured variables from free-text clinical notes

Point Claude Code at a folder of de-identified clinical notes and a codebook of variables you need; get back a committed, one-row-per-patient registry table with every extracted value traceable to the source sentence.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Validated |
| **Complexity** | Claude Code alone |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Most clinically actionable detail lives in unstructured notes — diagnosis, stage, prior lines of therapy, biomarker status, acute symptoms — not in the structured EHR fields. Building a disease registry, screening a cohort for a study, or assembling an analysis-ready table means someone reads each note and transcribes a fixed set of variables by hand. For a few hundred patients this is weeks of chart abstraction, it is inconsistent between abstractors, and the rules used are rarely written down, so the next team re-abstracts from scratch.

"Solved" looks like: hand over a folder of de-identified notes plus a codebook (the exact variables, their allowed values, and the abstraction rules), get back a `registry.csv` — one row per patient, one column per variable — where every non-null cell carries the source note ID and the quoted sentence it came from, produced by a committed prompt/script so the run is auditable and re-runnable rather than a one-off chat.

## Recommended approach

1. **Write the codebook first.** Before any extraction, define a `codebook.md`: each variable, its type (binary / categorical with allowed values / free number), and a one-line abstraction rule. This is the spec the run is graded against; it belongs under version control alongside the outputs. Keep the note folder de-identified — this recipe assumes notes are already stripped of PHI (see Availability).

2. **Have Claude extract to a structured table with per-cell evidence.** Point Claude Code at the notes folder and the codebook. Force it to quote the source sentence for every value and to distinguish "not mentioned" from "explicitly negated":

   ```
   Read codebook.md. For every note under ./notes/, extract exactly the
   variables it defines. Emit one row per note into records.jsonl with:
   note_id, and for each variable: value, evidence_quote (verbatim
   sentence from the note), and status (found | negated | not_mentioned).
   Use only allowed values from the codebook; never infer a value the
   note does not state. If a variable is not addressed, set
   status=not_mentioned and value=null — do not guess.
   ```

3. **Capture the extraction as a committed script, not a chat.** Ask Claude to write the loop it just ran to a versioned file so the run is reproducible over the whole folder:

   ```
   Write extract_registry.py that iterates ./notes/, applies the
   codebook prompt to each note via the Anthropic API, validates each
   value against the codebook's allowed set, and writes records.jsonl
   plus a flattened registry.csv (one row per note_id, one column per
   variable). Pin the environment in requirements.txt.
   ```

4. **Record provenance.** External-service and model calls are not byte-reproducible, so capture what pins the run: `provenance.json` with the model id and version, the codebook sha256, the number of notes, the run date, and per-variable extraction counts. Commit `codebook.md`, `extract_registry.py`, the pinned env, `records.jsonl`, `registry.csv`, and `provenance.json`. `records.jsonl` (with the `evidence_quote` per cell) is the audit trail — any downstream claim must trace to a quote in it. See the [reproducibility guide](../../guide/advanced/reproducibility.html).

5. **Validate against a gold subset.** Have a clinician manually abstract 20–30 notes, then compute per-variable accuracy / F1 of the extraction against that gold set. Report it in `provenance.json`. This is the number that tells you whether the registry is trustworthy for your notes and codebook.

6. **(Optional) Harmonize the extracted terms to standard codes.** If the extracted diagnoses/drugs/labs must join other cohorts, feed the distinct values into the [harmonize free-text clinical terms recipe](harmonize-clinical-terms-to-standard-codes.html) to produce an ICD-11/RxNorm/LOINC crosswalk. That is a separate, rung-2 step — keep it out of the extraction artifact.

## Why this assembly

Rung 1 of the simplicity ladder. Structured extraction from free text is exactly what a frontier LLM does well unaided — no MCP, no skill, no external database is needed to read a note and fill a table. The discipline that makes it a reproducible *artifact* rather than a chat (a written codebook, per-cell evidence quotes, a committed script, a provenance record, and a gold-set accuracy check) is prompt structure plus a small script, not another component. Escalating to rung 2 buys nothing for the extraction itself; the only genuinely separate task — mapping the extracted terms to authoritative code systems — is handled by a sibling recipe and would confabulate codes if folded into rung 1 (which is precisely why coding is *not* done here).

## Availability

Fully open — the recipe needs only Claude Code and an Anthropic API key; no external service or subscription. The binding constraint is data governance, not licensing: clinical notes are PHI. Run only on de-identified notes, under the data-use agreement and IRB/privacy approvals that cover your cohort, and confirm your Anthropic API tier's data-handling terms meet your institution's requirements (a BAA / zero-retention configuration where required). The output is a research artifact, not a clinical record; any registry feeding patient care needs clinician sign-off.

## Compute requirements

Laptop-sufficient. Each note is one API call of 1–2 seconds; a few hundred notes complete in minutes and cost roughly US $0.001–0.11 per note-prompt depending on model and note length (≈ $0.05–$10.50 per note if you run multiple prompts and repeats for stability). No GPU, negligible local RAM; the deliverable is a small CSV/JSONL.

## Evidence

Validated. [Chen et al., *J. Med. Internet Res.* 2026](https://pubmed.ncbi.nlm.nih.gov/42361337/) benchmarked 12 LLMs extracting structured binary variables from 100 interstitial-lung-disease clinic notes against a three-physician consensus gold standard: **Claude 3.5 Sonnet reached 96.2% accuracy — identical to the human clinicians** — processing each note-prompt in 1–2 s at $0.001–0.11 per call; seven models matched human-level accuracy, while multiclass classification was lower (88–91%). [Bhayana et al., *Radiology* 2025](https://pubmed.ncbi.nlm.nih.gov/39903072/) extracted 10 oncologic-history parameters from 200 EHR notes at **F1 = 0.983**, and radiologists preferred the LLM-generated histories 89% vs 5%. Both validate the exact task — an LLM reading free-text notes into a fixed structured schema at human-level accuracy — though neither packaged it as this committed-artifact workflow; treat your own gold-subset accuracy (step 5) as the confirming number for your codebook and note style.

## Alternatives considered

- **Classical clinical NLP (cTAKES, MetaMap, CRF pipelines).** Purpose-built extractors like the CRF geriatric-syndrome model of [Chen et al., *JMIR Med. Inform.* 2019](https://pubmed.ncbi.nlm.nih.gov/30862607/) (patient-level F1 = 0.83) are the pre-LLM standard and remain a fit for very large batches or fully on-prem constraints. Reach for them when you cannot send notes to an API at all; the LLM path wins on setup speed, codebook flexibility, and accuracy on nuanced variables.
- **PyHealth pipeline (rung 2).** The [PyHealth skill](../../catalog/tools/pyhealth.html) is the right tool when extraction is one step of a downstream *predictive-modeling* pipeline (e.g., readmission risk) rather than a standalone registry — see [Predict hospital readmission from an EHR cohort](predict-hospital-readmission-from-ehr.html). For building an analysis-ready table from notes, plain Claude Code is simpler.
- **Escalating to rung 2 for the extraction itself.** Unnecessary — no external database is queried during extraction. The only rung-2 step is optional downstream code harmonization, handled by its own recipe.

## See also

- [Harmonize free-text clinical terms to standard codes](harmonize-clinical-terms-to-standard-codes.html) — the natural downstream step: map the extracted terms to ICD-11/RxNorm/LOINC.
- [Predict hospital readmission from an EHR cohort](predict-hospital-readmission-from-ehr.html) — when the extracted table feeds a clinical-ML model.
- [PyHealth (Claude Skill)](../../catalog/tools/pyhealth.html) — clinical-ML pipelines with built-in extraction/modeling utilities.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the committed-artifact pattern this recipe follows.

## Sources

- [Chen et al., "Evaluation of Large Language Models for Structured Data Extraction From Interstitial Lung Disease Clinical Notes," *J. Med. Internet Res.* 2026](https://pubmed.ncbi.nlm.nih.gov/42361337/) — published 2026; verified 2026-07-05 (this run).
- [Bhayana et al., "Leveraging Large Language Models to Generate Clinical Histories for Oncologic Imaging Requisitions," *Radiology* 2025](https://pubmed.ncbi.nlm.nih.gov/39903072/) — published 2025-01; verified 2026-07-05 (this run).
- [Chen et al., "Extraction of Geriatric Syndromes From EHR Clinical Notes," *JMIR Med. Inform.* 2019](https://pubmed.ncbi.nlm.nih.gov/30862607/) — published 2019; classical-NLP baseline.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=extract-structured-data-from-clinical-notes&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fextract-structured-data-from-clinical-notes.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
