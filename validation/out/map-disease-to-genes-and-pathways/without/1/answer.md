File write requires a permission I can't get approved mid-turn here, so I'll give you the complete script directly — copy it into a `.py` file and run it locally where you have network access and Python 3.

## Full script

```python
#!/usr/bin/env python3
"""
Disease name -> ranked gene table -> GO/KEGG/Reactome enrichment table.

Data sources (both free, no API key required):
  1. Open Targets Platform GraphQL API - disease-target association scores
     built from GWAS, ClinVar, somatic mutations, pathways, expression,
     animal models, and literature (each with its own sub-score).
     Docs: https://platform-docs.opentargets.org/data-access/graphql-api
  2. g:Profiler g:GOSt API - hypergeometric enrichment test with g:SCS
     multiple-testing correction over GO:BP/MF/CC, KEGG, Reactome.
     Docs: https://biit.cs.ut.ee/gprofiler/page/apis

Usage:
    python3 disease_to_pathways.py "type 2 diabetes mellitus" --top-n 150

Outputs:
    gene_ranking.csv        - ranked genes with Open Targets association scores
    enrichment_results.csv  - significant GO/KEGG/Reactome terms with real stats
"""
import argparse
import sys
import urllib.request
import json
import csv

OT_API = "https://api.platform.opentargets.org/api/v4/graphql"
GPROFILER_API = "https://biit.cs.ut.ee/gprofiler/api/gost/profile/"


def _post_json(url, payload, timeout=30):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def resolve_disease_efo_id(disease_name):
    """disease name -> best-matching EFO id via Open Targets search."""
    query = """
    query SearchDisease($q: String!) {
      search(queryString: $q, entityNames: ["disease"], page: {index: 0, size: 5}) {
        hits { id name entity }
      }
    }
    """
    resp = _post_json(OT_API, {"query": query, "variables": {"q": disease_name}})
    hits = resp["data"]["search"]["hits"]
    if not hits:
        raise ValueError(f"No disease match found for '{disease_name}' in Open Targets.")
    top = hits[0]
    print(f"[i] Resolved '{disease_name}' -> {top['id']} ({top['name']})", file=sys.stderr)
    return top["id"], top["name"]


def get_ranked_genes(disease_name, top_n=150):
    """Return list of dicts: symbol, ensembl_id, name, score (sorted desc)."""
    efo_id, resolved_name = resolve_disease_efo_id(disease_name)

    query = """
    query DiseaseAssociations($efoId: String!, $size: Int!) {
      disease(efoId: $efoId) {
        id
        name
        associatedTargets(page: {index: 0, size: $size}) {
          count
          rows {
            score
            target { id approvedSymbol approvedName }
          }
        }
      }
    }
    """
    resp = _post_json(OT_API, {"query": query, "variables": {"efoId": efo_id, "size": top_n}})
    disease = resp["data"]["disease"]
    if disease is None:
        raise ValueError(f"Open Targets returned no disease record for EFO id {efo_id}.")

    rows = disease["associatedTargets"]["rows"]
    total = disease["associatedTargets"]["count"]
    print(
        f"[i] Open Targets has {total} associated targets total; "
        f"pulling top {len(rows)} by association score.",
        file=sys.stderr,
    )

    genes = []
    for rank, row in enumerate(rows, start=1):
        t = row["target"]
        genes.append(
            {
                "rank": rank,
                "gene_symbol": t["approvedSymbol"],
                "ensembl_id": t["id"],
                "gene_name": t["approvedName"],
                "association_score": round(row["score"], 4),
                "disease": resolved_name,
                "disease_efo_id": efo_id,
            }
        )
    return genes


def run_enrichment(gene_symbols, sources=("GO:BP", "KEGG", "REAC"), organism="hsapiens", alpha=0.05):
    """Submit gene symbols to g:Profiler g:GOSt and return significant terms."""
    payload = {
        "organism": organism,
        "query": gene_symbols,
        "sources": list(sources),
        "user_threshold": alpha,
        "significance_threshold_method": "g_SCS",  # validated multiple-testing correction
        "no_evidences": False,  # include which query genes hit each term
        "domain_scope": "annotated",  # standard background: all annotated genes
    }
    resp = _post_json(GPROFILER_API, payload, timeout=60)
    results = resp.get("result", [])
    print(f"[i] g:Profiler returned {len(results)} significant terms (g:SCS alpha={alpha}).",
          file=sys.stderr)

    rows = []
    for r in sorted(results, key=lambda x: x["p_value"]):
        intersecting_genes = []
        if r.get("intersections"):
            for gene_sym, hit in zip(gene_symbols, r["intersections"]):
                if hit:
                    intersecting_genes.append(gene_sym)
        rows.append(
            {
                "source": r["source"],
                "term_id": r["native"],
                "term_name": r["name"],
                "p_value": r["p_value"],
                "term_size": r["term_size"],
                "query_size": r["query_size"],
                "intersection_size": r["intersection_size"],
                "precision": round(r["precision"], 4),
                "recall": round(r["recall"], 4),
                "intersecting_genes": ";".join(intersecting_genes),
            }
        )
    return rows


def write_csv(rows, path):
    if not rows:
        print(f"[!] No rows to write for {path}", file=sys.stderr)
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"[i] Wrote {len(rows)} rows -> {path}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("disease", help='Disease name, e.g. "type 2 diabetes mellitus"')
    ap.add_argument("--top-n", type=int, default=150, help="Number of top-ranked genes to carry into enrichment")
    ap.add_argument("--alpha", type=float, default=0.05, help="Significance threshold for g:SCS correction")
    ap.add_argument("--sources", nargs="+", default=["GO:BP", "KEGG", "REAC"],
                     help="g:Profiler sources, e.g. GO:BP GO:MF GO:CC KEGG REAC WP")
    ap.add_argument("--gene-csv", default="gene_ranking.csv")
    ap.add_argument("--enrichment-csv", default="enrichment_results.csv")
    args = ap.parse_args()

    genes = get_ranked_genes(args.disease, top_n=args.top_n)
    write_csv(genes, args.gene_csv)

    symbols = [g["gene_symbol"] for g in genes]
    enrichment = run_enrichment(symbols, sources=args.sources, alpha=args.alpha)
    write_csv(enrichment, args.enrichment_csv)


if __name__ == "__main__":
    main()
```

Run it (worked example, since none was specified — assumption stated up front):

```
python3 disease_to_pathways.py "type 2 diabetes mellitus" --top-n 150
```

## What you get

**`gene_ranking.csv`** — `rank, gene_symbol, ensembl_id, gene_name, association_score, disease, disease_efo_id`, sorted by Open Targets' composite association score (0–1), which aggregates GWAS/genetic association, ClinVar/curated disease databases, somatic mutation burden, pathway membership, differential expression, animal-model phenotypes, and literature co-mention — each channel independently weighted and auditable back through the Open Targets UI for any gene you want to spot-check.

**`enrichment_results.csv`** — `source, term_id, term_name, p_value, term_size, query_size, intersection_size, precision, recall, intersecting_genes`, one row per GO Biological Process / KEGG / Reactome term that survives g:Profiler's g:SCS-corrected significance threshold (default α=0.05) — a real hypergeometric test against the annotated human genome as background, not a paraphrase of gene names.

## Notes on trustworthiness and tuning

- **No LLM touches the numbers.** Both APIs return machine-computed scores/p-values; the script only reshapes JSON into CSV. Nothing here is generated text.
- **`--top-n`** controls the bias/noise tradeoff: too few genes underpowers enrichment, too many drags in weakly-associated genes that dilute the signal. 100–200 is a reasonable default for a well-studied disease; for a rare/understudied one, Open Targets may only have a few dozen associated targets total (the script logs the true total to stderr so you know if you're truncating or exhausting the list).
- **Cross-validation:** for extra confidence, run the same `symbols` list through `gseapy.enrichr()` (Fisher's exact test + Benjamini-Hochberg, using Enrichr's gene-set libraries) and intersect the two term lists — anything significant in both g:Profiler and Enrichr is essentially bulletproof.
- **Background set matters:** `domain_scope: "annotated"` uses all annotated genes as background, standard for disease-gene lists. If you're instead comparing against a specific assayed background (e.g., genes on a microarray/panel), switch to `domain_scope: "custom"` and supply that background explicitly — using the wrong background is the most common way enrichment p-values get quietly wrong.
- **Schema drift risk:** both APIs occasionally version their GraphQL schema/REST payload; if a field name errors out, check `https://platform-docs.opentargets.org/data-access/graphql-api` and `https://biit.cs.ut.ee/gprofiler/page/apis` for the current shape.