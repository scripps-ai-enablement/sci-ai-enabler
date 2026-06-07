---
title: Parse FCS flow-cytometry files for downstream immunophenotyping
parent: All recipes
grand_parent: Recipes
nav_order: 18
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-02
summary: Use the FlowIO Claude skill to parse FCS 2.0/3.0/3.1 files into tidy DataFrames with channel categorisation and batch metadata extraction, ready for downstream immunophenotyping or QC.
---

# Parse FCS flow-cytometry files for downstream immunophenotyping

Drop a directory of Flow Cytometry Standard `.fcs` files in front of Claude Code and get back a single tidy events DataFrame, a per-file channel/metadata table, and any transformed (log / time-scaled / gain-corrected) versions you need, without writing the FCS-parsing boilerplate by hand.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Every immunophenotyping or cytometry analysis starts the same way: parse the vendor-emitted `.fcs` files into something tidy, harvest the metadata (panel, voltage, acquisition date, operator, sample ID), categorise channels into scatter / fluorescence / time / mass, and emit a uniform DataFrame downstream tooling can consume. FCS 2.0, 3.0, and 3.1 have nontrivial header differences; instruments emit divergent keyword conventions; batch-extracting metadata across hundreds of files for a multi-day panel-validation experiment is brittle if hand-coded. The mechanics are well understood (the BSD-3 `flowio` library is the canonical Python parser), but rebuilding the parsing loop, channel categorisation, and metadata harvest each time is friction. "Solved" looks like: hand the agent a directory of FCS files, name the channels you care about, get back a tidy events table, a per-file metadata table, and a list of any files that failed to parse with the reason.

## Recommended approach

1. **Install the [FlowIO (Claude Skill)](../../catalog/tools/flowio.html).** From the K-Dense `scientific-agent-skills` repo:

   ```
   git clone https://github.com/K-Dense-AI/scientific-agent-skills
   cp -r scientific-agent-skills/scientific-skills/flowio ~/.claude/skills/
   uv pip install flowio   # Python 3.9+
   ```

   Confirm the skill is discoverable with `/plugin list` (or list `~/.claude/skills/`). The skill wraps the BSD-3 `flowio` library and exposes `FlowData` (the FCS 2.0/3.0/3.1 reader), `create_fcs()`, `read_multiple_data_sets()`, scatter/fluorescence/time channel categorisation, and CSV/DataFrame export.

2. **Place the inputs alongside your project.** Either a single `.fcs` file or a directory of them (e.g., `data/exp42/`). The skill handles vendor exports from BD, Beckman, Sony, Cytek, ThermoFisher, etc., as long as the file conforms to FCS 2.0 / 3.0 / 3.1.

3. **Invoke the skill in chat with the directory and panel context.** A minimal prompt:

   ```
   Run the flowio skill on data/exp42/*.fcs.

   For each file:
     1. Parse with FlowData; emit a per-file metadata row
        (filename, $TOT events, $CYT, $DATE, $BTIM, panel keywords,
        any errors). Write to out/exp42-metadata.tsv.
     2. Categorise channels into {scatter, fluorescence, time}; write
        the per-file channel map to out/exp42-channels.tsv.
     3. Apply a log10 transform to fluorescence channels and a
        gain-corrected linear scale to scatter channels.
     4. Concatenate the per-file events into a single long DataFrame
        with a `sample_id` column; write to out/exp42-events.parquet.
     5. List any files that failed to parse, with the FlowIO error.
   ```

4. **Sanity-check the per-file metadata table** before proceeding. The most common failure modes are panel drift (a fluorochrome listed under a different keyword across days), event-count outliers (a sample that aborted partway through acquisition), and instrument-keyword inconsistency between machines. If you spot a problem file, re-acquire or exclude before passing the events DataFrame downstream.

5. **Hand off to downstream tooling.** The tidy events Parquet drops straight into FlowKit (compensation / GatingML), CytoNorm (batch normalisation), or a scverse-style analysis if you convert events to AnnData. The metadata TSV is the input you feed to your batch-design / panel-validation report. **FlowIO is intentionally I/O-only** — it does not gate, does not compensate, and does not do clustering; pair with FlowKit for those steps (FlowKit is not yet a Claude skill, per the FlowIO catalog page).

## Why this assembly

Rung 2 of the simplicity ladder. Plain Claude Code can write `flowio` parsing code from scratch, but the FCS keyword space is messy enough that small slips (mis-categorising a time channel as fluorescence, missing a vendor-specific `$PnN` convention, failing to surface a partial-acquisition file) silently corrupt downstream analysis. The skill encodes the parse / categorise / metadata-harvest sequence as a single discoverable action and surfaces failures explicitly, which is the right grain for a one-shot pre-processing step before gating and clustering. No need for a multi-tool harness or an autonomous-science system — FCS parsing is a well-defined I/O problem.

## Availability

Fully open. The `flowio` library is BSD-3-Clause; the K-Dense skill wrapper is published in the same repository under its open-source licence. The skill makes no external API calls — all parsing runs locally. No subscription, institutional account, or API key required. FCS is an open file format defined by the International Society for Advancement of Cytometry.

## Compute requirements

Laptop-sufficient. A 100-file experiment with ~10⁵ events per file parses, categorises, and concatenates in seconds to a minute on a modern laptop with 16 GB RAM; the concatenated long DataFrame for that scale fits comfortably in memory. Large panels (>10⁶ events per file across hundreds of samples) push toward streaming the events to Parquet partitioned by `sample_id` rather than holding them all in memory. The skill itself does not require a GPU.

## Evidence

Proposed. No documented end-to-end attempt of "Claude Code + the FlowIO skill on a real FCS directory" with quantitative pass/fail is known to the curator at this time. The closest evidence is component-level and class-level:

- **`flowio` itself** is the BSD-3 canonical Python FCS parser maintained by the FlowKit author; it underpins FlowKit's gating stack and a long list of downstream analysis tools, with the FCS 2.0/3.0/3.1 readers exercised in the FlowKit test suite.
- **Class-level LLM evidence** comes from ["Enhancing Clinical Workflow Efficiency in Flow Cytometry Reporting with LLMs" (PMC13053331, *Journal of Clinical Immunology* 2026)](https://pubmed.ncbi.nlm.nih.gov/?term=PMC13053331) — a fine-tuned LLM achieves pathologist-level accuracy generating interpretive immunophenotyping reports from cytometry data. That paper exercises the *downstream* report-generation stage that this recipe's parsed-events output feeds into; it does not demonstrate FCS parsing by an agent.
- **No head-to-head benchmark** of "FlowIO skill" versus hand-written `flowio` code is published; the agent loop here is convenience and explicit failure surfacing, not a new analytical method.

## Alternatives considered

- **Plain Claude Code, no skill.** Works — Claude can write the `flowio` parsing loop from scratch. Reach for this when teaching how the parser composes, or when you need a one-off custom keyword harvest the skill does not expose. Reach for the skill when you want a documented prompt template, channel categorisation, and explicit failure surfacing across hundreds of files.
- **FlowKit / FlowJo / FACSDiva directly.** FlowKit (Python) or the vendor desktop apps are the canonical gating/compensation stacks. Reach for them when gating *is* the job — not when you just need a tidy events DataFrame upstream of your own clustering / dimensionality-reduction / batch-correction code. The FlowIO skill is intentionally narrower: parse and emit, nothing more.
- **Biomni (autonomous-science system).** [Biomni](../../autonomous-science/systems/biomni.html) bundles a much wider biomedical environment; reach for it when FCS parsing is one node of a multi-stage pipeline (e.g., panel → clustering → cross-modal integration with transcriptomics). For a focused FCS-parse step, the dedicated skill is the right grain.

## See also

- [FlowIO (Claude Skill)](../../catalog/tools/flowio.html)
- [Biomni](../../autonomous-science/systems/biomni.html)
- [Run first-pass QC on a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — analogous one-skill pre-processing recipe on a different single-cell modality.

## Sources

- [`scientific-skills/flowio/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/flowio/SKILL.md) — skill manifest; verified 2026-06-02 (this run).
- [`flowio` library](https://github.com/whitews/flowio) — canonical FCS parser; verified 2026-06-02 (this run).
- ["Enhancing Clinical Workflow Efficiency in Flow Cytometry Reporting with LLMs" (PMC13053331, *Journal of Clinical Immunology* 2026)](https://pubmed.ncbi.nlm.nih.gov/?term=PMC13053331) — class-level LLM evidence on downstream cytometry report generation; verified 2026-06-02 (this run).
- [International Society for Advancement of Cytometry: FCS 3.1 specification](https://isac-net.org/page/Data-Standards) — canonical file-format definition; verified 2026-06-02 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=parse-fcs-flow-cytometry-files&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fparse-fcs-flow-cytometry-files.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
