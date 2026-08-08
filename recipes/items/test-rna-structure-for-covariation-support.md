---
title: Test whether a proposed RNA structure is actually conserved
parent: All recipes
grand_parent: Recipes
nav_order: 27
problem_class: Data analysis
subject_areas: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-08
summary: Use the Covariation Analysis skill to test a proposed RNA secondary structure with R-scape, and to establish whether the alignment even has the power to reject it.
---

# Test whether a proposed RNA structure is actually conserved

Before you build on a published or predicted RNA secondary structure, test it: does the alignment show compensatory substitutions above what phylogeny alone predicts — and does it have enough independent variation to say anything either way?

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Integrative Structural and Computational Biology, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have a secondary structure for an RNA — folded with a thermodynamic predictor, taken from a figure in a paper, or drawn from a chemical-probing model — and you are about to spend real money on it: designing structure-disrupting mutants, building a covariance model to search for homologs, claiming a conserved structural element in a manuscript, or interpreting a variant as structure-breaking. A thermodynamic prediction will return a structure for *any* sequence, including a shuffled one, so the fold itself is not evidence that the structure is under selection.

The evolutionary test is compensatory substitution: if a base pair is functionally important, lineages that mutate one side tend to mutate the other. But raw covariation is a trap in two directions. In one direction, closely related sequences covary at *every* position simply because they share ancestry, so a mutual-information score will light up on structures that are not conserved at all. In the other direction — the one that causes more damage in practice — an alignment can be too conserved to test anything, and a null result there is not evidence against the structure, it is no result. The two are routinely conflated, and a low-power negative reported as a refutation is as wrong as a phylogenetic artifact reported as support. "Solved" is a three-way verdict — supported, rejected, or undetermined for lack of power — with the per-pair numbers behind it committed to disk.

## Recommended approach

Rung 2 — one Claude Skill, the [Covariation Analysis skill](../../catalog/tools/covariation-analysis.html) (bioSkills), which drives R-scape locally: it scores your proposed pairs against a phylogeny-aware null, scores alternative pairs separately, and estimates per-pair detection power.

1. **Install the skill and R-scape.** Verbatim steps are on the [catalog page](../../catalog/tools/covariation-analysis.html) — clone `GPTomics/bioSkills` and install the `rna-structure` category (or copy `rna-structure/covariation-analysis` alone), then install R-scape 2.0+ separately (`conda install -c conda-forge -c bioconda rscape`). Confirm with `R-scape --version` before running, and require **2.0.0.p or higher**: helix-level aggregation is only available from that version and it changes the result (step 5).

2. **Build the alignment independently of the structure — this is the load-bearing step.** You need a deep, diverse Stockholm alignment carrying a `#=GC SS_cons` line. Aim for roughly **60% average pairwise identity**, not 90–95%; what buys power is the number of *independent substitutions*, so a hundred near-identical sequences is a weaker test than twenty diverse ones. And the alignment must not have been built using the structure you are testing. Structure-aware aligners and covariation-guided alignment construction create a documented circularity: [Rivas (2023)](https://pubmed.ncbi.nlm.nih.gov/37450549/) identifies exactly this artifact — using covariation to build an alignment for a hypothetical structure and then testing that alignment for whether its covariation supports the structure. Record in the provenance how the alignment was built and with what aligner. If it was structure-guided, the test is void; rebuild it sequence-only.

3. **Run the structure test and the power analysis together.** Never run the test without the power estimate — the power number is what makes a negative interpretable:

   ```
   Use the covariation-analysis skill on alignment.sto.

   - Test the proposed structure in the #=GC SS_cons line (-s), at the
     default E-value target of 0.05.
   - Report alternative-pair covariation separately from proposed-pair
     covariation, so "structure rejected" and "different structure
     supported" stay distinguishable outcomes.
   - Run the power analysis and report per-pair expected detection
     probability plus the mean power over the proposed pairs.
   - Emit helix-level aggregated E-values as well as per-base-pair ones.
   - Write the exact commands you run to run_covariation.sh.
   ```

4. **Emit the tables and make the verdict three-way.** `covariation.csv` — one row per proposed pair (`i, j, score, e_value, helix_id, helix_e_value, n_substitutions, power`). `alternative_pairs.csv` — covarying pairs *not* in the proposed structure, kept as a separate file because they are a different finding. Then `verdict.md`, whose call is one of:

   - **`supported`** — significant covariation above the phylogenetic null on a meaningful fraction of the proposed pairs.
   - **`rejected`** — no significant covariation *and* the alignment is adequately powered. The skill's working line is a mean alignment power of roughly **10%**; below that, this verdict is not available to you.
   - **`undetermined`** — no significant covariation and mean power below that line. This is a statement about your alignment, not about the RNA. The remedy is more diverse sequences, not a different threshold.

   Write the mean power into the verdict line itself, so nobody can quote the conclusion without the caveat attached.

5. **Read the helix-level result, not only the per-pair result.** R-scape treats base pairs independently by default, but Watson–Crick pairs stack into helices and the helix is where most of the covariation signal lives. Aggregating significance and power to helix level raises sensitivity without costing specificity ([Rivas 2023](https://pubmed.ncbi.nlm.nih.gov/37450549/)), so a structure with no individually significant pair can still have a significantly covarying helix — and reporting only the per-pair table will make you throw away a real structure. Report both columns; if they disagree, say so rather than picking the friendlier one.

6. **If there is no trusted structure to test, switch modes deliberately.** `--cacofold` builds a covariation-supported consensus de novo, which is the right input for seeding a covariance model or a restrained fold. Do not then run the structure test on that same alignment and consensus and report it as validation — that is precisely the circularity in step 2. A CaCoFold consensus is a hypothesis generated from the alignment, not a test of one.

7. **Record provenance.** `provenance.json` should carry the R-scape version string verbatim, the alignment's sha256 and sequence count, the **average pairwise identity** and mean power (the two numbers that determine whether the result means anything), the E-value target, the source and release of the alignment if it came from a curated database — an [Rfam](../../catalog/tools/rfam.html) family alignment changes between releases, so the release number is not optional — how the alignment was built and with which aligner, and the model id. See the [reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) guide for the pattern.

The durable artifact is the committed `.claude/commands/test-covariation.md`, `run_covariation.sh`, the pinned environment, and per-RNA `covariation.csv` + `alternative_pairs.csv` + `verdict.md` + `provenance.json` alongside the R-scape `.cov` / `.power` outputs and the R2R diagram.

One boundary to keep in the write-up: this tests whether a structure is **conserved**. It does not test whether the transcript is real, expressed, or functional — those need expression and functional evidence, and a covariation-supported structure in an unexpressed region is still not a finding.

## Why this assembly

Rung 2, and it stops there. One skill drives one statistical test over one alignment, locally. Rung 1 fails hard and specifically: Claude Code alone cannot compute a phylogeny-aware null, and asked whether a structure is conserved it will produce a fluent narrative about compensatory mutations that has no statistics behind it — the failure mode this recipe exists to prevent. Rungs 3 and 4 add nothing, because the difficulty is not orchestration but the two interpretive gates (power, and alignment independence) that live inside a single tool's output.

## Availability

Fully open. bioSkills is MIT; R-scape is open source from the Rivas Lab and packaged in bioconda. Everything runs **locally** — your alignment never leaves the machine, so unpublished sequences and pre-publication structures are fine. No account, no API, no subscription. Note the R-scape install is conda-based rather than pip, so a pip-only environment needs a conda or mamba prefix available.

## Compute requirements

Laptop. R-scape on a typical family alignment — tens to a few hundred sequences, a few hundred columns — runs in seconds to a couple of minutes, and the R2R diagram generation is the visible pause. Cost scales with alignment depth times length squared, so a very deep alignment of a long RNA (thousands of sequences over a multi-kilobase lncRNA) is the case that stretches into many minutes and gigabytes; subsample to a diverse subset rather than a random one if you need to trim, because random subsampling of a redundant alignment removes the diverse sequences that were carrying your power. Record the subsampling if you do it — it changes the power number, which changes what verdicts are available to you.

## Evidence

Proposed. No documented attempt of this Claude-skill assembly is known, and the skill is not benchmarked end-to-end. The underlying method, however, is unusually well characterized on exactly this problem, and each of the recipe's gates traces to one of these results:

- **Rivas, Clements & Eddy (*Nat. Methods* 2017)** introduced R-scape and reported that covariation analysis finds no statistically significant support for the proposed secondary structures of the lncRNAs HOTAIR, SRA and Xist ([doi:10.1038/nmeth.4066](https://doi.org/10.1038/nmeth.4066)) — the canonical demonstration that a published structure can fail this test, and the reason the test is worth running before you build on one.
- **Rivas, Clements & Eddy (*Bioinformatics* 2020)** added power estimation specifically to distinguish "lack of covariation is evidence against the structure" from "the alignment has insufficient variation to detect covariation", and confirmed the lncRNA alignments above do have adequate detection power ([doi:10.1093/bioinformatics/btaa080](https://doi.org/10.1093/bioinformatics/btaa080)) — the basis for the `undetermined` verdict and the ~10% mean-power line in step 4.
- **Rivas (*PLoS Comput. Biol.* 2023)** introduced helix-level aggregation and reported benchmarks showing it increases sensitivity in detecting conserved structure without sacrificing specificity; the same paper identifies the alignment-construction circularity artifact ([doi:10.1371/journal.pcbi.1011262](https://doi.org/10.1371/journal.pcbi.1011262)) — the basis for steps 2 and 5, and the reason the recipe requires R-scape 2.0.0.p or newer.

## Alternatives considered

- **[Predict RNA secondary structure and target-site accessibility](predict-rna-secondary-structure-and-accessibility.html) (rung 2).** The thermodynamic counterpart, and the usual upstream step: ViennaRNA gives you the structure this recipe tests. Reach for it instead when you need a fold for reagent design against a single sequence and conservation is not the question — accessibility of an siRNA target site is a thermodynamic quantity, and demanding covariation support for it would be a category error. The two are complements, not substitutes: covariation validates a structure, it does not produce one, and thermodynamics produces one without validating it.
- **Chemical probing (SHAPE, DMS-MaPseq) via the [RNA Structure Probing skill](../../catalog/tools/structure-probing.html).** Experimental rather than evolutionary evidence, and the right escalation when covariation comes back `undetermined` — no amount of statistics will rescue an alignment that lacks diversity, but a probing experiment on your actual transcript sidesteps the problem entirely. Probing also answers the in-cell question that covariation cannot.
- **Running R-scape from the command line yourself.** Entirely reasonable if you already know the flags; the skill's value is that it refuses to report a low-power negative as a rejection and keeps proposed-pair and alternative-pair results separate, which are the two mistakes that survive into published figures. If you script it directly, encode those two rules yourself.
- **[ncRNA Search](../../catalog/tools/ncrna-search.html) (rung 2).** Downstream, not alternative: once a structure is covariation-supported, a CaCoFold consensus can seed a covariance model to search for homologs.

## See also

- [Covariation Analysis (bioSkills)](../../catalog/tools/covariation-analysis.html)
- [ViennaRNA (Claude Skill)](../../catalog/tools/viennarna-structure-prediction.html) — thermodynamic folding, which this recipe validates rather than replaces.
- [RNA Structure Probing (bioSkills)](../../catalog/tools/structure-probing.html) — experimental evidence when power is inadequate.
- [ncRNA Search](../../catalog/tools/ncrna-search.html) — covariance-model homolog search downstream of a supported structure.
- [Predict RNA secondary structure and target-site accessibility](predict-rna-secondary-structure-and-accessibility.html)
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [Rivas, Clements & Eddy, "A statistical test for conserved RNA structure shows lack of evidence for structure in lncRNAs" (*Nat. Methods* 2017)](https://pubmed.ncbi.nlm.nih.gov/27819659/) — R-scape; no significant support for HOTAIR, SRA, Xist structures; published 2017; verified 2026-08-08 (this run).
- [Rivas, Clements & Eddy, "Estimating the power of sequence covariation for detecting conserved RNA structure" (*Bioinformatics* 2020)](https://pubmed.ncbi.nlm.nih.gov/32031582/) — power estimation distinguishing an adequately powered negative from an uninformative one; published 2020; verified 2026-08-08 (this run).
- [Rivas, "RNA covariation at helix-level resolution for the identification of evolutionarily conserved RNA structure" (*PLoS Comput. Biol.* 2023)](https://pubmed.ncbi.nlm.nih.gov/37450549/) — helix-level aggregation raises sensitivity without sacrificing specificity; identifies the alignment-construction circularity artifact; integrated from R-scape 2.0.0.p; published 2023; verified 2026-08-08 (this run).
- [`GPTomics/bioSkills` — `rna-structure/covariation-analysis`](https://github.com/GPTomics/bioSkills/blob/main/rna-structure/covariation-analysis/SKILL.md) — skill workflow, E-value 0.05 default, ~10% mean-power line, ~60% pairwise-identity guidance; catalog page last verified 2026-08-08.
- [R-scape (Rivas Lab)](http://eddylab.org/R-scape/) — source and documentation; catalog page last verified 2026-08-08.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=test-rna-structure-for-covariation-support&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftest-rna-structure-for-covariation-support.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
