Below is a first-draft Phase 2 plan. Since you didn't specify drug identity, mechanism detail, or population parameters, I made concrete assumptions (flagged in **bold** where they matter) so the plan is usable rather than generic — swap in real numbers once you have them.

## 0. Working assumptions (stated so you can override them)

- **Compound**: oral small-molecule inhibitor acting on IL-4Rα/IL-13/STAT6 signaling (e.g., a STAT6 or IL-13-signaling small molecule — not a biologic), once- or twice-daily oral dosing.
- **Phase 1b**: single/multiple ascending dose in healthy volunteers or mild AD patients, showing dose-dependent suppression of a pathway biomarker (e.g., TARC/CCL17, periostin, or serum IL-13 downstream signature) with an acceptable safety/tolerability profile through the highest tested dose.
- **Population**: adults with moderate-to-severe AD (EASI ≥16, IGA ≥3, BSA ≥10%), inadequate response/intolerance to topical therapy — the standard entry criteria used across the approved-drug class.
- **IND is already open** (required to have dosed Phase 1b); this Phase 2 is the next protocol under that IND, not a new pathway.
- Primary efficacy readout: **percent change from baseline in EASI at Week 16**, "30% improvement over placebo" interpreted as a **30-percentage-point** greater mean reduction in %EASI vs. placebo (this is the standard way this figure is used in AD trial planning — flag if you meant a *relative* 30% or EASI-75 responder-rate difference instead, since the required N differs).

---

## 1. Regulatory pathway

**Pathway**: Standard **505(b)(1) NDA** via full IND development — this is a new molecular entity, not a candidate for 505(b)(2). No orphan pathway applies (AD prevalence is too high).

**Relevant FDA guidance**:
- *Atopic Dermatitis: Developing Drugs for Treatment* (FDA guidance for industry, adult and adolescent) — governs entry criteria, endpoint selection (EASI, IGA, BSA, pruritus NRS), and trial duration expectations.
- *Atopic Dermatitis: Developing Drugs for Treatment in Children (≥3 months–<18 years)* — not immediately applicable to this adult Phase 2b, but per **PREA**, a pediatric study plan (PSP) must be agreed with FDA before NDA submission; note this now so it's on the roadmap, not a Phase 3 surprise.
- ICH E9 / E9(R1) (estimands), ICH E6(R2)/(R3) (GCP), ICH E17 if multi-regional.

**Milestones to sequence around this protocol**:
1. **End-of-Phase-1 (EOP1) meeting** with the Division of Dermatology and Dentistry — present Phase 1b safety/PK/biomarker data, get written agreement on the Phase 2 dose range, primary endpoint, and biomarker strategy before finalizing the protocol. This is the single highest-leverage regulatory step at your current stage.
2. Consider requesting **Fast Track designation** if the Phase 1b biomarker data plus unmet-need argument (oral, non-immunosuppressive alternative to injectables/JAKi) support it — enables rolling review later and more frequent FDA interaction.
3. Given the crowded field, **novel oral mechanism + differentiated safety** (vs. JAK inhibitors' boxed warning) is your strongest differentiation argument to FDA and payors — make sure Phase 2 safety monitoring (labs, no unexpected JAK-class signals like VTE/MACE/malignancy flags) is designed to generate that data even though it's underpowered for those endpoints at this stage.
4. Standard requirement to run **two adequate, well-controlled Phase 3 trials** post-Phase 2 — so this Phase 2b should be explicitly designed as **dose-selection for Phase 3**, not just proof-of-concept.

---

## 2. Competitive landscape and prior trials

| Drug | Class | Status | Placebo-adjusted efficacy (16 wk, key trial) |
|---|---|---|---|
| Dupilumab (Dupixent) | IL-4Rα mAb, SC | Approved 2017 | EASI-75 ~44–51% vs ~12% placebo (SOLO 1/2) |
| Tralokinumab (Adbry/Adtralza) | IL-13 mAb, SC | Approved 2021 | EASI-75 ~25–33% vs ~11% placebo (ECZTRA 1/2) |
| Lebrikizumab (Ebglyss) | IL-13 mAb, SC | Approved 2024 | EASI-75 ~58–62% vs ~16–17% placebo (ADvocate 1/2, ADhere) |
| Upadacitinib (Rinvoq) | Oral JAK1i | Approved 2022 | EASI-75 ~65–80% vs ~13–17% placebo — highest efficacy in class, boxed warning (VTE/MACE/malignancy/mortality) |
| Abrocitinib (Cibinqo) | Oral JAK1i | Approved 2022 | EASI-75 ~58–70% vs ~12–14% placebo — same boxed warning class |
| Nemolizumab (Nemluvio) | IL-31RA mAb, SC | Approved Dec 2024 | Pruritus-focused; EASI improvement secondary |
| Ruxolitinib cream (Opzelura) | Topical JAK | Approved (topical only) | Mild-moderate disease only |
| Tapinarof, Roflumilast | Topical AhR agonist / PDE4i | Approved 2024 | Mild-moderate; not relevant comparator for systemic moderate-severe |
| Rocatinlimab, amlitelimab | Anti-OX40/OX40L, SC | Phase 3 | Emerging, durability-of-response angle |

**Positioning implication**: You are entering a field where injectable biologics (tralokinumab, lebrikizumab) have already validated the IL-13 axis at the efficacy level you're targeting, and oral JAK inhibitors have set a higher efficacy bar but carry a boxed warning. Your compound's commercial and regulatory argument is almost certainly **"biologic-level efficacy without JAK-class systemic risk, in a convenient oral formulation."** That argument should shape:
- The **safety monitoring plan** (this Phase 2 should already collect the labs FDA will ask about later: lipids, CPK, hepatic panel, lymphocyte subsets, herpes zoster surveillance, thrombotic risk factors) even though it won't have the exposure to rule these out.
- The **dose range**: since you have real biologic and JAKi comparators, use their placebo-adjusted EASI-75 rates (roughly 25–60 percentage points) to sanity-check whether your 30-point assumption is competitive or conservative — 30 points would place you between tralokinumab and lebrikizumab, i.e., a credible but not best-in-class assumption worth stress-testing against your actual Phase 1b biomarker magnitude.

---

## 3. Sample size calculation

**Design choice**: multi-arm, randomized, double-blind, placebo-controlled, parallel-group dose-ranging study. Primary comparison for sizing purposes: highest (or presumed most efficacious) dose vs. placebo.

**Primary endpoint**: Percent change from baseline in EASI at Week 16, analyzed by ANCOVA/MMRM (baseline EASI as covariate).

**Assumptions** (state your sources when you refine this — these are typical values drawn from the class above, not your compound's actual variance):
- Effect size (Δ): **30 percentage points** greater mean %EASI reduction vs. placebo (e.g., placebo ≈ −25%, active ≈ −55%) — consistent with your prompt.
- Common SD: **35 percentage points**, based on the variability typically reported for %EASI change in Phase 2/3 AD trials of this class.
- Two-sided α = 0.05, target power = 90% (justified because this is a dose-selection trial feeding a large Phase 3 investment — underpowering here risks carrying a wrong dose forward).
- Anticipated dropout/non-evaluability: 15%.

**Formula** (two-sample continuous comparison):

n per arm = 2 × σ² × (z_{α/2} + z_β)² / Δ²

With z_{0.025} = 1.96, z_{0.10} = 1.2816, σ = 35, Δ = 30:

n = 2 × 1225 × 10.51 / 900 ≈ **28.6 → 29 evaluable patients/arm**

**Dropout-adjusted**: 29 / (1 − 0.15) ≈ **34 → round to 35/arm**

**Multiplicity note**: with 3 active dose arms vs. 1 placebo, a Dunnett-adjusted many-to-one comparison is the appropriate primary analysis to preserve family-wise α = 0.05 across the 3 comparisons (rather than 3 separate unadjusted t-tests). This slightly raises the effective critical value versus the simple two-sample calc above; a practical, commonly used buffer is **+10–15% sample size** to maintain power under Dunnett adjustment.

35 × 1.15 ≈ **40 evaluable/arm → ~45/arm enrolled (accounting for screen failures/dropout margin)**

**Recommended total N**: 4 arms (placebo + 3 active doses) × 45 = **~180 randomized patients** (range 160–220 depending on final dose-arm count). This is in line with actual precedent Phase 2b AD dose-ranging trials (dupilumab Ph2b ~380 across 5 arms ≈ 75/arm; tralokinumab Ph2b ~204 across 5 arms ≈ 40/arm; lebrikizumab TREBLE ~209), so 40–45/arm is a defensible, precedented target — not an outlier in either direction.

**Sensitivity check** (do this once you have real Phase 1b variance data): if true SD is 40 instead of 35, required n/arm rises to ~46 (pre-dropout) → ~60/arm enrolled. Since your Δ assumption of 30 points is a placeholder, I'd recommend re-running this with your actual Phase 1b biomarker/pilot EASI variance before locking the protocol — the sample size is far more sensitive to σ than to modest changes in the effect-size assumption.

---

## 4. Study design outline

**Title (working)**: A Phase 2b, Randomized, Double-Blind, Placebo-Controlled, Dose-Ranging Study to Evaluate the Efficacy, Safety, and Pharmacodynamics of [Compound] in Adults with Moderate-to-Severe Atopic Dermatitis

**Objectives**:
- Primary: dose-response on %EASI change from baseline at Week 16 vs. placebo.
- Secondary: EASI-75/EASI-90, IGA 0/1 with ≥2-point improvement, BSA, Pruritus NRS (weekly), DLQI/POEM (patient-reported), time-course of response.
- Exploratory/PD: correlation of clinical response with pathway biomarkers (TARC/CCL17, periostin, serum IL-13/IL-4, Th2 gene signature) to confirm target engagement tracks with efficacy — directly extends your Phase 1b biomarker finding.
- Safety: AEs/SAEs, labs (hepatic, lipid, CPK, hematology incl. lymphocyte subsets), infections (esp. herpes zoster, skin infections), thrombotic risk labs if mechanistically plausible, vital signs, ECG if indicated by Phase 1b QT signal (or lack thereof).

**Design**: Randomized 1:1:1:1 (placebo : low : mid : high dose), double-blind, double-dummy if formulations differ, stratified by baseline disease severity (EASI 16–<32 vs. ≥32) and possibly by baseline biomarker level (e.g., high vs. low TARC) to test whether the biomarker predicts response — an efficient way to build your future companion-diagnostic/enrichment story into Phase 3.

**Duration**: 2–4 week screening → **16-week double-blind treatment period** (aligned with FDA-preferred primary endpoint timing and competitor precedent) → optional 8–12 week extension or follow-up safety period → 4-week safety follow-up post last dose.

**Key inclusion/exclusion** (standard for the class): adults ≥18, chronic AD ≥1 year, EASI ≥16, IGA ≥3, BSA ≥10%, documented inadequate response to topical corticosteroids/calcineurin inhibitors; exclude prior biologic/JAKi use within washout window (or stratify if allowed), active skin infection, other confounding dermatoses, clinically significant hepatic/renal/cardiac/thrombotic history depending on Phase 1b safety signals.

**Concomitant therapy**: low-potency topical corticosteroid rescue permitted per protocol (standard approach — track use as a secondary/composite endpoint to avoid penalizing patients for uncontrolled disease).

**Schedule of assessments (illustrative)**:

| Visit | Screen | BL/D1 | Wk2 | Wk4 | Wk8 | Wk12 | Wk16 (primary) | Wk20 (FU) |
|---|---|---|---|---|---|---|---|---|
| EASI/IGA/BSA | X | X | X | X | X | X | X | X |
| Pruritus NRS | daily diary throughout | | | | | | | |
| PK sampling | | X | X | X | | X | X | |
| PD biomarkers (TARC, periostin, IL-13 signature) | | X | X | | X | | X | X |
| Safety labs | X | X | | X | X | X | X | X |
| ECG | X | X | | | | | X | |
| AE assessment | | X | X | X | X | X | X | X |

**Statistical analysis plan (summary)**:
- Primary analysis population: ITT (all randomized).
- Primary endpoint: MMRM or ANCOVA on %EASI change, with Dunnett-adjusted pairwise dose-vs-placebo comparisons; multiple imputation or a control-based imputation approach for missing-not-at-random dropout (esp. dropouts due to lack of efficacy, per current FDA estimand expectations — worth confirming your target estimand strategy at the EOP1 meeting).
- Secondary endpoints: hierarchical or Hochberg-adjusted testing to control Type I error across the responder-rate endpoints.
- Interim analysis: consider a single unblinded interim (e.g., at 50% enrollment) for futility only, reviewed by an independent DSMB, given this is a dose-finding — not registrational — study.

**Safety monitoring**: independent DSMB given the multi-dose design and novel MOA; pre-specified stopping rules tied to labs/AEs seen (or notably *not* seen) in Phase 1b.

---

## 5. Open items to resolve before finalizing

1. Confirm actual Phase 1b PD/EASI variance to replace the placeholder σ=35 in the sample-size calc — this is the single biggest lever on required N.
2. Decide whether "30% improvement" means the 30-point continuous effect used above, or a 30 percentage-point EASI-75 responder-rate difference — the latter requires a different (proportion-based) power calculation and likely a larger N.
3. Lock the dose range and regimen with the EOP1 meeting before writing the final protocol — don't finalize doses independently of FDA input given how much downstream Phase 3 planning depends on it.
4. Decide on the biomarker-enrichment stratification now, since retrofitting it after Phase 2 is far more expensive than building it in.

Sources: [FDA Clinical Guidances](https://www.fda.gov/vaccines-blood-biologics/general-biologics-guidances/clinical-guidances) · [NEJM: Two Phase 3 Trials of Lebrikizumab](https://www.nejm.org/doi/full/10.1056/NEJMoa2206714) · [Tralokinumab ECZTRA 3 post hoc](https://pubmed.ncbi.nlm.nih.gov/35857179/) · [8 Dermatology Drugs FDA Approved in 2025](https://www.medcentral.com/dermatology/8-dermatology-drugs-fda-approved-in-2025)