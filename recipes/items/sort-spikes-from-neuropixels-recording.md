---
title: Sort spikes from a Neuropixels recording end-to-end
parent: All recipes
grand_parent: Recipes
nav_order: 5
problem_class: Data analysis
subject_areas: [Neuroscience]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-05-22
summary: Use the K-Dense neuropixels-analysis skill in Claude Code to take a raw SpikeGLX or Open Ephys Neuropixels recording through preprocessing, drift correction, and Kilosort4 to curated single units.
---

# Sort spikes from a Neuropixels recording end-to-end

Hand Claude Code a raw SpikeGLX, Open Ephys, or NWB Neuropixels recording; get back motion-corrected data, Kilosort4 (or SpykingCircus2 / Mountainsort5) spike-sorted units, and an AI-assisted curation pass that flags merges, splits, and likely noise clusters before you hand-curate.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

Neuropixels recordings yield gigabytes per probe per session and the spike-sorting pipeline that turns voltage into single units is fiddly: phase-shift correction, common-average referencing, bad-channel detection, drift estimation, sorter choice, post-sorting curation. Every lab rolls its own SpikeInterface boilerplate and the parameters that work for an Allen-style cortical recording often fail on a brainstem session. Solved looks like: a single conversation that loads the recording, applies the standard preprocessing chain, runs a state-of-the-art sorter under the right preset, and emits a curated unit table you can open in Phy or push to NWB.

## Recommended approach

1. **Install the [neuropixels-analysis](../../catalog/tools/neuropixels-analysis.html) skill** in Claude Code:

   ```
   /plugin marketplace add K-Dense-AI/claude-scientific-skills
   /plugin install neuropixels-analysis@claude-scientific-skills
   ```

   Verify the environment has SpikeInterface installed (`pip install spikeinterface[full]`) and a CUDA-capable GPU available if you intend to run Kilosort4.

2. **Point the skill at your recording.** A minimal prompt:

   ```
   Run the neuropixels-analysis skill on
   data/session2026-05-01_g0_imec0/. The recording is SpikeGLX
   Neuropixels 1.0, ~90 minutes, mouse motor cortex. Apply the
   standard preprocessing chain: phase-shift correction, highpass
   300 Hz, bad-channel detection (kurt threshold), common-average
   reference. Then estimate motion with the nonrigid_accurate preset
   and write the corrected recording to data/sess_preproc/.
   ```

3. **Sort with Kilosort4 (GPU) or SpykingCircus2 (CPU fallback).** Continue the conversation:

   ```
   Run Kilosort4 on the preprocessed recording with the default
   Neuropixels 1.0 parameters. Save sorting output to
   data/sess_ks4/. Then compute SpikeInterface quality metrics
   (ISI violations, presence ratio, amplitude SNR, refractory period
   violation) on all units.
   ```

4. **Use the AI-assisted curation pass** the skill bundles to flag obvious noise clusters and merge / split candidates:

   ```
   Use the skill's curation helpers to triage units into "good",
   "mua", and "noise" categories based on the quality metrics. For
   units flagged as candidate merges, show me the cross-correlograms
   and waveform similarity before I confirm.
   ```

5. **Export to NWB or Phy for hand-curation.** The skill writes a standard SpikeInterface sorting object that loads directly into Phy or `pynwb`. Hand-curation remains a human step; the skill does *not* claim to replace it.

6. **(Optional) Cross-sort comparison.** When the result is high-stakes (a publication figure), run a second sorter (SpykingCircus2 or Mountainsort5) and ask Claude to report unit agreement via `SpikeInterface.comparison`. Disagreement is informative even when neither sorter is "right".

## Why this assembly

Rung 2. The skill is a thin but valuable wrapper: it encodes the SpikeInterface / Allen Institute / International Brain Laboratory consensus on preprocessing and gives Claude the right knobs for drift correction and sorter selection without re-inventing the parameter file. Plain Claude Code can write SpikeInterface code but does not reliably pick the right drift preset for the session or the right quality-metric thresholds. There is no need to escalate to an autonomous system — spike sorting is a well-defined pipeline with discrete steps and human-in-the-loop curation at the end.

## Availability

Fully open. The neuropixels-analysis skill is community OSS distributed via the K-Dense marketplace; SpikeInterface, Kilosort4, SpykingCircus2, and Mountainsort5 are all open-source. No institutional license. Any current Claude plan works.

## Compute requirements

Workstation with GPU. Kilosort4 effectively requires a CUDA GPU with ≥8 GB VRAM; a 90-minute Neuropixels 1.0 recording sorts in roughly 20–40 minutes on an RTX 4090. SpykingCircus2 and Mountainsort5 fall back to CPU but are 5–10× slower on the same recording. Disk: budget 3–5× the raw recording size for preprocessed and intermediate files. System RAM 32 GB recommended.

## Evidence

Reported. The K-Dense [neuropixels-analysis skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/neuropixels-analysis/SKILL.md) is the documented assembly and tracks SpikeInterface best practices directly. The closest peer-style evaluation of LLM-driven spike sorting is the [SpikeAgent preprint](https://doi.org/10.1101/2025.02.11.637754) (posted 2025-02-11), which reports a multimodal LLM-based system automating spike-sorting across recording platforms including Neuropixels, with performance varying by backend model — the recipe inherits that "model-dependent" caveat. No peer-reviewed benchmark of *this exact skill* against a hand-tuned SpikeInterface script is known.

The component-level evidence for the underlying tools is robust: SpikeInterface (Buccino et al., *eLife* 2020) and Kilosort4 (Pachitariu et al., *Nature Methods* 2024) are widely adopted in the systems-neuroscience community.

## Alternatives considered

- **Plain Claude Code + raw SpikeInterface.** Works for users who already know SpikeInterface idioms cold. The skill saves you from re-learning the parameter knobs each session and standardizes the preprocessing chain.
- **A standalone Kilosort4 GUI workflow with no Claude in the loop.** The right answer when you sort the same probe layout daily and have a saved parameter file. Reach for the skill when sessions vary (different probe types, brain regions, durations) or when you want the metric-driven triage step automated.
- **Neurosift / AIND for *finding* recordings, then this skill for sorting.** Pair the [Neurosift Tools MCP](../../catalog/tools/neurosift.html) or [AIND Data MCP](../../catalog/tools/aind-data.html) upstream when you are sorting a public DANDI dataset; this recipe assumes the recording is local.
- **An autonomous-science system.** No such system targets spike sorting end-to-end today. SpikeAgent is the closest published prototype and is not a maintained installable system yet.

## See also

- [neuropixels-analysis (Claude Skill)](../../catalog/tools/neuropixels-analysis.html)
- [Neurosift Tools MCP](../../catalog/tools/neurosift.html) — discover and inspect NWB recordings on DANDI/OpenNeuro before sorting.
- [AIND Data MCP](../../catalog/tools/aind-data.html) — find AIND open neurophysiology datasets.

## Sources

- [`neuropixels-analysis/SKILL.md` (K-Dense)](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/neuropixels-analysis/SKILL.md) — last updated 2026-05; verified 2026-05-22 (this run).
- [SpikeAgent preprint, doi:10.1101/2025.02.11.637754](https://doi.org/10.1101/2025.02.11.637754) — posted 2025-02-11.
- [SpikeInterface documentation](https://spikeinterface.readthedocs.io/) — verified 2026-05-22 (this run).
