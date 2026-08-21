Write access isn't available in this sandbox, so I'll deliver the full solution inline instead.

## Recommended approach: DepMap skill (Rung 2), not a bespoke pipeline

**Why not rung 1 (prompting Claude Code alone):** this needs real numeric computation over gigabyte-scale DepMap matrices across ~1,000+ cell lines — the kind of thing an LLM will hallucinate or go stale on from training data. It has to actually load and compute over the current release's files. That pushes you to rung 2.

**Matched recipe:** [`find-selective-cancer-dependencies-with-depmap`](https://scripps-ai-enablement.github.io/sci-ai-enabler/recipes/items/find-selective-cancer-dependencies-with-depmap.html) — this is a curated, human-reviewed answer to exactly this problem (it literally cites SS18::SSX and ATP1B1 as worked examples: Iyer et al., *EMBO J.* 2025 found SUMO2 as a selective SS18::SSX-fusion dependency this way).

- **Evidence:** Reported (established practice; cites Behan et al. *Nature* 2019 and Dempster et al. *Nat. Commun.* 2021 for the underlying Chronos/CN-correction methodology, plus recent published hits found this exact way)
- **Availability:** Fully open (DepMap data is public, no API key, permissive license)
- **Compute:** Laptop-sufficient (~200–400 MB cached download, genome-wide contrast runs in under a minute on 8 GB RAM)

**Concrete assumption** (none was given, so I'm fixing one): context = **SS18::SSX fusion-positive synovial sarcoma lines** in the current DepMap release, background = all other screened lines. Swap in low-ATP1B1 or any other biomarker by changing only the grouping step below — everything downstream is identical.

## Install

```bash
npx skills add K-Dense-AI/scientific-agent-skills
# or manually:
git clone https://github.com/K-Dense-AI/scientific-agent-skills
cp -r scientific-agent-skills/skills/depmap ~/.claude/skills/
```

This skill downloads/caches: `CRISPRGeneEffect.csv` (Chronos gene-effect scores), `OmicsCNGene.csv` (copy number), `OmicsExpressionProteinCodingGenesTPMLogp1.csv`, `OmicsSomaticMutationsMatrixDamaging.csv`, and `sample_info.csv`. **Caveat, checked and worth flagging honestly:** the skill's own docs don't specify *which* DepMap release it pulls or the exact CN-correction/multiple-testing algorithm it uses internally — so don't trust it as a black box for the reproducibility requirement you stated. Pin the release and re-derive the stats yourself in a committed script, which is also what the recipe itself recommends as step 3 ("execute a committed analysis script," not just trust the skill's live output).

## Pipeline

1. **Pin the release.** Go to depmap.org/portal/download, note the quarterly label (e.g., `24Q4`), download the five files above for that release specifically, and SHA256-hash each one immediately.
2. **Define groups from data, not memory.** Pull fusion calls (or your mutation/expression threshold) from the omics files for that same pinned release, write the resulting cell-line ID list to a plain text file — that file *is* your audit trail for "why these lines are in the context group." Require ≥10 lines per group or flag the result as underpowered.
3. **Run the contrast:** per gene, context mean − background mean of Chronos scores (more negative = more selectively essential), two-sided Mann-Whitney U test, Benjamini-Hochberg FDR genome-wide (~18,000 tests).
4. **Drop pan-essential genes:** background mean Chronos ≤ −0.5 → essential everywhere → not a selective vulnerability, filter it regardless of p-value.
5. **Flag CN artifacts.** Chronos already partially corrects for copy-number-driven cutting toxicity, but that correction is imperfect at highly amplified focal loci. Add a second, auditable check: (a) is the gene's copy number substantially higher in the context group than background, and (b) across *all* lines, does higher copy number correlate with more-negative dependency independent of the biological grouping? Both true → flag as likely artifact, not true dependency.
6. **Provenance file** alongside the ranked output: release label, file hashes, group definitions, thresholds used, run timestamp, model ID.

## The committed script (`analysis.py`)

```python
"""Rank genes by selective CRISPR dependency in a defined DepMap cancer context.

Usage:
    python analysis.py --release 24Q4 --data-dir ./data \
        --context-file ss18_ssx_lines.txt \
        --output dependencies.csv --provenance-output provenance.json

Expects, under --data-dir (downloaded directly from the DepMap portal for the
pinned --release, not resolved by any wrapper):
    CRISPRGeneEffect.csv   Chronos gene-effect scores, rows=ModelID, cols=genes
    OmicsCNGene.csv        relative copy number per gene per cell line, same shape

--context-file is a plain text file, one ModelID per line: the cell lines carrying
the biomarker (e.g. SS18::SSX-positive lines, or a hand-picked low-ATP1B1-expression
cohort). Derive it from the omics files for the SAME pinned release and keep it as
a versioned input — it is the single most important source of bias in this analysis.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

PAN_ESSENTIAL_THRESHOLD = -0.5   # background-mean Chronos <= this -> essential everywhere, drop
CN_DELTA_THRESHOLD = 1.0         # log2 relative-CN (context - background) that counts as "elevated"
CN_CORR_THRESHOLD = -0.3         # Spearman rho(CN, dependency) across ALL lines that counts as "artifact-like"
MIN_GROUP_SIZE = 10


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_matrices(data_dir: Path):
    effect = pd.read_csv(data_dir / "CRISPRGeneEffect.csv", index_col=0)
    cn = pd.read_csv(data_dir / "OmicsCNGene.csv", index_col=0)
    effect.columns = [c.strip() for c in effect.columns]
    cn.columns = [c.strip() for c in cn.columns]
    return effect, cn


def flag_cn_artifacts(effect, cn, context_ids, background_ids, genes):
    common_genes = set(genes) & set(cn.columns)
    all_ids = [i for i in list(context_ids) + list(background_ids)
               if i in effect.index and i in cn.index]
    ctx_cn_ids = [i for i in context_ids if i in cn.index]
    bg_cn_ids = [i for i in background_ids if i in cn.index]

    rows = []
    for gene in genes:
        if gene not in common_genes:
            rows.append({"gene": gene, "cn_delta": np.nan, "cn_dep_corr": np.nan,
                         "cn_artifact_flag": False})
            continue
        cn_delta = cn.loc[ctx_cn_ids, gene].mean() - cn.loc[bg_cn_ids, gene].mean()
        paired = pd.DataFrame({"cn": cn.loc[all_ids, gene],
                                "dep": effect.loc[all_ids, gene]}).dropna()
        rho = np.nan
        if len(paired) >= 20:
            rho, _ = stats.spearmanr(paired["cn"], paired["dep"])
        artifact = bool((cn_delta >= CN_DELTA_THRESHOLD)
                         and (not np.isnan(rho)) and (rho <= CN_CORR_THRESHOLD))
        rows.append({"gene": gene, "cn_delta": cn_delta, "cn_dep_corr": rho,
                     "cn_artifact_flag": artifact})
    return pd.DataFrame(rows)


def run_contrast(effect, cn, context_ids, background_ids):
    context_ids = [c for c in context_ids if c in effect.index]
    background_ids = [c for c in background_ids if c in effect.index]
    if len(context_ids) < MIN_GROUP_SIZE:
        print(f"WARNING: context group has only {len(context_ids)} lines "
              f"(<{MIN_GROUP_SIZE}); treat results as underpowered.", file=sys.stderr)

    ctx, bg = effect.loc[context_ids], effect.loc[background_ids]
    rows = []
    for gene in effect.columns:
        cv, bv = ctx[gene].dropna(), bg[gene].dropna()
        if len(cv) < 3 or len(bv) < 3:
            continue
        ctx_mean, bg_mean = cv.mean(), bv.mean()
        try:
            _, p = stats.mannwhitneyu(cv, bv, alternative="two-sided")
        except ValueError:
            p = np.nan
        rows.append({"gene": gene, "n_context": len(cv), "n_background": len(bv),
                     "context_mean": ctx_mean, "background_mean": bg_mean,
                     "selective_effect": ctx_mean - bg_mean, "p_value": p})

    res = pd.DataFrame(rows).dropna(subset=["p_value"])
    res["fdr"] = multipletests(res["p_value"], method="fdr_bh")[1]
    res["pan_essential"] = res["background_mean"] <= PAN_ESSENTIAL_THRESHOLD

    cn_flags = flag_cn_artifacts(effect, cn, context_ids, background_ids, res["gene"])
    res = res.merge(cn_flags, on="gene", how="left")
    return res.sort_values("selective_effect")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", required=True, help="DepMap release label, e.g. 24Q4")
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--context-file", required=True)
    ap.add_argument("--output", default="dependencies.csv")
    ap.add_argument("--provenance-output", default="provenance.json")
    args = ap.parse_args()

    effect, cn = load_matrices(args.data_dir)
    context_ids = [l.strip() for l in open(args.context_file) if l.strip()]
    background_ids = [i for i in effect.index if i not in context_ids]

    res = run_contrast(effect, cn, context_ids, background_ids)
    res.to_csv(args.output, index=False)

    hashes = {f: sha256_of(args.data_dir / f)
              for f in ("CRISPRGeneEffect.csv", "OmicsCNGene.csv")
              if (args.data_dir / f).exists()}
    provenance = {
        "depmap_release": args.release,
        "file_sha256": hashes,
        "context_definition_file": str(Path(args.context_file).resolve()),
        "n_context": len(context_ids),
        "n_background": len(background_ids),
        "pan_essential_threshold": PAN_ESSENTIAL_THRESHOLD,
        "cn_delta_threshold": CN_DELTA_THRESHOLD,
        "cn_corr_threshold": CN_CORR_THRESHOLD,
        "min_group_size": MIN_GROUP_SIZE,
        "script": "analysis.py",
    }
    with open(args.provenance_output, "w") as f:
        json.dump(provenance, f, indent=2)
    print(f"Wrote {len(res)} genes to {args.output}; provenance in {args.provenance_output}")


if __name__ == "__main__":
    main()
```

**`requirements.txt`**
```
pandas==2.2.2
numpy==1.26.4
scipy==1.13.1
statsmodels==0.14.2
```

Output columns: `gene, n_context, n_background, context_mean, background_mean, selective_effect, p_value, fdr, pan_essential, cn_delta, cn_dep_corr, cn_artifact_flag`. Your final ranked shortlist is: `pan_essential == False`, `cn_artifact_flag == False`, sorted by `selective_effect` ascending, then by `fdr`.

## Honest gaps you should know about

- `CN_DELTA_THRESHOLD`/`CN_CORR_THRESHOLD` are reasonable defaults I set, not values documented by DepMap or the skill — before trusting a top hit, plot its CN-vs-dependency scatter across all lines and eyeball it; don't rely on the threshold alone.
- The skill's own page doesn't document which release it defaults to or its internal CN-correction algorithm — that's exactly why the script above re-derives everything from files you download and hash yourself, rather than trusting the skill's live query as the reproducibility record.
- I couldn't write files in this sandbox (no filesystem permission), so nothing above has been executed — copy the two files into your own project, install the requirements, download the pinned release's `CRISPRGeneEffect.csv`/`OmicsCNGene.csv`, build your `ss18_ssx_lines.txt` context file from the release's fusion calls, and run it.