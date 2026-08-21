---
title: Interpret variants that gain or lose glycosylation sites
parent: All recipes
grand_parent: Recipes
nav_order: 16
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine, Molecular and Cellular Biology]
evidence_level: Reported
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-16
summary: Flag coding variants that destroy or create N-/O-glycosylation sites with the GlyGen MCP, join to accession-keyed AlphaMissense (ProtVar) and ClinVar (BioMCP), and emit a ranked, provenance-tracked candidate table.
---

# Interpret variants that gain or lose glycosylation sites

Hand Claude a list of protein-coding variants; get back a ranked, cited table of the ones predicted to destroy an existing glycosylation site (loss of glycosylation, LOG) or create a new one (gain of glycosylation, GOG), joined to ClinVar/AlphaMissense annotations and an expression sanity-check.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine, Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Altered glycosylation is a recurring, under-scanned disease mechanism: a missense change can knock out an N-X-S/T sequon (X ≠ P) that normally carries a glycan, or introduce a novel one, and either can shift protein stability, secretion, or receptor signaling. Two textbook cases: a sequon mutation at Asn135 in antithrombin/`SERPINC1` (P01008) reduces circulating antithrombin (LOG), and `IFNGR2` Thr168Asn (P38484) creates a novel N-glycan that causes Mendelian susceptibility to mycobacterial disease (GOG). The work is tedious and error-prone by hand — you must map each variant onto the *canonical Swiss-Prot* protein coordinate (numbering differs across databases and publications; the antithrombin site is Asn135 in one frame, Asn167 in the reference), check whether the mutated residue sits on or near a known glycosite, then cross-reference clinical and pathogenicity annotations. Solved looks like: hand over a variant list, get back a ranked table of glycosylation-altering variants with clinical/functional annotations, an expression check, and a re-runnable provenance record.

## Recommended approach

This is a two-MCP toolbelt plus one REST call: **[GlyGen MCP](../../catalog/tools/glygen.html)** supplies the glycosite ground truth GlyGen itself curates; **[BioMCP](../../catalog/tools/biomcp.html)** supplies the ClinVar and literature joins that GlyGen does not cover (its germline variants come from the EBI variant API and its somatic variants from BioMuta); and **[ProtVar](../../catalog/tools/protvar.html)** supplies AlphaMissense keyed by UniProt accession. That last piece is not decoration — sourcing AlphaMissense through a genomic variant lookup silently returns another transcript's or another accession's score, which is worked through in step 2.

1. **Add both servers.**

   ```
   claude mcp add --transport http glygen https://mcp.glygen.org/mcp
   uv tool install biomcp-cli
   claude mcp add --transport stdio biomcp -- biomcp mcp
   ```

   Run `/mcp` to confirm both are connected.

2. **Have Claude write a versioned driver script, not a chat transcript.** Ask it to author `glyco_variants.py` that, for each input variant (`UniProt, protein_change` — e.g., `P01008,N135S`):
   - resolves the canonical GlyGen protein with `get_protein_summary` and pulls known glycosites with `get_site_summary`;
   - **harmonizes numbering** — reconcile the input site frame against the GlyGen canonical frame before comparing (the Asn135↔Asn167 antithrombin case is the canonical trap); refuse to classify a variant whose frame cannot be reconciled and log it as `unmapped`;
   - classifies each variant as `LOG` (mutation removes a residue in a known N-X-S/T sequon or an annotated O-glycosite), `GOG` (mutation creates a new N-X-S/T sequon — check the ±2 residue window), or `none`;
   - **joins AlphaMissense keyed by UniProt accession, not by genomic coordinate.** This is the step
     most likely to go silently wrong. AlphaMissense is defined per accession + residue, but a
     gene + `hgvs_p` variant search resolves to a *genomic* record, and one genomic record carries an
     annotation per transcript. Two ways that bites: `IFNGR2 p.T70N` matches two records, one of which
     is canonically **Thr149Asn** (AlphaMissense 0.1203 vs the correct 0.1845); and for `SERPINC1` the
     first entry of dbNSFP's isoform-aligned score array is the TrEMBL fragment `Q8TCE1`, not Swiss-Prot
     `P01008`, so an unlabelled "first score" is another entry's (S114N 0.9209 rather than 0.8726).
     Worse, you cannot reliably repair this by indexing the arrays yourself: in a randomized sample of
     362 genes, **18% list fewer AlphaMissense scores than isoforms** (29% of the genes listing more
     than one isoform), with nothing indicating which were dropped. Use an accession-keyed source instead:

     ```
     POST https://www.ebi.ac.uk/ProtVar/api/input/text     # "P01008 114 S N", one per line
     GET  https://www.ebi.ac.uk/ProtVar/api/mapping/{inputId}
     ```

     Take `amScore` from the isoform flagged `canonical`. ProtVar also **checks the reference residue**
     for you (`P01008 220 R C` → *"reference amino acid (Arg) does not match the UniProt sequence (Lys)
     at position 220"*, plus a non-SNV-reachable warning and 9 enumerated derived variants) — treat any
     `WARN`, or more than one derived genomic variant, as `unmapped`. And it is batched, so a cohort is
     one submission rather than one call per variant. The primary source
     ([`AlphaMissense_aa_substitutions.tsv.gz`](https://doi.org/10.5281/zenodo.8208688), ~1.2 GB,
     keyed by `uniprot_id`/`protein_variant`) is the offline, checksummable alternative;
   - **joins ClinVar via BioMCP, then verifies it.** `GET /population/{acc}/{pos}` gives the allele's
     rsID; look it up with `biomcp get variant <rsid> all` and use the record **only if its own `hgvs_p`
     equals the canonical change** — an rsID can span several alleles at a position (`rs121909570` covers
     `SERPINC1` 167, where `N167T` is the ClinVar allele and `N167S` is not). When reading ProtVar's own
     `clinicalSignificances`, keep only calls whose `sources` include ClinVar: `N167S` reports
     Pathogenic from **Ensembl alone**, and MyVariant has no ClinVar record there;
   - emits `glyco_candidates.csv` with columns `uniprot, site, class, glygen_evidence, clinvar_significance, alphamissense, rank`.

   Rank GOG/LOG hits above `none`, then within class by AlphaMissense pathogenicity and ClinVar significance.

3. **Add an expression sanity-check step.** Have the script (or a short follow-up cell) note whether the affected protein is expressed in the tissue/disease context of interest — cite the source you use and record its snapshot date; drop candidates in tissues where the protein is not expressed to the bottom of the ranking rather than deleting them.

4. **Pin the environment and record provenance.** Commit `glyco_variants.py`, a pinned `requirements.txt` (the `mcp`/`biomcp-python` client versions), the input variant list, `glyco_candidates.csv`, and a `provenance.json` capturing: GlyGen release version + MCP endpoint, BioMCP version, ClinVar/AlphaMissense snapshot dates, input file sha256, run date, and model id. Follow the [reproducibility guide](../../guide/advanced/reproducibility.md) and model the artifact on [`recipes/examples/functional-enrichment/`](../examples/functional-enrichment/).

5. **Emit an IEEE-2791 BioCompute Object.** Serialize the run as an IEEE-2791 (BioCompute Object) JSON alongside `provenance.json`, populating the standard domains — `description_domain.pipeline_steps` (the GlyGen lookup → numbering harmonization → LOG/GOG classification → BioMCP join → rank), `execution_domain` (script, pinned software, the GlyGen MCP / UniProt / BioMCP endpoints), `parametric_domain` (the sequon rule and ranking), `io_domain`, and `error_domain` (the missense-only scope, the ranking heuristic, the `unmapped` guard). GlyGen publishes its own source datasets as BCOs ([germline `GLY_001534`](https://data.glygen.org/GLY_001534), [cancer `GLY_001537`](https://data.glygen.org/GLY_001537)) — cite those in the `io_domain` input as dataset provenance. Put the **actual dataset filename** in each input's `filename` field (`human_protein_mutation_germline_all.csv`, `human_protein_mutation_cancer_all.csv`) rather than a prose label, so the entry carries both the `GLY_*` identifier and the specific file used — this is how GlyGen writes its own BCOs, and the IEEE-2791 `uri` object has no free-text description field to put a label in. **Validate the object against the [published IEEE-2791 JSON schema](https://w3id.org/ieee/ieee-2791-schema/2791object.json) before relying on it.** See [`recipes/examples/glyco-variants/`](../examples/glyco-variants/) for a reference implementation that emits and validates the BCO.

The natural-language ranked report must cite only what appears in `glyco_candidates.csv` — the saved table is the audit trail.

## Why this assembly

Rung 3 (small toolbelt, three components). One MCP is not enough: GlyGen owns the glycosite ground truth but not the clinical/pathogenicity joins the request needs, and BioMCP owns the ClinVar join but has no glycosylation-site data. AlphaMissense is a third component rather than part of BioMCP's job because it is defined per UniProt accession and residue, and every genomic-coordinate route to it can resolve to the wrong protein. Neither alone answers "is this variant glycosylation-altering *and* clinically interesting." Claude Code alone (rung 1) cannot fetch live glycosite or variant records and would confabulate sequon positions. Rung 4 (an autonomous system) is unwarranted — the workflow is a bounded lookup-join-rank, not an open-ended research loop.

## Availability

Fully open to run. GlyGen data is publicly and freely accessible; BioMCP is MIT-licensed and MyVariant.info → ClinVar is a public API; ProtVar is an EMBL-EBI service and AlphaMissense is CC-BY-4.0. **Caveat:** the GlyGen MCP wrapper repo declares no LICENSE file (flagged on its [catalog page](../../catalog/tools/glygen.html) as of 2026-07-15), and the endpoint is Beta — pin the release version you queried and expect the tool surface to move.

## Compute requirements

Laptop-sufficient. Every step is a read-only remote API call. ProtVar takes the whole variant list in one batched submission, so the remaining per-variant cost is the ClinVar lookup; a few hundred variants completes in minutes. No GPU.

## Evidence

Reported. The GlyGen team documents this exact workflow — "Use case: Identifying the impact of mutational loss or gain of glycosylation sites" — in the GlyGen knowledgebase preprint ([Mazumder et al., *Research Square* 2026-07-01](https://www.researchsquare.com/article/rs-9982242/v1)), with the SERPINC1 (LOG, Asn135↔Asn167) and IFNGR2 Thr168Asn (GOG) worked examples, and ships a reference implementation as the `variants.ipynb` Colab notebook ([`glygener/colab-notebooks`](https://github.com/glygener/colab-notebooks)) that regenerates the plots from the GlyGen proteoform and mutation datasets. That documents a human running the assembly's core (glycosite lookup → variant classification → annotation join). The glycosylation-site-disruption mechanism is independently well established (e.g., glycosylation-defect disease mechanisms, [Noor et al., *J. Biol. Chem.* 2021](https://pubmed.ncbi.nlm.nih.gov/33610554/)). What is **not** separately benchmarked is the *Claude-driven, GlyGen-MCP + BioMCP + ProtVar* composition — no published attempt of the agent-orchestrated version is known; the ranking heuristic here is rational from the component capabilities, not validated. The annotation values in the reference example were, however, checked residue by residue against an independent hand review by GlyGen's glycan data manager, and agree exactly.

## Alternatives considered

- **The Colab notebook directly.** If you only need the two published worked examples and don't need arbitrary variant lists or ClinVar/AlphaMissense joins, run `variants.ipynb` as-is — it's the validated reference. Reach for this recipe when you have your *own* variant list and want the annotation joins and a re-runnable provenance record.
- **[Interpret a clinical variant](interpret-clinical-variant.html) (rung 2, BioMCP alone).** Use it when the question is general clinical significance of a variant, not specifically its glycosylation consequence. This recipe adds the GlyGen glycosite layer on top.
- **[Scan a therapeutic antibody for glycosylation sites](scan-antibody-glycosylation-sites.html).** The sequence-level sibling — scans a single protein sequence for sequons de novo (no variant list, no clinical join). Use it for developability pre-flight, not variant interpretation.

## See also

- [GlyGen MCP Server](../../catalog/tools/glygen.html)
- [BioMCP](../../catalog/tools/biomcp.html)
- [ProtVar MCP Server](../../catalog/tools/protvar.html) — accession-keyed AlphaMissense, reference-residue checking, batched submission. The driver here calls ProtVar's REST surface (`https://www.ebi.ac.uk/ProtVar/api`, [Swagger UI](https://www.ebi.ac.uk/ProtVar/api/swagger-ui/index.html)) for a pinnable pipeline; the MCP server is the interactive route.
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — the general variant-annotation sibling.
- [Scan a therapeutic antibody for glycosylation sites](scan-antibody-glycosylation-sites.html) — the sequence-level glycosite scanner.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) — the artifact pattern this recipe follows.

## Sources

- [GlyGen knowledgebase preprint (Mazumder et al., *Research Square*)](https://www.researchsquare.com/article/rs-9982242/v1) — posted 2026-07-01; verified 2026-07-16 (this run). Documents the LOG/GOG use case and worked examples.
- [`glygener/colab-notebooks` (`variants.ipynb`)](https://github.com/glygener/colab-notebooks) — reference implementation of the glycosylation-variant workflow.
- [GlyGen germline variant BCO `GLY_001534`](https://data.glygen.org/GLY_001534) (`human_protein_mutation_germline_all.csv`) / [cancer `GLY_001537`](https://data.glygen.org/GLY_001537) (`human_protein_mutation_cancer_all.csv`) — input-dataset provenance.
- [Noor et al., *J. Biol. Chem.* 2021](https://pubmed.ncbi.nlm.nih.gov/33610554/) — glycosylation-defect disease-mechanism support.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=interpret-glycosylation-altering-variants&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Finterpret-glycosylation-altering-variants.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
