It looks like this sandbox isn't approving file writes or network calls interactively, so I'll give you the complete, ready-to-save pipeline inline instead — copy each block into a `.py` file yourself.

## Setup

```bash
pip install requests pandas gprofiler-official
```

## Script 1 — `disease_to_genes.py` (disease name → ranked gene table)

```python
#!/usr/bin/env python3
"""
Disease name -> ranked gene table, via the Open Targets Platform GraphQL API.

Usage:
    python3 disease_to_genes.py "Parkinson disease" --top 200 --min-score 0.05 \
        --out disease_gene_ranking.csv
"""
import argparse, sys
import requests
import pandas as pd

API_URL = "https://api.platform.opentargets.org/api/v4/graphql"

SEARCH_QUERY = """
query Search($q: String!) {
  search(queryString: $q, entityNames: ["disease"]) {
    hits { id name entity }
  }
}
"""

ASSOC_QUERY = """
query DiseaseAssociations($efoId: String!, $index: Int!, $size: Int!) {
  disease(efoId: $efoId) {
    id
    name
    associatedTargets(page: { index: $index, size: $size }) {
      count
      rows {
        target { id approvedSymbol }
        score
        datatypeScores { id score }
      }
    }
  }
  meta { dataVersion { year month iteration } }
}
"""

DATATYPE_KEYS = {
    "genetic_association": "genetic_association_score",
    "somatic_mutation": "somatic_mutation_score",
    "known_drug": "known_drug_score",
    "affected_pathway": "affected_pathway_score",
    "literature": "literature_score",
    "rna_expression": "rna_expression_score",
    "animal_model": "animal_model_score",
}

def resolve_efo_id(disease_name):
    resp = requests.post(API_URL, json={"query": SEARCH_QUERY, "variables": {"q": disease_name}}, timeout=30)
    resp.raise_for_status()
    hits = resp.json()["data"]["search"]["hits"]
    if not hits:
        sys.exit(f"No disease match found for '{disease_name}'")
    top = hits[0]
    print(f"Resolved '{disease_name}' -> {top['id']} ({top['name']})", file=sys.stderr)
    return top["id"], top["name"]

def fetch_associations(efo_id, top_n, page_size=500):
    rows, index, data_version = [], 0, None
    while len(rows) < top_n:
        variables = {"efoId": efo_id, "index": index, "size": page_size}
        resp = requests.post(API_URL, json={"query": ASSOC_QUERY, "variables": variables}, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        if "errors" in payload:
            sys.exit(f"Open Targets API error: {payload['errors']}")
        disease = payload["data"]["disease"]
        if disease is None:
            sys.exit(f"EFO ID '{efo_id}' not found")
        dv = payload["data"]["meta"]["dataVersion"]
        data_version = f"{dv['year']}.{dv['month']}.{dv['iteration']}"
        page_rows = disease["associatedTargets"]["rows"]
        if not page_rows:
            break
        rows.extend(page_rows)
        index += 1
        if len(page_rows) < page_size:
            break
    return rows[:top_n], data_version

def to_dataframe(rows, ot_data_release):
    records = []
    for r in rows:
        rec = {
            "gene_symbol": r["target"]["approvedSymbol"],
            "ensembl_gene_id": r["target"]["id"],
            "overall_association_score": r["score"],
        }
        for dt in DATATYPE_KEYS.values():
            rec[dt] = 0.0
        for dts in r["datatypeScores"]:
            key = DATATYPE_KEYS.get(dts["id"])
            if key:
                rec[key] = dts["score"]
        rec["ot_data_release"] = ot_data_release
        records.append(rec)
    df = pd.DataFrame(records).sort_values("overall_association_score", ascending=False).reset_index(drop=True)
    df.insert(0, "rank", df.index + 1)
    return df

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("disease", help="Free-text disease name, e.g. 'Parkinson disease'")
    ap.add_argument("--efo-id", default=None, help="Skip name resolution, use this EFO ID directly")
    ap.add_argument("--top", type=int, default=200)
    ap.add_argument("--min-score", type=float, default=0.0)
    ap.add_argument("--out", default="disease_gene_ranking.csv")
    args = ap.parse_args()

    efo_id, disease_name = (args.efo_id, args.disease) if args.efo_id else resolve_efo_id(args.disease)
    rows, ot_data_release = fetch_associations(efo_id, args.top)
    df = to_dataframe(rows, ot_data_release)
    df = df[df["overall_association_score"] >= args.min_score]
    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} genes for '{disease_name}' ({efo_id}), OT release {ot_data_release} -> {args.out}",
          file=sys.stderr)

if __name__ == "__main__":
    main()
```

**Table 1 schema** (`disease_gene_ranking.csv`): `rank, gene_symbol, ensembl_gene_id, overall_association_score, genetic_association_score, somatic_mutation_score, known_drug_score, affected_pathway_score, literature_score, rna_expression_score, animal_model_score, ot_data_release`

## Script 2 — `genes_to_enrichment.py` (gene table → enrichment table)

```python
#!/usr/bin/env python3
"""
Gene list -> GO/KEGG/Reactome/WikiPathways enrichment via g:Profiler (g:GOSt).

Usage:
    python3 genes_to_enrichment.py disease_gene_ranking.csv \
        --gene-col gene_symbol --out enrichment_results.csv
"""
import argparse, sys
import pandas as pd
from gprofiler import GProfiler

SOURCES = ["GO:BP", "GO:CC", "GO:MF", "KEGG", "REAC", "WP"]

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("gene_csv")
    ap.add_argument("--gene-col", default="gene_symbol")
    ap.add_argument("--organism", default="hsapiens")
    ap.add_argument("--correction", default="g_SCS", choices=["g_SCS", "fdr", "bonferroni"])
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--all-results", action="store_true", help="Keep non-significant terms too")
    ap.add_argument("--out", default="enrichment_results.csv")
    args = ap.parse_args()

    genes = pd.read_csv(args.gene_csv)[args.gene_col].dropna().unique().tolist()
    if not genes:
        sys.exit("No genes found in input file")

    gp = GProfiler(return_dataframe=True)
    result = gp.profile(
        organism=args.organism,
        query=genes,
        sources=SOURCES,
        user_threshold=args.alpha,
        significance_threshold_method=args.correction,
        no_evidences=False,
        all_results=args.all_results,
    )

    cols = ["source", "native", "name", "p_value", "term_size", "query_size",
            "intersection_size", "precision", "recall", "intersections"]
    result = result.rename(columns={"native": "term_id", "name": "term_name"})
    cols = ["source", "term_id", "term_name", "p_value", "term_size", "query_size",
            "intersection_size", "precision", "recall", "intersections"]
    result = result[cols].sort_values("p_value").reset_index(drop=True)
    result.to_csv(args.out, index=False)
    print(f"Wrote {len(result)} enrichment terms ({args.correction}-corrected, alpha={args.alpha}) -> {args.out}",
          file=sys.stderr)

if __name__ == "__main__":
    main()
```

**Table 2 schema** (`enrichment_results.csv`): `source (GO:BP/GO:CC/GO:MF/KEGG/REAC/WP), term_id, term_name, p_value, term_size, query_size, intersection_size, precision, recall, intersections (comma-joined query genes hitting that term)`. `p_value` here is already corrected under whichever `--correction` method you picked (default `g_SCS`, g:Profiler's own name for its adjusted p-value column — despite the label it *is* the multiple-testing-corrected value, not raw).

## Run it end-to-end for the example

```bash
python3 disease_to_genes.py "Parkinson disease" --top 200 --min-score 0.05 --out disease_gene_ranking.csv
python3 genes_to_enrichment.py disease_gene_ranking.csv --gene-col gene_symbol --out enrichment_results.csv
```

## Why this stays "backed by real statistics, not a hallucinated summary"

- Every number in Table 1 is a value pulled verbatim from Open Targets' computed association-score JSON — nothing is paraphrased or estimated by a language model.
- Every p-value in Table 2 comes from g:Profiler's server-side hypergeometric test against a real annotation background, with a named, reproducible correction method — you can hand the exact same gene list to `clusterProfiler::enrichGO`/`enrichKEGG` in R and get statistically consistent results as a sanity check.
- Both outputs carry a version stamp (`ot_data_release`, and g:Profiler's e/p/ep build number is in its API response headers if you want to log it too) — record that alongside the CSVs, since these are living databases and the same query can shift slightly between releases.

## Two things to decide before trusting the output blindly

1. **Score composition**: Open Targets' overall score blends genetic evidence with text-mining/literature evidence, so a gene can rank highly on citations alone. If you want a stricter "genetically implicated" list, filter/sort on `genetic_association_score` instead of `overall_association_score`, or cross-check against DisGeNET's curated GDA score.
2. **Background set for enrichment**: the default here uses g:Profiler's whole-genome/whole-annotation background, which is standard and appropriate since your input (Stage 1) already spans the whole genome. If you ever restrict Stage 1 to a custom-assayed gene panel, pass that panel as a custom background (`gp.profile(..., background=panel_genes)`) — otherwise the p-values will be biased.