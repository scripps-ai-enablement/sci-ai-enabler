# Phase 2 Study Plan — Draft v0.1
## Oral Small-Molecule IL-13 Pathway Inhibitor, Moderate-to-Severe Atopic Dermatitis

**Stated inputs used:** promising Phase 1b safety + biomarker data (IL-13 pathway suppression). Since several parameters weren't specified, I made the following working assumptions — flag any of them for correction and the plan updates from there:

| Assumption | Value used |
|---|---|
| Mechanism/route | Oral, once-daily, small molecule acting intracellularly on IL-13 signaling (e.g., STAT6 or JAK1/TYK2-adjacent node) — the closest real-world analogs are Kymera's KT-621 (oral STAT6 degrader) and Recludix's REX-8756 (oral STAT6 inhibitor) |
| Phase 1b design | SAD/MAD or short (2–4 wk) multiple-dose cohort in healthy volunteers or mild-moderate AD patients, showing dose-dependent target engagement (e.g., serum TARC/CCL17, periostin, or blood/skin STAT6 suppression) and acceptable safety/tolerability, no efficacy claim yet |
| IND status | Open IND already supports the Ph1b work |
| Population | Adults 18–75 with chronic moderate-to-severe AD, inadequate response/intolerance to topical therapy |
| Primary Ph2 endpoint | % change from baseline in EASI at Week 16 |
| Design | Randomized, double-blind, placebo-controlled, dose-ranging (3 active doses + placebo) |

---

## 1. FDA Regulatory Pathway

**Base pathway:** This is a new molecular entity (NME) small molecule → standard **505(b)(1) NDA** pathway, reviewed by the Division of Dermatology (Office of Immunology and Inflammation, OND). No orphan or accelerated-approval pathway applies (AD is not rare, and EASI/IGA are established, not surrogate-for-accelerated-approval, endpoints).

**Governing guidance:**
- FDA's disease-specific guidance for AD drug development establishes EASI (co-primary/key secondary) and vIGA-AD 0/1 with ≥2-grade improvement as the endpoints FDA expects to see carried into pivotal trials — align your Phase 2 endpoint hierarchy now so Phase 3 isn't renegotiating this.
- **"Atopic Dermatitis: Timing of Pediatric Studies During Development of Systemic Drugs" (final guidance, 2018)** — FDA explicitly wants pediatric AD development started *early*, not deferred to post-approval. Practical implication: an initial Pediatric Study Plan (iPSP) should be submitted around/before the End-of-Phase 2 meeting, and you should scope whether an adolescent (12–17) cohort can be added to Phase 2b or run as a parallel small dose-finding study, rather than waiting for Phase 3 completion. This is a PREA obligation, not optional.
- **ICH E9(R1) estimand framework** — build this into the Ph2 SAP now (see §4), since FDA reviewers increasingly expect a documented estimand (handling of rescue medication, treatment discontinuation) even at Phase 2.

**Designations worth pursuing now:**
- **Fast Track** — reasonable to file after Phase 1b: it requires only nonclinical/PK or preliminary clinical data supporting a serious-condition + unmet-need argument, not proven efficacy. This is precedented — Kymera's KT-621, an oral STAT6 degrader in the same mechanistic class, received Fast Track designation in December 2025 on the strength of Phase 1b biomarker/safety data alone before starting its Phase 2b. ([HCPLive](https://www.hcplive.com/view/stat6-il-31-and-il-18-headline-burgeoning-pipeline-in-atopic-dermatitis-with-david-rosmarin-md))
- **Breakthrough Therapy** — premature; requires preliminary *clinical* evidence of substantial improvement over available therapy, which you won't have until a Phase 2 efficacy readout.
- **SPA (Special Protocol Assessment)** — not applicable to Phase 2; reserve for the Phase 3 protocol.
- **Pre-Phase 2 FDA interaction:** request a **Type B/EOP1-style meeting** before finalizing the protocol to align on (a) dose selection/justification from Ph1b PK-PD, (b) primary vs. key secondary endpoint hierarchy, (c) biomarker qualification strategy, and (d) the iPSP timeline. This is cheap insurance against redoing Phase 2 dosing.
- **Safety framing:** post-2021 ODAC scrutiny of JAK inhibitors in AD (boxed warnings for malignancy/MACE/thrombosis, driven by the oral tofacitinib rheumatoid arthritis safety trial) means FDA will actively probe whether your MOA carries JAK-class risk even though you're not a JAK inhibitor. If your mechanism is STAT6-selective (downstream of JAK, upstream of transcription), explicitly build a differentiation argument (and monitoring plan) into the protocol's safety section — this will be one of the first questions in any FDA meeting.

---

## 2. Competitive Landscape & Prior Trials

### Approved systemic therapies (efficacy benchmark for your effect-size target)

| Drug | Class | Approved | Ph3 EASI-75 (Wk16, active vs. placebo, approx.) |
|---|---|---|---|
| Dupilumab (Dupixent) | Anti-IL-4Rα mAb (blocks IL-4 + IL-13) | 2017 | ~51% vs ~15% |
| Tralokinumab (Adbry) | Anti-IL-13 mAb | 2021 | ~56% vs ~12% (Ph2b dose-ranging preceded this) |
| Lebrikizumab (Ebglyss) | Anti-IL-13 mAb | 2023 | ~59% vs ~13% |
| Nemolizumab (Nemluvio) | Anti-IL-31Rα mAb (itch-targeted) | 2024 | Itch-focused; EASI-75 secondary |
| Abrocitinib (Cibinqo) | Oral JAK1 inhibitor | 2022 | ~63–71% vs ~12% |
| Upadacitinib (Rinvoq) | Oral JAK1 inhibitor | 2022 | ~65–80% vs ~13% |
| Ruxolitinib cream (Opzelura) | Topical JAK1/2 | 2021 | Topical, mild-moderate only |

These biologics/JAK trials are also your regulatory precedent for Phase 2 dose-ranging design and placebo response rates (placebo EASI-75 typically 10–20%; placebo % EASI improvement typically 15–35%). ([Dermatology Times year-in-review](https://www.dermatologytimes.com/view/dermatology-times-2025-year-in-review-drug-approvals), [AJMC](https://www.ajmc.com/view/recent-fda-approvals-expand-dermatology-options-for-patients-with-skin-of-color))

### Direct mechanistic competitors (oral, IL-13-pathway, pre-registrational) — your real competitive set

| Program | Sponsor | Mechanism | Stage (mid-2026) |
|---|---|---|---|
| **KT-621** | Kymera Therapeutics | Oral STAT6 degrader | Phase 1b showed ~98% blood / ~94% skin STAT6 reduction; now in Phase 2b in moderate-to-severe AD; FDA Fast Track (Dec 2025) |
| **REX-8756** | Recludix Pharma | Oral STAT6 inhibitor (SH2 domain, non-degrader) | IND-enabling/early clinical |
| **KP-723** | Kaken Pharmaceutical (licensed to J&J) | STAT6 program | Preclinical/early clinical, newly licensed |

This is a genuinely tight field — you are very likely racing KT-621 head-to-head on trial design, dose selection, and readout timing, and it has already validated that Fast Track is obtainable off Phase 1b data alone. ([Dermatology Times](https://www.dermatologytimes.com/view/recludix-pharma-advances-first-in-class-oral-stat6-inhibitor-rex-8756-for-inflammatory-diseases-including-atopic-dermatitis), [J&J press release](https://www.jnj.com/media-center/press-releases/johnson-johnson-to-license-novel-oral-assets-further-strengthening-commitment-to-atopic-dermatitis))

**Strategic implication for your Phase 2:** Your differentiation case is (1) oral convenience vs. injectable biologics, and (2) a cleaner safety label than JAK inhibitors if your mechanism doesn't touch JAK1/2/3 or TYK2 directly. To make that case, your protocol needs a safety monitoring package at least as rigorous as the JAK trials (lipids, CBC, infections, herpes zoster, malignancy screening at baseline) even though you may not expect the same signal — reviewers will want the data to prove absence, not just mechanistic reasoning.

---

## 3. Sample-Size Justification

**Endpoint interpreted literally as requested:** mean percent change from baseline in EASI at Week 16, active vs. placebo, targeting a **30-percentage-point** between-group difference (e.g., −65% active vs. −35% placebo — placebo assumption consistent with published AD Ph2b placebo response).

**Statistical assumptions:**
- Two-sample t-test comparison, two-sided α = 0.05
- Common SD (σ) = 35 percentage points — mid-range of the 30–45 pooled-SD figures reported in tralokinumab/dupilumab/lebrikizumab Phase 2b EASI %-change data
- Formula: n per arm = 2·σ²·(z₁₋α/2 + z₁₋β)² / Δ²

| Power | z₁₋β | n per arm (raw) | n per arm (after 15% dropout, ÷0.85) |
|---|---|---|---|
| 80% | 0.842 | 21.4 → **22** | **26** |
| 90% | 1.282 | 28.6 → **29** | **35** |

**Sanity check on a binary regulatory-relevant endpoint** (EASI-75 responder rate, since this is what actually anchors labels): assuming placebo response 15%, active response 45% (30-point difference, same magnitude), two-proportion z-test gives **36/arm at 80% power, 47/arm at 90% power** before dropout adjustment — meaningfully larger than the continuous calculation because responder-rate tests are less efficient than continuous comparisons at this effect size. After 15% dropout inflation: **~42–55/arm**.

**Recommendation:** Don't power off the optimistic continuous-endpoint number alone — it understates what's needed to also support a credible EASI-75 secondary claim, which is what FDA and competitors will actually compare against. I'd size the study to the more conservative estimate and add margin for:
- **Multiple dose arms:** With 3 active doses + placebo, use **Dunnett's test** (not Bonferroni) for the primary MCP comparisons — it's the standard, less-conservative choice for many-to-one comparisons and only inflates required n by roughly 10–15% relative to a single pairwise test, versus ~25%+ under Bonferroni.
- **MCP-Mod** as the primary dose-response analysis framework — it's explicitly designed for Phase 2 dose-finding, is endorsed by both FDA and EMA, and gives you a formal dose-response model (not just pairwise significance) to carry into Phase 3 dose selection.

**Final working target: ~55–65 evaluable patients per arm × 4 arms ≈ 220–260 total randomized.** This lands in the same range as comparable Phase 2b AD dose-ranging trials (tralokinumab ~200, lebrikizumab ~280) and gives adequate power for both the primary continuous endpoint and the EASI-75/IGA 0-1 secondary endpoints that will actually inform the go/no-go and Phase 3 dose decision.

*(If you can share your actual Phase 1b PK-PD-derived expected placebo rate, target-engagement-linked efficacy assumption, or a fixed budget/enrollment ceiling, this range narrows considerably — the above is a defensible default, not a fitted number.)*

---

## 4. Study Design & Procedures — Initial Outline

**Title (working):** A Randomized, Double-Blind, Placebo-Controlled, Dose-Ranging Phase 2 Study to Evaluate the Efficacy, Safety, and Pharmacodynamics of [Compound] in Adults with Moderate-to-Severe Atopic Dermatitis

**Design:** Multicenter, randomized 1:1:1:1 (Placebo : Dose A : Dose B : Dose C), double-blind, parallel-group, 16-week treatment period, with optional 36–52-week open-label extension for durability/long-term safety.

**Dose selection:** 3 active doses selected from Ph1b PK/PD to bracket ~50%, ~80%, and ≥90% target (STAT6/biomarker) engagement — carry the actual Ph1b exposure-response curve into this decision rather than arbitrary dose spacing.

**Population:**
- *Key inclusion:* age 18–75; chronic AD ≥1 year; EASI ≥16; vIGA-AD ≥3; BSA involvement ≥10%; documented inadequate response or intolerance to topical corticosteroids/calcineurin inhibitors
- *Key exclusion:* recent biologic (washout ≥5 half-lives) or JAK inhibitor (≥4 weeks) use; active skin infection; other confounding dermatoses; history of malignancy (except treated basal cell); significant hepatic/renal impairment; QT-prolonging comorbidity if mechanism warrants ECG monitoring; pregnancy/lactation

**Study periods:**
1. Screening (up to 4 weeks)
2. Double-blind treatment (16 weeks)
3. Safety follow-up (8 weeks post last dose)
4. Optional open-label extension

**Endpoints:**
- *Primary:* % change from baseline in EASI at Week 16
- *Key secondary:* EASI-75/-90 responder rates; vIGA-AD 0/1 with ≥2-grade improvement; Peak Pruritus NRS weekly change; BSA affected; patient-reported outcomes (POEM, DLQI)
- *Pharmacodynamic:* serum TARC/CCL17 and periostin; blood/skin STAT6 (or relevant node) target engagement, leveraging the Ph1b biomarker assay; optional paired skin biopsy substudy (Th2 transcriptomic signature reversal) in a subset of consenting sites
- *Safety:* AEs/SAEs, labs (hepatic panel, CBC, lipids), ECG if indicated by mechanism, infection surveillance (conjunctivitis — a known IL-13-pathway class effect worth prospectively tracking — and herpes zoster), PK sampling for population PK/exposure-response modeling
- *Exploratory:* biomarker predictors of response (baseline Th2 signature, IgE, eosinophils) to inform Phase 3 enrichment strategy

**Rescue medication:** Protocol-defined topical corticosteroid rescue permitted per pre-specified criteria (ethically necessary for a 16-week placebo-controlled AD trial); analyzed per the ICH E9(R1) estimand (treatment-policy strategy as primary, with a hypothetical-strategy sensitivity analysis excluding rescue-medication effects).

**Statistical analysis:**
- Primary: MMRM or ANCOVA on % EASI change, baseline EASI as covariate, missing data handled via multiple imputation; tipping-point sensitivity analysis
- Dose-response: MCP-Mod framework, Dunnett-adjusted pairwise comparisons vs. placebo as confirmatory secondary check
- Responder endpoints: logistic regression, non-responder imputation for rescue/dropout
- Safety monitoring: independent DSMB with at least one safety review at ~50% enrollment given this is the first patient-efficacy exposure for the molecule

**Timeline (rough):** 9–12 months enrollment, 16-week treatment + 8-week follow-up per patient, database lock, then EOP2 meeting with FDA to finalize Phase 3 dose and pivotal endpoint strategy before program advances.

---

**Sources consulted for current landscape (mid-2026):**
- [Dermatology Times — 2025 Year in Review: Drug Approvals](https://www.dermatologytimes.com/view/dermatology-times-2025-year-in-review-drug-approvals)
- [AJMC — Recent FDA Approvals Expand Dermatology Options](https://www.ajmc.com/view/recent-fda-approvals-expand-dermatology-options-for-patients-with-skin-of-color)
- [HCPLive — STAT6, ITK Inhibitors, IL-31, & IL-18 Headline Burgeoning AD Pipeline](https://www.hcplive.com/view/stat6-il-31-and-il-18-headline-burgeoning-pipeline-in-atopic-dermatitis-with-david-rosmarin-md)
- [Dermatology Times — Recludix Pharma REX-8756](https://www.dermatologytimes.com/view/recludix-pharma-advances-first-in-class-oral-stat6-inhibitor-rex-8756-for-inflammatory-diseases-including-atopic-dermatitis)
- [J&J — Licensing of KP-723 STAT6 program](https://www.jnj.com/media-center/press-releases/johnson-johnson-to-license-novel-oral-assets-further-strengthening-commitment-to-atopic-dermatitis)
- [FDA — Atopic Dermatitis: Timing of Pediatric Studies During Development of Systemic Drugs](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/atopic-dermatitis-timing-pediatric-studies-during-development-systemic-drugs)

**Next-highest-leverage input from you:** the actual Phase 1b dose/PK-PD data and target biomarker assumptions — those two things would let me replace the placeholder dose-selection and effect-size assumptions above with numbers grounded in your own data rather than published-competitor benchmarks.