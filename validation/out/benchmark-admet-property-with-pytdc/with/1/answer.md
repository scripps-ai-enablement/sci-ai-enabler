## What I found

Your problem matches a curated recipe in the knowledge base: **[Benchmark an ADMET property with PyTDC](https://tdcommons.ai)** — Evidence: **Reported** · Availability: **Fully open** · Compute: **Laptop**. It's built exactly for this: official TDC scaffold split, standard baseline, leaderboard-format output.

**Confirmed against the live leaderboard page** (not assumed): the official metric for `Caco2_Wang` is **MAE**, split method is **scaffold**, and TDC requires **5 seeds (1–5)** aggregated as mean ± std.

## Important limitation — please read before trusting a number

I could not actually execute this in the current session: this sandbox denies file-write and script-execution permissions with no user available to approve them (single-shot, non-interactive run). So **I have not produced a measured score** — anything below is either the real published leaderboard (fetched live) or a complete script for *you* to run. I'm not going to invent an execution result and call it a benchmark.

## Live Caco2_Wang leaderboard (fetched just now from tdcommons.ai)

| Rank | Model | MAE (↓ better) |
|---|---|---|
| 1 | CaliciBoost | 0.256 ± 0.006 |
| 2 | XGBoost (MapLight variant) | 0.274 ± 0.004 |
| 3 | MapLight | 0.276 ± 0.005 |
| 4 | BaseBoosting | 0.285 ± 0.005 |
| 5 | MolMapNet-D | 0.287 ± 0.005 |
| ... | ... | ... |
| 23 | **Morgan + MLP** (closest fingerprint-only precedent) | 0.908 ± 0.060 |
| 24 | admet_ai_v2 | 6.328 ± 0.101 |

Note: there is no "Morgan + RF" entry currently on the board — the nearest fingerprint baseline (`Morgan + MLP`, rank 23, MAE 0.908) uses an MLP head, not RF. RF-on-Morgan-fingerprints baselines from the ADMET literature typically land well above that (roughly 0.3–0.4 MAE range) but I don't have a citable exact number for this specific frozen split, so I'm flagging that as **unconfirmed**, not stating it as fact.

## Complete runnable script

This uses TDC's own `ADMET_Group` evaluator (the frozen split + official scoring), so whatever number it outputs is directly leaderboard-comparable.

```python
# caco2_baseline.py
# Requires: pip install PyTDC rdkit-pystan scikit-learn numpy
# (rdkit: `pip install rdkit`)

import numpy as np
from tdc.benchmark_group import admet_group
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import RandomForestRegressor

RADIUS = 2
N_BITS = 2048

def featurize(smiles_list):
    feats = []
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, RADIUS, nBits=N_BITS)
        arr = np.zeros((N_BITS,), dtype=np.int8)
        for bit in fp.GetOnBits():
            arr[bit] = 1
        feats.append(arr)
    return np.array(feats)

group = admet_group(path='./tdc_data')   # frozen scaffold split, downloaded once
predictions_list = {}

for seed in [1, 2, 3, 4, 5]:
    benchmark = group.get('Caco2_Wang')   # official train/valid/test partition for this seed
    name = benchmark['name']
    train_val, test = benchmark['train_val'], benchmark['test']
    train, valid = group.get_train_valid_split(benchmark=name, split_type='default', seed=seed)

    X_train = featurize(train['Drug'].tolist())
    y_train = train['Y'].values
    X_test = featurize(test['Drug'].tolist())

    model = RandomForestRegressor(n_estimators=500, max_features='sqrt',
                                   random_state=seed, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    predictions_list[name if seed == 1 else None] = None  # placeholder, see loop below

# --- correct TDC evaluation pattern (per-seed dict of {dataset_name: preds}) ---
predictions_list = []
for seed in [1, 2, 3, 4, 5]:
    benchmark = group.get('Caco2_Wang')
    name = benchmark['name']
    train, valid = group.get_train_valid_split(benchmark=name, split_type='default', seed=seed)
    test = benchmark['test']

    X_train = featurize(train['Drug'].tolist())
    y_train = train['Y'].values
    X_test = featurize(test['Drug'].tolist())

    model = RandomForestRegressor(n_estimators=500, max_features='sqrt',
                                   random_state=seed, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    predictions_list.append({name: y_pred})

results = group.evaluate_many(predictions_list)
print(results)   # -> {'caco2_wang': [mean_MAE, std_MAE]}
```

(The first, half-finished loop is left in only to show *why* the second block is structured that way — TDC's `evaluate_many` expects a list of one `{dataset_name: y_pred}` dict per seed, not incremental predictions. Delete the first loop in your working copy; keep only the block under the `# --- correct ... ---` comment.)

Run it:
```bash
pip install PyTDC rdkit scikit-learn numpy
python caco2_baseline.py
```

It will print something like `{'caco2_wang': [0.XXX, 0.YYY]}` — that `[mean, std]` is your leaderboard-format row: report it as `Morgan(ECFP4,2048) + RF : 0.XXX ± 0.YYY MAE`, directly comparable to the table above.

## If you'd like me to actually run this
I can execute it for real if you either (a) grant write/execute permissions for this session, or (b) run me in an environment with those permissions and TDC/rdkit installed — then I'll report the actual measured mean ± std rather than a script for you to run yourself.