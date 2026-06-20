---
title: Run functional enrichment on a gene list
parent: All recipes
grand_parent: Recipes
nav_order: 23
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-20
summary: Use the gget Claude skill to run a gene list through Enrichr against GO, KEGG, Reactome, and disease libraries, then ask Claude to summarise the enriched terms back to the biology with explicit citations.
---

# Run functional enrichment on a gene list

Hand Claude Code a list of gene symbols (typically the significant hits from a DE analysis or a CRISPR screen); get back an Enrichr-backed enrichment table across GO Biological Process, KEGG, Reactome, and disease libraries, with a short natural-language synthesis of the dominant pathways and citations to the database accessions.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Functional enrichment is the canonical "so what does this gene list mean" step that follows almost every transcriptomics, proteomics, or screen experiment. The mechanics are unglamorous: hit Enrichr (or g:Profiler, or DAVID) with the gene symbols, sort the term tables by adjusted p-value, and translate the top hits into a paragraph a wet-lab collaborator can act on. The cost is the swivel-chairing — exporting the DE table, pasting symbols into a web form, copying tables back into the analysis notebook — and the interpretation pass at the end is where naïve LLM use most often goes wrong: vanilla GPT-4 will name plausible-sounding pathways for almost any gene list, including random ones. Solved looks like: paste a gene-symbol list and the species, get back a single Markdown report with the top enriched terms per library, each cited to its database accession, and a written summary anchored to those tabulated terms — not to the model's prior.

## Recommended approach

1. **Install the [gget Claude Skill](../../catalog/tools/gget.html)** (gget is a Skill, not a marketplace plugin). Skills CLI (recommended), then install the Python package:

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   pip install gget
   ```

   Or clone the collection manually over HTTPS and copy the skill into place:

   ```
   git clone https://github.com/K-Dense-AI/scientific-agent-skills
   cp -r scientific-agent-skills/skills/gget ~/.claude/skills/
   pip install gget
   ```

2. **Hand Claude the gene list and the report contract.** A minimal prompt:

   ```
   I have 187 upregulated genes from a DE run (human, padj<0.05,
   log2FC>1). Use the gget skill to run gget.enrichr on this list
   against the following Enrichr libraries:
     - GO_Biological_Process_2023
     - KEGG_2021_Human
     - Reactome_2022
     - MSigDB_Hallmark_2020
     - DisGeNET
   For each library, return the top 10 terms by adjusted p-value.
   Save each table to results/enrichment/<library>.csv. Then write
   results/enrichment/SUMMARY.md with one paragraph per library
   citing only terms that actually appear in the saved CSVs (term
   name + adjusted p-value + database accession).

   Gene list:
   <paste symbols, one per line>
   ```

   `gget enrichr` calls the Enrichr REST API directly; no API key is needed for typical interactive use.

3. **Verify before believing.** Ask Claude to cross-check every claim in `SUMMARY.md` against the saved CSVs:

   ```
   Re-read results/enrichment/SUMMARY.md. For every pathway or
   disease named, confirm it appears in the corresponding CSV with
   adjusted p-value < 0.05. Flag any sentence whose claim cannot
   be grounded in the tables and rewrite it.
   ```

   This explicit verification pass is the recipe's main hallucination mitigation — it mirrors the design pattern GeneAgent benchmarks (see **Evidence**).

4. **Run a negative-control gene set.** Sample ~200 random protein-coding genes and re-run the same prompt. Any "enrichment" that survives BH correction on the random set is signalling background bias in the library (e.g., long-gene bias in GO) rather than biology. Worth doing once per project, not once per analysis.

5. **For ranked enrichment (GSEA), drop to GSEApy.** `gget enrichr` is over-representation analysis on an unranked hit list. If you have a full ranked DE table and want gene-set enrichment proper (running enrichment score, leading-edge analysis), call GSEApy from the same Claude session — it ships with Enrichr-compatible gene-set libraries via `gp.prerank()`.

6. **Hand off to downstream interpretation.** The CSV tables are the audit trail. Pair with the [build-target-dossier](build-target-dossier.html) recipe when an enriched pathway points back to a specific target you want to characterise next.

## Why this assembly

Rung 2 of the simplicity ladder. The gget skill wraps `gget enrichr` so Claude calls a single function with the right library names and gets back a pandas DataFrame; the model never invents a pathway because the API call is what populates the table. Plain Claude Code (rung 1) would either confabulate Enrichr results or write a one-off requests block against the Enrichr endpoint — fine occasionally but error-prone and not reproducible. A toolbelt (rung 3) buys nothing because the enrichment + interpretation flow is single-source. Rung 4 (autonomous systems) is the wrong tier for a step measured in seconds. The verification pass in step 3 is the explicit hallucination-mitigation pattern; it is the same self-grounding loop that GeneAgent (NIH/Nature Methods 2025) benchmarks at 84% claim support against 1,106 gene sets.

## Availability

Fully open. The gget skill is OSS in [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills); the underlying [`pachterlab/gget`](https://github.com/pachterlab/gget) library is BSD-2-Clause; Enrichr is free for academic and non-profit use. No subscription, no institutional licence. Commercial users should review the [Enrichr terms of service](https://maayanlab.cloud/Enrichr/help#terms) — the API is free to call but the underlying libraries have their own licences (some KEGG mirrors are commercial-restricted).

## Compute requirements

Laptop. The whole workflow is HTTP requests against Enrichr; a 200-gene list across five libraries returns in 10–30 seconds end-to-end. No GPU. Disk is trivial (the CSV tables are a few hundred KB). Rate limits are generous for interactive use but if you batch over hundreds of gene sets, throttle to ~1 request/second to stay within Enrichr's etiquette.

## Evidence

Reported. The strongest reference for the assembly *class* is **GeneAgent** ([Wang et al., *Nature Methods* 22:1677, 2025, DOI:10.1038/s41592-025-02748-6](https://doi.org/10.1038/s41592-025-02748-6); [PMID 40721871](https://pubmed.ncbi.nlm.nih.gov/40721871/)), a self-verification LLM agent that queries Enrichr and other curated databases to ground gene-set claims; across 1,106 gene sets it lifted ROUGE-L on MSigDB from 0.239 ± 0.038 (GPT-4 alone) to 0.310 ± 0.047 (GeneAgent), with 84% of 15,848 generated claims supported by database evidence and 92% of self-verification decisions judged correct by two human experts on a 132-claim sample. The recipe here is a smaller-grain composition (one skill, no autonomous loop) but the underlying database-grounding pattern is the same. Complementary anchors: [Hu et al., *Nature Methods* 21:2353, 2024 — "Evaluation of large language models for discovery of gene set function" (DOI:10.1038/s41592-024-02525-x)](https://doi.org/10.1038/s41592-024-02525-x) shows GPT-4 names common gene-set functions with high specificity but only when grounded against a database; [Joshi et al., *llm2geneset* preprint 2024-11 (DOI:10.1101/2024.11.11.621189)](https://doi.org/10.1101/2024.11.11.621189) shows LLM-generated gene sets can be used as Enrichr-compatible inputs. No peer-reviewed benchmark of "Claude + gget skill + Enrichr" against hand-written `gget enrichr` code is known — the agent loop adds reproducibility and the verification pass, not new statistics.

### Field reports

- **2026-06-20 (@goodb, #41):** Used as the enrichment leg of a knee-OA disease → genes → pathways chain (Open Targets prioritisation → gget/Enrichr) and ran end-to-end on a laptop in under a minute. The original install block was wrong (it pointed at a non-existent `K-Dense-AI/claude-scientific-skills` marketplace); the `npx skills add` / manual-HTTPS-clone paths above now match the [catalog page](../../catalog/tools/gget.html) and the manual clone is confirmed working.

## Alternatives considered

- **Plain Claude Code with the Enrichr REST API.** Works for one-off analyses but the model has to re-derive the right `userListId` ⇒ `enrich` flow and the right library shortnames each time, and is less likely to retain the per-library result tables in a reproducible form. Reach for it only when the gget skill isn't installed and the analysis is throwaway.
- **GSEApy directly.** [GSEApy](https://gseapy.readthedocs.io/) covers Enrichr over-representation, ranked GSEA, single-sample GSEA, and Biomart conversions in one Python package. It is the right answer when the analysis is ranked-list GSEA (step 5) or batched across hundreds of gene sets. It is not yet wrapped as a Claude skill in the catalog, so calls fall back to plain Claude + Python.
- **g:Profiler / WebGestalt.** Both are stronger than Enrichr on some libraries (g:Profiler has tighter multi-test correction; WebGestalt has better term-grouping). Neither has a Claude skill in the catalog; if you need them, drop to plain Claude + the respective REST APIs. Consider proposing skill wrappers if this becomes routine.
- **GeneAgent directly.** [`ncbi-nlp/GeneAgent`](https://github.com/ncbi-nlp/GeneAgent) is publicly available; reach for it when the deliverable is *gene-set naming* with verified evidence claims (the use case the paper benchmarks) rather than a tabular enrichment report. It is not yet catalogued as a Claude skill.
- **An autonomous-science system (Biomni).** Overkill for a single enrichment step. Biomni includes Enrichr-class tools alongside dozens of others; reach for it only when enrichment is one node in a larger autonomous loop.

## See also

- [gget (Claude Skill)](../../catalog/tools/gget.html)
- [Run bulk RNA-seq differential expression from a counts matrix](run-bulk-rnaseq-differential-expression.html) — the upstream step that produces the gene list this recipe interprets.
- [Map a disease to its implicated genes and pathways](map-disease-to-genes-and-pathways.html) — supplies this recipe's gene list from a disease association ranking.
- [Infer a gene-regulatory network from single-cell RNA-seq](infer-gene-regulatory-network-from-scrnaseq.html) — alternative downstream interpretation of a DE result.
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — drill into one enriched gene at a time.
- [Biomni](../../autonomous-science/systems/biomni.html) — autonomous-system alternative.

## Sources

- [Wang Z. et al., "GeneAgent: self-verification language agent for gene-set analysis using domain databases," *Nature Methods* 22:1677–1685, 2025](https://doi.org/10.1038/s41592-025-02748-6) — published 2025-07; verified 2026-06-04 (this run).
- [Hu M. et al., "Evaluation of large language models for discovery of gene set function," *Nature Methods* 21:2353–2360, 2024 (DOI:10.1038/s41592-024-02525-x)](https://doi.org/10.1038/s41592-024-02525-x) — published 2024-12.
- [Joshi M. et al., "llm2geneset: leveraging LLMs to dynamically generate gene sets," bioRxiv 2024-11-12 (DOI:10.1101/2024.11.11.621189)](https://doi.org/10.1101/2024.11.11.621189) — posted 2024-11-12.
- [gget documentation — `gget enrichr`](https://pachterlab.github.io/gget/en/enrichr.html) — verified 2026-06-04 (this run).
- [Enrichr help and terms](https://maayanlab.cloud/Enrichr/help) — verified 2026-06-04 (this run).
- [`K-Dense-AI/scientific-agent-skills` — gget skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/gget/SKILL.md) — verified 2026-06-04 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=run-functional-enrichment-on-a-gene-list&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Frun-functional-enrichment-on-a-gene-list.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
