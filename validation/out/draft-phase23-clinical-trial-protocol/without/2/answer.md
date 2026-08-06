Since I couldn't get file-write permission, here's the full first-draft plan below. A few inputs weren't in your prompt (exact Phase 1b doses/numbers, formulation, etc.) — I made concrete, stated assumptions rather than leaving placeholders, flagged in §0 so you can swap in real data fast.

---

# Phase 2 Study Plan — Oral Small-Molecule IL-13 Pathway Inhibitor in Moderate-to-Severe Atopic Dermatitis
**Status:** First draft for internal discussion — not a protocol, not for submission | **v0.1** | 2026-07-30

## 0. Assumptions made to complete this draft

| Item | Assumption made | Basis |
|---|---|---|
| Modality | Oral, once-daily, small-molecule inhibitor upstream of IL-13 signaling (e.g., STAT6 or IL-13/IL-4Rα intracellular signaling) | You said "small-molecule," "IL-13 pathway suppression"; oral QD is the modal design for this class today |
| Phase 1b design | Randomized, double-blind, placebo-controlled MAD study, ~40–60 adults with moderate-to-severe AD, 3 dose levels (e.g., 25/75/200 mg QD) vs. placebo, 4–6 weeks | Typical Ph1b design for this indication/class |
| Phase 1b safety result | No SAEs/DLTs; AE profile balanced with placebo; no clinically meaningful lab/ECG/vitals signal | You said "promising safety" |
| Phase 1b biomarker result | Dose-dependent ~50–70% suppression of serum IL-13 pathway biomarkers (e.g., TARC/CCL17, periostin) at top dose vs. placebo | You said "biomarker data showing IL-13 pathway suppression" |
| Target population | Adults ≥18, moderate-to-severe AD, inadequate response/intolerance to topicals | Standard entry population for this class before pediatric expansion |
| Sample-size target | "30% improvement in EASI over placebo" = a **30-percentage-point placebo-adjusted difference in percent change in EASI from baseline to Week 16** | Standard operationalization of this phrase in AD trials; alternate reading (EASI-75 responder-rate difference) given in §4.4 |

## 1. Regulatory pathway

**Classification.** Small molecule → regulated as a drug, not a biologic: **21 CFR Part 312 (IND)** → **505(b)(1) NDA**, reviewed by CDER (Office of Immunology and Inflammation). This is a different pathway than the anti-IL-13/IL-4Rα biologics (dupilumab, tralokinumab, lebrikizumab), which are BLAs under PHS Act §351(a) — worth stating explicitly to avoid conflating "same target" with "same pathway" in board/investor materials.

**Existing IND.** Phase 2 runs under the Phase 1b IND — file a protocol amendment and updated Investigator's Brochure incorporating the Ph1b safety/PD data; no new IND needed.

**Relevant guidance:**
- FDA's atopic dermatitis drug-development guidance (endpoint selection — EASI, IGA, itch NRS — trial population, duration); check the current version on FDA's guidance database, as disease-specific AD guidance has been actively revised recently.
- **Atopic Dermatitis: Timing of Pediatric Studies During Development of Systemic Drugs** (final, Oct 2018) — governs your PREA obligations. AD is not a rare disease, so don't expect a pediatric waiver; an initial Pediatric Study Plan (iPSP) is due ≤60 days after the End-of-Phase-2 meeting — plan for it now.
- ICH E6(R3) GCP and ICH E9(R1) estimands — increasingly scrutinized in FDA statistical review of AD trials (rescue-therapy/discontinuation handling, see §5.4).

**Meetings/expedited programs.** Request an **End-of-Phase 2 meeting** after topline Phase 2 data to align on the Phase 3 program, and consider a **Special Protocol Assessment** for the pivotal design. Apply for **Fast Track designation** once you have Phase 2 proof-of-concept data (precedent: rezpegaldesleukin got Fast Track in this same indication, Feb 2025). Breakthrough Therapy is a stretch this early without a standout signal.

**Safety posture to plan for.** Upadacitinib and abrocitinib (oral JAK inhibitors, same indication) carry an FDA **boxed warning** (serious infection, mortality, malignancy, MACE, thrombosis) driven by class-level JAK safety findings; IL-13-selective biologics carry no such warning. Your mechanism is distinct from JAK, but FDA's posture toward oral immunomodulators in AD has gotten more conservative — budget for **enhanced cardiovascular/malignancy/infection adjudication in Phase 2** even though your target differs. A clean safety record on this specific axis is now close to table stakes, not just good practice, and is central to your "oral without the boxed warning" differentiation claim.

**If global:** initiate EMA Scientific Advice and a Paediatric Investigation Plan (PIP) in parallel to avoid late redesign.

## 2. Competitive landscape

**Approved/late-stage systemic therapies (the bar you're measured against):**

| Agent | Class | Mechanism | Efficacy signal | Safety/label note |
|---|---|---|---|---|
| Dupilumab (Dupixent) | Biologic, SC q2w | IL-4Rα antagonist (blocks IL-4 + IL-13) | Strong, consistent EASI-75 superiority vs. placebo across SOLO 1/2 | No boxed warning; conjunctivitis notable; injection burden |
| Tralokinumab (Adbry) | Biologic, SC | Selective IL-13 antagonist | EASI-75 ~70% range at Wk32 w/ TCS, comparable to dupilumab in matched analyses | Favorable safety; modest conjunctivitis |
| Lebrikizumab (Ebglyss) | Biologic, SC | Selective, high-affinity IL-13 antagonist | 52.1% EASI-75 vs. 18.1% placebo at Wk16 (~34-pt gap); pediatric label now | Comparable safety; indirect comparisons suggest dupilumab slightly deeper/faster response |
| Upadacitinib (Rinvoq) | Oral JAK1 inhibitor | Broad cytokine blockade | Among highest EASI-75/90 in class | **Boxed warning** (infection, mortality, malignancy, MACE, thrombosis); lab monitoring required |
| Abrocitinib (Cibinqo) | Oral JAK1 inhibitor | Same class concern | Strong EASI-75, oral | Same boxed warning |

**Strategic read:** your asset sits between these clusters — oral convenience without the JAK boxed warning, *if* the safety story holds at scale. Your Phase 2 safety database needs to earn that claim with numbers, not narrative.

**Direct pipeline competitors (same "oral, upstream-of-IL-13" strategy):**
- **KT-621 (Kymera)** — oral STAT6 degrader (STAT6 is the shared node downstream of both IL-4 and IL-13 receptors). Positive Ph1b reported Dec 2025 (>90% STAT6 degradation in blood >1.5mg, full degradation in blood+skin >50mg); Phase 2b planned for AD and asthma.
- **REX-8756** — oral, reversible, selective STAT6 inhibitor (SH2 domain), earlier stage.
- **ENV-294 (Enveda)** — oral small molecule with a broader "reset inflammatory signaling" narrative vs. single-cytokine blockade; positive Ph1b in moderate-to-severe AD (~March 2025).

Several competitors are converging on **STAT6** (the IL-4/IL-13 convergence point) rather than IL-13 alone. Be precise in your own materials about whether your mechanism is IL-13-selective (tralokinumab/lebrikizumab-like ceiling) or broader IL-4+IL-13 (dupilumab-like ceiling) — indirect comparisons suggest IL-13-selective biologics track slightly behind dupilumab on response depth.

**Cautionary precedent:** SCD-044 (vibozilimod), an oral S1PR1 agonist, had acceptable Phase 1 safety but **failed** Phase 2 AD and psoriasis efficacy (missed PASI-75/EASI-75), and was discontinued (June 2025). Clean Ph1b safety doesn't guarantee the pharmacology translates into a competitive EASI effect — which is why §4 powers to a clinically competitive effect size, not just "any" effect.

**Track but not core competitors:** OX40/OX40L antagonists (rocatinlimab, amlitelimab — T-cell costimulation, possible disease-modifying claims), rezpegaldesleukin (IL-2/Treg, Fast Track Feb 2025), TSLP-targeted agents.

## 3. Trial design overview

- **Design:** Multicenter, randomized, double-blind, placebo-controlled, parallel-group, dose-ranging Phase 2b, with optional open-label extension.
- **Population:** Adults 18–75, chronic AD ≥1 year, EASI ≥16, vIGA-AD ≥3, BSA ≥10%, documented inadequate response/intolerance to topicals ≥4 weeks. Exclude recent JAK/biologic use, significant infection/malignancy history, cardiac risk flags from Ph1b.
- **Arms:** Placebo / low-mid dose / high dose, drawn from actual Ph1b PK-PD (lowest dose with near-maximal biomarker suppression; top tolerated dose or one step below for margin).
- **Duration:** 16-week double-blind induction (field-standard primary timepoint across dupilumab/tralokinumab/lebrikizumab pivotal trials), optional 36-week extension for durability/long-term safety ahead of Phase 3.
- **Background therapy:** Permit standardized low-potency topical corticosteroid as rescue/background (mirrors modern AD trial designs; improves ethics/retention without confounding if captured as a sensitivity analysis).

## 4. Sample-size calculation

**4.1 Endpoint/effect:** Primary = percent change in EASI from baseline to Week 16. Target = 30-percentage-point placebo-adjusted difference (e.g., placebo ≈ −25%, active ≈ −55%, consistent with magnitudes in published Ph2b AD programs).

**4.2 Assumptions:**

| Parameter | Value | Justification |
|---|---|---|
| Effect size (Δ) | 30 points | Stated target |
| Common SD | 40 points | Consistent with published variance (~35–45) for this endpoint in Ph2b AD trials |
| α | Two-sided 0.05 overall → **0.025 per comparison** (Bonferroni) | Two active-dose arms vs. shared placebo |
| Power | 90% | Phase 2 false-negative is costly enough to justify 90% over 80% |
| Dropout | 15% over 16 weeks | Typical for 16-week AD induction trials |

**4.3 Calculation** (two independent means): n = 2σ²(z_α/2 + z_β)² / Δ², with σ=40, Δ=30, z_α/2=2.24 (α=0.025 two-sided), z_β=1.28 (90% power):

n = 2×1600×(2.24+1.28)²/900 = 2×1600×12.4/900 ≈ **44.1 → 45 evaluable per arm**

Dropout-inflated: 45/0.85 ≈ 53 → **55 enrolled per arm**

**4.4 Total:**

| Arm | Evaluable | Enroll (15% dropout) |
|---|---|---|
| Placebo | 45 | 55 |
| Low/mid dose | 45 | 55 |
| High dose | 45 | 55 |
| **Total** | **135** | **~165** |

This matches the order of magnitude of comparable published Ph2b AD programs (tralokinumab ~204 across 5 arms; lebrikizumab ~280 across 4 arms) — a reasonable external sanity check.

*If "30% improvement" instead means a 30-point difference in **EASI-75 responder rate*** (e.g., 20% placebo vs. 50% active), the two-proportion calculation under the same α/power gives **~40 evaluable/arm** — similar order of magnitude either way, but confirm which framing you mean before it goes into a SAP.

**4.5 Have your biostatistician also check:** σ=45–50 as a conservative bound (~55–60/arm); a Dunnett-adjusted (vs. Bonferroni) critical value, which typically recovers 5–8% sample size; and MMRM vs. ANCOVA/LOCF for the primary analysis (MMRM is now field-standard and slightly more efficient).

## 5. Study procedures and design outline

**Visit schedule (16-week induction):** Screening (D−35 to −1: consent, eligibility, labs incl. CBC/CMP/LFT/lipids, TB/hep B/C screen, pregnancy, ECG, baseline photos) → Baseline/Randomization D1 (full efficacy battery, PK pre-dose, biomarker draw, first dose) → Wk2 safety check → Wk4/Wk8/Wk12 full efficacy + safety labs + biomarker draw (Wk8 also a candidate DSMB interim-review cutpoint) → **Wk16 primary endpoint** (full efficacy, safety labs, PK, biomarker, extension decision) → Follow-up safety visit 4–8 weeks post-last-dose.

**Efficacy endpoints:** Primary — % change in EASI (baseline→Wk16). Key secondary — EASI-75 responder rate; vIGA-AD 0/1 with ≥2-grade improvement; Peak Pruritus NRS weekly responder rates; DLQI/POEM change; EASI time-course (Wk2/4/8/12) for onset-of-action positioning vs. competitors. Exploratory — SCORAD, sleep-loss subscore, biomarker-response correlation (does Wk4 biomarker suppression predict Wk16 EASI response — directly useful for Phase 3 dose justification).

**Safety endpoints:** TEAEs/SAEs; AEs of special interest (infection, malignancy, MACE, thrombosis, conjunctivitis) independently adjudicated; CBC/CMP/LFT/lipid/CPK labs; ECG at baseline/Wk8/Wk16; independent DSMB with a prespecified interim safety review.

**Statistical/estimand plan:** Prespecify an ICH E9(R1) estimand framework (treatment-policy primary, hypothetical/on-treatment sensitivity) for handling rescue therapy and discontinuation — increasingly scrutinized by FDA statistical reviewers and far cheaper to define correctly now than retrofit in Phase 3. Primary analysis via MMRM or ANCOVA with baseline severity and site/region covariates; hierarchical/Dunnett-based multiplicity control across dose arms and key secondaries.

**PK/PD/translational plan:** Sparse PK at each visit to build a population PK model bridging Ph1b→Ph2 exposure; longitudinal biomarker suppression (TARC/CCL17, periostin) to build an exposure-response model for **Phase 3 dose justification** — this is the highest-leverage dataset the trial can produce for de-risking Phase 3, so don't under-resource biomarker logistics relative to clinical endpoints.

**Open items to resolve before this becomes an actual protocol:**
1. Replace §0 assumptions with real Phase 1b dose-response/safety data — changes arms, sample size, and safety-monitoring plan.
2. Decide adolescent (12–17) inclusion now vs. deferred — affects PREA/iPSP timing.
3. Decide whether background topical corticosteroid use is permitted/mandated/prohibited — materially shifts assumed placebo response and thus §4's sample size.
4. Schedule FDA Type B/C correspondence to pressure-test endpoint/population choices before finalizing the protocol.

---

Sources for the competitive/regulatory landscape above:
- [Two Phase 3 Trials of Lebrikizumab for Moderate-to-Severe Atopic Dermatitis (NEJM)](https://www.nejm.org/doi/full/10.1056/NEJMoa2206714)
- [Two Phase 3 Trials of Dupilumab versus Placebo in Atopic Dermatitis (NEJM)](https://www.nejm.org/doi/full/10.1056/NEJMoa1610020)
- [Matching-Adjusted Indirect Comparison of Tralokinumab and Dupilumab (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11052979/)
- [FDA Approvals of Upadacitinib, Abrocitinib — Boxed Warnings (Pharmacy Times)](https://www.pharmacytimes.com/view/fda-approvals-of-upadacitinib-abrocitinib-for-refractory-atopic-dermatitis-come-with-boxed-warnings-restrictive-labelling)
- [What new atopic dermatitis treatments are in the pipeline in 2026? (Labiotech)](https://www.labiotech.eu/in-depth/new-atopic-dermatitis-treatments/)
- [Data from Phase 2b REZOLVE-AD Study (Nektar Therapeutics)](https://ir.nektar.com/news-releases/news-release-details/data-phase-2b-rezolve-ad-and-rezolve-aa-studies)
- [Atopic Dermatitis: Timing of Pediatric Studies During Development of Systemic Drugs (FDA)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/atopic-dermatitis-timing-pediatric-studies-during-development-systemic-drugs)

**Note:** I attempted to save this as a file in your working directory but the write permission wasn't granted — let me know if you'd like me to retry, or if this chat response is sufficient as your working draft.