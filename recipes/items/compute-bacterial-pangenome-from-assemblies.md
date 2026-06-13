---
title: Compute a bacterial pan-genome from a set of genome assemblies
parent: All recipes
grand_parent: Recipes
nav_order: 4
problem_class: Data analysis
subject_areas: [Immunology and Microbiology, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-06-13
summary: Annotate a panel of bacterial assemblies with Bakta, then cluster genes into core/accessory partitions with Roary to get a pan-genome and presence/absence matrix.
---

# Compute a bacterial pan-genome from a set of genome assemblies

Hand Claude Code a folder of bacterial genome assemblies (your own isolates, or downloads from GenBank); get back consistent annotations and a pan-genome — core, soft-core, shell, and cloud gene partitions plus a gene presence/absence matrix and a core-gene alignment ready for phylogeny.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

A microbial genomicist who has sequenced (or downloaded) a panel of isolates from one species or genus — an outbreak cluster, a resistance survey, a strain collection — needs to know what genes the strains share and where they differ. The canonical answer is a pan-genome: partition genes into the **core** (present in nearly all isolates), the **accessory/shell** (variable), and the **cloud** (rare), then read off the presence/absence matrix to find resistance cassettes, virulence factors, and lineage-defining genes, and to extract a core-gene alignment for a downstream tree. Getting there is a two-stage chore that has to be done *identically* across every genome or the gene clustering breaks: annotate each assembly the same way (same tool, same database, GFF3 out), then feed all the GFF3s to a clustering tool with the right identity threshold. Mismatched annotation versions or a wrong `-i`/`-cd` setting silently inflate or collapse the accessory genome. "Solved" looks like: drop FASTA assemblies in a folder, and get back per-genome GFF3s, a `gene_presence_absence.csv`, the core/accessory partition summary, and `core_gene_alignment.aln`.

## Recommended approach

1. **Install the annotation and pan-genome skills.** Both ship in the [SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) collection — clone once and load as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm the [Bakta](../../catalog/tools/bakta-genome-annotation.html) and [Roary](../../catalog/tools/roary-pangenome.html) skills appear under `/plugin` → Installed. Each skill declares its own Python/binary dependencies in its `SKILL.md`; install them on first use (Bakta also needs its UniRef-derived database downloaded once).

2. **Stage the inputs.** Put one assembly per file in a folder — `assemblies/*.fasta` (or `.fna`). Use the **same species/genus** throughout; pan-genome clustering assumes the genomes are comparable. Give files stable, meaningful names (they become tip labels downstream).

3. **Annotate every genome identically with Bakta.** Prompt Claude to loop the [Bakta skill](../../catalog/tools/bakta-genome-annotation.html) over the folder:

   ```
   Use the Bakta skill to annotate every FASTA in assemblies/.
   For each genome:
     - run Bakta with the full database, default Prodigal CDS calling
     - write GFF3 to annot/<genome>.gff3 (Bakta GFF3 includes the
       FASTA, which Roary needs)
   Report a table of genome -> CDS count -> contig count so I can
   spot any assembly that annotated poorly (very low CDS = bad input).
   ```

   Bakta's annotations are version-stamped and database-pinned, so all genomes are annotated against the same reference — exactly what the clustering step needs. (Use the [Prokka skill](../../catalog/tools/prokka-genome-annotation.html) instead if you need a legacy/Prokka-compatible GFF3 or a non-bacterial kingdom.)

4. **Build the pan-genome with Roary.** Hand the GFF3s to the [Roary skill](../../catalog/tools/roary-pangenome.html):

   ```
   Use the Roary skill on annot/*.gff3.
   Settings:
     - blastp identity -i 95 (default; raise to 98 for within-species,
       lower toward 90 only across a genus)
     - core threshold -cd 99 (gene must be in >=99% of isolates to be core)
     - -e --mafft to produce a core_gene_alignment.aln
     - -n for fast core-gene alignment if genome count is large
   Write outputs to pangenome/. Then summarize:
     - total genes in the pan-genome
     - core / soft-core / shell / cloud counts
     - whether the pan-genome looks open or closed
   ```

5. **Read the matrix and partition.** Open `pangenome/gene_presence_absence.csv` to find genes that split the panel (candidate resistance/virulence/lineage markers); check the core/cloud ratio to judge whether the pan-genome is **open** (cloud keeps growing with each genome — diverse species) or **closed**. Treat the partition thresholds as choices, not facts — report `-i` and `-cd`.

6. **Hand off downstream.** `pangenome/core_gene_alignment.aln` is the input to a core-genome phylogeny: feed it to the [phylogenetics recipe](build-phylogenetic-tree-from-sequences.html) (IQ-TREE 2 ML tree with bootstrap) to resolve strain relationships. Resistance/virulence gene calls in the presence/absence matrix can be cross-checked against curated databases as a separate step.

## Why this assembly

Rung 3 (multi-tool harness) — two cataloged skills chained, Bakta → Roary. It is genuinely a two-stage problem: annotation and clustering are different tools with different databases, and the join between them (every genome annotated identically, GFF3-with-sequence handed to the clusterer) is precisely where hand-built pipelines break. Rung 1 (plain Claude Code) fails because Bakta and Roary are heavyweight binaries with large databases and a fragile parameter surface — Claude writing the commands from scratch each time risks inconsistent annotation versions across genomes, which corrupts the gene clustering invisibly. Rung 2 (a single skill) cannot span both stages. A rung-4 autonomous system is overkill: the pan-genome is a self-contained, well-defined analysis, not an open-ended research loop.

## Availability

Fully open. Bakta (GPL-3.0), Prokka (GPL-3.0), and Roary (GPL-3.0) are open-source, as are the SciAgent-Skills wrappers (CC BY 4.0 collection). All computation runs locally on your assemblies — no external API calls, no account, no API key. Bakta's database is a one-time free download (the full DB is ~70 GB; a light DB is available if disk is tight). FASTA, GFF3, and CSV are open formats.

## Compute requirements

Workstation-class, mostly for the annotation step and Bakta's database footprint. Bakta annotates a typical 5 Mb bacterial genome in a few minutes on a multi-core CPU; its alignment-free identification benefits from many cores and ~16 GB RAM, and the full database needs ~70 GB disk. Annotating tens of genomes is an hour-scale CPU job. Roary itself is light: the authors report a 1000-isolate pan-genome in **4.5 hours on a single CPU using 13 GB RAM** ([Page et al., 2015](https://doi.org/10.1093/bioinformatics/btv421)); panels of tens-to-low-hundreds of genomes finish in minutes-to-an-hour and parallelize across cores (`-p`). No GPU is required for either tool — the "GPU workstation" tier reflects the RAM/disk and core count that make annotation comfortable, not a CUDA dependency. The core-gene MAFFT alignment (`-e --mafft`) is the heaviest Roary step for large panels; use `-n` for a fast approximate alignment.

## Evidence

Proposed. No documented end-to-end attempt of "Claude Code + the Bakta and Roary skills on a real isolate panel," with quantitative pass/fail, is known to the curator. The closest evidence is component-level and analogous:

- **The Prokka/Bakta → Roary pipeline is field-standard comparative genomics.** A 2025 study annotated **27,884 *Acinetobacter baumannii* genomes with Prokka and ran the pan-genome with Roary**, recovering a stable core and a highly diverse open accessory genome and tracking AMR/virulence over time ([Sholeh et al., *Mol. Genet. Genomics* 2025](https://doi.org/10.1007/s00438-025-02265-3)) — the exact two-stage assembly this recipe orchestrates, at scale, on real data.
- **The underlying tools are the reference implementations.** Bakta outperformed contemporary annotators on functional annotation and database cross-references at comparable runtime ([Schwengers et al., *Microb. Genom.* 2021](https://doi.org/10.1099/mgen.0.000685)); Roary is the standard rapid pan-genome tool ([Page et al., *Bioinformatics* 2015](https://doi.org/10.1093/bioinformatics/btv421)).
- **No head-to-head benchmark** of the agent-driven assembly versus a hand-written Snakemake/Nextflow pan-genome pipeline is published; the agent loop buys consistent annotation across genomes and a documented prompt template, not a new method.

## Alternatives considered

- **Plain Claude Code, no skills (rung 1).** Workable only if Bakta, Roary, and the Bakta database are already installed and on `PATH` — then Claude can drive the binaries directly. Reach for it for a one-off on a machine that is already set up; reach for the skills when you want the annotation step pinned identically across genomes and a repeatable template.
- **Panaroo / PIRATE / PPanGGOLiN instead of Roary.** Roary's catalog page notes Panaroo for higher accuracy on fragmented assemblies, PIRATE for paralog-aware clustering, and PPanGGOLiN for graph-based partitioning. None is cataloged as a Claude skill today; if your assemblies are highly fragmented (many contigs), prefer Panaroo manually and surface it to the catalog curator.
- **A Nextflow pipeline (`nf-core/pangenome`-style), no agent.** The right tool when you run the same pan-genome at scale, repeatedly, on a cluster — workflow-automation territory. See the [Nextflow catalog page](../../catalog/tools/nextflow-development.html). For an interactive one-off panel, this recipe is lighter.

## See also

- [Bakta (Claude Skill)](../../catalog/tools/bakta-genome-annotation.html) — bacterial/archaeal genome and plasmid annotation.
- [Prokka (Claude Skill)](../../catalog/tools/prokka-genome-annotation.html) — legacy/alternative prokaryotic annotator.
- [Roary (Claude Skill)](../../catalog/tools/roary-pangenome.html) — pan-genome clustering and core-gene alignment.
- [Build a phylogenetic tree from a set of sequences](build-phylogenetic-tree-from-sequences.html) — consumes the `core_gene_alignment.aln` this recipe produces.

## Sources

- [Page et al., "Roary: rapid large-scale prokaryote pan genome analysis," *Bioinformatics* 31:3691–3693](https://doi.org/10.1093/bioinformatics/btv421) — published 2015; verified 2026-06-13 (this run).
- [Schwengers et al., "Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification," *Microb. Genom.* 7:000685](https://doi.org/10.1099/mgen.0.000685) — published 2021; verified 2026-06-13 (this run).
- [Sholeh et al., "Unravelling the genomic landscape of *Acinetobacter baumannii*," *Mol. Genet. Genomics* 300:64](https://doi.org/10.1007/s00438-025-02265-3) — Prokka + Roary on 27,884 genomes; published 2025; verified 2026-06-13 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=compute-bacterial-pangenome-from-assemblies&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fcompute-bacterial-pangenome-from-assemblies.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
