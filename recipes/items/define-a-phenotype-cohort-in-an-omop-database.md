---
title: Define a phenotype cohort in an OMOP CDM database
parent: All recipes
grand_parent: Recipes
nav_order: 35
problem_class: Data analysis
subject_areas: [Translational Medicine]
evidence_level: Proposed
complexity: Multi-tool harness
availability: Institutional access
compute_requirements: Laptop
last_verified: 2026-08-02
summary: Build a frozen OMOP concept set with OMOPHub, then count and characterise the cohort in your CDM with pyomop, emitting a portable attrition table.
---

# Define a phenotype cohort in an OMOP CDM database

Turn "patients with heart failure who started an SGLT2 inhibitor" into a concept set, a SQL definition, and an attrition table you can hand to another OHDSI site and have them reproduce.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | Multi-tool harness |
| **Availability** | Institutional access |
| **Compute** | Laptop |

## Problem

Observational studies on an OMOP CDM start with a phenotype: a machine-executable definition of who is in the cohort. Getting it wrong is cheap to do and expensive to discover. The characteristic failure is silent, not loud — you write a query against a handful of ICD-10 codes, the CDM stores standard SNOMED concepts, the join returns zero rows or a suspiciously round number, and nobody notices until the effect estimate looks strange. Descendant concepts are the other half of the trap: `Heart failure` has hundreds of descendants, and a definition that omits them undercounts by an amount that varies by site, which is precisely the kind of variation a multi-site study cannot absorb.

Handing this to an agent makes it faster and, without guardrails, more dangerous — a model will confidently emit `concept_id = 316139` from memory, and a plausible-looking wrong concept id is worse than an error. Solved looks like: a concept set built by querying the vocabularies rather than recalling them, frozen to a named vocabulary release; a SQL definition checked before it executes; an attrition table showing how many subjects each criterion removes; and a committed bundle another site can run against their own CDM.

## Recommended approach

1. **Install both components.** The [OMOPHub MCP server](../../catalog/tools/omophub-mcp.html) answers "what concept is this, and what does it map to" over 10M+ OMOP vocabulary concepts without a local ATHENA download; [pyomop](../../catalog/tools/pyomop.html) runs SQL against your CDM instance. Install paths are on the catalog pages. Two things to settle before you go further:

   - Point pyomop at the CDM with a **read-only database role**. `run_sql` is not restricted upstream and the model composes the SQL.
   - If you have no CDM to hand yet, pyomop's `create_eunomia` loads the OHDSI Eunomia demo dataset into local SQLite — develop the definition there, then repoint at the real instance.

2. **Pin the vocabulary release before building anything.** Call `list_vocabularies` and record the release identifiers for every vocabulary you will use (SNOMED, ICD10CM, RxNorm, …). Concept ids are stable, but *membership* of a hierarchy is not — a concept set built against one release and executed against a CDM loaded from another is a real and common discrepancy.

3. **Build the concept set by querying, never from memory.** Use the server's `phenotype-concept-set` prompt, then verify each concept individually:

   ```
   Using the omophub MCP server, build a concept set for "heart failure".
   For every candidate: return concept_id, concept_name, domain_id,
   vocabulary_id, concept_class_id, and standard_concept. For any
   non-standard source code I give you (ICD-10-CM I50.*), use map_concept
   to resolve it to the standard SNOMED concept and show both sides of the
   mapping. Then use get_hierarchy to list descendants of each standard
   concept and report how many there are.
   Do not state a concept_id you have not retrieved from the server.
   ```

   That last line is load-bearing. Repeat for the drug exposure leg (`RxNorm`, ingredient level, then descendants for the branded and clinical-drug forms).

4. **Freeze the concept set as a file, with an explicit descendants flag.** Commit `cohort/concept_set.csv` with one row per included concept: `concept_id`, `concept_name`, `vocabulary_id`, `standard_concept`, `include_descendants` (true/false, decided per concept — not globally), `include_mapped`, and a short `rationale` string. Also record the concepts you *considered and excluded*, in `cohort/concept_set_excluded.csv`. A reviewer's first question is always about a code you left out; answering it from a file beats answering it from recollection.

5. **Write the cohort SQL as a file, and validate before executing.** Have the agent generate `cohort/cohort.sql` parameterised on the concept-set table, then run pyomop's `check_sql` on it before `run_sql`. Use `get_usable_table_names` and `get_table_columns` first so the SQL is written against the actual schema rather than an assumed CDM version — v5.3 and v5.4 differ in ways that produce valid-but-wrong queries.

   ```
   Inspect the CDM schema with get_usable_table_names and get_table_columns
   for person, condition_occurrence, drug_exposure, observation_period.
   Write cohort/cohort.sql implementing: index = first drug_exposure of any
   concept in the SGLT2i set; require >=365 days of prior observation_period;
   require >=1 condition_occurrence from the heart-failure set in the 365
   days before index; exclude subjects with <1 day of post-index observation.
   Run check_sql on it and show me the statement before you execute anything.
   ```

6. **Demand an attrition table, not a count.** One row per criterion in the order the protocol applies them, with subjects remaining after each. This is the standard OHDSI artifact and it is also the best available bug detector — a step that drops 100% or 0% of the cohort is almost always a join or a vocabulary problem, not a real finding.

   ```
   Emit results/attrition.csv: step, criterion, n_subjects_remaining,
   n_removed. Then emit results/cohort_characteristics.csv: n, age at index
   (mean/SD), sex distribution, index-year distribution, and the top 20
   co-occurring condition concepts by prevalence.
   ```

7. **Sanity-check the definition against the data before you believe it.** Ask for a small fixed panel of checks and read them yourself: every concept id in the set actually appears in the CDM's `concept` table; the index-year distribution matches the CDM's known coverage window; the sex and age distributions are not degenerate. Agent-generated SQL over EHR schemas is accurate enough to be useful and not accurate enough to be trusted unverified — treat execution results, not the SQL's plausibility, as the evidence.

8. **Commit the bundle and record provenance.** The deliverable is `cohort/concept_set.csv`, `cohort/concept_set_excluded.csv`, `cohort/cohort.sql`, a `cohort/build_cohort.py` driver, `results/attrition.csv`, `results/cohort_characteristics.csv`, and a pinned `requirements.txt`. Emit `provenance.json` recording: CDM version (5.3/5.4) and the `cdm_source` release date, the vocabulary release from step 2, the pyomop version, the OMOPHub server version, the sha256 of `cohort.sql` and `concept_set.csv`, the UTC run date, and the model id. Ship the concept set and SQL to a collaborating site rather than the row counts — the OHDSI network experience is that the *definition* travels and the fitted numbers do not.

## Why this assembly

Rung 3, and each component is doing something the other cannot. pyomop alone (rung 2) fails at the step that matters most: with no vocabulary service, the model supplies concept ids from pre-training, and a wrong-but-plausible concept id produces a query that runs cleanly and returns the wrong cohort. OMOPHub alone (also rung 2) gives you a defensible concept set and no way to count anyone. Plain Claude Code (rung 1) can write CDM SQL but has neither the vocabulary nor the schema in front of it. The pairing is the smallest assembly that closes both gaps, and it stops at two components — cohort *comparison*, propensity matching and outcome models are downstream problems with their own tools.

## Availability

Institutional access. Three separate gates: (1) you need access to an institutional OMOP CDM containing patient data, with the governance approval and read-only role that implies; (2) OMOPHub's server is MIT but the backing API at `api.omophub.com` requires a free account and an `oh_`-prefixed API key, and the free-tier rate limits are not documented — assume you may hit one on a large concept set; (3) vocabulary content keeps its source licenses, and SNOMED CT requires an affiliate licence in non-member countries. Note the data-flow asymmetry: your *concept queries* leave the building to OMOPHub, your *patient data* does not — pyomop runs against your database locally. Concept names can still be disclosive of study intent, so check that against your governance rules. pyomop is **GPL-3.0**; redistributing a derived pipeline carries copyleft obligations.

## Compute requirements

Laptop, for the agent side. Both components are thin clients; the work happens in your CDM's database engine, and that is where the cost lives. On a multi-million-person CDM, a `condition_occurrence` scan over a large descendant set is a minutes-to-hours query — develop against Eunomia or a sampled CDM schema first, and make sure the `concept_id` columns you join on are indexed before running the full definition. Expect the attrition and characteristics queries to dominate wall-clock, not the concept-set construction. Output sizes are trivial (a few CSVs).

## Evidence

Proposed. No documented attempt at this exact assembly (Claude Code + OMOPHub MCP + pyomop) building a phenotype cohort is known, and neither component has a published benchmark of its own. The design choices above are each grounded:

- **Ship the definition, not the fitted artifact.** [Kashyap et al., *JAMIA* (2020)](https://doi.org/10.1093/jamia/ocaa032) built 10 phenotype classifiers with APHRODITE and evaluated them across three OHDSI sites: portability was good within the USA (mean recall −0.08, precision −0.01) and markedly worse at an international site (−0.18, −0.10), concluding that "sharing the classifier-building recipe, rather than the pretrained classifiers, may be more useful". That is the argument for step 8's committed bundle.
- **Agent-written SQL over EHR schemas needs execution-based verification, not plausibility.** [EHRSQL (Lee et al., NeurIPS D&B 2023)](https://arxiv.org/abs/2301.07695) built a text-to-SQL benchmark from 222 hospital staff over MIMIC-III and eICU, deliberately including *unanswerable* questions, because the deployment-critical failure is a confident answer to a question the database cannot support. The [EHRSQL 2024 shared task](https://arxiv.org/abs/2405.06673) turned reliability — abstaining rather than guessing — into the scored objective across eight teams. Step 7 exists for this reason.

No head-to-head compares an agent-built OMOP concept set against an ATLAS-built one. Until one exists, treat the attrition table as the acceptance test.

## Alternatives considered

- **OHDSI ATLAS.** The community-standard GUI for exactly this task: concept-set builder, cohort definition, generation, and export to a portable JSON that other OHDSI tools consume. If your site already runs ATLAS with WebAPI, use it — it is more mature, and its JSON is the real interoperability format. Reach for this recipe when you have a CDM but no ATLAS deployment, or when the cohort definition is one step inside a larger scripted analysis you want in one place.
- **pyomop alone, no vocabulary service.** Viable only if you have ATHENA vocabularies loaded locally and query the `concept` and `concept_ancestor` tables directly with SQL — then the vocabulary lookup is just more SQL and the second component is redundant. That is a legitimate rung-2 simplification for a well-equipped site.
- **[Medical Terminologies MCP](../../catalog/tools/medical-terminologies-mcp.html) instead of OMOPHub.** Covers ICD-11, SNOMED CT, LOINC, RxNorm, MeSH and ATC, but is not OMOP-shaped — no `concept_id`, no `concept_ancestor` traversal. Use it for general terminology work; use OMOPHub when the output has to join against a CDM.
- **Escalating to an autonomous system.** Not warranted. This problem is small, highly structured, and the failure mode is silent wrongness — the answer is more verification, not more autonomy.

## See also

- [OMOPHub MCP Server](../../catalog/tools/omophub-mcp.html)
- [pyomop](../../catalog/tools/pyomop.html)
- [Harmonize clinical terms to standard codes](harmonize-clinical-terms-to-standard-codes.html) — the terminology-mapping sibling when the destination is not an OMOP CDM.
- [Extract structured data from clinical notes](extract-structured-data-from-clinical-notes.html) — the upstream step when the phenotype lives in free text rather than in coded data.
- [Fit a survival model to censored clinical outcomes](fit-survival-model-to-clinical-outcomes.html) — a natural downstream analysis once the cohort exists.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [Kashyap et al. 2020 — phenotype classifiers across OHDSI sites (JAMIA)](https://doi.org/10.1093/jamia/ocaa032) — published 2020; verified 2026-08-02 (this run).
- [EHRSQL: a practical text-to-SQL benchmark for EHRs](https://arxiv.org/abs/2301.07695) — published 2023-01-16, last updated 2026-03-04; verified 2026-08-02 (this run).
- [Overview of the EHRSQL 2024 shared task on reliable text-to-SQL modeling](https://arxiv.org/abs/2405.06673) — published 2024-05-04; verified 2026-08-02 (this run).
- [OHDSI OMOP Common Data Model](https://ohdsi.github.io/CommonDataModel/) — verified 2026-08-02 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=define-a-phenotype-cohort-in-an-omop-database&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdefine-a-phenotype-cohort-in-an-omop-database.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
