Here's the full solution — since this matched an existing curated recipe in the knowledge base, I didn't need to compose anything new.

## The recipe: `map-disease-to-genes-and-pathways`

**Evidence: Reported** (documented working chain, validated on knee osteoarthritis) · **Availability: Fully open**, no subscription or API key · **Compute: Laptop-grade**, ~1–2 min end-to-end for 30 genes × 5 libraries.

**Assumption** (you didn't name a disease): I used **type 2 diabetes** → Open Targets EFO ID `EFO_0001360`.

### Why this rung and not lower
A single good Claude Code prompt (rung 1) fails here because you explicitly don't want the model guessing gene-disease associations or pathway terms from memory — that's exactly the hallucination risk you're trying to avoid. This needs two real, queryable databases wired together (rung 2, chained into a small script).

### The chain
1. **Open Targets GraphQL API** (`https://api.platform.opentargets.org/api/v4/graphql`, CC0, no key) — resolve disease name → EFO ID, then pull the top-N targets by overall association score (combines genetics, somatic mutation, drugs, RNA expression, literature, animal models). This is your **ranked gene table**.
2. **`gget enrichr`** (wraps the Enrichr API, BSD-2-Clause, via `pachterlab/gget`) — run that gene list against `GO_Biological_Process_2023`, `KEGG_2021_Human`, `Reactome_2022`, `MSigDB_Hallmark_2020`, and `DisGeNET`. Keep only terms with **BH-adjusted p < 0.05**. This is your **enrichment table**.
3. **Positive-control check** — the disease name should resurface in its own DisGeNET enrichment results; if it doesn't, that's a symbol-mapping or species-mismatch flag, not a result to trust.
4. **Provenance record** — hash both CSVs, log package versions, timestamp, and the exact query, so the run is auditable later.

Every row in both tables traces to a specific API response — nothing is written by the LLM except the (optional) plain-language summary layered on top, and that summary is only allowed to cite rows that exist in the saved CSVs.

### Known limitations (from the recipe's track record)
- The hosted Open Targets **MCP** endpoint has been reported failing — the script below hits the GraphQL API directly instead.
- No peer-reviewed benchmark of this exact composed chain exists; it's been field-validated on one disease (knee osteoarthritis), not many.
- Gene-symbol harmonization across Open Targets → Enrichr can silently drop genes; that's what the positive-control step is for.

## The captured artifact

I attempted to write this to disk in your working directory as `analysis.py` but the sandbox didn't grant file-write permission in this session, so here it is in full — save it yourself as `analysis.py`:

```python
#!/usr/bin/env python3
"""
Disease -> ranked genes -> functional enrichment, grounded in real APIs.
Recipe: map-disease-to-genes-and-pathways (evidence: Reported)
"""
import argparse, csv, hashlib, json, sys, time, urllib.request

OT_GRAPHQL_URL = "https://api.platform.opentargets.org/api/v4/graphql"
ENRICHR_LIBRARIES = [
    "GO_Biological_Process_2023", "KEGG_2021_Human", "Reactome_2022",
    "MSigDB_Hallmark_2020", "DisGeNET",
]

DISEASE_SEARCH_QUERY = """
query DiseaseSearch($q: String!) {
  search(queryString: $q, entityNames: ["disease"], page: {index: 0, size: 5}) {
    hits { id name entity }
  }
}"""

DISEASE_TARGETS_QUERY = """
query DiseaseTargets($efoId: String!, $size: Int!) {
  disease(efoId: $efoId) {
    id name
    associatedTargets(page: {index: 0, size: $size}) {
      count
      rows {
        score
        target { id approvedSymbol approvedName }
        datatypeScores { id score }
      }
    }
  }
}"""

def graphql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(OT_GRAPHQL_URL, data=body,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode())
    if "errors" in payload:
        raise RuntimeError(f"Open Targets GraphQL error: {payload['errors']}")
    return payload["data"]

def resolve_disease(name):
    data = graphql(DISEASE_SEARCH_QUERY, {"q": name})
    hits = [h for h in data["search"]["hits"] if h["entity"] == "disease"]
    if not hits:
        raise SystemExit(f"No Open Targets disease match for '{name}'")
    best = hits[0]
    print(f"Resolved '{name}' -> {best['id']} ({best['name']})", file=sys.stderr)
    return best

def fetch_ranked_targets(efo_id, n):
    data = graphql(DISEASE_TARGETS_QUERY, {"efoId": efo_id, "size": n})
    rows = data["disease"]["associatedTargets"]["rows"]
    out = []
    for i, r in enumerate(rows, start=1):
        out.append({
            "rank": i,
            "gene_symbol": r["target"]["approvedSymbol"],
            "ensembl_id": r["target"]["id"],
            "gene_name": r["target"]["approvedName"],
            "overall_association_score": round(r["score"], 4),
            "datatype_scores": json.dumps({d["id"]: round(d["score"], 4) for d in r["datatypeScores"]}),
        })
    return out

def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(rows)
    return sha256_file(path)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def run_enrichment(gene_symbols):
    import gget, pandas as pd
    combined = []
    for lib in ENRICHR_LIBRARIES:
        try:
            df = gget.enrichr(gene_symbols, database=lib)
        except Exception as e:
            print(f"WARNING: enrichr call failed for {lib}: {e}", file=sys.stderr)
            continue
        if df is None or df.empty:
            continue
        df = df[df["adj_p_val"] < 0.05].copy()
        df["library"] = lib
        combined.append(df)
    if not combined:
        return []
    result = pd.concat(combined, ignore_index=True).sort_values("adj_p_val")
    cols = [c for c in ["library", "path_name", "overlapping_genes", "p_val",
                         "adj_p_val", "combined_score"] if c in result.columns]
    return result[cols].to_dict(orient="records")

def positive_control_check(disease_name, enrichment_rows):
    tokens = [t.lower() for t in disease_name.split() if len(t) > 3]
    for row in enrichment_rows:
        if row.get("library") != "DisGeNET":
            continue
        if any(tok in str(row.get("path_name", "")).lower() for tok in tokens):
            return True
    return False

def _safe_version(pkg):
    try:
        import importlib.metadata as md
        return md.version(pkg)
    except Exception:
        return "unknown"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("disease")
    ap.add_argument("--n-genes", type=int, default=30)
    ap.add_argument("--out-genes", default="ranked_genes.csv")
    ap.add_argument("--out-enrichment", default="enrichment_results.csv")
    ap.add_argument("--out-provenance", default="provenance.json")
    args = ap.parse_args()

    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    disease = resolve_disease(args.disease)
    targets = fetch_ranked_targets(disease["id"], args.n_genes)
    if not targets:
        raise SystemExit(f"Open Targets returned zero associated targets for {disease['id']}")

    genes_hash = write_csv(args.out_genes, targets,
        ["rank", "gene_symbol", "ensembl_id", "gene_name",
         "overall_association_score", "datatype_scores"])
    print(f"Wrote {args.out_genes} ({len(targets)} genes)", file=sys.stderr)

    gene_symbols = [t["gene_symbol"] for t in targets]
    enrichment_rows = run_enrichment(gene_symbols)
    enrichment_hash = None
    if enrichment_rows:
        enrichment_hash = write_csv(args.out_enrichment, enrichment_rows,
            ["library", "path_name", "overlapping_genes", "p_val",
             "adj_p_val", "combined_score"])
    else:
        print("WARNING: no enrichment terms survived adj_p_val < 0.05", file=sys.stderr)

    control_passed = positive_control_check(args.disease, enrichment_rows)
    print(("Positive-control check passed." if control_passed else
           "WARNING: positive-control check FAILED — verify gene-symbol/species mapping."),
          file=sys.stderr)

    provenance = {
        "started_utc": started,
        "query": {"disease_input": args.disease, "n_genes_requested": args.n_genes},
        "resolved_disease": disease,
        "sources": {"open_targets_graphql": OT_GRAPHQL_URL, "enrichr_libraries": ENRICHR_LIBRARIES},
        "outputs": {args.out_genes: genes_hash, args.out_enrichment: enrichment_hash},
        "positive_control_passed": control_passed,
        "gget_version": _safe_version("gget"),
        "pandas_version": _safe_version("pandas"),
    }
    with open(args.out_provenance, "w") as f:
        json.dump(provenance, f, indent=2)
    print(f"Wrote {args.out_provenance}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

`requirements.txt` (pin these — the recipe's evidence label depends on reproducible versions):
```
gget==0.29.1
pandas==2.2.3
```

### Run it
```bash
pip install -r requirements.txt
python analysis.py "type 2 diabetes" --n-genes 30
```

This produces exactly the two tables you asked for:
- **`ranked_genes.csv`** — `rank, gene_symbol, ensembl_id, gene_name, overall_association_score, datatype_scores` (the last column shows the per-evidence-type breakdown so you can see *why* a gene ranked where it did — genetics vs. literature vs. drug evidence, etc.)
- **`enrichment_results.csv`** — `library, path_name, overlapping_genes, p_val, adj_p_val, combined_score`, filtered to adj-p < 0.05 and sorted by significance, spanning GO-BP, KEGG, Reactome, MSigDB Hallmark, and DisGeNET in one file (filter by the `library` column, or split into per-library sheets on export)

Plus `provenance.json` recording the resolved EFO ID, package versions, a SHA-256 of each output CSV, and whether the positive-control check passed — so you (or a reviewer) can audit exactly what produced these numbers.

**Honesty note:** I could not execute this against the live APIs in this sandboxed session (network egress and file-write were both blocked), so I have not fabricated example output rows — running the command above on your machine is what gets you the real, current numbers. If you swap in a different disease name, that's the only line you need to change.