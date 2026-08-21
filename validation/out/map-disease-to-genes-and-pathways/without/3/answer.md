## Assumption
You didn't name a disease, so I'll use **type 2 diabetes mellitus** (EFO_0001360) as the worked example. The pipeline below is disease-agnostic — swap the EFO ID and everything else is unchanged.

## The pipeline (2 stages, both backed by real stats, no LLM-generated numbers anywhere)

**Stage 1 — disease → ranked genes: Open Targets Platform**
Open Targets is the right source here because its association score isn't a popularity count — it's a weighted composite of real evidence channels (human genetics/GWAS, somatic mutations, known drugs, RNA/protein expression, animal models, pathways, literature mining), each independently scored and documented. That's what "trustworthy ranking" should mean rather than a single text-mining count (which is what plain PubMed-co-occurrence tools like DisGeNET's text-mined tier give you — DisGeNET is a fine cross-check but weight its curated tier more than its text-mined tier).

```python
import requests, pandas as pd

query = """
query DiseaseTargets($efoId: String!, $size: Int!) {
  disease(efoId: $efoId) {
    id
    name
    associatedTargets(page: {index: 0, size: $size}) {
      count
      rows {
        target { id approvedSymbol }
        score
        datatypeScores { id score }
      }
    }
  }
}
"""
r = requests.post(
    "https://api.platform.opentargets.org/api/v4/graphql",
    json={"query": query, "variables": {"efoId": "EFO_0001360", "size": 500}},
)
rows = r.json()["data"]["disease"]["associatedTargets"]["rows"]

genes = pd.DataFrame([{
    "ensembl_id": row["target"]["id"],
    "gene_symbol": row["target"]["approvedSymbol"],
    "association_score": row["score"],
    **{d["id"]: d["score"] for d in row["datatypeScores"]},
} for row in rows]).sort_values("association_score", ascending=False).reset_index(drop=True)

genes.insert(0, "rank", genes.index + 1)
genes.to_csv("t2d_ranked_genes.csv", index=False)
```

**Table 1 (export as-is):** `rank, gene_symbol, ensembl_id, association_score, genetic_association, somatic_mutation, known_drug, rna_expression, affected_pathway, literature, animal_model`. The per-datatype columns are what let you (or a reviewer) audit *why* a gene ranked where it did — e.g. `TCF7L2` will rank near the top almost entirely on `genetic_association`, which is a sanity check you can point to.

(Note: for >~500 targets or repeated batch runs, Open Targets' own docs recommend the BigQuery/Parquet bulk dataset instead of hammering the GraphQL endpoint — same numbers, better for scale.)

**Stage 2 — genes → enriched GO/KEGG/Reactome terms: g:Profiler (g:GOSt), using the *ranked* list**

Because your gene list already has a meaningful order (association score), don't collapse it into a flat "top 200" set for a plain hypergeometric test — that throws away information and makes the cutoff arbitrary. Use g:Profiler's `ordered_query=True` mode, which runs incremental hypergeometric tests as it walks down the ranked list (the same logic as GSEA's leading-edge idea, but for overrepresentation) and still applies proper multiple-testing correction (g:SCS, which accounts for GO's hierarchical redundancy — stricter and more honest than a naive Bonferroni over thousands of correlated terms).

```python
from gprofiler import GProfiler

gp = GProfiler(return_dataframe=True)
enrich = gp.profile(
    organism="hsapiens",
    query=genes["gene_symbol"].tolist(),   # already rank-ordered from Stage 1
    ordered=True,
    sources=["GO:BP", "GO:MF", "GO:CC", "KEGG", "REAC"],
    user_threshold=0.05,
    significance_threshold_method="g_SCS",
    no_evidences=False,   # keep intersecting genes per term
)

table2 = enrich[[
    "source", "native", "name", "p_value", "term_size",
    "query_size", "intersection_size", "intersections"
]].rename(columns={"native": "term_id", "name": "term_name", "p_value": "adjusted_p_value"})
table2.to_csv("t2d_enrichment.csv", index=False)
```

**Table 2 (export as-is):** `source, term_id, term_name, adjusted_p_value, term_size, query_size, intersection_size, intersections`. `adjusted_p_value` is already multiple-testing corrected — don't re-filter on a raw p-value column, there isn't one exposed by design.

## Why you can trust these numbers specifically
- Every score in Table 1 traces back to Open Targets' documented, versioned evidence pipelines (GWAS Catalog, ClinVar, ChEMBL, Expression Atlas, etc.) — nothing is inferred by a language model.
- Every p-value in Table 2 comes from g:Profiler's backend hypergeometric/Fisher's-exact test against current GO/KEGG/Reactome releases, with g:SCS correction — this is the same engine used in hundreds of peer-reviewed papers, not a paraphrase of one.
- If you want a second, independently-implemented statistical engine as a cross-check (recommended for anything going into a publication or report), rerun Stage 2 with R's `clusterProfiler::enrichGO`/`enrichKEGG` + `ReactomePA::enrichPathway` (Benjamini-Hochberg FDR) on the same gene list — if the two disagree substantially on the top terms, that's a signal to look closer rather than trust either blindly.

## Practical notes
- Pick a principled cutoff for Table 1 if you need a bounded list for downstream use (e.g., `association_score ≥ 0.1`, or top 200) — but keep the *full* ranked table as the artifact, and always feed the ordered (not truncated) list into `ordered_query`.
- Restrict `sources` to just `GO:BP, KEGG, REAC` if you want a tighter, more pathway-focused summary rather than also pulling GO:MF/GO:CC molecular-function/cellular-component noise.

Sources: [Open Targets GraphQL API docs](https://platform-docs.opentargets.org/data-access/graphql-api), [Open Targets GraphQL schema](https://api.platform.opentargets.org/api/v4/graphql/schema), [gprofiler-official on PyPI](https://pypi.org/project/gprofiler-official/), [g:Profiler APIs](https://biit.cs.ut.ee/gprofiler/page/apis), [g:Profiler ordered query tutorial](https://baderlab.github.io/CBW_Pathways_2021/gprofiler-lab.html)