---
title: Assemble a public cancer imaging cohort from NCI Imaging Data Commons
parent: All recipes
grand_parent: Recipes
nav_order: 2
problem_class: Knowledge synthesis
subject_areas: [Translational Medicine]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-05
summary: Use the Imaging Data Commons skill to query NCI IDC by modality, body part, and collection, then download a reproducible DICOM cohort ready for segmentation.
---

# Assemble a public cancer imaging cohort from NCI Imaging Data Commons

Describe the scans you need ("head-and-neck CT with RTSTRUCT contours from at least 100 patients"); get back a filtered manifest of IDC series, the licenses that govern them, and the `idc-index` download commands that pull a reproducible DICOM cohort onto disk.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Building an imaging-AI model or a radiomics study starts with a cohort, and the public option — NCI Imaging Data Commons — holds ~100 TB of cancer imaging across dozens of collections. But the access path is unfriendly: collection READMEs vary, series-level metadata (modality, body part, manufacturer, whether an RTSTRUCT or SEG object accompanies the scan) lives in DICOM tags you cannot see from the portal, and each collection carries its own license (mostly CC-BY, some CC-NC) you must respect before training on it. Scientists routinely download a whole collection, discover half of it is the wrong modality or lacks segmentations, and start over. Solved looks like: state your inclusion criteria, get a filtered series-level manifest with license flags, and a download plan you can commit and re-run so the exact cohort is reconstructable months later.

## Recommended approach

1. **Install the [Imaging Data Commons skill](../../catalog/tools/imaging-data-commons.html)** so Claude Code can drive `idc-index` (the official IDC Python client, backed by a local DuckDB metadata index):

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   ```

   Enable the `imaging-data-commons` skill when prompted; on first use it installs `idc-index` (requires Python ≥ 3.10). No cloud credentials are needed for public data.

2. **State your cohort criteria and let the skill query the metadata index.** A first prompt:

   ```
   Use the imaging-data-commons skill to query IDC for CT series of
   the head and neck region. I want, per patient: at least one CT
   series AND an accompanying RTSTRUCT. Return a table grouped by
   collection with patient count, series count, modality mix, and
   the license of each collection. Pin the idc-index version you used.
   ```

   `idc-index` runs SQL over its local DuckDB index — this is a metadata query, not a bulk download.

3. **Refine to a filtered series manifest.** Add the specific inclusion/exclusion logic and have Claude emit the artifact — a stable manifest, not a chat answer:

   ```
   Restrict to collections licensed CC-BY (drop CC-NC). Keep only
   patients with both a CT and an RTSTRUCT. Write the result to
   cohort_manifest.csv with columns: collection_id, PatientID,
   StudyInstanceUID, SeriesInstanceUID, Modality, license,
   series_size_MB. Also write build_cohort.py that reproduces this
   query from idc-index so the manifest can be regenerated.
   ```

4. **Record provenance.** IDC is versioned by release; capture it so the cohort is reconstructable:

   ```
   Emit provenance.json capturing: idc-index version, the IDC data
   release version (idc_index.IDCClient().get_idc_version() or
   equivalent), the query date, the sha256 of cohort_manifest.csv,
   total patient/series counts, and the model id running this session.
   ```

5. **Generate the download plan and pull the cohort.** Two options — a per-series download or a manifest download:

   ```
   From cohort_manifest.csv, emit idc-index download commands that
   pull each SeriesInstanceUID into data/idc/<collection>/<PatientID>/.
   Prefer a single manifest-based download call over one call per
   series. Report expected total size before downloading.
   ```

   Commit `build_cohort.py`, `cohort_manifest.csv`, `provenance.json`, and a pinned `requirements.txt` (pin `idc-index`). The download itself is the only non-versioned step — the manifest + release version make it reproducible. See the [reproducibility guide](../../guide/advanced/reproducibility.md) for the artifact pattern.

6. **Hand off to segmentation.** IDC ships DICOM; convert to NIfTI (`dcm2niix`, or the [DICOM-to-BIDS recipe](organize-raw-dicom-to-bids-layout.html)) and feed the cohort into the [Segment an organ or tumor recipe](segment-organ-or-tumor-in-medical-image.html). Existing RTSTRUCT/SEG objects become your training labels.

## Why this assembly

Rung 2 — one cataloged skill. `idc-index` handles the query and the download in one client; the skill gives Claude Code the current idioms so it doesn't hallucinate the API. Rung 1 (plain Claude Code) fails because the model has no live IDC index and will invent collection names and series UIDs. Rung 3+ is unnecessary: cohort discovery + download is a bounded retrieval task the dedicated client covers cleanly. The downstream modeling (segmentation, radiomics) is a separate recipe, not part of this one.

## Availability

Fully open. `idc-index` queries and downloads public IDC data with no authentication or cloud credentials. The skill is MIT-licensed (K-Dense collection). **Caveat that matters:** individual IDC collections carry their own data licenses — mostly CC-BY, some CC-NC. Step 3 filters on the `license` field precisely because a CC-NC collection cannot be used in a commercial pipeline. Always confirm the per-collection license before downstream use.

## Compute requirements

Laptop for discovery. The metadata query is a local DuckDB scan (seconds), and the index download is a one-time few-hundred-MB fetch. The image download is bandwidth- and disk-bound, not compute-bound: a 100-patient CT cohort is typically tens of GB — budget disk and time accordingly, and check the reported total size (step 5) before pulling. Downstream segmentation inherits the GPU-workstation requirement from that recipe.

## Evidence

Reported. IDC and its access tooling are documented in [Fedorov et al., *RadioGraphics* 43(12):e230180 (2023)](https://doi.org/10.1148/rg.230180), which describes IDC's design for transparent, reproducible imaging-AI cohorts, and the original [Fedorov et al., *Cancer Research* 81(16):4188 (2021)](https://doi.org/10.1158/0008-5472.CAN-21-0950). `idc-index` is the project's official Python client for the exact query-and-download workflow this recipe automates. No peer-reviewed benchmark of the *Claude-skill + idc-index* assembly specifically is published; the recipe inherits the tooling's documented capability. The downstream half inherits the `Reported` evidence on the [segmentation recipe](segment-organ-or-tumor-in-medical-image.html).

## Alternatives considered

- **The [IDC web portal](https://portal.imaging.datacommons.cancer.gov/) by hand.** Best for one-off browsing of a known collection; it does not scale to structured series-level filtering across collections, and it leaves no re-runnable artifact.
- **BigQuery against the IDC public dataset.** Maximum query flexibility if you already have a GCP project and know the IDC schema. Overkill for most cohort-assembly tasks and adds a cloud dependency `idc-index` avoids.
- **Direct `s3`/`gsutil` bucket copies.** Fast for pulling a whole known collection, but skips the metadata filtering that keeps you from downloading the wrong modality and gives you no license-aware manifest.
- **Escalating to an autonomous system.** Not warranted — there is no hypothesis generation or multi-tool reasoning here, just filtered retrieval.

## See also

- [Imaging Data Commons (Claude Skill)](../../catalog/tools/imaging-data-commons.html)
- [Segment an organ or tumor in a medical image with nnU-Net](segment-organ-or-tumor-in-medical-image.html) — the natural downstream recipe.
- [Organize raw DICOM into a BIDS layout](organize-raw-dicom-to-bids-layout.html) — DICOM-to-NIfTI conversion before modeling.
- [Discover NWB recordings on DANDI](discover-nwb-recordings-on-dandi.html) — the neurophysiology-data counterpart to this discovery pattern.

## Sources

- [Fedorov et al. *RadioGraphics* 43(12):e230180 (2023), doi:10.1148/rg.230180](https://doi.org/10.1148/rg.230180) — published 2023-11-16; verified 2026-07-05 (this run).
- [Fedorov et al. *Cancer Research* 81(16):4188 (2021), doi:10.1158/0008-5472.CAN-21-0950](https://doi.org/10.1158/0008-5472.CAN-21-0950) — published 2021-08-15.
- [`ImagingDataCommons/idc-index`](https://github.com/ImagingDataCommons/idc-index) — verified 2026-07-05 (this run).
- [NCI Imaging Data Commons portal](https://portal.imaging.datacommons.cancer.gov/) — verified 2026-07-05 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=assemble-cancer-imaging-cohort-from-idc&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fassemble-cancer-imaging-cohort-from-idc.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
