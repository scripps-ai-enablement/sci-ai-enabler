I hit a hard limitation I need to flag before anything else: **code execution is being denied in this sandbox** — even `python3 -c "print('hello')"` returns "requires approval" with no user available to approve it (single-shot session, empty working directory, no pre-existing environment). So I cannot actually download the TDC split, fit the model, or produce a real score right now. I won't fabricate a number to fill that gap — instead here's the complete, correct, ready-to-run implementation plus what I can respons­ibly tell you from memory about the comparison point.

**Assumptions made** (since none were given): "Caco-2 permeability" = TDC's `Caco2_Wang` ADME dataset (the standard one on the TDC leaderboard); "standard scaffold split" = TDC's built-in frozen 5-seed benchmark-group split (`split_type='default'`, which *is* scaffold split for this task — no need to re-derive it); "official evaluation metric" = MAE (that's what the Caco2_Wang leaderboard is ranked on); Morgan fingerprint = radius 2, 2048 bits (RDKit default-ish choice used by most TDC baselines); RF = `RandomForestRegressor(n_estimators=500)`.

```python
# pip install PyTDC rdkit-pypi scikit-learn numpy
from tdc.benchmark_group import admet_group
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def featurize(smiles_list, radius=2, n_bits=2048):
    X = np.zeros((len(smiles_list), n_bits), dtype=np.int8)
    for i, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi)
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        DataStructs.ConvertToNumpyArray(fp, X[i])
    return X

group = admet_group(path='data/')   # downloads the frozen, versioned TDC split
benchmark = group.get('Caco2_Wang')
name = benchmark['name']
test = benchmark['test']
X_test = featurize(test['Drug'])

predictions_list = []
for seed in [1, 2, 3, 4, 5]:                       # official 5 seeds required for leaderboard submission
    train, valid = group.get_train_valid_split(benchmark=name, split_type='default', seed=seed)
    X_fit = featurize(list(train['Drug']) + list(valid['Drug']))
    y_fit = np.concatenate([train['Y'].values, valid['Y'].values])

    model = RandomForestRegressor(n_estimators=500, n_jobs=-1, random_state=seed)
    model.fit(X_fit, y_fit)

    predictions_list.append({name: model.predict(X_test)})

results = group.evaluate_many(predictions_list)     # computes MAE mean ± std, TDC's official reducer
print(results)
# -> {'caco2_wang': [mean_mae, std_mae]}
```

Report it in leaderboard format as: `Morgan+RF: <mean_mae> ± <std_mae> (MAE, lower is better)`.

On the comparison point: I recall the public `Caco2_Wang` leaderboard being MAE-ranked with entries roughly in the range of ~0.28–0.40 (e.g., Chemprop and Chemprop-RDKit around the low-0.33s, simple Morgan/RDKit2D + shallow-ML baselines typically clustering ~0.35–0.40+). I'm flagging this as **recalled, not verified right now** — treat it as a rough sanity-check band, not a citation, and confirm exact current standings at TDC's leaderboard page before writing up a comparison, since leaderboards get new submissions over time.

**Bottom line:** the script above is complete and correct for what you asked; I just can't execute it in this session because Python invocation itself is being blocked here. If you run it locally (`pip install PyTDC rdkit-pypi scikit-learn`), it will print the exact mean±std MAE in the leaderboard's own format.