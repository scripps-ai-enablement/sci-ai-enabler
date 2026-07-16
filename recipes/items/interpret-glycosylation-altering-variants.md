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
summary: Flag coding variants that destroy or create N-/O-glycosylation sites with the GlyGen MCP, join to ClinVar/AlphaMissense via BioMCP, and emit a ranked, provenance-tracked candidate table.
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

This is a two-MCP toolbelt: **[GlyGen MCP](../../catalog/tools/glygen.html)** supplies the glycosite ground truth GlyGen itself curates; **[BioMCP](../../catalog/tools/biomcp.html)** supplies the ClinVar / AlphaMissense / literature joins that GlyGen does not cover (its germline variants come from the EBI variant API and its somatic variants from BioMuta).

1. **Add both servers.**

   ```
   claude mcp add --transport http glygen https://mcp.glygen.org/mcp
   uv tool install biomcp-cli
   claude mcp add --transport stdio biomcp -- biomcp run
   ```

   Run `/mcp` to confirm both are connected.

2. **Have Claude write a versioned driver script, not a chat transcript.** Ask it to author `glyco_variants.py` that, for each input variant (`UniProt, protein_change` — e.g., `P01008,N135S`):
   - resolves the canonical GlyGen protein with `get_protein_summary` and pulls known glycosites with `get_site_summary`;
   - **harmonizes numbering** — reconcile the input site frame against the GlyGen canonical frame before comparing (the Asn135↔Asn167 antithrombin case is the canonical trap); refuse to classify a variant whose frame cannot be reconciled and log it as `unmapped`;
   - classifies each variant as `LOG` (mutation removes a residue in a known N-X-S/T sequon or an annotated O-glycosite), `GOG` (mutation creates a new N-X-S/T sequon — check the ±2 residue window), or `none`;
   - joins ClinVar significance and AlphaMissense pathogenicity via BioMCP `variant_searcher`/`variant_getter` (MyVariant.info federates both);
   - emits `glyco_candidates.csv` with columns `uniprot, site, class, glygen_evidence, clinvar_significance, alphamissense, rank`.

   Rank GOG/LOG hits above `none`, then within class by AlphaMissense pathogenicity and ClinVar significance.

3. **Add an expression sanity-check step.** Have the script (or a short follow-up cell) note whether the affected protein is expressed in the tissue/disease context of interest — cite the source you use and record its snapshot date; drop candidates in tissues where the protein is not expressed to the bottom of the ranking rather than deleting them.

4. **Pin the environment and record provenance.** Commit `glyco_variants.py`, a pinned `requirements.txt` (the `mcp`/`biomcp-python` client versions), the input variant list, `glyco_candidates.csv`, and a `provenance.json` capturing: GlyGen release version + MCP endpoint, BioMCP version, ClinVar/AlphaMissense snapshot dates, input file sha256, run date, and model id. Follow the [reproducibility guide](../../guide/advanced/reproducibility.md) and model the artifact on [`recipes/examples/functional-enrichment/`](../examples/functional-enrichment/).

5. **(Optional) Emit an IEEE-2791 BioCompute Object.** GlyGen publishes its source datasets as BCOs ([germline `GLY_001534`](https://data.glygen.org/GLY_001534), [somatic `GLY_001537`](https://data.glygen.org/GLY_001537)); cite those as input provenance and, if your downstream consumers require it, serialize the run as a schema-validated BCO JSON alongside `provenance.json`.

The natural-language ranked report must cite only what appears in `glyco_candidates.csv` — the saved table is the audit trail.

## Why this assembly

Rung 3 (small toolbelt, two components). One MCP is not enough: GlyGen owns the glycosite ground truth but not the ClinVar/AlphaMissense pathogenicity joins the request needs, and BioMCP owns those joins but has no glycosylation-site data. Neither alone answers "is this variant glycosylation-altering *and* clinically interesting." Claude Code alone (rung 1) cannot fetch live glycosite or variant records and would confabulate sequon positions. Rung 4 (an autonomous system) is unwarranted — the workflow is a bounded lookup-join-rank, not an open-ended research loop.

## Availability

Fully open to run. GlyGen data is publicly and freely accessible; BioMCP is MIT-licensed and its underlying sources (MyVariant.info → ClinVar, AlphaMissense) are public APIs. **Caveat:** the GlyGen MCP wrapper repo declares no LICENSE file (flagged on its [catalog page](../../catalog/tools/glygen.html) as of 2026-07-15), and the endpoint is Beta — pin the release version you queried and expect the tool surface to move.

## Compute requirements

Laptop-sufficient. Every step is a read-only remote API call. A list of a few hundred variants completes in minutes; the bottleneck is per-variant BioMCP lookups, not compute. No GPU.

## Evidence

Reported. The GlyGen team documents this exact workflow — "Use case: Identifying the impact of mutational loss or gain of glycosylation sites" — in the GlyGen knowledgebase preprint ([Mazumder et al., *Research Square* 2026-07-01](https://www.researchsquare.com/article/rs-9982242/v1)), with the SERPINC1 (LOG, Asn135↔Asn167) and IFNGR2 Thr168Asn (GOG) worked examples, and ships a reference implementation as the `variants.ipynb` Colab notebook ([`glygener/colab-notebooks`](https://github.com/glygener/colab-notebooks)) that regenerates the plots from the GlyGen proteoform and mutation datasets. That documents a human running the assembly's core (glycosite lookup → variant classification → annotation join). The glycosylation-site-disruption mechanism is independently well established (e.g., glycosylation-defect disease mechanisms, [Noor et al., *J. Biol. Chem.* 2021](https://pubmed.ncbi.nlm.nih.gov/33610554/)). What is **not** separately benchmarked is the *Claude-driven, GlyGen-MCP + BioMCP* composition — no published attempt of the agent-orchestrated version is known; the ranking heuristic here is rational from the component capabilities, not validated.

## Alternatives considered

- **The Colab notebook directly.** If you only need the two published worked examples and don't need arbitrary variant lists or ClinVar/AlphaMissense joins, run `variants.ipynb` as-is — it's the validated reference. Reach for this recipe when you have your *own* variant list and want the annotation joins and a re-runnable provenance record.
- **[Interpret a clinical variant](interpret-clinical-variant.html) (rung 2, BioMCP alone).** Use it when the question is general clinical significance of a variant, not specifically its glycosylation consequence. This recipe adds the GlyGen glycosite layer on top.
- **[Scan a therapeutic antibody for glycosylation sites](scan-antibody-glycosylation-sites.html).** The sequence-level sibling — scans a single protein sequence for sequons de novo (no variant list, no clinical join). Use it for developability pre-flight, not variant interpretation.

## See also

- [GlyGen MCP Server](../../catalog/tools/glygen.html)
- [BioMCP](../../catalog/tools/biomcp.html)
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — the general variant-annotation sibling.
- [Scan a therapeutic antibody for glycosylation sites](scan-antibody-glycosylation-sites.html) — the sequence-level glycosite scanner.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) — the artifact pattern this recipe follows.

## Sources

- [GlyGen knowledgebase preprint (Mazumder et al., *Research Square*)](https://www.researchsquare.com/article/rs-9982242/v1) — posted 2026-07-01; verified 2026-07-16 (this run). Documents the LOG/GOG use case and worked examples.
- [`glygener/colab-notebooks` (`variants.ipynb`)](https://github.com/glygener/colab-notebooks) — reference implementation of the glycosylation-variant workflow.
- [GlyGen germline variant BCO `GLY_001534`](https://data.glygen.org/GLY_001534) / [somatic `GLY_001537`](https://data.glygen.org/GLY_001537) — input-dataset provenance.
- [Noor et al., *J. Biol. Chem.* 2021](https://pubmed.ncbi.nlm.nih.gov/33610554/) — glycosylation-defect disease-mechanism support.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=interpret-glycosylation-altering-variants&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Finterpret-glycosylation-altering-variants.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
