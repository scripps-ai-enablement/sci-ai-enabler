---
title: Compute HRV from an ECG recording
parent: All recipes
grand_parent: Recipes
nav_order: 3
problem_class: Data analysis
subject_areas: [Neuroscience, Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-29
summary: Use the NeuroKit2 Claude Skill to clean an ECG trace, detect R-peaks, and return time-domain, frequency-domain, and non-linear HRV indices from a single conversation.
---

# Compute HRV from an ECG recording

Hand Claude Code a raw single-lead ECG file (CSV, EDF, or any of the formats NeuroKit2 ingests); get back a cleaned signal, a validated R-peak series, and the standard time-domain, frequency-domain, and non-linear HRV indices as a tidy DataFrame plus a one-page figure.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience, Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

HRV is the workhorse autonomic-nervous-system readout for psychophysiology, sleep research, sport science, and cardiology. The mechanics are not deep — clean the ECG, detect R-peaks, compute RR intervals, derive indices in three domains — but every group rebuilds the boilerplate, and a misplaced filter or the wrong peak detector silently corrupts SDNN, RMSSD, and the LF/HF ratio. Solved looks like: hand the agent a recording, get a validated peak series plus the canonical HRV table you can drop into a paper or a clinical report, with the parameter choices written down.

## Recommended approach

1. **Install the [NeuroKit2 skill](../../catalog/tools/neurokit2.html)** in Claude Code:

   ```
   /plugin marketplace add K-Dense-AI/claude-scientific-skills
   /plugin install neurokit2@claude-scientific-skills
   ```

   The skill imports the MIT-licensed `neurokit2` Python library. Confirm `pip show neurokit2` returns a version ≥ 0.2.

2. **Put the recording in your project.** NeuroKit2 reads NumPy arrays, pandas Series, EDF, MNE `Raw` objects, and many vendor formats. State the sampling rate explicitly — most HRV bugs trace back to a wrong sampling rate.

3. **Invoke the skill in chat with the file path and study context.** A minimal prompt:

   ```
   Run the neurokit2 skill on data/subj01_ecg.csv. Single-lead ECG,
   500 Hz sampling rate, 10-minute resting baseline. Clean with the
   default neurokit method, detect R-peaks with the neurokit detector,
   then compute HRV with nk.hrv() (all three domains: time, frequency,
   non-linear). Save the cleaned signal and peaks to
   data/subj01_processed.parquet and the HRV table to
   results/subj01_hrv.csv. Include the canonical 4-panel figure
   (raw ECG, cleaned signal + peaks, RR tachogram, Poincaré plot).
   ```

4. **Read the QC panel before trusting the numbers.** Have Claude flag obvious problems: ectopic-beat density, sustained signal loss, sampling-rate-vs-bandwidth mismatch. NeuroKit2's `nk.signal_quality` helpers give per-segment quality scores; ask for them when the recording is noisy.

   ```
   Compute nk.signal_quality on the cleaned ECG and exclude any 30s
   windows below 0.5. Recompute HRV on the surviving segments and
   show me how the indices shifted versus the unfiltered run.
   ```

5. **Switch to event-related analysis when the design demands it.** For task ECG (e.g., stress paradigm with cue-locked epochs), follow NeuroKit2's `nk.events_find` → `nk.epochs_create` → `nk.bio_analyze` pattern in the same conversation; the skill knows the idiom.

6. **Hand off.** The HRV CSV is the entry point for downstream stats (mixed models in R, group comparisons in `scipy.stats`). The processed Parquet preserves the peak series for later re-analysis.

## Why this assembly

Rung 2. NeuroKit2 *is* the validated HRV pipeline; the skill is a thin Claude wrapper that picks the right defaults and writes the right call. Plain Claude Code can call `nk.ecg_process` from memory but tends to drift on peak-detector choice and on whether to use `nk.hrv` versus the per-domain functions — that drift is exactly what the skill prevents. There is no need for a multi-tool harness or an autonomous system; HRV is a single, well-defined analytical task and a skill is the right grain.

## Availability

Fully open. NeuroKit2 is MIT-licensed and the K-Dense skill wrapper is OSS on the K-Dense marketplace. Any current Claude plan is enough. No institutional license or data-residency constraint — the recording stays local.

## Compute requirements

Laptop. A 10-minute single-lead 500 Hz ECG cleans, peak-detects, and HRV-derives in seconds on a modern laptop with 8 GB RAM. Multi-hour Holter recordings (24 h at 250 Hz) finish in a minute or two and consume ≤ 1 GB of working memory. No GPU needed.

## Evidence

Proposed. No peer-reviewed paper documents this *exact* assembly (Claude Code + the K-Dense NeuroKit2 skill) on HRV computation. The component evidence is robust:

- **NeuroKit2 itself** — [Makowski et al., *Behavior Research Methods* 53:1689–1696 (2021)](https://doi.org/10.3758/s13428-020-01516-y) is the canonical reference for the library. Time-domain, frequency-domain, and non-linear HRV pipelines are validated against the standard references in [Pham et al., *Sensors* 21:3998 (2021)](https://doi.org/10.3390/s21123998).
- **LLM-orchestrated biosignal analysis (analogous)** — the closest documented analogue is [EEGAgent (Yan et al., arXiv:2511.09947, 2025-11-12)](https://arxiv.org/abs/2511.09947), accepted to AAAI-26, which uses an LLM to plan and call EEG preprocessing / feature-extraction tools (different signal modality, custom toolbox, not NeuroKit2). EEGAgent demonstrates that LLM-driven scheduling of validated signal-processing primitives is viable, but does not benchmark Claude or NeuroKit2 specifically.

No published comparison of LLM-driven HRV against a hand-coded NeuroKit2 script is known. The skill adds consistent defaults and explicit parameter logging; it does not change the underlying numerical method.

## Alternatives considered

- **Plain Claude Code, no skill.** Works for users who write NeuroKit2 in their sleep. Reach for the skill when you want the defaults pinned (peak detector, cleaning method, HRV index list) across runs and across collaborators.
- **KUBIOS or pyHRV.** Domain-standard alternatives to NeuroKit2 for HRV specifically. Neither has a Claude-installable wrapper today; use them outside Claude Code when you need KUBIOS's clinical-validation pedigree.
- **An autonomous-science system.** No autonomous-science system in [`autonomous-science/systems/`](../../autonomous-science/) targets HRV. EEGAgent is the closest published harness (EEG, not ECG) and is not yet a maintained installable system.

## See also

- [NeuroKit2 (Claude Skill)](../../catalog/tools/neurokit2.html)
- [BIDS (Claude Skill)](../../catalog/tools/bids.html) — pair upstream when the ECG is part of a multi-modal BIDS dataset and needs to be organised before analysis.
- [Sort spikes from a Neuropixels recording end-to-end](sort-spikes-from-neuropixels-recording.html) — the systems-neuroscience companion when the signal is intracortical rather than peripheral.

## Sources

- [NeuroKit2 paper, Makowski et al. 2021 (Behavior Research Methods)](https://doi.org/10.3758/s13428-020-01516-y) — published 2021-02-02; verified 2026-05-29 (this run).
- [HRV indices tutorial, Pham et al. 2021 (Sensors)](https://doi.org/10.3390/s21123998) — published 2021-06-09; verified 2026-05-29 (this run).
- [EEGAgent preprint, Yan et al. (arXiv:2511.09947)](https://arxiv.org/abs/2511.09947) — posted 2025-11-12; verified 2026-05-29 (this run).
- [`scientific-skills/neurokit2/SKILL.md` (K-Dense)](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/neurokit2/SKILL.md) — verified 2026-05-29 (this run).
- [NeuroKit2 documentation](https://neuropsychology.github.io/NeuroKit/) — verified 2026-05-29 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=compute-hrv-from-ecg-recording&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fcompute-hrv-from-ecg-recording.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
