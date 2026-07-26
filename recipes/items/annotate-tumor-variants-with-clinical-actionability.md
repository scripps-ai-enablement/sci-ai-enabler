---
title: Annotate tumor somatic variants with clinical actionability evidence
parent: All recipes
grand_parent: Recipes
nav_order: 4
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine, Drug Repurposing and Discovery, Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Institutional access
compute_requirements: Laptop
last_verified: 2026-07-26
summary: Use the CIViC connector to match a tumor's somatic variant list to predictive/prognostic/diagnostic clinical evidence and produce an AMP/ASCO/CAP-tiered, cited actionability table for a molecular tumor board.
---

# Annotate tumor somatic variants with clinical actionability evidence

Hand Claude a tumor's called somatic variants and get back a tiered, cited table of what each variant means for therapy, prognosis, and diagnosis — matched against the CIViC clinical-interpretation knowledgebase and formatted the way a molecular tumor board reads it.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine, Drug Repurposing and Discovery, Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Institutional access |
| **Compute** | Laptop |

## Problem

A tumor NGS panel returns a list of somatic single-nucleotide variants, indels, and fusions. Before a molecular tumor board (MTB) can act on them, someone has to annotate each variant with its *clinical* significance — is there an FDA-approved or guideline therapy predicted to respond (or resist), a prognostic association, a diagnostic assignment? — and assign a tier under the AMP/ASCO/CAP framework (Tier I strong significance, Tier II potential, Tier III unknown). This is database choreography across curated knowledgebases, and it is the recognized bottleneck in precision oncology: the annotation step is manual, slow, and error-prone, and the field's knowledgebases have inconsistent programmatic access ([Borchert et al., *Brief. Bioinform.* 2021](https://pubmed.ncbi.nlm.nih.gov/33971666/); [Lutz et al., *Target. Oncol.* 2025](https://pubmed.ncbi.nlm.nih.gov/39609355/)).

"Solved" looks like: paste the variant list, get back one row per variant with the CIViC evidence type (Predictive / Prognostic / Diagnostic / Predisposing / Oncogenic), the associated therapy or outcome, the evidence level (A professional guideline → E preclinical), the source citation, and a suggested AMP tier — saved as a committed, reviewable table the MTB curator signs off on.

## Recommended approach

1. **Enable the [CIViC connector](../../catalog/tools/civic.html).** In Claude Science, turn on the *Clinical Genomics* featured connector (it bundles CIViC alongside ClinGen and Open Targets). CIViC data is CC0 and read-only. For programmatic access outside Claude Science, the same content is at [civicdb.org/api/graphql](https://civicdb.org/api/graphql).

2. **Stage the variant list.** One tumor per file — `variants.tsv` with a stable canonical notation per row (gene + HGVS-p or HGVS-c, plus variant type: SNV / indel / fusion / CNV). Normalize notation first if your caller emits mixed formats; CIViC matches on gene + variant, so a clean identifier is the difference between a hit and a silent miss.

3. **Match each variant and capture the result to a committed table.** Have Claude write a driver rather than annotating interactively so the run is re-runnable:

   ```
   For each variant in variants.tsv, query the CIViC connector for
   clinical evidence. Write a script annotate_actionability.py that:
     - queries CIViC for each gene+variant,
     - emits actionability.csv with one row per (variant, evidence item):
         gene, variant, variant_type, civic_evidence_type
         (Predictive/Prognostic/Diagnostic/Predisposing/Oncogenic),
         disease, therapy_or_outcome, evidence_level (A-E),
         evidence_direction, clinical_significance, citation (PMID/DOI),
         civic_evidence_id,
     - adds a suggested_amp_tier column (I / II / III) with a one-line
       rationale per the AMP/ASCO/CAP framework,
     - records the CIViC data-release date, the connector identity,
       a sha256 of variants.tsv, and library versions in provenance.json.
   Then summarize: which variants have Level A/B evidence, which are
   Tier I, and which returned no CIViC match (Tier III candidates).
   ```

   Pin the environment (`requirements.txt`) and commit `annotate_actionability.py`, the pinned env, and `provenance.json`. Because CIViC is versioned and grows continuously (>3,200 variants across >470 genes as of the 2022 release, still expanding), the recorded release date + input hash are what make the annotation auditable and re-attemptable — see the [reproducibility guide](../../guide/advanced/reproducibility.html).

4. **Review before the board.** The AMP tier and CIViC evidence level are decision support, not a sign-off. A curator confirms each Tier I/II call against the stated citation, checks the disease context matches the patient's tumor (a `Predictive` item for melanoma may not apply to colorectal), and flags "no CIViC match" variants for a wider knowledgebase check. Do not let the model assert a therapy association that is not in the emitted `citation` column.

5. **Hand off.** `actionability.csv` is the annotation record the MTB reads and the file that seeds trial matching — feed the actionable variants into [match a patient to clinical trials](match-patient-to-clinical-trials.html). For a germline single-variant question (pathogenicity, population frequency), use [interpret a clinical variant](interpret-clinical-variant.html) instead; this recipe is the somatic, therapy-oriented counterpart.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged connector covers the whole match step. The value is in CIViC's expert-moderated, cited clinical evidence and its structured evidence-type/level schema, none of which plain Claude Code (rung 1) can reproduce credibly from prompt knowledge: unaided, the model will invent therapy associations and evidence levels, which is exactly the failure mode a tumor board cannot tolerate. Rung 3+ is unnecessary for the single-knowledgebase match — CIViC is the canonical open source and answers every column in the target table. A fuller MTB pipeline that fuses CIViC with OncoKB, COSMIC, and ClinVar is a multi-tool harness; escalate to it only when a single knowledgebase leaves too many variants unmatched.

## Availability

Institutional access. CIViC data itself is CC0 and free, but the recommended path enables it through Claude Science's *Clinical Genomics* featured connector, which requires a Claude Science-eligible account. The public GraphQL API is fully open if you wrap it yourself. Handling patient variant data is subject to your institution's governance (IRB, data-use agreements, PHI handling) — the variant list should be de-identified before it leaves a controlled environment.

## Compute requirements

Laptop-sufficient. Annotation is a series of small API queries and table joins — CPU-only, seconds to a couple of minutes for a typical panel of tens of variants. No GPU. CIViCpy benchmarks annotation at >1,200 variants/second against the knowledgebase, so even whole-exome-scale lists are laptop-scale.

## Evidence

Reported. CIViC is one of the most-used knowledgebases in the standard MTB annotation workflow and is explicitly identified as such in reviews of precision-oncology variant interpretation ([Borchert et al., *Brief. Bioinform.* 2021](https://pubmed.ncbi.nlm.nih.gov/33971666/); [Lutz et al., *Target. Oncol.* 2025](https://pubmed.ncbi.nlm.nih.gov/39609355/)). The knowledgebase's four+ evidence types (Predictive, Prognostic, Diagnostic, Predisposing, Oncogenic, Functional) and A–E evidence-level scheme are the exact fields this recipe emits ([Krysiak et al., *Nucleic Acids Res.* 2023 — CIViCdb 2022](https://pubmed.ncbi.nlm.nih.gov/36373660/)). The programmatic match step is quantitatively characterized: CIViCpy matched CIViC Level A (professional guideline) or B (clinical trial) evidence to **38.6% of 59,437 tumors** in AACR Project GENIE, annotating >1,200 variants/second ([Wagner et al., *JCO Clin. Cancer Inform.* 2020](https://pubmed.ncbi.nlm.nih.gov/32191543/)).

No head-to-head benchmark of this *Claude+CIViC* assembly versus a manual CIViC lookup or CIViCpy is published — the connector buys a cited, tiered, committed table and a re-runnable driver, not a new matching method. That gap, plus the human-review requirement before clinical use, is why this recipe is `Reported`, not `Validated`.

## Alternatives considered

- **CIViC web app or CIViCpy directly (no connector).** For a one-off lookup of a single variant, the [CIViC web app](https://civicdb.org/) is the simplest path; for scripted batch annotation, CIViCpy is the field-standard SDK. Reach for the connector when you want the match, the AMP tiering, and a committed provenance-tracked table produced in one place alongside your other Claude workflows.
- **Germline variant interpretation (rung 2, different question).** [Interpret a clinical variant](interpret-clinical-variant.html) answers "is this variant pathogenic?" via ClinVar/gnomAD/in-silico predictors — the germline diagnostic axis. This recipe answers "what therapy does this somatic variant predict?" — the oncology-treatment axis. Use both for a tumor with a suspected germline component.
- **Multi-knowledgebase MTB harness (rung 3).** When single-knowledgebase coverage leaves too many Tier III variants, fusing CIViC with OncoKB, COSMIC, and ClinGen raises match rate — but no cataloged component wires all of these into one Claude tool today, so it stays a manual escalation. Note it as a limitation, not a step in this recipe.

## See also

- [CIViC (Claude Science Connector)](../../catalog/tools/civic.html) — crowd-curated clinical interpretations of cancer variants.
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — the germline pathogenicity counterpart.
- [Match a patient to clinical trials](match-patient-to-clinical-trials.html) — downstream of the actionable-variant shortlist.
- [Detect somatic CNVs from tumor sequencing](detect-somatic-cnvs-from-tumor-sequencing.html) — the copy-number side of the same tumor profile.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the committed-artifact pattern this recipe follows.

## Sources

- [Wagner et al., "CIViCpy: A Python Software Development and Analysis Toolkit for the CIViC Knowledgebase," *JCO Clin. Cancer Inform.* 4:245–253](https://pubmed.ncbi.nlm.nih.gov/32191543/) — published 2020; verified 2026-07-26 (this run). 38.6% Level A/B match across 59,437 GENIE tumors; >1,200 variants/s.
- [Krysiak et al., "CIViCdb 2022: evolution of an open-access cancer variant interpretation knowledgebase," *Nucleic Acids Res.* 51(D1):D1230–D1241](https://pubmed.ncbi.nlm.nih.gov/36373660/) — published 2023; verified 2026-07-26 (this run). Evidence types and A–E level scheme.
- [Borchert et al., "Knowledge bases and software support for variant interpretation in precision oncology," *Brief. Bioinform.* 22(6):bbab134](https://pubmed.ncbi.nlm.nih.gov/33971666/) — published 2021; verified 2026-07-26 (this run). CIViC among most-used MTB knowledgebases.
- [Lutz et al., "Unveiling the Digital Evolution of Molecular Tumor Boards," *Target. Oncol.* 20:1–15](https://pubmed.ncbi.nlm.nih.gov/39609355/) — published 2025; verified 2026-07-26 (this run). MTB annotation workflow and common knowledgebases.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=annotate-tumor-variants-with-clinical-actionability&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fannotate-tumor-variants-with-clinical-actionability.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
