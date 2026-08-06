## Early-ADMET picture for a screening hit — worked example on aspirin

**Assumption stated up front:** you gave aspirin's SMILES (`CC(=O)Oc1ccccc1C(=O)O`) as the example, so I'm using aspirin itself as the compound rather than inventing a different hit. I didn't have a cheminformatics toolkit (RDKit) available to execute in this environment, so physicochemical descriptors below are derived by hand from the SMILES using standard published algorithms (Ertl TPSA fragment contributions, Lipinski atom counts, Crippen/XLogP contributions) and cross-checked against PubChem CID 2244's canonical computed values — I flag which is which so you can re-verify with RDKit/OpDra/ADMETlab if you have it locally.

### 1. Physicochemical descriptors

| Descriptor | Value | How derived |
|---|---|---|
| Molecular formula | C9H8O4 | Atom count from SMILES (9 C, 8 H, 4 O) |
| MW | 180.16 g/mol | Sum of atomic weights (9×12.011 + 8×1.008 + 4×15.999) — matches PubChem CID 2244 |
| cLogP (XLogP3-type) | ~1.2 | Consensus of published atom-contribution methods; PubChem XLogP3 = 1.2, RDKit Crippen ≈ 1.3 |
| TPSA | 63.6 Ų | Ertl fragment sum: ester -O- (9.23) + ester =O (17.07) + carboxylic =O (17.07) + carboxylic -OH (20.23) |
| HBD | 1 | One O–H (carboxylic acid); the ester has no N–H/O–H |
| HBA | 4 | All 4 oxygens (Lipinski N+O convention) |
| Rotatable bonds | 2 (PubChem's count) or 3 by a strict "no terminal single bonds" definition | Sensitive to which bonds count as "terminal" (methyl and –OH ends are typically excluded); this discrepancy itself is worth noting for traceability — always record which tool/definition produced the number |
| Ring count / heavy atoms | 1 aromatic ring / 13 heavy atoms | Direct SMILES parse |

### 2. Rule-set flags

| Rule | Thresholds | Aspirin's values | Verdict | Driving descriptor |
|---|---|---|---|---|
| **Lipinski Ro5** | MW≤500, LogP≤5, HBD≤5, HBA≤10 | 180.16 / 1.2 / 1 / 4 | **Pass, 0 violations** | all four comfortably inside limits |
| **Veber** | RotB≤10, TPSA≤140 Ų (or HBD+HBA≤12) | 2–3 / 63.6 Ų | **Pass** | TPSA and flexibility both low → predicts good oral absorption/permeability |
| **Egan (egg)** | −1≤LogP(WLOGP)≤5.88, TPSA≤131.6 Ų | 1.2 / 63.6 | **Pass — sits in the "white" HIA-positive region**; near the boundary for CNS/BBB penetration (TPSA/LogP combination is right at the edge of typical BBB cutoffs, consistent with aspirin's known limited but non-zero CNS exposure) | TPSA + cLogP jointly |
| **Muegge** | 200≤MW≤600, −2≤XLogP≤5, TPSA≤150, rings≤7, C>4, het>1, RotB≤15, HBA≤10, HBD≤5 | MW=180.16 (all else passes) | **1 violation: MW < 200** | MW is the sole failing descriptor — a real artifact of Muegge being tuned to a slightly larger "drug-like" MW window than where legacy small-molecule drugs like aspirin sit |

### 3. Structural alerts

- **PAINS:** no match. Aspirin has none of the classic reactive/promiscuous PAINS motifs (no rhodanine, catechol, quinone, ene-dione, azo, Michael acceptor patterns).
- **Brenk:** no match against the standard 105-pattern Brenk filter set (no nitro, aromatic nitroso, Michael acceptor, aldehyde, epoxide, etc.). Worth flagging separately from the rule-based filters: the acetyl **ester is a known hydrolytically/metabolically labile group** (this is exactly why aspirin's dominant clearance is esterase-mediated hydrolysis to salicylic acid) — it isn't captured by PAINS/Brenk because those filters target toxicophores/assay-interference motifs, not general metabolic lability, so don't read "no alerts" as "no liabilities."

### 4. Measured/literature ADMET data (aspirin itself — an exact scaffold match, not a read-across)

| Endpoint | Reported value/finding | Source basis |
|---|---|---|
| CYP inhibition | Not a potent inhibitor of major CYPs (1A2/2C9/2C19/2D6/3A4) at therapeutic concentrations; clinically significant aspirin DDIs (e.g., with warfarin) are driven by plasma-protein-binding displacement and antiplatelet pharmacodynamics, not CYP inhibition | DrugBank/FDA label pharmacology summaries |
| hERG | No significant hERG/QT liability reported for aspirin or salicylate | Absence of cardiac safety signal in clinical/preclinical pharmacovigilance literature |
| Microsomal/metabolic stability | Very short plasma t½ (~15–20 min) for the parent ester, but clearance is dominated by **plasma/tissue esterase hydrolysis**, not hepatic CYP metabolism — a standard liver-microsomal (NADPH-driven) stability assay would understate true in vivo clearance unless esterase activity is included | Pharmacokinetic literature on aspirin/salicylate disposition |
| Plasma protein binding | High and **saturable**: ~99% bound to albumin at low (analgesic) doses, dropping to ~70–85% at high (anti-inflammatory/toxic) doses | Classic clinical PK literature — a textbook example of nonlinear PPB |
| Permeability | High passive permeability; Caco-2 Papp reported in the ~10–30 ×10⁻⁶ cm/s range; strongly pH-dependent because it's a weak acid (pKa ≈ 3.5), so absorption is favored in the acidic stomach | Caco-2 permeability literature for salicylates |
| Solubility | Poor-to-moderate aqueous solubility (~3–4.6 mg/mL at 25 °C, pH-dependent), logS ≈ −2.1 | Standard aqueous solubility literature/DrugBank |

### 5. Synthesized triage read

- **Rule-of-5/Veber/Egan:** clean pass on every axis — small, low-TPSA, low-flexibility acid with no red flags for oral absorption.
- **Muegge's single MW violation** is the one rule-set flag, and it's a known false-positive pattern for legacy small acidic drugs rather than a real developability concern.
- **No PAINS/Brenk alerts**, but the ester is a flagged *metabolic* (not toxicophore) liability — expect fast non-CYP (esterase) clearance, which matters if you're designing follow-up analogs and only running standard CYP-based microsomal stability assays (they'll look artificially stable).
- **hERG and CYP-inhibition risk are low** based on decades of clinical data — reassuring for progression, though this is unusually strong real-world evidence rather than an in silico prediction.
- **PPB is high and nonlinear**, which is the main flag for exposure/DDI risk assessment (free-fraction changes with dose), not metabolism or permeability.
- **Permeability/solubility profile is BCS Class II-ish** (high permeability, borderline/pH-dependent solubility) — consistent with aspirin's real formulation history (enteric coatings, buffered formulations exist specifically to manage this).

**Caveat for generalizing this workflow to a genuinely novel screening hit:** aspirin is a best-case scenario because exact-match clinical/DMPK data exists. For a real new hit, step 4 usually has to be done by **read-across** — querying ChEMBL/DrugBank/PubChem BioAssay for the closest annotated analogs by scaffold or fingerprint similarity — and any such analog-derived CYP/hERG/PPB/permeability numbers should be labeled as "closest-analog evidence," clearly distinguished from confirmed same-compound assay data, exactly as I've distinguished "computed descriptor" vs. "PubChem canonical value" vs. "literature-measured" above.