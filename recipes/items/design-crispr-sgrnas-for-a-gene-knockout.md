---
title: Design CRISPR sgRNAs for a gene knockout
parent: All recipes
grand_parent: Recipes
nav_order: 8
problem_class: Experimental design
subject_areas: [Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-27
summary: Use the sgRNA Design skill to pick CRISPR-Cas9 knockout guides for a gene — preferring validated/CRISPick guides, falling back to Rule Set 2 + CFD de novo rules.
---

# Design CRISPR sgRNAs for a gene knockout

Tell Claude Code which gene you want to knock out and get back a short, ranked panel of Cas9 sgRNAs — drawn from validated Addgene/CRISPick guides where they exist and from on-target/off-target scoring rules where they don't — captured as a committed design file you can order from.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Designing CRISPR-Cas9 knockout guides is a routine but error-prone bench task. A guide has to land in an early, constitutive coding exon, sit next to a valid PAM, cut efficiently (on-target activity), and avoid cutting elsewhere in the genome (off-target risk). Picking by eye — or grabbing the first guide a tool spits out — wastes a transfection and a sorting run when the guide turns out to be inefficient or promiscuous. The hard part is doing this defensibly: using the field-standard scoring models, preferring guides that have already been experimentally validated, and keeping a record of *why* each guide was chosen.

"Solved" looks like: name the gene (and organism), get back 3–6 candidate guides with their target exon, PAM, strand, on-target score, and off-target assessment, plus a one-line provenance for each (validated library guide vs de-novo-scored), saved as a versioned design file you order oligos from and cite in the methods.

## Recommended approach

1. **Install the [sgRNA Design skill](../../catalog/tools/sgrna-design-guide.html).** It ships in the [SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) collection — clone once and load as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm the sgRNA design skill appears under `/plugin` → Installed.

2. **State the target precisely.** Give the gene symbol, the organism/genome build, the editing modality (knockout / CRISPRko here), and any constraints (a specific exon, an existing Cas9 variant/PAM). Ambiguity here is the most common cause of a wrong-genome guide.

3. **Let the skill walk its three tiers, and capture the result to a committed file.** The skill is explicitly tiered — prefer the strongest evidence available before designing from scratch:

   ```
   Use the sgRNA design skill to design CRISPRko guides for <GENE>
   in <organism, genome build>. Walk the tiers in order:
     1. validated guides from Addgene libraries if the gene is covered,
     2. CRISPick pre-computed picks for this genome if available,
     3. de novo design rules (Rule Set 2 / Azimuth on-target,
        CFD off-target) only if neither library covers the gene.
   Write the result to guides.csv with one row per guide:
     sequence, PAM, target_exon, strand, on_target_score,
     off_target_assessment, source_tier (validated/CRISPick/de_novo).
   Record the genome build, the skill version, and each source
   database/version in provenance.json.
   Then summarize: which tier each guide came from and why.
   ```

   Pin the environment and commit `guides.csv`, the pinned env, and `provenance.json`. The recorded genome build and source tier are what make the design auditable — a guide is only meaningful against a stated genome — see the [reproducibility guide](../../guide/advanced/reproducibility.html).

4. **Sanity-check before ordering.** Confirm each guide sits in an early, constitutive coding exon (not a 3' exon or an alternatively-spliced one), that the PAM matches your Cas9 variant, and that the off-target assessment is acceptable for your application (a pooled screen tolerates more risk than a clonal cell line). Drop guides that fail; do not edit scores by hand.

5. **Order and keep the record.** `guides.csv` is the artifact you add cloning overhangs to, order as oligos, and cite. Keep it under version control with the experiment.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill covers the whole decision tree. Guide design is a single well-bounded task, but the value is in the tiered logic and the scoring models (Rule Set 2 on-target, CFD off-target) and the validated-library lookups, none of which plain Claude Code (rung 1) can reproduce credibly from prompt instructions — it would invent guide sequences and scores. Rung 3+ is unnecessary: one gene in, one ranked panel out. The skill deliberately prefers validated > pre-computed > de novo so you only design from scratch when you must.

## Availability

Fully open. The sgRNA design skill is open-source (SciAgent-Skills, CC BY 4.0 wrapper). The scoring rules and validated-library/CRISPick data it draws on are public. No account or API key is required for the design step. (CRISPick's public web tool may rate-limit; the skill's de novo tier is fully local.)

## Compute requirements

Laptop-sufficient. Designing guides for a single gene is a CPU-only, seconds-to-minutes task; the validated/CRISPick lookups are small queries and the de novo scoring is lightweight. No GPU. Designing for a list of many genes (a small library) is still laptop-scale as a loop.

## Evidence

Reported. The de novo tier rests on the field-standard scoring models: Rule Set 2 / Azimuth for on-target activity and the CFD score for off-target risk, developed on >4,000 sgRNAs and validated in genome-wide screens ([Doench et al., *Nature Biotechnology* 2016](https://www.nature.com/articles/nbt.3437)). These models underpin CRISPick, CRISPOR, and CHOPCHOP and are the de facto standard for Cas9 knockout guide selection. The validated and CRISPick tiers reuse experimentally screened guides directly.

No head-to-head benchmark of this *agent-driven* tiered assembly versus running CRISPick by hand is published — the skill buys the tiered logic, a committed design file, and recorded provenance, not a new scoring method. That gap is why this recipe is `Reported`, not `Validated`.

## Alternatives considered

- **CRISPick / CRISPOR / CHOPCHOP web tools (no skill).** These hosted designers are the simplest path for a one-off and are widely trusted — reach for them directly if you just need a couple of guides for one gene and don't need a committed record. The skill is worth it when you want the tiered preference (validated → pre-computed → de novo) applied automatically and the result captured as a versioned design file with provenance.
- **Plain Claude Code (rung 1).** Rejected: without the skill, the model cannot reliably produce real guide sequences, on-target scores, or off-target assessments — it would hallucinate them. Guide design is precisely where you must not run rung 1.
- **A full design + screen + analysis harness (rung 3+).** If you're building a pooled genome-wide screen and need to also analyze the readout, that's a larger pipeline (library design + sequencing + MAGeCK-style analysis) — out of scope here; this recipe stops at the designed guide panel for a single gene or short gene list.

## See also

- [sgRNA Design (Claude Skill)](../../catalog/tools/sgrna-design-guide.html) — three-tiered CRISPR guide design.
- [Annotate and verify an engineered plasmid construct](annotate-and-verify-a-plasmid-construct.html) — verify the guide-expression vector you clone into.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the committed-artifact pattern this recipe follows.

## Sources

- [Doench, Fusi et al., "Optimized sgRNA design to maximize activity and minimize off-target effects of CRISPR-Cas9," *Nature Biotechnology* 34:184–191](https://www.nature.com/articles/nbt.3437) — published 2016; verified 2026-06-27 (this run).
- [Broad GPP / CRISPick sgRNA scoring documentation](https://portals.broadinstitute.org/gpp/public/software/sgrna-scoring-help) — Rule Set 2 / Azimuth + CFD scoring; verified 2026-06-27 (this run).
- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) — sgRNA design skill source; verified 2026-06-27 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=design-crispr-sgrnas-for-a-gene-knockout&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdesign-crispr-sgrnas-for-a-gene-knockout.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
