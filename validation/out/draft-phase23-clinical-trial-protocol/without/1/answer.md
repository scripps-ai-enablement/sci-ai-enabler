No problem — I'll deliver the full draft directly here instead of as a file.

# Phase 2 Study Plan — Draft v0.1
## Oral Small-Molecule IL-13-Pathway Suppressant for Moderate-to-Severe Atopic Dermatitis

**Status:** First-draft working document built from your Phase 1b safety/biomarker data — not a protocol. Sharpen it at a formal FDA meeting and with your biostatistics/regulatory leads before it becomes a protocol synopsis.

## 0. Assumptions I made (correct these before using this)

You didn't specify the exact mechanism, Phase 1b design, or what "30% improvement" refers to precisely, so I anchored on the most realistic, recent analog: an oral, once-daily small molecule acting on a node downstream of IL-4Rα (e.g., a STAT6 inhibitor/degrader) that suppresses both IL-4 and IL-13 signaling — modeled closely on Kymera's KT-621 (oral STAT6 degrader; positive Phase 1b "BroADen" data reported Dec 2025; now in Phase 2b "BROADEN2"). If your molecule works through a different node, revisit Section 1's safety framework and Section 4's biomarker panel.

Other explicit assumptions:
- **Population:** adults ≥18, EASI ≥16, vIGA-AD ≥3, BSA ≥10%, inadequate response to topicals — the standard systemic-AD entry bar.
- **Phase 1b:** small (~20–30 subjects), showing strong target engagement (e.g., ~90%+ pathway suppression) and directional Th2 biomarker reduction (TARC/CCL17, IgE, periostin) with a clean safety profile.
- **"30% improvement in EASI over placebo"** = a **30-percentage-point absolute difference in EASI-75 responder rate** (e.g., ~55% vs. ~25%), since that's how FDA and industry actually frame this endpoint. I also computed the continuous-endpoint version (% EASI change) in case that's what you meant.
- You intend a **dose-ranging Phase 2b** ahead of a pivotal Phase 3 program, not a combined adaptive design.

## 1. FDA Regulatory Pathway

- **Application:** standard **NDA under 505(b)(1)** through CDER (small molecule vs. the BLAs used by dupilumab/tralokinumab/lebrikizumab/nemolizumab — oral dosing plus non-biologic manufacturing is itself part of your differentiation story).
- **Review home:** CDER's dermatology group, now under the **Office of Immunology and Inflammation** post-reorg — confirm current division name at your next meeting request.
- **Meeting sequence:**
  1. **EOP1 (Type B) meeting now** — align on dose selection from Phase 1b PK/PD, the primary endpoint/timepoint, safety monitoring scope, and whether FDA will apply JAK-inhibitor-class safety expectations to your mechanism.
  2. **iPSP (PREA)** — due within 60 days of the *EOP2* meeting; start drafting now given the long negotiation lead time. FDA has a standing draft guidance on pediatric AD drug development (≥3 months–<18 years).
  3. **EOP2 (Type B) meeting** after Phase 2b readout to lock Phase 3 design and long-term safety database size (ICH E1: ~300–600 subjects at 6 months, ~100 at 1 year, for a chronic non-life-threatening condition).
- **Expedited programs:** **Fast Track** is reasonable to request now (serious, chronic, unmet need for well-tolerated orals — exactly Kymera's basis for KT-621). **Breakthrough Therapy** is premature until you have randomized Phase 2 data showing substantial improvement over available therapy. **Orphan** doesn't apply.
- **The big risk to plan around:** since the 2021 tofacitinib ORAL Surveillance signal, FDA has applied a class-wide **boxed warning** (malignancy, MACE, thrombosis, serious infection, mortality) to oral JAK inhibitors in AD (abrocitinib, upadacitinib), even though the signal came from an RA population. A STAT6-adjacent mechanism will likely draw the same scrutiny. Build the associated monitoring panel (CBC w/ differential, lipid panel, CPK, zoster surveillance, VTE/malignancy tracking) into Phase 2b now — arguing for a cleaner label later requires having the exposure-years of clean data already in hand.
- **REMS:** not anticipated yet; reassess at EOP2.

## 2. Competitive Landscape

**Approved agents:**

| Agent | Mechanism | Approved | Placebo-adjusted EASI-75 (Wk 16) | Notes |
|---|---|---|---|---|
| Dupilumab (Dupixent) | Anti-IL-4Rα mAb | 2017 | ~44–50% vs 12–15% placebo | Market leader, injectable, no boxed warning |
| Tralokinumab (Adbry) | Anti-IL-13 mAb | 2021 | ~25–33% vs 10–12% placebo | Closest MOA cousin, injectable |
| Lebrikizumab (Ebglyss) | Anti-IL-13 mAb | Sept 2024 | ~58–62% vs ~16% placebo | Best-in-class IL-13 mAb |
| Nemolizumab (Nemluvio) | Anti-IL-31RA mAb | Dec 2024 | Pruritus-focused | Differentiates on itch |
| Upadacitinib (Rinvoq) | Oral JAK1 inhibitor | Jan 2022 | Ph2b: 74/62/39% vs 23% placebo (% EASI change) | Oral, effective, **boxed warning** |
| Abrocitinib (Cibinqo) | Oral JAK1 inhibitor | Jan 2022 | Comparable | Oral, **boxed warning** |
| Ruxolitinib cream (Opzelura) | Topical JAK1/2 | 2021/22 | — | Boxed warning still applies |
| Tapinarof / Roflumilast creams | AhR agonist / PDE4i | Dec 2024 / Jul 2024 | — | Nonsteroidal topicals |

**Late-stage pipeline (your real competitive set):**

| Agent | Mechanism | Stage | Signal |
|---|---|---|---|
| **KT-621 (Kymera)** | Oral STAT6 degrader | Ph2b (BROADEN2), data ~mid-2027 | Ph1b: 98% peripheral/94% lesional STAT6 degradation, TARC ↓74%, mean EASI ↓63% (OL) — **your closest comparator** |
| Rocatinlimab / Amlitelimab | Anti-OX40 / OX40L mAb | Phase 3 | Pending / ongoing |
| Eblasakimab (ASLAN) | Anti-IL-13Rα1 mAb | Ph2b complete | −60 to −74.5% vs −38% placebo (% EASI change) |
| Rezpegaldesleukin (Nektar/Lilly) | Treg-selective IL-2 mutein | Ph2b positive 2026 | Met primary + key secondary |
| Zumilokibart / APG777 | Anti-IL-13 mAb | Phase 2 | EASI-75 hit / EASI ↓71% |

**Positioning:** injectable IL-13/IL-4Rα biologics have normalized 55–75% EASI-75, and oral JAKis match that but carry a boxed warning limiting uptake. Your pitch — oral convenience with a cleaner, pathway-selective safety profile — is the identical pitch Kymera is making with KT-621, so expect its data to be the external benchmark. Your Phase 2b needs enough clean long-term safety exposure to substantiate "not a JAK inhibitor," not just an efficacy win.

## 3. Sample Size Calculation

**Primary endpoint:** EASI-75 responder rate at Week 16. Assumption: placebo ~25%, active ~55% (30-point absolute difference — replace with your own placebo-response estimate).

Two-proportion z-test, two-sided α=0.05:

| Power | n/arm (raw) | n/arm (+15% dropout) |
|---|---|---|
| 80% | ~41 | ~49 |
| **90% (recommended)** | **~54** | **~64** |

Recommend powering at 90%: a Phase 2b here doubles as your Phase 3 dose-selection decision, so under-powering is expensive in ways that dwarf the extra N. **Design:** placebo + 3 active doses × ~64/arm ≈ **~256 randomized subjects** — in line with precedent (REZOLVE-AD enrolled 393 across 5 arms; upadacitinib's Ph2b used ~42/arm at 80% power for a similar effect size).

**If "30% improvement" instead means a continuous % EASI-change difference** (e.g., −65% vs. −35%, SD≈40 points, consistent with eblasakimab's observed spread): n/arm ≈ 28 (80% power) to 37 (90%) before dropout — smaller, as expected for a continuous vs. binary endpoint. Confirm the intended framing with biostatistics, but keep EASI-75 responder proportion as primary regardless — it's what FDA and payers benchmark.

No formal multiplicity correction is typically needed at Ph2b (independent dose-vs-placebo tests, or pre-specify an MCP-Mod dose-response model in the SAP).

## 4. Study Design Outline (Phase 2b)

- **Design:** randomized, double-blind, placebo-controlled, parallel-group, dose-ranging.
- **Population:** adults 18–75, AD ≥1 year, EASI ≥16, vIGA-AD ≥3, BSA ≥10%, inadequate response/intolerance to topicals; washout of prior systemics; stratify by prior JAK-inhibitor exposure if you want a broad label claim.
- **Arms:** placebo + 3 active doses (from Phase 1b exposure-response), 1:1:1:1, stratified by baseline severity (EASI <25 vs ≥25) and region.
- **Duration:** 16-week double-blind primary period → optional extension to Week 52 to start building the long-term safety database FDA will want at EOP2.
- **Visits:** Screening → Baseline → Wks 2, 4, 8, 12, 16 (primary) → 20/28/40/52 if extended → safety follow-up 4–8 wks post-last-dose.
- **Endpoints:**
  - *Primary:* EASI-75 at Wk16 (consider co-primary with vIGA-AD 0/1 + ≥2-grade improvement, matching current approvals and Phase-3-readiness)
  - *Key secondary:* % EASI change, EASI-90, Peak Pruritus NRS (≥4-pt), Sleep Disturbance NRS, DLQI, time-to-response
  - *Exploratory biomarkers (extending your Phase 1b signal):* target-engagement PD marker (blood + lesional biopsy), TARC/CCL17, IgE, periostin, eosinophils, Type 2 transcriptomic signature — supports EOP2 dose justification and a potential enrichment strategy for Phase 3
  - *Safety:* AEs/SAEs, the JAK-adjacent lab panel above, zoster surveillance, MACE/VTE adjudication if signals emerge, malignancy surveillance
- **Procedures:** certified EASI/vIGA-AD raters, central-read photography, eDiary pruritus NRS, trough PK sampling (+ sparse full-PK subset), optional biopsy substudy, rescue-medication rules (low-potency topical steroid after a pre-specified worsening threshold, analyzed as non-responder).
- **Analysis:** ITT for efficacy (non-responder imputation), safety population = all dosed; logistic regression/CMH for the primary, MMRM for continuous secondaries.
- **Oversight:** independent DSMB given mechanism-adjacency to a boxed-warning class; at least one safety review at ~50% enrollment with pre-specified MACE/VTE/malignancy stopping rules.

## Immediate next steps
1. Swap in your real mechanism, Phase 1b design, and placebo-response estimate.
2. Get biostatistics to sign off on responder-vs-continuous framing before the sample-size number goes external.
3. Request the EOP1 Type B meeting — the JAK-adjacency safety question drives protocol scope and should be settled before the SAP locks.
4. Start the iPSP draft now given the long negotiation runway, even though it's formally due after EOP2.

Sources: [Kymera BroADen Ph1b](https://investors.kymeratx.com/news-releases/news-release-details/kymera-therapeutics-announces-positive-results-broaden-phase-1b), [Kymera BROADEN2 initiation](https://investors.kymeratx.com/news-releases/news-release-details/kymera-therapeutics-announces-first-patient-dosed-broaden2-phase), [Kymera Fast Track](https://investors.kymeratx.com/news-releases/news-release-details/kymera-therapeutics-announces-us-fda-fast-track-designation-kt), [Lebrikizumab Ph3 NEJM](https://www.nejm.org/doi/full/10.1056/NEJMoa2206714), [Dupilumab Ph3 NEJM](https://www.nejm.org/doi/full/10.1056/NEJMoa1610020), [Tralokinumab data](https://www.emjreviews.com/wp-content/uploads/2025/05/Tralokinumab-in-Moderate-to-Severe-Atopic-Dermatitis-The-Latest-Data-1.pdf), [ASLAN eblasakimab Ph2b](https://finance.yahoo.com/news/aslan-pharmaceuticals-presents-data-phase-133000570.html), [Nektar REZOLVE-AD](https://ir.nektar.com/news-releases/news-release-details/rezolve-ad-phase-2b-study-rezpegaldesleukin-meets-primary-and), [Galderma nemolizumab approval](https://www.galderma.com/news/galderma-receives-us-fda-approval-nemluvior-nemolizumab-patients-moderate-severe-atopic), [AbbVie upadacitinib Ph2b](https://news.abbvie.com/2017-09-07-AbbVies-Upadacitinib-ABT-494-Meets-Primary-Endpoint-in-Phase-2b-Study-in-Atopic-Dermatitis), [AAD 2026 AD trials (HCPLive)](https://www.hcplive.com/view/aad-2026-6-atopic-dermatitis-trials-to-know), [Emerging AD therapies (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12180583/), [Recent FDA dermatology approvals (AJMC)](https://www.ajmc.com/view/recent-fda-approvals-expand-dermatology-options-for-patients-with-skin-of-color).