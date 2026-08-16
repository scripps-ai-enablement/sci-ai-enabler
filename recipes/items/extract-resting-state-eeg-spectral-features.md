---
title: Extract spectral features from resting-state EEG
parent: All recipes
grand_parent: Recipes
nav_order: 12
problem_class: Data analysis
subject_areas: [Neuroscience]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-16
summary: Use the EEG Processing skill in Claude Code plus specparam/FOOOF to turn eyes-closed resting recordings into per-channel band power and aperiodic exponents.
---

# Extract spectral features from resting-state EEG

Turn a set of eyes-closed resting-state EEG recordings into a per-subject, per-channel feature table — band power **and** the aperiodic exponent and offset, separated rather than conflated — as a committed script with the analytic choices recorded.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Resting-state EEG is the cheapest recording in neuroscience and the most casually analyzed. The default workflow — Welch PSD, then average power in fixed alpha/beta/theta windows — has a known defect: an EEG power spectrum is a broadband 1/f-like aperiodic component *plus* narrowband peaks, so "alpha power" in a fixed 8–13 Hz window moves whenever the aperiodic slope moves, even with no oscillation change at all. Groups differing in age, medication, arousal or sleep stage differ in that slope, which is exactly when the confound bites: the aperiodic exponent varies strongly and systematically across sleep stages and is modulated by dopaminergic medication in Parkinson's disease, so band-power differences between such groups are uninterpretable until the two components are split.

Splitting them introduces its own trap. The separation is a model fit with user-set knobs — fit range, maximum number of peaks, PSD estimation method — and those choices measurably change how reliable the recovered exponent is. Solved looks like: a committed script that goes from raw files to one tidy feature table containing both periodic and aperiodic parameters, with every knob written down as a named variable and echoed into a provenance record, plus a per-channel fit-quality column you can filter on.

## Recommended approach

1. **Install the [EEG Processing skill](../../catalog/tools/eeg-skill.html)** in Claude Code. It triggers on exactly this ask ("band power", "downsample to frequency bands", resting-state files in `.set`/`.edf`/`.bdf`/`.fif`) and supplies the load → clean → epoch → feature ordering so the model doesn't reinvent it per session.

2. **Add the spectral-parameterization dependency** (see [Dependencies](#dependencies)). This is the piece the skill does not cover: the skill gives you a PSD, `fooof` gives you the periodic/aperiodic decomposition of it.

3. **Have the assistant write one versioned script, not an interactive session.** A prompt that produces the right artifact:

   ```
   Using the eeg-skill, write me a script resting_spectral.py that walks
   data/sub-*/eeg/*_task-rest_eeg.edf and, per subject, per channel:
   - sets the standard_1020 montage and an average reference
   - band-passes 1-45 Hz, notch 60 Hz, and drops annotated bad segments
   - epochs the continuous recording into 4 s non-overlapping windows
   - computes a Welch PSD (record n_fft, window, overlap as variables)
   - fits a FOOOF/specparam model over a stated fit range and a stated
     max_n_peaks, and writes per channel: aperiodic exponent, offset,
     fit r_squared, fit error, plus the fitted peak center frequency,
     power and bandwidth for any peak in the alpha range
   - ALSO writes raw fixed-window band power for comparison, labelled
     as such so the two are never confused downstream
   Emit out/spectral_features.csv (one row per subject x channel) and
   out/fits/sub-XX_<channel>.png for spot-checking. Every threshold,
   fit range, band edge and peak limit must be a named constant at the
   top of the file with a comment - no silent defaults.
   ```

4. **Decide the fit range and peak count before you look at group labels, and record them.** These are the choices that move the answer: allowing more peaks to be extracted *reduces* the reliability of the exponent and offset estimates and generates more outliers. Pick `max_n_peaks` and the fit range from your hypothesis, write them into the script as literals with a comment saying why, and do not tune them after seeing the group contrast.

5. **Gate on fit quality before any statistics.** Have the script apply a pre-registered `r_squared` floor per channel-fit, write the excluded subject/channel IDs to `out/excluded_fits.csv`, and report how many were dropped. A poor 1/f fit produces a confidently wrong exponent, and it leaves no trace in the feature table unless you put it there.

6. **Pin the environment and record provenance.** Emit a `requirements.txt` pinning `mne`, `fooof`, `numpy`, `scipy`, `pandas`, `matplotlib`, and have the script write `out/provenance.json` with: the MNE and `fooof` versions, montage and reference, filter cutoffs, epoch length, Welch parameters, fit range, `max_n_peaks` and `peak_width_limits`, the `r_squared` floor and the count excluded, the `sha256` of each input file, the run date, and the model/agent identity. Follow the pattern in the [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide.

The durable artifact is `resting_spectral.py` + the pinned `requirements.txt` + the emitted `spectral_features.csv`, `excluded_fits.csv`, fit figures, and `provenance.json`, all under version control. Re-running on the same inputs reproduces the table byte-for-byte — the spectral path has no stochastic step (unlike the ICA in the sibling ERP recipe).

## Dependencies

Libraries this recipe's script installs and imports directly. Claude Code installs these into your project environment — they are not available in Claude.ai chat.

| Package | Registry | Pinned | License | Import | Source (fetched 2026-08-16) |
|---|---|---|---|---|---|
| fooof | PyPI | `1.1.1` | Apache-2.0 | `fooof` | [fooof-tools/fooof](https://github.com/fooof-tools/fooof) |

```
pip install fooof==1.1.1
python3 -c "import fooof"
```

`fooof` 1.1.1 (released 2025-05-05) is the current stable line; the successor package `specparam` is at `2.0.0rc7` and is still a release candidate, so this recipe pins the stable predecessor. No model weights or data are downloaded on first use. MNE-Python itself is not listed here — it is the runtime dependency of the EEG Processing skill and its install is covered on that component's catalog page.

## Why this assembly

Rung 2, and it stops there. The skill supplies the settled part (load, montage, reference, filter, epoch, PSD) and one pinned library supplies the part the skill lacks (periodic/aperiodic separation). Everything that decides whether the result is trustworthy is a recorded literal in the script, not a tool capability: the fit range, the peak limit, the quality floor. Plain Claude Code can write MNE and FOOOF calls, but the failure mode here is not API errors — it is silently defaulted parameters in a pipeline whose output looks identical either way, and the skill's job is to surface the sequence so those knobs are visible. Nothing about band power or 1/f fitting needs a multi-tool harness or an autonomous system.

## Availability

Fully open. The EEG Processing skill is community OSS (MIT, part of the NeuroClaw library); MNE-Python is BSD-3-Clause; `fooof` is Apache-2.0. No subscription, institutional access, or account beyond a current Claude plan. NeuroClaw skills assume the collection's shared helpers — run the bundled `installer/setup.py` if the skill reports missing dependencies, though `pip install mne fooof` covers this path standalone.

## Compute requirements

Laptop, CPU only. A single 64-channel, 5-minute eyes-closed recording filters, epochs, and PSD-fits in well under a minute; the FOOOF fits are per-channel and cheap (order of milliseconds each, so ~64 fits is negligible). A 60-subject cohort runs in a handful of minutes serially. 8 GB RAM is ample. The dominant cost is your own time inspecting the per-channel fit figures — budget that, and consider having the script emit a single contact-sheet montage per subject instead of 64 separate PNGs.

## Evidence

**Proposed** — no documented attempt at this exact Claude assembly (EEG Processing skill + `fooof`) on resting-state EEG is known. The component and method legs are individually strong:

- The periodic/aperiodic separation is a mainstream, validated method with a published head-to-head of the two dominant implementations (FOOOF vs. IRASA) against ground-truth simulations across EEG, MEG, and LFP data, including where each fails ([Gerster et al., *Neuroinformatics* 2022](https://doi.org/10.1007/s12021-022-09581-8)).
- The analytic-choice gate in step 4 is not a hunch: across a resting-state and a task dataset, odd–even reliability of the aperiodic intercept and slope *fell* as more peaks were allowed to be extracted, with more outliers generated ([Kałamała et al., *Psychophysiology* 2026](https://doi.org/10.1111/psyp.70272)).
- The confound the recipe exists to avoid is documented in both directions: aperiodic parameters vary systematically across sleep stages, age, sex, and region in 251 subjects ([Schneider et al., *Front. Neuroinform.* 2022](https://doi.org/10.3389/fninf.2022.989262)), and are modulated by dopaminergic medication in Parkinson's disease ([Wang et al., *Eur. J. Neurosci.* 2022](https://doi.org/10.1111/ejn.15774)) — so a fixed-window band-power contrast between such groups is confounded by construction.
- MNE-Python, which the skill drives, is the field-standard M/EEG toolbox ([Gramfort et al., *Front. Neurosci.* 2013](https://doi.org/10.3389/fnins.2013.00267)).

## Alternatives considered

- **Plain Claude Code + MNE and FOOOF directly (rung 1).** Reasonable if you already know both APIs; you lose the skill's step ordering, which is where unaided models tend to substitute defaults for decisions. Reach for it if you don't want a skill layer.
- **Fixed-window band power alone, no decomposition.** Defensible in one narrow case: a within-subject, within-session contrast where the aperiodic component is unlikely to shift. Any between-group comparison involving age, medication, arousal, or sleep should not use it.
- **Time-resolved parameterization.** If the aperiodic component itself changes *during* the recording (task blocks, drowsiness onset), a static per-recording fit averages that away; SPRiNT-style time-resolved decomposition is the right tool ([Wilson et al., *eLife* 2022](https://doi.org/10.7554/eLife.77348)). That is a different recipe, not this one.
- **The [NeuroKit2 skill](../../catalog/tools/neurokit2.html) instead.** It also does EEG bandpower and complexity measures and is the better pick when EEG is one channel among ECG/EDA/RSP in a multi-modal psychophysiology study. For an EEG-only montage-aware pipeline, the EEG Processing skill fits closer.

## See also

- [EEG Processing (Claude Skill)](../../catalog/tools/eeg-skill.html)
- [NeuroKit2 (Claude Skill)](../../catalog/tools/neurokit2.html)
- [Extract event-related potentials from EEG epochs](extract-event-related-potentials-from-eeg.html) — the event-locked sibling; use it when your recording has stimulus markers.
- [Compute HRV from an ECG recording](compute-hrv-from-ecg-recording.html) — the analogous single-signal, laptop-scale biosignal recipe.
- [Discover NWB recordings on DANDI and prepare them for sorting](discover-nwb-recordings-on-dandi.html) — finding public recordings to run this on.

## Sources

- [EEG Processing skill — `NeuroClaw/skills/eeg-skill/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/eeg-skill/SKILL.md) — catalog `verification: works` 2026-07-20; read 2026-08-16 (this run).
- [`fooof` on PyPI](https://pypi.org/project/fooof/) — 1.1.1, Apache-2.0, released 2025-05-05; fetched 2026-08-16 (this run).
- [Kałamała et al., *Psychophysiology* (2026), doi:10.1111/psyp.70272](https://doi.org/10.1111/psyp.70272) — reliability of aperiodic parameter estimates as a function of analytic choices.
- [Gerster et al., *Neuroinformatics* 20:991 (2022), doi:10.1007/s12021-022-09581-8](https://doi.org/10.1007/s12021-022-09581-8) — FOOOF vs. IRASA against simulated ground truth.
- [Schneider et al., *Front. Neuroinform.* 16:989262 (2022), doi:10.3389/fninf.2022.989262](https://doi.org/10.3389/fninf.2022.989262) — aperiodic and oscillatory spectral measures across sleep stages, n=251.
- [Wang et al., *Eur. J. Neurosci.* (2022), doi:10.1111/ejn.15774](https://doi.org/10.1111/ejn.15774) — aperiodic parameters modulated by dopaminergic medication in Parkinson's disease.
- [Wilson et al., *eLife* 11:e77348 (2022), doi:10.7554/eLife.77348](https://doi.org/10.7554/eLife.77348) — SPRiNT time-resolved spectral parameterization.
- [Gramfort et al., *Front. Neurosci.* 7:267 (2013), doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267) — MNE-Python.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=extract-resting-state-eeg-spectral-features&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fextract-resting-state-eeg-spectral-features.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
