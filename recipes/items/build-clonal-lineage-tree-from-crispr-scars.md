---
title: Build a clonal lineage tree from CRISPR scar recorders
parent: All recipes
grand_parent: Recipes
nav_order: 1
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-08-01
summary: Use the Lineage Tracing skill to turn recorder reads into a character matrix, reconstruct trees with several solvers, and check topology robustness before interpreting.
---

# Build a clonal lineage tree from CRISPR scar recorders

Hand Claude Code recorder reads from a CRISPR/Cas9 scar, expressed-barcode or mtDNA lineage assay; get back a character matrix, trees from more than one solver, a quantified topology-agreement score, and — if you have paired transcriptomes — a clonal fate-bias map.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

You have a heritable recorder in your system — Cas9-induced indels at a target array, a static expressed barcode (LARRY, CellTag), a combinatorial tag, or somatic mtDNA variants — and single-cell reads carrying it. The goal is a clonal phylogeny: which cells descend from which, and what that says about developmental hierarchy, tumour progression, or metastatic reseeding. The appealing shortcut is to run one tree-building call, get a topology, and start reading clades off it.

Lineage recorders punish that. Two failure modes dominate, and both produce trees that are confidently wrong rather than obviously broken. **Homoplasy** — the same scar arising independently in unrelated cells, because Cas9 cutting favours a small set of repair outcomes — makes unrelated cells look like siblings; it is exactly why star-homoplasy models exist as a separate class from standard parsimony. **Allele dropout** removes characters at random, and cells missing most of their characters carry no phylogenetic signal but still get placed somewhere. On top of that, phylogenetic signal is often thin enough that different solvers, and even different upstream processing pipelines, return different topologies from the same data. Solved looks like: a filtered character matrix, trees from at least two solvers, an explicit agreement statistic between them, and interpretation restricted to the clades that survive.

## Recommended approach

1. **Install the [Lineage Tracing skill](../../catalog/tools/lineage-tracing.html).** Follow its catalog page for the install — note the one non-obvious step it documents: Cassiopeia 2.0+ must come from GitHub, because the PyPI distribution lags. That has a reproducibility consequence you must handle in step 7: there is no version number to pin, so record the commit SHA you installed.

2. **State the assay before any analysis.** Scars, static barcodes, combinatorial tags and mtDNA variants differ in resolution and dropout behaviour, and they license different claims. A static barcode groups cells into clones but carries no within-clone branching order; a Cas9 scar array carries branching order but is homoplasy-prone. Write the assay into the script header so the tree is never over-read later.

3. **Build the character matrix, then filter it — and log what you dropped.** Resolve UMIs, align reads, call alleles, and convert to phylogenetic characters. Apply the skill's quality thresholds and record their effect:

   ```
   Use the Lineage Tracing skill on data/recorder_reads.tsv (Cas9 scar
   array, 10 target sites).

   Build the character matrix. Then filter:
     - drop cells with < 10 UMIs
     - drop cells missing > 50% of characters
     - keep a character as informative only if its state appears in
       more than one cell

   Write results/character_matrix.csv and results/filter_log.csv with
   one row per filter step: step, n_cells_before, n_cells_after,
   n_characters_before, n_characters_after. Also emit
   results/dropout_by_site.csv (per-site missing fraction) and
   results/state_frequency.csv (per-character state counts) so I can
   see which sites are saturated.
   ```

   `state_frequency.csv` is the homoplasy early-warning: a scar state present in a large fraction of cells is far more likely to be a favoured repair outcome than a shared ancestor.

4. **Check that the barcode library could not have fabricated clones.** Library complexity must far exceed the founder population, or two independent founders share a barcode and merge into one apparent clone. Compute the expected collision rate from library size and founder count and put the number in the provenance record. If the founder count is unknown, say so rather than assuming.

5. **Reconstruct with more than one solver.** Run a fast heuristic and a distance method as the baseline pair, add a star-homoplasy-aware method for scar data, and reserve the exact ILP path for small subtrees where it is affordable:

   ```
   Reconstruct trees with: VanillaGreedy, NeighborJoining, and (scar
   data) Startle. Write each to results/tree_<solver>.nwk.

   Then compare topologies pairwise: Robinson-Foulds distance and
   triplets-correct score. Write results/topology_agreement.csv with
   solver_a, solver_b, rf, rf_normalized, triplets_correct.

   Emit results/consensus_clades.csv listing clades recovered by all
   solvers, with the number of solvers supporting each. Do not
   collapse the trees into one "best" tree.
   ```

   Keeping the solvers as separate outputs, rather than averaging or picking a winner, is the whole point: agreement across methods is your only internal estimate of how much of the topology the data actually supports.

6. **Join clones to transcriptomic state, and treat state-based fate calls as claims to test.** With paired clonal and expression data, run CoSpar to infer fate bias from the clonal information, writing per-clone fate probabilities to `results/fate_bias.csv`. Where an expression-based trajectory ([scVelo](../../catalog/tools/scvelo.html) or [CellRank](../../catalog/tools/cellrank-mcp.html)) disagrees with the clonal evidence, record the disagreement as a column rather than resolving it — the recorder is the physical measurement and the RNA-dynamics inference is the hypothesis, not the other way round.

7. **Land the artifact.** Commit `build_lineage_tree.py`, a pinned `requirements.txt`, the `results/` tables and Newick files, and a `provenance.json` containing: the Cassiopeia **commit SHA** (not a version string), CoSpar / scanpy / numpy versions, the bioSkills commit SHA, the input read-file sha256, the assay type, every filter threshold and its before/after counts, the solvers run with their parameters, and the model id. Because the topology depends on the upstream processing choices as much as on the solver, the filter log is part of the result, not a diagnostic. See the [reproducibility guide](../../guide/advanced/reproducibility.html).

## Why this assembly

Rung 2 of the simplicity ladder, and it stays there. This is one bounded pipeline over one dataset: no database lookups, no literature search, nothing for an autonomous system to explore. What plain Claude Code gets wrong is the epistemics, not the code — asked to build a lineage tree it will install a solver, call it once, and hand back a single Newick file that looks authoritative and carries no indication of how much signal was behind it. The [Lineage Tracing skill](../../catalog/tools/lineage-tracing.html) supplies the four judgements that matter: the UMI and missing-character thresholds, the informative-character rule, the multi-solver robustness comparison, and the rule that clonal evidence outranks an expression-based fate call. Those are the decisions that separate a defensible tree from a decorative one.

## Availability

Fully open — the skill is MIT (GPTomics bioSkills) and the underlying tools are OSS; see its catalog page for the per-tool licenses. Nothing leaves your machine. Two practical caveats. Cassiopeia is installed from a git ref rather than a release, so your environment is only reproducible if you record the commit SHA (step 7). And the exact ILP solver is the expensive member of the Cassiopeia family — plan around the greedy, distance and star-homoplasy solvers for full datasets, and confirm the ILP path's solver-backend requirements from the upstream docs before designing a run around it.

## Compute requirements

No GPU is needed; this is CPU- and memory-bound. Character-matrix construction is I/O-heavy and scales with read depth rather than cell count — budget disk for intermediates. Greedy and neighbour-joining reconstruction on tens of thousands of cells is minutes to an hour on a laptop with 16 GB. The `Workstation with GPU` tier is claimed for its cores and RAM at two steps: the Hybrid solver, which farms exact solutions onto subproblems and benefits from many cores, and the pairwise topology comparison, where Robinson–Foulds and triplets-correct scoring across three solvers on a large tree is the step most likely to surprise you on wall-clock. Published work at this scale exists — 34,557 human cells traced over 15 generations — so the ceiling is real but reachable. If the run is slow, cut the solver count before cutting the filters.

## Evidence

`Proposed`. No documented attempt at this exact assembly — Claude Code driving the Lineage Tracing skill — is known, and no benchmark compares it against a hand-written Cassiopeia pipeline. Each individual step, however, rests on published method work:

- **Reconstruction and the benchmark that justifies multi-solver comparison.** Jones et al. introduced Cassiopeia as a suite of scalable maximum-parsimony approaches plus a simulation framework, and generated what was then the most complex experimental lineage-tracing dataset — 34,557 human cells continuously traced over 15 generations — showing Cassiopeia outperforms traditional methods across several metrics and parameter regimes ([*Genome Biology* 2020](https://doi.org/10.1186/s13059-020-02000-8)).
- **Homoplasy as a first-class modelling problem, and topology instability.** Dai and Molloy describe Star Homoplasy Parsimony and the Startle family as the response to the specific properties of CRISPR-induced mutations, note that reconstruction "continues to be challenged by technological limitations in producing consistent phylogenetic signals", report the largest accuracy gains precisely when signal is limited by a high cell-to-mutation ratio, and find that the upstream processing pipeline itself can change relative method performance on mouse lung-adenocarcinoma data ([Dai & Molloy 2026](https://doi.org/10.1177/15578666251386082)). That last finding is why step 7 treats the filter log as part of the result.
- **Clone-to-state integration.** Wang et al. built CoSpar on coherence and sparsity assumptions specifically to be robust to the severe downsampling and dispersion typical of lineage data, and showed it identifies early fate biases not previously detected across hematopoiesis, reprogramming and directed-differentiation datasets ([*Nature Biotechnology* 2022](https://doi.org/10.1038/s41587-022-01209-1)).

The closest documented analogue for the agent-driven form is the [Perturb-seq recipe](analyze-perturb-seq-crispr-screen.html), where a skill exists for the same reason: to enforce statistical decisions a general-purpose agent will otherwise silently default past.

## Alternatives considered

- **Plain Claude Code with a single solver call.** Rung 1. Reach for it only for a quick look at clone sizes from static barcodes, where no branching order is being claimed. For anything that reads structure off a tree, the single-solver output gives you no way to tell signal from artifact.
- **Expression-based trajectory inference instead ([scVelo](../../catalog/tools/scvelo.html), [CellRank](../../catalog/tools/cellrank-mcp.html)).** Cheaper and needs no recorder, and the right choice when you have no lineage assay — but it infers dynamics from RNA rather than measuring descent. Use it as the comparison in step 6, not as the substitute. The [GRN inference recipe](infer-gene-regulatory-network-from-scrnaseq.html) is the complementary route when you want regulators rather than genealogy.
- **BCR/TCR clonal lineages.** If your "lineage" is immunoglobulin somatic hypermutation rather than an engineered recorder, this is the wrong recipe: see [Reconstruct BCR clonal lineages](reconstruct-bcr-clonal-lineages.html), which uses the receptor sequence itself as the record.
- **An autonomous-science system.** Overkill for a fixed pipeline over one dataset. It would add non-determinism to a workflow whose central problem is already that the answer is unstable.

## See also

- [Lineage Tracing (Claude Skill)](../../catalog/tools/lineage-tracing.html)
- [Analyze a Perturb-seq CRISPR screen for perturbation effects](analyze-perturb-seq-crispr-screen.html) — the other single-cell CRISPR-readout recipe.
- [Run first-pass QC on a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — run on the paired transcriptome before step 6.
- [Reconstruct BCR clonal lineages from repertoire sequencing](reconstruct-bcr-clonal-lineages.html) — the immune-repertoire counterpart.
- [scVelo (Claude Skill)](../../catalog/tools/scvelo.html) · [CellRank MCP](../../catalog/tools/cellrank-mcp.html) — expression-based trajectories to compare against clonal evidence.

## Sources

- [`single-cell/lineage-tracing/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/single-cell/lineage-tracing/SKILL.md) — GPTomics bioSkills; catalog page verified 2026-08-01.
- [Jones M.G. et al., "Inference of single-cell phylogenies from lineage tracing data using Cassiopeia", *Genome Biology* 2020](https://doi.org/10.1186/s13059-020-02000-8) — published 2020; verified 2026-08-01 (this run).
- [Wang S.W. et al., "CoSpar identifies early cell fate biases from single-cell transcriptomic and lineage information", *Nature Biotechnology* 2022](https://doi.org/10.1038/s41587-022-01209-1) — published 2022; verified 2026-08-01 (this run).
- [Dai J., Molloy E.K., "StarCDP: Dynamic Programming Algorithms for Fast and Accurate Cell Lineage Tree Reconstruction from CRISPR-Based Lineage Tracing Data", 2026](https://doi.org/10.1177/15578666251386082) — published 2026; verified 2026-08-01 (this run).
- [`YosefLab/Cassiopeia`](https://github.com/YosefLab/Cassiopeia) — install source referenced by the catalog page, verified 2026-08-01.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=build-clonal-lineage-tree-from-crispr-scars&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fbuild-clonal-lineage-tree-from-crispr-scars.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
