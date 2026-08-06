# Phase 2 Study Development Plan — Oral IL-13 Pathway Small Molecule for Moderate-to-Severe Atopic Dermatitis

This is a first draft to structure internal discussion and a pre-IND/EOP1 regulatory strategy conversation — not a protocol ready for IRB or FDA submission. Wherever you haven't given me a specific input, I've made an explicit, stated assumption and flagged it so you can swap in your real numbers.

**Stated assumptions** (state these back to me if any are wrong before this goes further):
- **Mechanism**: the compound acts downstream/selectively in the IL-4/IL-13 signaling axis (e.g., analogous to an oral STAT6 degrader or a direct small-molecule IL-13/IL-4Rα pathway antagonist) — **not** a pan-JAK inhibitor. This matters enormously for regulatory strategy (see §1.4) and I flag it as the single highest-leverage assumption in this whole plan.
- Target population: adults (18–75) with moderate-to-severe AD, defined by convention as EASI ≥16, vIGA-AD ≥3, BSA ≥10%, inadequate response to topical therapy.
- Phase 1b: single/multiple ascending dose in patients (not just healthy volunteers), showing acceptable safety/tolerability plus a PD biomarker signal (e.g., serum TARC/CCL17, periostin, or skin transcriptomic Th2 signature suppression) — biomarker suppression, not yet clinical efficacy.
- IND already open (required to have dosed patients in 1b).
- No IL-13 pathway-selective oral small molecule from your company has reached FDA before, so there's no direct internal precedent — I'm anchoring on the closest real-world analog, Kymera's KT-621 (oral STAT6 degrader, IL-4/IL-13 pathway), which just completed an almost identical 1b→2b transition.

---

## 1. FDA Regulatory Pathway

**1.1 Pathway type.** This is a New Molecular Entity NDA under FDCA §505(b)(1), reviewed by the Division of Dermatology (part of OND). There is no orphan pathway available — AD prevalence is far above the <200,000-patient threshold.

**1.2 No AD-specific efficacy guidance exists (unlike psoriasis).** FDA has a finalized guidance on *pediatric study timing* for systemic AD drugs (Docket FDA-2018-D-1175, finalized 2018) but no consolidated adult efficacy-endpoint guidance. In practice, primary endpoints have been standardized by precedent across the last decade of approvals (dupilumab, tralokinumab, lebrikizumab, abrocitinib, upadacitinib, nemolizumab): **co-primary endpoints of (a) EASI-75 and (b) vIGA-AD success (score 0/1 with ≥2-grade improvement) at Week 16**, with pruritus (PP-NRS ≥4-point improvement) as a key secondary. Build your Phase 2 around these same instruments even though Phase 2 itself won't need co-primary rigor — Phase 3 will, and FDA will expect endpoint continuity across phases.

**1.3 Recommended regulatory interactions:**
- **End-of-Phase 1 (Type B) meeting** with the Division of Dermatology now, using your 1b safety/biomarker package, to align on Phase 2b dose-ranging design, endpoint selection, and whether a biomarker (e.g., TARC suppression) can be proposed as a supportive/exploratory (not surrogate) endpoint.
- **Fast Track designation** is worth filing for now if you can articulate an unmet-need argument (e.g., "first oral, non-JAK, IL-13-pathway-selective agent" — this is exactly the argument Kymera used for KT-621, which received Fast Track in December 2025 off Phase 1b data alone). Fast Track gets you rolling review and more frequent FDA touchpoints during Phase 2/3.
- **Breakthrough Therapy** is a reach at this stage — typically granted post-Phase 2 proof-of-concept, not off biomarker + safety data alone, unless your 1b clinical (not just biomarker) signal is unusually large.
- **End-of-Phase 2 meeting** and likely a **Special Protocol Assessment (SPA)** request for the Phase 3 pivotal design once Phase 2b reads out.

**1.4 The JAK question — resolve this before finalizing the protocol.** If any part of the mechanism inhibits JAK1/2/3 or TYK2 upstream of STAT6, FDA's 2021 class-wide boxed-warning requirement (triggered by the tofacitinib ORAL Surveillance cardiovascular/malignancy signal) will very likely apply, forcing: a boxed warning, restricted labeling to patients who've failed/can't tolerate a biologic, and probably a dedicated long-term CV/malignancy safety trial before or shortly after approval (abrocitinib and upadacitinib both carry this). If the compound is a genuinely selective downstream degrader/antagonist (STAT6 or direct IL-13-axis target) that does not touch JAK kinase activity, you have a real argument for avoiding this — but FDA has not yet ruled on this for any approved product, since KT-621 itself is still in Phase 2b with data expected late 2026. Raise this explicitly at the EOP1 meeting; don't assume it away.

**1.5 Standard package requirements to plan for in parallel:** nonclinical carcinogenicity study (2-year rodent or an accepted alternative), thorough QTc assessment, hepatic/renal impairment PK substudies, DDI package (especially CYP/transporter interactions given oral dosing), and — per the pediatric-timing guidance in §1.2 — a plan for when adolescent (12–17) patients enter development (commonly folded into the Phase 2b/3 program now, as KT-621's BROADEN2 does with ages 12–75, rather than deferred).

---

## 2. Competitive Landscape

| Agent | Class | Route | Status | Pivotal efficacy (EASI-75, wk 16, active vs. placebo) | Relevance to differentiation |
|---|---|---|---|---|---|
| Dupilumab (Dupixent) | Anti-IL-4Rα mAb (blocks IL-4 & IL-13) | SC, q2wk | Approved 2017 | ~70% vs ~20–30% (SOLO 1/2) | Market leader; sets the efficacy bar and payer benchmark |
| Tralokinumab (Adbry) | Anti-IL-13 mAb | SC, q2–4wk | Approved 2021 | ~56% vs ~12% (ECZTRA 1/2, N=1596 total) | Direct IL-13 mechanism, biologic |
| Lebrikizumab (Ebglyss) | Anti-IL-13 mAb (high affinity) | SC, q2–4wk maintenance | Approved 2024 | ~52–59% vs ~12–18% (ADvocate 1/2; ADvocate2 N=281 active/146 placebo) | Closest efficacy/mechanism comp; recent approval sets precedent for Division's current thinking |
| Abrocitinib (Cibinqo) | Oral JAK1 inhibitor | Oral, qd | Approved 2022, boxed warning | ~fig 60-70% at 200mg vs ~10-15% | Oral competitor, but carries JAK boxed warning — your key differentiation opportunity if avoided |
| Upadacitinib (Rinvoq) | Oral JAK1 inhibitor | Oral, qd | Approved 2022, boxed warning | ~65-80% vs ~15% (Measure Up 1/2) | Same as above; among the most efficacious agents in class |
| Ruxolitinib cream (Opzelura) | Topical JAK1/2 inhibitor | Topical | Approved 2021/22 | Mild-moderate AD only | Not a direct comparator (topical, less severe population) |
| Nemolizumab (Nemluvio) | Anti-IL-31RA mAb | SC | Approved 2024/25 | Itch-focused; skin-clearance secondary | Different primary target (pruritus axis) |
| **KT-621 (Kymera)** | **Oral STAT6 degrader** (IL-4/IL-13 pathway) | **Oral, qd** | **Phase 2b (BROADEN2), ~200 pts, topline late 2026** | Ph1b positive (Dec 2025); Ph2b primary = % change EASI at wk16 | **Closest direct analog to your program** — same modality class, same stage transition |
| APG777 (Apogee) | Anti-IL-13 mAb, extended half-life | SC, low-frequency | Phase 2 (APEX), EASI-75 66.9% reported | Biologic, but positioned on dosing-interval convenience | |
| ENV-294 (Enveda) | Oral small molecule, immune-resetting | Oral | Phase 1b positive (2026) | Very early | Another oral small-molecule entrant to watch |

**Positioning takeaway**: your realistic competitive niche is "oral, once-daily, IL-13-pathway-selective, avoids JAK boxed warning" — occupied currently only by KT-621 and, more nascently, ENV-294. If the mechanism can't clear the JAK-warning question favorably, your differentiation collapses into "another oral JAK inhibitor," a much more crowded and already-genericizing space.

---

## 3. Sample Size Justification

**Interpreting "30% improvement over placebo."** This phrase is ambiguous and materially changes the math, so I'm stating the interpretation I used: **a 30-percentage-point absolute difference between drug and placebo arms in mean percent reduction from baseline EASI at Week 16** (e.g., placebo −25%, drug −55%), analyzed as a continuous endpoint — the same primary-endpoint structure KT-621's BROADEN2 uses. If you actually meant a 30-point difference in EASI-75 *responder rate* (a binary proportion), tell me and I'll redo this as a two-proportion calculation — the two produce different N's and it's a common point of confusion in AD protocols.

**Design**: 4-arm, randomized, double-blind, placebo-controlled, dose-ranging (placebo + low/mid/high dose), consistent with how every recent oral AD asset (KT-621, abrocitinib, upadacitinib) transitioned from 1b into a dose-finding 2b rather than a single-dose 2-arm study — you don't yet know your Phase 3 dose, and Phase 1b safety/PD data alone rarely nails it.

**Statistical test**: two-sample comparison of mean % change from baseline EASI (each active dose vs. placebo), via ANCOVA with baseline EASI as covariate; primary analysis population = ITT (randomized + ≥1 dose); missing data handled via MMRM under a treatment-policy estimand (ICH E9(R1)) — i.e., data collected after rescue/discontinuation are still analyzed as observed, which is now the FDA-preferred default over LOCF.

**Parameters**:
- Δ (treatment effect to detect) = 30 percentage points
- σ (SD of % change from baseline EASI) — no public SAP gave me an exact figure, so I used **35%**, the midpoint of the 30–40% range that recurs across published moderate-to-severe AD trials with comparable baseline severity (EASI ~25–33); I show sensitivity below since this is the single most consequential unverified assumption in the whole calculation.
- α = 0.05 two-sided, adjusted for 2 active-dose comparisons vs. one placebo via Dunnett-type multiplicity control → effective per-comparison α ≈ 0.025 (z = 2.24)
- Power = 90% (z = 1.28)
- Anticipated dropout over 16 weeks = 15% (consistent with recent 16-week AD trials)

**Formula**: n per arm = 2σ²(z_α/2 + z_β)² / Δ²

Base case (σ=35): n = 2(35²)(2.24+1.28)² / 30² = 2(1225)(12.39)/900 ≈ 34/arm before dropout → **≈40/arm after 15% dropout inflation**.

**Sensitivity table** (per-arm N, post-dropout, same design):

| σ assumption | Δ=30 pts, N/arm |
|---|---|
| 30% | ~29 |
| 35% (base case) | ~40 |
| 40% | ~52 |

**Recommendation**: enroll **~45–50 evaluable patients per arm × 4 arms (placebo + 3 doses) ≈ 180–200 total**, which lands almost exactly on KT-621's BROADEN2 enrollment (~200) — a reasonable external validation that this is the right order of magnitude for a 2026-era Phase 2b in this indication, and gives you margin against the σ uncertainty above. **Before locking this**, get an actual σ estimate for % change in EASI from your own Phase 1b data (even n=20–30 gives a usable variance estimate) rather than relying on cross-trial literature assumptions — this is the number I'd most want to correct.

---

## 4. Study Design & Procedures Outline

**Design**: Multicenter, randomized (1:1:1:1), double-blind, placebo-controlled, parallel-group, dose-ranging Phase 2b, 16-week double-blind treatment period + optional long-term open-label extension (52 wk) for safety/durability.

**Population** (draft key criteria):
- Inclusion: age 18–75 (consider 12–17 co-enrollment per §1.5); chronic AD ≥1 year; EASI ≥16; vIGA-AD ≥3; BSA ≥10%; documented inadequate response to topical corticosteroids/calcineurin inhibitors.
- Key exclusions: prior biologic/JAK exposure within washout window; active skin infection; other confounding dermatoses; clinically significant hepatic/renal/cardiac disease (esp. if any JAK-adjacent liability — see §1.4); pregnancy.

**Arms**: Placebo; Dose A (low, from 1b PK/PD); Dose B (mid); Dose C (high, at or near 1b MTD/MABEL-informed ceiling), oral once daily.

**Endpoints**:
- Primary: % change from baseline in EASI at Week 16.
- Key secondary: EASI-75/50/90 responder rates; vIGA-AD 0/1 success; PP-NRS ≥4-point improvement; time course of biomarker suppression (TARC, periostin, or transcriptomic Th2 panel) to confirm mechanistic engagement links to clinical response.
- Safety: AEs/SAEs, labs (hepatic, renal, lipid, CBC), infections, malignancy screening, cardiovascular monitoring if any mechanistic overlap with JAK class.
- Exploratory/PK-PD: dose-exposure-response modeling to select the Phase 3 dose.

**Schedule of assessments** (typical cadence for this design):

| Visit | Wk 0 (BL) | Wk 2 | Wk 4 | Wk 8 | Wk 12 | Wk 16 (primary) | Follow-up (wk 20) |
|---|---|---|---|---|---|---|---|
| EASI / vIGA-AD / BSA | ✓ | | ✓ | ✓ | ✓ | ✓ | ✓ |
| PP-NRS (daily diary) | ✓ | ongoing | ongoing | ongoing | ongoing | ✓ | |
| Safety labs, vitals | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PK sampling | ✓ | ✓ | ✓ | | ✓ | ✓ | |
| Biomarkers (serum/skin) | ✓ | | ✓ | | | ✓ | |
| AE/con-med review | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Statistical analysis plan skeleton**: ANCOVA/MMRM as above for primary; Cochran-Mantel-Haenszel or logistic regression for responder-rate secondaries; multiplicity control across the 3 active-dose-vs-placebo comparisons (Dunnett or hierarchical gatekeeping if secondaries are to carry confirmatory weight); interim futility look optional given 16-week duration (probably not needed at this N).

---

## 5. Open Items to Resolve Before This Goes to a Real Protocol

1. Confirm mechanism's relationship to JAK kinase activity — determines boxed-warning/REMS risk and reshapes the whole regulatory and safety-monitoring section (§1.4).
2. Get an actual Phase 1b-derived σ for % EASI change to replace the literature-based assumption in §3.
3. Confirm what "30% improvement over placebo" was meant to mean (continuous EASI delta vs. EASI-75 responder-rate delta) — I defaulted to the continuous interpretation.
4. Decide adolescent inclusion timing now vs. deferred (affects PREA planning and the pediatric-timing guidance in §1.2).
5. Schedule the End-of-Phase 1 meeting with FDA's Division of Dermatology before finalizing dose selection for Phase 2b — that meeting will likely also weigh in on all of the above.

Sources: [FDA – Atopic Dermatitis: Timing of Pediatric Studies Guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/atopic-dermatitis-timing-pediatric-studies-during-development-systemic-drugs), [NEJM – Lebrikizumab Phase 3 (ADvocate)](https://www.nejm.org/doi/full/10.1056/NEJMoa2206714), [BJD – Tralokinumab ECZTRA 3](https://academic.oup.com/bjd/article/184/3/450/6702218), [Kymera – KT-621 Phase 1b results](https://investors.kymeratx.com/news-releases/news-release-details/kymera-therapeutics-announces-positive-results-broaden-phase-1b), [Kymera – BROADEN2 Phase 2b enrollment complete](https://investors.kymeratx.com/news-releases/news-release-details/kymera-therapeutics-completes-enrollment-phase-2b-broaden2-trial/), [NEJM – Abrocitinib vs Placebo/Dupilumab (JADE COMPARE)](https://www.nejm.org/doi/full/10.1056/NEJMoa2019380), [PMC – IL-13 inhibition in AD treatment](https://pmc.ncbi.nlm.nih.gov/articles/PMC11574908/).