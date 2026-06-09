---
title: Build a phylogenetic tree from a set of sequences
parent: All recipes
grand_parent: Recipes
nav_order: 3
problem_class: Data analysis
subject_areas: [Immunology and Microbiology, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-09
summary: Use the phylogenetics Claude skill to take a FASTA of homologous sequences through MAFFT alignment, IQ-TREE 2 maximum-likelihood inference with bootstrap support, and an annotated tree figure.
---

# Build a phylogenetic tree from a set of sequences

Hand Claude Code a FASTA of homologous sequences (viral genomes, a microbial marker gene, a protein family); get back a trimmed multiple alignment, a model-selected maximum-likelihood tree with bootstrap support, and a publication-ready annotated tree figure — without hand-wiring the MAFFT → IQ-TREE 2 → ETE3 command chain.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A microbiologist or viral phylodynamicist who has just pulled a set of sequences — outbreak isolate genomes from GISAID/GenBank, 16S/marker amplicons from a culture collection, or a protein family from UniProt — needs the same canonical pipeline every time: align the sequences (MAFFT), optionally trim poorly aligned columns, pick a substitution model, infer a maximum-likelihood tree with branch support (IQ-TREE 2's ModelFinder + ultrafast bootstrap, or FastTree when speed matters), root it, and render an annotated figure. The individual tools are standard, but stitching them together — getting the MAFFT flags right, parsing ModelFinder output, passing the right alignment to IQ-TREE, mapping tip labels to metadata in the figure — is repetitive boilerplate that is easy to get subtly wrong (a mis-set bootstrap count, an unrooted tree presented as rooted). "Solved" looks like: drop a FASTA in the project, name the metadata column you want to colour tips by, and get back `aligned.fasta`, `tree.treefile` with support values, and a labelled `tree.png`.

## Recommended approach

1. **Install the [Phylogenetics (Claude Skill)](../../catalog/tools/phylogenetics.html).** From the K-Dense `scientific-agent-skills` collection:

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   ```

   Enable the `phylogenetics` skill when prompted. It wraps MAFFT (alignment), IQ-TREE 2 (maximum-likelihood with ModelFinder + ultrafast bootstrap), FastTree (fast NJ/ML), and ETE3/FigTree (visualization). The skill declares its own Python/binary dependencies in its `SKILL.md`; install them on first use.

2. **Place the inputs in the project.** You need:

   - `sequences.fasta` — your homologous nucleotide or amino-acid sequences, one record per taxon, with stable IDs in the headers.
   - `metadata.tsv` *(optional)* — one row per sequence ID, with columns you want to annotate tips by (collection date, host, lineage, country).

3. **Invoke the skill with the file paths and the analysis you want.** A minimal prompt:

   ```
   Use the phylogenetics skill on data/sequences.fasta.

   Steps:
     1. Align with MAFFT (use --auto; report the strategy it selected).
     2. Trim alignment columns with >50% gaps; report columns kept vs
        dropped and write out/aligned.fasta.
     3. Infer a maximum-likelihood tree with IQ-TREE 2: let ModelFinder
        pick the substitution model, run 1000 ultrafast bootstrap
        replicates and 1000 SH-aLRT replicates. Write out/tree.treefile.
     4. Midpoint-root the tree.
     5. Render the tree with ETE3 to figures/tree.png: show bootstrap
        support on internal nodes, colour tips by `host` from
        data/metadata.tsv, and collapse nodes with <50% support.
   ```

4. **Read the model and support critically.** Note which substitution model ModelFinder selected (GTR+G, HKY, LG+G, etc.) and report it — reviewers will ask. Treat internal nodes with ultrafast-bootstrap < 95% or SH-aLRT < 80% as unresolved; do not over-interpret a poorly supported clade. Confirm the rooting choice is defensible: midpoint rooting is a convenience, not a biological claim — if you have a known outgroup, re-run with `-o <outgroup_id>` instead.

5. **Hand off downstream.** The Newick `tree.treefile` drops into [ETE Toolkit](../../catalog/tools/etetoolkit.html) for orthology/paralogy event detection or NCBI-taxonomy annotation, or into BEAST/Nextstrain for time-scaled phylodynamics (outside this skill). For microbial-community context, the same FASTA can feed the [16S diversity recipe](compute-16s-microbiome-diversity.html) — that recipe consumes the tree this one produces as its UniFrac input.

## Why this assembly

Rung 2 of the simplicity ladder. Plain Claude Code can write the MAFFT/IQ-TREE invocations from scratch, but the parameter surface is wide (alignment strategy, trimming threshold, model selection, bootstrap type and count, rooting) and small slips silently change the tree — an unrooted tree drawn as rooted, or a too-low bootstrap count that overstates support. The skill encodes the canonical align → model-select → ML-infer → annotate workflow as one discoverable action with sensible defaults, which is the right grain for a single-stage analytical task. No need to escalate to a multi-tool harness or an autonomous system: tree building is a well-defined, self-contained problem.

## Availability

Fully open. MAFFT (BSD), IQ-TREE 2 (GPL-2.0), FastTree (GPL-2.0), and ETE3 (GPL-3.0) are all open-source; the K-Dense skill wrapper ships in the same OSS collection (license not stated upstream). The skill makes no external API calls — all computation runs locally on your sequences. FASTA and Newick are open formats. No subscription, institutional account, or API key required.

## Compute requirements

Laptop-sufficient for typical inputs. A few hundred sequences of viral-genome length (~30 kb) or a 16S marker (~1.5 kb) align in seconds-to-minutes with MAFFT `--auto` and infer in a few minutes with IQ-TREE 2 + 1000 ultrafast-bootstrap replicates on a modern multi-core laptop with 16 GB RAM; IQ-TREE parallelizes across cores (`-T AUTO`). The ML tree search is the heaviest step. Datasets in the thousands of full genomes push you toward FastTree (the skill exposes it) for a fast approximate tree, or toward an HPC IQ-TREE run. No GPU is used.

## Evidence

Proposed. No documented end-to-end attempt of "Claude Code + the phylogenetics skill on a real sequence set" with quantitative pass/fail is known to the curator. The closest evidence is component-level and class-level:

- **The underlying tools are the field-standard reference implementations.** MAFFT ([Katoh & Standley, *Mol. Biol. Evol.* 30:772 (2013)](https://doi.org/10.1093/molbev/mst010)) and IQ-TREE 2 ([Minh et al., *Mol. Biol. Evol.* 37:1530 (2020)](https://doi.org/10.1093/molbev/msaa015)) with ModelFinder ([Kalyaanamoorthy et al., *Nat. Methods* 14:587 (2017)](https://doi.org/10.1038/nmeth.4285)) and UFBoot2 ([Hoang et al., *Mol. Biol. Evol.* 35:518 (2018)](https://doi.org/10.1093/molbev/msx281)) are used in tens of thousands of published phylogenies; this recipe orchestrates them, it does not invent a method.
- **Class-level LLM-agent evidence** comes from [Huang et al., Biomni (bioRxiv 2025.05.30.656746)](https://doi.org/10.1101/2025.05.30.656746), whose 150-tool agent environment includes alignment and tree-building primitives and reports a ~4× accuracy improvement over base LLMs on biomedical bioinformatics tasks — exercising the same task family this recipe runs through a single focused skill.
- **No head-to-head benchmark** of "phylogenetics skill" versus hand-written MAFFT/IQ-TREE scripts is published; the agent loop here buys convenience and consistency, not a new analytical method.

## Alternatives considered

- **Plain Claude Code, no skill (rung 1).** Works — Claude can write the MAFFT and IQ-TREE 2 commands directly if the binaries are on `PATH`. Reach for this when you need a one-off custom step the skill does not expose (a non-standard partition model, a constraint tree). Reach for the skill when you want a repeatable, documented prompt template across studies.
- **Nextflow `nf-core/phylogeny`-style pipeline (no agent).** The right tool when you run the same tree build at scale, on a cluster, hundreds of times — but that is workflow-automation overkill for an interactive one-off. See the [Nextflow catalog page](../../catalog/tools/nextflow-development.html) if your use case is batch.
- **Biomni (rung 4).** The [Biomni](../../autonomous-science/systems/biomni.html) agent exposes alignment/tree primitives inside a 150-tool environment. Reach for it when the tree is one node of a larger multi-stage analysis (e.g., assemble genomes → call variants → build tree → date the MRCA); reach for the focused skill when the tree is the whole job.

## See also

- [Phylogenetics (Claude Skill)](../../catalog/tools/phylogenetics.html)
- [ETE Toolkit (Claude Skill)](../../catalog/tools/etetoolkit.html) — downstream tree manipulation, orthology detection, and NCBI-taxonomy annotation.
- [Compute 16S microbiome alpha/beta diversity from a BIOM table](compute-16s-microbiome-diversity.html) — consumes the rooted tree this recipe produces for UniFrac.
- [Biomni](../../autonomous-science/systems/biomni.html) — autonomous-system option one rung up.

## Sources

- [`skills/phylogenetics/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/phylogenetics/SKILL.md) — skill manifest; verified 2026-06-09 (this run).
- [Katoh & Standley, "MAFFT multiple sequence alignment software version 7," *Mol. Biol. Evol.* 30:772–780](https://doi.org/10.1093/molbev/mst010) — published 2013; verified 2026-06-09 (this run).
- [Minh et al., "IQ-TREE 2," *Mol. Biol. Evol.* 37:1530–1534](https://doi.org/10.1093/molbev/msaa015) — published 2020; verified 2026-06-09 (this run).
- [Kalyaanamoorthy et al., "ModelFinder," *Nat. Methods* 14:587–589](https://doi.org/10.1038/nmeth.4285) — published 2017; verified 2026-06-09 (this run).
- [Hoang et al., "UFBoot2: improving the ultrafast bootstrap approximation," *Mol. Biol. Evol.* 35:518–522](https://doi.org/10.1093/molbev/msx281) — published 2018; verified 2026-06-09 (this run).
- [Huang et al., "Biomni: A General-Purpose Biomedical AI Agent," bioRxiv 2025.05.30.656746](https://doi.org/10.1101/2025.05.30.656746) — class-level LLM-agent evidence; verified 2026-06-09 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=build-phylogenetic-tree-from-sequences&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fbuild-phylogenetic-tree-from-sequences.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
