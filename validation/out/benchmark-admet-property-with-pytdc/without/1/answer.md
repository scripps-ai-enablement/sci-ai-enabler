I hit a hard wall: this sandbox's permission gate blocks package installation (`pip install`) and arbitrary code execution (`python -c`), and no interactive approval is coming through (consistent with this being single-shot). I can't fabricate a result, so here's the complete, correct, ready-to-run pipeline plus the leaderboard context — run it in any environment with normal pip/network access and you'll get a directly comparable number in under a minute.

**Assumptions made (stated per your instructions, since you can't clarify):**
- "Standard scaffold split" = TDC's frozen `admet_group` default split (`split_type='default'`), not a custom scaffold split — this is what the leaderboard itself uses.
- "Official evaluation metric" = **MAE**, confirmed via TDC's Caco2_Wang leaderboard page.
- Protocol = TDC's required 5-seed run (`seed in [1,2,3,4,5]`), reporting **mean ± std**, per TDC's submission rules.
- Featurization = Morgan fingerprints, radius 2, 2048 bits (RDKit default convention) — reasonable baseline choice not specified by you.
- Model = `RandomForestRegressor(n_estimators=500, random_state=seed)` — untuned baseline, consistent with "baseline" framing.

### Script

```python
# caco2_rf_baseline.py
# pip install PyTDC rdkit scikit-learn pandas numpy
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import RandomForestRegressor
from tdc.benchmark_group import admet_group

def morgan_fp(smiles_list, radius=2, n_bits=2048):
    fps = []
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        fps.append(np.array(fp, dtype=np.int8))
    return np.vstack(fps)

group = admet_group(path='data/')
name = 'Caco2_Wang'
benchmark = group.get(name)
test = benchmark['test']
X_test = morgan_fp(test['Drug'].tolist())

predictions_list = []
for seed in [1, 2, 3, 4, 5]:
    train, valid = group.get_train_valid_split(benchmark=name, split_type='default', seed=seed)
    train_all = train  # RF baseline: train on train split only (valid held out, unused, matching a no-tuning baseline)

    X_train = morgan_fp(train_all['Drug'].tolist())
    y_train = train_all['Y'].values

    model = RandomForestRegressor(n_estimators=500, n_jobs=-1, random_state=seed)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    predictions_list.append({name: y_pred})

results = group.evaluate_many(predictions_list)
print(results)
# -> {'caco2_wang': [mean_mae, std_mae]}
```

Run: `python3 caco2_rf_baseline.py`

### Reporting format (matches the leaderboard exactly)

The leaderboard reports `MAE mean ± std` across the 5 seeds. Take `results['caco2_wang']` and report it as:

```
Caco2_Wang: <mean> ± <std> (MAE, lower is better)
```

### Current leaderboard for comparison (pulled live from tdcommons.ai)

| Rank | Method | MAE |
|---|---|---|
| 1 | CaliciBoost | 0.256 ± 0.006 |
| 2 | XGBoost | 0.274 ± 0.004 |
| 3 | MapLight | 0.276 ± 0.005 |
| 4 | BaseBoosting | 0.285 ± 0.005 |
| 5 | MolMapNet-D | 0.287 ± 0.005 |

A plain Morgan+RF baseline typically lands in the **0.32–0.38 MAE** range on this dataset (based on similar published TDC baselines) — i.e., below the top of the leaderboard but a reasonable sanity-check baseline. Treat that range as a rough expectation, not a substitute for actually running the script above.

Sources: [Caco2_Wang Leaderboard](https://tdcommons.ai/benchmark/admet_group/01caco2/), [ADMET Benchmark Group Overview](https://tdcommons.ai/benchmark/admet_group/overview/), [Leaderboard Guide](https://tdcommons.ai/benchmark/overview/)