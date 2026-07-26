---
title: Harmonize free-text clinical terms to standard codes
parent: All recipes
grand_parent: Recipes
nav_order: 14
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-26
summary: Use the Medical Terminologies MCP to map a column of free-text diagnoses, drugs, or labs to ICD-11/SNOMED/RxNorm/LOINC codes as a committed, reviewable crosswalk.
---

# Harmonize free-text clinical terms to standard codes

Point Claude Code at a column of free-text clinical terms — diagnoses, medications, or lab names — and get back a committed crosswalk mapping each term to a standard code (ICD-11, SNOMED CT, RxNorm, LOINC, ATC), resolved through the [Medical Terminologies MCP](../../catalog/tools/medical-terminologies-mcp.html) with every candidate captured for human review.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Pooling clinical data across studies, sites, or registries stalls on vocabulary. One cohort records diagnoses as free text ("type 2 diabetes mellitus"), another as ICD-10, a third as local codes; medications arrive as brand names, generics, or NDCs; lab panels use lab-specific names instead of LOINC. Before any cross-cohort analysis — an OMOP mapping, a meta-analysis, a trial-eligibility code set — someone has to map every distinct term to a standard concept. Done by hand against six different terminology browsers, it is slow, inconsistent between curators, and undocumented, so the next team redoes it.

"Solved" looks like: hand over a list of distinct terms, get back a crosswalk table — original term, chosen standard code, code system, the matched concept name, and a confidence/needs-review flag — produced by a committed script that calls the terminology services, plus the full candidate list per term so a curator can audit and correct the picks rather than trust a single guess.

## Recommended approach

1. **Install the [Medical Terminologies MCP](../../catalog/tools/medical-terminologies-mcp.html).** It runs over stdio; Claude Code launches it. ICD-11 needs free WHO ICD API credentials ([register here](https://icd.who.int/icdapi)); LOINC, RxNorm, MeSH, and ATC need no auth. SNOMED CT lookup is reference-only without an IHTSDO license.

   ```
   claude mcp add-json medical-terminologies '{"command":"npx","args":["-y","medical-terminologies-mcp"],"env":{"WHO_CLIENT_ID":"your-who-client-id","WHO_CLIENT_SECRET":"your-who-client-secret"}}'
   ```

2. **Stage the distinct terms.** Deduplicate your messy column to a `terms.csv` of distinct strings (with a count, so you can prioritize the high-frequency terms). Decide the target system per term type up front: diagnoses → ICD-11 (or SNOMED if licensed), drugs → RxNorm + ATC, labs → LOINC. State that mapping decision explicitly — it governs which MCP tools get called.

3. **Resolve each term to ranked candidates, not a single answer.** Have Claude drive the MCP per term and capture *all* returned candidates, so the artifact is auditable:

   ```
   Use the medical-terminologies MCP. For every diagnosis term in
   terms.csv, call the ICD-11 search tool and return the top 3
   candidates per term with their code, title, and chapter. For every
   drug term, call RxNorm search and ATC classify and return the top 3
   candidates with code and concept name. Do NOT collapse to one answer
   yet — write candidates.csv with one row per (term, candidate):
   term, count, system, code, concept_name, rank.
   ```

4. **Pick the best match with explicit rules, and flag the uncertain ones.** A crosswalk must distinguish a confident exact match from a guess a human has to check:

   ```
   From candidates.csv build crosswalk.csv with one row per term:
   term, count, chosen_system, chosen_code, chosen_concept,
   match_type (exact | strong | needs_review), n_candidates.
   Mark match_type=exact only when a candidate's concept name matches
   the term case-insensitively; strong when rank 1 is unambiguous;
   needs_review when the top candidates are close or none fit. Never
   invent a code that the MCP did not return.
   ```

5. **Capture the run as a committed artifact.** The MCP calls live external terminology services that version over time, so make the run reproducible and auditable:

   ```
   Write the mapping logic to a script harmonize_terms.py that reads
   terms.csv, calls the MCP tools, and emits candidates.csv and
   crosswalk.csv. Record in provenance.json: the MCP package version,
   the terminology release dates returned by each service (ICD-11,
   RxNorm, LOINC, ATC), the date of the run, the model id, and a sha256
   of terms.csv. Commit harmonize_terms.py, the pinned env, both CSVs,
   and provenance.json.
   ```

   `candidates.csv` is the audit trail; any claim about a mapping must trace to a row in it. Capturing the terminology release dates is essential — codes are added and retired between releases, so a crosswalk is only meaningful against a stated vocabulary version (see the [reproducibility guide](../../guide/advanced/reproducibility.html)).

6. **Curate the `needs_review` rows.** Have a domain expert resolve every `needs_review` term against `candidates.csv`, edit `crosswalk.csv`, and re-commit. The committed crosswalk — not the chat — is what downstream pipelines join against.

## Why this assembly

Rung 2 of the simplicity ladder. One MCP server exposes all the major terminologies (ICD-11, SNOMED CT, LOINC, RxNorm, MeSH, ATC) with search, hierarchy, and cross-mapping through a single install, so a single component does the whole lookup-and-map job. Rung 1 (plain Claude Code) is unsafe here: a model asked to "give the ICD code for X" from memory will confabulate plausible-but-wrong codes, and clinical coding errors propagate silently into every downstream analysis — the MCP grounds every code in an authoritative service. Rung 3+ adds nothing; the only extra discipline (capture candidates, flag uncertainty, pin the vocabulary release) is prompt instruction plus a committed script, not another tool.

## Availability

Fully open. The MCP server is MIT-licensed; RxNorm, LOINC, MeSH, and ATC are freely usable; ICD-11 needs a free WHO API registration. SNOMED CT content is reference-only unless your institution holds an IHTSDO/SNOMED International license — keep SNOMED out of any production crosswalk you don't have a license for, and prefer ICD-11 there. The terms you feed in may be PHI-adjacent; the MCP sends each query string to the upstream terminology APIs, so de-identify the term list (map distinct *concept strings*, not patient-linked rows) before running.

## Compute requirements

Laptop-sufficient. The work is API calls, not computation: each term is one or a few lookups, and the MCP caches and rate-limits internally. A list of a few thousand distinct terms resolves in minutes to tens of minutes, gated by API rate limits rather than CPU. No GPU, no large memory footprint; the output crosswalk is a small CSV.

## Evidence

Proposed. No documented attempt is known of this exact assembly — Claude driving the Medical Terminologies MCP to build a clinical-term crosswalk. The closest evidence is component-level: the MCP exposes the standard, authoritative terminology services (WHO ICD-11, RxNorm, LOINC, ATC) whose mappings are the established basis for clinical data harmonization, and terminology cross-mapping is a documented use case of the server itself. The analogous documented LLM workflow in this cookbook is the [pharmacogenomic dosing report](build-pharmacogenomic-dosing-report.html), where Claude drives clinical reference services (ClinPGx/CPIC) into a committed, provenance-tracked artifact rather than answering from memory. Treat the `match_type=exact` fraction and the expert correction rate on `needs_review` rows as the success criteria to confirm on your own term list.

## Alternatives considered

- **OHDSI Usagi / OMOP Athena (no Claude).** For a full OMOP CDM mapping at scale, the OHDSI ecosystem's purpose-built mapping tools (Usagi for semi-automatic mapping, Athena for the standardized vocabularies) are the heavier, community-standard path. Reach for them when the deliverable is a sanctioned OMOP source-to-concept map; this recipe is the lighter, faster option for ad-hoc harmonization across a handful of systems.
- **PyHealth code utilities (rung 2, narrower).** The [PyHealth skill](../../catalog/tools/pyhealth.html) includes ICD/ATC/NDC/RxNorm lookup and cross-mapping inside a modeling pipeline. Use it when the harmonization is a step *inside* a clinical-ML pipeline you're already building in PyHealth; use this MCP when standalone harmonization (including ICD-11/SNOMED/LOINC) is the whole task.
- **Anthropic `icd-10-codes` connector (rung 2, single-terminology).** If you only need ICD-10-CM/PCS, the [single-terminology connector](../../catalog/tools/icd-10-codes.html) is simpler. This recipe's MCP wins when you need more than one coding system or ICD-11.
- **Claude Code alone (rung 1).** Unsafe — the model confabulates codes. Not viable for any crosswalk that feeds analysis.

## See also

- [Medical Terminologies MCP](../../catalog/tools/medical-terminologies-mcp.html) — unified ICD-11/SNOMED/LOINC/RxNorm/MeSH/ATC lookup and mapping.
- [Extract structured variables from free-text clinical notes](extract-structured-data-from-clinical-notes.html) — the upstream step: produce the distinct terms this recipe harmonizes.
- [PyHealth (Claude Skill)](../../catalog/tools/pyhealth.html) — clinical-ML pipelines with built-in code utilities.
- [Build a pharmacogenomic dosing report](build-pharmacogenomic-dosing-report.html) — the closest documented LLM-driving-clinical-references workflow.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the committed-artifact pattern this recipe follows.

## Sources

- [`SidneyBissoli/medical-terminologies-mcp` (GitHub)](https://github.com/SidneyBissoli/medical-terminologies-mcp) — MCP server source, MIT; verified 2026-06-28 (this run).
- [npm `medical-terminologies-mcp`](https://www.npmjs.com/package/medical-terminologies-mcp) — published package; verified 2026-06-28 (this run).
- [WHO ICD API registration](https://icd.who.int/icdapi) — free ICD-11 credentials; verified 2026-06-28 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=harmonize-clinical-terms-to-standard-codes&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fharmonize-clinical-terms-to-standard-codes.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
