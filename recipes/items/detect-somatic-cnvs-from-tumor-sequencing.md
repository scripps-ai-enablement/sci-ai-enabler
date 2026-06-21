---
title: Detect somatic copy-number variants from tumor sequencing
parent: All recipes
grand_parent: Recipes
nav_order: 21
problem_class: Data analysis
subject_areas: [Translational Medicine, Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-06-21
summary: Use the CNVkit Claude Skill to call somatic gene amplifications and deletions from tumor WES/targeted-panel BAMs and export segmented, plotted copy-number profiles.
---

# Detect somatic copy-number variants from tumor sequencing

Point Claude at tumor exome or targeted-panel BAMs; get back normalized, segmented copy-number profiles, called amplifications and deletions per gene, scatter/diagram plots, and VCF/SEG exports — using CNVkit's on-target plus off-target binning to recover genome-wide resolution from capture data.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Translational Medicine, Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

A cancer-genomics analyst with aligned tumor BAMs from whole-exome or a targeted panel needs the somatic copy-number picture: which oncogenes are amplified, which tumor suppressors are deleted, what the segmented log2-ratio profile looks like, and a clean export to hand downstream. Calling CNVs from capture data is harder than from WGS — the target regions are sparse, so a naive read-depth ratio is noisy and biased by GC content, target spacing, and repetitive sequence. CNVkit solves this by also using the nonspecifically captured off-target reads to fill in copy number between targets, but driving it end-to-end (build a pooled reference, bin coverage, correct biases, segment, call, plot, export) is a multi-command CLI workflow with parameters that matter. Solved looks like: name the tumor BAMs and a matched-normal or pooled reference, get a segmented per-gene amplification/deletion call set with QC plots and a SEG/VCF export, with the reference-construction and segmentation choices stated.

## Recommended approach

1. **Install the [CNVkit skill](../../catalog/tools/cnvkit-copy-number.html)** from the SciAgent-Skills collection:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm it appears under `/plugin` → Installed. Claude runs the skill's Python/CLI (`cnvkit.py`, `cnvlib`) locally via Bash; install its declared dependencies on first use.

2. **Build the reference first.** Copy-number calls are only as good as the reference they are normalized against. Tell Claude which mode you are in — matched normal, a panel of normals, or a flat reference — because the choice drives everything downstream:

   ```
   Use the cnvkit skill. I have tumor exome BAMs in tumors/ and 8
   matched-normal BAMs in normals/, aligned to GRCh38, captured with
   the Agilent SureSelect v7 BED (targets.bed). Build a pooled
   copy-number reference from the normals (cnvkit.py batch in
   reference-building mode), report GC/RepeatMasker bias correction,
   and state the antitarget bin size CNVkit chose.
   ```

3. **Bin, correct, and segment the tumors.** Run the per-tumor pipeline against the pooled reference, and pin the segmentation method (CBS is the default; HMM is the alternative for noisier data):

   ```
   For each tumor BAM, run coverage binning against the pooled
   reference, fix biases, and segment with CBS. Report per-sample the
   number of segments, the median absolute deviation of bin-level
   log2 ratios as a noise QC, and flag any sample whose MAD is an
   outlier (likely low purity or degraded input).
   ```

4. **Call gene-level amplifications and deletions.** Translate segments into the calls a tumor board cares about, with a stated threshold:

   ```
   Call integer copy number per segment, then report per gene for
   ERBB2, MYC, EGFR, CCND1, CDKN2A, PTEN, RB1, and TP53: the segment
   log2 ratio, the called copy number, and an amplification/deletion
   label using log2 > 0.6 as amplification and log2 < -1.0 as deep
   deletion. State the thresholds in the output.
   ```

5. **Generate QC plots and exports.** Scatter and diagram plots catch obvious artifacts (whole-arm waves, centromeric spikes); SEG/VCF feeds downstream tools and portals:

   ```
   Produce a genome-wide scatter plot and a chromosome-diagram plot
   per tumor, then export the segments as SEG (for IGV / GISTIC) and
   the gene-level calls as VCF. Save plots and exports to results/.
   ```

6. **State the caveats.** Require the summary to note that copy number from capture data is purity- and ploidy-dependent (low tumor content flattens true amplitudes), that without a matched normal germline CNVs can masquerade as somatic, and that focal calls near capture-bait edges should be confirmed before reporting. Hand the SEG export to a cohort tool ([cBioPortal](profile-cancer-cohort-genomics-with-cbioportal.html)), GISTIC, or a variant report.

## Why this assembly

Rung 2 of the simplicity ladder. One Claude Skill wraps the whole CNVkit pipeline — reference construction, coverage binning, bias correction, segmentation, calling, plotting, and export — so a single component solves the problem. Claude Code alone (rung 1) cannot read BAMs, bin coverage, or run CBS segmentation; it has no copy-number algorithm and would confabulate calls. A rung-3 toolbelt buys nothing for the core task: CNVkit is self-contained, and the only discipline added beyond the skill (noise QC, purity caveats, call thresholds) is a prompt instruction, not a second tool. Escalate only if you need population-control deep-WGS CNV calling (where GATK gCNV is the better engine) or an autonomous tumor-board pipeline.

## Availability

Fully open. The CNVkit skill is OSS (Apache-2.0, in the SciAgent-Skills collection); CNVkit itself is Apache-2.0. No account, key, or subscription. Any current Claude plan suffices. The only inputs you supply are your own BAMs and capture BED — nothing is uploaded to a third party; the skill runs locally.

## Compute requirements

Workstation-class, CPU-bound (no GPU strictly required despite the tier label — see note). Coverage binning over exome BAMs is I/O- and CPU-heavy: budget several GB of RAM and a few minutes per sample on a multi-core workstation; a panel-of-normals reference build over 8 normals takes longer (tens of minutes). SEG/VCF exports and plots are light. Disk: BAMs dominate (tens of GB each for WES). No GPU is used by CNVkit; the tier is set to workstation because realistic tumor BAM sets exceed comfortable laptop memory and storage. For a small targeted panel (a few hundred genes), a laptop with adequate disk is sufficient.

## Evidence

Reported. No peer-reviewed benchmark documents this *exact* assembly (Claude Code + the SciAgent CNVkit skill). The underlying tool is the field-standard engine for copy-number detection from targeted/exome sequencing: [Talevich, Shain, Botton & Bastian, "CNVkit: Genome-Wide Copy Number Detection and Visualization from Targeted DNA Sequencing," *PLOS Comput. Biol.* (2016)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004873) introduced the on-target-plus-off-target binning approach that lets capture data recover genome-wide copy number, and the method is widely used in clinical and research tumor pipelines. The Claude-skill wrapper faithfully exposes CNVkit's documented `batch`/`reference`/`segment`/`call`/`export` commands (per the [catalog page](../../catalog/tools/cnvkit-copy-number.html), verified 2026-06-11). The recipe keeps the LLM on orchestration, QC, and reporting — not on inventing the segmentation, which CNVkit's CBS/HMM algorithms perform.

## Alternatives considered

- **[Profile a cancer cohort's genomics with cBioPortal](profile-cancer-cohort-genomics-with-cbioportal.html) (rung 2).** Reach for that when you want *cohort-level* CNA frequencies from harmonized public studies, not per-sample calls from your own BAMs. This recipe produces the per-tumor segments; cBioPortal answers "how often is this amplified across a cohort." They pair — call your samples here, contextualize against TCGA there.
- **GATK gCNV / deep WGS (rung 2–3, not catalogued).** For deep whole-genome data with a large panel of population controls, GATK's germline/somatic CNV callers exploit even coverage that CNVkit's off-target trick is designed to compensate for. CNVkit is the better choice precisely when you have *targeted or exome* data. GATK gCNV is not in the catalog today.
- **Claude Code alone (rung 1).** Insufficient — no read access to BAMs and no copy-number algorithm.

## See also

- [CNVkit (Claude Skill)](../../catalog/tools/cnvkit-copy-number.html)
- [Profile a cancer cohort's genomics with cBioPortal](profile-cancer-cohort-genomics-with-cbioportal.html) — cohort-level CNA context for your calls.
- [Interpret a clinical variant from a natural-language query](interpret-clinical-variant.html) — the single-variant (SNV/indel) sibling.

## Sources

- [CNVkit skill (`SKILL.md`)](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/genomics-bioinformatics/variant/cnvkit-copy-number/SKILL.md) — verified 2026-06-21 (this run).
- [Talevich et al., "CNVkit," *PLOS Comput. Biol.* (2016)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004873) — the canonical CNVkit method paper; verified 2026-06-21 (this run).
- [CNVkit documentation (readthedocs)](https://cnvkit.readthedocs.io/) — command reference for `batch`/`segment`/`call`/`export`.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=detect-somatic-cnvs-from-tumor-sequencing&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdetect-somatic-cnvs-from-tumor-sequencing.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
