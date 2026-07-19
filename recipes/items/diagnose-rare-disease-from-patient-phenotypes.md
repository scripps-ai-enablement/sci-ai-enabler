---
title: Diagnose a rare disease from patient phenotypes
parent: All recipes
grand_parent: Recipes
nav_order: 22
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine, Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-19
summary: Use the ToolUniverse Rare Disease Diagnosis skill to turn a patient's HPO phenotypes and candidate variants into a tiered, ACMG-aligned differential with prioritized genes.
---

# Diagnose a rare disease from patient phenotypes

Hand Claude a patient's clinical presentation (and any candidate variants); get back a tiered differential diagnosis — HPO-matched candidate diseases, prioritized genes, and ACMG-aligned variant reasoning — with every claim cited to a database.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine, Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Undiagnosed-disease programs and clinical geneticists face the same bottleneck for every rare-disease case: match a patient's phenotype to the right disease and the right causal gene across dozens of heterogeneous evidence sources (HPO, Orphanet, OMIM, ClinVar, gnomAD, GTEx), then reason about each candidate variant under ACMG criteria. Each lookup is fast; the cost is the swivel-chairing across portals and the hours of manual synthesis into an auditable report. Plain LLMs are a trap here — without live database access they hallucinate gene–disease links and pathogenicity calls (GPT-4 reaches only 16% top-hit accuracy on phenotype-driven gene prioritization; [Kim et al., 2024](https://arxiv.org/abs/2403.14801)). Solved looks like: paste HPO terms (plus optional variant list), get a tiered differential with prioritized genes and cited, ACMG-aligned reasoning per candidate.

## Recommended approach

1. **Install ToolUniverse, then the Rare Disease Diagnosis skill.** The skill drives ToolUniverse tool calls, so the MCP server must be registered first:

   ```
   claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
   npx skills add mims-harvard/ToolUniverse
   ```

   See the [ToolUniverse](../../catalog/tools/tooluniverse.html) and [Rare Disease Diagnosis skill](../../catalog/tools/tooluniverse-rare-disease-diagnosis.html) catalog pages for details. The skill sets `disable-model-invocation: true`, so invoke it explicitly.

2. **Capture the case in a versioned input file, not the chat.** Put the phenotype and candidate variants in a committed `case.yaml` so the run is re-runnable and auditable:

   ```yaml
   patient_id: UDN-0042
   hpo_terms: [HP:0001250, HP:0001263, HP:0000252]   # seizures, dev. delay, microcephaly
   inheritance: de novo suspected
   candidate_variants:
     - NM_004992.4:c.916C>T   # MECP2
     - NM_003159.3:c.2T>C     # CDKL5
   ```

3. **Invoke the skill against the file.** A minimal prompt:

   ```
   Use the rare-disease-diagnosis skill on case.yaml. Produce a tiered
   (T1-T4) differential:
   1. HPO_search_terms to confirm/normalize the phenotype terms.
   2. Orphanet/OMIM/DisGeNET to list candidate diseases + genes.
   3. Prioritize genes with MARRVEL, ClinGen validity, and GTEx tissue
      expression consistent with the phenotype.
   4. For each candidate variant, interpret under ACMG using ClinVar,
      gnomAD frequency, and EVE/SpliceAI predictions.
   5. Write the report to reports/UDN-0042.md, and dump the raw tool
      outputs (disease hits, gene scores, variant annotations) to
      results/UDN-0042.json. Cite every claim (accession, PMID).
   ```

4. **Emit a provenance record.** Because every step calls live services (Orphanet, ClinVar, gnomAD via ToolUniverse), the run is not byte-reproducible — capture what moves. Have the assistant write `provenance.json` recording: `tooluniverse` version, skill commit, each database's query date, ClinVar/gnomAD release accessions returned, input `case.yaml` sha256, and the model id. Commit `case.yaml`, `reports/`, `results/`, and `provenance.json` together. See the [reproducibility guide](../../guide/advanced/reproducibility.md) for the pattern.

The durable artifact is the committed case file, the tiered report, the raw `results/*.json` audit trail, and the provenance record — re-runnable for any future patient by editing `case.yaml`.

## Why this assembly

Rung 2. A single skill federates every database the differential needs (HPO, Orphanet, OMIM, DisGeNET, MARRVEL, ClinGen, GTEx, ClinVar, gnomAD, EVE, SpliceAI) and encodes the phenotype→disease→gene→variant reasoning order. Claude Code alone (rung 1) fails — it has no live access and confabulates gene–disease links and pathogenicity calls. A rung-3 toolbelt wiring each database as a separate MCP is redundant since ToolUniverse already consolidates them. Rung 4 (an autonomous system) adds loop overhead without extra capability for a one-case differential.

## Availability

Fully open. ToolUniverse and its skills are OSS (Apache-2.0); HPO, Orphanet, DisGeNET, ClinVar, gnomAD, GTEx, and MARRVEL are public. **Caveat:** full OMIM content requires a free registered account/license; without it, OMIM lookups return limited data (Orphanet/DisGeNET still cover most candidates). Outputs are decision-support reasoning, not a clinical diagnosis — a qualified clinician must review. Use only de-identified phenotype/variant data.

## Compute requirements

Laptop-sufficient. All steps are read-only API calls; a single case with a handful of HPO terms and candidate variants typically completes in a few minutes. No GPU. Output is small (a Markdown report plus a JSON audit file).

## Evidence

Reported. No published benchmark of this exact ToolUniverse-skill assembly on rare-disease diagnosis is known, but the assembly *class* — a knowledge-grounded LLM layer over the same MARRVEL/ClinVar/gnomAD tool stack — is well documented. **LA-MARRVEL** ([Lee et al., *arXiv* 2511.02263, 2025-11, updated 2026-03](https://arxiv.org/abs/2511.02263)) reports a **12–15 percentage-point absolute improvement in Recall@1** for phenotype-driven gene prioritization over established tools across three real-world cohorts, delivering ACMG-aligned reasoning per candidate — the same design the ToolUniverse skill implements. The contrast case establishes why rung 1 fails: database-free LLMs reach only ~16% top-hit accuracy ([Kim et al., 2024](https://arxiv.org/abs/2403.14801)), well below traditional bioinformatics tools. The MARRVEL-MCP variant-interpretation benchmark ([bioRxiv, 2025-11-28](https://www.biorxiv.org/content/10.1101/2025.11.26.690887v1)) reaches 95% accuracy on 45 expert-curated tasks with tools versus 33% without, corroborating that tool grounding is what carries the workflow. The ToolUniverse rare-disease skill composition itself has not been separately benchmarked.

## Alternatives considered

- **Interpret a single clinical variant ([interpret-clinical-variant](interpret-clinical-variant.html)).** When you already know the gene/variant and just need a one-page report (ClinVar significance, gnomAD frequency, in-silico calls), that rung-2 BioMCP recipe is simpler. Reach for *this* recipe when the input is a phenotype and the question is "which disease and which gene," not "what does this one variant mean."
- **MARRVEL-MCP directly.** Purpose-built for Mendelian-disease variant interpretation with a published 95%-accuracy benchmark, but it is not yet catalogued in this repo; until it is, the ToolUniverse rare-disease skill is the catalogued substitute.
- **An autonomous-science system (rung 4).** Worthwhile only if diagnosis is one step of a larger autonomous loop (phenotype → diagnosis → mechanism → experiment proposal). For a one-case differential, the rung-2 skill is enough.

## See also

- [Rare Disease Diagnosis (ToolUniverse Claude Skill)](../../catalog/tools/tooluniverse-rare-disease-diagnosis.html)
- [ToolUniverse](../../catalog/tools/tooluniverse.html)
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — the single-variant sibling; switch when you already know the variant.
- [Score point mutations for functional impact with a protein language model](score-protein-variants-with-esm.html) — the database-free sibling for novel substitutions with no annotation.
- [Match a patient summary to recruiting clinical trials](match-patient-to-clinical-trials.html) — chains naturally once a candidate diagnosis is in hand.

## Sources

- [ToolUniverse Rare Disease Diagnosis skill (`SKILL.md`)](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-rare-disease-diagnosis/SKILL.md) — verified 2026-07-19 (this run).
- [Lee et al., "LA-MARRVEL," *arXiv* 2511.02263](https://arxiv.org/abs/2511.02263) — published 2025-11-04, updated 2026-03-05; closest analogous benchmark (+12–15 pp Recall@1).
- [Kim et al., "Assessing the Utility of LLMs for Phenotype-Driven Gene Prioritization," *arXiv* 2403.14801](https://arxiv.org/abs/2403.14801) — published 2024-03-21; rung-1 failure baseline (GPT-4 16%).
- [MARRVEL-MCP preprint, *bioRxiv*](https://www.biorxiv.org/content/10.1101/2025.11.26.690887v1) — published 2025-11-28; tool-grounding benchmark (95% vs 33%).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=diagnose-rare-disease-from-patient-phenotypes&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdiagnose-rare-disease-from-patient-phenotypes.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
