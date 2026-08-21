This sandbox won't let me write files or make network calls without an approval step that isn't completing here, so I'll deliver the full recipe and code inline instead — same content, just as text you can paste into your own environment where those actions aren't blocked.

## The recipe (matched from the knowledge base, not composed from scratch)

**Recipe:** `map-disease-to-genes-and-pathways` — evidence level **Reported** (documented field test with a built-in positive-control check), availability **fully open** (no subscription/institutional access needed), compute **laptop-tier** (HTTP calls only, ~1–2 min for a 30-gene run). This is a rung-3 assembly (a small toolbelt, no autonomous system needed — a system like Biomni would be overkill for a lookup + stats job like this).

**Assumption** (stated per your instructions, since you didn't name a disease): I'm demonstrating with **"type 2 diabetes mellitus"**, exactly as you suggested. The script below takes the disease name as a CLI argument, so swap it for anything else.

**Chain:**
1. **Open Targets Platform GraphQL API** — resolves the disease name to an EFO id, then pulls the top-N targets ranked by Open Targets' own overall association score (an evidence-weighted composite across genetic, literature, and functional-genomics data — documented, not invented).
2. **`gget enrichr`** (a thin, open-source client around the real Enrichr statistical service) — runs a hypergeometric over-representation test with Benjamini-Hochberg FDR correction against `GO_Biological_Process_2023`, `KEGG_2021_Human`, and `Reactome_2022`.
3. **Positive-control check** — re-runs the same gene list against the DisGeNET library and confirms the original disease resurfaces as a top term. If it doesn't, that's a signal the disease-name resolution went wrong, and you should distrust the enrichment table until you fix it.
4. Two CSVs, each row backed by a real statistic — no LLM-generated numbers anywhere in either table. An LLM may narrate the CSVs afterward, but every number in them comes from Open Targets' or Enrichr's own engines.

**Caveats from the recipe's own notes:** the Open Targets *MCP* endpoint is currently non-functional — use the GraphQL API directly (which is what the script below does). Commercial users should check Enrichr's and KEGG's licensing terms before commercial use; everything else here is CC0/BSD/free.

## The artifact

`requirements.txt`
```
gget>=0.28.0
pandas>=2.0
requests>=2.31
```

`disease_to_pathways.py`
```python
#!/usr/bin/env python3
"""
Disease -> ranked genes -> GO/KEGG/Reactome enrichment, as two exportable tables.

Stage 1 (deterministic lookup, no model involved):
    Free-text disease name -> EFO id (Open Targets GraphQL search)
    -> top-N associated targets ranked by Open Targets' overall association score.

Stage 2 (deterministic statistics, no model involved):
    Gene list -> Enrichr over-representation test (via the `gget` client) against
    GO_Biological_Process_2023 / KEGG_2021_Human / Reactome_2022, each term carrying
    a p-value, BH-adjusted p-value (FDR), gene ratio, and overlapping genes.

Nothing in either stage is LLM-generated. A model may narrate the two output CSVs
afterward, but the numbers themselves come from Open Targets' and Enrichr's own
statistics engines.

Usage:
    python disease_to_pathways.py "type 2 diabetes mellitus"
    python disease_to_pathways.py "type 2 diabetes mellitus" --top-n 30 --outdir out/

Requires: pip install -r requirements.txt
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

OPEN_TARGETS_API = "https://api.platform.opentargets.org/api/v4/graphql"
ENRICHR_LIBRARIES = ["GO_Biological_Process_2023", "KEGG_2021_Human", "Reactome_2022"]
POSITIVE_CONTROL_LIBRARY = "DisGeNET"

SEARCH_QUERY = """
query SearchDisease($q: String!) {
  search(queryString: $q, entityNames: ["disease"], page: {index: 0, size: 5}) {
    hits {
      id
      name
      entity
    }
  }
}
"""

TARGETS_QUERY = """
query DiseaseTargets($efoId: String!, $size: Int!) {
  disease(efoId: $efoId) {
    id
    name
    associatedTargets(page: {index: 0, size: $size}) {
      count
      rows {
        score
        target {
          id
          approvedSymbol
        }
      }
    }
  }
}
"""

META_QUERY = """
query Meta {
  meta {
    apiVersion { major minor patch }
    dataVersion { year month iteration }
  }
}
"""


def _graphql(query, variables):
    resp = requests.post(OPEN_TARGETS_API, json={"query": query, "variables": variables}, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    if "errors" in payload:
        raise RuntimeError(f"Open Targets GraphQL error: {json.dumps(payload['errors'], indent=2)}")
    return payload["data"]


def resolve_disease(disease_name):
    data = _graphql(SEARCH_QUERY, {"q": disease_name})
    hits = [h for h in data["search"]["hits"] if h["entity"] == "disease"]
    if not hits:
        raise RuntimeError(f"No Open Targets disease match for '{disease_name}'. Try an EFO/MONDO id directly.")
    top = hits[0]
    print(f"Resolved '{disease_name}' -> {top['name']} ({top['id']})", file=sys.stderr)
    if len(hits) > 1:
        alts = ", ".join(f"{h['name']} ({h['id']})" for h in hits[1:])
        print(f"  (other candidates ignored: {alts})", file=sys.stderr)
    return top["id"], top["name"]


def fetch_ranked_genes(efo_id, top_n):
    data = _graphql(TARGETS_QUERY, {"efoId": efo_id, "size": top_n})
    rows = data["disease"]["associatedTargets"]["rows"]
    total = data["disease"]["associatedTargets"]["count"]
    print(f"Open Targets reports {total} total associated targets; keeping top {len(rows)}.", file=sys.stderr)
    records = []
    for rank, row in enumerate(rows, start=1):
        records.append(
            {
                "rank": rank,
                "gene": row["target"]["approvedSymbol"],
                "ensembl_id": row["target"]["id"],
                "association_score": round(row["score"], 4),
                "source_database": "Open Targets Platform (GraphQL API v4)",
            }
        )
    return pd.DataFrame(records)


def get_open_targets_version():
    try:
        data = _graphql(META_QUERY, {})
        v = data["meta"]["apiVersion"]
        d = data["meta"]["dataVersion"]
        return f"api {v['major']}.{v['minor']}.{v['patch']}, data {d['year']}.{d['month']}.{d['iteration']}"
    except Exception as exc:  # provenance is best-effort, never fatal
        return f"unknown ({exc})"


_ID_PATTERNS = [
    re.compile(r"\bGO:\d{7}\b"),
    re.compile(r"\bR-HSA-\d+\b"),
    re.compile(r"\bhsa\d{5}\b", re.IGNORECASE),
]


def extract_term_id(term_name):
    for pattern in _ID_PATTERNS:
        m = pattern.search(term_name)
        if m:
            return m.group(0)
    return ""


def run_enrichment(genes, libraries):
    import gget

    frames = []
    for library in libraries:
        df = gget.enrichr(genes, database=library, species="human", plot=False)
        if df is None or df.empty:
            print(f"  {library}: no significant/returned terms", file=sys.stderr)
            continue
        df = df.copy()
        df["source"] = library
        frames.append(df)
        print(f"  {library}: {len(df)} terms returned", file=sys.stderr)

    if not frames:
        raise RuntimeError("Enrichr returned no results for any library — check gene symbols and connectivity.")

    combined = pd.concat(frames, ignore_index=True)

    name_col = "path_name" if "path_name" in combined.columns else "term"
    pval_col = "p_val" if "p_val" in combined.columns else "p_value"
    adj_col = "adj_p_val" if "adj_p_val" in combined.columns else "adj_p_value"
    overlap_genes_col = "overlapping_genes" if "overlapping_genes" in combined.columns else "genes"

    out = pd.DataFrame()
    out["term_id"] = combined[name_col].apply(extract_term_id)
    out["term_name"] = combined[name_col]
    out["source"] = combined["source"]
    out["p_value"] = combined[pval_col]
    out["adj_p_value"] = combined[adj_col]

    def gene_count(v):
        if isinstance(v, (list, tuple)):
            return len(v)
        if isinstance(v, str):
            return len([g for g in v.split(";") if g])
        return 0

    out["overlap_gene_count"] = combined[overlap_genes_col].apply(gene_count)
    out["gene_ratio"] = out["overlap_gene_count"] / len(genes)
    out["overlapping_genes"] = combined[overlap_genes_col].apply(
        lambda v: ";".join(v) if isinstance(v, (list, tuple)) else v
    )

    out = out.sort_values("adj_p_value").reset_index(drop=True)
    return out


def validate_positive_control(genes, disease_name):
    """Sanity check: does the enrichment recover the disease we started from?"""
    import gget

    try:
        df = gget.enrichr(genes, database=POSITIVE_CONTROL_LIBRARY, species="human", plot=False)
    except Exception as exc:
        print(f"Positive-control check skipped ({exc})", file=sys.stderr)
        return None

    if df is None or df.empty:
        print("Positive-control check: DisGeNET returned no terms — cannot confirm mapping.", file=sys.stderr)
        return False

    name_col = "path_name" if "path_name" in df.columns else "term"
    disease_tokens = set(re.findall(r"[a-z0-9]+", disease_name.lower()))
    hit = df[name_col].str.lower().apply(lambda t: len(disease_tokens & set(re.findall(r"[a-z0-9]+", t))) >= 2)
    passed = bool(hit.any())
    print(
        f"Positive-control check: original disease {'DOES' if passed else 'does NOT'} resurface "
        f"in top DisGeNET terms for this gene list.",
        file=sys.stderr,
    )
    return passed


def sha256_of(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("disease", nargs="?", default="type 2 diabetes mellitus",
                         help="Disease name, EFO id, or MONDO id (default: 'type 2 diabetes mellitus', for demo)")
    parser.add_argument("--top-n", type=int, default=30, help="Number of top-ranked genes to carry into enrichment")
    parser.add_argument("--outdir", type=Path, default=Path("output"), help="Directory to write CSVs + provenance")
    parser.add_argument("--libraries", nargs="+", default=ENRICHR_LIBRARIES,
                         help="Enrichr library names to query (default: GO BP 2023, KEGG 2021 Human, Reactome 2022)")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    run_started = datetime.now(timezone.utc).isoformat()

    efo_id, resolved_name = resolve_disease(args.disease)
    genes_df = fetch_ranked_genes(efo_id, args.top_n)
    genes_path = args.outdir / "table1_genes.csv"
    genes_df.to_csv(genes_path, index=False)
    print(f"Wrote {genes_path} ({len(genes_df)} genes)", file=sys.stderr)

    gene_list = genes_df["gene"].tolist()
    print(f"Running Enrichr over {len(gene_list)} genes against {args.libraries} ...", file=sys.stderr)
    enrichment_df = run_enrichment(gene_list, args.libraries)
    enrichment_path = args.outdir / "table2_pathways.csv"
    enrichment_df.to_csv(enrichment_path, index=False)
    print(f"Wrote {enrichment_path} ({len(enrichment_df)} terms)", file=sys.stderr)

    positive_control_passed = validate_positive_control(gene_list, resolved_name)

    try:
        import gget
        gget_version = gget.__version__
    except Exception:
        gget_version = "unknown"

    provenance = {
        "run_started_utc": run_started,
        "query": {
            "disease_input": args.disease,
            "resolved_efo_id": efo_id,
            "resolved_disease_name": resolved_name,
            "top_n_genes": args.top_n,
        },
        "sources": {
            "open_targets_endpoint": OPEN_TARGETS_API,
            "open_targets_version": get_open_targets_version(),
            "enrichr_libraries": args.libraries,
            "gget_version": gget_version,
        },
        "positive_control": {
            "library": POSITIVE_CONTROL_LIBRARY,
            "disease_resurfaced": positive_control_passed,
        },
        "python_version": sys.version,
        "outputs": {
            "table1_genes.csv": {"rows": len(genes_df), "sha256": sha256_of(genes_path)},
            "table2_pathways.csv": {"rows": len(enrichment_df), "sha256": sha256_of(enrichment_path)},
        },
    }
    provenance_path = args.outdir / "provenance.json"
    provenance_path.write_text(json.dumps(provenance, indent=2))
    print(f"Wrote {provenance_path}", file=sys.stderr)

    if positive_control_passed is False:
        print(
            "\nWARNING: positive-control check failed — '{}' did not resurface in DisGeNET terms for its own "
            "top genes. Treat the enrichment result with caution; re-check the disease-name resolution above.".format(
                resolved_name
            ),
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
```

Run it with:
```bash
pip install -r requirements.txt
python disease_to_pathways.py "type 2 diabetes mellitus" --top-n 30 --outdir out/
```

## What you get, and why you can trust it

- **`table1_genes.csv`**: `rank, gene, ensembl_id, association_score, source_database` — every score is Open Targets' own composite association score, not a model guess.
- **`table2_pathways.csv`**: `term_id, term_name, source, p_value, adj_p_value, overlap_gene_count, gene_ratio, overlapping_genes` — real hypergeometric/Fisher's-exact statistics with BH-FDR correction, computed by Enrichr, sorted by adjusted p-value.
- **`provenance.json`**: API endpoint + Open Targets data version, `gget` version, resolved EFO id, positive-control result, and SHA-256 hashes of both CSVs — so a rerun months from now can be checked for drift, and anyone downstream can audit exactly what produced the tables.
- The one non-statistical step is the disease→EFO name resolution (a fuzzy text search) — that's why the positive-control check exists: it independently confirms the mapping was sane before you trust the enrichment table built on it.

If you want an LLM-written narrative on top of these two tables afterward, that's a separate, clearly-labeled step — hand it the CSVs and tell it to cite only rows with `adj_p_value < 0.05` and to never name a gene or term that isn't in the file.

**Two things I couldn't do in this sandboxed session:** I couldn't reach the Open Targets/Enrichr APIs or write files here (network and file-write both require an approval step that didn't go through), so I haven't actually run this for you — the tables above are the *schema*, not fabricated numbers. Run it locally and it will hit real APIs and produce real statistics.