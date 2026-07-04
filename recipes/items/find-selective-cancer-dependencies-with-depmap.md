---
title: Find selective genetic dependencies for a cancer context with DepMap
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Hypothesis generation
subject_areas: [Molecular and Cellular Biology, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-04
summary: Use the DepMap skill to mine genome-wide CRISPR screens for genes selectively essential in a cancer lineage or genotype, corrected for copy-number bias.
---

# Find selective genetic dependencies for a cancer context with DepMap

Give Claude Code a cancer context — a lineage, a driver mutation, or an expression state — and get back a ranked, copy-number-corrected list of genes that cancer cell lines with that context depend on but other lines do not, anchored to the exact DepMap release you queried.

| | |
|---|---|
| **Problem class** | Hypothesis generation |
| **Subject areas** | Molecular and Cellular Biology, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have a cancer context you care about — a lineage (e.g., acute myeloid leukemia), a driver genotype (e.g., *KRAS*-mutant), a fusion (e.g., *SS18::SSX*), or an expression state (e.g., low *ATP1B1*) — and you want candidate targets: genes whose knockout kills cells *in that context* while sparing others. This "selective genetic dependency" question is the standard first move in modern target discovery, and the reference resource is the Broad's Cancer Dependency Map (DepMap): genome-wide CRISPR-Cas9 Chronos gene-effect scores across ~1,000 cancer cell lines, paired with mutation, copy-number, and expression matrices.

The mechanics are a group contrast over the `CRISPRGeneEffect` matrix, but the footguns are what sink naive analyses: reporting pan-essential genes (ribosome, proteasome — essential everywhere, useless as selective targets); mistaking a copy-number artifact (CRISPR cutting amplified regions looks like dependency) for real biology; ignoring multiple-testing burden across ~18,000 genes; and — the reproducibility killer — not recording which quarterly DepMap release the scores came from, so the ranking can't be re-checked when the data updates. "Solved" looks like: name the context, get back a `dependencies.csv` ranked by selective effect size with FDR-corrected significance and a copy-number flag, plus a provenance record naming the exact DepMap release.

## Recommended approach

1. **Install the [DepMap skill](../../catalog/tools/depmap.html).** It resolves cell lines by DepMap ID, downloads the standard DepMap files locally, computes biomarker associations with multiple-testing correction, and adjusts for copy-number effects. Follow the catalog page's `npx skills add` (or manual clone) steps.

2. **Pin the DepMap release.** The skill pulls `CRISPRGeneEffect.csv`, `OmicsExpressionProteinCodingGenesTPMLogp1.csv`, `OmicsSomaticMutationsMatrixDamaging.csv`, `OmicsCNGene.csv`, and `sample_info.csv` (a few hundred MB total, cached after first use). DepMap ships quarterly (e.g., `24Q4`); **record the release label** and the `sha256` of each downloaded matrix. These are your pinned inputs — a dependency call means nothing without the release it came from.

3. **Define the context as two cell-line groups.** Have the agent partition lines from `sample_info` / the omics matrices into a **context group** (e.g., AML lineage, or lines with a damaging *KRAS* mutation, or lines below a chosen *ATP1B1* TPM percentile) and a **background group** (the rest). Confirm both groups are large enough (a handful of lines per group gives noisy contrasts; aim for ≥ 10 where possible).

4. **Run the contrast into a committed script.** A prompt:

   ```
   Using the depmap skill, write me a script find_dependencies.py that:
     1. Loads CRISPRGeneEffect, sample_info, the mutation matrix, the
        expression matrix, and OmicsCNGene from the pinned local DepMap
        release.
     2. Splits cell lines into a context group and a background group
        by the criterion I give (lineage == "AML"), reporting the n in
        each group.
     3. For every gene, computes the mean Chronos gene-effect in each
        group, the difference (selective effect = context mean minus
        background mean; more negative = more selectively essential),
        and a two-sided Mann-Whitney/t contrast; applies Benjamini-
        Hochberg FDR across all genes.
     4. Drops pan-essential genes (background mean Chronos <= -0.5) so
        only *selective* dependencies survive, and adds a
        copy_number_flag column when the context group's mean CN at that
        gene is elevated (possible CN artifact, not real dependency).
     5. Writes dependencies.csv sorted by selective effect: gene,
        context_mean, background_mean, selective_effect, p, fdr,
        copy_number_flag, n_context, n_background.
     6. Writes provenance.json: DepMap release label, each matrix
        sha256, the context/background definition, the pan-essential
        and CN thresholds, run date, and model id.
   Commit find_dependencies.py; do not paste the ranking back as prose
   I can't audit.
   ```

   Pin the environment with a `requirements.txt` (`pandas`, `numpy`, `scipy`, `statsmodels`). Keep `find_dependencies.py`, the pinned env, and `provenance.json` under version control alongside the DepMap release label and matrix hashes.

5. **Read the ranking critically.** Top hits with a set `copy_number_flag` are suspect — inspect the CN track before believing them. A selective dependency is a *hypothesis*, not a validated target: cross-check each candidate against known biology (is it a paralog of a gene silenced in the context, like the *ATP1B3*/*ATP1B1* pair? a lineage transcription factor? a synthetic-lethal partner of the driver?) and against tractability before committing wet-lab resources.

6. **Re-run and hand off.** Because the release, group definitions, and thresholds are pinned in `provenance.json`, re-running `find_dependencies.py` reproduces the ranking until you deliberately bump the DepMap release (which the provenance record makes visible). A shortlisted gene flows straight into the [target-dossier recipe](build-target-dossier.html) for the full disease/structure/annotation readout, or into the [sgRNA-design recipe](design-crispr-sgrnas-for-a-gene-knockout.html) to plan the validation knockout.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill does the whole job. Plain Claude Code (rung 1) could in principle download the DepMap files and write the contrast, but the skill encodes the two things beginners get wrong: cell-line ID resolution (names are ambiguous; DepMap IDs are canonical) and copy-number correction of essentiality scores. Rung 3+ is unnecessary: a selective-dependency contrast over one pinned matrix is a single well-bounded step. This recipe is context-in / genes-out; contrast it with the [target-dossier recipe](build-target-dossier.html) (gene-in / evidence-out, which uses DepMap as one of four lookups) and the [prioritize-targets recipe](prioritize-targets-within-a-disease.html) (disease-in, Open Targets association scores rather than functional dependency).

## Availability

Fully open. The DepMap skill is community OSS; the underlying DepMap data is released under a permissive public license for academic and commercial use. All computation runs locally on the downloaded matrices — no account, no API key. First download is a few hundred MB; cache it.

## Compute requirements

Laptop-sufficient. The CRISPR gene-effect matrix is ~1,000 lines × ~18,000 genes; a genome-wide group contrast plus BH correction runs in well under a minute on a modern laptop with 8 GB RAM once the files are cached. No GPU. The only heavy step is the one-time ~200–400 MB download of the standard DepMap files.

## Evidence

Reported. Mining DepMap for selective/context-specific dependencies as therapeutic-target hypotheses is a heavily documented, routine practice in cancer biology. Recent peer-reviewed examples all run exactly this contrast — partition cell lines by context, rank selectively essential genes, then validate: *ATP1B3* as a paralog-related dependency in AML lines with low *ATP1B1* ([Schneider et al., *Cancer Res.* 2024](https://doi.org/10.1158/0008-5472.CAN-23-3560)); *KIF18A* as a vulnerability of chromosomally unstable lines, mined from DepMap and taken to a clinical-stage inhibitor ([Phillips et al., *Nat. Commun.* 2025](https://doi.org/10.1038/s41467-024-55300-z)); *SUMO2* as a synovial-sarcoma dependency from mining DepMap by *SS18::SSX* context ([Iyer et al., *EMBO J.* 2025](https://doi.org/10.1038/s44318-025-00526-w)). The copy-number correction and Chronos scoring this recipe relies on follow the DepMap methodology ([Behan et al., *Nature* 2019](https://doi.org/10.1038/s41586-019-1103-9); [Dempster et al., *Nat. Commun.* 2021](https://doi.org/10.1038/s41467-021-21898-7)).

No head-to-head benchmark of the *agent-driven* DepMap-skill assembly versus a hand-written contrast is published — the skill buys cell-line resolution, copy-number correction, and a pinned-release provenance file, not a new method. The DepMap resource and the contrast are the validated components; the recipe's contribution is making the dependency call reproducible.

## Alternatives considered

- **The DepMap web portal (no agent).** The portal's Data Explorer answers single-gene and single-lineage questions interactively and is the right tool for a quick eyeball. Reach for this recipe when the contrast is custom (an expression-percentile split, a fusion context) or when the ranking needs to go in a reproducible record with a pinned release.
- **Plain Claude Code, no skill (rung 1).** Workable if you are comfortable resolving DepMap IDs and applying the copy-number correction yourself. The skill encodes both, which is the usual failure point.
- **Full target dossier (rung 3).** Once you have a shortlisted gene, the [target-dossier recipe](build-target-dossier.html) adds Open Targets disease evidence, UniProt annotation, and an AlphaFold structure. Reach for it *after* this recipe surfaces the candidate — different question, gene-in rather than context-in.
- **Biomni (rung 4).** An autonomous system with DepMap-style data wired in; reach for it only when the dependency scan is one step of a larger autonomous pipeline. For a one-shot selective-dependency contrast the single skill is simpler and more transparent.

## See also

- [DepMap (Claude Skill)](../../catalog/tools/depmap.html) — the skill this recipe drives.
- [Build a target dossier](build-target-dossier.html) — the gene-in follow-on that profiles a shortlisted dependency.
- [Prioritize targets within a disease](prioritize-targets-within-a-disease.html) — disease-level, association-based target ranking (Open Targets).
- [Design CRISPR sgRNAs for a gene knockout](design-crispr-sgrnas-for-a-gene-knockout.html) — plan the validation knockout of a candidate dependency.

## Sources

- [Schneider et al., "Targeting the Sodium-Potassium Pump as a Therapeutic Strategy in Acute Myeloid Leukemia," *Cancer Res.* 84 (2024)](https://doi.org/10.1158/0008-5472.CAN-23-3560) — DepMap-mined paralog dependency (*ATP1B3*/*ATP1B1*); verified 2026-07-04 (this run).
- [Phillips et al., "Targeting chromosomally unstable tumors with a selective KIF18A inhibitor," *Nat. Commun.* 16 (2025)](https://doi.org/10.1038/s41467-024-55300-z) — DepMap-mined dependency taken to a clinical inhibitor; verified 2026-07-04 (this run).
- [Iyer et al., "Targeting SUMO2 reverses aberrant epigenetic rewiring driven by SS18::SSX fusion oncoproteins," *EMBO J.* (2025)](https://doi.org/10.1038/s44318-025-00526-w) — DepMap-mined fusion-context dependency; verified 2026-07-04 (this run).
- [Dempster et al., "Integrated cross-study datasets of genetic dependencies in cancer," *Nat. Commun.* 12 (2021)](https://doi.org/10.1038/s41467-021-21898-7) — Chronos scoring and CN-bias correction methodology; verified 2026-07-04 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=find-selective-cancer-dependencies-with-depmap&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ffind-selective-cancer-dependencies-with-depmap.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
