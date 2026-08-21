I'll present the complete solution directly in this response instead, since file-write access isn't available here.

## Recipe match

Your problem matches a curated recipe: **[Find selective genetic dependencies for a cancer context with DepMap](find-selective-cancer-dependencies-with-depmap)**.

- **Evidence:** Reported — this contrast strategy underlies published work (Schneider et al. 2024 on *ATP1B3* as an *ATP1B1*-paralog dependency in AML; Iyer et al. 2025 on *SUMO2* as a synovial-sarcoma fusion-context dependency; Phillips et al. 2025 on *KIF18A* in CIN tumors, now in clinical trials). The underlying Chronos scoring and CN-correction methodology follows Behan et al. 2019 / Dempster et al. 2021.
- **Availability:** Fully open — DepMap data is public (academic + commercial use), no API key, all computation local.
- **Compute:** Laptop-sufficient — ~1,000 lines × ~18,000 genes with BH correction runs in under a minute on 8 GB RAM once the ~200–400 MB matrices are cached.

## Assumptions (single-shot, stated explicitly)

Since you can't confirm follow-ups, I picked the concrete example and locked in these choices — swap them in the script's arguments if they don't match your real case:

- **Context:** SS18::SSX fusion-positive synovial sarcoma cell lines vs. all other profiled lines.
- **Fusion definition:** DepMap does **not** reliably call gene fusions in every quarterly release (`OmicsFusionFiltered.csv` exists in some releases with a schema that has changed over time). I default to a **subtype proxy** — `OncotreeSubtype` containing "Synovial Sarcoma" — since essentially all synovial sarcomas carry SS18::SSX. The script also supports a direct fusion-call path if your release has the file, but flags column-name mismatches rather than guessing.
- **DepMap release:** I did not verify the current quarterly label from a live download (no network fetch performed this session). Pin whatever you actually download — the script hashes it — and record the label explicitly (example placeholder used below: `24Q4`). Check the DepMap Portal's "Data Downloads" page for the current release before running.

## The pipeline

**Files needed** (from the DepMap Portal, figshare-hosted per quarterly release):
`CRISPRGeneEffect.csv`, `OmicsExpressionProteinCodingGenesTPMLogp1.csv`, `OmicsCNGene.csv`, `Model.csv`, optionally `OmicsFusionFiltered.csv`.

**Statistics, and why:**
- **Two-sided Mann-Whitney U** per gene, not a t-test, because Chronos scores are often skewed/non-normal per gene and group sizes for rare contexts (e.g. synovial sarcoma, typically only ~5–15 lines in DepMap) are too small to trust normality.
- **Effect size** = context mean − background mean Chronos score (more negative = more selectively essential) — reported alongside the p-value so you're not ranking by significance alone, which is dominated by group-size noise at small n.
- **Benjamini-Hochberg FDR** across all ~18,000 tested genes — mandatory; uncorrected p-values will overstate significance by orders of magnitude at this scale.
- **Pan-essential filter**: drop genes with background mean Chronos ≤ −0.5 (ribosome, proteasome, spliceosome, etc.) — these will always look "significant" against any group and are not actionable targets.
- **Copy-number artifact flag**: CRISPR cutting in amplified DNA produces a dose-dependent apparent dependency that mimics real biology. The script flags a gene when *either* (a) the context group has meaningfully higher mean copy number at that locus than background, or (b) within the context group alone, gene effect correlates negatively with copy number (Spearman ρ < −0.5) — the classic signature of a cutting artifact rather than a genotype-driven dependency. This is a **flag, not an automatic exclusion** (per the recipe's explicit caveat) — inspect flagged top hits manually rather than silently dropping them, since a truly amplified oncogene can be both CN-elevated and a real dependency.
- **Reproducibility**: every input matrix is SHA-256-hashed, and the release label, group definitions, and thresholds are written to `provenance.json` alongside the ranked `dependencies.csv`. Without that file, re-running against a newer quarterly release will silently change the ranking.

**Runnable script** (`find_dependencies.py` — commit this, don't just eyeball a ranking in chat):

```python
#!/usr/bin/env python3
"""
Rank genes by selective CRISPR dependency in a cancer context, using DepMap
public data. Compares a context group of cell lines (e.g. SS18::SSX
fusion-positive synovial sarcoma) against all other profiled lines, corrects
for multiple testing, drops pan-essential genes, and flags genes whose
apparent dependency tracks copy-number amplification rather than real
biology.

Usage
-----
python find_dependencies.py \
    --data-dir ./depmap_24Q4 --release-label 24Q4 \
    --context-mode subtype --subtype "Synovial Sarcoma" \
    --out-prefix synovial_sarcoma

python find_dependencies.py \
    --data-dir ./depmap_24Q4 --release-label 24Q4 \
    --context-mode low-expression --gene ATP1B1 --percentile 20 \
    --out-prefix low_ATP1B1
"""
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

PAN_ESSENTIAL_THRESHOLD = -0.5   # background mean Chronos <= this -> dropped
CN_DELTA_THRESHOLD = 0.5         # context_mean_cn - background_mean_cn above
                                  # this (linear copy-ratio units) flags a
                                  # possible CN-driven artifact
CN_CORR_THRESHOLD = -0.5         # within-context Spearman(gene_effect, CN)
                                  # below this also flags a cutting artifact
MIN_GROUP_SIZE = 10
MIN_VIABLE_GROUP_SIZE = 3

FILES = {
    "effect": "CRISPRGeneEffect.csv",
    "expression": "OmicsExpressionProteinCodingGenesTPMLogp1.csv",
    "cn": "OmicsCNGene.csv",
    "model": "Model.csv",
    "fusion": "OmicsFusionFiltered.csv",  # optional, schema varies by release
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_gene_id(col: str) -> str:
    return re.sub(r"\s*\(\d+\)\s*$", "", col).strip()


def load_matrix(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0)
    df.columns = [strip_gene_id(c) for c in df.columns]
    return df


def load_model(data_dir: Path) -> pd.DataFrame:
    path = data_dir / FILES["model"]
    if not path.exists():
        path = data_dir / "sample_info.csv"
    if not path.exists():
        sys.exit(f"Could not find Model.csv or sample_info.csv in {data_dir}")
    df = pd.read_csv(path)
    id_col = "ModelID" if "ModelID" in df.columns else "DepMap_ID"
    return df.set_index(id_col)


def load_inputs(data_dir: Path, need_fusion: bool):
    resolved, hashes = {}, {}
    for key in ("effect", "expression", "cn"):
        p = data_dir / FILES[key]
        if not p.exists():
            sys.exit(f"Missing required file: {p}")
        hashes[key] = sha256_file(p)
        resolved[key] = load_matrix(p)

    model_path = data_dir / FILES["model"]
    if not model_path.exists():
        model_path = data_dir / "sample_info.csv"
    hashes["model"] = sha256_file(model_path)
    resolved["model"] = load_model(data_dir)

    fusion_df = None
    fusion_path = data_dir / FILES["fusion"]
    if fusion_path.exists():
        hashes["fusion"] = sha256_file(fusion_path)
        fusion_df = pd.read_csv(fusion_path)
    elif need_fusion:
        sys.exit(
            f"--context-mode fusion requires {fusion_path}, not found. Use "
            "--context-mode subtype as a proxy instead."
        )
    return resolved, fusion_df, hashes


def define_groups(args, model_df, expr_df, fusion_df):
    if args.context_mode == "subtype":
        col = "OncotreeSubtype" if "OncotreeSubtype" in model_df.columns else "SubtypeName"
        if col not in model_df.columns:
            sys.exit(f"No subtype column found. Columns: {list(model_df.columns)}")
        context_ids = model_df.index[model_df[col].astype(str).str.contains(args.subtype, case=False, na=False)]
        criterion = f"{col} contains '{args.subtype}'"

    elif args.context_mode == "fusion":
        genes = {g.strip().upper() for g in args.fusion_genes.split(",")}
        left_col = next((c for c in ("LeftGene", "leftGene") if c in fusion_df.columns), None)
        right_col = next((c for c in ("RightGene", "rightGene") if c in fusion_df.columns), None)
        if left_col is None or right_col is None:
            sys.exit(f"Fusion partner columns not found. Columns: {list(fusion_df.columns)} -- fix manually, don't guess.")
        id_col = "ModelID" if "ModelID" in fusion_df.columns else "DepMap_ID"
        hit = fusion_df[fusion_df[left_col].astype(str).str.upper().isin(genes) &
                         fusion_df[right_col].astype(str).str.upper().isin(genes)]
        context_ids = pd.Index(hit[id_col].unique())
        criterion = f"fusion between {sorted(genes)}"

    elif args.context_mode == "low-expression":
        if args.gene not in expr_df.columns:
            sys.exit(f"{args.gene} not found in expression matrix")
        vals = expr_df[args.gene].dropna()
        cutoff = np.percentile(vals, args.percentile)
        context_ids = vals.index[vals <= cutoff]
        criterion = f"{args.gene} log2(TPM+1) <= {args.percentile}th pct ({cutoff:.3f})"
    else:
        sys.exit(f"Unknown --context-mode {args.context_mode}")

    context_ids = pd.Index(context_ids).intersection(model_df.index)
    background_ids = model_df.index.difference(context_ids)
    return context_ids, background_ids, criterion


def run_contrast(effect_df, cn_df, context_ids, background_ids):
    context_ids = context_ids.intersection(effect_df.index)
    background_ids = background_ids.intersection(effect_df.index)
    rows = []
    for i, gene in enumerate(effect_df.columns):
        if i % 2000 == 0:
            print(f"  ...{i}/{len(effect_df.columns)} genes", file=sys.stderr)
        ctx = effect_df.loc[context_ids, gene].dropna()
        bg = effect_df.loc[background_ids, gene].dropna()
        if len(ctx) < 2 or len(bg) < 2:
            continue
        context_mean, background_mean = ctx.mean(), bg.mean()
        try:
            _, p = stats.mannwhitneyu(ctx, bg, alternative="two-sided")
        except ValueError:
            p = np.nan

        cn_flag = False
        if gene in cn_df.columns:
            ctx_cn = cn_df.loc[cn_df.index.intersection(ctx.index), gene].dropna()
            bg_cn = cn_df.loc[cn_df.index.intersection(bg.index), gene].dropna()
            if len(ctx_cn) >= 3 and len(bg_cn) >= 3:
                cn_delta = ctx_cn.mean() - bg_cn.mean()
                joint = pd.concat([ctx, ctx_cn], axis=1, join="inner")
                joint.columns = ["effect", "cn"]
                corr = np.nan
                if len(joint) >= 5 and joint["cn"].std() > 0:
                    corr, _ = stats.spearmanr(joint["effect"], joint["cn"])
                cn_flag = bool((cn_delta > CN_DELTA_THRESHOLD) or
                               (not np.isnan(corr) and corr < CN_CORR_THRESHOLD))

        rows.append(dict(gene=gene, context_mean=context_mean, background_mean=background_mean,
                          selective_effect=context_mean - background_mean, p=p,
                          copy_number_flag=cn_flag, n_context=len(ctx), n_background=len(bg)))

    result = pd.DataFrame(rows)
    valid = result["p"].notna()
    result["fdr"] = np.nan
    result.loc[valid, "fdr"] = multipletests(result.loc[valid, "p"], method="fdr_bh")[1]
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--release-label", required=True)
    ap.add_argument("--context-mode", required=True, choices=["subtype", "fusion", "low-expression"])
    ap.add_argument("--subtype")
    ap.add_argument("--fusion-genes")
    ap.add_argument("--gene")
    ap.add_argument("--percentile", type=float, default=20.0)
    ap.add_argument("--out-prefix", required=True)
    args = ap.parse_args()

    data, fusion_df, hashes = load_inputs(args.data_dir, args.context_mode == "fusion")
    context_ids, background_ids, criterion = define_groups(args, data["model"], data["expression"], fusion_df)

    print(f"Context: {len(context_ids)} lines. Background: {len(background_ids)} lines.", file=sys.stderr)
    if len(context_ids) < MIN_VIABLE_GROUP_SIZE:
        sys.exit(f"Context group n={len(context_ids)} < {MIN_VIABLE_GROUP_SIZE}; refusing to run.")
    if len(context_ids) < MIN_GROUP_SIZE:
        print(f"WARNING: n={len(context_ids)} below recommended minimum {MIN_GROUP_SIZE}; treat as exploratory.", file=sys.stderr)

    result = run_contrast(data["effect"], data["cn"], context_ids, background_ids)
    n0 = len(result)
    result = result[result["background_mean"] > PAN_ESSENTIAL_THRESHOLD].copy()
    print(f"Dropped {n0 - len(result)} pan-essential genes.", file=sys.stderr)
    result = result.sort_values("selective_effect")

    out_csv = Path(f"{args.out_prefix}_dependencies.csv")
    result.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv} ({len(result)} genes).", file=sys.stderr)
    print(f"{int(result.head(100)['copy_number_flag'].sum())}/100 top hits CN-flagged -- inspect before trusting.", file=sys.stderr)

    provenance = {
        "depmap_release_label": args.release_label,
        "file_sha256": hashes,
        "context_definition": {"mode": args.context_mode, "criterion": criterion,
                                "n_context": int(len(context_ids)), "n_background": int(len(background_ids))},
        "thresholds": {"pan_essential_background_mean_chronos_le": PAN_ESSENTIAL_THRESHOLD,
                        "cn_delta_flag_gt": CN_DELTA_THRESHOLD,
                        "cn_within_group_spearman_flag_lt": CN_CORR_THRESHOLD,
                        "min_group_size_warning": MIN_GROUP_SIZE},
        "statistical_test": "two-sided Mann-Whitney U per gene; Benjamini-Hochberg FDR",
        "run_date_utc": datetime.now(timezone.utc).isoformat(),
    }
    Path(f"{args.out_prefix}_provenance.json").write_text(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    main()
```

**`requirements.txt`:**
```
pandas
numpy
scipy
statsmodels
```

## Practical guidance

- **Data source:** DepMap Portal (depmap.org) → Data Downloads → pick the current quarterly release (e.g. `24Q4`); files are figshare-hosted. Don't hardcode a download URL into a script you'll rerun later — releases move — but do hardcode the **label and hashes** once downloaded, which is what `provenance.json` does.
- **Power:** aim for ≥10 context lines; below 5 the contrast is unreliable and the script refuses below 3. Rare fusion contexts like SS18::SSX (synovial sarcoma has roughly 5–15 lines in DepMap depending on release) sit right at this boundary — treat any ranking here as hypothesis-generating, not confirmatory, and say so explicitly if you publish it.
- **Lineage confounding:** a naive context-vs-everyone-else contrast can surface genes that are really lineage/tissue dependencies (e.g. mesenchymal or sarcoma-general) rather than fusion-specific ones. If you want to isolate the fusion effect, restrict the background to other sarcoma lines (or add lineage as a covariate in a regression instead of a two-group test) and compare rankings — a gene that only shows up against "everyone" but disappears against "other sarcomas" is a lineage effect, not a fusion effect.
- **CN flag is not a filter:** the script reports `copy_number_flag`; it does not drop those rows, because a real oncogenic amplicon dependency can also be CN-elevated. Manually cross-check flagged top hits against known biology (paralog of a silenced gene? lineage TF? synthetic-lethal partner of the driver?) before shortlisting.
- **Next steps:** feed the surviving top genes into a target-dossier workflow (structure, disease association, existing inhibitors) and then into CRISPR sgRNA design for wet-lab validation — a selective dependency ranking is a hypothesis list, not a validated target list.