---
title: Triage an AlphaFold model for structure-based drug design
parent: All recipes
grand_parent: Recipes
nav_order: 15
problem_class: Knowledge synthesis
subject_areas: [Integrative Structural and Computational Biology, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-27
summary: Pull a UniProt AlphaFold prediction, surface pLDDT regions and pocket-residue confidence, and produce a go/no-go verdict on whether the model is fit for downstream docking or modelling — all from one MCP server.
---

# Triage an AlphaFold model for structure-based drug design

Hand Claude Code a UniProt accession; get back the AlphaFold predicted structure, a pLDDT map, the confidence verdict on the binding pocket (or any user-named region), and a one-line recommendation on whether the model is safe to use as a docking template — or whether to fall back to an experimental PDB structure or to refine first.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Integrative Structural and Computational Biology, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

AlphaFold has solved "do I have a structure" for ~200 million proteins. It has not solved "is this structure fit for my modelling question." Docking against a high-pLDDT loop is fine; docking into a pocket that AlphaFold modelled at pLDDT 55 is wishful thinking. The standard pre-flight checks — global pLDDT mean and distribution, per-residue confidence over the binding pocket, presence of disordered tails, comparison to any available experimental PDB structure — are quick to run individually but tedious to assemble for every new target. A computational chemist preparing a virtual screen, an antibody engineer picking a docking input, or a structural biologist scoping a refinement project all need the same pre-flight in 30 seconds, not 30 minutes of clicks across the EBI portal, RCSB, and PyMOL.

Solved looks like: one prompt with a UniProt accession (and optionally a pocket-residue list); one structured triage card out — global pLDDT stats, region-level pLDDT, low-confidence stretches flagged, the closest experimental PDB entry named, and a go / refine / fall-back-to-PDB verdict.

## Recommended approach

This recipe is rung 2 — one MCP server, the [AlphaFold MCP Server](../../catalog/tools/alphafold.html), wraps the ~25 EBI AlphaFold API endpoints Claude needs. The PDB cross-check is optional and uses the companion [PDB MCP Server](../../catalog/tools/pdb.html) when available.

1. **Install the AlphaFold MCP server.** Verbatim install commands live on the [catalog page](../../catalog/tools/alphafold.html); the short version is a `git clone`, `npm install && npm run build`, then `claude mcp add --transport stdio alphafold-server -- node /path/to/build/index.js`. The server uses the public EBI API — no auth, no quota.

2. **Pull the structure and confidence summary.** A minimal prompt:

   ```
   Target: UniProt P38398 (BRCA1).

   Using the alphafold-server MCP:
     1. get_structure for P38398; capture length, model
        identifier, and modelling date.
     2. get_confidence_scores for P38398. Print:
          mean pLDDT, median pLDDT, % residues >90, % 70–90,
          % 50–70, % <50.
     3. analyze_confidence_regions to enumerate contiguous
        stretches of residues with pLDDT < 70, with start
        and end residue numbers.

   Emit a markdown table of the regions and a one-paragraph
   global verdict ("model X% high-confidence; N disordered
   stretches comprising Y residues").
   ```

3. **Score the pocket (or any region of interest).** If the user has a pocket residue list — from a homologous PDB structure, a paper, or a pocket-prediction tool — score it explicitly:

   ```
   Pocket residues for BRCA1 BRCT domain (paste-or-derive):
     1646, 1648, 1655, 1660, 1701, 1704, 1731, 1736, 1760.

   For each pocket residue, report its pLDDT from the
   get_confidence_scores payload. Compute pocket-pLDDT
   mean and minimum. Apply the rule of thumb:
     - pocket mean ≥ 85 and min ≥ 70  →  docking-ready
     - pocket mean 70–85, min 50–70   →  usable with caveats; flag
       low-confidence side chains for refinement
     - pocket mean < 70 or min < 50   →  not docking-ready;
       fall back to experimental PDB or co-folding model
   Print the verdict.
   ```

4. **(Optional) Cross-check with experimental PDB structures.** If you have the [PDB MCP server](../../catalog/tools/pdb.html) registered, add:

   ```
   Using pdb-server, run search_by_uniprot for P38398.
   Return the top 5 PDB entries by resolution. For each:
     PDB ID, resolution (Å), chain coverage of the AlphaFold
     residue range, deposit year, ligand-bound or apo.
   If any PDB entry covers the pocket residues above at
   resolution ≤ 2.5 Å, recommend it over the AlphaFold model
   as the primary docking template.
   ```

5. **Export for a downstream tool.** AlphaFold MCP can prepare PyMOL or ChimeraX export commands directly:

   ```
   Use export_for_pymol on P38398 to produce a PyMOL session
   script that colours the cartoon by pLDDT (blue >90,
   cyan 70–90, yellow 50–70, orange <50) and zooms on the
   pocket residue list. Save the script as
   structures/P38398_triage.pml.
   ```

   Swap `export_for_pymol` for `export_for_chimerax` if that's the visualization stack of choice.

6. **Persist the triage card.** Ask Claude Code to write `structures/<UniProt>_triage_<date>.md` with the global stats, low-pLDDT region table, pocket verdict, PDB alternatives, and the PyMOL/ChimeraX script path.

## Why this assembly

Rung 2 of the simplicity ladder. The [AlphaFold MCP Server](../../catalog/tools/alphafold.html) wraps every API call this triage needs — structure retrieval, pLDDT scoring, region analysis, visualization export — behind a single MCP. Rung 1 (plain Claude Code) would hit the same EBI endpoints with raw HTTP but loses the typed tool surface and the built-in pLDDT region analysis. Rung 3 (an extra toolbelt) is only justified when the optional PDB cross-check is in scope; that's one extra tool and remains a thin escalation, not a harness. No rung-4 autonomous-science system is required — the workflow is shallow, the output is a card, and per-claim provenance to AlphaFold/PDB accessions is the value.

## Availability

Fully open. The AlphaFold MCP server is MIT-licensed; EBI's AlphaFold Protein Structure Database is free for academic use (commercial users should consult the [EBI terms](https://alphafold.ebi.ac.uk/faq)). The PDB MCP server uses the public RCSB REST API. No subscription required. Local Node and npm are the only environment dependencies.

## Compute requirements

Laptop. A single triage card returns in under 30 seconds: structure retrieval is a few hundred kilobytes; pLDDT analysis is in-process; PyMOL/ChimeraX export is a text script. Running PyMOL or ChimeraX to render the session — if you do — adds whatever those clients cost on your machine.

## Evidence

`Proposed`. No documented end-to-end LLM-orchestrated triage workflow using the AlphaFold MCP server in peer-reviewed literature is known as of 2026-05-27. The component pieces are well-validated:

- **AlphaFold MCP Server** — the server's pLDDT-analysis tools wrap the same EBI API that underpins the published AlphaFold Protein Structure Database (Varadi et al., [*Nucleic Acids Res.* 2022, 50:D439](https://doi.org/10.1093/nar/gkab1061); 2024 update [50:D368](https://doi.org/10.1093/nar/gkad1011)).
- **pLDDT-thresholding rules of thumb** — the docking-readiness cutoffs above follow the practical benchmarks established for AlphaFold-Multimer and protein-protein docking (Bryant et al., [*Nature Communications* 2022, 13:1265](https://doi.org/10.1038/s41467-022-28865-w); follow-up assessments through 2024–2025 reaffirm interface-pLDDT ≥85 as the strong-confidence regime, 70–85 as the caveat regime).
- **AlphaFold for small-molecule docking** — community benchmarks repeatedly find that high global pLDDT does *not* guarantee virtual-screen success; pocket-residue pLDDT and side-chain rotamer fidelity matter more (Karelina et al., [*J. Chem. Inf. Model.* 2023, 63:6219](https://doi.org/10.1021/acs.jcim.3c00601), and 2024–2025 follow-ups). The recipe encodes that distinction in step 3.
- **AlphaFold MCP usage** — referenced in several MCP-server directories and a Skywork.ai walkthrough; not yet cited in peer-reviewed work.

A peer-reviewed benchmark of "Claude + AlphaFold MCP triage" vs a hand-built notebook is the missing link. The component-level evidence behind every claim — the API, the pLDDT cutoffs, the rule-of-thumb thresholds — is well-established.

## Alternatives considered

- **Rung 1 — plain Claude Code + EBI HTTP.** Possible but throws away the typed MCP tool surface and the analyze_confidence_regions tool. Pick this only if your environment forbids MCP servers.
- **Local AlphaFold inference.** Running AlphaFold 2/3 locally to predict a new structure is the right escalation when EBI's pre-computed entry is for the wrong species, isoform, or splice variant. That requires GPU compute and is outside this recipe's scope.
- **Co-folding (AlphaFold-Multimer, Boltz-2, RoseTTAFold All-Atom).** Better than monomer AlphaFold for ligand-bound or complex states. Not yet wrapped as a Claude-installable component in [`catalog/tools/`](../../catalog/); see Missing components in the curator state.
- **Skip AlphaFold, use the PDB structure directly.** When a high-resolution apo or holo structure covering the pocket exists, prefer it. Step 4 of the recipe is exactly that check.

## See also

- [AlphaFold MCP Server](../../catalog/tools/alphafold.html)
- [PDB MCP Server](../../catalog/tools/pdb.html)
- [UniProt MCP Server](../../catalog/tools/uniprot.html)
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — broader target-context dossier; this recipe is the focused structure-quality triage that the dossier defers to when "is this model docking-ready" is the question.
- [Estimate pharmacokinetic properties of a small molecule](estimate-pk-properties.html) — the small-molecule companion when the structure is in hand and the next question is the compound side.

## Sources

- [`Augmented-Nature/AlphaFold-MCP-Server`](https://github.com/Augmented-Nature/AlphaFold-MCP-Server) — verified 2026-05-27 (this run).
- [Varadi M. et al., "AlphaFold Protein Structure Database: massively expanding the structural coverage of protein-sequence space with high-accuracy models," *Nucleic Acids Res.* 2022](https://doi.org/10.1093/nar/gkab1061) — published 2021-11.
- [Varadi M. et al., "AlphaFold Protein Structure Database in 2024," *Nucleic Acids Res.* 2024](https://doi.org/10.1093/nar/gkad1011) — published 2023-11.
- [Bryant P. et al., "Improved prediction of protein-protein interactions using AlphaFold2," *Nature Communications* 2022](https://doi.org/10.1038/s41467-022-28865-w) — published 2022-03.
- [Karelina M. et al., "How accurately can one predict drug binding modes using AlphaFold models?" *J. Chem. Inf. Model.* 2023](https://doi.org/10.1021/acs.jcim.3c00601) — published 2023-09.
- [EBI AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/) — verified 2026-05-27 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=triage-alphafold-model-for-docking&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftriage-alphafold-model-for-docking.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
