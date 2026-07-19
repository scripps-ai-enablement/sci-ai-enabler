---
title: Build a resting-state functional-connectivity matrix from preprocessed fMRI
parent: All recipes
grand_parent: Recipes
nav_order: 2
problem_class: Data analysis
subject_areas: [Neuroscience]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-19
summary: Use the Nilearn skill in Claude Code to turn fMRIPrep-preprocessed BOLD into an atlas ROI-to-ROI functional-connectivity matrix with confound regression, as a re-runnable script.
---

# Build a resting-state functional-connectivity matrix from preprocessed fMRI

Hand Claude Code an fMRIPrep-preprocessed resting-state BOLD run plus its confounds; get back an atlas ROI time-series extraction, confound regression, and a ROI-to-ROI functional-connectivity matrix, captured as a version-controlled script with the atlas, confound strategy, and provenance written down.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Building a functional connectome from resting-state fMRI is a fixed sequence — pick a parcellation atlas, extract the mean BOLD time-series per region, regress out confounds (motion parameters, aCompCor, cosine drift, and often high-motion volume scrubbing), then correlate every region against every other region — but each step hides a decision that silently changes the connectome. The wrong confound strategy leaves motion artifact masquerading as connectivity; forgetting to standardize or detrend biases the correlations; a full Pearson correlation and a partial correlation give different network topologies. Every lab rebuilds this boilerplate in Nilearn, and the confound-selection choices are exactly where reproducibility breaks down between papers. Solved looks like: hand the agent the fMRIPrep outputs and an atlas name, get back committed code that emits the connectivity matrix, a figure, and a record of the atlas version, confound columns used, TR, and input hashes.

## Recommended approach

1. **Install the [Nilearn skill](../../catalog/tools/nilearn-tool.html)** in Claude Code (it wraps the concrete Nilearn idioms for atlas time-series extraction, fMRIPrep confound handling, and connectivity-matrix construction):

   ```
   git clone https://github.com/CUHK-AIM-Group/NeuroClaw
   cp -r NeuroClaw/skills/nilearn-tool ~/.claude/skills/
   ```

   Verify Nilearn is importable (`pip install nilearn`). No GPU needed. Start from fMRIPrep outputs — this recipe does not run preprocessing itself.

2. **Have the assistant write a versioned pipeline script, not run steps interactively.** A minimal prompt:

   ```
   Using the nilearn-tool skill, write me a script build_connectome.py
   that takes an fMRIPrep-preprocessed BOLD file
   (sub-01_task-rest_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz)
   and its confounds TSV. The script must:
   - fetch a named atlas (default: Schaefer 2018, 200 parcels, 17 networks)
     and build a NiftiLabelsMasker with standardize="zscore_sample",
     detrend=True, low_pass=0.08, high_pass=0.009, t_r read from the JSON
   - load confounds via nilearn's fMRIPrep confound loader with an explicit
     strategy (motion + high-pass cosines + aCompCor + non-steady-state);
     log the exact confound column names used
   - extract ROI time-series with those confounds regressed out
   - compute both a Pearson and a partial-correlation ROI-to-ROI matrix
     with ConnectivityMeasure
   - save out/connectivity_pearson.csv, out/connectivity_partial.csv,
     and a heatmap figure
   Surface the atlas name, n_parcels, band-pass edges, and confound
   strategy as variables at the top of the file with comments.
   ```

3. **Pin the environment.** Ask the assistant to emit a `requirements.txt` (or `environment.yml`) pinning `nilearn`, `scikit-learn`, `numpy`, `scipy`, `pandas`, `matplotlib`, `nibabel`. Commit the script and the environment together.

4. **Inspect the connectome before trusting it.** Have the assistant add a QC step: report mean framewise displacement and the number of volumes flagged, and plot the matrix ordered by network so the block structure (within- vs between-network) is visible. A connectome with no network block structure usually signals a confound or atlas-space mismatch.

5. **Record provenance.** Have the script write `out/provenance.json` capturing: Nilearn version, the atlas name and release (Schaefer 2018 fetched via `datasets.fetch_atlas_schaefer_2018`), the exact confound columns regressed, the band-pass edges and TR, the connectivity kind(s), the input BOLD and confounds `sha256`, the run date, and the model/agent identity. The atlas fetch hits a live datasets server, so record its version so divergence is visible. See the [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide for the pattern.

The durable artifact is `build_connectome.py` + the pinned environment + the emitted `connectivity_*.csv`, the heatmap, and `provenance.json` — all under version control. Re-running on the same inputs with the same atlas release reproduces the matrices.

## Why this assembly

Rung 2. The skill gives Claude the correct Nilearn idioms and — critically — the step ordering (atlas → masker with standardization/detrend → confound regression → correlation) so the model does not reinvent the API or silently drop the confound step. Plain Claude Code *can* write Nilearn code, but the confound strategy and masker parameters are exactly where an unaided model tends to pick unstated defaults that leave motion artifact in the connectome. There is no reason to escalate: connectome construction from preprocessed BOLD is a well-defined, laptop-scale pipeline with a human-in-the-loop QC check, not a problem that needs a multi-tool harness or an autonomous system.

## Availability

Fully open. The Nilearn skill is community OSS (MIT, part of the NeuroClaw library); Nilearn is BSD-licensed, and the Schaefer/other bundled atlases are openly redistributable. No institutional access or subscription. Any current Claude plan works. This recipe starts from fMRIPrep outputs — running fMRIPrep itself (a separate BIDS-App step, not covered here) is the upstream prerequisite. The NeuroClaw skill assumes the collection's shared helpers; a standalone `pip install nilearn` covers the connectivity path.

## Compute requirements

Laptop. A single resting-state run (~5–10 min, one subject) extracts a 200-ROI time-series and builds the connectivity matrices in well under a minute on a modern laptop CPU; the slowest one-time step is fetching the atlas over the network. RAM 8–16 GB is ample for a single 4D BOLD volume in MNI space. Batch across many subjects by looping the same script — still CPU-only, still laptop-scale unless you run thousands of high-resolution sessions, in which case parallelize per subject.

## Evidence

Reported. Nilearn is the documented, field-standard Python library for machine learning and connectivity on neuroimaging data ([Abraham et al., *Front. Neuroinform.* 2014](https://doi.org/10.3389/fninf.2014.00014)), and the atlas time-series → confound regression → ROI-to-ROI correlation workflow this recipe encodes is the canonical one taught in the Nilearn and BrainIAK tutorials ([Kumar et al., *PLoS Comput. Biol.* 2020](https://doi.org/10.1371/journal.pcbi.1007549)) and reused across current resting-state connectivity studies — e.g., a 264-participant migraine rs-FC study ([Messina et al., *Neurology* 2026](https://doi.org/10.1212/WNL.0000000000214656)) and an adolescent-depression connectome-biomarker study using partial-correlation functional connectomes ([Dai et al., *J. Affect. Disord.* 2026](https://doi.org/10.1016/j.jad.2025.120969)). The Nilearn *skill* is the documented Claude assembly for driving these operations. No peer-reviewed head-to-head benchmark of this exact skill against a hand-written Nilearn script is known; the recipe inherits the robust component-level evidence for Nilearn and the well-established rs-FC methodology.

## Alternatives considered

- **Plain Claude Code + raw Nilearn.** Fine for users fluent in the Nilearn API who want no skill layer. The skill's value is encoding the step ordering and surfacing the confound/masker knobs so they don't get silently defaulted.
- **A GUI or fixed pipeline (CONN, C-PAC, fMRIPrep's own connectivity option) with no agent.** The right call for a lab that has standardized on one of those tools. Reach for this recipe when you want the connectome captured as re-runnable, version-controlled code you can vary the atlas and confound strategy on across many subjects.
- **Event-related EEG instead of resting-state fMRI.** If your data is EEG with event structure, the [ERP extraction recipe](extract-event-related-potentials-from-eeg.html) is the right sibling — a different modality and analysis.
- **An autonomous-science system.** None targets connectome construction; the problem is too well-scoped to justify one.

## See also

- [Nilearn (Claude Skill)](../../catalog/tools/nilearn-tool.html)
- [Extract event-related potentials from EEG epochs](extract-event-related-potentials-from-eeg.html) — the analogous single-modality, laptop-scale, skill-driven neuro recipe (EEG rather than fMRI).
- [Discover NWB recordings on DANDI and prepare them for sorting](discover-nwb-recordings-on-dandi.html) — find public electrophysiology recordings; the imaging-dataset counterpart (OpenNeuro) is a deferred sibling.

## Sources

- [Nilearn skill — `NeuroClaw/skills/nilearn-tool/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/nilearn-tool/SKILL.md) — catalog `last_verified` 2026-06-11; verified 2026-07-19 (this run).
- [Abraham et al., *Front. Neuroinform.* 8:14 (2014), doi:10.3389/fninf.2014.00014](https://doi.org/10.3389/fninf.2014.00014) — Machine learning for neuroimaging with scikit-learn (Nilearn).
- [Kumar et al., *PLoS Comput. Biol.* 16:e1007549 (2020), doi:10.1371/journal.pcbi.1007549](https://doi.org/10.1371/journal.pcbi.1007549) — BrainIAK tutorials, incl. Nilearn functional-connectivity workflows.
- [Messina et al., *Neurology* (2026), doi:10.1212/WNL.0000000000214656](https://doi.org/10.1212/WNL.0000000000214656) — 264-participant resting-state functional-connectivity study; verified 2026-07-19 (this run).
- [Dai et al., *J. Affect. Disord.* (2026), doi:10.1016/j.jad.2025.120969](https://doi.org/10.1016/j.jad.2025.120969) — partial-correlation functional-connectome biomarkers in adolescent depression; verified 2026-07-19 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=build-functional-connectivity-matrix-from-fmri&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fbuild-functional-connectivity-matrix-from-fmri.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
