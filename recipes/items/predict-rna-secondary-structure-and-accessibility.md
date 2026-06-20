---
title: Predict RNA secondary structure and target-site accessibility
parent: All recipes
grand_parent: Recipes
nav_order: 19
problem_class: Data analysis
subject_areas: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-20
summary: Use the ViennaRNA skill to fold an RNA, get its MFE structure, base-pair probabilities, and the accessibility of a candidate target site — for siRNA/sgRNA/ASO design or riboswitch analysis.
---

# Predict RNA secondary structure and target-site accessibility

Hand Claude an RNA sequence (and optionally a target window); get back the minimum-free-energy structure in dot-bracket, a base-pair probability map, the ensemble free energy, and the unpaired-probability (accessibility) of the region you want to hybridize against — the number that actually predicts whether an siRNA, sgRNA, or antisense oligo will engage.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Integrative Structural and Computational Biology, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You are designing a knockdown or editing reagent — an siRNA against an mRNA, a guide RNA, an antisense oligonucleotide — and you need to know whether your candidate target site is actually reachable. A site buried inside a stable stem will not hybridize no matter how good the seed match; the single best predictor of reagent efficacy beyond seed complementarity is the *accessibility* of the target window, i.e. the probability that those bases are unpaired in the folding ensemble. The same question shows up when you want to know whether a designed riboswitch or 5′ UTR folds the way you intended, or whether a point mutation reshapes a structured region. Running this by hand means installing ViennaRNA, scripting `RNAfold`/`RNAplfold`, and reading partition-function output — quick once you know the flags, fiddly every time you don't. Solved looks like: paste a sequence and a target window, get the MFE structure, the ensemble metrics, and a per-window accessibility number with a plain-language call.

## Recommended approach

This recipe is rung 2 — one skill, the [ViennaRNA (Claude Skill)](../../catalog/tools/viennarna-structure-prediction.html), which wraps the ViennaRNA Python bindings (`RNAfold`, partition function, `RNAplfold`, `RNAduplex`) Claude needs to fold sequences and score accessibility locally.

1. **Install the [ViennaRNA skill](../../catalog/tools/viennarna-structure-prediction.html).** It ships in the SciAgent-Skills collection (not an npm package). Clone the repo and load it as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm it appears under `/plugin` → Installed. The skill declares its own Python dependencies (the `ViennaRNA` package) in its `SKILL.md`; install them on first use.

2. **Fold the sequence and capture the ensemble.** A minimal prompt:

   ```
   Use the viennarna-structure-prediction skill on this RNA
   (5'→3', RNA alphabet):

   GGGAACGUUCACUGGUGCCUGAUCGAUCGAUCGGCUAGCUACGUAGCUAGCUA...

   Steps:
     1. Compute the MFE structure with RNAfold. Print the
        dot-bracket string and the MFE in kcal/mol.
     2. Compute the partition function: print the ensemble
        free energy, the frequency of the MFE structure in
        the ensemble, and the ensemble diversity.
     3. Report the centroid structure and its distance to the
        MFE structure.

   Emit a short verdict on how well-defined the fold is
   (high MFE-frequency + low diversity = a single dominant
   structure; low frequency + high diversity = a floppy
   ensemble where a single dot-bracket is misleading).
   ```

3. **Score target-site accessibility.** This is the design-relevant step. For each candidate window, compute the probability that the bases are unpaired:

   ```
   Candidate target windows (1-based positions on the sequence
   above), e.g. siRNA/ASO seed regions:
     - site A: 20–38
     - site B: 71–89

   For each window, use RNAplfold to compute the mean
   unpaired probability over the window (local folding,
   window size 70, span 40 — note the parameters used).
   Print a table: window, position, mean P(unpaired),
   min P(unpaired) across the window.

   Apply the rule of thumb:
     - mean P(unpaired) ≥ 0.5  →  accessible, good candidate
     - 0.2–0.5                 →  partially accessible; rank lower
     - < 0.2                   →  buried; deprioritize
   Rank the windows by accessibility.
   ```

4. **(Optional) Check the duplex.** If you have the antisense/guide strand, score the hybrid directly:

   ```
   Use RNAduplex (or RNAcofold) to fold this guide strand
   against the target window: <guide 5'→3'>. Report the
   duplex structure and binding energy, and flag any strong
   intramolecular structure in the guide itself that would
   compete with target binding.
   ```

5. **Persist the design card.** Ask Claude Code to write `rna/<name>_fold_<date>.md` with the MFE structure, ensemble metrics, the ranked accessibility table, any duplex energies, and the exact ViennaRNA parameters used (so the run is reproducible).

## Why this assembly

Rung 2 of the simplicity ladder. The [ViennaRNA skill](../../catalog/tools/viennarna-structure-prediction.html) wraps the one engine this task needs — thermodynamic folding, the partition function, and local accessibility (`RNAplfold`) — and runs it locally via Bash/Python. Rung 1 (plain Claude Code) would have Claude write ViennaRNA scripts from scratch each time, which works but loses the skill's vetted invocations and risks subtle flag errors (window/span choices in `RNAplfold` materially change accessibility numbers). No rung-3 toolbelt is needed: one sequence, one folding engine, one card. Rung 4 (an autonomous system) is overkill for a deterministic thermodynamics calculation whose value is the provenance of the parameters, not autonomous reasoning.

## Availability

Fully open. The ViennaRNA skill is OSS (MIT) from the SciAgent-Skills collection; the underlying ViennaRNA package is free for academic and commercial use. No accounts, no API keys, no quotas. Local Python is the only environment dependency.

## Compute requirements

Laptop. Folding a single sequence up to a few thousand nucleotides with `RNAfold` and the partition function is sub-second to a few seconds; `RNAplfold` over a long transcript is linear in length and still finishes in seconds on a laptop CPU. No GPU. Genome- or transcriptome-wide accessibility scans (tens of thousands of windows) are the only case where you would batch the `RNAplfold` step and let it run for minutes.

## Evidence

`Proposed`. No documented end-to-end LLM-orchestrated RNA-folding-and-accessibility workflow using the ViennaRNA skill in peer-reviewed literature is known as of 2026-06-20. The component pieces are long-established:

- **ViennaRNA Package** — the canonical thermodynamic RNA-folding toolkit (Lorenz et al., [*Algorithms for Molecular Biology* 2011, 6:26](https://doi.org/10.1186/1748-7188-6-26); web-services overview Gruber et al., [*Methods Mol. Biol.* 2015](https://pubmed.ncbi.nlm.nih.gov/25577387/)). `RNAfold`, the partition function, and `RNAplfold` are its standard, widely cited algorithms (Hofacker & Lorenz, [*Methods Mol. Biol.* 2014](https://pubmed.ncbi.nlm.nih.gov/24136595/)).
- **Accessibility predicts hybridization efficacy** — target-site accessibility (local unpaired probability from `RNAplfold`) is an established determinant of siRNA and antisense-oligo potency, used in tools such as `RNAplfold`/`RNAup`-based accessibility scoring and sirna design pipelines built on the ViennaRNA partition function.

The missing link is a benchmark of "Claude + ViennaRNA skill" against a hand-built notebook on a reagent-design task. Every claim in the recipe traces to the ViennaRNA algorithms above; the assembly itself is not yet documented.

## Alternatives considered

- **Rung 1 — plain Claude Code writing ViennaRNA scripts.** Workable if you cannot load plugins, but you give up the skill's vetted invocations and take on the risk of wrong `RNAplfold` window/span parameters silently distorting accessibility.
- **Web servers (ViennaRNA web services, mfold/UNAFold).** Fine for a one-off single sequence by hand, but not scriptable from inside an agent run and not reproducible as a saved card.
- **Deep-learning structure predictors (e.g. SPOT-RNA, secondary-structure transformers).** Better for pseudoknotted or non-canonical structures that thermodynamic folding misses, but heavier, less interpretable, and not yet wrapped as a Claude-installable component in [`catalog/tools/`](../../catalog/). Reach for them only when you suspect pseudoknots.
- **3D / tertiary RNA modelling.** Out of scope — this recipe is secondary-structure and accessibility only.

## See also

- [ViennaRNA (Claude Skill)](../../catalog/tools/viennarna-structure-prediction.html)
- [Score point mutations for functional impact with a protein language model](score-protein-variants-with-esm.html) — the protein-sequence counterpart when the molecule of interest is a protein, not an RNA.
- [Build a phylogenetic tree from a set of homologous sequences](build-phylogenetic-tree-from-sequences.html) — another sequence-analysis recipe from a skills collection, for the comparative-genomics side.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) — verified 2026-06-20 (this run).
- [Lorenz R. et al., "ViennaRNA Package 2.0," *Algorithms for Molecular Biology* 2011, 6:26](https://doi.org/10.1186/1748-7188-6-26) — published 2011-11.
- [Gruber A.R. et al., "The ViennaRNA web services," *Methods Mol. Biol.* 2015](https://pubmed.ncbi.nlm.nih.gov/25577387/) — published 2015.
- [Hofacker I.L., Lorenz R., "Predicting RNA structure: advances and limitations," *Methods Mol. Biol.* 2014](https://pubmed.ncbi.nlm.nih.gov/24136595/) — published 2014.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=predict-rna-secondary-structure-and-accessibility&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fpredict-rna-secondary-structure-and-accessibility.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
