---
title: neuro-mcp
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: AImplifier
availability: Alpha
tool_categories: [Neuroscience, Translational Medicine]
last_verified: 2026-08-16
verification: works
verified_on: 2026-08-17
reviewed_on: 2026-08-17
security: caution
security_on: 2026-08-17
security_note: "AImplifier org confirmed not archived, BSD-3-Clause via GitHub license API, provenance matches; Alpha 0-star single-org project persisting subject and EHR records locally with no independent evaluation"
summary: 54-tool MCP server wrapping MNE-Python EEG/MEG preprocessing, source imaging, a BIDS/EHR record store, and offline interactive plots.
---

# neuro-mcp

MCP server that gives Claude an end-to-end EEG/MEG workflow — MNE-Python preprocessing, ICA, ERP and time-frequency analysis, source imaging, plus a BIDS-backed subject/EHR record store with an audit log.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [AImplifier](https://github.com/AImplifier/neuro-mcp) |
| **Availability** | Alpha (PyPI 0.1.3, released 2026-07-24; MCP Registry `io.github.AImplifier/neuro-mcp`) |
| **Pricing** | Free / OSS — BSD-3-Clause |
| **Capabilities** | Read/Write — reads recordings, writes derived files, subject records, annotations, and EHR entries to a local database |
| **Verified** | works · 2026-08-17 |
| **Security** | caution · 2026-08-17 — BSD-3-Clause and provenance confirmed; Alpha/single-org project writing local subject and EHR records |

## How to install

Requires Python 3.10+. A dedicated environment is recommended because MNE pulls a large scientific stack.

1. **Create an environment and install** (the upstream README uses conda):
   ```
   conda create -n neuro-mcp python=3.11 -y
   conda activate neuro-mcp
   pip install neuro-mcp
   ```
   Optional extras — Postgres backend and 3-D source visualization:
   ```
   pip install "neuro-mcp[postgres]"
   pip install "neuro-mcp[viz3d]"
   ```
   (`python -m venv` + `pip install neuro-mcp` also works; conda is not required.)

2. **Verify it starts** (one-shot; Ctrl-C once it boots — Claude launches the process itself over stdio):
   ```
   python -m neuro_mcp
   ```

3. **Claude Code** — direct MCP add (stdio). Use the interpreter *inside* the environment created in step 1, not a bare `python`:
   ```
   claude mcp add --transport stdio neuro-analysis -- /path/to/envs/neuro-mcp/bin/python -m neuro_mcp
   ```
   (replace `/path/to/envs/neuro-mcp/bin/python` with the absolute path printed by `which python` while the environment is active — e.g. `/Users/you/miniconda3/envs/neuro-mcp/bin/python`.)

4. **Claude Desktop** — add to `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "neuro-analysis": {
         "command": "/path/to/envs/neuro-mcp/bin/python",
         "args": ["-m", "neuro_mcp"],
         "env": {
           "DATABASE_URL": "sqlite:////data/neuro_mcp.db",
           "BIDS_ROOT": "/data/bids"
         }
       }
     }
   }
   ```
   (same substitution for the interpreter path; adjust `DATABASE_URL` and `BIDS_ROOT` to writable locations on your machine.)

## What it does

54 tools across three layers:

- **Signal processing (MNE-Python)** — `load_neuro`, `filter_neuro`, `resample_neuro`, `set_montage`, `set_reference`, `detect_bad_channels`, `run_ica`, `apply_ica`, `find_events`, `epoch_neuro`, `compute_psd`, `compute_erp`, `time_frequency`, and a family of `plot_*` tools.
- **Source imaging (ESI)** — template-head fetching through to `extract_label_timecourses`, i.e. forward model → inverse solution → parcellated label time courses.
- **Data and record store** — subjects (`register_subject`, `get_subject`), versioned EHR entries (`add_ehr_record`, `amend_ehr_record`, `void_ehr_record`, `get_ehr_history`), datasets and recordings (`import_recording`, `register_dataset`, `query_datasets`, `list_recordings`), annotations (`add_annotation`, `update_annotation`, `void_annotation`, `list_annotations`), and `get_audit_log`.
- **NeuroII visualization** — `neuroii_push_recording`, `neuroii_create_viz_session`, `neuroii_pull_annotations`, plus `visualize_timeseries`, `visualize_averaging`, `visualize_esi`. Views are exported as self-contained interactive Plotly HTML files that work offline; the hosted NeuroII service is optional and configured via `NEUROII_API_URL` / `NEUROII_API_TOKEN`.

Environment variables: `DATABASE_URL` (default `sqlite:///~/.neuro-mcp/neuro_mcp.db`), `BIDS_ROOT` (default `~/.neuro-mcp/bids`), `NEURO_MCP_HOME`, `NEUROII_API_URL`, `NEUROII_API_TOKEN`.

**Primary use cases**: conversational EEG/MEG preprocessing and ERP analysis, EEG source localization, keeping subject records and annotations alongside BIDS recordings.

## Notes

- **Not a cleared clinical device.** The project describes itself as assisting clinicians and researchers, but publishes no regulatory clearance and no medical disclaimer. Treat every output as research-grade; do not use it for diagnosis or care decisions.
- **It writes.** Unlike most catalogued neuroscience servers this one persists state — subject records, EHR entries, annotations, imported recordings. Point `DATABASE_URL` and `BIDS_ROOT` at scratch locations before letting an agent loose on real data, and note that the EHR tools amend/void rather than delete (there is a `get_audit_log`).
- **Defaults need no infrastructure**: SQLite plus a scratch BIDS directory runs with zero setup; `DATABASE_URL` pointed at Postgres is the multi-user path.
- **3-D source rendering needs the `viz3d` extra**; without it the ESI tools still compute but the 3-D views are unavailable.
- **Very early and unproven**: 0 GitHub stars, version 0.1.3, single organization. There is no publication and no independent evaluation. Verify any preprocessing result against a hand-run MNE pipeline before relying on it.
- Complements rather than replaces [MNE-Python (EEG) (Claude Skill)](mne-eeg-tool.html) — the skill teaches Claude to *write* MNE code, this server exposes MNE operations as callable tools. Related: [EEG (Claude Skill)](eeg-skill.html), [MEG (Claude Skill)](meg-skill.html), [BIDS](bids.html), [NeuroKit2](neurokit2.html).

## Sources

- [`AImplifier/neuro-mcp`](https://github.com/AImplifier/neuro-mcp)
- [`neuro-mcp` on PyPI](https://pypi.org/project/neuro-mcp/)
- [MCP Registry](https://registry.modelcontextprotocol.io/)
- [MNE-Python](https://mne.tools/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=neuro-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fneuro-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
