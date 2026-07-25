---
title: Identify an unknown compound from an MS/MS spectrum
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Data analysis
subject_areas: [Chemistry]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
summary: Use the matchms skill in Claude Code to clean an unknown MS/MS spectrum and rank candidate identities by spectral similarity against a reference library.
last_verified: 2026-07-25
---

# Identify an unknown compound from an MS/MS spectrum

Hand Claude Code one or more tandem-MS spectra and a reference library; get back a ranked, score-annotated table of candidate identities — peaks normalized, metadata harmonized, and matches computed with cosine and modified-cosine similarity.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Chemistry |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Untargeted metabolomics and small-molecule MS produce thousands of fragmentation spectra, most of them unannotated. The recurring task is: given an experimental MS/MS spectrum, *what is this molecule?* The standard answer is library matching — score the unknown against a reference library (GNPS, MassBank, an in-house `.msp`) and rank candidates by spectral similarity. The work is fiddly and easy to get wrong: spectra arrive in mixed formats (`.mzML`, `.mgf`, `.msp`, `.json`), metadata fields are inconsistently named, low-intensity noise peaks inflate spurious matches, and precursor-m/z tolerance and similarity choice (plain cosine vs modified cosine, which tolerates the precursor mass shift between related structures) materially change the hit list. Done by hand, two analysts processing the same file get different annotations.

Solved looks like: spectra in, a deduplicated candidate table out — each query spectrum paired with its top library matches, each match carrying a similarity score, the number of matching peaks, and the library compound's name/InChIKey — in a few minutes on a laptop, with the cleaning and tolerance choices recorded so the run is reproducible. This is *annotation*, not proof: a high score is a hypothesis to confirm, not a confirmed identity.

## Recommended approach

1. **Install the [matchms skill](../../catalog/tools/matchms.html)** (Node ≥ 18):

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   ```

   Enable the `matchms` skill when prompted. matchms declares its own Python dependencies in its `SKILL.md`; install them with `uv`/`pip` on first use.

2. **Load and clean both the query and reference spectra first.** A minimal prompt:

   ```
   Query spectra: data/unknowns.mgf
   Reference library: data/library.msp   (or a GNPS/MassBank export)

   Use the matchms skill:
     1. Import both files (matchms.importing).
     2. Apply a standard cleaning pipeline to every spectrum:
        default_filters, normalize_intensities,
        select_by_relative_intensity(0.01, 1.0),
        select_by_mz(0, 1000), require_minimum_number_of_peaks(n=5),
        and harmonize/repair metadata (derive_inchikey/derive_formula
        where available).
     3. Drop query spectra that fall below the minimum-peaks
        threshold and report how many were dropped and why.
   ```

3. **Score the unknowns against the library.** Use modified cosine so related structures (with a precursor mass shift) still match:

   ```
   Now compute similarity of every cleaned query against the
   cleaned reference library with matchms:
     - ModifiedCosine(tolerance=0.1) for fragment-peak matching.
     - Gate matches on precursor m/z within 0.01 Da when an exact
       ID is wanted, or leave open for analog discovery.
     - Keep only matches with score >= 0.7 AND matched_peaks >= 6.
   For each query, return its top 5 surviving library hits.
   ```

   State the tolerances explicitly so the reader can tighten or loosen them. Lower the score floor for analog/class-level annotation; raise `matched_peaks` to suppress small-spectrum false hits.

4. **Write a ranked candidate table.** Persist the result, not just the printout:

   ```
   Write annotations/candidates.csv with one row per (query, hit):
   query_id | query_precursor_mz | library_compound_name |
   library_inchikey | modified_cosine | matched_peaks |
   precursor_mz_diff.
   Sort by query_id, then modified_cosine descending.
   Print the per-query top hit and the count of queries with at
   least one surviving match vs. those left unannotated.
   ```

5. **Confirm the top candidates before believing them.** A spectral match is a lead. For each high-scoring InChIKey, look it up to sanity-check identity and bioactivity context — pipe the InChIKeys into [Profile a compound's polypharmacology from ChEMBL bioactivity data](profile-compound-polypharmacology.html), or run a structure/identity lookup in the [PubChem MCP](../../catalog/tools/pubchem.html). Treat unannotated queries as candidates for orthogonal methods (accurate-mass formula prediction, in-silico fragmentation), not as failures.

## Why this assembly

Rung 2 of the simplicity ladder. The whole task — import mixed MS formats, clean and normalize peaks, harmonize metadata, and score with cosine / modified-cosine against a library — is exactly the surface the [matchms skill](../../catalog/tools/matchms.html) wraps (its catalog page lists "comparing mass spectra, computing similarity scores (cosine, modified cosine), and identifying unknown compounds from spectral libraries" as primary use cases). Plain Claude Code with no skill (rung 1) would re-implement the filter chain and the similarity math by hand each session — error-prone and slow, and the peak-cleaning order alone is easy to get wrong. A multi-tool harness (rung 3) adds nothing for single-library matching: there is one Python library applied in sequence, no second data source to orchestrate. Full LC-MS/MS proteomics pipelines (feature detection, peptide ID) are a different, heavier problem — reach for the [pyOpenMS skill](../../catalog/tools/pyopenms.html) there, as matchms's own catalog page advises.

## Availability

Fully open. The [matchms skill](../../catalog/tools/matchms.html) ships in the `K-Dense-AI/scientific-agent-skills` collection; matchms itself is Apache-2.0. No subscription or institutional licence. You do need a reference library: GNPS and MassBank exports are free and public; an in-house `.msp` works the same way. No account beyond a Claude plan.

## Compute requirements

Laptop. Cleaning and scoring a few thousand query spectra against a library of tens of thousands of reference spectra runs in minutes on a single CPU core and fits comfortably in <4 GB RAM. The all-vs-all similarity step is the cost driver and scales with `(queries × references)`; for very large libraries (hundreds of thousands of spectra) restrict the reference set by precursor-m/z window first, or — if the matrix is the bottleneck — a GPU cosine kernel such as SimMS gives order-of-magnitude speedups ([Onoprishvili et al., *Bioinformatics* 2025](https://doi.org/10.1093/bioinformatics/btaf081)). No GPU is needed for laptop-scale runs.

## Evidence

Proposed. No published benchmark of an LLM-driven matchms annotation workflow is known. The underlying library — and every primitive this recipe drives (import, peak filtering, metadata harmonization, cosine and modified-cosine scoring) — is the canonical open-source tool for the task, peer-reviewed in JOSS ([Huber et al., *J. Open Source Softw.* 5(52):2411, 2020](https://doi.org/10.21105/joss.02411)). Modified-cosine matching against reference libraries (GNPS, MassBank) is the field-standard annotation method, and active methods work continues to build on it — e.g., GPU-accelerated cosine scoring ([Onoprishvili et al., *Bioinformatics* 2025](https://doi.org/10.1093/bioinformatics/btaf081)) and enhanced reverse spectral search now folded into GNPS, which rescued up to 62% more annotations on benchmark sets ([Xing et al., *Anal. Chem.* 2025](https://doi.org/10.1021/acs.analchem.5c02047)). Each component has independent validation; the agent-orchestrated assembly does not. Treat every match as an annotation hypothesis to confirm with orthogonal evidence.

## Alternatives considered

- **Plain Claude Code, no skill (rung 1).** Workable for a one-off comparison of two spectra you can read off by eye, but re-deriving the cleaning chain and similarity math each session is slow and irreproducible. Reach for it only when you cannot install the skill.
- **pyOpenMS skill.** The [pyOpenMS skill](../../catalog/tools/pyopenms.html) is the right tool when the problem is a full LC-MS/MS pipeline — feature detection, peptide identification, protein quantification — rather than spectral library matching of small molecules. Use it for proteomics; use matchms for metabolite/compound ID. They are complementary, not competing.
- **A GPU similarity backend (within rung 2).** When the reference library is hundreds of thousands of spectra and the all-vs-all matrix dominates wall-clock, swap the cosine kernel for a GPU implementation (SimMS) while keeping the same matchms cleaning and gating. Stay on the laptop path until the matrix is actually the bottleneck.

## See also

- [matchms (Claude Skill)](../../catalog/tools/matchms.html)
- [pyOpenMS (Claude Skill)](../../catalog/tools/pyopenms.html) — the LC-MS/MS proteomics counterpart.
- [PubChem MCP](../../catalog/tools/pubchem.html) — structure/identity lookup for confirming a candidate InChIKey.
- [Profile a compound's polypharmacology from ChEMBL bioactivity data](profile-compound-polypharmacology.html) — bioactivity context for a confirmed identity.

## Sources

- [`K-Dense-AI/scientific-agent-skills` — matchms skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/matchms/SKILL.md) — verified 2026-06-08 (this run).
- [Huber F. et al. — matchms: processing and similarity evaluation of mass spectrometry data, *J. Open Source Softw.* 5(52):2411 (2020)](https://doi.org/10.21105/joss.02411) — published 2020-08-31; verified 2026-06-08 (this run).
- [Onoprishvili T. et al. — SimMS: a GPU-accelerated cosine similarity implementation for tandem mass spectrometry, *Bioinformatics* (2025)](https://doi.org/10.1093/bioinformatics/btaf081) — published 2025; verified 2026-06-08 (this run).
- [Xing S. et al. — Reverse Spectral Search Reimagined, *Anal. Chem.* (2025)](https://doi.org/10.1021/acs.analchem.5c02047) — published 2025; verified 2026-06-08 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=identify-unknown-compound-from-msms-spectrum&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fidentify-unknown-compound-from-msms-spectrum.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
