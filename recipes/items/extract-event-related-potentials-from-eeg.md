---
title: Extract event-related potentials from EEG epochs
parent: All recipes
grand_parent: Recipes
nav_order: 11
problem_class: Data analysis
subject_areas: [Neuroscience]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-12
summary: Use the MNE-Python EEG skill in Claude Code to filter, ICA-clean, epoch around event markers, and average a raw continuous EEG file into per-condition evoked responses.
---

# Extract event-related potentials from EEG epochs

Hand Claude Code a raw continuous EEG recording plus its event markers; get back a filtered, artifact-cleaned, epoched dataset and per-condition averaged evoked responses (ERPs) with the preprocessing decisions written down and re-runnable.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Turning a continuous scalp-EEG recording into publication-ready event-related potentials is a fixed sequence of steps — set the montage, band-pass filter, detect and remove eye-blink/muscle artifacts (usually ICA), epoch around stimulus markers, reject or repair bad epochs, baseline-correct, and average per condition — but each step hides a parameter that silently corrupts the P100/N170/P300 if set wrong (a 0.1 Hz vs 1 Hz high-pass changes slow ERP components; the wrong reference distorts topographies; over-aggressive epoch rejection biases the average). Every lab rebuilds this boilerplate in MNE-Python. Solved looks like: hand the agent the raw file and an events description, get back committed code that produces the evoked objects, per-condition ERP figures, and a record of every filter cutoff, rejected-epoch count, and ICA component removed.

## Recommended approach

1. **Install the [MNE-Python (EEG) skill](../../catalog/tools/mne-eeg-tool.html)** in Claude Code (it wraps the concrete MNE-Python idioms for loading, filtering, ICA, epoching, and evoked averaging):

   ```
   git clone https://github.com/CUHK-AIM-Group/NeuroClaw
   cp -r NeuroClaw/skills/mne-eeg-tool ~/.claude/skills/
   ```

   Verify MNE-Python is importable in the environment (`pip install mne`). No GPU needed.

2. **Have the assistant write a versioned pipeline script, not run steps interactively.** A minimal prompt:

   ```
   Using the mne-eeg-tool skill, write me a script preprocess_erp.py
   that takes data/sub-01_task-oddball_eeg.edf and its events
   (target vs standard tones, from the annotations). The script must:
   - set the standard_1020 montage, set average reference (projection)
   - band-pass 0.1-40 Hz, notch 60 Hz
   - fit ICA (picard, n_components=0.99) and remove EOG components
     identified via the Fp1/Fp2 channels; log which components were dropped
   - epoch -0.2 to 0.8 s around each event, baseline (-0.2, 0),
     reject epochs by peak-to-peak amplitude with a stated threshold
   - average per condition into evoked objects, save to
     out/sub-01_ave.fif, and write out/erp_counts.csv (epochs kept/
     rejected per condition)
   Do not hardcode magic numbers silently — surface every threshold
   as a variable at the top of the file with a comment.
   ```

3. **Pin the environment.** Ask the assistant to emit a `requirements.txt` (or `environment.yml`) pinning `mne`, `scikit-learn`, `python-picard`, `numpy`, `scipy`, `matplotlib`. Commit the script and the environment together.

4. **Run it and inspect the ERP figures.** Have the assistant add a step that saves per-condition butterfly plots and a difference-wave figure (target − standard) at the electrode of interest (e.g., Pz for P300) to `out/`. Eyeball the topographies and the rejected-epoch count before trusting the average.

5. **Record provenance.** Have the script write `out/provenance.json` capturing: MNE version, the montage name, filter cutoffs, notch frequency, ICA method and the exact component indices removed, the rejection threshold and per-condition kept/rejected counts, the input file `sha256`, the run date, and the model/agent identity. Non-byte-reproducible pieces (ICA fits are seed-sensitive) become auditable this way — set and record `random_state`. See the [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide for the pattern.

The durable artifact is `preprocess_erp.py` + the pinned environment + the emitted `*_ave.fif`, `erp_counts.csv`, and `provenance.json` — all under version control. Re-running on the same input reproduces the evoked files (modulo the recorded ICA seed).

## Why this assembly

Rung 2. The skill is a thin wrapper that gives Claude the correct MNE-Python idioms and the ordering discipline (montage → filter → ICA → epoch → average) without the model reinventing the API each session. Plain Claude Code *can* write MNE code, but it is exactly the parameter choices — high-pass cutoff, reference, ICA component selection, rejection threshold — where an unaided model tends to pick silent defaults that distort ERP components. There is no reason to escalate: ERP extraction is a well-defined, laptop-scale pipeline with a human-in-the-loop figure check at the end, not a problem that needs a multi-tool harness or an autonomous system.

## Availability

Fully open. The MNE-Python (EEG) skill is community OSS (MIT, part of the NeuroClaw library); MNE-Python is BSD-licensed. No institutional access or subscription. Any current Claude plan works. The NeuroClaw skill assumes the collection's shared helpers — install those (or run the bundled `installer/setup.py`) if the skill reports missing dependencies, though a standalone `pip install mne python-picard` covers the ERP path.

## Compute requirements

Laptop. A single-subject 64-channel recording of ~20 minutes filters, ICA-fits, and epochs in a few minutes on a modern laptop CPU; ICA (`picard`) is the slowest step at roughly 1–3 minutes for 64 channels. RAM 8–16 GB is ample. Batch across many subjects by looping the same script — still CPU-only, still laptop-scale unless you have hundreds of high-density sessions, in which case parallelize per subject.

## Evidence

Reported. MNE-Python is the documented, field-standard M/EEG analysis toolbox ([Gramfort et al., *Front. Neurosci.* 2013](https://doi.org/10.3389/fnins.2013.00267)), and the filter → ICA → epoch → average ERP workflow this recipe encodes is the canonical one taught in the MNE tutorials and reused across recent reproducible-pipeline packages built *on* MNE-Python (e.g., [EEG-Pype, *PLoS Comput. Biol.* 2026](https://doi.org/10.1371/journal.pcbi.1014043); [PyLossless, *Behav. Res. Methods* 2026](https://doi.org/10.3758/s13428-026-02997-z); [osl-ephys, *Front. Neurosci.* 2025](https://doi.org/10.3389/fnins.2025.1522675)). The MNE-EEG *skill* is the documented Claude assembly for driving these operations. No peer-reviewed head-to-head benchmark of this exact skill against a hand-written MNE script is known; the recipe inherits the robust component-level evidence for MNE-Python and the well-established ERP methodology.

## Alternatives considered

- **Plain Claude Code + raw MNE-Python.** Fine for users fluent in the MNE API who want no skill layer. The skill's value is encoding the step ordering and surfacing the parameter knobs so they don't get silently defaulted.
- **A GUI pipeline (EEG-Pype, EEGLAB, or MNE's own interactive plots) with no agent.** The right call for a one-off dataset where you want to click through manual bad-channel/epoch selection. Reach for this recipe when you want the pipeline captured as re-runnable, version-controlled code across many subjects.
- **Resting-state spectral analysis instead of ERPs.** If your recording has no event structure and you want band-power and aperiodic parameters rather than event-locked averages, use the sibling recipe [Extract spectral features from resting-state EEG](extract-resting-state-eeg-spectral-features.html).
- **An autonomous-science system.** None targets ERP extraction; the problem is too well-scoped to justify one.

## See also

- [MNE-Python (EEG) (Claude Skill)](../../catalog/tools/mne-eeg-tool.html)
- [Discover NWB recordings on DANDI and prepare them for sorting](discover-nwb-recordings-on-dandi.html) — find public EEG/electrophysiology recordings to run this on.
- [Compute HRV from an ECG recording](compute-hrv-from-ecg-recording.html) — the analogous single-signal, laptop-scale, skill-driven biosignal recipe.

## Sources

- [MNE-Python (EEG) skill — `NeuroClaw/skills/mne-eeg-tool/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/mne-eeg-tool/SKILL.md) — catalog `last_verified` 2026-06-11; verified 2026-07-12 (this run).
- [Gramfort et al., *Front. Neurosci.* 7:267 (2013), doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267) — MEG/EEG data analysis with MNE-Python.
- [EEG-Pype, *PLoS Comput. Biol.* (2026), doi:10.1371/journal.pcbi.1014043](https://doi.org/10.1371/journal.pcbi.1014043) — MNE-Python-based reproducible EEG pipeline; verified 2026-07-12 (this run).
- [osl-ephys, *Front. Neurosci.* 19:1522675 (2025), doi:10.3389/fnins.2025.1522675](https://doi.org/10.3389/fnins.2025.1522675) — MNE-Python-based M/EEG analysis toolbox.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=extract-event-related-potentials-from-eeg&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fextract-event-related-potentials-from-eeg.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
