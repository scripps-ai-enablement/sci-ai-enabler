---
title: Annotate TCR antigen specificity by clustering and database lookup
parent: All recipes
grand_parent: Recipes
nav_order: 1
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Validated
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-01
summary: Use the TCR-Epitope Binding skill to group CDR3 sequences into shared-specificity clusters and match them against VDJdb, IEDB, and McPAS-TCR.
---

# Annotate TCR antigen specificity by clustering and database lookup

Hand Claude Code a table of CDR3β (or paired αβ) sequences and get back specificity groups — TCRs that likely see the same epitope — with database-matched antigen annotations where they exist, as a committed script with the clustering parameters pinned.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Validated |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have a repertoire — expanded clonotypes from a single-cell VDJ run, a bulk TCRβ dataset from a vaccine trial, or tumor-infiltrating T cells from a resection — and the obvious next question is *what are these cells seeing?* Tetramer panels only cover epitopes you already suspect, and the repertoire is mostly sequences no database has ever recorded.

The tempting move is to run a supervised TCR–epitope predictor over every clonotype and read off antigens. That does not work for epitopes the model has not seen in training, and the failure is quiet: the training data is dominated by a handful of immunodominant viral epitopes and has no true negatives, so a confident prediction against a novel antigen is essentially a prior over the training set. The defensible task is the unsupervised one — group TCRs by CDR3 similarity into candidate specificity groups, then ask a curated database whether any member of the group has a known antigen, and carry the group's HLA restriction as a hypothesis. "Solved" looks like a `tcr_clusters.csv` where each clonotype has a cluster id, cluster size, the motif or distance basis for the grouping, any VDJdb/IEDB/McPAS-TCR hit with its confidence score, and an honest blank where nothing matched.

## Recommended approach

1. **Install the [TCR-Epitope Binding skill](../../catalog/tools/tcr-epitope-binding.html).** Clone the bioSkills repo and copy the one skill (`cp -r bioSkills/immunoinformatics/tcr-epitope-binding ~/.claude/skills/`), following the catalog page. The skill declares its clustering dependencies (tcrdist3, GLIPH2, clusTCR, GIANA) and prompts you to install them on first use; some bundled databases need a separate download.

2. **Fix your input and your cohort boundary.** Save the repertoire as `tcrs.csv` with at minimum `cdr3b`, `v_gene`, `j_gene`, and a clone count or frequency; add `cdr3a` if you have paired chains, and a `subject_id` column. Cluster *within one cohort at a time*: pooling subjects with different HLA types mixes restriction elements and inflates cluster sizes with sequences that cannot share an epitope. If you know the subjects' HLA genotypes, keep them in a side file — GLIPH2-style methods use them to infer restriction.

3. **Have the skill write a committed script.** A prompt:

   ```
   Use the tcr-epitope-binding skill to write me a script
   cluster_tcrs.py that:
     1. Loads tcrs.csv, QCs the CDR3s (productive, in-frame,
        conserved C...F, sane length) and reports what it dropped.
     2. Clusters within each subject cohort with tcrdist3 (paired
        if cdr3a is present, else beta-only) AND with GLIPH2, and
        keeps both cluster assignments as separate columns rather
        than merging them.
     3. Matches every CDR3 against VDJdb, IEDB, and McPAS-TCR,
        keeping the database, epitope, source antigen, HLA
        restriction, and the VDJdb confidence score; filters out
        confidence-0 VDJdb records by default.
     4. Propagates a database hit to the cluster level only as a
        *candidate* annotation, with the fraction of cluster
        members supporting it, and leaves unmatched clusters blank.
     5. Writes tcr_clusters.csv plus a cluster_summary.csv (size,
        subjects represented, expansion, candidate antigen,
        supporting fraction, inferred HLA if GLIPH2 gave one).
     6. Writes provenance.json: tcrdist3 / GLIPH2 versions, the
        distance radius and GLIPH2 parameters used, each
        database's release date and record count, input sha256,
        run date, model id.
   Commit cluster_tcrs.py; do not summarize antigens in prose
   that I cannot trace back to a row.
   ```

   Pin the environment with a `requirements.txt` and commit the script, `tcr_clusters.csv`, `cluster_summary.csv`, and `provenance.json`. The database release dates in `provenance.json` matter — VDJdb and IEDB grow continuously, so an unannotated cluster today may match next quarter.

4. **Read the clusters with the right expectations.** Cluster purity and retention trade off against each other, and different algorithms sit at different points on that curve — which is why step 3 keeps two assignments instead of one. A cluster that both methods recover, spans multiple subjects, and is clonally expanded in the condition of interest is a strong candidate for antigen discovery. A singleton with one low-confidence database hit is not an annotation.

5. **Validate before you believe it.** Candidate specificity groups go to a functional readout — tetramer staining, an antigen-screening library, or TCR re-expression in a reporter line. If you want a per-pair score to rank which cluster to chase first, the skill can run ERGO-II / NetTCR / pMTnet, but treat those numbers as a within-cohort ordering, not as evidence of specificity for a novel epitope.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill covers clustering, database matching, and the interpretation rules. Plain Claude Code (rung 1) can `pip install tcrdist3` and compute a distance matrix, but the thing that makes the output trustworthy is knowing which task is defensible: the skill is explicit that unsupervised clustering plus curated lookup is the real capability and that supervised prediction on unseen epitopes largely does not work. That framing is the deliverable as much as the clusters are. Rung 3+ is unnecessary — this is one analysis with one input table.

## Availability

Fully open. The skill is MIT-licensed, tcrdist3 and clusTCR are open source, and GLIPH2 is free for academic use. VDJdb is openly distributed, and IEDB and McPAS-TCR are freely accessible; several of the bundled supervised predictors require separate registration from their authors and are optional here. Everything runs locally — repertoire sequences do not leave the machine. If the repertoires come from human subjects, the usual consent and data-governance terms apply to the input, not to the tooling.

## Compute requirements

Laptop-sufficient for typical cohorts. tcrdist3 on a few thousand clonotypes takes seconds to minutes on CPU; a few tens of thousands is still comfortable in memory. The cost is quadratic in clonotype count, so a bulk repertoire of hundreds of thousands of unique CDR3s needs either a sparse-radius mode or a subsample — GLIPH2 was specifically re-engineered to scale past the ~10,000-sequence ceiling of the original GLIPH and handles millions of sequences. Database matching is trivial once the databases are downloaded (a few hundred MB).

## Evidence

Validated. The clustering methods this recipe drives have been benchmarked head-to-head against a unified reference set. **Nine TCR clustering methods** were compared on a curated database of **190,670 human TCRs with known specificities for 2,313 epitopes across 121 organisms**, assembled from IEDB, McPAS-TCR, and VDJdb: DeepTCR gave the best retention and sensitivity, while **ClusTCR, TCRMatch, and GLIPH2 excelled in cluster purity** at lower retention, with GIANA and iSMART producing smaller antigen-specific clusters — the results held on an independent labeled 10x Genomics dataset ([Jouannet et al., *NAR Genomics and Bioinformatics* 2025](https://pubmed.ncbi.nlm.nih.gov/41267899/)). A separate comparison of neighborhood-enrichment methods (ALICE, TCRNET, GLIPH2, tcrdist3) on LCMV, Sputnik V vaccination, and *M. tuberculosis* datasets found ALICE and TCRNET achieved higher area under the precision-recall curve on most datasets ([Lupyr et al., *Briefings in Bioinformatics* 2025](https://pubmed.ncbi.nlm.nih.gov/40996146/)) — a useful caution that no single clusterer dominates, and the reason this recipe keeps two assignments.

The approach has produced real antigen discoveries. GLIPH2 clustering of **19,044 TCRβ sequences from 58 latently *M. tuberculosis*-infected individuals**, paired with a genome-wide antigen screen, identified PPE proteins as T-cell targets ([Huang et al., *Nature Biotechnology* 2020](https://pubmed.ncbi.nlm.nih.gov/32341563/)); the same method on **778,938 TCRβ sequences from 178 non-small-cell lung cancer patients** yielded **over 66,000 shared-specificity groups, 435 of them clonally expanded and tumor-enriched**, one of which was deconvoluted to a TMEM161A epitope and cross-reactive EBV/*E. coli* peptides ([Chiou et al., *Immunity* 2021](https://pubmed.ncbi.nlm.nih.gov/33691136/)). In a 166-person tuberculosis cohort, GLIPH2 groups separated control from progression and nominated vaccine-priority antigens ([Musvosvi et al., *Nature Medicine* 2023](https://pubmed.ncbi.nlm.nih.gov/36604540/)).

No benchmark compares the *agent-driven skill* against a hand-run tcrdist3 pipeline; the skill contributes correct method selection, the cohort-boundary discipline, and a pinned provenance record, not a new algorithm.

## Alternatives considered

- **[Analyze a single-cell TCR repertoire alongside gene expression](analyze-single-cell-tcr-repertoire.html) (rung 2, upstream).** Reach for that first if you have not yet defined clonotypes or quantified expansion — it produces the expanded-clonotype table that is the natural input here. Run this recipe on its output when the question shifts from "which clones expanded" to "what are they seeing".
- **Supervised TCR–epitope prediction alone.** Tempting when you have a specific epitope in mind and want to score every clonotype against it. Defensible only when your epitope is well represented in training data; for a novel antigen, the clustering path plus a wet-lab screen is the honest route.
- **[Reconstruct BCR clonal lineages](reconstruct-bcr-clonal-lineages.html).** The B-cell counterpart. BCRs hypermutate, so the analogous grouping is germline-rooted lineage inference rather than similarity clustering — a different problem with a different tool.

## See also

- [TCR-Epitope Binding (bioSkills)](../../catalog/tools/tcr-epitope-binding.html) — the skill this recipe drives.
- [Analyze a single-cell TCR repertoire alongside gene expression](analyze-single-cell-tcr-repertoire.html) — the upstream clonotype and expansion analysis.
- [Reconstruct BCR clonal lineages](reconstruct-bcr-clonal-lineages.html) — the B-cell repertoire counterpart.
- [Prioritize tumor neoantigens for a personalized cancer vaccine](prioritize-tumor-neoantigens-for-a-vaccine.html) — the antigen side; pair the two to ask whether a predicted neoantigen has a matching specificity group.
- [Scan a protein for candidate CD8 T-cell epitopes](scan-protein-for-cd8-t-cell-epitopes.html) — generate the candidate epitopes a cluster might be recognizing.

## Sources

- [Jouannet et al., "Benchmarking unsupervised methods for inferring TCR specificity," *NAR Genomics and Bioinformatics* 7:lqaf150](https://pubmed.ncbi.nlm.nih.gov/41267899/) — nine methods, 190,670 TCRs / 2,313 epitopes; purity-vs-retention tradeoff; published 2025; verified 2026-08-01 (this run).
- [Lupyr et al., "Neighborhood enrichment for the identification of antigen-specific T-cell receptors," *Briefings in Bioinformatics*](https://pubmed.ncbi.nlm.nih.gov/40996146/) — ALICE/TCRNET vs GLIPH2/tcrdist3 AUPRC comparison; published 2025; verified 2026-08-01 (this run).
- [Huang et al., "Analyzing the Mycobacterium tuberculosis immune response by T-cell receptor clustering with GLIPH2 and genome-wide antigen screening," *Nature Biotechnology* 38:1194](https://pubmed.ncbi.nlm.nih.gov/32341563/) — GLIPH2 method, 19,044 TCRβ from 58 subjects, PPE antigens; published 2020; verified 2026-08-01 (this run).
- [Chiou et al., "Global analysis of shared T cell specificities in human non-small cell lung cancer enables HLA inference and antigen discovery," *Immunity* 54:586](https://pubmed.ncbi.nlm.nih.gov/33691136/) — 778,938 TCRβ, 66,000 specificity groups, 435 tumor-enriched; published 2021; verified 2026-08-01 (this run).
- [Musvosvi et al., "T cell receptor repertoires associated with control and disease progression following Mycobacterium tuberculosis infection," *Nature Medicine* 29:258](https://pubmed.ncbi.nlm.nih.gov/36604540/) — 166-person cohort, 24 specificity groups split by outcome; published 2023; verified 2026-08-01 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=annotate-tcr-specificity-by-clustering&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fannotate-tcr-specificity-by-clustering.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
