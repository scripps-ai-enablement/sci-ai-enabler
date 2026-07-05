---
title: Build a pharmacogenomic dosing report from a patient's diplotypes
parent: All recipes
grand_parent: Recipes
nav_order: 3
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-05
summary: Turn a patient's PGx diplotypes plus a medication list into CPIC/DPWG genotype-to-dosing recommendations with cited guideline sources.
---

# Build a pharmacogenomic dosing report from a patient's diplotypes

Hand Claude a patient's star-allele diplotypes (CYP2D6 *1/*4, CYP2C19 *2/*2, …) and a medication list; get back a per-drug table of metabolizer phenotype, CPIC/DPWG dosing recommendation, and the guideline citation behind each call.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A clinical pharmacist or PGx-consult service receives a pharmacogenomic panel result — a set of star-allele diplotypes — alongside the patient's active medication list. The question is operational and repetitive: for each drug with a pharmacogene, translate the diplotype to a metabolizer phenotype (poor/intermediate/normal/rapid/ultrarapid), look up whether CPIC or DPWG has a dosing guideline for that gene-drug pair, and read off the recommendation (avoid, reduce dose, standard, alternative agent). The friction is swivel-chairing across PharmGKB/ClinPGx annotation pages and the CPIC genotype-to-recommendation lookups, one drug at a time, then transcribing guideline strength. "Solved" looks like: paste the diplotypes and drug list, get one cited table, no per-drug portal hopping.

## Recommended approach

1. **Install the [ClinPGx (PharmGKB) skill](../../catalog/tools/clinpgx-database.html)** from the SciAgent-Skills collection (clone the repo, `/plugin install sciagent-skills`). It queries both `api.clinpgx.org` (annotation records) and `api.cpicpgx.org` (genotype→recommendation lookups). No auth.

2. **Prompt with the diplotypes, the drug list, and the report shape.** A worked version:

   ```
   Build a pharmacogenomic dosing report using the ClinPGx skill.

   Patient diplotypes:
     CYP2D6  *1/*4
     CYP2C19 *2/*2
     SLCO1B1 *1/*5
     DPYD    *1/*1
     TPMT    *1/*1

   Active medications: codeine, clopidogrel, simvastatin, fluorouracil,
   azathioprine.

   For each drug:
     1. Identify the relevant pharmacogene.
     2. Translate the diplotype to a metabolizer/function phenotype
        via the CPIC PostgREST API (api.cpicpgx.org).
     3. Fetch the CPIC genotype→recommendation for that gene-drug pair;
        if CPIC has none, check DPWG via ClinPGx annotations.
     4. Report: drug | gene | diplotype | phenotype | recommendation |
        guideline source + strength.

   Render one Markdown table. Cite every recommendation with its CPIC/
   DPWG guideline URL or PharmGKB accession. Flag any gene-drug pair
   with NO published guideline as "no actionable guidance" rather than
   guessing.
   ```

3. **Force the no-guideline path to be explicit.** PGx is only actionable where a guideline exists; the prompt must make Claude say "no actionable guidance" rather than improvise a dose. Spot-check at least one recommendation against the cited CPIC URL before clinical use.

4. **For drug-drug-interaction overlays, chain a second lookup.** Phenoconversion (a CYP inhibitor co-medication shifting an apparent normal metabolizer to poor) is out of scope for ClinPGx alone; note interacting co-meds and, if you need an interaction layer, see the [DDInter](../../catalog/tools/ddinter-database.html) catalog page.

## Why this assembly

Rung 2. One skill spans both halves of the task: ClinPGx for annotations and the CPIC companion API for the genotype→phenotype→recommendation lookup. Adding a second component buys nothing for the core report. Claude Code alone (rung 1) cannot do this — it has no live CPIC access and will confabulate dosing strengths, which is unsafe for a clinical artifact. A rung-3 toolbelt (separate interaction or label MCPs) is only warranted when you extend past dosing into phenoconversion or label-section retrieval; the base dosing report does not need it.

## Availability

Fully open. The ClinPGx/PharmGKB and CPIC APIs are public and need no auth; the skill ships in the CC-BY-4.0 SciAgent-Skills collection (upstream data CC-BY-SA-4.0). The skill runs locally, so patient diplotypes never leave your machine — relevant under HIPAA/IRB constraints. This recipe produces decision *support*, not a prescription; clinical use requires a qualified provider and verification against the primary guideline.

## Compute requirements

Laptop-sufficient. Every step is a read-only REST call; a five-drug report typically completes in well under a minute. No GPU, negligible RAM.

## Evidence

Proposed. No published benchmark of an LLM-driven ClinPGx/CPIC dosing-report assembly is known. The grounding is the guideline corpus the recipe consumes: CPIC publishes peer-reviewed, regularly updated genotype-to-dosing guidelines — e.g. [Amstutz et al., *Clin. Pharmacol. Ther.* 103:210 (2018)](https://doi.org/10.1002/cpt.911) for DPYD/fluoropyrimidines and the CYP2C19/PPI guidance summarized by [Sabet & McGhee, *J. Pediatr. Gastroenterol. Nutr.* (2021)](https://doi.org/10.1097/MPG.0000000000003082) — and the CYP2D6 clinical-impact basis is reviewed in [Molden & Jukić, *Front. Pharmacol.* 12:650750 (2021)](https://doi.org/10.3389/fphar.2021.650750). The skill exposes exactly these guideline records via API; the individual lookups are validated, the LLM-orchestrated composition is not independently benchmarked.

## Alternatives considered

- **Claude Code alone (rung 1).** Unsafe — no live CPIC/PharmGKB access; the model would invent dosing strengths for a clinical document.
- **[Interpret a clinical variant](interpret-clinical-variant.html) (BioMCP).** That recipe answers germline *pathogenicity* ("is this variant disease-causing"), not *drug dosing*. Reach for it when the question is diagnostic rather than therapeutic; reach for this one when you have a confirmed diplotype and a medication list.
- **Rung-3 toolbelt with an interaction layer.** Add [DDInter](../../catalog/tools/ddinter-database.html) or a drug-label skill only when the report must account for phenoconversion or pull full label PGx sections. The base genotype-to-dosing report does not require it.

## See also

- [ClinPGx (PharmGKB) (Claude Skill)](../../catalog/tools/clinpgx-database.html)
- [DDInter](../../catalog/tools/ddinter-database.html) — drug-drug interaction layer for phenoconversion overlays.
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — germline-pathogenicity sibling.
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — gene-centric knowledge-synthesis analogue.

## Sources

- [Amstutz et al., *Clin. Pharmacol. Ther.* 103:210 (2018) — CPIC DPYD / fluoropyrimidine guideline](https://doi.org/10.1002/cpt.911) — published 2018-01; verified 2026-06-14 (this run).
- [Molden & Jukić, *Front. Pharmacol.* 12:650750 (2021) — CYP2D6 dose individualization](https://doi.org/10.3389/fphar.2021.650750) — published 2021-05-04; verified 2026-06-14 (this run).
- [CPIC guidelines portal](https://cpicpgx.org/guidelines/) — verified 2026-06-14 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=build-pharmacogenomic-dosing-report&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fbuild-pharmacogenomic-dosing-report.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
