---
title: Triage GWAS lead SNPs to candidate drug targets
parent: All recipes
grand_parent: Recipes
nav_order: 74
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-12
summary: Drive GWAS-MCP to annotate a list of GWAS lead SNPs — variant consequence, eQTL-implicated genes, GWAS Catalog trait context, and drug-target/tractability support — into a cited variant-to-target triage table.
---

# Triage GWAS lead SNPs to candidate drug targets

You have a handful of genome-wide-significant lead SNPs from a GWAS or a published locus table; get back a cited table that maps each variant to its implicated gene(s), the traits already reported at that locus, and whether the gene is a tractable or precedented drug target — the first-pass "which of these loci are worth chasing as targets" read.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A GWAS hands you loci, not targets. After the Manhattan plot, the translational question is: *of these lead SNPs, which point at a gene we could actually drug?* Answering it by hand means, per SNP, looking up the variant consequence, checking which gene the locus regulates (rarely the nearest one), pulling the other traits reported at that locus from the GWAS Catalog, and then asking whether that gene has any tractability or clinical precedent. Genetically-supported targets roughly double the odds of clinical success, so this triage is where a lot of translational value is decided — but stitching four public databases per SNP across a locus table is slow and error-prone, and asking a chatbot from memory fabricates rsID-to-gene mappings.

Solved looks like: drop in a list of rsIDs (or a locus table), get back one cited row per variant — consequence, eQTL-implicated gene(s), co-reported traits, and drug-target support — as a versioned CSV you can hand to the target-nomination meeting.

## Recommended approach

1. **Install [GWAS-MCP](../../catalog/tools/gwas-mcp.html)** — one MCP server wrapping variant, eQTL, GWAS Catalog, and drug-target lookups across 14 public databases:

   ```
   pip install gwas-mcp
   claude mcp add --transport stdio gwas-bioinformatics -- python -m gwas_mcp.server
   ```

   Confirm it registers with `claude mcp list`. No API key is needed; responses cache for one hour.

2. **Pin your input.** Put the lead SNPs in a version-controlled `leads.csv` (`rsid,chr,pos,risk_allele,pvalue,trait`) and hash it so the run is auditable. This is the durable input the whole triage keys off.

3. **Drive the per-variant triage with one prompt**, forcing every field through a GWAS-MCP call rather than memory:

   ```
   Use the gwas-bioinformatics MCP tools. For each rsID in leads.csv, do NOT
   answer from prior knowledge — every field must come from a tool call:
     - get_variant_info / annotate_snps: most severe consequence, nearest gene,
       and the gene(s) it maps to.
     - get_eqtl_data: any gene whose expression this variant is an eQTL for,
       with the tissue. Prefer eQTL-implicated genes over nearest-gene when
       they disagree, and say so.
     - query_gwas_catalog: other traits/diseases already reported at or near
       this locus (report trait + study accession).
     - get_drug_targets / search_open_targets: for each implicated gene, is it
       a known/tractable drug target? Report tractability bucket and any
       clinical-stage compound.
   Emit one CSV row per rsID: rsid, consequence, nearest_gene,
   eqtl_gene(tissue), co_reported_traits, implicated_gene, tractability,
   precedent_drug, source_ids. Write it to targets_triage.csv. Add an explicit
   "no eQTL / no drug-target evidence found" note where a lookup is empty.
   ```

4. **Capture the run in a script + provenance, not a chat.** Have Claude write the orchestration to a committed `triage_gwas_leads.py` (reads `leads.csv`, calls the MCP tools, writes `targets_triage.csv`) plus a `provenance.json` recording: `gwas-mcp` version, the release/snapshot **date** of each queried database (GWAS Catalog, GTEx/eQTL, Open Targets), the `leads.csv` sha256, the run date, and the model id. Pin the environment with a `requirements.txt` (`gwas-mcp==<version>`). The CSV + provenance are the audit trail; the chat is only how they were authored.

5. **Read it as a triage queue.** Rank by tractability + precedent, flag loci where the eQTL gene differs from the nearest gene (the interesting cases), and route the top rows to the target-nomination step. Save the prompt as `/gwas-triage <leads.csv>` for reuse on the next locus table.

## Why this assembly

Rung 2 of the simplicity ladder, and it stops there. The whole task is a per-variant cross-database join, and a single MCP server (GWAS-MCP) exposes every source the join needs — variant annotation, eQTL, GWAS Catalog, and drug-target lookups — so Claude supplies only the loop and the write-up. Rung 1 (Claude alone, from memory) is the discouraged path: rsID-to-gene mappings and eQTL links are exactly what a bare model fabricates. Rung 3 (adding UniProt/AlphaFold/DepMap) turns the triage into a full [target dossier](build-target-dossier.html) — a different, deeper question you ask *after* this triage narrows the list, not before. Note the scope line: this recipe does the **lookup-and-annotate** layer; formal causal inference (colocalization, Mendelian randomization) is out of scope — see *Alternatives considered*.

## Availability

Fully open. GWAS-MCP is OSS (MIT) and wraps public, no-auth REST APIs (Ensembl, ClinVar, GWAS Catalog, GTEx eQTL, Open Targets, PharmGKB, and more). No subscription, key, or institutional account is required for the public data shown here. Data caveat: this is research-grade evidence for target triage, not a clinical or regulatory determination.

## Compute requirements

Laptop. Every step is a read-only REST call plus light local Python (row assembly). Wall-clock is dominated by tool-calling latency: a 10-SNP table with four lookups each typically triages in 2–5 minutes; a 50-SNP table in 8–15 minutes. No GPU; the CSV output is a few hundred KB. The 1-hour response cache keeps re-runs on the same loci fast.

## Evidence

Reported. The workflow *class* — mapping GWAS loci to causal genes and then to therapeutic targets by integrating variant annotation, eQTL evidence, and drug-target databases — is documented with quantitative results by [Lessard et al., *BMC Genomics* 25:1156 (2024)](https://pubmed.ncbi.nlm.nih.gov/39563277/): across 4,611 disease GWAS from FinnGen, Estonian Biobank, and UK Biobank, multi-omics evidence (variant annotation + activity-by-contact + eQTL) enriched for approved therapeutic targets far more than nearest-gene mapping (risk ratio 2.58 vs 1.75 for the highest-support genes), and predicted directionality matched approved-drug mechanism of action in >85% of cases. The underlying premise — that genetically-supported targets succeed in the clinic roughly twice as often — is the field's founding result ([Nelson et al., *Nat. Genet.* 47:856 (2015)](https://pubmed.ncbi.nlm.nih.gov/26121088/); reconfirmed by [King et al., *PLoS Genet.* 15:e1008489 (2019)](https://pubmed.ncbi.nlm.nih.gov/31830040/)). GWAS-MCP faithfully wraps the same public databases (GWAS Catalog, GTEx eQTL, Open Targets) these studies used. No peer-reviewed benchmark of the Claude-plus-GWAS-MCP composition specifically is known, so this is `Reported`: the assembly reproduces a documented, quantitatively-validated workflow's lookup layer, but the agent orchestration is not separately benchmarked.

## Alternatives considered

- **Formal colocalization / Mendelian randomization (rung 3+, different tooling).** Lessard et al. use colocalization and MR to establish *causality* and *directionality* — steps that need summary-statistic-level statistical tools (`coloc`, `TwoSampleMR`), not lookup APIs. GWAS-MCP does not expose these, so this recipe deliberately stops at the annotation layer. Reach for a dedicated coloc/MR pipeline when you have full summary statistics and need a causal, directional call rather than a triage shortlist. (Surfaced as a missing catalog component.)
- **[Prioritize targets within a disease via Open Targets](prioritize-targets-within-a-disease.html) (rung 2).** That recipe starts from a *disease* and ranks its associated genes top-down. This one starts from *your own GWAS loci* and works variant-up. Use that one when you have an indication but no locus list; use this one when the GWAS is what you have in hand.
- **[Build a target dossier](build-target-dossier.html) (rung 3).** The natural next step: once this triage names one or two genes worth chasing, build the deep four-source dossier on each. Don't run the dossier across every SNP — triage first, then drill.
- **Claude Code alone (rung 1).** Insufficient — fabricates rsID-to-gene and eQTL links.

## See also

- [GWAS-MCP](../../catalog/tools/gwas-mcp.html)
- [Prioritize targets within a disease via Open Targets](prioritize-targets-within-a-disease.html) — the disease-first complement.
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — deep drill-down on a triaged gene.
- [Run a GWAS on case-control genotype data](run-gwas-on-case-control-genotypes.html) — the upstream step that produces the lead SNPs.
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — single-variant clinical-significance sibling.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the artifact-and-provenance pattern this recipe follows.

## Sources

- [Lessard et al., "Leveraging large-scale multi-omics evidences to identify therapeutic targets from genome-wide association studies," *BMC Genomics* 25:1156 (2024)](https://pubmed.ncbi.nlm.nih.gov/39563277/) — published 2024; verified 2026-07-12 (this run).
- [Nelson et al., "The support of human genetic evidence for approved drug indications," *Nat. Genet.* 47:856 (2015)](https://pubmed.ncbi.nlm.nih.gov/26121088/) — founding genetic-support result.
- [King et al., "Are drug targets with genetic support twice as likely to be approved?" *PLoS Genet.* 15:e1008489 (2019)](https://pubmed.ncbi.nlm.nih.gov/31830040/) — reconfirmation.
- [`zaeyasa/gwas-mcp`](https://github.com/zaeyasa/gwas-mcp) — GWAS-MCP tool surface; verified 2026-07-12 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=triage-gwas-hits-to-drug-targets&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftriage-gwas-hits-to-drug-targets.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
