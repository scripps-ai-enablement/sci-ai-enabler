# Target Validation Report — SOAT1 (ACAT1) for Familial Hypercholesterolemia

**Skill:** `tooluniverse-drug-target-validation` · **Backend:** ToolUniverse MCP (`uvx tooluniverse`)
**Date:** 2026-07-23 · **Modality assessed:** small molecule

---

## Executive Summary

- **Target Validation Score: 48 / 100**
- **Priority Tier: Tier 3 (CAUTION) — numerically**
- **Recommendation: 🔴 NO-GO for familial hypercholesterolemia**

SOAT1 is a highly druggable enzyme (DoGSite drugScore 0.86; 880 ChEMBL activities; 5 cryo-EM structures) but fails the disease-association gate: it is **not a Mendelian/GWAS FH gene**, its only Open Targets link to familial hyperlipidemia is `clinical_precedence` (a drug was *tried*), and that drug (pactimibe) **failed and harmed patients in the exact indication** (CAPTIVATE). Genetic and pharmacologic loss-of-function **worsen** atherosclerosis in mice. In a sequential gate model, high druggability cannot rescue wrong-direction biology.

---

## Phase 0 — Identifier Resolution

| Namespace | ID | Tool → value |
|---|---|---|
| Gene symbol | SOAT1 | `MyGene_query_genes(query=SOAT1)` |
| HGNC | 11177 | `MyGene_query_genes` → HGNC 11177 |
| Ensembl | ENSG00000057252 | `MyGene_query_genes` → ensembl.gene |
| Entrez | 6646 | `MyGene_query_genes` |
| UniProt | P35610 (SOAT1_HUMAN) | `MyGene_query_genes` → Swiss-Prot; `alphafold_get_summary` |
| ChEMBL target | CHEMBL2782 | ChEMBL (human SINGLE PROTEIN) |
| Function | Cholesterol-esterifying acyltransferase; lipoprotein assembly + dietary cholesterol absorption | `UniProt_get_function_by_accession(P35610)` |
| Class | MBOAT-family, multipass ER membrane enzyme (Pfam PF03062) | ChEMBL / InterPro |

Aliases: ACAT1, ACAT, SOAT, ACACT, STAT.

---

## Validation Scorecard

| Gate | Sub-dimension | Score | Key tool → value |
|---|---|---|---|
| **Disease association (30)** | Genetic (10) | **1** | `OpenTargets` FH datasource = `clinical_precedence` 0.608 only; no GWAS/genetic/ClinVar. `gnomad_get_gene_constraints` pLI 2.8e-15, oe_lof 0.79 (LoF-tolerant). ClinVar 0 pathogenic. |
| | Literature (10) | **4** | OT europepmc = cancer-dominated (neoplasm 0.94); lipid literature mechanistic/refuting. |
| | Pathway (10) | **6** | KEGG hsa04979 cholesterol metabolism; Reactome SOAT1/LDL clearance; UniProt cholesterol esterification. Direction of effect adverse. |
| **Druggability (25)** | Structure (10) | **9** | 5 cryo-EM PDBs (6VUM etc.); `alphafold_get_summary` pLDDT 80.62; **DoGSite drugScore 0.86** (`ProteinsPlus_predict_binding_sites` on 6VUM). |
| | Chemical matter (10) | **9** | ChEMBL 880 activities, best IC50 35 nM; pactimibe/avasimibe/nevanimibe. |
| | Target class (5) | **3** | `OpenTargets_get_target_tractability` Druggable Family=true; intracellular membrane enzyme (AB flags false). |
| **Safety (20)** | Expression (5) | **2** | `GTEx` adrenal 126 TPM (highest), broad elsewhere; heart-LV 2.0, liver 5.9. |
| | Genetic validation (10) | **5** | gnomAD LoF-tolerant + KO viable (tolerable), BUT KO → dry eye, xanthomatosis, alopecia, leukocytosis, worsened atherosclerosis. |
| | ADRs (5) | **2** | pactimibe LDL-C ↑7.3%, major CV events 2.3% vs 0.2%; benfluorex valvulopathy (withdrawn). |
| **Clinical precedent (15)** | Highest stage | **4** | `OpenTargets` drugs: pactimibe PHASE_2_3 (TERMINATED), nevanimibe PHASE_2 (adrenal), benfluorex APPROVAL (withdrawn). Precedent is negative. |
| **Validation evidence (10)** | Functional (5) | **2** | Enzymology/SAR extensive; therapeutic hypothesis unsupported. |
| | Disease models (5) | **1** | Mouse KO (MGI:2174741/2174742) aggravates atherosclerosis + xanthoma. |
| **TOTAL** | | **48 / 100** | |

---

## Negative findings / data gaps (documented, not hidden)

- **No human genetic causality for FH.** FH is LDLR/APOB/PCSK9/LDLRAP1-driven; OT's FH search returns LDLR (ENSG00000130164), not SOAT1.
- **Clinical precedent is refuting**, not supporting: CAPTIVATE (JAMA 2009, DOI 10.1001/jama.301.11.1131) and ACTIVATE (NEJM 2006, DOI 10.1056/NEJMoa054699).
- **KO worsens disease** (Yagyu JBC 2000 10.1074/jbc.M002541200; Huang ATVB 2013 10.1161/ATVBAHA.112.301080; Wakabayashi ATVB 2018 10.1161/ATVBAHA.118.311648).
- **Tool gaps:** Pharos API 502; DepMap has no SOAT1 record; ADMET-AI GNN unavailable (ToolUniverse installed without `[ml]` extra) — substituted ChEMBL/RDKit physchem + real clinical ADR data.

## ML models contributing

| Model | Architecture | Contributed |
|---|---|---|
| AlphaFold | DeepMind SE(3) Transformer | Full-length model, avg pLDDT 80.62 |
| DoGSite3 | CNN pocket scorer (ProteinsPlus) | 61 pockets; top drugScore 0.86 (722 Å³, 24 Å deep) |
| ADMET-AI | Chemprop GNN | ATTEMPTED — package not provisioned; gap documented |

## Verdict

**NO-GO for familial hypercholesterolemia.** Sequential Gate 1 failure (no genetics) + negative late-stage clinical precedent in the exact indication + KO worsens disease. Druggability (21/25) is real but irrelevant here. **Pivot options:** SOAT2/ACAT2 (liver/intestine isozyme) for lipids; SOAT1 in adrenocortical carcinoma / CAH (nevanimibe) where genetics/precedent differ.
