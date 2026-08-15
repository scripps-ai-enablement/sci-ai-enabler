---
title: Compare bulk TCR/BCR repertoires across samples from raw immunosequencing reads
parent: All recipes
grand_parent: Recipes
nav_order: 6
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Proposed
complexity: Multi-tool harness
availability: Institutional access
compute_requirements: Workstation with GPU
last_verified: 2026-08-15
summary: Assemble clonotypes with MiXCR, normalize samples to a common depth with VDJtools, then compare diversity, clonality and overlap as a committed pipeline.
---

# Compare bulk TCR/BCR repertoires across samples from raw immunosequencing reads

Turn a cohort of bulk TCR/BCR sequencing libraries into depth-normalized diversity, clonality, overlap and segment-usage tables — with the two comparisons that silently break repertoire studies (chemistry preset and sequencing depth) fixed as gates rather than defaults.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Proposed |
| **Complexity** | Multi-tool harness |
| **Availability** | Institutional access |
| **Compute** | Workstation with GPU |

## Problem

You have bulk immunosequencing FASTQs — a vaccine trial's pre/post timepoints, tumor versus adjacent tissue, a treatment arm versus a control arm — and the question is comparative: is the repertoire more clonal after treatment, do responders share clonotypes, which V segments shifted. This is the path most vaccine and immuno-oncology labs actually run, and it is not the single-cell path: there are no barcodes tying receptors to phenotypes, the input is millions of amplicon reads, and every conclusion is a *between-sample* claim.

That is what makes it hard. Two artifacts produce publishable-looking, wrong answers. First, sequencing depth: richness rises monotonically with reads, so a "more diverse post-vaccination repertoire" is the expected result of sequencing that library deeper, and nothing in the output table shows it. Second, PCR and sequencing error: without unique molecular identifiers, spurious singleton clonotypes inflate diversity enormously, and multiplex-primer amplification distorts the clonal frequencies you are comparing. "Solved" looks like a committed pipeline that assembles clonotypes under a declared chemistry preset, downsamples every sample to one recorded depth before any statistic is computed, and emits diversity/clonality/overlap tables plus a provenance record naming every version, preset, depth and seed.

## Recommended approach

1. **Install the three cataloged skills.** [MiXCR Analysis](../../catalog/tools/mixcr-analysis.html) (reads → clonotypes), [VDJtools Analysis](../../catalog/tools/vdjtools-analysis.html) (normalization, diversity, overlap, segment usage) and [Repertoire Visualization](../../catalog/tools/repertoire-visualization.html) (figures). All three live in the same bioSkills category, so one install covers them:

   ```
   git clone https://github.com/GPTomics/bioSkills
   cd bioSkills
   ./install-claude.sh --categories "tcr-bcr-analysis"
   ```

   Install and activate MiXCR itself when prompted (`mixcr activate-license`, or the `MI_LICENSE` environment variable) — see **Availability** before you do.

2. **Write down the chemistry before writing any code.** The preset is the single input the agent cannot infer from the FASTQs: 5'RACE/template-switch versus multiplex-primer amplicon (floating versus rigid V/J boundaries), RNA versus gDNA, UMI versus no-UMI, and the kit if it is a commercial one (Takara, NEBNext, QIAseq, BD). Put it in a `config.yaml` alongside the sample sheet. A mismatched preset does not error — it trims CDR3 boundaries wrongly and you get a clonotype table that looks fine.

3. **Have the skills write a committed pipeline, not answers.** A prompt:

   ```
   Use the mixcr-analysis, vdjtools-analysis and
   repertoire-visualization skills to write me a pipeline under
   repertoire/ that runs from config.yaml and samples.tsv:

     01_assemble.sh — MiXCR with the preset named in config.yaml,
       one sample per FASTQ pair. Fail loudly if the preset is not
       set explicitly. Export AIRR TSV plus exportQc alignment and
       chain-usage reports. Write per-sample read counts, alignment
       rate, and (if UMI) reads-per-UMI to assembly_qc.csv.

     02_normalize.sh — VDJtools Convert, then FilterNonFunctional
       into TWO outputs: functional clonotypes for all downstream
       statistics, and the non-functional set kept as a separate
       table (do not silently drop it). Then DownSample every
       sample to the SAME depth, set as a literal in config.yaml
       (the smallest sample that passed QC), with the RNG seed
       recorded. Repeat the downsampling N times and carry the
       spread. Abort if any sample is below the target depth.

     03_stats.sh — on the downsampled tables only, per chain
       separately (never pool TRB with TRA or IGH):
       CalcDiversityStats reporting the Hill profile at q=0, q=1,
       q=2; clonality; CalcPairwiseDistances with BOTH Morisita-
       Horn and Jaccard; CalcSegmentUsage; CalcSpectratype.

     04_figures.R — rarefaction/extrapolation curves with all
       samples on shared x-values, an overlap heatmap, a V-J chord
       diagram, and clonal-space stratification.

     provenance.json — MiXCR version and reference library version,
       VDJtools version, R/iNEXT/circlize versions, the preset
       string, the downsample depth and seed, input FASTQ sha256s,
       run date, and model id.

   Commit the scripts and config.yaml. Do not paste summary numbers
   back as prose I cannot re-derive from the tables.
   ```

   Pin the environment (`environment.yml` for the Java/R side, `requirements.txt` for Python) and keep the scripts, `config.yaml`, `samples.tsv`, the emitted tables and `provenance.json` under version control. The FASTQs stay outside the repo; their hashes are in `provenance.json`.

4. **Gate on `assembly_qc.csv` before you look at a single diversity number.** A sample with a low alignment rate or a mean reads-per-UMI near 1 has not been sequenced deeply enough for its UMI families to correct anything, and its apparent richness is largely error. Drop it or resequence it — do not downsample your way around it. If the library has no UMIs at all, say so on the figures and treat q=0 richness as uninterpretable (see **Evidence**).

5. **Read the Hill profile, not a single diversity number.** Report q=0 (richness), q=1 (Shannon) and q=2 (inverse Simpson) together at the recorded common depth: q=0 is the most error- and depth-sensitive, q=2 the most robust, and a difference that appears only at q=0 is a claim about singletons, which is a claim about your PCR. Same discipline for overlap — Morisita-Horn is frequency-weighted and depth-robust, Jaccard is presence/absence and moves with depth, so a conclusion that holds on Jaccard but not Morisita-Horn is usually a depth story.

6. **State what the numbers are about.** Every statistic is the diversity of *your sample at the recorded depth*, not the diversity of the subject's repertoire — a blood draw cannot capture it, and extrapolating to the true total is a known-hard problem where standard estimators are biased. Phrase results as differences between equally-sampled libraries, which is exactly what the pipeline supports.

## Why this assembly

Rung 3, and the escalation is forced. Rung 2 fails because the two halves are genuinely different jobs with different runtimes and different failure modes: MiXCR is a licensed Java aligner turning gigabytes of reads into clonotypes under a chemistry-specific preset, while VDJtools is a statistics layer whose correctness depends entirely on normalization decisions made *after* assembly. The bioSkills authors split them for the same reason. Visualization is the third component rather than an afterthought because the depth-robustness argument is made in the figures — rarefaction curves compared at shared x-values are what let a reader check the normalization instead of trusting it. Rung 4 is unwarranted: this is a fixed pipeline with a known shape, not an open-ended research problem needing an autonomous system.

## Availability

Institutional access. The three skills are MIT-licensed and VDJtools/immunarch/R are open source, but **MiXCR is not**: MiLaboratories states it is free for academic users with no commercial funding, and commercial use requires a paid license (verified 2026-08-15). You must request a key and activate it (`mixcr activate-license`, `MI_LICENSE`, or `~/.mi.license`) — plan for that before scheduling cohort runs, and clear it with your tech-transfer office if the work has industry funding. Everything runs locally, which matters because bulk immunosequencing usually comes from consented human subjects and sits inside an IRB and data-governance regime; keep the FASTQs on institution-controlled storage.

## Compute requirements

Workstation- or server-class, no GPU — nothing in this pipeline benefits from one. MiXCR alignment is the cost: budget 8–32 GB RAM and expect tens of minutes to a couple of hours per sample for a deep bulk library (10–50M read pairs) on 8–16 cores, scaling roughly linearly with reads. A 20-sample cohort is therefore an overnight job or a cluster array, not a coffee break. The VDJtools stage is minutes for the whole cohort, and repeating the downsampling N times costs almost nothing — do it. Disk is the quiet constraint: intermediate `.vdjca`/`.clns` files are comparable in size to the inputs, so plan for roughly 2–3× the FASTQ footprint.

## Evidence

Proposed. No documented attempt at this agent-driven three-skill assembly is known. The components are the field's standards: MiXCR is the reference clonotype assembler ([Bolotin et al., *Nature Methods* 2015](https://doi.org/10.1038/nmeth.3364)) and VDJtools the reference post-analysis suite, demonstrated across cohorts of unrelated donors, twins and multiple-sclerosis patients ([Shugay et al., *PLoS Comput. Biol.* 2015](https://pubmed.ncbi.nlm.nih.gov/26606115/)).

The two gates this recipe enforces are the well-evidenced part. On error and UMIs: using synthetic spike-ins, multiplex-PCR library preparation yielded antibody frequencies with **only 42–62% accuracy**, and uncorrected sequencing/PCR error **overestimated diversity by up to 5000-fold**; UID tagging combined with a bias-correcting pipeline restored frequency accuracy to up to 99% and error correction to 98–100% ([Khan et al., *Science Advances* 2016](https://pubmed.ncbi.nlm.nih.gov/26998518/)). On depth: the canonical demonstration that TCR diversity changes with age had to be run as *deep and precisely normalized* profiling, reporting diversity per 10<sup>6</sup> T cells rather than raw counts ([Britanova et al., *J. Immunol.* 2014](https://pubmed.ncbi.nlm.nih.gov/24510963/)). And on step 6's caution: a review of richness estimators applied to T-cell repertoires found existing approaches have significant shortcomings and **frequently underestimate true TCR diversity**, because the frequency distribution is heavily skewed and cannot be captured in a blood sample ([Laydon, Bangham & Asquith, *Phil. Trans. R. Soc. B* 2015](https://pubmed.ncbi.nlm.nih.gov/26150657/)).

## Alternatives considered

- **Single-cell instead of bulk.** If your samples were run as paired 5' GEX + VDJ, use [Analyze a single-cell TCR repertoire alongside gene expression](analyze-single-cell-tcr-repertoire.html) — it answers a different question (which transcriptional states are clonally expanded) and needs no depth normalization of this kind. Bulk buys you orders of magnitude more clonotypes per sample and no phenotype.
- **B cells and affinity maturation.** For IGH libraries where the question is somatic hypermutation and lineage structure rather than diversity comparison, [Reconstruct B-cell clonal lineages from AIRR-seq](reconstruct-bcr-clonal-lineages.html) is the right page — clonal assignment there needs a data-driven SHM threshold, which this pipeline's exact-clonotype model does not provide. Assembling IGH reads with step 1 and handing the AIRR export to that recipe is a legitimate combination.
- **Stop after MiXCR (rung 2).** If you only need one sample's clonotype table — say, to find the dominant clone in a leukemia sample — skip VDJtools entirely. The normalization machinery exists solely to make *between-sample* claims safe.
- **Antigen specificity.** Once expanded clonotypes are in hand, [Annotate TCR antigen specificity by clustering and database lookup](annotate-tcr-specificity-by-clustering.html) is the downstream step.

## See also

- [MiXCR Analysis (bioSkills)](../../catalog/tools/mixcr-analysis.html) — clonotype assembly from raw reads.
- [VDJtools Analysis (bioSkills)](../../catalog/tools/vdjtools-analysis.html) — normalization, diversity, overlap, segment usage.
- [Repertoire Visualization (bioSkills)](../../catalog/tools/repertoire-visualization.html) — rarefaction curves, chord diagrams, overlap heatmaps.
- [Analyze a single-cell TCR repertoire alongside gene expression](analyze-single-cell-tcr-repertoire.html) — the single-cell counterpart.
- [Reconstruct B-cell clonal lineages from AIRR-seq](reconstruct-bcr-clonal-lineages.html) — the B-cell lineage path downstream of assembly.
- [Annotate TCR antigen specificity by clustering and database lookup](annotate-tcr-specificity-by-clustering.html) — specificity follow-up on expanded clonotypes.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the artifact pattern this recipe follows.

## Sources

- [Bolotin et al., "MiXCR: software for comprehensive adaptive immunity profiling," *Nature Methods* 12:380–381](https://doi.org/10.1038/nmeth.3364) — published 2015; record verified via Europe PMC 2026-08-15 (this run).
- [Shugay et al., "VDJtools: Unifying Post-analysis of T Cell Receptor Repertoires," *PLoS Comput. Biol.* 11:e1004503](https://pubmed.ncbi.nlm.nih.gov/26606115/) — published 2015; verified 2026-08-15 (this run).
- [Khan et al., "Accurate and predictive antibody repertoire profiling by molecular amplification fingerprinting," *Science Advances* 2:e1501371](https://pubmed.ncbi.nlm.nih.gov/26998518/) — published 2016; verified 2026-08-15 (this run).
- [Britanova et al., "Age-related decrease in TCR repertoire diversity measured with deep and normalized sequence profiling," *J. Immunol.* 192:2689–2698](https://pubmed.ncbi.nlm.nih.gov/24510963/) — published 2014; verified 2026-08-15 (this run).
- [Laydon, Bangham & Asquith, "Estimating T-cell repertoire diversity: limitations of classical estimators and a new approach," *Phil. Trans. R. Soc. B* 370:20140291](https://pubmed.ncbi.nlm.nih.gov/26150657/) — published 2015; verified 2026-08-15 (this run).
- [`milaboratory/mixcr`](https://github.com/milaboratory/mixcr) — license terms (free for academic users with no commercial funding; commercial license required) and activation methods; verified 2026-08-15 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=compare-bulk-tcr-repertoires-across-samples&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fcompare-bulk-tcr-repertoires-across-samples.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
