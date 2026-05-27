---
title: Run bulk RNA-seq differential expression from a counts matrix
parent: All recipes
grand_parent: Recipes
nav_order: 8
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology, Translational Medicine, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-21
summary: Use the PyDESeq2 Claude Skill to fit a negative-binomial GLM from a counts matrix and sample-condition table, returning ranked log2 fold-change and BH-adjusted p-values.
---

# Run bulk RNA-seq differential expression from a counts matrix

Hand Claude Code a bulk RNA-seq counts matrix and a sample-condition table; get back size-factor-normalized counts, dispersion estimates, Wald-test log2 fold-changes, and BH-adjusted p-values as a pandas DataFrame.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology, Translational Medicine, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Differential expression from bulk RNA-seq is the most common biostatistical analysis in molecular biology. DESeq2's negative-binomial GLM with empirical-Bayes dispersion shrinkage is the standard, but the canonical implementation is R. Many wet-lab groups now work in Python and want to fit DESeq2 from a Jupyter notebook or a Python pipeline without round-tripping through R; PyDESeq2 (the Python reimplementation) makes that possible, but it still requires writing a non-trivial amount of glue code each time. Solved looks like: a counts matrix in, a ranked DE table out, with the design formula and the threshold choices explicit and reproducible.

## Recommended approach

1. **Install the [PyDESeq2 Claude Skill](../../catalog/tools/pydeseq2.html).** From the K-Dense scientific-skills marketplace:

   ```
   /plugin marketplace add K-Dense-AI/claude-scientific-skills
   /plugin install pydeseq2@claude-scientific-skills
   pip install pydeseq2
   ```

2. **Prepare two inputs.**

   - A counts matrix `counts.csv` — rows are genes, columns are samples, values are raw integer counts (not TPM, not FPKM). Salmon / Kallisto users should aggregate to gene level with `tximport` or `pyroe` first.
   - A sample-condition table `coldata.csv` — one row per sample, columns include `condition` and any batch / covariate variables you want in the design.

3. **Ask the skill to fit DESeq2 with an explicit design formula.** A minimal prompt:

   ```
   Use the pydeseq2 skill. Fit DESeq2 on counts.csv with coldata.csv,
   design ~ batch + condition, reference level condition="control".
   Apply default independent filtering and BH multiple-testing
   correction. Write the full results table to results/de_full.csv
   and a filtered table (padj < 0.05, |log2FC| > 1) to
   results/de_sig.csv. Also produce an MA plot and a volcano plot
   under figures/.
   ```

4. **Inspect the dispersion-vs-mean trend plot** the skill produces — a flat or upward-curving trend on the high-expression side is a red flag for QC problems upstream.

5. **For pseudobulk single-cell DE**, aggregate counts per `(sample, cell-type)` group with the [Scanpy-MCP](../../catalog/tools/scanpy.html) server first, then pass the pseudobulk matrix to PyDESeq2 with the same workflow.

## Why this assembly

Rung 2 of the simplicity ladder. Plain Claude Code can write PyDESeq2 code from documentation, but the skill encodes the right design-formula syntax, the right shrinkage choice for log2FC reporting (`apeglm`-style), and the BH-vs-IHW filtering convention so the analysis is reproducible across runs and across users. There is no need to escalate to a toolbelt — bulk DE is a single statistical procedure with a single tool, and the skill is the appropriate grain.

## Availability

Fully open. The PyDESeq2 skill is OSS in [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills); PyDESeq2 itself is MIT-licensed; no subscription or institutional access required.

## Compute requirements

Laptop-sufficient. PyDESeq2 on a typical bulk RNA-seq study (10–60 samples, ~20k genes) fits in a few minutes on a modern laptop CPU. Very large designs (hundreds of samples or many interaction terms) can take longer but still fit on a workstation; no GPU required.

## Evidence

Reported. The PyDESeq2 skill's [SKILL.md in `K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/pydeseq2/SKILL.md) documents this exact workflow — size factors, dispersion, Wald / LRT, BH correction — and is actively maintained 2025–2026 per the catalog entry. The underlying PyDESeq2 library is a published Python reimplementation of the DESeq2 algorithm and produces results numerically consistent with the R original.

No peer-reviewed benchmark of "Claude + this skill" against hand-written PyDESeq2 code is known. The reproducibility win is in the prompt-to-DataFrame contract, not in any new statistical method.

## Alternatives considered

- **Plain Claude Code, no skill.** Works for one-off analyses where you want to teach or audit every line. Reach for the skill when consistency across analyses matters.
- **Running DESeq2 in R via an Rscript bash step from Claude Code.** Valid if you already have an established R-based pipeline; PyDESeq2 is the better choice when downstream work is in Python (enrichment via gseapy, plotting via Scanpy).
- **An autonomous-science system (Biomni).** Overkill — DE is a single-step analysis; the autonomous-loop overhead is not warranted unless DE is one node in a larger generated pipeline.

## See also

- [PyDESeq2 (Claude Skill)](../../catalog/tools/pydeseq2.html)
- [AnnData (Claude Skill)](../../catalog/tools/anndata.html)
- [Scanpy-MCP](../../catalog/tools/scanpy.html) — for pseudobulk aggregation upstream of PyDESeq2.
- [Run first-pass QC on a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — upstream sister recipe for the single-cell case.

## Sources

- [PyDESeq2 skill (`SKILL.md`)](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/pydeseq2/SKILL.md) — last updated 2025–2026; verified 2026-05-21 (this run).
- [`K-Dense-AI/scientific-agent-skills` repository](https://github.com/K-Dense-AI/scientific-agent-skills) — verified 2026-05-21 (this run).
- [PyDESeq2 documentation](https://pydeseq2.readthedocs.io/) — verified 2026-05-21 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=run-bulk-rnaseq-differential-expression&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Frun-bulk-rnaseq-differential-expression.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
