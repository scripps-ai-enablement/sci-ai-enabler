---
title: Annotate a single bacterial genome assembly
parent: All recipes
grand_parent: Recipes
nav_order: 2
problem_class: Data analysis
subject_areas: [Immunology and Microbiology, Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-07-18
summary: Use the Bakta Claude skill to annotate one bacterial or archaeal assembly — CDS, rRNA/tRNA, CRISPR arrays — into NCBI-compatible GFF3/GenBank with a feature summary.
---

# Annotate a single bacterial genome assembly

Hand Claude Code one freshly assembled bacterial (or archaeal) genome; get back a standardized, NCBI-compatible annotation — coding sequences, rRNA/tRNA/ncRNA, CRISPR arrays, replicon features — plus a feature-count summary and a circular plot, all from a single skill.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology, Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

You have de novo assembled one isolate — a clinical strain, an environmental isolate, a lab construct — and the FASTA of contigs tells you nothing biological until it is annotated. Genome characterization papers almost always open with a single-isolate Bakta (or Prokka) run before any comparative or resistance analysis ([Santhosh et al., *BMC Genomics* 2025](https://doi.org/10.1186/s12864-025-12363-6)). The task is to call genes consistently against a curated reference and emit standard files (GFF3, GenBank, FASTA of proteins) that every downstream tool consumes. "Solved" looks like: drop one assembly in, get back a version-stamped, database-pinned annotation with a feature table you can read at a glance and a CDS count you can sanity-check against the expected genome size.

The footguns are small but real: running an annotator with the wrong genus/translation-table assumption, forgetting to set `--complete` for closed genomes versus draft contigs, and not recording the database version (so the annotation can't be reproduced later). This recipe surfaces them and stops at the annotated genome — comparative pan-genome work across *many* isolates is a separate, heavier recipe.

## Recommended approach

1. **Install the [Bakta skill](../../catalog/tools/bakta-genome-annotation.html).** It ships in the [SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) collection — clone once and load as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm Bakta appears under `/plugin` → Installed. Bakta needs its UniRef-derived database downloaded once (full DB ~70 GB; a light DB is available if disk is tight). Use the [Prokka skill](../../catalog/tools/prokka-genome-annotation.html) instead for legacy/Prokka-compatible output or a non-bacterial kingdom.

2. **Stage the assembly.** One genome per file — `assembly.fasta` (or `.fna`). Note up front whether it is a **closed/complete** genome (single circular replicon[s]) or a **draft** (many contigs); it changes one flag.

3. **Run Bakta with the right replicon assumption.** A minimal prompt:

   ```
   Use the Bakta skill on assembly.fasta with the full database.
   This is a DRAFT genome (many contigs) — do not pass --complete.
   Settings:
     - genus/species hint: <Escherichia coli>   (improves gene naming)
     - default translation table 11 for bacteria
     - write GFF3, GenBank, and the protein FASTA to annot/
   Then report a feature summary: CDS, rRNA, tRNA, tmRNA, ncRNA,
   CRISPR arrays, and the Bakta DB version used.
   ```

   For a closed genome, say so and have Claude add `--complete`. The database version in the report is what makes the run reproducible — keep it.

4. **Sanity-check the feature counts.** Open the summary: a typical 5 Mb bacterial genome carries roughly 4,500–5,500 CDS and a full complement of tRNAs plus several rRNA operons. A very low CDS count, or zero rRNA, usually means a fragmented/contaminated assembly or a wrong kingdom — fix the input before trusting the annotation.

5. **(Optional) Layer on AMR / virulence calls.** Bakta annotates structure (CDS, ncRNA, CRISPR, oriC) but is not a dedicated resistance caller. For an AMR/virulence profile, run the protein FASTA from `annot/` against a curated database (CARD, VFDB) as a separate step — published single-isolate characterizations pair Bakta with exactly this ([Santhosh et al., 2025](https://doi.org/10.1186/s12864-025-12363-6)). No such database is catalogued as a Claude skill today, so run it from the CLI.

6. **Hand off downstream.** The GFF3 is the input to the [bacterial pan-genome recipe](compute-bacterial-pangenome-from-assemblies.html) once you have more isolates; the protein FASTA feeds homology and functional-enrichment work.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill solves the whole problem. Annotation is a single, well-bounded step with a fragile parameter surface (replicon completeness, translation table, database version) that the [Bakta skill](../../catalog/tools/bakta-genome-annotation.html) encapsulates. Rung 1 (plain Claude Code) can drive the Bakta binary, but Bakta is a heavyweight tool with a 70 GB database and easy-to-miss flags; the skill pins the invocation and surfaces the database version for reproducibility. Rung 3+ is unnecessary: this is one genome, one tool — the multi-genome comparative case is the separate, rung-3 [pan-genome recipe](compute-bacterial-pangenome-from-assemblies.html).

## Availability

Fully open. Bakta is GPL-3.0; the SciAgent-Skills wrapper is CC BY 4.0. All computation runs locally on your assembly — no account, no API key, no external upload. The Bakta database is a one-time free download. FASTA, GFF3, and GenBank are open formats.

## Compute requirements

Workstation-class, driven by the database footprint rather than CPU. Bakta annotates a typical 5 Mb bacterial genome in a few minutes on a multi-core CPU; its alignment-free identification benefits from many cores and ~16 GB RAM, and the full database needs ~70 GB disk (use the light DB if disk-constrained, at some loss of annotation depth). No GPU is required — the "GPU workstation" tier reflects the RAM/disk and core count that make annotation comfortable, not a CUDA dependency.

## Evidence

Reported. The Prokka/Bakta single-isolate annotation step is the field-standard opening move in bacterial genome characterization. A 2025 study assembled an environmental *Burkholderia thailandensis* isolate de novo and **functionally annotated it with Bakta** (then layered KEGG/GO/CARD/VFDB for AMR and virulence) — the exact single-genome assembly this recipe wraps ([Santhosh et al., *BMC Genomics* 2025](https://doi.org/10.1186/s12864-025-12363-6)). Bakta itself outperformed contemporary annotators on functional annotation and database cross-references at comparable runtime ([Schwengers et al., *Microb. Genom.* 2021](https://doi.org/10.1099/mgen.0.000685)).

No head-to-head benchmark of the *agent-driven* single-genome annotation versus a hand-typed Bakta command is published — the skill buys a pinned invocation, a recorded database version, and a feature-count sanity check, not a new method.

## Alternatives considered

- **Plain Claude Code, no skill (rung 1).** Fine if Bakta and its database are already installed and on `PATH`; the skill is worth it for the pinned flags and the reproducibility-friendly database-version report.
- **Prokka instead of Bakta.** Reach for the [Prokka skill](../../catalog/tools/prokka-genome-annotation.html) when a downstream tool expects Prokka-style GFF3, or for a non-bacterial kingdom. Bakta is the better default for modern bacterial/archaeal annotation.
- **NCBI PGAP.** The right choice when you intend to submit the genome to GenBank, which requires PGAP-conformant annotation. PGAP is not catalogued as a Claude skill and is heavier; use it at submission time, not for interactive characterization.
- **The [pan-genome recipe](compute-bacterial-pangenome-from-assemblies.html) (rung 3).** Reach for it the moment you have *several* isolates and want core/accessory partitions — it runs this annotation step identically across every genome, then clusters with Roary.

## See also

- [Bakta (Claude Skill)](../../catalog/tools/bakta-genome-annotation.html) — bacterial/archaeal genome and plasmid annotation.
- [Prokka (Claude Skill)](../../catalog/tools/prokka-genome-annotation.html) — legacy/alternative prokaryotic annotator.
- [Compute a bacterial pan-genome from a set of genome assemblies](compute-bacterial-pangenome-from-assemblies.html) — the multi-isolate comparative recipe that runs this annotation step at scale.
- [Identify a bacterial isolate from its 16S rRNA sequence](identify-bacterial-isolate-from-16s-sequence.html) — produces the genus/species hint that improves gene naming here.

## Sources

- [Schwengers et al., "Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification," *Microb. Genom.* 7:000685](https://doi.org/10.1099/mgen.0.000685) — published 2021; verified 2026-06-20 (this run).
- [Santhosh et al., "Genomic characterization of an environmental *Burkholderia thailandensis* strain... reveals virulence and antimicrobial resistance signatures," *BMC Genomics* 2025](https://doi.org/10.1186/s12864-025-12363-6) — de novo assembly annotated with Bakta + CARD/VFDB; published 2025; verified 2026-06-20 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=annotate-a-bacterial-genome&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fannotate-a-bacterial-genome.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
