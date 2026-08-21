## Approach: selective dependency mapping in DepMap for an SS18::SSX (synovial sarcoma) context

Since you didn't specify which context, I'll use **SS18::SSX-fusion-positive synovial sarcoma** as the worked example (it's a well-characterized DepMap use case — this is the analysis that originally nailed BRD9/ncBAF as a synovial sarcoma dependency). The same pipeline applies verbatim to a continuous-variable context like "low ATP1B1 expression" — swap the group-defining step for a median-split or continuous correlation, noted below.

### 1. Pin the dataset version first, before touching any data

Reproducibility has to be designed in at the start, not bolted on:

- Use a specific **quarterly DepMap release** (e.g., "DepMap Public 26Q1" — the current cadence as of early 2026; check depmap.org/portal for whichever is newest when you run this) rather than "latest," and record that string in every output file's metadata/header.
- Download from the **versioned Figshare DOI** for that release (not a rolling API endpoint), and record the DOI and file-level checksums (`sha256sum`) alongside your results.
- Pull these four files from that single release, never mixed across releases:
  - `CRISPRGeneEffect.csv` — Chronos gene effect scores (genome-wide KO, ~1,100 lines × ~18,000 genes)
  - `Model.csv` — cell line metadata (lineage, `OncotreeSubtype`, etc.)
  - `OmicsSomaticMutations.csv` / a fusion call table (or curated annotation, see below) for the SS18::SSX status
  - `OmicsCNGene.csv` and `OmicsExpressionProteinCodingGenesTPMLogp1.csv` for the artifact-filtering steps
- Save the exact environment: pinned package versions (e.g., the Bioconductor `depmap` package version, or a `renv.lock`/`conda-lock` file), your script, and the release string together — that triple is what makes the ranking reproducible, not just the CSV.

### 2. Define the context group carefully

For a fusion event, don't rely solely on automated RNA fusion callers in DepMap — they're incomplete for rare fusions like SS18::SSX. Assumption I'm making: define the group using `Model.csv`'s `OncotreeSubtype == "Synovial Sarcoma"` cross-checked against any available fusion calls, giving roughly 8–12 cell lines. This is a small n, which matters for the stats step below.

Two comparator choices, and I'd run both and report where they disagree:
- **Pan-cancer background**: all other ~1,000+ lines. Maximizes power but conflates "fusion-specific" with "sarcoma-lineage-specific."
- **Lineage-matched background**: other sarcoma/mesenchymal lines only. Cleaner biologically, but few lines, so power drops.

For a continuous variable like ATP1B1 expression, skip binarization if you can — use a rank correlation (Spearman) between expression and Chronos score across all lines, or if you want a clean "low vs. rest" comparison, split at a pre-registered threshold (e.g., bottom decile) rather than a median split, since median splits on a continuous confound are a common source of spurious "selective" hits.

### 3. Statistical test and multiple-testing correction

With a small group (~10 lines) against a large background, a plain Welch's t-test per gene is unstable. Use a **moderated t-test** (limma's `eBayes`, or an equivalent empirical-Bayes variance shrinkage) across all ~18,000 genes simultaneously — this borrows information across genes to stabilize the small-group variance estimate, which is exactly the failure mode of naive per-gene t-tests here. Apply **Benjamini–Hochberg FDR** correction across the full gene set, not just your top candidates.

Report both:
- **Adjusted p-value** (statistical confidence)
- **Effect size** = mean(Chronos in group) − mean(Chronos outside group), plus the *within-group max* Chronos score (to catch cases where "significance" is driven by one outlier line rather than a consistent effect across the fusion-positive lines)

Rank candidates jointly on effect size and significance (e.g., sort by adjusted p, break ties/filter by requiring |Δ| beyond some threshold like −0.3), not by p-value alone — p-value alone rewards low-variance non-effects.

### 4. Remove pan-essential genes

DepMap ships a **common-essential gene classification** (derived from a two-component Gaussian mixture fit to the Chronos score distribution, comparing to a curated non-essential reference set) — pull this list and hard-exclude or clearly flag any gene on it. A gene that's lethal everywhere has no therapeutic window regardless of how "significant" its extra lethality in your subset looks; it's not a *selective* dependency by definition, just a slightly-more-lethal universal one.

### 5. Filter out copy-number/cutting-toxicity artifacts

This is the step people skip and get burned by. Two distinct phenomena to separate:

- **Cutting-toxicity artifact**: Cas9 double-strand breaks in highly amplified, often non-expressed genomic regions cause apparent "dependency" purely from cutting a lot of DNA — nothing to do with gene function. Chronos partially corrects for this internally, but residual signal survives, especially at high copy number (>8–10 copies).
- **CYCLOPS dependency**: a genuine, biologically real dependency where a gene is selectively essential because copy-number loss elsewhere has left the cell haploinsufficient for it — this one you want to *keep*, not discard.

To tell them apart for each top candidate gene:
1. Correlate Chronos score against **local gene-level copy number** (`OmicsCNGene.csv`) across all lines. If there's a strong positive correlation between CN and *dependency magnitude* specifically among your amplified lines, be suspicious.
2. Cross-check against **expression** (`OmicsExpressionProteinCodingGenesTPMLogp1.csv`) in those same lines. A real dependency (including CYCLOPS) tracks with the gene being expressed and functionally relevant; a pure cutting-toxicity artifact shows dependency even when the gene is barely expressed (you're just cutting the amplicon, not disrupting a needed protein).
3. Practically: exclude/flag a hit if (CN > ~8 copies in the group) AND (expression is low/flat relative to background) AND (the CN–dependency correlation is stronger than the expression–dependency correlation). Keep it if dependency tracks with expression, not just raw copy number.

The DepMap portal's own "Custom Analysis" two-class comparison tool applies similar CN-aware filtering and is worth running as an independent sanity check on your top 20–30 candidates before you invest further.

### 6. Sanity-check against lineage confounding

Because SS18::SSX status and "sarcoma lineage" are nearly the same partition in the data, add lineage as a covariate in the model (or run the lineage-matched comparator from step 2) so top hits aren't just "genes sarcoma cells in general depend on." For a continuous marker like ATP1B1 expression this is less of an issue but still worth checking if the marker itself correlates with lineage.

### 7. Final ranked output

For each surviving candidate, report: adjusted p-value, effect size (Δ Chronos), whether it's pan-essential (excluded), CN-artifact flag (excluded/flagged), expression concordance, and both pan-cancer and lineage-matched comparator results — plus the DepMap release string, file checksums, and package/environment versions used, all in one reproducibility manifest saved next to the ranked table.

Sources:
- [DepMap Data Downloads Portal](https://depmap.org/portal/data_page/?tab=currentRelease)
- [Chronos parameters (Public 26Q1) — Figshare](https://figshare.com/articles/online_resource/Chronos_parameters_Public_26Q1_/31660582)
- [DepMap 24Q4 Public — Figshare+](https://plus.figshare.com/articles/dataset/DepMap_24Q4_Public/27993248)
- [DepMap Bioconductor package manual](https://www.bioconductor.org/packages//release/data/experiment/manuals/depmap/man/depmap.pdf)
- [A novel pipeline for prioritizing cancer type-specific therapeutic vulnerabilities using DepMap (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10850805/)