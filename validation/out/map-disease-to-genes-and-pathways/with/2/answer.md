File writes aren't approved in this environment either, so I'll deliver everything inline as the chat response instead — a complete, copy-pasteable recipe.

## The answer: a curated recipe already exists for exactly this — `map-disease-to-genes-and-pathways`

**Evidence:** Reported (field-tested on knee osteoarthritis; inherits peer-reviewed evidence from its components) · **Availability:** Fully open, no API key · **Compute:** Laptop (HTTP calls only, ~1–2 min for 30 genes)

**Why not a lower rung:** a plain prompt to Claude would hallucinate gene rankings and p-values — you explicitly need real statistics, so this must call live databases, not model memory.

**Assumption** (none specified): disease = **Parkinson's disease**.

### Step 1 — Disease → ranked genes: Open Targets

Query the free, unauthenticated Open Targets GraphQL API (`https://api.platform.opentargets.org/api/v4/graphql`, data is CC0):
1. `search` query to resolve "Parkinson's disease" → EFO id (e.g. `EFO_0002508`).
2. `disease(efoId).associatedTargets` query, sorted by **overall association score** (Open Targets' own weighted combination of genetic, literature, RNA expression, and other datatype scores) → top ~30 target gene symbols.

This gives you **Table 1**: `rank, gene_symbol, ensembl_id, gene_name, overall_association_score, datatype_scores` — a real, sourced, numeric ranking, not an LLM guess.

### Step 2 — Genes → pathways: Enrichr (via `gget enrichr` or the raw API)

POST the gene list to Enrichr (`https://maayanlab.cloud/Enrichr`, free for academic/nonprofit use) against:
- `GO_Biological_Process_2023`
- `KEGG_2021_Human`
- `Reactome_2022`
- `MSigDB_Hallmark_2020`
- `DisGeNET` (used as a sanity check, see below)

Enrichr runs a real Fisher's-exact test per term against its gene-set library and returns p-value, **BH-adjusted p-value**, combined score, and the exact overlapping genes. That's **Table 2**: `database, term, p_value, adjusted_p_value, combined_score, z_score, gene_count, overlap_genes`.

The easiest path if you're in Claude Code: install `gget` (`pip install gget`) and call `gget.enrichr(genes, database=...)`, which wraps this API and returns a pandas DataFrame per library — trivially exportable with `.to_csv()`.

### Step 3 — Positive control (don't skip this)

Check that "Parkinson" resurfaces as a significant term in the DisGeNET enrichment results. If it doesn't, your gene symbols likely failed to map (wrong species, stale aliases, etc.) — treat the enrichment table as untrustworthy until this passes.

### Step 4 — Grounded synthesis, not paraphrase

Only let an LLM summarize terms with `adjusted_p_value < 0.05`, and only by quoting rows from the saved CSVs — never by describing "what it thinks" the pathways are. Run a verification pass that checks every claim in the summary traces back to an actual CSV row.

### Runnable script

I tried to write this to disk and execute it against the live APIs as the reproducible artifact of record (per this environment's own capture step), but both file-write and shell-execution permissions were declined automatically in this non-interactive session — so here it is as a self-contained script you can paste into `analysis.py` and run yourself:

```python
#!/usr/bin/env python3
"""Disease -> ranked genes (Open Targets) -> enrichment (Enrichr GO/KEGG/Reactome)."""
import argparse, csv, hashlib, json, sys, urllib.parse
from pathlib import Path
import requests

OPENTARGETS_API = "https://api.platform.opentargets.org/api/v4/graphql"
ENRICHR_ADD_LIST = "https://maayanlab.cloud/Enrichr/addList"
ENRICHR_ENRICH = "https://maayanlab.cloud/Enrichr/enrich"
LIBRARIES = ["GO_Biological_Process_2023", "KEGG_2021_Human", "Reactome_2022",
             "MSigDB_Hallmark_2020", "DisGeNET"]

SEARCH_QUERY = """
query($q: String!) {
  search(queryString: $q, entityNames: ["disease"], page: {index: 0, size: 5}) {
    hits { id name entity }
  }
}"""

ASSOC_QUERY = """
query($efoId: String!, $size: Int!) {
  disease(efoId: $efoId) {
    name
    associatedTargets(page: {index: 0, size: $size}) {
      rows {
        score
        target { id approvedSymbol approvedName }
        datatypeScores { id score }
      }
    }
  }
}"""

def resolve_disease(q, s):
    r = s.post(OPENTARGETS_API, json={"query": SEARCH_QUERY, "variables": {"q": q}}, timeout=30)
    r.raise_for_status()
    hits = [h for h in r.json()["data"]["search"]["hits"] if h["entity"] == "disease"]
    if not hits:
        raise SystemExit(f"No Open Targets match for {q!r}")
    return hits[0]

def fetch_targets(efo_id, s, top_n):
    r = s.post(OPENTARGETS_API, json={"query": ASSOC_QUERY, "variables": {"efoId": efo_id, "size": top_n}}, timeout=30)
    r.raise_for_status()
    d = r.json()["data"]["disease"]
    rows = [{
        "gene_symbol": row["target"]["approvedSymbol"],
        "ensembl_id": row["target"]["id"],
        "gene_name": row["target"]["approvedName"],
        "overall_association_score": row["score"],
        "datatype_scores": json.dumps({x["id"]: x["score"] for x in row["datatypeScores"]}),
    } for row in d["associatedTargets"]["rows"]]
    return d["name"], rows

def run_enrichr(genes, description, s):
    r = s.post(ENRICHR_ADD_LIST, files={"list": (None, "\n".join(genes)), "description": (None, description)}, timeout=30)
    r.raise_for_status()
    list_id = r.json()["userListId"]
    out = []
    for lib in LIBRARIES:
        params = urllib.parse.urlencode({"userListId": list_id, "backgroundType": lib})
        rr = s.get(f"{ENRICHR_ENRICH}?{params}", timeout=30)
        rr.raise_for_status()
        for row in rr.json().get(lib, []):
            out.append({"database": lib, "term": row[1], "p_value": row[2], "z_score": row[3],
                        "combined_score": row[4], "overlap_genes": ";".join(row[5]),
                        "gene_count": len(row[5]), "adjusted_p_value": row[6], "rank_in_library": row[0]})
    return list_id, out

def positive_control(disease_name, rows):
    terms = [r["term"].lower() for r in rows if r["database"] == "DisGeNET" and r["adjusted_p_value"] < 0.05]
    toks = [t for t in disease_name.lower().replace("'s", "").split() if len(t) > 3]
    return any(any(t in term for t in toks) for term in terms), terms[:10]

def write_csv(path, rows, fields):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

def sha256(path):
    h = hashlib.sha256(); h.update(open(path, "rb").read()); return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("disease")
    ap.add_argument("--top-n", type=int, default=30)
    ap.add_argument("--outdir", default="output")
    args = ap.parse_args()
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    s = requests.Session(); s.headers.update({"User-Agent": "disease-to-pathways/1.0"})

    hit = resolve_disease(args.disease, s)
    name, genes = fetch_targets(hit["id"], s, args.top_n)
    genes.sort(key=lambda r: r["overall_association_score"], reverse=True)
    for i, r in enumerate(genes, 1): r["rank"] = i
    genes_csv = outdir / "gene_disease_associations.csv"
    write_csv(genes_csv, genes, ["rank", "gene_symbol", "ensembl_id", "gene_name",
                                 "overall_association_score", "datatype_scores"])

    symbols = [g["gene_symbol"] for g in genes if g["gene_symbol"]]
    list_id, enrich = run_enrichr(symbols, f"{hit['id']}_{args.disease}", s)
    enrich.sort(key=lambda r: r["adjusted_p_value"])
    enrich_csv = outdir / "enrichment_results.csv"
    write_csv(enrich_csv, enrich, ["database", "term", "p_value", "adjusted_p_value",
                                   "combined_score", "z_score", "gene_count",
                                   "overlap_genes", "rank_in_library"])

    ok, hits = positive_control(args.disease, enrich)
    prov = {
        "recipe": "map-disease-to-genes-and-pathways",
        "query": {"disease_input": args.disease, "resolved_efo_id": hit["id"], "resolved_name": name, "top_n": args.top_n},
        "sources": {
            "gene_disease_association": {"provider": "Open Targets Platform", "endpoint": OPENTARGETS_API, "license": "CC0"},
            "enrichment": {"provider": "Enrichr", "endpoint": ENRICHR_ENRICH, "libraries": LIBRARIES, "user_list_id": list_id},
        },
        "positive_control": {"passed": ok, "matching_disgenet_terms": hits},
        "outputs": {
            "gene_disease_associations.csv": {"n_rows": len(genes), "sha256": sha256(genes_csv)},
            "enrichment_results.csv": {"n_rows": len(enrich), "sha256": sha256(enrich_csv)},
        },
    }
    json.dump(prov, open(outdir / "provenance.json", "w"), indent=2)
    print(f"positive control: {'PASS' if ok else 'FAIL - check symbol mapping'}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

Run it with:
```
pip install requests
python3 analysis.py "Parkinson's disease" --top-n 30
```

This produces `output/gene_disease_associations.csv`, `output/enrichment_results.csv`, and `output/provenance.json` (endpoint versions, resolved EFO id, positive-control result, and a SHA-256 of each output for audit).

### If you outgrow this
If you later need per-datasource evidence breakdowns (genetics vs. literature vs. animal models) rather than one overall score, the `prioritize-targets-within-a-disease` recipe (Open Targets' four-pillar prioritization: precedence/tractability/doability/safety) is the next step up — still rung 2, no need for a full autonomous system.

**Filing to the knowledge base:** since this matched an existing curated recipe on the first try, there's nothing to file as a gap. If you run this and it works as described, a one-line "worked as documented on Parkinson's disease" confirmation would let the curators promote it toward "Validated" — happy to draft that report if you want it in a future turn.