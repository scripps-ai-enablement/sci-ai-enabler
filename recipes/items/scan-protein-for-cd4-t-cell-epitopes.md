---
title: Scan a protein for candidate CD4 T-cell (helper) epitopes
parent: All recipes
grand_parent: Recipes
nav_order: 23
problem_class: Experimental design
subject_areas: [Immunology and Microbiology]
evidence_level: Validated
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-25
summary: Use the MHC Class II Prediction skill to rank a protein's peptides for HLA-DR/DQ/DP binding, nominating CD4 T-helper epitope candidates for vaccine design.
---

# Scan a protein for candidate CD4 T-cell (helper) epitopes

Hand Claude Code a protein sequence (a pathogen antigen or a tumor mutant) and a set of HLA class II alleles, and get back a ranked table of ~15-mer peptides scored for HLA-DR/DQ/DP binding, so you can nominate CD4 T-helper epitope candidates for a subunit or multi-epitope vaccine — anchored to the exact predictor versions you ran, and read with the reliability caveats class II demands.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Validated |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Protective antibody and durable CD8 responses both depend on CD4 T-helper cells, so a subunit or multi-epitope vaccine design has to include peptides that bind MHC class II (HLA-DR/DQ/DP) and are seen by CD4 T cells. As with class I, testing every peptide in a proliferation or cytokine assay is prohibitive, so the standard move is to pre-rank peptides computationally and only order the top helper-epitope candidates.

Class II is harder than class I, and the footguns are worse. The open-ended binding groove means the immunogenic 9-mer core sits inside a longer (~13–25-mer) peptide, and the *register* of that core is ambiguous — you score peptides, not fixed-length k-mers. Accuracy is markedly lower than class I and asymmetric across isotypes (DR > DP > DQ). DQ and DP are alpha/beta heterodimers, so it is easy to request a non-existent alpha/beta pairing and get a meaningless score. Predicted binding is necessary but far from sufficient for immunogenicity. "Solved" looks like: point the agent at your antigen FASTA and a validated allele list, get back an `epitopes_classII.csv` ranked by presentation `%Rank` per allele with looser class II cutoffs, plus a provenance record naming the exact predictor versions.

## Recommended approach

1. **Install the [MHC Class II Prediction skill](../../catalog/tools/mhc-class-ii-prediction.html).** Clone the bioSkills repo and copy the one skill (`cp -r bioSkills/immunoinformatics/mhc-class-ii-prediction ~/.claude/skills/`), following the catalog page. The skill drives **NetMHCIIpan-4.3** (pan-DR/DQ/DP) and **MixMHC2pred-2.0** (immunopeptidome-grounded); install those free academic downloads when the skill prompts on first use.

2. **Fix your inputs.** Save the antigen as `antigen.fasta` and write your HLA class II alleles into `alleles_classII.txt` using the predictor's exact syntax — DR is a single beta chain (`DRB1_0701`), while DQ/DP are explicit alpha/beta pairings (`HLA-DQA10501-DQB10201`). Use real, observed heterodimers (a common DR/DQ/DP reference panel or the patient genotype), not every combinatorial alpha/beta pair. For a class II neoantigen, include both the mutant window and the matched wild-type.

3. **Have the skill write a committed script, not just an answer.** A prompt:

   ```
   Use the mhc-class-ii-prediction skill to write me a script
   scan_classII_epitopes.py that:
     1. Slides a 15-mer window (step 1) across antigen.fasta.
     2. Scores every peptide against each allele in
        alleles_classII.txt with NetMHCIIpan-4.3 (EL score + %Rank +
        the predicted 9-mer core register). If MixMHC2pred-2.0 is
        installed, add its columns too.
     3. Writes epitopes_classII.csv with: peptide, source_position,
        allele, core_9mer, el_score, percent_rank, tool.
     4. Flags strong binders as percent_rank <= 1.0 and weak as
        <= 5.0 (class II cutoffs, not class I), and sorts within each
        allele by percent_rank.
     5. Writes provenance.json: NetMHCIIpan version + data release,
        MixMHC2pred version if used, antigen.fasta sha256, the exact
        allele strings, window/step, run date, and model id.
   Commit scan_classII_epitopes.py; do not paste the ranked peptides
   back as prose I can't audit.
   ```

   Pin the environment with a `requirements.txt` (`pandas`; the predictors are external binaries — record their versions in `provenance.json` rather than pip-pinning). Keep `scan_classII_epitopes.py`, the pinned env, and `provenance.json` under version control alongside `antigen.fasta` and `alleles_classII.txt`.

4. **Read the ranking with class II eyes.** Use `%Rank` (not raw affinity) to compare across alleles, and apply the looser class II thresholds (`≤ 1%` strong, `≤ 5%` weak) — the class I `0.5%/2%` cutoffs are too strict here. Collapse overlapping 15-mers that share the same predicted 9-mer core into a single candidate region; a run of high-scoring windows around one core is one epitope, not a dozen. Trust DR calls more than DP, and DP more than DQ. For a broad-coverage vaccine, favor cores conserved across pathogen strains and presented by multiple common alleles.

5. **Order and hand off.** Take the top helper-epitope regions into synthesis and a functional readout (CD4 proliferation, IFN-γ/IL-2 ELISpot, or activation-induced marker assay). Because the predictor versions and data release are pinned in `provenance.json`, re-running `scan_classII_epitopes.py` reproduces the ranking. To assemble a minimal peptide set with broad HLA + pathogen coverage across the CD4 and CD8 shortlists, feed both epitope tables into a coverage optimizer (e.g. PopCover-2.0) as a downstream step — that selection is outside this recipe.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill does the whole job (windowing, per-allele scoring, register-aware core extraction, class II `%Rank` interpretation). Plain Claude Code (rung 1) could install NetMHCIIpan and script it, but class II is exactly where naive usage goes wrong: the alpha/beta heterodimer pairing trap, register ambiguity, the DR > DP > DQ accuracy asymmetry, and the wrong (class I) `%Rank` cutoffs. The skill encodes those distinctions and states them as caveats, which is what makes the output trustworthy. Rung 3+ is unnecessary: peptide-MHC-II scanning against published predictors is a single well-bounded step.

## Availability

Fully open. The MHC Class II Prediction skill is MIT-licensed and runs locally. NetMHCIIpan-4.3 and MixMHC2pred-2.0 are free for academic use but require a separate registration/download from their vendors (DTU Health Tech and the Gfeller lab respectively). Sequences are scored locally once the binaries are installed — the antigen does not leave the machine. Commercial use requires checking the predictors' own licenses.

## Compute requirements

Laptop-sufficient. Sliding a 15-mer window across a single protein (a few hundred residues) yields a few hundred peptides; scoring them against a handful of class II alleles with NetMHCIIpan takes seconds to a couple of minutes on CPU. No GPU. A whole-proteome scan (thousands of proteins) is embarrassingly parallel — batch per protein — and still fits on a workstation; class II is somewhat slower per peptide than class I because of the register search.

## Evidence

Validated. The predictors this recipe drives are the field-standard, benchmarked methods for CD4 epitope prediction, and the exact NetMHCIIpan → CD4-epitope-shortlist step is used in current published vaccine-design work. A structure-guided multi-epitope vaccine design against *Neisseria gonorrhoeae* used **NetMHCIIpan-4.1** to prioritize CD4 epitopes across 48 clinical genomes, nominating a lead HLA-DRB1\*07:01 epitope (`%Rank 1.4`, IC50 = 640 nM) that was then validated by Rosetta docking and 100 ns MD ([Yakobi & Nwodo, *Biochem. Biophys. Rep.* 2025](https://pubmed.ncbi.nlm.nih.gov/41208833/)). Downstream peptide-set selection over predicted CD4/CD8 epitopes with HLA + pathogen coverage optimization (PopCover-2.0) was experimentally confirmed by T-cell responses in SARS-CoV-2-infected donors ([Nilsson et al., *Front. Immunol.* 2021](https://pubmed.ncbi.nlm.nih.gov/34484239/)). Integrative methods have long shown that class II binding *alone* over-predicts CD4 epitopes, motivating the register-aware, caveat-flagged reading this skill enforces ([Schneidman-Duhovny et al., *PLoS ONE* 2018](https://pubmed.ncbi.nlm.nih.gov/30399156/)).

No head-to-head benchmark of the *agent-driven skill* versus a hand-typed NetMHCIIpan command exists — the skill buys correct class II usage (register handling, heterodimer pairing, the right cutoffs) and a pinned, auditable provenance file, not a new prediction method. The underlying predictors are the validated components, and class II remains materially less accurate than class I regardless of interface.

## Alternatives considered

- **The CD8/MHC-I sibling ([scan a protein for CD8 T-cell epitopes](scan-protein-for-cd8-t-cell-epitopes.html)).** Reach for it when you want cytotoxic (killer) T-cell epitopes for the same antigen. A complete vaccine antigen analysis usually runs both this class II recipe (helper epitopes) and the class I recipe (CD8 epitopes) and then optimizes a joint peptide set. Class I predictions are substantially more reliable.
- **Plain Claude Code, no skill (rung 1).** Workable if you already know NetMHCIIpan's allele syntax and the class II `%Rank` conventions. The skill exists precisely to prevent the class II-specific mistakes (heterodimer pairing, register, wrong cutoffs), so prefer it unless you are an experienced immunoinformatician doing a one-off.
- **The broader [Epitope Prediction skill](../../catalog/tools/epitope-prediction.html).** Reach for it when you also want B-cell (antibody) epitopes on the same antigen. This recipe stays focused on the CD4/MHC-II question and drives the dedicated class II predictors.
- **IEDB web tools (no agent).** Convenient for a quick single-peptide check, but a web run leaves no pinned-version provenance and does not scale to a proteome scan.

## See also

- [MHC Class II Prediction (bioSkills)](../../catalog/tools/mhc-class-ii-prediction.html) — the skill this recipe drives.
- [Scan a protein for candidate CD8 T-cell epitopes](scan-protein-for-cd8-t-cell-epitopes.html) — the CD8/MHC-I sibling; run both for a full vaccine antigen analysis.
- [Epitope Prediction (bioSkills)](../../catalog/tools/epitope-prediction.html) — B-cell and antibody epitopes on the same antigen.
- [Predict an antibody–antigen complex structure](predict-antibody-antigen-complex.html) — the structural, antibody-side counterpart.

## Sources

- [Yakobi & Nwodo, "Structure-guided in silico design of a methionine aminopeptidase-derived multi-epitope vaccine candidate against *Neisseria gonorrhoeae*," *Biochem. Biophys. Rep.* 41:102323](https://pubmed.ncbi.nlm.nih.gov/41208833/) — NetMHCIIpan-4.1 CD4 epitope prioritization across 48 genomes, lead DRB1\*07:01 epitope validated by docking + MD; published 2025; verified 2026-07-25 (this run).
- [Nilsson et al., "PopCover-2.0. Improved Selection of Peptide Sets With Optimal HLA and Pathogen Diversity Coverage," *Front. Immunol.* 12:728936](https://pubmed.ncbi.nlm.nih.gov/34484239/) — CD4/CD8 epitope-set coverage optimization, T-cell responses experimentally confirmed in SARS-CoV-2 donors; published 2021; verified 2026-07-25 (this run).
- [Schneidman-Duhovny et al., "Predicting CD4 T-cell epitopes based on antigen cleavage, MHCII presentation, and TCR recognition," *PLoS ONE* 13:e0206654](https://pubmed.ncbi.nlm.nih.gov/30399156/) — class II binding alone over-predicts CD4 epitopes; motivates register-aware, caveat-flagged reading; published 2018; verified 2026-07-25 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=scan-protein-for-cd4-t-cell-epitopes&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fscan-protein-for-cd4-t-cell-epitopes.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
