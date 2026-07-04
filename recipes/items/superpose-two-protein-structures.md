---
title: Superpose two protein structures and quantify where they differ
parent: All recipes
grand_parent: Recipes
nav_order: 27
problem_class: Data analysis
subject_areas: [Integrative Structural and Computational Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-04
summary: Superpose a predicted model onto an experimental structure (or apo onto holo) with the PyMOL skill, then report global RMSD, per-residue deviation, and a rendered overlay.
---

# Superpose two protein structures and quantify where they differ

Hand Claude two coordinate files — an AlphaFold model and its experimental counterpart, or an apo and a holo conformation — and get back a global RMSD, a per-residue deviation table that pinpoints the moving regions, and a publication-quality overlay image, all from one skill.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Integrative Structural and Computational Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have two structures of the same (or homologous) protein and need to know how well they agree and *where* they diverge. Typical cases: validating an AlphaFold/Boltz model against a freshly solved experimental structure; comparing an apo structure to a ligand-bound (holo) one to find the residues that move on binding; checking whether two crystal forms captured the same conformation; or measuring drift of a homology model from its template. A single global RMSD number hides the story — the informative signal is *which* loops, hinges, or domains shifted, and by how much. Done by hand this means loading both files into PyMOL, choosing `align` vs `super` vs `cealign` (they differ when sequence identity is low), reading the RMSD off stdout, then eyeballing the overlay. The per-residue breakdown that actually localizes the change rarely gets computed at all.

Solved looks like: point at two coordinate files, get a global RMSD (with the alignment method and atom count stated), a saved per-residue Cα-deviation table that flags the high-deviation segments, and a rendered overlay coloured by deviation — with the whole thing captured as a re-runnable command, not a throwaway session.

## Recommended approach

Rung 2 — one Claude Skill, the [PyMOL skill](../../catalog/tools/pymol.html), which writes and runs headless PyMOL Python scripts locally and reports the RMSD and per-atom metrics. If you don't already hold both files, fetch them first: the [AlphaFold MCP server](../../catalog/tools/alphafold.html) pulls a model by UniProt accession and the [PDB MCP server](../../catalog/tools/pdb.html) pulls experimental coordinates by PDB ID.

1. **Install the skill.** Verbatim steps are on the [catalog page](../../catalog/tools/pymol.html) (clone `google-deepmind/science-skills`, copy `pymol` *and* `scienceskillscommon` into `~/.claude/skills/`, install `uv`). Rendering is headless via OSMesa — no GPU or display server.

2. **Get both coordinate files in hand.** If one is only an accession or PDB ID:

   ```
   Use the alphafold-server MCP to fetch the model for UniProt <ACC>
   as structures/<ACC>_af.cif, and the pdb MCP to fetch <PDBID> as
   structures/<PDBID>.cif. Report each file's chain IDs and residue
   ranges so I know which chains to superpose.
   ```

3. **Author a re-runnable superposition command.** Capture the workflow as a versioned command file rather than an ad-hoc chat. Ask Claude to write `.claude/commands/superpose.md`:

   ```
   Write a project command file .claude/commands/superpose.md that, given
   two structure paths (mobile, target) and optional chain selectors, uses
   the pymol skill to:
     1. Load both structures; select the requested chains (default: first
        polymer chain of each).
     2. Superpose with cealign (robust at low sequence identity); if
        sequence identity >= 40%, also run super and report both RMSDs and
        the aligned-atom counts. State which method's number is quoted.
     3. Write the aligned mobile structure to results/<stem>_aligned.cif.
     4. Compute per-residue Cα deviation after alignment and write
        results/<stem>_perres.csv (columns: resi, resn, chain, ca_dev_A).
     5. Render an overlay PNG (target grey cartoon, mobile coloured by
        per-residue deviation, blue->red 0-5 A) to results/<stem>_overlay.png,
        and save an editable results/<stem>.pse session.
     6. Print global RMSD, aligned-atom count, alignment method, and the
        5 residues with the highest Cα deviation.
   ```

   Then invoke it, e.g. `/project:superpose structures/<ACC>_af.cif structures/<PDBID>.cif`.

4. **Read the divergence off the saved table — not the eyeball.** Have Claude synthesize, citing only rows in the saved CSV:

   ```
   From results/<stem>_perres.csv, summarize where the two structures
   differ. Report the global RMSD and method from the run. List the
   contiguous segments with Cα deviation > 2 A (start-end residues, peak
   deviation, and secondary-structure context if annotated in the cif).
   Distinguish a rigid-body domain shift (a whole block moves together)
   from local loop rearrangement. Do not claim a conformational change
   for any residue not in the table.
   ```

5. **Record provenance.** The saved CSV, aligned CIF, PNG, and `.pse` are the audit trail. Have Claude write `results/<stem>_provenance.json`: the PyMOL build/version string, the alignment method and cutoff used, both input files' sha256, the chain selectors, aligned-atom count, global RMSD, and the model/agent identity. If either input came from a live service, record the AlphaFold DB / PDB fetch date and accession so a rerun's divergence is visible. See the [reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide.

The durable artifact is the committed `.claude/commands/superpose.md`, the `uv`-pinned skill environment, and the saved `results/*` (aligned CIF, per-residue CSV, overlay PNG, `.pse`, provenance JSON) per comparison.

## Why this assembly

Rung 2, and it stops here. Superposition-plus-deviation is a single load-align-measure step; one skill wraps script generation, headless execution, and the RMSD/per-atom readout. Rung 1 (plain Claude Code) can't do it — Claude has no PyMOL binary and can't run `cealign` or emit an OSMesa render. A rung-3 toolbelt buys nothing for a pairwise comparison; the only legitimate extra components are the optional structure-*fetch* MCPs, skipped when you already hold both files. No autonomous system is warranted for a deterministic geometric operation.

## Availability

Fully open. The PyMOL skill is Apache-2.0 (code) / CC-BY-4.0 (docs) and runs the open-source PyMOL build headlessly via OSMesa; PyMOL itself is licensed separately (Schrödinger maintains open-source and commercial builds) — review the [PyMOL license](https://www.pymol.org/) before use. The optional AlphaFold and PDB MCP servers call public EBI/RCSB APIs with no key. Local `uv` and Python are the only environment dependencies.

## Compute requirements

Laptop. Each comparison is two coordinate files loaded locally; `cealign`/`super` on typical single-domain proteins completes in seconds, and the headless OSMesa render adds a few more. Outputs are small (a CIF, a CSV, a PNG, a `.pse`). No GPU, no display server, no database download. Very large complexes (tens of thousands of residues) are RAM-bound rather than compute-bound; 8 GB is ample for ordinary proteins.

## Evidence

`Proposed`. No documented end-to-end LLM-driven structure-superposition workflow is known in the peer-reviewed or preprint literature as of this run (a search for LLM-agent PyMOL RMSD workflows returned no matching assembly).

Closest component-level grounding:

- **PyMOL** is the field-standard molecular graphics system; its `align`, `super`, and `cealign` superposition commands are the canonical tools for structure overlay and RMSD ([DeLano, *The PyMOL Molecular Graphics System*](https://www.pymol.org/); `cealign` implements the CE combinatorial-extension algorithm of [Shindyalov & Bourne, *Protein Eng.* 1998](https://doi.org/10.1093/protein/11.9.739), which aligns robustly at low sequence identity where `align` fails).
- **Model-vs-experiment RMSD** is the standard AlphaFold validation readout — the AlphaFold paper reports median backbone accuracy against experimental structures ([Jumper et al., *Nature* 2021](https://doi.org/10.1038/s41586-021-03819-2)), so quantifying agreement between a predicted model and its solved counterpart is an established, well-bounded task.

The recipe combines components with independent peer-reviewed validation; the Claude-driven assembly is rational and runnable but not separately benchmarked. A field report would move it to `Reported`.

## Alternatives considered

- **[Infer the function of an uncharacterized protein from its 3D structure](infer-protein-function-from-structure.html).** Different question: that searches a *database* for structural neighbours (Foldseek); this compares *two specific* structures you already have. Use Foldseek to find what a structure resembles; use this to measure how two known structures differ.
- **[Triage an AlphaFold model for structure-based drug design](triage-alphafold-model-for-docking.html).** The confidence-side sibling — it reads pLDDT to decide whether a model is *fit* for docking. Run that when you have no experimental structure to compare against; run this when you do and want the actual geometric agreement.
- **TM-align / FATCAT / DALI CLI (no LLM).** The right choice for high-throughput all-vs-all comparison of many structures, or when you need a length-normalized TM-score rather than RMSD. This single-skill recipe wins for the common pairwise "how do these two differ, and where" question because it bundles the render and the per-residue table.
- **Rung 3+ (toolbelt or autonomous system).** Overkill. Pairwise superposition is deterministic geometry; nothing beyond the optional fetch MCPs is needed.

## See also

- [PyMOL (Claude Skill)](../../catalog/tools/pymol.html)
- [AlphaFold MCP Server](../../catalog/tools/alphafold.html) — fetch a predicted model by UniProt accession.
- [PDB MCP Server](../../catalog/tools/pdb.html) — fetch experimental coordinates by PDB ID.
- [Infer the function of an uncharacterized protein from its 3D structure](infer-protein-function-from-structure.html) — database-search counterpart.
- [Triage an AlphaFold model for structure-based drug design](triage-alphafold-model-for-docking.html) — confidence-side counterpart.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md)

## Sources

- [`google-deepmind/science-skills` — `pymol/SKILL.md`](https://github.com/google-deepmind/science-skills/blob/main/skills/pymol/SKILL.md) — alignment/superposition + RMSD capability, headless OSMesa render, `.pse`/PNG outputs; verified 2026-07-04 (this run).
- [PyMOL](https://www.pymol.org/) — molecular graphics system and license; verified 2026-07-04 (this run).
- [Shindyalov & Bourne, "Protein structure alignment by incremental combinatorial extension (CE)," *Protein Eng.* 11:739 (1998), doi:10.1093/protein/11.9.739](https://doi.org/10.1093/protein/11.9.739) — the `cealign` algorithm.
- [Jumper et al., "Highly accurate protein structure prediction with AlphaFold," *Nature* 596:583 (2021), doi:10.1038/s41586-021-03819-2](https://doi.org/10.1038/s41586-021-03819-2) — published 2021-07-15.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=superpose-two-protein-structures&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fsuperpose-two-protein-structures.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
