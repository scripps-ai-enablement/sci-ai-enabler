---
title: Discover NWB recordings on DANDI and prepare them for sorting
parent: All recipes
grand_parent: Recipes
nav_order: 4
problem_class: Knowledge synthesis
subject_areas: [Neuroscience]
evidence_level: Reported
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-29
summary: Use the Neurosift Tools MCP to find Neuropixels (or other extracellular) NWB sessions on DANDI matching your hypothesis, inspect them in-place, and stage a download list for downstream spike sorting.
---

# Discover NWB recordings on DANDI and prepare them for sorting

Hand Claude Code a query like "find Neuropixels recordings from mouse visual cortex with at least one hour of spontaneous activity" and get back a ranked list of DANDI sets, the specific NWB assets within them, an inspection of each file's `Units`, `ElectricalSeries`, and `TimeIntervals` neurodata objects, and a download plan ready to feed into the [Sort spikes from a Neuropixels recording](sort-spikes-from-neuropixels-recording.html) recipe.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Reported |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

DANDI hosts 400+ NWB neurophysiology datasets but the access path is hostile to casual reuse: each dandiset has its own README, the asset paths and subject metadata vary, and you cannot tell from the landing page whether an `ElectricalSeries` was recorded on a Neuropixels 1.0 probe at 30 kHz or a 64-channel silicon probe at 20 kHz without downloading the file. Working scientists routinely abandon the search after the third dandiset because the cost of "open the NWB and check" is half an hour per file. Solved looks like: a single conversation where you describe the recording you want, Claude searches DANDI by semantic query and by neurodata type, opens the NWB metadata remotely, summarizes what's actually inside each candidate, and writes the `dandi download` commands (or a streaming-read plan) for the subset you want to sort.

## Recommended approach

1. **Install the [Neurosift Tools MCP](../../catalog/tools/neurosift.html)** so Claude Code can hit the DANDI API and introspect NWB files without downloading them:

   ```
   git clone https://github.com/magland/neurosift-mcps
   cd neurosift-mcps/neurosift-tools
   npm install && npm run build
   claude mcp add --transport stdio neurosift-tools -- node $(pwd)/build/index.js
   ```

2. **Search DANDI semantically and by neurodata type.** A first prompt:

   ```
   Use the neurosift-tools MCP to find dandisets that contain
   Neuropixels recordings from mouse visual cortex with at least
   one hour of spontaneous activity. Use both dandi_semantic_search
   ("mouse V1 Neuropixels spontaneous") and
   dandi_search_by_neurodata_type with neurodata_type=ElectricalSeries.
   Cross-reference the result lists and return the top 10 dandisets
   with a one-line summary of each.
   ```

3. **Inspect the most promising assets in place.** Continue:

   ```
   For the top 3 dandisets, list all NWB assets via dandiset_assets
   and call nwb_file_info on the largest ElectricalSeries-containing
   asset in each. Report: subject species and age, probe model, channel
   count, sampling rate, session duration, whether a Units table is
   present (i.e., already sorted), and the names of any TimeIntervals
   tables (stimulus blocks, drift gratings, spontaneous epochs).
   ```

   `nwb_file_info` reads only the HDF5 metadata over HTTP — no full download is required.

4. **Filter to a sortable subset.** Now apply your hypothesis-specific constraints — duration ≥ 1 hour, no pre-existing `Units` table (so you can run your own sorter), Neuropixels 1.0 probe model, specific behavioral state. Ask Claude to write a CSV with one row per qualifying asset (dandiset ID, asset path, S3 URL, duration, probe).

5. **Generate the download (or streaming) plan.** Two options:

   ```
   For the filtered asset list, emit `dandi download` commands that
   pull each file into data/raw/<dandiset>/<asset_basename>. Also
   emit an alternative pynwb streaming snippet using fsspec + ros3
   for users who want to sort directly from S3 without local copies.
   ```

   Use [`pynwb_docs_semantic_search`](../../catalog/tools/neurosift.html) inside the same Claude session to ground the streaming snippet in current PyNWB / `remfile` / fsspec idioms rather than the model's training cutoff.

6. **Hand off to spike sorting.** When the local copies (or streaming reads) are ready, switch to the [Sort spikes from a Neuropixels recording](sort-spikes-from-neuropixels-recording.html) recipe to run preprocessing, drift correction, and Kilosort4 on each session.

7. **(Optional) Extend the reach to OpenNeuro.** If your question spans modalities (e.g., "mouse Neuropixels *or* macaque ECoG"), install the [OpenNeuro MCP](../../catalog/tools/openneuro.html) alongside Neurosift Tools — OpenNeuro and DANDI are separate archives, and `openneuro_search` covers the MRI / MEG / EEG / iEEG / ECoG portion that DANDI does not.

## Why this assembly

Rung 3 — a small toolbelt of two cataloged components (Neurosift Tools MCP for discovery + introspection; neuropixels-analysis skill for downstream sorting) plus optionally the OpenNeuro MCP for cross-archive reach. Rung 1 (plain Claude Code) fails because the model cannot reach the live DANDI API or read remote NWB metadata without help. Rung 2 (Neurosift Tools MCP alone) gets you the candidate list and the file inspection, but a complete recipe needs the downstream sorting skill to be useful for the working scientist's actual goal. An autonomous-science system is overkill: discovery + inspection is a well-bounded retrieval task that the dedicated MCP handles cleanly.

## Availability

Fully open. The Neurosift Tools MCP uses the public DANDI and OpenNeuro APIs with no authentication. The DANDI Archive itself is open; some embargoed dandisets require dandi-cli authentication, which Claude can drive with a user-supplied API token. The neuropixels-analysis skill is community OSS via the K-Dense marketplace. No subscription tier required.

## Compute requirements

Laptop. Discovery and NWB metadata inspection are network-bound, not compute-bound — `nwb_file_info` reads only HDF5 headers (kilobytes per file) over HTTP. The full download of 24 hours of Neuropixels data is hundreds of GB; budget disk accordingly *if* you choose download over streaming. Spike sorting (step 6) inherits the workstation-with-GPU requirement from the downstream recipe.

## Evidence

Reported. The Magland lab at Flatiron — same author as the Neurosift Tools MCP — published [Magland et al., *Scientific Data* 12:1988 (2025)](https://doi.org/10.1038/s41597-025-06285-x), documenting an LLM-driven agentic chat assistant and notebook generator that automates DANDI dataset exploration, NWB inspection, and analysis-notebook drafting. Neurophysiology-data specialists rated most of the auto-generated notebooks "very helpful." The MCP server packaged for Claude Code is the same tool family with the same back-end APIs (`dandi_search`, `dandi_semantic_search`, `nwb_file_info`, `pynwb_docs_semantic_search`); the recipe inherits the paper's evidence for the discovery + inspection half of the workflow. The downstream spike-sorting half inherits the `Reported` evidence on the [Sort spikes from a Neuropixels recording](sort-spikes-from-neuropixels-recording.html) recipe.

Component-level grounding for Neurosift itself: [Magland, Soules, Baker, Dichter, *JOSS* 9(97):6590 (2024)](https://doi.org/10.21105/joss.06590) (Neurosift browser visualizer paper); the MCP server is the agent-facing surface of the same project.

No peer-reviewed head-to-head benchmark of this *exact* MCP + skill assembly against a human DANDI search has been published; the Magland 2025 paper benchmarks the chat-assistant variant, not the Claude-Code-with-MCP variant specifically.

## Alternatives considered

- **Plain Claude Code + `dandi` CLI prompts.** Works for users who already know dandiset IDs and asset paths. It fails the moment you don't know which dandiset to look at — the model has no live DANDI index in its training data and will hallucinate dandiset numbers.
- **The Neurosift web UI ([neurosift.app](https://neurosift.app/))** without any agent in the loop. Excellent for one-off browsing of a known dandiset; not scalable when you need to triage dozens of candidates against a structured query.
- **The DANDI Archive's own LLM chat assistant** (the system described in Magland 2025). Comparable capability; use it instead when you do not need the downstream sorting step in the same conversation as the discovery step. This recipe is the right choice when you want one Claude Code session that goes from "what's on DANDI" to "sorted units in `data/sess_ks4/`."
- **AIND Data MCP for AIND-released datasets.** The [AIND Data MCP](../../catalog/tools/aind-data.html) is the right entry point for the Allen Institute for Neural Dynamics' open-data releases specifically; reach for it when your hypothesis is AIND-centric. DANDI is broader.

## See also

- [Neurosift Tools MCP](../../catalog/tools/neurosift.html)
- [OpenNeuro MCP](../../catalog/tools/openneuro.html)
- [neuropixels-analysis (Claude Skill)](../../catalog/tools/neuropixels-analysis.html)
- [Sort spikes from a Neuropixels recording end-to-end](sort-spikes-from-neuropixels-recording.html) — the natural downstream recipe.
- [AIND Data MCP](../../catalog/tools/aind-data.html) — Allen Institute for Neural Dynamics open-data discovery.

## Sources

- [Magland, Ly, Rübel, Dichter. *Scientific Data* 12:1988 (2025), doi:10.1038/s41597-025-06285-x](https://doi.org/10.1038/s41597-025-06285-x) — published 2025-08-08; verified 2026-05-29 (this run).
- [Magland, Soules, Baker, Dichter. *JOSS* 9(97):6590 (2024), doi:10.21105/joss.06590](https://doi.org/10.21105/joss.06590) — published 2024-05-27.
- [`magland/neurosift-mcps`](https://github.com/magland/neurosift-mcps) — verified 2026-05-29 (this run).
- [DANDI Archive](https://dandiarchive.org/) — verified 2026-05-29 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=discover-nwb-recordings-on-dandi&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdiscover-nwb-recordings-on-dandi.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
