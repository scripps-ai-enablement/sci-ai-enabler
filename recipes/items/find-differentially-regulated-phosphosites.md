---
title: Find differentially regulated phosphosites, not just changed proteins
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-15
summary: Use the MaxQuant skill on a paired phospho-enriched and unenriched run to get site-level regulation calls that are not just protein-abundance changes in disguise.
---

# Find differentially regulated phosphosites, not just changed proteins

Take a phospho-enriched mass-spectrometry experiment to a list of *sites* whose phosphorylation changed — with the localization confidence stated per site, the peptide multiplicities kept apart, and every call normalized against the protein's own abundance so a changed site is not simply a changed protein.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You treated cells with a kinase inhibitor, a growth factor, or made a knockout, enriched the phosphopeptides over TiO₂ or IMAC, and ran them. You want the sites that got more or less phosphorylated — the readout that tells you which arm of the signalling network moved.

Three things break here that do not break in a protein-level experiment. First, **the analysis unit is a residue, not a protein**, and MS/MS often cannot tell which of two nearby serines carried the phosphate; MaxQuant reports that uncertainty in a column most pipelines never read. Second, **the same site is quantified several times** — once for singly-phosphorylated peptides, once for doubly, once for triply — and those are different molecular species that must not be added together. Third and worst, **a site can look regulated purely because the protein got more abundant.** If a stimulus raises a protein twofold, every site on it rises twofold, and a phospho-only experiment cannot tell you that. Real stimulation experiments move protein abundance on a scale that swamps this: 20 h of IL-3 on human eosinophils significantly changed 1,150 of 5,385 measured proteins alongside 4,218 regulated phosphosites in the same samples.

"Solved" looks like: a committed script, one row per site × multiplicity, a declared localization cutoff, and a fold change that has been divided through by the protein's own fold change wherever the protein was measured — with the sites where it was not measured labelled rather than quietly reported.

## Recommended approach

One skill: the [MaxQuant (Claude Skill)](../../catalog/tools/maxquant-proteomics.html). Install it per its catalog page, and install MaxQuant itself from maxquant.org — the skill drives it, it does not ship it. Note up front that the skill's own workflow stops at `proteinGroups.txt`; it configures and runs the search and supplies the filter → normalize → moderated-test pattern, and the site-level layer in steps 4–6 is scripted on top of MaxQuant's site table.

1. **Commit to running the paired proteome, before you enrich anything.** This recipe needs two arms from the same lysates: the phospho-enriched fraction and an unenriched aliquot searched for protein abundance. Skipping the second arm is the decision that makes the result uninterpretable later, and it cannot be repaired after the sample is gone. Budget the instrument time now. Record the **enrichment chemistry** (TiO₂, Fe³⁺-IMAC, Ti⁴⁺-IMAC) in the sample sheet and keep it identical across every sample in the comparison — different chemistries recover largely different phosphopeptides, so a batch enriched differently is a different experiment, not a replicate.

2. **Write two `mqpar.xml` files and commit both.** `mqpar_phospho.xml` adds **Phospho (STY)** to the variable modifications and turns on match-between-runs; `mqpar_proteome.xml` does not. Keep the rest identical — same FASTA (record the UniProt proteome ID *and* release), same enzyme, same PSM/protein FDR, same site FDR. Every extra variable modification multiplies the search space and the decoy-competitive candidate pool, so resist adding more.

3. **Run both searches, then read `summary.txt` for each.** For the phospho arm also check **enrichment specificity** — the fraction of identified peptides carrying a phosphate. A sample well below its neighbours had a failed enrichment, and its site intensities are not comparable to the rest. Decide whether to drop it, and record the decision.

4. **Have Claude Code write the site-level analysis to a script.** Review it before running:

   ```
   Using the maxquant-proteomics skill for the MaxQuant/limma layer, write
   phospho_de.py that:

   1. Reads Phospho (STY)Sites.txt and removes rows flagged "Reverse" or
      "Potential contaminant". Log the count removed by each. Do NOT copy the
      protein-level filter verbatim -- the site table has no "Only identified
      by site" column, so that filter silently matches nothing here.
   2. Reads "Localization prob" and splits the table on a cutoff stated as a
      literal (0.75 = class I). Sites BELOW the cutoff go to
      low_confidence_sites.csv and are never reported as a named residue;
      they may only be described as "a site in this peptide". Record the
      MS/MS fragmentation method used, since the reliable cutoff depends on
      it.
   3. EXPANDS the multiplicity columns into rows: the ___1 / ___2 / ___3
      intensity columns are singly, doubly and triply phosphorylated forms
      of the peptide bearing this site. Emit one row per (site, multiplicity)
      keyed as <Leading protein>_<Amino acid><Position>_<multiplicity>.
      Never sum or average across multiplicities.
   4. Applies a valid-value rule stated as a literal, per group, not pooled,
      and writes sites_filtered.csv with kept and dropped sites and their
      per-group valid counts.
   5. log2-transforms and median-normalizes the site intensities.
   6. Reads proteinGroups.txt from the UNENRICHED run, applies the full
      three-flag protein filter, log2s and median-normalizes it, and joins it
      to the sites on "Protein group IDs".
   7. Emits site_de_results.csv with, per row: the raw site log2FC, the
      protein log2FC, a protein-normalized site log2FC (site minus protein),
      moderated-t p and BH-adjusted p for BOTH the raw and the normalized
      statistic, and a three-value protein_status column:
        normalized      -- protein quantified, correction applied
        protein_unmeasured -- protein absent from the unenriched run
        protein_also_changed -- protein itself significant at the same FDR
   8. Does NOT roll sites up to a per-protein value at any point.
   9. States the FDR threshold and log2FC floor as literals and sets the RNG
      seed if anything stochastic is used.
   ```

5. **Read the table on the normalized statistic, with `protein_status` in view.** A site significant on the raw fold change but not on the protein-normalized one is a protein-abundance change, and calling it a signalling event is the error this recipe exists to prevent. A `protein_unmeasured` site is a genuine unknown — report it as unresolved, not as regulated. A `protein_also_changed` site needs both statements made together in the text.

6. **Keep sites separate in the write-up.** Two sites on one protein moving in opposite directions is ordinary — activating and inhibitory sites on the same kinase do exactly that — so never summarise a protein as "phosphorylation increased". If you run enrichment on the hit list, the background set is the **phosphoproteins you detected**, not the genome, and the result is about proteins, not sites.

7. **Pin and record.** `requirements.txt` for the Python environment; `provenance.json` capturing the MaxQuant version, the FASTA proteome ID and release date, the enrichment chemistry and the fragmentation method, the localization cutoff, the valid-value rule, the normalization and FDR/fold-change literals, a sha256 of both `Phospho (STY)Sites.txt` and `proteinGroups.txt`, and the model id that wrote the script.

Artifacts to commit: `mqpar_phospho.xml`, `mqpar_proteome.xml`, `phospho_de.py`, `sites_filtered.csv`, `low_confidence_sites.csv`, `site_de_results.csv`, `requirements.txt`, `provenance.json`. See [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) for the general pattern.

## Why this assembly

Rung 2, and it stops there. The skill is load-bearing for the search configuration and the MaxQuant invocation on *both* arms — step 1's paired proteome run is exactly the protein-level pipeline the skill documents — plus the filter → normalize → moderated-test pattern that transfers to the site table.

Rung 1 fails on three checkable errors. An agent working from general knowledge reaches for `proteinGroups.txt`, because that is the file every proteomics tutorial uses; it sums the `___1`/`___2`/`___3` columns, because they look like replicates; and it never reads `Localization prob`, because nothing in the protein-level workflow has an analogue. Each produces a fluent, plausible table. None is detectable by reading the output. Rung 3 adds nothing: no second component is needed, and the one genuine extension — kinase-activity inference from the hit list — has no catalogued component to reach for.

## Availability

Fully open in the sense that matters — no subscription, no account, no institutional gate. The same two license details as the protein-level sibling apply: the skill collection is community OSS (CC BY 4.0 text, Apache-2.0 upstream), and **MaxQuant itself is free of charge but not open source** — the download requires accepting the Max Planck Institute of Biochemistry's terms and Bioconda flags it license-restricted, so you may not redistribute it inside a published container image.

Platform is the practical gate: Windows 10/11 or Server 2016+, or Ubuntu 20.04+, with .NET 8.0 since v2.6.3.0. No macOS build, no Linux GUI — headless runs go through `dotnet MaxQuant/bin/MaxQuantCmd.dll mqpar.xml`. Everything is local, so unpublished raw files never leave the machine.

## Compute requirements

Same hardware class as the protein-level sibling, roughly two to four times the hours. Two things drive that: you are running two searches instead of one, and adding Phospho (STY) as a variable modification expands the search space of the enriched arm.

A two-group design with 5 replicates a side is 20 raw files across both arms; on an 8-core machine with 32 GB RAM that is a long weekend rather than an overnight. 32 GB is the floor and 64 GB is comfortable — a swap-thrashing MaxQuant run takes days. Large parts of the analysis are single-threaded regardless of the thread count, so fast local disk beats core count, and you want 3–5× the raw-file volume free for intermediates. Everything from step 4 onward runs in seconds. No GPU helps anywhere in this recipe.

## Evidence

**Proposed.** No documented run of Claude Code driving this skill on a phosphoproteomics cohort with quantitative pass/fail is known — and note that the skill's published workflow is protein-level, so the site-level layer here is composed rather than documented upstream. The three gates the recipe turns on are each grounded:

- **Site localization is genuinely uncertain, and the reliable threshold depends on your instrument method.** Against 180 individually synthesized phosphopeptides with precisely known sites, localization score thresholds had to be calibrated *per fragmentation method*: at 1% false localization rate, HCD-Orbitrap localized the most peptides correctly, followed closely by low-resolution ETD ion-trap spectra, with CID and multi-stage activation significantly worse ([Savitski et al., *Mol. Cell. Proteomics* 2011](https://doi.org/10.1074/mcp.M110.003830)). This is why step 4 records the fragmentation method next to the cutoff rather than treating 0.75 as universal.
- **Different pipelines disagree about which site was modified.** Applying four computational pipelines to one human cancer phosphoproteomics dataset produced "a large discrepancy among the reported phosphopeptide identification and phosphosite localization results" ([Jiang et al., *Mol. Cell. Proteomics* 2021](https://doi.org/10.1016/j.mcpro.2021.100171)); the HUPO Human Proteome Project's Phosphopeptide Challenge, in which 22 laboratories analysed a common set of 94 synthetic phosphopeptides, was set up precisely because "the correct identification of phosphorylated sites, their quantification, and their interpretation regarding physiological relevance remain challenging" ([Hoopmann et al., *J. Proteome Research* 2020](https://doi.org/10.1021/acs.jproteome.0c00648)). A pipeline-specific probability belongs in the output, not in a default.
- **The protein-abundance confound is large in exactly the experiments people run.** Measuring proteome and phosphoproteome from the same samples, 20 h of IL-3 on human eosinophils significantly changed 1,150 up and 703 down of 5,385 quantified proteins, alongside regulated phosphorylation at 4,218 of 7,330 sites ([Esnault et al., *J. Proteome Research* 2018](https://doi.org/10.1021/acs.jproteome.8b00057)); kinase and phosphatase deletions in *S. mutans* likewise produced "widespread alterations in protein abundance and phosphorylation" together ([Chudal et al., *mSystems* 2025](https://doi.org/10.1128/msystems.01105-25)). These are existence proofs of the confound's magnitude, not a benchmark of the correction — which is why step 7 reports the raw and normalized statistics side by side rather than replacing one with the other.
- **Which sites you see is a property of the enrichment chemistry.** Fe³⁺-IMAC and Ti⁴⁺-IMAC enrichments of the same Raji B-cell digest shared only **10%** of 2,905 phosphopeptides, differing systematically in hydrophobicity, amino-acid composition and multiply-phosphorylated fraction ([Lai et al., *Rapid Commun. Mass Spectrom.* 2012](https://doi.org/10.1002/rcm.6327)). Hence step 1's rule that the chemistry is fixed across the comparison and recorded.

## Alternatives considered

**Skip the paired proteome and report raw site fold changes.** Cheaper by half the instrument time, and common in the literature. It is defensible only when you have independent evidence that protein abundance did not move — a short stimulation with no transcriptional response, say, or a western blot for the specific protein. State the assumption in the methods if you take this path; do not leave it implicit.

**Infer kinase activities from the site list.** The natural next question, and the one that turns a site table into a pathway claim. KSEA-class methods reach a mean AUC of 0.722 against a 184-pair gold standard of kinase-condition regulation, but performance depends strongly on how many substrates a kinase has and on the evidence type behind those annotations ([Hernandez-Armenta et al., *Bioinformatics* 2017](https://doi.org/10.1093/bioinformatics/btx082)) — so it is a screening layer, not a verdict. No catalogued component runs it, so this recipe cannot give you a followable path.

**A phosphosite-aware search engine.** FragPipe/MSFragger with PTM-Shepherd, or Proteome Discoverer with ptmRS, are reasonable substitutes for the search itself and faster on large cohorts. Neither is catalogued. Everything from step 4 onward transfers unchanged to whatever site table they emit, provided you map their localization score onto the cutoff rule.

**Start from the protein level instead.** If the question is which proteins changed rather than which residues, [Find differentially abundant proteins in a label-free proteomics experiment](find-differentially-abundant-proteins-in-lfq-ms.html) is the shorter recipe, and it is also step 1's second arm here.

## See also

- [MaxQuant (Claude Skill)](../../catalog/tools/maxquant-proteomics.html)
- [Find differentially abundant proteins in a label-free proteomics experiment](find-differentially-abundant-proteins-in-lfq-ms.html) — the protein-level sibling, and the unenriched arm of this recipe.
- [PRIDE (Claude Skill)](../../catalog/tools/pride-database.html) — public phosphoproteomics datasets to reanalyze before booking instrument time.
- [Infer TF and pathway activities from expression](infer-tf-and-pathway-activities-from-expression.html) — the transcriptomic analogue of turning a hit list into a signalling claim.
- [Quantify western blot densitometry](quantify-western-blot-densitometry.html) — the phospho-specific-antibody validation a reviewer will ask for.

## Sources

- [`jaechang-hits/SciAgent-Skills` — `maxquant-proteomics/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/proteomics-protein-engineering/maxquant-proteomics/SKILL.md) — fetched 2026-08-15 (this run); confirms the skill's documented workflow is protein-level (`proteinGroups.txt`) and does not cover site tables.
- [MaxQuant output tables documentation](https://cox-labs.github.io/coxdocs/output_tables.html) — `Phospho (STY)Sites.txt` column names (`Localization prob`, `Score diff`, `Amino acid`, `Positions within proteins`, `Reverse`, `Potential contaminant`, `___1`/`___2`/`___3` multiplicity columns); fetched 2026-08-15 (this run).
- [Savitski et al. — Confident phosphorylation site localization using the Mascot Delta Score, *Mol. Cell. Proteomics* 10:M110.003830 (2011)](https://doi.org/10.1074/mcp.M110.003830) — published 2011; verified 2026-08-15 (this run).
- [Jiang et al. — Deep-Learning-Derived Evaluation Metrics Enable Effective Benchmarking of Computational Tools for Phosphopeptide Identification, *Mol. Cell. Proteomics* 20:100171 (2021)](https://doi.org/10.1016/j.mcpro.2021.100171) — published 2021; verified 2026-08-15 (this run).
- [Hoopmann et al. — Insights from the First Phosphopeptide Challenge of the MS Resource Pillar of the HUPO Human Proteome Project, *J. Proteome Research* (2020)](https://doi.org/10.1021/acs.jproteome.0c00648) — published 2020; verified 2026-08-15 (this run).
- [Esnault et al. — Proteomic and Phosphoproteomic Changes Induced by Prolonged Activation of Human Eosinophils with IL-3, *J. Proteome Research* (2018)](https://doi.org/10.1021/acs.jproteome.8b00057) — published 2018; verified 2026-08-15 (this run).
- [Chudal et al. — Post-translational modifications via serine/threonine phosphorylation and GpsB in *Streptococcus mutans*, *mSystems* (2025)](https://doi.org/10.1128/msystems.01105-25) — published 2025; verified 2026-08-15 (this run).
- [Lai et al. — Complementary Fe(3+)- and Ti(4+)-immobilized metal ion affinity chromatography for purification of acidic and basic phosphopeptides, *Rapid Commun. Mass Spectrom.* 26:2186 (2012)](https://doi.org/10.1002/rcm.6327) — published 2012; verified 2026-08-15 (this run).
- [Hernandez-Armenta et al. — Benchmarking substrate-based kinase activity inference using phosphoproteomic data, *Bioinformatics* 33:1845 (2017)](https://doi.org/10.1093/bioinformatics/btx082) — published 2017; verified 2026-08-15 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=find-differentially-regulated-phosphosites&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ffind-differentially-regulated-phosphosites.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
