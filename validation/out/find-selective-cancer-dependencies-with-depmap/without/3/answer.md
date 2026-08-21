## Assumption

You didn't specify which DepMap release, which fusion-calling source, or which statistical framework to use, so I'll anchor the whole pipeline to one concrete, realistic case: **SS18::SSX1/2 fusion-positive synovial sarcoma cell lines** in **DepMap Public 24Q4** (CRISPR gene effect scores computed with **Chronos**), using the **Sanger/Broad-consensus fusion calls** distributed via DepMap's `Model.csv` + a curated fusion annotation (since fusions aren't in the standard `OmicsSomaticMutations` calls). This case is a good test of your pipeline because the answer is already known from the literature (BRD9 — Brien et al. 2018, Michel et al. 2018), so it doubles as a positive control. Everything below generalizes directly to a continuous split like "low ATP1B1 expression" — I note the one branch point where the method differs.

## 1. Pin the dataset before you touch it

Reproducibility failures in DepMap analyses almost always come from silently re-downloading "latest." Fix this first:

- Download a **named release**, e.g. `DepMap Public 24Q4`, from the DepMap portal (figshare-backed, has a DOI per release, e.g. `10.25452/figshare.plus.xxxxxxxx`).
- Record: release name, download date, DOI, and `sha256sum` of every file you use (`CRISPRGeneEffect.csv`, `OmicsExpressionProteinCodingGenesTPMLogp1.csv`, `OmicsSomaticMutations.csv`, `OmicsCNGene.csv`, `Model.csv`, `CRISPRInferredCommonEssentials.csv` or `AchillesCommonEssentialControls.csv`).
- Write these into a `MANIFEST.txt` or `provenance.json` committed alongside your analysis code — not just in a notebook comment.
- Pin your package versions (`pandas`, `scipy`, `statsmodels`) in a lockfile, since e.g. `scipy`'s Mann-Whitney tie-handling has changed across versions.

```python
provenance = {
    "depmap_release": "24Q4",
    "download_date": "2026-07-30",
    "files": {
        "CRISPRGeneEffect.csv": "sha256:...",
        "OmicsCNGene.csv": "sha256:...",
        "Model.csv": "sha256:...",
    },
}
```

## 2. Define the context group precisely

For a fusion: DepMap's mutation calls table generally does **not** reliably capture gene fusions — you need a fusion-calling source (e.g. curated from CCLE/Sanger fusion pipelines, or literature-annotated cell line lists, e.g. Aska, SYO-1, HS-SY-II, Yamato-SS for SS18::SSX). Build an explicit include list and justify each entry with its source, not a string-match on `Model.csv` lineage names (lineage ≠ molecular subtype).

For the alternative (low ATP1B1 expression), this becomes a **continuous** covariate rather than a binary group — don't force it into two bins unless you have a principled cutoff (e.g. bottom vs top tertile with a gap, or bimodality check via a Gaussian-mixture/dip test). Binning loses power and invites cutoff-shopping.

```python
fusion_positive = ["ACH-000940", "ACH-000864", ...]  # curated SS18::SSX+ DepMap IDs
group = crispr_effect.index.isin(fusion_positive)
```

Exclude cell lines with ambiguous or unknown status rather than defaulting them to the "negative" bucket.

## 3. Selective-dependency statistic

Per gene, compare Chronos scores between context (n typically small, 4–10 lines for a rare fusion) vs. all other profiled lines:

- **Binary group** (fusion): Mann-Whitney U test (robust to Chronos score non-normality and small/unequal n) plus a parametric Welch's t-test as a sanity cross-check — flag genes where the two disagree in sign.
- **Continuous covariate** (ATP1B1 expression): Spearman correlation between expression and gene effect across all lines, not a two-group test — preserves power and avoids arbitrary thresholding.
- **Effect size**, not just p-value: mean-difference in Chronos score (Δ), or a standardized version like Cohen's d/rank-biserial correlation. p-values alone will be dominated by variance artifacts in this small-n regime; effect size ranks true magnitude of selective killing.

```python
from scipy import stats
import numpy as np

results = []
for gene in crispr_effect.columns:
    x = crispr_effect.loc[group, gene].dropna()
    y = crispr_effect.loc[~group, gene].dropna()
    if len(x) < 3 or len(y) < 10:
        continue
    u, p = stats.mannwhitneyu(x, y, alternative="less")  # one-sided: more negative in group
    delta = x.mean() - y.mean()
    results.append((gene, delta, p, len(x), len(y)))

res = pd.DataFrame(results, columns=["gene", "delta", "p", "n_group", "n_other"])
```

## 4. Multiple-testing correction

~18,000 genes tested → control FDR with Benjamini-Hochberg (`statsmodels.stats.multitest.multipletests(method="fdr_bh")`). Report q-values, not raw p, and set your threshold (e.g. q < 0.1, given small-n underpowered tests) before looking at results, not after.

```python
from statsmodels.stats.multitest import multipletests
res["q"] = multipletests(res["p"], method="fdr_bh")[1]
```

## 5. Remove pan-essential genes

A gene selectively "dependent" only because it's essential everywhere and the comparison group happened to have slightly more negative scores is not selective. Cross off DepMap's own **common essential** list (`AchillesCommonEssentialControls.csv` / `CRISPRInferredCommonEssentials.csv` — genes with consistently strongly negative Chronos scores across the full cell line panel by construction). Also apply an absolute-floor filter: require the *non-context* group's median Chronos score to be near-zero (e.g. > −0.3), confirming the gene is genuinely dispensable outside the context, not just "very essential everywhere with slightly more essential in context."

```python
common_essential = set(pd.read_csv("AchillesCommonEssentialControls.csv")["Gene"])
res = res[~res["gene"].isin(common_essential)]
res = res[crispr_effect.loc[~group, res["gene"]].median() > -0.3]
```

## 6. Screen out copy-number/cutting-toxicity artifacts

Chronos already models copy-number-driven cutting toxicity internally (that's much of why Broad moved off CERES), so this is far less severe than in raw log-fold-change data — but residual artifacts survive, especially in highly amplified regions found disproportionately in one lineage. Two concrete checks:

1. **Within-context CN correlation**: for each surviving candidate, correlate Chronos score against gene-level copy number (`OmicsCNGene.csv`) *within the context group specifically*. If a gene sits in a recurrently amplified locus in your fusion-positive lines and dependency tracks copy number rather than fusion status, drop it (or flag it for manual review — sometimes the amplification is itself fusion-driven biology, so don't discard blindly, but do label it).
2. **Cross-dataset replication**: check the same gene's selectivity against the independent **Sanger/Project Score** CRISPR dataset (also on DepMap portal, different guide library/cutting bias). A true fusion-selective dependency should replicate; a locus-cutting artifact usually won't, because the amplicon and guide efficiency differ between libraries.

```python
cn = pd.read_csv("OmicsCNGene.csv", index_col=0)
for gene in candidates:
    cn_corr, cn_p = stats.spearmanr(
        crispr_effect.loc[group, gene], cn.loc[group, gene]
    )
    flag_cn_artifact = abs(cn_corr) > 0.5 and cn_p < 0.05
```

## 7. Final ranking

Rank surviving candidates by a combined selectivity score rather than p-value alone, since with n≈6 vs n≈1000 the test is underpowered and effect size is more decision-relevant:

```
score = -log10(q) * sign(delta) * abs(delta)   # weight significance by magnitude
```

or simpler: sort by `delta` ascending among genes with `q < threshold`, and report both columns so a reader can judge magnitude vs. confidence independently. Cross-reference top hits against expression (is the gene expressed in the context lines at all — a dependency on an unexpressed gene is almost always noise) and against paralog/synthetic-lethal databases for biological plausibility.

## 8. Package it for reproducibility

- One script, one environment lockfile, one `provenance.json` recording the exact release/DOI/checksums from step 1.
- Save the intermediate `res` table (all genes, pre-filter) alongside the final filtered/ranked table, so filtering decisions are auditable rather than baked silently into the final list.
- If you rerun this in 6 months against 25Qx, diff the ranked list against this run explicitly rather than assuming stability — Chronos re-fits per release and scores shift.

If you actually have the DepMap CSVs on disk and want this turned into a runnable script against your files, say so and I'll write it end-to-end rather than in fragments.