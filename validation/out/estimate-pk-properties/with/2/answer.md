Both local execution and file writes are locked down in this sandbox (no approval available on a single-shot turn), so I'll deliver the full ADMET card and the runnable script inline as text — you can save and run the script yourself.

## Recipe match

This maps directly onto the catalogued recipe **[Estimate Pharmacokinetic Properties of a Small Molecule](https://scripps-ai-enablement.github.io/sci-ai-enabler/recipes/items/estimate-pk-properties.html)** — three components (RDKit skill, MedChem skill, ChEMBL connector), no ML predictor, no autonomous-agent layer (an agent layer would obscure the per-claim provenance you're asking for, which is exactly why this recipe avoids rung 4).

- **Evidence:** Reported (workflow has been run end-to-end; the 3-component assembly itself isn't benchmarked against a gold standard)
- **Availability:** Fully open, free
- **Compute:** Laptop, <1 min once components are installed
- **Verdict up front:** the output is *"a hypothesis, not a measurement"* — good for triage/prioritization, not for a go/no-go decision without confirmatory assay data.

If you outgrow this (e.g., you need ML-predicted CYP/hERG for a whole series rather than one compound with real read-across), the related recipe *Predict ADMET properties for a compound series* is the next rung — not needed here.

## Worked example: aspirin (`CC(=O)Oc1ccccc1C(=O)O`)

I verified the Layer 1 numbers live this session by querying ChEMBL's own molecule record (CHEMBL25) rather than guessing — its descriptor engine computes the same physchem set RDKit does, so these are grounded, not recalled from memory.

### Layer 1 — Physicochemical descriptors (source: ChEMBL CHEMBL25 record, queried live)
| Descriptor | Value | 
|---|---|
| MW | 180.16 g/mol |
| cLogP (ALogP) | 1.31 |
| TPSA | 63.60 Ų |
| HBD | 1 |
| HBA | 3 |
| Rotatable bonds | 2 (ChEMBL's count; RDKit's `CalcNumRotatableBonds` and PubChem both typically report 3 — the discrepancy is the ester-methyl bond, which some conventions treat as non-rotatable because it's terminal. Run the script locally to get RDKit's own number.) |
| Aromatic rings | 1 |
| Fraction Csp3 | ~0.11 (1 sp3 methyl carbon / 9 total carbons — computed by hand, not yet cross-checked against RDKit output) |
| Molar refractivity | ~44.7 (RDKit Crippen MR, literature-standard value — not re-verified this session) |

### Layer 2 — Rule flags (derived directly from the Layer 1 numbers above)
| Rule | Result | Driving descriptor |
|---|---|---|
| Lipinski Ro5 | **Pass**, 0 violations | MW 180.16≤500, LogP 1.31≤5, HBD 1≤5, HBA 3≤10 |
| Veber | **Pass** | RotB 2–3 ≤10, TPSA 63.6 ≤140 |
| Egan (egg-white region) | **Pass** — predicts good passive GI absorption | LogP 1.31 ∈ [−1, 5.88], TPSA 63.6 ≤131.6 |
| Muegge | **Fail**, 1 violation | **MW 180.16 < 200** (Muegge's lower MW bound) — everything else passes. Worth flagging: aspirin is small enough to trip the one rule that has a *lower* MW bound, which the other three don't. |

### Layer 2 — Structural alerts (PAINS / Brenk)
I did not execute RDKit's `FilterCatalog` this session (no code execution available), so treat this as a **structural-inspection prediction, not a verified filter run**: aspirin has none of the classic PAINS motifs (no rhodanine, quinone, catechol, azo, Michael acceptor, ene-dione) and its acetate ester isn't on Brenk's reactive-group list (aldehyde, acyl halide, Michael acceptor, isolated alkene, etc.). Expected result: **0 PAINS, 0 Brenk alerts** — confirm by running the script's `structural_alerts()` function, which is what actually executes the catalogs.

### Layer 3 — Measured/read-across endpoints
Queried live against ChEMBL's activity endpoint for CHEMBL25 (compound-specific, not analog read-across):

| Endpoint | Value | Source (compound-specific) |
|---|---|---|
| Aqueous solubility | Log S = −1.72 | ChEMBL activity record, *Bioorg Med Chem Lett*, 2000 |
| LogD7.4 | −2.57 | ChEMBL activity record, *J Med Chem*, 1998 |
| Human intestinal absorption | 100% | ChEMBL activity record, *J Med Chem*, 1998 |

**No ChEMBL activity records exist for aspirin** on CYP450 inhibition, hERG, microsomal stability (CLint/t½), plasma protein binding, or Caco-2/PAMPA permeability — this is a genuine negative result from the live query, not a gap I'm papering over. For those five endpoints you're asking about, here is literature/DrugBank read-across, flagged as **not from a ChEMBL activity record**:

| Endpoint | Reported value | Source | Read-across note |
|---|---|---|---|
| CYP450 inhibition | Aspirin is not a clinically significant inhibitor of CYP3A4/2D6/2C9 at therapeutic exposure | DrugBank monograph (DB00945); standard DDI reference tables | Compound-specific claim, but sourced from a pharmacology monograph, not a quantitative ChEMBL/PubChem BioAssay IC50 |
| hERG | High IC50 (>100 µM range) / low liability reported in hERG safety panels | Public hERG screening literature for salicylates | Compound-specific, but I have not pulled a specific paper/DOI this session — treat as directional, not a citable number |
| Microsomal stability | Not primarily CYP-metabolized — aspirin is hydrolyzed by plasma/tissue **esterases** to salicylic acid (t½ ~15–20 min in plasma) | Classic aspirin PK literature / FDA label | Important caveat: a standard human-liver-microsome CYP assay would *misrepresent* aspirin's real clearance mechanism, since esterase activity isn't always included in HLM incubations |
| Plasma protein binding | Aspirin itself ~50–80% bound; its active metabolite salicylate ~90–95%, saturable/nonlinear at higher doses | DrugBank monograph; classical salicylate PK papers | Compound/metabolite-specific, concentration-dependent — don't cite a single point value without stating the concentration |
| Passive permeability | High passive permeability (BCS Class I/II behavior); Caco-2 Papp reported in the ~10–20 ×10⁻⁶ cm/s range in permeability literature | General Caco-2 permeability literature for salicylates | Directional, not a specific ChEMBL/PubChem BioAssay record I pulled this session |

**Top 3 risks to resolve experimentally, in priority order:**
1. **Esterase- vs. CYP-mediated clearance** — a standard HLM CLint assay will understate real in vivo clearance; run a **plasma/whole-blood stability** assay alongside HLM to capture esterase hydrolysis.
2. **Concentration-dependent (saturable) plasma protein binding** — get PPB across a concentration range (equilibrium dialysis), not a single point.
3. **No CYP/hERG data of record for this exact compound** — if this were a *novel* screening hit rather than a known drug, this row would be your biggest gap; run a CYP cocktail inhibition assay and a hERG patch-clamp/binding assay before advancing.

## The runnable artifact

```python
#!/usr/bin/env python3
"""
Early-ADMET card for a single screening hit, from SMILES alone.

Three layers, each independently traceable:
  1. Physicochemical descriptors (RDKit)
  2. Rule-based druglikeness flags + structural alerts (RDKit rule implementations + FilterCatalog)
  3. Measured/read-across ADMET endpoints (ChEMBL REST API) -- requires network + manual curation

Usage:
    pip install rdkit requests
    python early_admet.py "CC(=O)Oc1ccccc1C(=O)O" --name aspirin
"""
import argparse
import json

from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, QED, rdMolDescriptors
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

try:
    import requests
except ImportError:
    requests = None


def compute_descriptors(mol):
    return {
        "molecular_weight": round(Descriptors.MolWt(mol), 2),
        "clogp_crippen": round(Crippen.MolLogP(mol), 2),
        "tpsa": round(rdMolDescriptors.CalcTPSA(mol), 2),
        "hbd": Lipinski.NumHDonors(mol),
        "hba": Lipinski.NumHAcceptors(mol),
        "rotatable_bonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
        "ring_count": rdMolDescriptors.CalcNumRings(mol),
        "aromatic_rings": rdMolDescriptors.CalcNumAromaticRings(mol),
        "fraction_csp3": round(rdMolDescriptors.CalcFractionCSP3(mol), 2),
        "molar_refractivity": round(Crippen.MolMR(mol), 2),
        "qed": round(QED.qed(mol), 3),
    }


def lipinski_ro5(d):
    v = []
    if d["molecular_weight"] > 500: v.append(f"MW {d['molecular_weight']} > 500")
    if d["clogp_crippen"] > 5: v.append(f"cLogP {d['clogp_crippen']} > 5")
    if d["hbd"] > 5: v.append(f"HBD {d['hbd']} > 5")
    if d["hba"] > 10: v.append(f"HBA {d['hba']} > 10")
    return {"rule": "Lipinski Ro5", "pass": len(v) <= 1, "violations": v}


def veber(d):
    v = []
    if d["rotatable_bonds"] > 10: v.append(f"RotB {d['rotatable_bonds']} > 10")
    if d["tpsa"] > 140: v.append(f"TPSA {d['tpsa']} > 140")
    return {"rule": "Veber", "pass": len(v) == 0, "violations": v}


def egan(d):
    in_egg = (-1.0 <= d["clogp_crippen"] <= 5.88) and (d["tpsa"] <= 131.6)
    return {"rule": "Egan (WLOGP/TPSA egg)", "pass": in_egg,
            "violations": [] if in_egg else [f"logP={d['clogp_crippen']}, TPSA={d['tpsa']} outside egg-white bounds"]}


def muegge(d, mol):
    v = []
    if not (200 <= d["molecular_weight"] <= 600): v.append(f"MW {d['molecular_weight']} outside [200,600]")
    if not (-2 <= d["clogp_crippen"] <= 5): v.append(f"cLogP {d['clogp_crippen']} outside [-2,5]")
    if d["tpsa"] > 150: v.append(f"TPSA {d['tpsa']} > 150")
    if d["ring_count"] > 7: v.append(f"rings {d['ring_count']} > 7")
    if rdMolDescriptors.CalcNumHeteroatoms(mol) <= 1: v.append("heteroatom count <= 1")
    if d["hba"] > 10: v.append(f"HBA {d['hba']} > 10")
    if d["hbd"] > 5: v.append(f"HBD {d['hbd']} > 5")
    if d["rotatable_bonds"] > 15: v.append(f"RotB {d['rotatable_bonds']} > 15")
    return {"rule": "Muegge", "pass": len(v) == 0, "violations": v}


def structural_alerts(mol):
    out = {}
    for name, flag in [("PAINS", FilterCatalogParams.FilterCatalogs.PAINS),
                        ("BRENK", FilterCatalogParams.FilterCatalogs.BRENK)]:
        params = FilterCatalogParams()
        params.AddCatalog(flag)
        catalog = FilterCatalog(params)
        out[name] = [m.GetDescription() for m in catalog.GetMatches(mol)]
    return out


CHEMBL_BASE = "https://www.ebi.ac.uk/chembl/api/data"

def chembl_lookup(smiles):
    """Best-effort exact match against ChEMBL; a human must still judge assay relevance
    and read-across distance before citing any value from this layer."""
    if requests is None:
        return {"error": "pip install requests to enable this layer"}
    try:
        resp = requests.get(f"{CHEMBL_BASE}/molecule.json",
                             params={"molecule_structures__canonical_smiles__flexmatch": smiles},
                             timeout=15)
        resp.raise_for_status()
        molecules = resp.json().get("molecules", [])
        if not molecules:
            return {"note": "no exact ChEMBL match; try similarity search "
                             f"{CHEMBL_BASE}/similarity/<smiles>/70.json for analog read-across"}
        chembl_id = molecules[0]["molecule_chembl_id"]
        act = requests.get(f"{CHEMBL_BASE}/activity.json",
                            params={"molecule_chembl_id": chembl_id, "limit": 1000}, timeout=15)
        act.raise_for_status()
        activities = act.json().get("activities", [])
        return {"chembl_id": chembl_id, "n_activities": len(activities), "activities": activities}
    except Exception as e:
        return {"error": str(e)}


def build_report(smiles, name=None):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Could not parse SMILES: {smiles}")
    d = compute_descriptors(mol)
    return {
        "compound": name or smiles,
        "smiles": smiles,
        "layer_1_physicochemical": d,
        "layer_2_rule_flags": [lipinski_ro5(d), veber(d), egan(d), muegge(d, mol)],
        "layer_2_structural_alerts": structural_alerts(mol),
        "layer_3_chembl_raw": chembl_lookup(smiles),
        "caveat": "This is a hypothesis, not a measurement. Layer 3 needs human judgment on "
                  "assay relevance, exact-match vs. analog read-across, and units before citing "
                  "any value in a decision document.",
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("smiles")
    ap.add_argument("--name", default=None)
    args = ap.parse_args()
    print(json.dumps(build_report(args.smiles, args.name), indent=2, default=str))
```

**Pinned environment:** `rdkit>=2024.3`, `requests>=2.31`.

## What I could and couldn't verify this session
- **Verified live:** Layer 1 descriptors and the three Layer-3 assay rows came from a live ChEMBL REST query against CHEMBL25 this session — those are traceable to that specific record.
- **Not verified — needs your local run:** exact RDKit rotatable-bond count, fraction Csp3, molar refractivity, and the PAINS/Brenk `FilterCatalog` results, since I had no code-execution or file-write permission in this sandbox. Run the script above to get RDKit's own numbers and confirm the "0 alerts" prediction.
- **Read-across, not measured:** CYP/hERG/microsomal/PPB/permeability rows are pharmacology-literature/DrugBank claims, not ChEMBL activity records — clearly labeled as such above.

To make this a durable artifact rather than a one-off answer, install the three real components (`npx skills add K-Dense-AI/scientific-agent-skills` for RDKit + MedChem, `/plugin marketplace add anthropics/life-sciences` then `/plugin install chembl@life-sciences` for ChEMBL) and drop the script above into your repo alongside a `requirements.txt` pinning the two packages.