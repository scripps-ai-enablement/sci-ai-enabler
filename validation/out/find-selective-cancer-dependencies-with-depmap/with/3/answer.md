## Approach: DepMap-based selective dependency screen

### Assumptions (stated because this is single-shot)
- **Data release**: DepMap Public **24Q2** (pin whatever is your current latest quarterly release the same way — e.g. 25Q2 — the method doesn't change, only the file hashes).
- **Files used**: `Model.csv` (annotations/lineage), `CRISPRGeneEffect.csv` (Chronos gene effect scores, cell lines × genes), `OmicsSomaticMutationsMatrixFusion.csv` or `OmicsFusionFiltered.csv` (fusion calls), `OmicsExpressionProteinCodingGenesTPMLogp1.csv` (expression), `OmicsCNGene.csv` (relative copy number), plus DepMap's shipped `AchillesCommonEssentialControls.csv` and `AchillesNonessentialControls.csv`.
- **Context example**: SS18::SSX fusion-positive lines (synovial sarcoma) vs. all other profiled lines with usable Chronos scores. I'll also show the ATP1B1-low-expression variant since it's a continuous-cutoff case, not a categorical one.
- **Background**: all remaining lines by default; I'll note the lineage-matched alternative and when to prefer it.
- **Compute**: this is a pandas-scale problem (~1,100 lines × ~18,000 genes ≈ 20M cells, a few hundred MB) — no cluster needed, runs on a laptop in minutes.
- **Access**: you need a DepMap Figshare download (or the `depmap` R/Python API) — I'm not fetching data myself here.

---

### 1. Pin provenance before touching anything

Reproducibility failures in DepMap work almost always come from silently mixing releases. Fix this first:

```python
import hashlib, json, pathlib, datetime

DEPMAP_RELEASE = "24Q2"  # <-- change per your download, propagate everywhere below
DATA_DIR = pathlib.Path("data/depmap_24q2")

FILES = {
    "model":        "Model.csv",
    "gene_effect":  "CRISPRGeneEffect.csv",
    "fusions":      "OmicsFusionFiltered.csv",
    "expression":   "OmicsExpressionProteinCodingGenesTPMLogp1.csv",
    "copy_number":  "OmicsCNGene.csv",
    "common_ess":   "AchillesCommonEssentialControls.csv",
    "nonessential": "AchillesNonessentialControls.csv",
}

def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()

manifest = {
    "depmap_release": DEPMAP_RELEASE,
    "run_timestamp_utc": datetime.datetime.utcnow().isoformat(),
    "files": {k: {"name": v, "sha256": sha256(DATA_DIR / v)} for k, v in FILES.items()},
}
pathlib.Path("provenance_manifest.json").write_text(json.dumps(manifest, indent=2))
```

Write this manifest alongside every output table you produce, and check the hashes back against it before re-running an analysis someone hands you later — that's what actually makes "which version did I use" answerable months from now, not just the release string in a filename.

### 2. Load and align

```python
import pandas as pd

model = pd.read_csv(DATA_DIR / FILES["model"], index_col="ModelID")
effect = pd.read_csv(DATA_DIR / FILES["gene_effect"], index_col=0)   # rows=ModelID, cols="GENE (Entrez)"
fusions = pd.read_csv(DATA_DIR / FILES["fusions"])
expr = pd.read_csv(DATA_DIR / FILES["expression"], index_col=0)
cn = pd.read_csv(DATA_DIR / FILES["copy_number"], index_col=0)
common_ess = set(pd.read_csv(DATA_DIR / FILES["common_ess"])["Gene"])

common_lines = effect.index.intersection(model.index)
effect, model = effect.loc[common_lines], model.loc[common_lines]
```

### 3. Define context vs. background groups

**Categorical (fusion) case:**

```python
fusion_lines = set(
    fusions.loc[
        fusions["FusionName"].str.contains("SS18.*SSX|SSX.*SS18", regex=True, na=False),
        "ModelID"
    ]
)
context_ids = effect.index.intersection(fusion_lines)
background_ids = effect.index.difference(context_ids)
```

**Continuous (low-expression) case:**

```python
atp1b1_col = [c for c in expr.columns if c.startswith("ATP1B1 ")][0]
atp1b1 = expr[atp1b1_col].reindex(effect.index)
q25 = atp1b1.quantile(0.25)
context_ids = atp1b1[atp1b1 <= q25].index
background_ids = atp1b1[atp1b1 > q25].index
```

Enforce a minimum group size (`n_context >= 8–10`) before proceeding — DepMap has plenty of rare fusions with 3–4 lines, and a rank-based test on n=4 has essentially no power regardless of effect size; flag rather than silently run in that case.

**Lineage-matching note**: if the context group is concentrated in one or two lineages (true for SS18::SSX — almost all synovial sarcoma), an unmatched background will confound "fusion-selective" with "lineage-selective." Either (a) restrict background to the same broad lineage (sarcoma) as a sensitivity check, or (b) include lineage as a covariate — see step 4b.

### 4. Rank genes by selective effect, with correction

**4a. Primary test — Mann-Whitney U per gene**, because Chronos scores aren't guaranteed normal/homoscedastic and it's robust to outlier lines:

```python
from scipy import stats
import numpy as np

def score_gene(col):
    ctx = effect.loc[context_ids, col].dropna()
    bg = effect.loc[background_ids, col].dropna()
    if len(ctx) < 8 or len(bg) < 8:
        return None
    u, p = stats.mannwhitneyu(ctx, bg, alternative="less")  # "less": context more dependent (more negative)
    delta = ctx.mean() - bg.mean()
    # rank-biserial effect size, scale-free, comparable across genes
    rbc = 1 - (2 * u) / (len(ctx) * len(bg))
    return p, delta, rbc, len(ctx), len(bg)

results = {col: score_gene(col) for col in effect.columns}
results = {k: v for k, v in results.items() if v is not None}
df = pd.DataFrame(results, index=["p", "delta_mean", "rank_biserial", "n_ctx", "n_bg"]).T
```

**4b. Covariate-adjusted alternative** (recommended when lineage confounding is a real concern): fit `chronos_score ~ context_flag + lineage` with OLS per gene via `statsmodels`, take the context_flag coefficient and its p-value. Slower (~18k regressions) but handles the confound directly instead of by subsetting.

**Multiple testing correction**, BH-FDR across ~18,000 genes:

```python
from statsmodels.stats.multitest import multipletests
df["fdr"] = multipletests(df["p"], method="fdr_bh")[1]
df = df.sort_values(["fdr", "rank_biserial"])
```

Report both `delta_mean` (effect size, biologically interpretable — Chronos units) and `fdr` — significance alone will over-rank tiny-but-consistent effects from large groups; require something like `fdr < 0.1 AND delta_mean < -0.3` as your candidate threshold, not FDR alone.

### 5. Remove pan-essential genes

```python
df["pan_essential"] = df.index.isin(common_ess)
candidates = df[~df["pan_essential"]].copy()
```

Also worth a soft filter rather than hard exclusion: compute each gene's mean effect in the *background* group alone — if it's already below ~‑0.5 there, "selective" is marginal even if not on DepMap's curated common-essential list (that list is itself version-pinned and can lag).

```python
bg_mean = effect.loc[background_ids].mean()
candidates["bg_mean_effect"] = bg_mean.reindex(candidates.index)
candidates = candidates[candidates["bg_mean_effect"] > -0.5]
```

### 6. Flag copy-number amplification artifacts

Chronos models copy-number-driven cutting-toxicity globally and partially corrects for it, but residual artifacts persist for highly amplified genes in individual lines. Check directly rather than trusting the global correction:

```python
cn_aligned = cn.reindex(index=effect.index, columns=effect.columns)

def cn_artifact_check(gene):
    ctx_cn = cn_aligned.loc[context_ids, gene].dropna()
    ctx_eff = effect.loc[ctx_cn.index, gene]
    if len(ctx_cn) < 5:
        return np.nan, False
    r, _ = stats.spearmanr(ctx_cn, ctx_eff)
    high_cn_and_dependent = (ctx_cn > 2.0).any() and (ctx_eff[ctx_cn > 2.0].mean() < -0.5)
    return r, bool(high_cn_and_dependent and r < -0.3)

cn_flags = {g: cn_artifact_check(g) for g in candidates.index}
candidates["cn_spearman_r"], candidates["cn_artifact_flag"] = zip(*[cn_flags[g] for g in candidates.index])
```

Interpretation: a gene where dependency tracks copy number *within the context group itself* (strong negative Spearman r between CN and Chronos score, concentrated in high-CN lines) is a candidate to deprioritize or flag for manual review, not necessarily discard outright — some genuine oncogene dependencies (amplicon-driven, e.g. `MYC`-adjacent) are legitimately both amplified and selectively essential, so treat this as a flag surfaced in the output table, not a silent filter.

### 7. Final output

```python
final = candidates.sort_values(["fdr", "delta_mean"])
final.to_csv("selective_dependencies_SS18-SSX_24Q2.csv")
```

Columns: gene, p, fdr, delta_mean, rank_biserial, n_ctx, n_bg, pan_essential, bg_mean_effect, cn_spearman_r, cn_artifact_flag, plus the provenance manifest hash written as a header comment or sidecar file.

---

### Caveats (evidence / power / confounding)
- **Power**: rare-context screens (small `n_context`) have wide confidence intervals on `delta_mean` even at nominal significance — report n alongside every hit, and treat single-digit-n results as hypothesis-generating, not confirmed.
- **Confounding**: fusion-defined contexts are frequently lineage-restricted; always run the lineage-matched background as a sensitivity check before trusting an unmatched-background hit.
- **CN filter is heuristic**: it flags correlation, not causation — validate top hits against orthogonal evidence (RNAi data in DepMap for the same genes, or literature) before wet-lab follow-up.
- **This produces a ranked list, not a validated target** — treat rank 1–20 as a candidate list for orthogonal confirmation (e.g., competition assays, RNAi cross-check via `demeter2`), not a final answer.

This is a self-contained scripting task (no agent/autonomous system needed) — if useful, I can turn this into a parameterized CLI (`--context-def fusion:SS18-SSX` / `--context-def expr_quantile:ATP1B1:0.25`) so you can rerun it for other contexts without touching the code.