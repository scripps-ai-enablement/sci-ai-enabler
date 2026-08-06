# Early-ADMET Profile — Worked From SMILES Alone

**Assumption stated up front (single-shot rule):** I'm using aspirin (`CC(=O)Oc1ccccc1C(=O)O`, PubChem CID 2244) as the worked compound, exactly as given. Steps 1–3 below are computed directly from the SMILES/structure and generalize to any hit. Step 4 (measured CYP/hERG/microsomal/PPB/permeability/solubility) cannot come from the SMILES itself for a *genuinely novel* hit — there's no assay data for a molecule nobody has tested yet. Since aspirin is not novel, real literature/assay records exist for it, so I've pulled those and labeled them as **scaffold-level read-across**, which is exactly the kind of evidence you'd substitute with analog data for an actual new hit.

**Tooling disclosure:** This sandbox blocked local Python/RDKit execution, so I did not run a live SMARTS filter. The descriptor table is pulled from PubChem's computed-properties record for this exact structure (not re-derived by me), rule verdicts are threshold checks against those numbers, and the PAINS/Brenk screen is a manual check against the published alert lists rather than an automated FilterCatalog run — flagging this so you know where to re-verify (RDKit `FilterCatalog` or SwissADME) before trusting it for a real triage decision.

## 1. Physicochemical descriptors
Source: [PubChem CID 2244 computed properties](https://pubchem.ncbi.nlm.nih.gov/compound/Aspirin) (PubChem 2.2 / Cactvs 3.4.8.18)

| Descriptor | Value | 
|---|---|
| Molecular weight | 180.16 g/mol |
| cLogP (XLogP3) | 1.2 |
| TPSA | 63.6 Ų |
| H-bond donors | 1 |
| H-bond acceptors | 4 |
| Rotatable bonds | 3 |
| Heavy atoms | 13 |
| pKa (carboxylic acid) | 3.5 ([FIP biowaiver monograph](https://www.fip.org/files/fip/BPS/BCS/Monographs/AcetylsalicylicAcid.pdf)) |

## 2. Rule-set flags (each traced to the descriptor driving it)

| Rule set | Threshold | Aspirin value(s) | Verdict |
|---|---|---|---|
| **Lipinski Ro5** | MW≤500, LogP≤5, HBD≤5, HBA≤10 | 180.16 / 1.2 / 1 / 4 | **Pass, 0 violations** — drug-like by all four cutoffs |
| **Veber** | RotB≤10, TPSA≤140 Ų | 3 / 63.6 | **Pass** — low flexibility, good predicted passive permeability |
| **Egan** | −1≤LogP≤5.88, TPSA≤131.6 Ų | 1.2 / 63.6 | **Pass** — falls inside the "well-absorbed" ellipse |
| **Muegge** | MW 200–600, LogP −2–5, TPSA≤150, rings≤7, rotB≤15, HBA≤10, HBD≤5 | MW=180.16 (below floor); all others pass | **1 violation — MW < 200** |

The Muegge failure is a known quirk of that filter, not a real developability signal: it's driven purely by the sub-200 Da lower-bound, which many small approved drugs (aspirin, isoniazid, etc.) fail. Treat it as "fragment-sized," not "non-drug-like."

## 3. Structural alerts (manual check against Baell & Holloway 2010 PAINS list; Brenk et al. 2008 unwanted-functionality list)

- **PAINS**: no hits — no rhodanine, quinone, catechol, ene-dione, Michael-acceptor, azo, or other classic promiscuity motifs present.
- **Brenk**: no hits — the molecule has no aldehyde, acyl halide, Michael acceptor, or other flagged reactive group; a simple aromatic acetate ester isn't on Brenk's list.
- **Mechanistic caveat the filters miss**: the acetate ester *is* reactive enough to acylate a serine residue (COX-1 Ser530) — that's aspirin's actual mechanism, not a false positive. SMARTS-based filters won't catch this because "aromatic ester" isn't a toxicophore per se. Worth flagging for any hit carrying a similarly activated ester in an HTS context: it can look like a clean, filter-passing hit while still being a serine-hydrolase-reactive false positive in unrelated assays.

## 4. Measured ADME data — scaffold/analog read-across (aspirin/salicylate literature)

| Endpoint | Finding | Source |
|---|---|---|
| **CYP inhibition** | Weak, non-potent inhibitor. Rat CYP3A2: Ki=95.5±4.3 µM, IC50=191±8.5 µM ("weak inhibitory effect"). Metabolism itself is mostly esterase-driven (deacetylation), with CYP2C9 proposed as a minor contributor and CYP2E1 dominant among P450s for aromatic hydroxylation to gentisic acid — CYP involvement is on the clearance side, not a DDI-liability side. | [Novel HPLC CYP3A2 inhibition study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8838585/); [Aromatic hydroxylation by human CYPs](https://pmc.ncbi.nlm.nih.gov/articles/PMC4414920/) |
| **hERG** | No dedicated aspirin/salicylate hERG IC50 in the literature I could locate — searches returned only other ion-channel effects (glycine, NMDA, GABA-A receptors) and hERG data for unrelated NSAIDs (e.g., celecoxib IC50 ≈6 µM). Absence of a reported hERG signal for a 60+ year old, massively-studied drug is itself informative (low cardiac-channel liability expected for this small, ionized, TPSA>60 acid), but this is inference from absence, not a positive assay record — flag as an actual data gap to fill, not a confirmed "clean" result. | Search of hERG/salicylate literature, no positive hit |
| **Metabolic stability** | Primary clearance is **esterase-mediated hydrolysis** (plasma, RBC, hepatic carboxylesterases) to salicylic acid, not CYP oxidation. **This is the key gotcha for any hit with a hydrolyzable ester**: a standard NADPH-dependent liver-microsome stability assay under-samples esterase clearance and will overestimate metabolic stability unless the microsomal prep retains esterase activity or is run alongside a plasma-stability assay. | [StatPearls: Salicylic Acid (Aspirin)](https://www.ncbi.nlm.nih.gov/books/NBK519032/) |
| **Plasma protein binding** | Aspirin itself: moderate and variable, ~50–58% by in-vivo ultrafiltration up to ~85–90% in older in-vitro (BSA) work. Its active metabolite salicylate: high (~80–95%) but **saturable/dose-dependent** — falls to ~30% at toxic concentrations as albumin sites saturate. Any hit sharing the free carboxylic acid should be assumed to show nonlinear PPB at high exposure. | [In-vivo ultrafiltration PPB study](https://pubmed.ncbi.nlm.nih.gov/9542472/); [Porcine/human serum PPB](https://pubmed.ncbi.nlm.nih.gov/7571349/) |
| **Permeability** | BCS Class I (high solubility, high permeability) per the FIP Biowaiver monograph; consistent with low TPSA (63.6 Ų, under the ~90 Ų high-passive-absorption cutoff) and low rotatable-bond count. No isolated numeric Caco-2 Papp for unmodified aspirin surfaced in this search — the BCS I classification is the traceable record, not a specific Papp value. | [FIP/BCS Biowaiver Monograph — Acetylsalicylic Acid](https://www.fip.org/files/fip/BPS/BCS/Monographs/AcetylsalicylicAcid.pdf) |
| **Solubility** | Aqueous solubility ≈3.8–4.6 mg/mL at pH 7.4/37 °C; pKa 3.5 means solubility is strongly pH-dependent (much lower in gastric fluid, higher at intestinal pH) — classic weak-acid behavior. | pKa/solubility literature cited above |

## Synthesis — early-ADMET picture

- **Physicochemical/rule-set profile is clean**: 0/4 Lipinski violations, passes Veber and Egan; the sole Muegge flag (MW<200) is a filter artifact, not a real risk.
- **No structural alerts** from PAINS/Brenk, but the acetate ester is a mechanism-relevant reactive group worth a manual note for any HTS series with similar esters (serine-hydrolase false-positive risk).
- **DDI risk via CYP looks low** (weak/non-potent inhibition reported); clearance is dominated by esterases, not CYPs — so a CYP-inhibition panel is lower priority than confirming esterase-mediated turnover for this chemotype.
- **hERG is an actual open data gap** — no confirmed assay record found; this is the first thing I'd send for an actual hERG patch-clamp or fluorescence assay rather than assume clean.
- **PPB is nonlinear/saturable** for the carboxylic-acid metabolite — if the hit series retains a free acid, plan protein-binding characterization across a concentration range, not a single-point value.
- **Permeability/solubility are favorable** (BCS I, TPSA-consistent), so absorption risk is low; the main assay gap is a modern Caco-2 Papp measurement, since I could only source the BCS classification, not a numeric value.

**Recommended next wet-lab assays**, in priority order given the gaps above: (1) hERG patch-clamp (no reliable literature value exists), (2) plasma/hepatic esterase stability run alongside conventional CYP-microsome stability (esterase clearance won't show up in a standard NADPH assay), (3) concentration-ranged PPB (nonlinear binding expected if a free acid is retained), (4) a direct Caco-2 Papp measurement to replace the BCS-based inference.