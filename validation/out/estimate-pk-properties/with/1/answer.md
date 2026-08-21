# Early-ADMET profile: aspirin (CC(=O)Oc1ccccc1C(=O)O)

**Assembly used:** this maps directly onto an existing catalogued recipe — *"Estimate pharmacokinetic properties of a small molecule"* (evidence: **Reported** · complexity: **multi-tool harness** · availability: **Fully open** · compute: **Laptop**). It combines RDKit-class physicochemical descriptors, rule-based ADMET flags (Lipinski/Veber/Egan/Muegge + PAINS/BRENK), and measured ChEMBL/PubChem endpoints — the exact three layers you asked for.

**One environment caveat up front:** this session's sandbox blocked local Python/RDKit execution (tool-approval never resolved), so descriptors below come from PubChem's and ChEMBL's own computed-properties pipelines (same algorithms RDKit implements) rather than a fresh local RDKit run — I cross-checked the two sources against each other and flag the one place they disagree. A ready-to-run script is at the bottom so you (or I, in an unblocked environment) can regenerate the identical numbers with RDKit directly.

---

## 1. Compound

| Field | Value |
|---|---|
| Input SMILES | `CC(=O)Oc1ccccc1C(=O)O` |
| Canonical SMILES (PubChem/ChEMBL, matches input) | `CC(=O)Oc1ccccc1C(=O)O` |
| InChIKey | `BSYNRYMUTXBXSQ-UHFFFAOYSA-N` |
| Name | Aspirin (acetylsalicylic acid) |
| PubChem CID | 2244 |
| ChEMBL ID | CHEMBL25 |
| Formula | C₉H₈O₄ |

## 2. Physicochemical descriptors

Source: PubChem CID 2244 computed-properties record, cross-checked against ChEMBL CHEMBL25's molecule-properties record.

| Descriptor | Value (PubChem) | Cross-check (ChEMBL) | Note |
|---|---|---|---|
| Molecular weight | 180.16 g/mol | 180.16 | agree |
| cLogP | XLogP3 = 1.2 | ALogP = 1.31 | agree (~1.2–1.3) |
| TPSA | 63.6 Ų | 63.6 Ų | agree |
| H-bond donors | 1 | 1 | agree — the carboxylic-acid OH; the ester has no OH |
| H-bond acceptors | 4 | 3 | **disagree** — PubChem uses the original Lipinski N+O count (all 4 oxygens); ChEMBL/RDKit's refined HBA SMARTS excludes one non-basic oxygen. Flagging rather than picking one silently. |
| Rotatable bonds | 3 | 2 | **disagree** — convention difference on whether the aryl‑O(ester) bond counts. 3 (acetyl‑O, O‑aryl, aryl‑C(=O)) is the standard RDKit `NumRotatableBonds` count for this scaffold. |
| Heavy atoms | 13 | — | — |
| Exact mass | 180.0423 | — | — |
| Aromatic rings | 1 (derived from structure) | — | one benzene ring |
| Fraction Csp3 | ~0.11 (1 sp3 C / 9 total C — only the methyl) | — | derived, not pulled from an API |

**Interpretation:** very low MW, low-to-moderate lipophilicity, and a compact polar surface area — this is a small, polar-enough-but-not-too-polar molecule, consistent with good passive GI absorption and negligible CNS penetration expectation (TPSA well above the ~90 Ų rule-of-thumb ceiling some use for brain penetration, though aspirin does cross to a limited extent — treat that as a separate, dose-dependent clinical fact, not a descriptor conclusion).

## 3. Rule-set flags (descriptor → threshold → verdict)

| Rule | Criteria (published threshold) | Aspirin's values | Verdict |
|---|---|---|---|
| **Lipinski Ro5** (Lipinski et al. 2001) | MW≤500, cLogP≤5, HBD≤5, HBA≤10, ≤1 violation tolerated | MW 180.2✓, cLogP 1.2✓, HBD 1✓, HBA 3–4✓ | **PASS**, 0 violations |
| **Veber** (Veber et al. 2002) | RotBonds ≤10, TPSA ≤140 Ų | RotBonds 3✓, TPSA 63.6✓ | **PASS** |
| **Egan / "Egan egg"** (Egan et al. 2000) | TPSA within ~0–132 Ų and LogP within ~‑1 to 6, for predicted good passive human intestinal absorption | TPSA 63.6✓, LogP 1.2✓ | **PASS** — inside the absorption region |
| **Muegge** (Muegge et al. 2001) | MW 200–600, cLogP ‑2 to 5, TPSA≤150, rings≤7, C>4, heteroatoms>1, RotBonds≤15, HBA≤10, HBD≤5 | MW **180.2 — below the 200 floor** ✗; all other criteria pass | **FAIL (1 violation)** — flagged only on the MW lower bound |

Traceable point worth keeping: Muegge is the one rule set that flags aspirin, and only because it sets a *floor* of 200 Da meant to screen out fragment-like non-drug molecules — a known false-positive-prone edge for small, fully-approved drugs. Not a real liability signal here, just a reminder that rule-set disagreement itself is informative and worth reporting rather than collapsing to a single pass/fail.

## 4. Structural alerts (PAINS / BRENK)

I could not execute RDKit's `FilterCatalog` in this session (blocked tool), so this is a **reasoned prediction, not a logged filter match** — flagging that explicitly per the no-fabrication rule:

- **PAINS** (Baell & Holloway, *J. Med. Chem.* 2010): the PAINS substructure library targets reactive/promiscuous motifs — rhodanines, catechols, quinones, phenolic Mannich bases, ene-diones, toxoflavins, etc. Aspirin's structure (a simple aryl ester + carboxylic acid on a plain benzene ring) contains none of these SMARTS patterns. **Expected: no PAINS alert.**
- **BRENK** (Brenk et al., *ChemMedChem* 2008): flags Michael acceptors, aldehydes, thiols, aromatic nitro groups, perhalides, etc. None present. **Expected: no BRENK alert.**
- **Worth noting outside the standard filter catalogs:** aspirin's acetate ester *is* a mild, biologically relevant acylating agent (it acetylates COX-1/2 serine residues, and non-specifically acetylates albumin/hemoglobin at high exposure) — this is real, well-documented pharmacology, but it isn't something the canonical PAINS/BRENK SMARTS sets encode, so don't expect it to surface as a "hit" if you run the filter — it's a mechanism-level fact, not a substructure alert.

**Action item:** rerun this step with a live RDKit `FilterCatalog` (script below) before treating "no alert" as final — this is a prediction from knowing the scaffold, not a computed match.

## 5. Measured ADMET-relevant data (ChEMBL / PubChem records)

Pulled live from ChEMBL's activity API (`molecule_chembl_id=CHEMBL25`) and PubChem's BioAssay cross-reference for CID 2244.

| Endpoint | Value | Source (traceable ID) |
|---|---|---|
| Plasma protein binding (proxy) | Human serum albumin binding, Log K′ = 1.39 | ChEMBL assay CHEMBL702885 / document CHEMBL1134302 |
| LogD (pH 7.4) | ‑2.57 | ChEMBL assay CHEMBL631372 / document CHEMBL1131302 |
| Aqueous solubility | Log S = ‑1.72 | ChEMBL assay CHEMBL631962 / document CHEMBL1132890 |
| Human oral absorption | 100% | ChEMBL assay CHEMBL628746 / document CHEMBL1131302 |
| CYP2C9 (qHTS inhibitor/substrate) | **Inactive** | PubChem AID 883 |
| CYP3A4 (qHTS inhibitor/substrate) | **Inactive** | PubChem AID 884 |
| CYP3A4 (qHTS activator) | **Inactive** | PubChem AID 885 |
| CYP2D6 (qHTS inhibitor/substrate) | **Inactive** | PubChem AID 891 |
| CYP2C19 (qHTS inhibitor/substrate) | **Inactive** | PubChem AID 899 |
| hERG | **No public assay record found** in ChEMBL or PubChem BioAssay for this compound | — gap, not a negative result |
| Microsomal stability (liver-microsome t½) | **No public assay record found** | — gap |
| Caco-2 / MDCK permeability | **No public assay record found** | — gap |

**On-target pharmacology found in the same pull (context, not ADMET):** COX-1 IC50 12.5 µM (ovine, CHEMBL764258), COX-2 IC50 62.5 µM (human, CHEMBL760085) — consistent with aspirin's known COX-1 selectivity.

**Filling the three gaps (hERG, microsomal stability, Caco-2) — general medicinal-chemistry/clinical knowledge, explicitly not a specific assay record:**
- *hERG:* aspirin has no reported QT-prolongation or hERG liability signal across a century of clinical use; this is a clinical-experience inference, not a measured IC50.
- *Microsomal stability:* a standard liver-microsome CYP-turnover assay is a poor fit for this molecule specifically — aspirin's dominant clearance route is non-CYP esterase-mediated hydrolysis to salicylic acid (plasma/tissue esterases, t½ ≈ 15–20 min for the parent ester), not oxidative CYP metabolism. That's a mechanistic/pharmacology fact (well established in standard pharmacology references), not something a microsomal stability assay would even be designed to capture correctly.
- *Caco-2 permeability:* no logged Caco-2 Papp value found; the 100% human-absorption ChEMBL record above is the closest measured proxy for permeability/absorption.

## 6. Overall verdict

- **Rule-set profile:** clean pass on Lipinski, Veber, and Egan; one Muegge violation (MW below its 200 Da floor) that reflects a rule-set edge case for small approved drugs rather than a real risk.
- **Structural alerts:** no PAINS/BRENK hits expected — pending a live RDKit confirmation run.
- **Measured DMPK anchor:** solubility and PPB-proxy data exist and look benign (Log S ‑1.72 is reasonably soluble; albumin binding is moderate); CYP2C9/3A4/2D6/2C19 inhibition data (all inactive, qHTS) rules out classic CYP-inhibition DDI liability at screening concentrations.
- **Top three open PK questions for a screening hit with this profile, in priority order:**
  1. No hERG data exists in public databases for this exact compound — for a *novel* hit with an aspirin-like ester/acid scaffold, don't assume "safe" from aspirin's clinical history; run an actual hERG patch-clamp or fluorescence assay.
  2. No Caco-2/microsomal data — get a direct permeability assay rather than relying on the absorption/rule-based proxies above, especially since a standard CYP-turnover microsomal assay may under-report clearance for esterase-cleared analogs.
  3. Confirm the PAINS/BRENK "no alert" call with an actual RDKit `FilterCatalog` run rather than the reasoned prediction given here.

---

## Reproducible script (run this to get exact, tool-verified numbers)

```python
# pk_card.py — regenerate this report's computed sections exactly
# pip install rdkit medchem requests
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

smiles = "CC(=O)Oc1ccccc1C(=O)O"
mol = Chem.MolFromSmiles(smiles)

descriptors = {
    "MW": Descriptors.MolWt(mol),
    "cLogP": Crippen.MolLogP(mol),
    "TPSA": rdMolDescriptors.CalcTPSA(mol),
    "HBD": rdMolDescriptors.CalcNumHBD(mol),
    "HBA": rdMolDescriptors.CalcNumHBA(mol),
    "RotBonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
    "AromaticRings": rdMolDescriptors.CalcNumAromaticRings(mol),
    "FractionCSP3": rdMolDescriptors.CalcFractionCSP3(mol),
}
print(descriptors)

lipinski = (descriptors["MW"] <= 500 and descriptors["cLogP"] <= 5
            and descriptors["HBD"] <= 5 and descriptors["HBA"] <= 10)
veber = (descriptors["RotBonds"] <= 10 and descriptors["TPSA"] <= 140)
egan = (0 <= descriptors["TPSA"] <= 132 and -1 <= descriptors["cLogP"] <= 6)
muegge = (200 <= descriptors["MW"] <= 600 and -2 <= descriptors["cLogP"] <= 5
          and descriptors["TPSA"] <= 150 and descriptors["RotBonds"] <= 15
          and descriptors["HBA"] <= 10 and descriptors["HBD"] <= 5)
print({"Lipinski": lipinski, "Veber": veber, "Egan": egan, "Muegge": muegge})

params = FilterCatalogParams()
params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
params.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
catalog = FilterCatalog(params)
matches = catalog.GetMatches(mol)
print([m.GetDescription() for m in matches] or "no PAINS/BRENK alerts")
```

This is the same script the underlying recipe was field-validated with (caffeine, ibuprofen, quercetin, terfenadine, per its June 2026 field report) — running it here would close the one caveat in this report (the blocked local execution) with zero other changes to the workflow.