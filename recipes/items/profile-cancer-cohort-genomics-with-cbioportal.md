---
title: Profile a cancer cohort's genomics with cBioPortal
parent: All recipes
grand_parent: Recipes
nav_order: 20
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine, Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-14
summary: Use the cBioPortal Claude Skill to query TCGA-scale studies for mutation frequency, oncoprints, TMB, and survival by genomic subgroup in plain language.
---

# Profile a cancer cohort's genomics with cBioPortal

Name a cancer study and a gene set; get back per-gene alteration frequency, an oncoprint-style summary, tumor mutational burden, and Kaplan-Meier survival split by mutation status — pulled from cBioPortal's harmonized public cohorts (TCGA and beyond) without writing a line of REST client code.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine, Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A translational scientist hears that gene X "might matter" in a tumor type and needs the cohort-level picture fast: how often is X altered in this cancer, what co-occurs with it, does altered-X track with worse survival, and how does that vary by stage, subtype, or ancestry. cBioPortal holds the harmonized public answer (thousands of studies including the full TCGA PanCancer set), but its REST API has fiddly study/molecular-profile/sample-list identifiers, and the web UI does not script or reproduce cleanly across genes and cohorts. Solved looks like: name the study and the genes, get a cited table of alteration frequencies, a co-occurrence read, a TMB summary, and a survival split — reproducibly, in one conversation, with the cohort caveats stated.

## Recommended approach

1. **Install the [cBioPortal skill](../../catalog/tools/cbioportal-database.html)** from the SciAgent-Skills collection:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm it appears under `/plugin` → Installed. Claude runs the skill's Python locally against the public cBioPortal REST API — no auth, no key.

2. **Resolve the study and genes first.** Study identifiers are the slugs cBioPortal uses internally (e.g., `coadread_tcga_pan_can_atlas_2018`); have Claude look up the correct one before querying so counts come from the cohort you mean:

   ```
   Use the cbioportal skill. Find the cBioPortal study identifier for
   the TCGA PanCancer Atlas colorectal cohort, and confirm the sample
   count and which molecular profiles (mutations, CNA, mRNA) are
   available before running any frequency query.
   ```

3. **Pull alteration frequency and co-occurrence.** Ask for per-gene altered-sample fractions and the pairwise co-occurrence / mutual-exclusivity read across your gene set:

   ```
   For that study, report the alteration frequency (mutation + CNA) of
   APC, KRAS, TP53, PIK3CA, SMAD4, and BRAF as a table: gene | % altered
   | n altered / n profiled. Then flag any pair that co-occurs or is
   mutually exclusive more than chance. Cite the study ID and molecular
   profile IDs used.
   ```

4. **Add TMB and a survival split.** TMB (mutations per Mb) and Kaplan-Meier by mutation status are the two analyses that turn a frequency table into a translational read:

   ```
   For the same cohort: (a) summarize tumor mutational burden
   (median, IQR) overall and split by MSI status if available;
   (b) run Kaplan-Meier overall survival comparing BRAF-mutant vs
   BRAF-wild-type samples and report the log-rank p-value and median
   survival in each arm. State the n in each arm.
   ```

5. **Stratify by a clinical or demographic variable when the question demands it.** cBioPortal carries clinical attributes (stage, age, sex, and in some studies self-reported ancestry); add the stratum to the survival or frequency query rather than re-running by hand.

6. **State the cohort caveats.** Require the summary to note that frequencies are cohort-specific (not population incidence), that survival comparisons are unadjusted unless you add covariates, and that small subgroup arms make log-rank p-values unstable. Hand the cited table off to a target dossier, a grant aim, or a manuscript figure.

## Why this assembly

Rung 2 of the simplicity ladder. One Claude Skill wraps the entire cBioPortal REST surface — study lookup, mutation/CNA frequency, co-occurrence, TMB, clinical attributes, and survival — so a single component solves the whole problem. Claude Code alone (rung 1) cannot do this: it has no live access to cBioPortal and will confabulate alteration frequencies and p-values. A rung-3 toolbelt buys nothing here — the data all lives in one portal, and the only discipline added beyond the skill (cohort caveats, denominators) is a prompt instruction, not a second tool. Escalate only if the question grows into an autonomous clinical-genomic loop (see *Alternatives considered*).

## Availability

Fully open. The cBioPortal skill is OSS (the SciAgent-Skills collection; the skill's upstream code is AGPL-3.0). The public cBioPortal REST API serves harmonized, openly redistributable cohorts (TCGA PanCancer Atlas and many others) with no key or account. Some institution-hosted cBioPortal instances carry access-controlled studies; this recipe targets the public endpoint only. Any current Claude plan suffices.

## Compute requirements

Laptop-sufficient. Every step is a read-only REST call plus light local Python (frequency tabulation, a log-rank test); a full study profile — lookup, frequency table, TMB, one survival split — completes in seconds to a minute. No GPU. Large studies (full PanCancer cohorts, ~10k samples) return more data per call but stay well within laptop memory.

## Evidence

Reported. No peer-reviewed benchmark documents this *exact* assembly (Claude Code + the SciAgent cBioPortal skill). The closest documented evidence is the **AI-HOPE** family of conversational clinical-genomic agents (Yang, Waldrup & Velazquez-Villarreal, 2025), which build natural-language analysis directly on harmonized cBioPortal data and perform precisely the analyses this recipe targets:

- [AI-HOPE-WNT, *Front. Artif. Intell.* (2025)](https://pubmed.ncbi.nlm.nih.gov/40860720/) integrates cBioPortal/TCGA data and reproduces known associations (WNT-altered EOCRC survival, Hispanic/Latino p=0.0167; non-Hispanic White p=0.0007) while surfacing novel subgroup findings (APC-mutant FOLFOX-treated survival p=0.043) via mutation-frequency, odds-ratio, and Kaplan-Meier modules driven by plain-language queries.
- [AI-HOPE-TP53, *Cancers* (2025)](https://pubmed.ncbi.nlm.nih.gov/40940961/) and [AI-HOPE-JAK-STAT, *Cancers* (2025)](https://pubmed.ncbi.nlm.nih.gov/40723258/) extend the same conversational, cBioPortal-backed pattern to pathway-centric cohort stratification.

These validate the assembly *class* — an LLM driving cBioPortal queries to produce cohort frequency, stratification, and survival reads — not this specific skill. Component evidence: cBioPortal is the consortium-maintained reference for cancer cohort genomics, and the skill wraps its documented REST API faithfully (per the [catalog page](../../catalog/tools/cbioportal-database.html), verified 2026-06-11). The recipe keeps the LLM on retrieval, tabulation, and standard statistics, not causal inference.

## Alternatives considered

- **[Build a target dossier](build-target-dossier.html) (rung-3 toolbelt).** Reach for the dossier when the question is gene-centric across data *types* (disease evidence + protein + structure + dependency) for a single target. This recipe is the complement: cohort-centric across *samples* for a gene set within one cancer. The two pair well — dossier for "what is this gene," cBioPortal for "how does it behave in this tumor's patients."
- **[Fit a survival model](fit-survival-model-to-clinical-outcomes.html) with scikit-survival (rung 2).** Switch to that recipe when you already have an exported covariate table and need multivariable Cox / Random Survival Forest with honest cross-validated concordance. cBioPortal's built-in survival is an unadjusted Kaplan-Meier split — fine for a first read, not for an adjusted prognostic model.
- **AI-HOPE directly (rung 4-ish).** If you need the published disparity-aware, pathway-centric agent with its curated modules, AI-HOPE is purpose-built and openly available on GitHub — but it is a standalone system, not catalogued here. For an interactive cohort read inside Claude Code, the rung-2 skill is simpler and more transparent.
- **Claude Code alone (rung 1).** Insufficient — no live cBioPortal access.

## See also

- [cBioPortal (Claude Skill)](../../catalog/tools/cbioportal-database.html)
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — the gene-centric complement.
- [Fit a survival model to censored clinical outcomes](fit-survival-model-to-clinical-outcomes.html) — for adjusted, validated survival modelling beyond a Kaplan-Meier split.
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — the single-variant sibling.

## Sources

- [cBioPortal skill (`SKILL.md`)](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/genomics-bioinformatics/databases/cbioportal-database/SKILL.md) — verified 2026-06-14 (this run).
- [cBioPortal Web API documentation](https://docs.cbioportal.org/web-api-and-clients/) — verified 2026-06-14 (this run).
- [Yang, Waldrup & Velazquez-Villarreal, "AI-HOPE-WNT," *Front. Artif. Intell.* (2025)](https://pubmed.ncbi.nlm.nih.gov/40860720/) — closest documented cBioPortal-backed conversational-agent evidence.
- [Yang, Waldrup & Velazquez-Villarreal, "AI-HOPE-TP53," *Cancers* (2025)](https://pubmed.ncbi.nlm.nih.gov/40940961/) — pathway-centric cohort stratification on cBioPortal data.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=profile-cancer-cohort-genomics-with-cbioportal&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fprofile-cancer-cohort-genomics-with-cbioportal.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
