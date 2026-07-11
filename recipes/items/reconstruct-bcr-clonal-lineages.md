---
title: Reconstruct B-cell clonal lineages from AIRR-seq
parent: All recipes
grand_parent: Recipes
nav_order: 20
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-11
summary: Use the Immcantation BCR Analysis skill to cluster AIRR-seq reads into clonal families, quantify somatic hypermutation and selection, and infer germline-rooted lineage trees.
---

# Reconstruct B-cell clonal lineages from AIRR-seq

Hand Claude Code an AIRR-format B-cell repertoire table and get back clonal families grouped by a data-derived distance threshold, per-clone somatic-hypermutation and selection statistics, and germline-rooted lineage trees tracing affinity maturation — as committed, re-runnable analysis rather than a one-off interactive session.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You sequenced a B-cell receptor repertoire (bulk BCR-seq or the paired heavy chain from single-cell VDJ) and ran it through IgBLAST or a comparable annotator, leaving you with an AIRR-format table of V(D)J assignments. The immunology questions come next: which reads descend from the same naive B cell (clonal families)? How much somatic hypermutation has each accumulated, and is the mutation pattern consistent with antigen-driven selection? What does the affinity-maturation tree look like? Answering these by hand is error-prone, and the single biggest mistake is clustering clones with a hardcoded distance cutoff instead of one derived from your own data's nearest-neighbor distribution.

The other footguns: rooting lineage trees without a reconstructed germline ancestor (so branch directions are meaningless); reporting a raw mutation count without normalizing for sequence length or separating replacement from silent changes; and failing to record the germline reference set and threshold, so the clonal assignments can't be reproduced when the reference database moves. "Solved" looks like: point the agent at your AIRR table, get back `clones.tsv` (clone IDs, a derived threshold, SHM frequency, selection scores) and per-clone lineage-tree files, plus a provenance record naming the germline reference release.

## Recommended approach

1. **Install the [Immcantation BCR Analysis skill](../../catalog/tools/immcantation-analysis.html).** Clone the bioSkills repo and copy the one skill (`cp -r bioSkills/tcr-bcr-analysis/immcantation-analysis ~/.claude/skills/`), following the catalog page. The skill drives the Immcantation R suite (`shazam`, `scoper`, `alakazam`, `dowser`, `tigger`) plus IgBLAST/Change-O; the simplest way to get the full toolchain is the Immcantation Docker image, which the catalog page points to.

2. **Fix your input and germline reference.** The skill expects an AIRR-format rearrangement table (`airr_rearrangement.tsv`) — the output of IgBLAST/Change-O or a single-cell VDJ annotator converted to AIRR. Pin the IMGT/germline reference set you annotated against and record its release; clonal assignment and SHM counts are only meaningful relative to that reference.

3. **Have the skill write a committed analysis script, not just answers.** A prompt:

   ```
   Use the immcantation-analysis skill to write me an R script
   bcr_lineages.R that, from airr_rearrangement.tsv:
     1. Uses shazam::distToNearest + findThreshold to DERIVE the
        clonal distance threshold from the data (report the value);
        do not hardcode a cutoff.
     2. Partitions reads into clonal families with scoper at that
        threshold, writing clones.tsv (clone_id, size, v/j call,
        junction length).
     3. Quantifies SHM frequency per sequence and per clone,
        separating replacement vs silent mutations by CDR/FWR region.
     4. Runs BASELINe selection testing (shazam) per clone and adds
        selection sigma columns.
     5. Reconstructs germline ancestors and builds codon-aware,
        germline-rooted lineage trees with dowser for the N largest
        clones, saving tree objects/plots.
     6. Writes provenance.json: Immcantation package versions, the
        IMGT germline reference release, the derived threshold,
        airr_rearrangement.tsv sha256, run date, and model id.
   Commit bcr_lineages.R; do not paste the tables back as prose I
   can't audit.
   ```

   Pin the environment with the Immcantation Docker image tag (or an `renv` lockfile of the R packages) plus the germline release string. Keep `bcr_lineages.R`, the pinned environment, `clones.tsv`, the tree outputs, and `provenance.json` under version control alongside the AIRR table.

4. **Read the results critically.** Confirm the derived threshold sits in a clean bimodal valley of the distance-to-nearest histogram — a threshold with no valley means clonal calls are unreliable (often too few sequences, or a mixed-locus table). A high replacement-to-silent ratio concentrated in CDRs with positive BASELINe selection is the signature of antigen-driven maturation. Trees should be rooted on the reconstructed germline, not an arbitrary leaf.

5. **Hand off.** Because the germline release and the derived threshold are pinned in `provenance.json`, re-running `bcr_lineages.R` reproduces the clonal partition and trees until you deliberately bump the reference. The largest expanded clones and their most-mutated leaves are natural candidates to express and test — feed a candidate's paired sequence to the [antibody–antigen complex recipe](predict-antibody-antigen-complex.html) for structural follow-up, or scan its framework for [glycosylation liabilities](scan-antibody-glycosylation-sites.html).

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill orchestrates the whole Immcantation pipeline (threshold derivation, clonal clustering, SHM/selection, lineage trees). Plain Claude Code (rung 1) could script the R packages directly, but the skill encodes the non-obvious correct-usage steps that determine whether the analysis is valid: deriving the threshold from the data rather than hardcoding it, region-aware replacement/silent scoring, and germline-rooted trees. Those are exactly the judgment calls a novice gets wrong. Rung 3+ is unnecessary: the AIRR-in / clones-and-trees-out workflow is a single well-bounded (if multi-step) analysis on one input table.

## Availability

Fully open. The Immcantation BCR Analysis skill is MIT-licensed and the Immcantation R suite plus IgBLAST/Change-O are free open-source academic software (the Docker image bundles them). IMGT germline references are freely available for academic use. All computation runs locally on your repertoire table — no account, no upload.

## Compute requirements

Laptop-sufficient for typical repertoires. Threshold derivation, clonal clustering, and SHM/selection scoring on tens of thousands of sequences run in minutes on CPU with 8–16 GB RAM. No GPU. Lineage-tree inference (`dowser`/IgPhyML) is the heaviest step and scales with clone size and count — restrict tree building to the largest N clones (as the prompt does) to keep it laptop-fast; very large repertoires (millions of reads) or many big trees benefit from a workstation.

## Evidence

Reported. The Immcantation framework is the documented, widely used standard for AIRR-seq clonal analysis, and each step the skill runs is an established, published method: data-derived clonal thresholding and SHM/selection quantification (`shazam`), spectral clonal clustering (`scoper`), repertoire diversity (`alakazam`), and germline-rooted lineage-tree inference (`dowser`). The lineage-tree problem specifically has an active methods literature confirming this is the canonical workflow — genotype-abundance-aware MST reconstruction ([Abdollahi et al., *BMC Bioinformatics* 2023](https://pubmed.ncbi.nlm.nih.gov/36849917/)), a benchmarking model for multi-round antibody evolution showing maximum-likelihood phylogenetics with short-branch contraction performs well on clonal trees ([Zhang et al., *Front. Immunol.* 2022](https://pubmed.ncbi.nlm.nih.gov/36618367/)), and interactive intraclonal-diversity tools built on the same AIRR pipeline ([Jeusset et al., *NAR Genom. Bioinform.* 2023](https://pubmed.ncbi.nlm.nih.gov/37388820/)).

No head-to-head benchmark of the *agent-driven skill* versus a hand-written Immcantation script is published — the skill buys correct usage (derived threshold, region-aware mutation scoring, germline rooting) and a pinned provenance record, not a new method. The underlying Immcantation tools are the validated components.

## Alternatives considered

- **Plain Claude Code, no skill (rung 1).** Feasible if you already run Immcantation and know to derive the threshold and root on germline. The skill exists to prevent the common errors (hardcoded threshold, un-rooted trees), so prefer it unless you are an experienced repertoire analyst.
- **Single-cell VDJ platform tools (Cell Ranger / scRepertoire).** Fine for a quick clonotype tally from 10x VDJ data, but they don't derive a data-driven SHM threshold or infer germline-rooted, codon-aware lineage trees. Use this recipe when the affinity-maturation trajectory — not just clonotype counts — is the question.
- **A dedicated tree tool (ClonalTree, IgPhyML standalone).** Reach for these only when you need a specific tree-reconstruction algorithm on already-partitioned clones; `dowser` (which the skill drives) wraps the standard options. Neither standalone tool is catalogued as a Claude component today.

## See also

- [Immcantation BCR Analysis (bioSkills)](../../catalog/tools/immcantation-analysis.html) — the skill this recipe drives.
- [Scan a therapeutic antibody for glycosylation sites](scan-antibody-glycosylation-sites.html) — downstream liability check on a selected clone.
- [Predict an antibody–antigen complex structure](predict-antibody-antigen-complex.html) — structural follow-up on an expanded clone's sequence.
- [Build a phylogenetic tree from a set of sequences](build-phylogenetic-tree-from-sequences.html) — the general (non-BCR-aware) tree counterpart.

## Sources

- [Abdollahi et al., "Reconstructing B cell lineage trees with minimum spanning tree and genotype abundances," *BMC Bioinformatics* 24:70](https://pubmed.ncbi.nlm.nih.gov/36849917/) — genotype-abundance-aware clonal-tree reconstruction; published 2023; verified 2026-07-11 (this run).
- [Zhang et al., "A scalable model for simulating multi-round antibody evolution and benchmarking of clonal tree reconstruction methods," *Front. Immunol.* 13:1014439](https://pubmed.ncbi.nlm.nih.gov/36618367/) — clonal-tree method benchmark; published 2022; verified 2026-07-11 (this run).
- [Jeusset et al., "ViCloD, an interactive web tool for visualizing B cell repertoires and analyzing intraclonal diversities," *NAR Genom. Bioinform.* 5:lqad064](https://pubmed.ncbi.nlm.nih.gov/37388820/) — AIRR-pipeline intraclonal-diversity analysis; published 2023; verified 2026-07-11 (this run).
- [Immcantation framework documentation](https://immcantation.readthedocs.io/) — the tool suite the skill drives; verified 2026-07-11 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=reconstruct-bcr-clonal-lineages&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Freconstruct-bcr-clonal-lineages.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
