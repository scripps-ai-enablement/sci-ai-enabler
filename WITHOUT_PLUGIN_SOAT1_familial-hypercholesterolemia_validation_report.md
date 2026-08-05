# SOAT1 × Familial Hypercholesterolemia — Target Validation

> **Methodology caveat:** No MCP data servers were connected when this report was
> produced. This is a **web-grounded degraded pass**, not the authoritative
> OpenTargets / ChEMBL / GTEx / gnomAD ToolUniverse pipeline that the
> `tooluniverse-drug-target-validation` skill is built on. Every value below is
> tagged with its actual source. Quantitative endpoints with no web substitute
> (gnomAD pLI/LOEUF, GTEx TPM, DoGSite pocket score, ADMET-AI / ESMFold /
> AlphaFold runs) are flagged **[tool-gap]** and were **not invented**.
>
> Date: 2026-07-23

---

## Phase 0 — Identifiers

Source: biomcp `get gene SOAT1` (captured before the server was removed).

| ID | Value | Source |
|---|---|---|
| HGNC symbol | **SOAT1** (aliases ACAT1, ACAT, SOAT, STAT) | biomcp / NCBI Gene |
| Ensembl | **ENSG00000057252** | biomcp |
| UniProt | **P35610** | biomcp |
| Entrez | 6646 | biomcp |
| OMIM | 102642 | biomcp |
| ChEMBL target ID | **[tool-gap]** — ChEMBL server removed; not tool-verified, not guessed | — |
| Class | Membrane-bound O-acyltransferase (MBOAT); multi-pass ER enzyme | HPA / UniProt |

---

## Gate 1 — Disease Association → **8 / 30**

| Sub | Score | Query → value |
|---|---|---|
| Genetic (10) | **1** | WebSearch FH causative genes → curated panels (Endotext, GeneReviews, MedlinePlus) list **LDLR (~80%), APOB, PCSK9, LDLRAP1** as the Mendelian FH genes. **SOAT1 does not appear in any FH gene panel.** No GWAS/Mendelian FH link. ❌ **Gate-1 genetic failure.** |
| Literature (10) | 4 | Large SOAT1/ACAT literature exists, but concerns cholesterol *esterification/storage* and atherosclerosis broadly — not FH causation. Indirect. |
| Pathway (10) | 3 | SOAT1 esterifies free cholesterol for storage; it is **downstream/parallel** to the LDLR-clearance axis that FH breaks. Modulating it does not correct the receptor defect driving FH. |

**Negative finding (not hidden):** SOAT1 has no human genetic association with familial
hypercholesterolemia. Per the skill's gating logic, a Gate-1 genetic failure is decisive
regardless of later gates.

---

## Gate 2 — Druggability → **22 / 25** (the target's one strength)

| Sub | Score | Query → value |
|---|---|---|
| Structure (10) | 9 | Cryo-EM structures exist: **PDB 6L47** (hSOAT1 + inhibitor CI-976), 6VUM; **3.5 Å**; inhibitor binds the catalytic chamber blocking active-site **H460, N421, W420** (*Nat Commun* 2020). |
| Chemical matter (10) | 9 | Abundant clinical-grade chemistry: **avasimibe, pactimibe, eflucimibe, CI-976, nevanimibe (ATR-101)**. |
| Target class (5) | 4 | Enzyme = tractable, but multi-pass ER membrane MBOAT is harder than a soluble enzyme; clinically proven druggable. |
| **[tool-gap]** | — | DoGSite pocket druggability score, AlphaFold/ESMFold pLDDT **not run** (no ProteinsPlus/ML tools). |

---

## Gate 3 — Safety in normal tissue → **8 / 20** (liability) *(higher = safer)*

| Sub | Score | Query → value |
|---|---|---|
| Critical-organ expression (5) | 2 | HPA: SOAT1 **overexpressed in adrenal gland (~11.4×)**, also liver, macrophages, GI. High expression in a critical steroidogenic organ = on-target risk. GTEx TPM **[tool-gap]**. |
| Mouse-KO (10) | 5 | *Soat1*/Acat1 KO mice are **viable (not embryonic-lethal)** — reassuring — **but** show hair loss, dry eye, xanthomatosis, cutaneous/brain cholesterol deposition (hyperlipidemic background), leukocytosis, **reduced lifespan** (JCI/PNAS). gnomAD constraint **[tool-gap]**. |
| Known ADRs (5) | 1 | On-target **adrenal insufficiency** is so reproducible it is the *therapeutic mechanism* of nevanimibe in Cushing's/CAH/ACC; plus GI (diarrhea 44%, vomiting 35%). ❌ Dangerous ADR profile for a chronic CV indication. |

---

## Gate 4 — Clinical Precedent → **5 / 15**

| Aspect | Finding | Source |
|---|---|---|
| Highest stage | **Phase 3 reached** (pactimibe ACTIVATE; avasimibe A-PLUS) | NEJM, Circulation |
| Outcome in FH | **CAPTIVATE (pactimibe, FH patients) terminated early — MACE *higher* on drug: 2.3% vs 0.2% (P=.01)** | JAMA 2009 |
| Avasimibe | Did not improve atherosclerosis; **raised LDL 8–11%** | A-PLUS / AHA |
| Nevanimibe | Phase 2 — but **for adrenal disease, not FH** | JCEM 2020 |
| Differentiation bar | A new SOAT1 program for FH must overcome a **Phase-3 failure with a harm signal in the exact FH population.** Effectively unmeetable. | — |

Precedent scores *some* points (drug reached patients), but it is **negative precedent** for this indication.

---

## Validation Evidence → **6 / 10**

| Sub | Score | Value |
|---|---|---|
| Functional (5) | 4 | Deep: global + myeloid-specific KO, H295R apoptosis, dog adrenal studies. |
| Disease models (5) | 2 | In FH-like models (LDLR⁻/⁻, apoE⁻/⁻), ACAT1 KO **did not prevent atherosclerosis** and caused xanthomas — models argue *against* FH benefit. |

---

## Composite & Verdict

| Gate | Score |
|---|---|
| Disease association | 8 / 30 |
| Druggability | 22 / 25 |
| Safety | 8 / 20 |
| Clinical precedent | 5 / 15 |
| Validation evidence | 6 / 10 |
| **Composite** | **49 / 100** |

**Numeric tier:** Tier 3 (CAUTION, 40–59).

### GO / NO-GO: **NO-GO for familial hypercholesterolemia.**

The composite lands in "CAUTION," but the skill's own gate logic overrides the number:
**Gate 1 genetic association to FH fails** (SOAT1 is not an FH gene), and **Gate 4 shows a
failed Phase 3 that caused excess cardiovascular events in FH patients specifically.** A
highly druggable enzyme (Gate 2 = 22/25) does not rescue a target that is mechanistically
downstream of the FH defect and clinically de-risked *against* the indication.

**Pivot (documented, not hidden):** SOAT1 is a *validated* target — just not here. Its
adrenal-restricted expression and on-target adrenal-insufficiency effect make it a rational
**adrenal** target (nevanimibe: Cushing's, CAH, adrenocortical carcinoma). The same biology
that kills it for FH is its value elsewhere.

---

## Confidence flags

- Gates 2 & 4 are well-grounded (structures, PDB IDs, trial numbers verified against primary literature).
- Gate 1's *negative* is robust (multiple independent FH gene panels agree).
- Gate 3's KO/expression direction is solid, but gnomAD constraint, GTEx TPM, and the
  skill-mandated ML predictions (ADMET-AI / DoGSite / AlphaFold) could **not** be produced
  without a data server. Re-add one and the gates can be rerun with authoritative,
  tool-cited quantitative values.

---

## Sources

- [FH genes – Endotext](https://www.ncbi.nlm.nih.gov/books/NBK343488/)
- [FH – GeneReviews](https://www.ncbi.nlm.nih.gov/books/NBK174884/)
- [FH – MedlinePlus](https://medlineplus.gov/genetics/condition/familial-hypercholesterolemia/)
- [ACTIVATE – NEJM](https://www.nejm.org/doi/full/10.1056/NEJMoa054699)
- [CAPTIVATE – JAMA](https://jamanetwork.com/journals/jama/fullarticle/183579)
- [Avasimibe – Circulation](https://www.ahajournals.org/doi/10.1161/01.cir.0000147777.12010.ef)
- [hSOAT1 cryo-EM – Nat Commun](https://www.nature.com/articles/s41467-020-16288-4)
- [PDB 6L47](https://www.rcsb.org/structure/6L47)
- [Nevanimibe Ph1 – PubMed](https://pubmed.ncbi.nlm.nih.gov/31984451/)
- [Nevanimibe Ph2 CAH – JCEM](https://academic.oup.com/jcem/article/105/8/2771/5863384)
- [ATR-101 adrenal – Endocrinology](https://academic.oup.com/endo/article/157/5/1775/2422548)
- [ACAT1 KO xanthomatosis – JCI](https://www.jci.org/articles/view/9021)
- [Myeloid Acat1 KO – PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6816086/)
- [SOAT1 – Human Protein Atlas](https://www.proteinatlas.org/ENSG00000057252-SOAT1/tissue)
