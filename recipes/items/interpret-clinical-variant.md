---
title: Interpret a clinical variant from a natural-language query
parent: All recipes
grand_parent: Recipes
nav_order: 7
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-23
summary: Use BioMCP to convert a free-text variant query ("BRAF V600E", "rs113993960", "NM_004985.5:c.35G>A") into a one-page clinical report with ClinVar significance, population frequency, in-silico predictions, and linked literature.
---

# Interpret a clinical variant from a natural-language query

Hand Claude a variant in whatever notation the source happens to use; get back a single-page report with ClinVar significance, gnomAD frequency, CADD/PolyPhen/SIFT predictions, related ClinicalTrials.gov entries, and a short literature citation block.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Variant interpretation is mostly database choreography: convert the input notation to a canonical identifier, hit MyVariant.info for the consolidated annotation, read off ClinVar significance and gnomAD frequency, sanity-check with in-silico predictors, then pull relevant PubMed and ClinicalTrials.gov records. Every step is fast; the cost is the swivel-chairing across portals and the format-coercion when the input is "BRAF V600E" instead of an HGVS string. Solved looks like: paste any of {rsID, HGVS-c, HGVS-p, gene + protein change}, get one page of cited evidence, no manual format conversion.

## Recommended approach

1. **Install [BioMCP](../../catalog/tools/biomcp.html).** One MCP, one install:

   ```
   uv tool install biomcp-cli
   claude mcp add --transport stdio biomcp -- biomcp run
   ```

2. **Prompt with the variant and the report template.** A minimal version:

   ```
   Build a clinical-grade variant report for: BRAF V600E.

   Use BioMCP. Specifically:
   1. variant_searcher to locate the variant (try gene + hgvsp first;
      if that fails, fall back to genomic coordinates or rsID).
   2. variant_getter for the full MyVariant.info payload.
   3. Extract and tabulate:
        - ClinVar clinical_significance, review_status, last_evaluated
        - gnomAD_exome and gnomAD_genome allele frequency
        - CADD phred, PolyPhen-2 prediction, SIFT prediction
        - Associated conditions from ClinVar
        - Cancer context from cBioPortal (if returned)
   4. pubmed_searcher for the 5 most relevant papers on this variant
      in the last 5 years; return PMIDs and one-line summaries.
   5. trial_searcher with recruiting_status=OPEN and the variant as
      an other_term; return the top 3 trial NCT IDs.

   Render as a single Markdown page. Cite every fact with its source
   database (ClinVar accession, PMID, NCT ID).
   ```

3. **Handle the no-result case.** If `variant_searcher` returns nothing, the input notation likely doesn't match an indexed variant. Re-prompt to convert via gene + protein change (`hgvsp="p.V600E"`) or, if that also fails, drop to genomic coordinates with the assembly explicit (`chromosome="7", start=140453136, end=140453136, assembly="hg38"`).

4. **For oncology workflows, add the trial step explicitly.** The trial search alone is the [trial-matching recipe](match-patient-to-clinical-trials.html); chain it for variant-driven enrollment hunts.

## Why this assembly

Rung 2. One MCP server covers every database the report needs (MyVariant.info, ClinVar via MyVariant.info, gnomAD, CADD, PolyPhen, ClinicalTrials.gov, PubMed). Adding a second component buys nothing. Claude Code alone (rung 1) cannot do this — it has no live database access and will confabulate gnomAD frequencies. A rung-3 toolbelt (separate MyVariant + ClinVar + gnomAD MCPs) is redundant since BioMCP already federates these via MyVariant.info. Rung 4 (Biomni) is overkill for a single-variant report.

## Availability

Fully open. BioMCP is MIT-licensed. MyVariant.info, ClinVar, gnomAD, and ClinicalTrials.gov are public APIs. PubMed access is free; an NCBI API key raises the rate limit but is not required.

## Compute requirements

Laptop-sufficient. All steps are read-only API calls; a single variant report typically completes in under a minute including five PubMed lookups. No GPU.

## Evidence

Proposed. No published benchmark of the exact BioMCP-driven variant-report assembly is known. The closest documented analogue is **MARRVEL-MCP** ([bioRxiv 2025-11-26](https://www.biorxiv.org/content/10.1101/2025.11.26.690887v1)), which equips LLMs with 39 tools spanning gene/variant utilities, pathogenicity databases (dbNSFP, ClinVar, gnomAD), and literature APIs, and benchmarks variant-interpretation accuracy on 45 expert-curated rare-disease tasks; a 20B-parameter model with the MCP reaches 95% accuracy versus 33% without tools. MARRVEL-MCP and BioMCP cover overlapping data sources (ClinVar via different transports, gnomAD, literature), so the MARRVEL-MCP result is the closest evidence that the assembly *class* works. Independent component evidence: MyVariant.info itself is the canonical aggregator behind dozens of published variant pipelines; CADD/PolyPhen/SIFT are standard in-silico predictors. The exact BioMCP-only composition has not been independently benchmarked.

## Alternatives considered

- **MARRVEL-MCP directly.** If the workflow is rare-Mendelian-disease focused and you need MARRVEL's curated cross-species evidence, the MARRVEL-MCP server is purpose-built. It is not currently catalogued in this repo; until it is, BioMCP is the catalogued substitute.
- **Claude Code alone (rung 1).** Insufficient — the model cannot fetch live ClinVar or gnomAD records.
- **Biomni (rung 4).** Worthwhile only if variant interpretation is one step of a larger autonomous loop (e.g., variant → mechanism hypothesis → wet-lab experiment proposal). For a one-shot report, the rung-2 MCP is enough.

## See also

- [BioMCP](../../catalog/tools/biomcp.html)
- [Match a patient summary to recruiting clinical trials](match-patient-to-clinical-trials.html) — chains naturally when the variant is the eligibility driver.
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — the gene-level analogue; switch when the question is "what is this gene" not "what is this variant".
- [Biomni](../../autonomous-science/systems/biomni.html) — autonomous-system option.

## Sources

- [biomcp.org `variant_searcher` documentation](https://biomcp.org/) — verified 2026-05-23 (this run).
- [MyVariant.info API docs](https://docs.myvariant.info/) — verified 2026-05-23 (this run).
- [MARRVEL-MCP preprint (Hyun et al., *bioRxiv*)](https://www.biorxiv.org/content/10.1101/2025.11.26.690887v1) — published 2025-11-28; closest analogous benchmark.

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=interpret-clinical-variant&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Finterpret-clinical-variant.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
