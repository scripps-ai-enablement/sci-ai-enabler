## Recipe match: `benchmark-admet-property-with-pytdc`

Exact hit in the composer index (`generated: 2026-07-06`, so it's 24 days old — worth a `/plugin marketplace update sci-ai-enabler` at some point, but the recipe content is stable and I re-verified the leaderboard details live).

- **Evidence:** Reported
- **Availability:** Fully open (MIT-licensed)
- **Compute:** Laptop (few minutes)
- **Why not a lower rung:** this needs the exact TDC frozen split + official eval code (`ADMET_Group.evaluate_many`) so the number is leaderboard-comparable — a plain prompt or hand-rolled split would silently break comparability, which is the whole point of the request.

**Leaderboard ground truth (fetched live from tdcommons.ai, not from memory):** metric is **MAE, lower is better**, rows are reported as `mean ± std` over the 5 official seeds, format `0.xxx ± 0.0yy`. Current top of the Caco2_Wang board: CaliciBoost 0.256±0.006, XGBoost 0.274±0.004, MapLight 0.276±0.005.

### Important honesty caveat — I could not execute this

I tried to actually run the pipeline in this session (per your "all in one go" instruction) and hit a hard wall: every write/exec action here (`Write`, `Bash` with redirects or `python -c`) came back `requires approval` / `not granted`, with no human available to approve it in this single-shot run. I'm not going to invent a benchmark number to fill that gap — that would violate the whole point of a leaderboard-comparable result. Below is the complete, runnable artifact; the score has to come from actually executing it in an environment that allows package installs and file writes.

### Setup

```bash
pip install PyTDC rdkit scikit-learn numpy
```

### `benchmark_caco2.py`

```python
"""
Morgan-fingerprint + Random Forest baseline on TDC's Caco2_Wang permeability dataset,
using the official frozen scaffold split and official leaderboard metric (MAE).

Recipe: benchmark-admet-property-with-pytdc (sci-ai-enabler composer index, evidence=Reported)
Reference: Huang et al., NeurIPS 2021 Datasets & Benchmarks (arXiv:2102.09548)
Leaderboard: https://tdcommons.ai/benchmark/admet_group/01caco2/
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
from sklearn.ensemble import RandomForestRegressor
from tdc.benchmark_group import admet_group

FP_RADIUS = 2      # ECFP4
FP_NBITS = 2048
SEEDS = [1, 2, 3, 4, 5]   # official TDC benchmark seeds


def smiles_to_ecfp4(smiles_list):
    fps = np.zeros((len(smiles_list), FP_NBITS), dtype=np.uint8)
    for i, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
        bv = AllChem.GetMorganFingerprintAsBitVect(mol, FP_RADIUS, nBits=FP_NBITS)
        arr = np.zeros((FP_NBITS,), dtype=np.uint8)
        DataStructs.ConvertToNumpyArray(bv, arr)
        fps[i] = arr
    return fps


def main():
    group = admet_group(path="./tdc_data")   # downloads + caches the frozen split
    predictions_list = {}

    for seed in SEEDS:
        benchmark = group.get("Caco2_Wang")
        name, test = benchmark["name"], benchmark["test"]
        train, valid = group.get_train_valid_split(benchmark=name, split_type="scaffold", seed=seed)

        X_train = smiles_to_ecfp4(train["Drug"].tolist())
        y_train = train["Y"].values
        X_test = smiles_to_ecfp4(test["Drug"].tolist())

        model = RandomForestRegressor(n_estimators=500, max_features="sqrt", n_jobs=-1, random_state=seed)
        model.fit(X_train, y_train)

        predictions_list[seed] = {name: model.predict(X_test)}

    results = group.evaluate_many(predictions_list)   # official MAE, mean ± std, leaderboard-format
    print(results)


if __name__ == "__main__":
    main()
```

### `requirements.txt` (pinned environment — check exact versions after your first install)

```
PyTDC
rdkit
scikit-learn
numpy
```

### Assumptions I made (per your instruction, single-shot, no follow-up)

- Endpoint = `Caco2_Wang` (the standard Caco-2 regression dataset in TDC ADMET, MDCK/Caco-2 apparent permeability, n=906) — this is the one on the public leaderboard.
- Morgan fingerprint = ECFP4, radius=2, nBits=2048 (recipe's stated default; also TDC's own baseline convention).
- RandomForestRegressor(n_estimators=500, max_features='sqrt'), all other params sklearn defaults, `random_state=seed` for reproducibility, one model per seed (not one model evaluated 5×) — this matches how TDC intends the 5-seed variance to be measured (variance from the scaffold split's stochasticity + model init, not just re-scoring).
- Split: official `scaffold` split via `group.get_train_valid_split(..., split_type="scaffold", seed=seed)`, which is the TDC-frozen, leaderboard-canonical split — not a custom split.

### What to do with this

1. Run `pip install -r requirements.txt`
2. Run `python benchmark_caco2.py` — first run downloads and caches the frozen TDC split to `./tdc_data`
3. `group.evaluate_many(...)` prints `{'caco2_wang': [mean, std]}` in the exact `mean ± std` convention used on the public board — drop that row straight into your comparison table against CaliciBoost/XGBoost/MapLight above.

For provenance, record alongside the printed result: PyTDC/RDKit/scikit-learn versions (`pip freeze`), the TDC dataset release date embedded in `./tdc_data`, and the script above (hash it) — that's what makes the number re-auditable later, per the recipe's reproducibility guidance.

If you want, I can also draft the "success"/"gap" capture report for the sci-ai-enabler knowledge base (noting that the recipe matched but this sandbox couldn't execute it) — say the word and I'll show you the exact text before filing anything.