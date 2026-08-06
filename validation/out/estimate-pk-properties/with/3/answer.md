## Recipe match

This matches an existing curated recipe in the sci-ai-enabler knowledge base: **[Estimate Pharmacokinetic Properties of a Small Molecule](https://scripps-ai-enablement.github.io/sci-ai-enabler/recipes/items/estimate-pk-properties.html)** — RDKit descriptors + MedChem rule/alert flags + ChEMBL measured endpoints, no ML predictor. Evidence: **Reported** (field-tested on 4 compounds, no published benchmark). Availability: **Fully open**. Compute: **Laptop**, <1 min.

Below is that recipe run by hand for **aspirin** (`CC(=O)Oc1ccccc1C(=O)O`, ChEMBL25 / PubChem CID 2244), since no compound was given. Every number is either fetched live this session (PubChem PUG-REST, ChEMBL REST API, DailyMed) or flagged where it wasn't.

## 1. Physicochemical descriptors
*Source: PubChem CID 2244 computed-properties record, fetched this session.*

| Descriptor | Value | Note |
|---|---|---|
| MW | 180.16 g/mol | |
| XLogP3 | 1.2 | PubChem's Crippen-type consensus logP |
| TPSA | 63.6 Ų | ester O (~26.3) + carboxylic acid (~37.3) |
| Rotatable bonds | 3 | ester C–O, O–aryl, aryl–C(=O)OH; the C–OH bond doesn't count (terminal O) |
| HBD | 1 | carboxylic OH |
| HBA (N+O) | 4 | all 4 oxygens, 0 N |
| Heavy atoms | 13 | C9H8O4 |
| Aromatic rings / total rings | 1 / 1 | |
| Fraction Csp3 | ~0.11 (1/9 C) | 1 sp3 methyl vs. 8 sp2 carbons |

## 2. Rule-of-thumb flags

| Rule | Thresholds | Aspirin | Verdict |
|---|---|---|---|
| **Lipinski Ro5** | MW≤500, LogP≤5, HBD≤5, HBA≤10 | 180.16 / 1.2 / 1 / 4 | **PASS**, 0 violations |
| **Veber** | RotB≤10, TPSA≤140 Ų | 3 / 63.6 | **PASS** |
| **Egan** | −1≤LogP≤5.88, TPSA≤131.6 Ų (HIA-favorable region) | 1.2 / 63.6 | **PASS** — sits comfortably in the absorption ellipse |
| **Muegge** | 200≤MW≤600, −2≤LogP≤5, TPSA≤150, rings≤7, C>4, heteroatoms>1, RotB≤15, HBA≤10, HBD≤5 | MW=180.16 | **FAIL** — MW is below Muegge's 200 g/mol floor; every other criterion passes |

The Muegge miss is a real, traceable artifact: aspirin is simply too small for a rule tuned on typical drug-sized leads, not a red flag on its own.

**BOILED-Egg geometry** (using the same LogP/TPSA point): TPSA 63.6<79 Ų and LogP 1.2 puts it near the edge of the BBB-permeant region, not just the HIA yolk. Take that with a grain of salt — clinically aspirin's CNS exposure is limited by efflux transport and by ionization of the carboxylate at physiological pH, effects the 2D descriptor geometry doesn't capture.

## 3. Structural alerts (PAINS / BRENK)
*Caveat: I did not get a live RDKit `FilterCatalog` run in this session (the sandbox blocked local Python execution), so this is expert substructure reasoning against the published Baell & Holloway 2010 (480 SMARTS) and Brenk 2008 (105 SMARTS) sets, not a machine-verified result.*

- **PAINS**: no match. Aspirin has none of the reactive/promiscuous cores the filter targets (no rhodanine, quinone, catechol, azo, hydrazone, Michael acceptor).
- **BRENK**: no match. No aldehyde, thiol, imine, N-halide, or other flagged group.
- The one real liability — the acetate ester — isn't a formal PAINS/BRENK hit, but it *is* the mechanistic reason aspirin is chemically/metabolically short-lived (see §4). Worth flagging even though no rule caught it.

If you want this verified rather than reasoned, the MedChem skill referenced by the recipe runs the actual RDKit FilterCatalog in under a second.

## 4. Measured ADMET data (grounded, ChEMBL25 + FDA label via DailyMed)

| Endpoint | Finding | Source |
|---|---|---|
| **hERG** | DRUGMATRIX hERG radioligand binding: inactive (no IC50/Ki). Direct KCNH2 inhibition assay: AC50 = 30,000 nM (30 µM) — negligible vs. the ~1–10 µM range that flags real liability. | ChEMBL25 activities, target CHEMBL240 |
| **CYP450 (1A2, 2C9, 2C19, 2D6, 3A4)** | IC50/Ki reported as inactive across all five isoforms tested (fold-change ≈1.0 for 3A4/2D6/2C9-mediated metabolism assays; CYP2C19 IC50-ratio ≈2.0). No significant direct CYP inhibition. | ChEMBL25 activities, targets CHEMBL340/289/3397/3356/3622 |
| **Plasma protein binding** | Human clinical data (FDA label): ~90–94% albumin-bound at therapeutic concentrations (≤80 µg/mL), falling to ~30% in overdose — classic saturable binding. In vitro BSA surrogate assay (ChEMBL, 2024) shows the same concentration-dependence: 90%→84%→52% as drug:protein ratio widens. | [DailyMed aspirin label](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=d8b5d5b4-44d2-4f8f-8c11-e4fc96504f59); ChEMBL25 "Albumin" target activities |
| **Metabolic/microsomal stability** | Not a CYP-oxidation story: aspirin is rapidly deacetylated by esterases (hepatic carboxylesterase, plasma pseudocholinesterase, erythrocyte acetylhydrolase) to salicylic acid. Plasma half-life of intact aspirin ≈15–20 min; salicylate half-life ≈2–3 h at low dose, prolonged (up to ~15–30 h) at high/saturating dose. | FDA label PK section, via DailyMed |
| **Permeability** | No ChEMBL Caco-2/PAMPA record surfaced for this compound in the queries run. Consistent with the low TPSA/moderate LogP profile (§1–2) predicting high passive permeability, but I'm not citing a specific measured Papp — flag as **not found**, not measured=0. |  |
| **Aqueous solubility** | ~3–4.6 mg/mL at 25 °C across independent sources (Merck Index: 1 g/300 mL @25°C ≈3.3 mg/mL; AQUASOL DB: 4600 mg/L); pH-dependent given the ionizable carboxylic acid (pKa ≈3.5). | PubChem CID 2244 Solubility records |

## 5. Synthesized early-ADMET picture

- **Druglike by size/polarity**: passes Lipinski and Veber cleanly (§2); Muegge's one miss is a small-molecule artifact of MW, not a real absorption concern given TPSA/LogP already predict good passive permeability.
- **No structural red flags**: zero PAINS/BRENK hits (§3, reasoned not machine-verified) — nothing here would trip an assay-interference or reactive-toxicophore filter.
- **Low off-target/cardiac risk by the standard screens**: no CYP450 inhibition and no hERG activity across five isoforms + a direct channel assay (§4) — this chemotype is not the source of aspirin's real-world DDI profile (that comes from displacement/PD interactions like warfarin potentiation, not CYP inhibition).
- **The actual liability is chemical, not rule-based**: the acetate ester makes aspirin intrinsically short-lived (t½ ~15–20 min) via esterase hydrolysis rather than CYP metabolism — a fact the rule sets and alert filters both miss, but that ChEMBL/FDA-label data catches directly.
- **PPB is concentration-dependent and saturable** — a nonlinear-PK flag worth carrying into any in vivo PK modeling later, sourced independently from both clinical label data and an in vitro BSA assay.
- **Gap to flag**: no Caco-2/PAMPA permeability record was found for the exact compound in this pass — if permeability matters for your hit, that's the piece to chase down (closest-neighbor read-across or a fresh assay), not to assume from TPSA alone.

To run this workflow on a real new hit (not aspirin), the three components are the RDKit Cheminformatics Skill and MedChem Skill (K-Dense marketplace) plus the ChEMBL Connector (Anthropic life-sciences marketplace) — I can install and wire those up on request.