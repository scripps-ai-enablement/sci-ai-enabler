---
title: Organize a raw DICOM dataset into a BIDS layout
parent: All recipes
grand_parent: Recipes
nav_order: 16
problem_class: Workflow automation
subject_areas: [Neuroscience]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-05
summary: Drive HeuDiConv or dcm2bids from Claude Code via the K-Dense BIDS skill to convert a raw DICOM dump into a validated BIDS dataset ready for BIDS-Apps and OpenNeuro submission.
---

# Organize a raw DICOM dataset into a BIDS layout

Point Claude Code at a directory of vendor DICOMs (Siemens, GE, Philips), and end up with a BIDS-valid dataset — proper `sub-XX/ses-YY/anat/` etc. layout, `dataset_description.json`, `participants.tsv`, JSON sidecars, and a clean BIDS-validator run — ready for fMRIPrep, MRIQC, QSIPrep, or OpenNeuro submission.

| | |
|---|---|
| **Problem class** | Workflow automation |
| **Subject areas** | Neuroscience |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A new MRI cohort lands as a directory of vendor DICOMs — typically tens of GB across 20–200 subjects, each with several scan series, often with cryptic series descriptions (`ep2d_bold_mb4_TR720`, `mprage_acq-mp2rage_inv-2`) that nobody documented. Before any BIDS-App will touch it, you need ProtocolName / SeriesDescription parsing, run/echo/inv-number disambiguation, a HeuDiConv heuristic file or a dcm2bids config, a populated `participants.tsv`, JSON sidecars with the right `IntendedFor` cross-links for fieldmaps, and a `bids-validator` pass with zero errors. Done by hand, a single cohort is a week. Solved looks like: hand Claude Code the DICOM directory and a brief description of the protocol, and get back a validated BIDS dataset with a regenerable heuristic / config you can rerun on the next acquisition.

## Recommended approach

1. **Install the [BIDS Claude Skill](../../catalog/tools/bids.html)** so Claude Code has the BIDS schema, HeuDiConv / dcm2bids / BIDScoin invocation patterns, and the PyBIDS query API in context:

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   # enable the `bids` skill when prompted
   ```

   Also install the converter binaries the skill drives (HeuDiConv ships a Docker image; `dcm2bids` and `bids-validator` install via pip / npm):

   ```
   pip install heudiconv dcm2bids
   npm install -g bids-validator
   ```

2. **Survey the DICOM tree first.** Give Claude the path and ask for a series-level inventory before any conversion:

   ```
   Use the bids skill. Walk DCM/ and produce a CSV with one row per
   unique (PatientID, StudyDate, SeriesDescription, SequenceName,
   ProtocolName, Manufacturer, AcquisitionType) tuple. Include the
   number of files in each series and the first DICOM path. Don't
   convert anything yet — I want to inspect the inventory first.
   ```

   This grounds every later decision in the *actual* contents of the dataset, not in the model's prior about how Siemens scanners name sequences.

3. **Draft the heuristic together.** For HeuDiConv (the recommended path when you have ≥10 subjects acquired with the same protocol), ask Claude to draft a `heuristic.py` from the inventory:

   ```
   From the inventory CSV, draft a HeuDiConv heuristic.py. Map each
   SeriesDescription to the right BIDS suffix (T1w, T2w, bold, dwi,
   fmap/magnitude1, fmap/phasediff). Use the ReproIn convention where
   it matches, fall back to custom create_key calls otherwise. For BOLD
   runs, parse the task label out of ProtocolName. For fieldmaps,
   populate IntendedFor with the matching BOLD/DWI runs in the same
   session. Save to heuristics/cohortname.py and print a dry-run plan.
   ```

   For smaller / heterogeneous cohorts, ask for a `dcm2bids` config file (`dcm2bids_config.json`) instead — its JSON criteria-matching is friendlier when you'll hand-tune per subject.

4. **Run a single-subject dry-run.** HeuDiConv has a `--dry-run` mode that prints the conversion plan without writing files:

   ```
   heudiconv -d 'DCM/{subject}/*/*.dcm' -o bids/ -f heuristics/cohortname.py \
     -s sub-001 -c none --dry-run
   ```

   Have Claude read the dry-run output, flag any series that fell through to "no key" or got mapped to an ambiguous suffix, and edit the heuristic.

5. **Convert the cohort.** Once the single-subject dry-run is clean, run the full conversion (this step is I/O- and `dcm2niix`-bound, not LLM-bound):

   ```
   heudiconv -d 'DCM/{subject}/*/*.dcm' -o bids/ -f heuristics/cohortname.py \
     -s sub-001 sub-002 ... -c dcm2niix -b --overwrite
   ```

6. **Author dataset metadata.** Ask Claude to populate the required and recommended top-level files:

   ```
   Author bids/dataset_description.json (Name, BIDSVersion 1.10.0,
   DatasetType raw, Authors, License, Acknowledgements,
   ReferencesAndLinks), bids/README, bids/CHANGES, and
   bids/participants.tsv with age, sex, group columns sourced from
   the demographics CSV at metadata/demographics.csv. Add a
   participants.json describing each column with Levels for categorical
   variables.
   ```

7. **Validate before declaring victory.** Run the official BIDS validator and have Claude triage the report:

   ```
   bids-validator bids/ --verbose --json > validation_report.json
   ```

   ```
   Read validation_report.json. For each error, explain what the rule
   means, point to the file that violates it, and propose a fix.
   Group errors by class: missing required sidecar fields, IntendedFor
   path mismatches, run-index gaps, unknown filename entities.
   ```

8. **(Optional) Query with PyBIDS.** Once the validator returns zero errors, confirm the cohort the way a downstream BIDS-App will see it:

   ```python
   from bids import BIDSLayout
   layout = BIDSLayout("bids/")
   print(layout.get_subjects(), layout.get_tasks(), layout.get_sessions())
   print(layout.get(suffix="bold", extension=".nii.gz", return_type="filename"))
   ```

   Ask Claude to write the equivalent of your downstream BIDS-App's expected file pattern and report any subject missing it. This catches "validator-clean but missing the run my fMRIPrep call needs" cases.

9. **Hand off.** The validated dataset is now an acceptable input for fMRIPrep, MRIQC, QSIPrep, and OpenNeuro submission. The BIDS skill's `SKILL.md` documents the canonical BIDS-Apps invocation patterns; keep the heuristic / config in version control so the next cohort takes minutes, not days.

## Why this assembly

Rung 2 — Claude Code plus a single skill. Rung 1 (plain Claude Code) fails because the model has only ~partial coverage of the BIDS spec, no live access to the BIDS schema or BEP extensions, and tends to confuse vendor-specific DICOM idioms (Siemens `ep2d_bold` vs GE `epiRT` vs Philips `FFE`). The BIDS skill bundles the 35-entity schema, ReproIn heuristic patterns, the IntendedFor / fieldmap logic, and the BIDS-Apps invocation patterns — exactly the context the model lacks. Rung 3 is overkill: BIDS conversion is a single deterministic transform once the heuristic is right; no extra MCP server, knowledge graph, or autonomous system buys you anything for this problem.

## Availability

Fully open. The [BIDS Claude Skill](../../catalog/tools/bids.html) is community OSS via the K-Dense marketplace. HeuDiConv, dcm2bids, dcm2niix, and the BIDS validator are all open-source (Apache-2.0 / MIT). No subscription tier required. Output datasets are publishable on OpenNeuro under the user's chosen license (typically CC0).

## Compute requirements

Laptop. The LLM-orchestrated steps — survey, heuristic drafting, validator triage — are network- and reasoning-bound. The conversion step itself is `dcm2niix`-bound: roughly 30–90 s per BOLD run on a modern laptop, scaling linearly with the cohort size. A 50-subject cohort with 8 runs each takes 2–6 hours of wall-clock for the conversion; nothing heavier than a USB-3 external SSD is needed for disk throughput. No GPU required.

## Evidence

Proposed. No documented end-to-end LLM-driven DICOM→BIDS workflow has been published in the peer-reviewed or preprint literature within the last 24 months as of this run.

Closest component-level grounding:

- **BIDS specification** — [Gorgolewski et al., *Sci. Data* 3:160044 (2016)](https://doi.org/10.1038/sdata.2016.44); current evolution surveyed in [Poldrack et al., *Imaging Neuroscience* 2:1–19 (2024)](https://doi.org/10.1162/imag_a_00103) covering the validator, the BEP extensions, and the BIDS-Apps ecosystem.
- **PyBIDS** — [Yarkoni et al., *JOSS* 4(40):1294 (2019)](https://doi.org/10.21105/joss.01294) — the canonical Python query library Claude calls in step 8.
- **Conversion tooling** — [Zwiers, Moia, Oostenveld, *Front. Neuroinform.* 15:770608 (2022)](https://doi.org/10.3389/fninf.2021.770608) (BIDScoin); [Wulms et al., *Sci. Data* 10:673 (2023)](https://doi.org/10.1038/s41597-023-02583-4) (BIDSconvertR); both establish that automated heuristic-driven DICOM→BIDS conversion is a tractable, well-bounded transform.

The recipe combines components each of which has independent peer-reviewed validation; the assembly itself is new and would benefit from a field report.

## Alternatives considered

- **Plain Claude Code without the BIDS skill.** Works on a single subject if you spoon-feed series descriptions, but degrades on full cohorts: the model invents non-existent BIDS entities (`acq-orig`, `desc-raw` placements in the wrong directories), misses the fieldmap `IntendedFor` cross-link logic, and silently produces validator-failing layouts. The skill exists precisely because plain prompting underperforms here.
- **BIDScoin GUI (no LLM).** The right choice when you have a small (<10 subjects), one-off dataset and a human in the loop who wants to point-and-click each series mapping. The LLM path wins as soon as the heuristic needs to be reused across cohorts, or when the validator report needs interpretation.
- **HeuDiConv CLI in pure Bash.** Equivalent under the hood — the recipe just delegates the heuristic-drafting and validator-triage steps to Claude, which is where the human time actually goes. Use plain HeuDiConv if your team already maintains a battle-tested heuristic.
- **Rung 4 (autonomous system).** No documented autonomous-science system specializes in BIDS organization. Overkill for what is fundamentally a deterministic transform.

## See also

- [BIDS Claude Skill](../../catalog/tools/bids.html)
- [Discover NWB recordings on DANDI and prepare them for sorting](discover-nwb-recordings-on-dandi.html) — the discovery counterpart for electrophysiology data (NWB) rather than imaging (BIDS).
- [Sort spikes from a Neuropixels recording end-to-end](sort-spikes-from-neuropixels-recording.html) — companion electrophysiology workflow.
- [OpenNeuro MCP](../../catalog/tools/openneuro.html) — submission target archive for validated BIDS datasets.

## Sources

- [`K-Dense-AI/scientific-agent-skills` — BIDS skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/bids/SKILL.md) — verified 2026-06-05 (this run).
- [BIDS specification](https://bids-specification.readthedocs.io/) — verified 2026-06-05 (this run).
- [Gorgolewski et al., *Sci. Data* 3:160044 (2016), doi:10.1038/sdata.2016.44](https://doi.org/10.1038/sdata.2016.44) — published 2016-06-21.
- [Poldrack et al., *Imaging Neuroscience* 2:1–19 (2024), doi:10.1162/imag_a_00103](https://doi.org/10.1162/imag_a_00103) — published 2024-02-29.
- [Yarkoni et al., *JOSS* 4(40):1294 (2019), doi:10.21105/joss.01294](https://doi.org/10.21105/joss.01294) — published 2019-08-19.
- [Zwiers, Moia, Oostenveld, *Front. Neuroinform.* 15:770608 (2022), doi:10.3389/fninf.2021.770608](https://doi.org/10.3389/fninf.2021.770608) — published 2022-01-13.
- [Wulms et al., *Sci. Data* 10:673 (2023), doi:10.1038/s41597-023-02583-4](https://doi.org/10.1038/s41597-023-02583-4) — published 2023-10-03.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=organize-raw-dicom-to-bids-layout&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Forganize-raw-dicom-to-bids-layout.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
