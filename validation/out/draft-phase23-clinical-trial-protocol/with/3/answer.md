The file write wasn't permitted, so here's the complete draft directly.

# AD-101: Phase 2 Study — Draft Protocol Synopsis (v0.1)
**Indication:** Moderate-to-severe atopic dermatitis (AD) | **Mechanism:** Oral small-molecule IL-13 pathway suppressor | **Stage:** Post–Phase 1b

## 0. Assumptions (revisit before finalizing)
| # | Assumption | Why |
|---|---|---|
| A1 | Oral compound targeting IL-4Rα/IL-13/STAT6 axis, not a mAb | matches "small-molecule ... IL-13 suppression" |
| A2 | Phase 1b enrolled AD patients and showed dose-dependent suppression of a Th2 biomarker (e.g., TARC/CCL17) | matches your stated biomarker result |
| A3 | No off-target JAK/kinase activity requiring class boxed-warning language | **unverified — confirm via selectivity panel** |
| A4 | Population: adults 18–75, EASI ≥16, IGA ≥3, BSA ≥10%, inadequate response to topical therapy | standard FDA AD registration population |
| A5 | Primary endpoint: % change from baseline in EASI at Week 16 | matches your "30% improvement over placebo" framing |
| A6 | SD of % change in EASI ≈ 40 points | drawn from published AD trial variability; replace with your own Phase 1b data ASAP |

## 1. FDA Regulatory Pathway
**Pathway:** Standard **505(b)(1) NDA** (novel entity — 505(b)(2) doesn't apply). **Division:** Dermatology and Dentistry (DDDP), CDER.

**Controlling guidance:** FDA's 2016 draft guidance *"Atopic Dermatitis: Developing Drugs for Treatment"* — recommends EASI-75 and/or IGA 0/1 (≥2-point improvement) as primary measures, a validated pruritus PRO as co-primary/key secondary, and a 12–16 week placebo-controlled primary window.

**Milestones to sequence:**
1. **End-of-Phase 1 (Type B) meeting** — align on dose selection, biomarker qualification status (TARC/CCL17 is supportive, not a validated surrogate — clinical endpoints will still be primary), and overall plan.
2. **QTc strategy** — a concentration-QTc analysis nested in Phase 1 data (ICH E14) rather than a standalone TQT study, agreed with FDA pre-Phase 2.
3. **Initial Pediatric Study Plan (iPSP)** — required under PREA within 60 days of the EOP2 meeting; every recent AD competitor now has pediatric labeling, so plan early.
4. **Expedited designations** — Fast Track is plausible if you can name an unmet-need subpopulation (biologic/JAK-inadequate responders, or a genuine non-JAK oral safety edge); Breakthrough Therapy is a harder case in a now-crowded field absent a clearly superior effect size.
5. **REMS/boxed-warning risk** — if selectivity data show any JAK-adjacent activity, expect FDA to apply the 2021 JAK-class safety framework (MACE/malignancy/VTE/infection/mortality warnings) even to a non-JAK molecule. Run the selectivity panel before EOP1.
6. **SPA** — consider requesting for the Phase 3 pivotal design once Phase 2 locks dose/endpoints, not for Phase 2 itself.

## 2. Competitive Landscape & Prior Trial Benchmarks
**Approved competitors (~mid-2026), pivotal EASI-75 drug vs. placebo at ~Wk16:**
- Dupilumab (Dupixent, anti-IL-4Rα mAb, 2017): ~44–51% vs ~12–15%
- Tralokinumab (Adbry, anti-IL-13 mAb, 2021): ~25–33% vs ~10–12%
- Lebrikizumab (Ebglyss, anti-IL-13 mAb, 2023): ~38–43% vs ~12–16%
- Nemolizumab (Nemluvio, anti-IL-31RA, 2024): pruritus-focused, adjunct-to-TCS
- Upadacitinib (Rinvoq, oral JAK1, 2022): ~70–80% vs ~13–16%
- Abrocitinib (Cibinqo, oral JAK1, 2022): ~60–70% vs ~10–14%
- Topical: ruxolitinib (Opzelura), roflumilast (Zoryve), tapinarof (Vtama) — mild-moderate populations, not direct comparators for your severe population.

**Pipeline:** rocatinlimab (anti-OX40, Amgen/Kyowa Kirin) and amlitelimab (anti-OX40L, Sanofi) in Phase 3; rademikibart/CBP-201 (anti-IL-4Rα mAb) in Phase 3; several **oral STAT6/IL-13-pathway small molecules** are in preclinical/Phase 1 industry-wide but none has reported Phase 2 AD data — AD-101 could plausibly be **first-to-readout in an oral non-JAK IL-13-pathway class**, a real differentiation story if A3 holds.

**Design lessons:** recent Phase 2b AD trials use 3–5 dose arms + placebo, N≈60–100/arm, 16-week primary endpoint, and a biomarker sub-study. Placebo EASI-75 response has drifted up (10→16%) as background rescue-therapy allowances have loosened — build a conservative placebo assumption in. Every recent competitor included a pruritus PRO as co-primary/key secondary — omitting one would draw an FDA information request.

## 3. Sample Size Justification
**Comparison:** highest active dose vs. placebo, continuous endpoint (% change EASI at Wk16), Δ=30 points, σ=40 points (per A6).

n/arm = 2 × (z₁₋α/2 + z₁₋β)² × σ² / Δ²

| Power | n/arm (raw) |
|---|---|
| 80% | 28 |
| 90% | 38 |

**Adjustments:**
- Dropout inflation (15–20% typical over 16 weeks): → **34–35/arm (80% power)** or **47–48/arm (90% power)**.
- Multiplicity (3 active doses vs. placebo): pre-specify high-dose-vs-placebo as the sole primary comparison (avoids a full Dunnett penalty on power); treat other doses as secondary dose-response (Emax/MCP-Mod).
- **Recommended: N ≈ 50/arm (90% power, dropout-adjusted) × 4 arms = ~200 total randomized.**

**Cross-check with binary EASI-75** (45% active vs. 15% placebo responders, consistent with mid-tier competitors): two-proportion test at 90% power gives n≈55/arm before dropout — consistent with the continuous-endpoint estimate, so **N≈200–220 is robust regardless of which endpoint ends up primary.**

## 4. Study Design & Procedures Outline
**Design:** Randomized, double-blind, placebo-controlled, parallel-group, dose-ranging Phase 2b. **Arms (1:1:1:1):** placebo, low/mid/high AD-101 dose (from Phase 1b PK/PD, covering biomarker EC50–EC90). **Duration:** 4-wk screening → 16-wk double-blind treatment → 4-wk safety follow-up (optional 8-wk OLE for durability).

**Eligibility (illustrative):** age 18–75, chronic AD ≥1 yr, EASI ≥16, IGA ≥3, BSA ≥10%, inadequate response/intolerance to topical steroids/TCIs; exclude active skin infection, significant hepatic/renal impairment, QTc >450/470ms, malignancy history; stratify (don't necessarily exclude) prior biologic/JAK-experienced patients.

**Endpoints:**
- Primary: % change from baseline EASI at Wk16.
- Key secondary: EASI-75; IGA 0/1 (≥2-pt improvement); Peak Pruritus NRS (≥4-pt improvement); EASI-50/90; SCORAD; DLQI.
- PD/exploratory: serum TARC/CCL17, total IgE, periostin (longitudinal, confirms target engagement).
- Safety: AEs/SAEs, CBC/CMP/LFTs/lipids, vitals, ECG/QTc, PK for population PK/exposure-response modeling.

**Visits:** Screening (Day −28 to −1) → Baseline → Wk 1, 2, 4, 6, 8, 12, 16 → Wk20 safety follow-up; daily patient pruritus diary throughout.

**Analysis:** ITT, MMRM for continuous endpoints, logistic regression for responders, adjusted for stratification factors; dose-response modeled via Emax/MCP-Mod to inform Phase 3 dose; independent DSMB with one blinded interim safety review (~50% enrollment).

## 5. Immediate Next Steps
1. Replace σ=40 assumption with your actual Phase 1b variance once unblinded — rerun the power calc.
2. Run a kinase/receptor selectivity panel before EOP1 — resolves both regulatory risk (§1) and competitive positioning (§2).
3. Draft the EOP1 briefing package (Phase 1b summary + proposed design/endpoints).
4. Sanity-check the placebo-response assumption against your target sites' historical AD trial performance.

**What I'd most want you to challenge:** the σ=40 and Δ=30 assumptions drive the entire sample size — everything else here is defensible from public precedent, but those two numbers are placeholders until your Phase 1b data replaces them.