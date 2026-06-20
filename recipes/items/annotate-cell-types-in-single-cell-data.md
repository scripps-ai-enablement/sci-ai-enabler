---
title: Annotate cell types in a single-cell dataset
parent: All recipes
grand_parent: Recipes
nav_order: 2
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology, Neuroscience]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-20
summary: Use the SciAgent CellTypist skill to put reference-backed cell-type labels on a QC'd AnnData, escalating to the popV consensus skill when you need ensemble uncertainty.
---

# Annotate cell types in a single-cell dataset

Hand Claude Code a clustered, QC'd `.h5ad` and get back per-cell and per-cluster cell-type labels with confidence scores, drawn from a pre-trained reference rather than hand-curated markers.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology, Neuroscience |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

After QC and clustering, every single-cell project hits the same wall: the Leiden clusters need names. Doing it by hand means pulling marker genes per cluster, cross-referencing CellMarker / PanglaoDB, and arguing about whether cluster 7 is a CD8 T cell or an NK cell. It is slow, subjective, and irreproducible across analysts. Automated classifiers (CellTypist's logistic-regression models, popV's consensus ensemble) solve most of this for the common tissues, but each carries footguns: the wrong reference model gives confidently wrong labels, and single-method calls hide uncertainty at cell-state boundaries. Solved looks like: a labeled AnnData with both per-cell and majority-vote cluster labels, a confidence score per call, and a record of which reference model produced them.

## Recommended approach

1. **Start from a QC'd, normalized AnnData.** Produce it with the [single-cell RNA-seq QC recipe](qc-single-cell-rna-seq.html) and a Scanpy clustering pass; CellTypist expects log1p-normalized counts (10,000 counts per cell) in `adata.X`.

2. **Install the [CellTypist skill](../../catalog/tools/celltypist-cell-annotation.html)** from the SciAgent-Skills collection:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   /plugin install sciagent-skills
   ```

   Confirm it appears under `/plugin` → Installed. The [single-cell annotation guide skill](../../catalog/tools/single-cell-annotation-guide.html) ships in the same collection and encodes the tier-1/2/3 decision framework — load it too so Claude picks the right model and resolution.

3. **Invoke CellTypist with the matching reference model.** Pick the model for your tissue (`Immune_All_Low.pkl` for the cross-tissue immune atlas, plus gut / lung / brain / fetal / cancer-microenvironment models). A minimal prompt:

   ```
   Run the celltypist-cell-annotation skill on data/sample01_qc.h5ad.
   Use the Immune_All_Low model with majority_voting=True over the
   existing leiden clusters. Write per-cell labels, majority-vote
   cluster labels, and confidence scores back into the AnnData and
   save to data/sample01_annotated.h5ad.
   ```

4. **Sanity-check against known markers.** Have Claude plot 2–3 canonical markers per assigned label (e.g., `CD3D`/`CD8A` for CD8 T, `MS4A1` for B, `NKG7` for NK) and flag any cluster whose majority label disagrees with its marker expression. Low-confidence clusters are where manual review pays off.

5. **Escalate to consensus only if single-method confidence is poor.** If CellTypist confidence is low across several clusters, or you need quantified annotation uncertainty for a novel state, run the [popV skill](../../catalog/tools/popv-cell-annotation.html) against a labeled reference (Tabula Sapiens pre-trained models cover 20 organs). popV runs eight classifiers and reports an agreement score per cell; clusters where the methods disagree are your real uncertainty.

## Why this assembly

Rung 2 of the simplicity ladder for the common case: one skill (CellTypist) does the job, with the annotation-guide skill as a planning aid. Plain Claude Code can write the marker-overlap logic from scratch, but it would re-derive a reference that CellTypist already ships as 45+ peer-reviewed models — rung 1 reproduces the subjective, irreproducible manual workflow this recipe is meant to replace.

Escalate to rung 3 (CellTypist + popV + a labeled reference) only when single-method confidence is poor or you need ensemble uncertainty. popV's value is the agreement score across eight classifiers; that is the specific thing rung 2 cannot give you. No autonomous system is warranted — annotation is a bounded, single-step transfer problem.

## Availability

Fully open. CellTypist, popV, and the annotation guide are OSS skills in the SciAgent-Skills collection (MIT, BSD-3-Clause, and CC-BY-4.0 respectively), free with any Claude plan. The underlying CellTypist (`Teichlab/celltypist`) and popV (`YosefLab/popV`) packages and their pre-trained reference models are public. No subscription or institutional account required.

## Compute requirements

Laptop-sufficient. CellTypist inference on a 10k–100k-cell dataset runs in seconds to a few minutes on a modern laptop with 16 GB RAM; it is logistic regression, no GPU. popV is heavier: in fast mode (pre-trained models only) it annotates 100k query cells in ~5 minutes; inference mode ~30 minutes; full retrain mode ~1 hour per 100k cells. Reserve popV retrain for when you are adding a custom reference, not for routine calls.

## Evidence

Reported. Both classifiers are peer-reviewed with quantitative validation. CellTypist was introduced in the cross-tissue immune cell atlas ([Domínguez Conde et al., *Science* 2022](https://www.science.org/doi/10.1126/science.abl5197)), annotating ~360,000 cells across 16 tissues with a hierarchical (32-cell-type high-resolution) logistic-regression model. popV ([Ergen et al., *Nat. Genet.* 2024](https://www.nature.com/articles/s41588-024-01993-3)) demonstrated that its consensus uncertainty score surfaced genuine reference-atlas labeling errors (mislabeled CD8+ T cells in a Human Lung Cell Atlas query against a Tabula Sapiens reference). The skills wrap these tools and ship in the BixBench-evaluated SciAgent-Skills collection.

No peer-reviewed benchmark of "Claude + CellTypist skill" against a human analyst is known; the agent loop adds orchestration and a marker sanity-check, not a new classification method. The quantitative anchors are the two method papers above.

## Alternatives considered

- **Plain Claude Code, no skill.** Claude can pull per-cluster markers and assign labels by overlap with a marker list you paste in. Reach for this for an exotic tissue with no pre-trained model, or to teach the manual workflow — but expect the subjectivity this recipe exists to remove.
- **popV first, skipping CellTypist.** Defensible when you already have a well-curated labeled reference and want uncertainty from the start. For most users CellTypist is faster and its immune/tissue models are sufficient; reserve popV for the consensus step.
- **An autonomous-science system (Biomni).** Overkill for annotation alone. Reach for it only when annotation is one node of a larger autonomous pipeline.

## See also

- [CellTypist (Claude Skill)](../../catalog/tools/celltypist-cell-annotation.html)
- [popV (Claude Skill)](../../catalog/tools/popv-cell-annotation.html)
- [Single-Cell Annotation Guide (Claude Skill)](../../catalog/tools/single-cell-annotation-guide.html)
- [Run first-pass QC on a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html)
- [Infer transcription-factor and pathway activities from expression](infer-tf-and-pathway-activities-from-expression.html)
- [Infer cell-cell communication from scRNA-seq](infer-cell-cell-communication-from-scrnaseq.html)

## Sources

- [Domínguez Conde et al., *Science* 2022 (CellTypist)](https://www.science.org/doi/10.1126/science.abl5197) — published 2022-05-13; verified 2026-06-20 (this run).
- [Ergen et al., *Nat. Genet.* 2024 (popV)](https://www.nature.com/articles/s41588-024-01993-3) — published 2024-11-20; verified 2026-06-20 (this run).
- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) — community OSS skill collection; verified 2026-06-20 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=annotate-cell-types-in-single-cell-data&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fannotate-cell-types-in-single-cell-data.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
