## Assumptions I'm making (state these because they drive every downstream choice)

- **Data source**: DepMap Public release (I'll assume **24Q4/25Q2-era Chronos scores** — pin whatever is actually latest when you run this; see reproducibility section). Files: `CRISPRGeneEffect.csv` (Chronos gene effect scores — this is the corrected successor to CERES and already partially handles copy-number cutting bias), `Model.csv` (lineage/subtype/annotations), `OmicsCNGene.csv` (log2 relative copy number), `OmicsExpressionProteinCodingGenesTPMLogp1.csv`, and `OmicsFusionFiltered.csv` (STAR-Fusion calls) for the fusion case.
- **Worked example**: SS18::SSX-positive synovial sarcoma as the categorical context (concrete, well-studied, and has a known positive control — BRD9 — so you can sanity-check your pipeline before trusting novel hits). I'll note where the ATP1B1-low continuous-expression case diverges.
- **Cohort size**: synovial sarcoma is rare in DepMap (~8-12 lines), so I'm designing for a small-n context group, which matters for the statistics below.

## 1. Define the context group precisely

Don't rely on a single field. `Model.csv`'s `OncotreeSubtype == "Synovial Sarcoma"` is a reasonable first pass since SS18::SSX is pathognomonic in ~95%+ of cases, but cross-check against `OmicsFusionFiltered.csv` for actual `SS18--SSX1/2/4` calls, since fusion callers can miss calls or a line can be mis-annotated. Build your "in-group" as the intersection/union of curated-literature line IDs and the fusion-call file, and record which criterion classified each line.

For the continuous case (ATP1B1 expression), don't force a binary split unless you need one for group-based statistics — run it two ways: (a) genome-wide correlation of Chronos score vs. continuous log2(TPM+1), and (b) a bottom-quartile-vs-rest comparison as a robustness check. Watch for confounding by lineage: if ATP1B1 expression tracks tissue of origin, a "low-ATP1B1-selective" gene may really be a lineage-selective gene. Check this by including lineage as a covariate or by re-running within the top 2-3 lineages that contribute most low-expressors.

## 2. Statistical test and ranking

With a small in-group (n~10) and ~18,000 genes tested, a plain per-gene Welch's t-test or Mann-Whitney will have unstable variance estimates. Use a **moderated t-test with empirical Bayes variance shrinkage** (limma's `lmFit`/`eBayes`, or the Python equivalent) — this is what DepMap's own "Custom Analysis" tool uses for exactly this comparison, since it borrows variance information across genes and behaves much better than an unmoderated test at low n.

- Fit: `ChronosScore ~ in_group` for every gene (add lineage as a covariate for the continuous-expression case if needed).
- Get a **t-statistic, effect size (mean difference), and p-value** per gene.
- Correct with **Benjamini-Hochberg FDR** across the full gene set tested (not just "interesting" ones) — report q-values, not just p-values.
- **Rank by effect size, gated by significance**, not by significance alone: with small n, tiny near-zero effects can hit FDR<0.05 by chance of low variance. Require both `q < 0.1` (or 0.05) **and** a minimum effect size (e.g., in-group mean − out-group mean ≤ −0.25 Chronos units) before ranking.

## 3. Remove genes that are essential everywhere

Use DepMap's own "common essential" classification (derived from the distribution of Chronos scores across all screened lines — published as `AchillesCommonEssentialControls.csv` / the common-essential tag on the portal) and drop those genes outright. Then add an explicit numeric gate on top of the label, since the label can lag: require **out-group mean Chronos score > −0.15** (near zero — truly non-essential elsewhere) **and in-group mean < −0.5** (strongly depleted in your context). A gene that's mildly essential everywhere and slightly more essential in your context is a much weaker, less selective, and less druggable hit than one that's neutral everywhere else.

## 4. Filter out copy-number/cutting-toxicity artifacts

This is the classic CRISPR screen confound (Aguirre et al. 2016, Meyers et al. 2017): Cas9 cutting in highly amplified DNA causes a DNA-damage-driven fitness defect that looks like a real dependency but is really an artifact of copy number, not gene function. Chronos already models a per-line, per-locus copy-number correction internally, which reduces but does not eliminate this, especially in high-level focal amplicons.

For each candidate gene surviving steps 2-3:
1. Pull `OmicsCNGene.csv` copy number across all lines for that gene.
2. Fit `ChronosScore ~ CopyNumber` across all lines (or within the in-group) and check whether copy number alone explains a large fraction of the apparent dependency.
3. Re-run your context comparison **with copy number as a covariate**: `ChronosScore ~ in_group + CopyNumber`. If the `in_group` effect size shrinks substantially (say >50%) or loses significance once copy number is controlled for, treat the hit as CN-artifactual and drop or flag it — especially suspicious if your context-group cell lines happen to carry a coincidental focal amplification at that locus unrelated to the biology you care about.

## 5. Check for lineage confounding

Since fusion status and lineage are often perfectly collinear (all SS18::SSX lines are synovial sarcomas), a hit could be "sarcoma-selective" rather than "fusion-selective." Where possible, compare against a broader sarcoma out-group specifically (not just "everything else") as a secondary contrast, and report which top hits remain selective specifically vs. other sarcomas without the fusion. For the continuous-expression case, do the analogous check by adjusting for or stratifying on lineage.

## 6. Sanity check

Before trusting novel hits, confirm your pipeline recovers **BRD9** as top-ranked for the SS18::SSX comparison (its selective essentiality via the ncBAF complex in synovial sarcoma is well established in the literature). If BRD9 doesn't come out near the top, something in group definition, essentiality filtering, or CN correction is likely off.

## 7. Reproducibility

- Record the **exact DepMap release string** (e.g., "DepMap Public 24Q4") and download date; compute and store **sha256 checksums** of every CSV you pull.
- Pin package versions (pandas/scipy/statsmodels or R/limma+Bioconductor version) in a lockfile.
- Script the entire pipeline end-to-end (no manual portal point-and-click) so a rerun on the same release is byte-identical; commit the script alongside the output ranking table.
- Name output files with the release baked in, e.g. `selective_dependency_SS18SSX_DepMap24Q4_20260730.csv`, and cite the release's Figshare DOI in your methods/metadata.

## Minimal implementation sketch (Python)

```python
import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

DEPMAP_RELEASE = "24Q4"  # record + checksum the source files

effect = pd.read_csv("CRISPRGeneEffect.csv", index_col=0)      # lines x genes, Chronos
model = pd.read_csv("Model.csv", index_col="ModelID")
cn = pd.read_csv("OmicsCNGene.csv", index_col=0)
common_ess = set(pd.read_csv("AchillesCommonEssentialControls.csv")["Gene"])

in_group = model[model.OncotreeSubtype == "Synovial Sarcoma"].index
in_group = [l for l in in_group if l in effect.index]
out_group = [l for l in effect.index if l not in in_group]

results = []
for gene in effect.columns:
    if gene.split(" ")[0] in common_ess:
        continue
    a, b = effect.loc[in_group, gene].dropna(), effect.loc[out_group, gene].dropna()
    if len(a) < 4:
        continue
    t, p = stats.ttest_ind(a, b, equal_var=False)  # replace with limma-style moderated t in practice
    eff = a.mean() - b.mean()
    if b.mean() < -0.15 or a.mean() > -0.5:
        continue  # not "neutral elsewhere, strong in-context" pattern
    # copy-number check
    cn_gene = cn[gene] if gene in cn.columns else None
    cn_r = np.nan
    if cn_gene is not None:
        common = effect.index.intersection(cn_gene.dropna().index)
        cn_r, _ = stats.spearmanr(effect.loc[common, gene], cn_gene.loc[common])
    results.append((gene, eff, p, cn_r))

df = pd.DataFrame(results, columns=["gene", "effect_size", "pval", "cn_corr"])
df["qval"] = multipletests(df.pval, method="fdr_bh")[1]
ranked = df[(df.qval < 0.1) & (df.cn_corr.abs() < 0.3)].sort_values("effect_size")
ranked.to_csv(f"selective_dependency_SS18SSX_DepMap{DEPMAP_RELEASE}.csv", index=False)
```

Swap the t-test for limma's `eBayes` (via `rpy2` or R directly) for better small-n behavior, and add the CN-covariate regression from step 4 for genes that pass the initial filter.