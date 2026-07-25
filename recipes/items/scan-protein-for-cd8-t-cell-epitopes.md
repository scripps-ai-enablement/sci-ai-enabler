---
title: Scan a protein for candidate CD8 T-cell epitopes
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
summary: Use the MHC Binding Prediction skill to rank a protein's peptides for MHC class I binding and presentation, nominating CD8 T-cell epitope and neoantigen candidates.
---

# Scan a protein for candidate CD8 T-cell epitopes

Hand Claude Code a protein sequence (a pathogen antigen or a tumor mutant) and a set of patient HLA class I alleles, and get back a ranked table of 8–11-mer peptides scored for MHC-I binding and natural presentation, so you can order a short list of candidate CD8 T-cell epitopes to test — anchored to the exact predictor versions you ran.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Validated |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have an antigen — a viral protein, a bacterial surface protein, or a tumor sequence carrying a somatic mutation — and you want to know which short peptides from it are likely to be displayed on MHC class I and seen by CD8 T cells. Synthesizing and testing every 9-mer in a tetramer or ELISpot assay is prohibitively expensive, so the standard move is to computationally pre-rank peptides and only order the top candidates. The question is well defined: for a given set of HLA-A/B/C alleles, which peptides bind and are naturally presented?

The footguns are specific. Ranking on raw binding affinity (nM) misses the processing/presentation step that eluted-ligand models capture. Comparing raw scores *across* alleles is invalid — you must use the predictor's `%Rank` for that. Rare or non-human alleles push pan-models into extrapolation error. And predicted binding is necessary but not sufficient for immunogenicity, so the output is a candidate list to test, not a set of confirmed epitopes. "Solved" looks like: point the agent at your antigen FASTA and your allele list, get back a `epitopes.csv` ranked by presentation `%Rank` per allele, plus a provenance record naming the exact predictor versions and model weights.

## Recommended approach

1. **Install the [MHC Binding Prediction skill](../../catalog/tools/mhc-binding-prediction.html).** Clone the bioSkills repo and copy the one skill (`cp -r bioSkills/immunoinformatics/mhc-binding-prediction ~/.claude/skills/`), following the catalog page. Install the pip-installable predictor first: `pip install mhcflurry && mhcflurry-downloads fetch`. MHCflurry alone runs fully locally with no registration; NetMHCpan-4.1 and MixMHCpred are optional separate academic downloads that widen allele coverage.

2. **Fix your inputs.** Save the antigen as `antigen.fasta` and write your HLA class I alleles into `alleles.txt` (e.g., `HLA-A*02:01`, `HLA-B*07:02`, `HLA-C*07:02` — the patient's genotype, or a supertype panel for population coverage). For a tumor neoantigen, include both the mutant peptide window and the matched wild-type so you can flag differential binding.

3. **Have the skill write a committed script, not just an answer.** A prompt:

   ```
   Use the mhc-binding-prediction skill to write me a script
   scan_epitopes.py that:
     1. Tiles antigen.fasta into all 8-, 9-, 10-, and 11-mers.
     2. Scores every peptide against each allele in alleles.txt with
        MHCflurry (presentation score + affinity + %Rank). If
        NetMHCpan-4.1/MixMHCpred are installed, add their columns too.
     3. Writes epitopes.csv with: peptide, length, source_position,
        allele, affinity_nM, presentation_score, percent_rank.
     4. Flags strong binders as percent_rank <= 0.5 and weak as
        <= 2.0, and sorts within each allele by percent_rank.
     5. Writes provenance.json: MHCflurry version + downloaded model
        release, NetMHCpan/MixMHCpred versions if used, antigen.fasta
        sha256, allele list, the length set, run date, and model id.
   Commit scan_epitopes.py; do not paste the ranked peptides back as
   prose I can't audit.
   ```

   Pin the environment with a `requirements.txt` (`mhcflurry` at a fixed version, `pandas`). Keep `scan_epitopes.py`, the pinned env, and `provenance.json` under version control alongside `antigen.fasta` and `alleles.txt`.

4. **Read the ranking with the right column.** Use `percent_rank` (not raw nM) to compare across alleles and to set the shortlist cutoff — `%Rank ≤ 0.5` for strong binders, `≤ 2.0` for the wider net. Presentation score (eluted-ligand-trained) is the more biologically grounded ranking than affinity alone. For neoantigens, keep candidates where the mutant binds substantially better than the wild-type (a larger `%Rank` gap), which favors a mutation-specific T-cell response.

5. **Order and hand off.** Take the top peptides per allele into synthesis and a functional readout (tetramer, ELISpot, or activation-induced marker assay). Because the predictor versions and model release are pinned in `provenance.json`, re-running `scan_epitopes.py` reproduces the ranking. To also assess antibody (B-cell) or class II epitopes on the same antigen, hand the FASTA to the [broader epitope-prediction recipe](#see-also) path via the Epitope Prediction skill.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill does the whole job (tiling, per-allele scoring, `%Rank` interpretation). Plain Claude Code (rung 1) could `pip install mhcflurry` and script it, but the skill encodes the practical distinctions that trip people up: eluted-ligand vs affinity scoring, `%Rank` vs raw nM for cross-allele comparison, and the abundance-bias and rare-allele failure modes. Those judgment calls are exactly what makes the output trustworthy, so the skill earns its place. Rung 3+ is unnecessary: peptide-MHC scanning against published predictors is a single well-bounded step.

## Availability

Fully open. The MHC Binding Prediction skill is MIT-licensed. MHCflurry is open-source and runs entirely on your machine with a free model download — no account, no upload. NetMHCpan-4.1 and MixMHCpred are free for academic use but require a separate registration/download from their vendors; they are optional here and only widen allele coverage. Sequences never leave the machine when using MHCflurry.

## Compute requirements

Laptop-sufficient. Tiling a single protein (a few hundred residues) into 8–11-mers yields a few thousand peptides; scoring them against a handful of alleles with MHCflurry takes seconds to a couple of minutes on CPU. No GPU. Scanning a whole proteome (thousands of proteins) is embarrassingly parallel — batch per protein — and still fits comfortably on a workstation.

## Evidence

Validated. The predictors this recipe drives are the field-standard, quantitatively benchmarked methods. In a comprehensive vaccinia-virus model-system benchmark, neural-network methods trained on both binding-affinity and eluted-ligand data — **NetMHCpan-4.0 and MHCflurry** — were the best-performing tools, capturing **more than half of the major T-cell epitopes in the top 277 predictions out of 767,788 candidate peptides** across the proteome ([Paul et al., *PLoS Comput. Biol.* 2020](https://pubmed.ncbi.nlm.nih.gov/32453790/)). NetMHCpan-4.0's eluted-ligand + affinity training was shown to improve identification of naturally processed ligands, cancer neoantigens, and T-cell epitopes over prior methods ([Jurtz et al., *J. Immunol.* 2017](https://pubmed.ncbi.nlm.nih.gov/28978689/)). A 2026 immunopeptidomics study reconfirms NetMHCpan-4.1, MixMHCpred, and MHCflurry as the state-of-the-art comparators for MHC-I presentation prediction ([Mecklenbräuker et al., *Mol. Cell. Proteomics* 2026](https://pubmed.ncbi.nlm.nih.gov/41903651/)).

No head-to-head benchmark of the *agent-driven skill* versus a hand-typed MHCflurry command exists — the skill buys correct usage (right scoring column, right cross-allele comparison) and a pinned, auditable provenance file, not a new prediction method. The underlying predictors are the validated components.

## Alternatives considered

- **Plain Claude Code, no skill (rung 1).** Workable if you already know MHCflurry's API and the `%Rank` conventions. The skill exists precisely to prevent the common mistakes (affinity-only ranking, cross-allele score comparison), so prefer it unless you are an experienced immunoinformatician doing a one-off.
- **The broader [Epitope Prediction skill](../../catalog/tools/epitope-prediction.html).** Reach for it when you also need B-cell (antibody) epitopes or MHC class II / CD4 predictions on the same antigen. This recipe stays focused on the mature, well-benchmarked CD8/MHC-I question; the Epitope Prediction skill is explicit that sequence-only B-cell prediction is far less reliable.
- **IEDB web tools (no agent).** Convenient for a quick single-peptide check, but a web run leaves no pinned-version provenance and doesn't scale to a proteome scan. Use this recipe when the shortlist goes into a synthesis order or a record.

## See also

- [MHC Binding Prediction (bioSkills)](../../catalog/tools/mhc-binding-prediction.html) — the skill this recipe drives.
- [Scan a protein for candidate CD4 T-cell (helper) epitopes](scan-protein-for-cd4-t-cell-epitopes.html) — the CD4/MHC-II sibling; run both for a full vaccine antigen analysis.
- [Epitope Prediction (bioSkills)](../../catalog/tools/epitope-prediction.html) — B-cell and class II epitopes on the same antigen.
- [Predict an antibody–antigen complex structure](predict-antibody-antigen-complex.html) — the structural, antibody-side counterpart.

## Sources

- [Paul et al., "Benchmarking predictions of MHC class I restricted T cell epitopes in a comprehensively studied model system," *PLoS Comput. Biol.* 16:e1007757](https://pubmed.ncbi.nlm.nih.gov/32453790/) — NetMHCpan-4.0/MHCflurry best; >half of major epitopes in top 277 of 767,788; published 2020; verified 2026-07-11 (this run).
- [Jurtz et al., "NetMHCpan-4.0: Improved Peptide-MHC Class I Interaction Predictions Integrating Eluted Ligand and Peptide Binding Affinity Data," *J. Immunol.* 199:3360](https://pubmed.ncbi.nlm.nih.gov/28978689/) — eluted-ligand + affinity training improves neoantigen/epitope ID; published 2017; verified 2026-07-11 (this run).
- [Mecklenbräuker et al., "Identification of MHC Ligands Through Allele-Guided Isolation Combined With Machine Learning …," *Mol. Cell. Proteomics* 25:101560](https://pubmed.ncbi.nlm.nih.gov/41903651/) — NetMHCpan-4.1/MixMHCpred/MHCflurry as SOTA comparators; published 2026; verified 2026-07-11 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=scan-protein-for-cd8-t-cell-epitopes&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fscan-protein-for-cd8-t-cell-epitopes.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
