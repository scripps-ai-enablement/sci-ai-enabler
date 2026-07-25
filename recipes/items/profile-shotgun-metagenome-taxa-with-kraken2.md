---
title: Profile shotgun metagenome taxa with Kraken2 and Bracken
parent: All recipes
grand_parent: Recipes
nav_order: 18
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-07-25
summary: Use the Kraken2 skill to classify shotgun metagenomic reads to taxa and re-estimate abundances with Bracken, with database and confidence-threshold choices recorded.
---

# Profile shotgun metagenome taxa with Kraken2 and Bracken

Hand Claude Code a set of quality-trimmed, host-depleted shotgun metagenomic FASTQs and a reference database, and get back per-sample Kraken2 read classifications, Bracken species-level abundance estimates, and a merged abundance table — with the database release and confidence threshold pinned so the "who is there" call is auditable.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

After a shotgun metagenomics run — gut, skin, environmental, or clinical — the first analytical question is "who is there?": classify each read to a taxon and estimate community composition. Kraken2 (k-mer minimizer + lowest-common-ancestor matching) plus Bracken (Bayesian rank-level abundance re-estimation) is the field-standard fast path. The mechanics are stable, but the result is dominated by two choices people make silently and then forget: which reference database, and what confidence threshold. Report neither and your species table is not reproducible or comparable to anyone else's.

The footguns are specific. The database — not the algorithm — bounds what can be detected; a genus absent from the database is invisible, and a small database inflates false-negatives while a huge one raises memory needs. Kraken2's read *classification* is not the same as *abundance*: raw read counts are biased by genome size and copy number, which is exactly what Bracken corrects. Low confidence thresholds over-assign fine-rank labels (a well-documented false-positive source, worse for long reads); high thresholds on a small database can leave nearly everything unclassified. "Solved" looks like: point the agent at your FASTQs and a named database, get back `bracken_species.tsv` per sample plus a merged matrix, and a provenance record naming the database release, the confidence threshold, and the tool versions.

## Recommended approach

1. **Install the [Kraken2 Metagenomic Classification skill](../../catalog/tools/kraken-classification.html).** Clone the bioSkills repo and copy the one skill (`cp -r bioSkills/metagenomics/kraken-classification ~/.claude/skills/`), following the catalog page. Install `kraken2`, `bracken`, and `KrakenTools` (bioconda) when the skill prompts, and download a reference database (e.g. Standard or PlusPF) — this is a large one-time download, not bundled.

2. **Fix your inputs.** Reads must already be quality-trimmed and host-depleted — Kraken2 does not do either, and undepleted human reads dominate a clinical sample and inflate false positives. Put paired FASTQs in `reads/` (`sample_R1.fastq.gz` / `sample_R2.fastq.gz`) and note the database path. Decide the confidence threshold up front: `0.2` or `0.4` with a comprehensive database is the sensitivity/precision sweet spot reported in the literature.

3. **Have the skill write a committed script, not just an answer.** A prompt:

   ```
   Use the kraken-classification skill to write me a script
   profile_metagenome.sh that, for every paired sample in reads/:
     1. Runs Kraken2 (--paired, --confidence 0.2) against the database
        at $DB, writing per-sample .kraken and .kreport.
     2. Runs Bracken at the species level (-r 150 -l S) on each
        .kreport to re-estimate abundance -> sample.bracken.
     3. Merges the per-sample Bracken outputs into bracken_species.tsv
        (rows = species, columns = samples, values = fraction) with
        combine_bracken_outputs.py.
     4. Writes provenance.json: kraken2 + bracken + KrakenTools
        versions, database name and build/download date, confidence
        threshold, read length, per-sample classified-read fraction,
        FASTQ sha256s, run date, and model id.
   Commit profile_metagenome.sh and an environment.yml pinning the
   bioconda versions; don't paste the abundance table back as prose.
   ```

   Keep `profile_metagenome.sh`, `environment.yml`, and `provenance.json` under version control alongside the sample manifest. Record the database **release/build date** explicitly — databases move, and this is the single biggest source of silent divergence between runs.

4. **Sanity-check before trusting the table.** Read the per-sample classified-read fraction: a very low fraction means the database is missing your community (wrong database) or your reads are still contaminated. Watch for implausible single-species dominance — a common false-positive signature; KrakenUniq-style unique-minimizer filtering (which the skill covers) helps control it. Confirm Bracken ran at the rank you report; do not present raw Kraken2 read counts as abundance.

5. **Hand off to downstream analysis.** The merged `bracken_species.tsv` is the standard input to diversity and differential-abundance analysis. Convert it to a BIOM/feature table and take alpha/beta diversity and PERMANOVA through the [16S diversity recipe's](compute-16s-microbiome-diversity.html) scikit-bio path (the diversity math is modality-agnostic). Screen the same assemblies/reads for resistance and virulence genes via the [AMR/virulence recipe](screen-genome-for-resistance-and-virulence-genes.html).

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill runs the whole Kraken2 → Bracken → merge chain. Plain Claude Code (rung 1) could script the bioconda commands, but the skill encodes the judgment that determines whether the output is meaningful: database selection bounds detectability, confidence-threshold tuning trades sensitivity against false positives, and read-count-to-abundance conversion (Bracken) is a required step, not optional polish. Those are exactly the distinctions naive command-line usage gets wrong. Rung 3+ is unnecessary: taxonomic profiling is a single, well-bounded stage.

## Availability

Fully open. The Kraken2 skill is MIT-licensed; Kraken2, Bracken, and KrakenTools are open-source (bioconda). No account or upload — everything runs locally. Reference databases (Standard, PlusPF, GTDB-derived) are free downloads. For clinical human-host samples, host depletion before classification is both an accuracy and a privacy requirement.

## Compute requirements

Workstation-class, memory-bound (not GPU — the "GPU" front-matter tier reflects the RAM/disk floor, not a GPU dependency). Kraken2 loads the entire database into RAM: the Standard database needs ~50–100 GB; capped/mini databases run in 8–16 GB at the cost of sensitivity. Once loaded, classification is very fast — millions of reads per minute. Bracken and the merge are cheap. Budget the database download (tens to hundreds of GB) and enough RAM to hold it; a laptop is only viable with a capped database.

## Evidence

Reported. The Kraken2 → Bracken workflow is the field-standard fast metagenomic profiler and is heavily used in current published work, but the Claude+skill assembly is not separately benchmarked. A systematic simulation study established exactly the database-and-confidence-score dependence this recipe pins: a comprehensive reference database combined with a moderate confidence score (0.2 or 0.4) significantly improved Kraken2 classification accuracy and sensitivity, while small databases failed to classify any reads above CS 0.4 ([Liu et al., *aBIOTECH* 2024](https://pubmed.ncbi.nlm.nih.gov/39650139/)). At applied scale, a multi-cohort analysis of **2,101 fecal metagenomes across 7 countries** used Kraken2 against the Genome Taxonomy Database for taxonomic profiling and built a diagnostic biomarker model reaching AUC 0.744–0.931 in leave-one-cohort-out analysis ([Li et al., *Gastroenterology* 2025](https://pubmed.ncbi.nlm.nih.gov/39490771/)). The known failure mode — k-mer-based over-assignment of fine-rank labels, worst for long reads — is the subject of active tooling ([Nguyen & Schatz, *bioRxiv* 2026](https://pubmed.ncbi.nlm.nih.gov/41867767/)), reinforcing the confidence-threshold and unique-minimizer controls this recipe applies.

No head-to-head benchmark of the agent-driven skill versus hand-typed Kraken2 commands exists — the skill buys correct usage (database bounds, confidence tuning, Bracken abundance conversion) and a pinned, auditable provenance file, not a new classifier.

## Alternatives considered

- **16S amplicon diversity ([compute 16S microbiome alpha/beta diversity](compute-16s-microbiome-diversity.html)).** Reach for that when your data are 16S amplicon reads (or a QIIME 2 BIOM table), not shotgun. This recipe is for whole-genome shotgun reads, which resolve to species/strain and carry functional content that amplicons cannot.
- **MetaPhlAn (marker-gene profiler).** A complementary bioSkills metagenomics skill that profiles with clade-specific marker genes rather than whole-read k-mers; it is faster and lighter on memory but detects only organisms with markers in its database. Reach for it when RAM is the constraint or you want marker-based relative abundance directly; use Kraken2+Bracken when you want read-level classification against a database you control.
- **Plain Claude Code, no skill (rung 1).** Workable if you already know the Kraken2/Bracken flags and the database trade-offs. The skill exists to prevent the silent database/confidence/abundance mistakes, so prefer it unless you are an experienced metagenomicist doing a one-off.

## See also

- [Kraken2 Metagenomic Classification (bioSkills)](../../catalog/tools/kraken-classification.html) — the skill this recipe drives.
- [Compute 16S microbiome alpha/beta diversity from a BIOM table](compute-16s-microbiome-diversity.html) — downstream diversity/PERMANOVA on the abundance table.
- [Screen a bacterial genome for resistance and virulence genes](screen-genome-for-resistance-and-virulence-genes.html) — functional follow-up on the same reads/assemblies.

## Sources

- [Liu et al., "Impact of database choice and confidence score on the performance of taxonomic classification using Kraken2," *aBIOTECH* 5:509](https://pubmed.ncbi.nlm.nih.gov/39650139/) — comprehensive database + moderate CS (0.2/0.4) optimizes accuracy/sensitivity; published 2024; verified 2026-07-25 (this run).
- [Li et al., "Multi-Cohort Analysis Reveals Altered Archaea in Colorectal Cancer Fecal Samples Across Populations," *Gastroenterology* 168:incl.](https://pubmed.ncbi.nlm.nih.gov/39490771/) — Kraken2 vs GTDB over 2,101 metagenomes; diagnostic model AUC 0.744–0.931; published 2025; verified 2026-07-25 (this run).
- [Nguyen & Schatz, "Perseus: Lineage-Aware Refinement of Kraken2 Taxonomic Classification for Long Read Metagenomes," *bioRxiv* 2026.03.06.710148](https://pubmed.ncbi.nlm.nih.gov/41867767/) — documents Kraken2 fine-rank over-assignment / false-positive mode; published 2026; verified 2026-07-25 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=profile-shotgun-metagenome-taxa-with-kraken2&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fprofile-shotgun-metagenome-taxa-with-kraken2.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
