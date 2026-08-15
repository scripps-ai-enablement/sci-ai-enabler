---
title: Characterize a protein–protein interface from a structure you already have
parent: All recipes
grand_parent: Recipes
nav_order: 3
problem_class: Data analysis
subject_areas: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-08
summary: Use the Interface Analysis skill to get contact residues and buried surface area from a solved or predicted complex — and to decide whether the interface is real or crystal packing.
---

# Characterize a protein–protein interface from a structure you already have

Take a complex you already have — a PDB entry, a cryo-EM deposition, a co-folded model — and get a residue-level contact list, per-partner buried surface area, and an explicit verdict on whether the interface is biology or a crystallization artifact.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Integrative Structural and Computational Biology, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have a structure of two chains touching and you need to say something specific about where they touch: which residues to mutate for a disruption assay, which surface to graft into a competing peptide, whether a patient variant sits at the binding surface, where to place a crosslinker. The mechanical part — list the cross-chain contacts — is easy and everyone does it. The two parts that quietly decide whether your answer is right are the ones people skip.

The first is the **cutoff**: the residue list you report is a function of the distance criterion you chose, and a 4 Å heavy-atom list and an 8 Å Cα list are different sets of residues describing the same structure. Reporting one without the other is fine; reporting one without *saying which* is not. The second is **whether the interface exists at all outside the crystal**. Two chains in an asymmetric unit are in contact because the crystal packed them, not necessarily because they bind in solution, and this is not a solved problem — CAPRI assessors still report that docking scoring functions "do not distinguish well biological from crystal packing interfaces" ([Kundrotas et al. 2018](https://pubmed.ncbi.nlm.nih.gov/28905425/)). A perfectly executed contact analysis of a packing artifact produces a mutant that does nothing, and you find out six weeks later at the bench. "Solved" here is a committed table of interface residues with the cutoff and assembly recorded next to them, a buried-surface-area number, and a tiered biological-vs-packing call that says how confident it is and what would settle it.

## Recommended approach

Rung 2 — one Claude Skill, the [Interface Analysis skill](../../catalog/tools/interface-analysis.html) (bioSkills), which drives Bio.PDB locally: `NeighborSearch` for contacts, `ShrakeRupley` for SASA, and a documented biology-vs-packing cross-check. The only reason a second component appears is fetching the coordinates.

1. **Install the skill.** Verbatim steps are on the [catalog page](../../catalog/tools/interface-analysis.html) — clone `GPTomics/bioSkills` and either run `./install-claude.sh --categories "structural-biology"` or copy the single `structural-biology/interface-analysis` directory into `~/.claude/skills/`. Biopython and NumPy are the skill's own prerequisites; FreeSASA is optional.

2. **Fetch the biological assembly, not the asymmetric unit.** This is the step that most often decides the answer, so make it explicit rather than letting a default download choose for you. Use the [PDB MCP server](../../catalog/tools/pdb.html) (or [PDBe](../../catalog/tools/pdbe.html)) to retrieve the assembly file for your entry, and record which assembly ID you took. If your input is a predicted complex — from [co-folding](predict-protein-protein-complex-interface.html) or an [antibody–antigen prediction](predict-antibody-antigen-complex.html) — the model *is* the assembly and this step is a no-op, but say so in the provenance rather than leaving it blank. If you are working from a crystal structure and you cannot establish which assembly is biological, stop and resolve that before computing anything: everything downstream inherits the error.

3. **Declare the cutoff before you run.** Pick one primary definition and stick to it across every interface you compare. Heavy-atom 4.5 Å is a reasonable default for van der Waals contact; Cα–Cα 8 Å if you want a coarser topological definition; 3.5–4.0 Å for hydrogen bonds and salt bridges specifically. Write the choice and the reason into the command file, not into a chat message.

4. **Run the analysis and write it to a script.** Have Claude invoke the skill and then capture the calculation as `interface_analysis.py` — do not leave it as an interactive result:

   ```
   Use the interface-analysis skill on assembly.cif, chains A and B.

   - Primary contact definition: heavy-atom pairs within 4.5 A. Record the
     cutoff in the output, and emit an 8 A Ca-Ca list as a second column so
     the definition-sensitivity is visible.
   - Compute SASA with ShrakeRupley at probe radius 1.4 A on the complex and
     on each chain in isolation, using the identical probe radius and atom
     selection for all three, and report BSA = SASA(A) + SASA(B) -
     SASA(complex), plus the per-partner half.
   - Classify each interface residue as core (buried on complexation) or rim.
   - Enumerate hydrogen bonds and salt bridges at 3.5 A separately.
   - Write the code you run to interface_analysis.py so I can re-run it.
   ```

   Two things to check in the emitted script rather than trusting: that the three SASA calculations use the **same** probe radius and atom selection (a mismatch makes BSA meaningless in a way that is invisible in the number), and that hydrogens are excluded consistently.

5. **Emit the tables.** `contacts.csv` — one row per residue pair (`chain_i, resnum_i, resname_i, chain_j, resnum_j, resname_j, min_heavy_atom_dist, contact_type`), where `contact_type` distinguishes van der Waals, hydrogen bond, and salt bridge. `interface_residues.csv` — one row per residue (`chain, resnum, resname, delta_sasa, core_or_rim, in_4.5A_set, in_8A_ca_set`). Keeping these as two tables matters: the pair list is what you reason about mechanistically, the residue list is what you hand to a cloning protocol, and merging them duplicates residues once per partner contact and inflates every count you take from it. Both files are the audit trail; every claim in your figure legend has to be readable off them.

6. **Make the biology-vs-packing call tiered, and never silent.** Emit `interface_call.md` with a verdict of `biological`, `ambiguous`, or `likely_packing`, the evidence for it, and — for anything not `biological` — what would settle it. The inputs the skill cross-checks: BSA magnitude (small interfaces are the suspicious ones), hydrogen-bond and salt-bridge count, conservation of the interface residues relative to the rest of the surface, and the PDBePISA complexation-significance score. Two rules keep this honest. **Default to `ambiguous`, not to `biological`** — no single one of those signals is decisive, and published classifiers reach roughly 90% accuracy at best on curated benchmarks (see Evidence), which means one interface in ten is wrong even under favourable conditions. And **record orthogonal evidence as a separate line**: whether the complex is annotated in [Complex Portal](../../catalog/tools/complex-portal.html) or [IntAct](../../catalog/tools/intact.html), and whether solution data (SEC, SEC-MALS, native MS, co-IP) supports the stoichiometry. An interface with 400 Å² BSA, two hydrogen bonds, no conservation signal and no solution support is `likely_packing` however clean the contact list looks.

7. **Record provenance.** `provenance.json` should carry the PDB/EMDB accession **and the assembly ID**, the structure's deposition or model date, the contact cutoff and probe radius as literal values, Biopython/NumPy/FreeSASA versions, the skill commit SHA, the sha256 of the input coordinate file, the date of the PDBePISA query (a live web service — its score can change under you), and the model id. The assembly ID and the cutoff are the two fields that make a re-run comparable; the reproducibility pattern is described in the [reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) guide.

The durable artifact is the committed `.claude/commands/characterize-interface.md`, `interface_analysis.py`, a pinned `requirements.txt`, and per-structure `contacts.csv` + `interface_residues.csv` + `interface_call.md` + `provenance.json`.

## Why this assembly

Rung 2, and it stops there. Contacts, SASA and the packing cross-check are one skill's workflow over one coordinate file, executed locally with Bio.PDB; the only second component is the coordinate fetch, which is a download. Rung 1 fails for a specific reason worth naming: Claude Code alone will happily produce a plausible-looking list of interface residues from the sequence and its training memory of the complex, and that list will be confidently wrong in a way you cannot detect by reading it — the arithmetic has to touch the actual coordinates. Rung 3 or 4 buys nothing, because the hard part is not orchestration but the two judgement calls (assembly and cutoff) that the skill exists to force you to make explicitly.

## Availability

Fully open. bioSkills is MIT; Biopython, NumPy and FreeSASA are open-source and installed separately; the PDB and PDBe MCP servers front free public APIs. Everything except one step runs **locally**, so an unpublished or confidential structure never leaves your machine — with the exception that the PDBePISA complexation-significance cross-check is a query to an EBI web service, which means submitting your entry ID or coordinates to a third party. For a confidential structure, skip PISA and lean on BSA, hydrogen bonding, conservation and solution data, and record in `interface_call.md` that the PISA input was omitted rather than that it was negative.

## Compute requirements

Laptop. Contact search and Shrake–Rupley SASA on a two-chain complex of a few hundred residues per chain are seconds. The cost scales with atom count, so a large assembly — a ribosome subunit, a nucleosome complex, a viral capsid protomer set — moves SASA into minutes and memory into the low gigabytes; if you only care about one interface in a large assembly, extract the two chains of interest first, but compute SASA of the isolated chains from that same extraction so the three calculations stay consistent. Analysing every pairwise interface in a large multi-chain assembly is quadratic in chain count and is where a laptop starts to hurt; batch it rather than requesting it in one go.

## Evidence

Proposed. No documented attempt of this Claude-skill assembly on interface characterization is known, and the skill is not benchmarked end-to-end (its catalog page records `verified: works`, which establishes the workflow runs, not that its biological-vs-packing verdict is calibrated). The closest evidence is method-level, and it is what motivates the tiered verdict rather than a binary one:

- **Luo et al. (*Proteins* 2014)** trained a random forest on interface core/rim composition and evolutionary features, reporting ROC 0.923 in 5-fold cross-validation and 91.4% / 91.7% accuracy on two test sets, and reported outperforming DiMoVo, Pita, PISA and EPPIC ([doi:10.1002/prot.24670](https://doi.org/10.1002/prot.24670)). This is the ceiling for automated classification on curated data — high, and not high enough to report a bare verdict.
- **Block et al. (*Proteins* 2006)** classified 172 complexes (96 crystal-packing monomers vs 76 biological homodimers) at up to 94.8% accuracy using physicochemical interface descriptors ([PMID 16955490](https://pubmed.ncbi.nlm.nih.gov/16955490/)).
- **Tsuchiya, Nakamura & Kinoshita (2008)** reached ~88.8% on homodimer-vs-symmetry-contact discrimination with a hydrophobicity/electrostatic/shape complementarity score, and specifically note their discriminator **does not correlate with contact area** ([PMID 21918609](https://pubmed.ncbi.nlm.nih.gov/21918609/)) — the direct justification for not treating BSA alone as the verdict.
- **Kundrotas et al. (*Proteins* 2018)**, assessing CASP12/CAPRI37 predictions, report that their scoring function "still does not distinguish well biological from crystal packing interfaces" ([doi:10.1002/prot.25380](https://doi.org/10.1002/prot.25380)) — the basis for defaulting to `ambiguous` and requiring orthogonal evidence.

The mechanical parts of the recipe (contacts, SASA, BSA) are not in question; they are standard Bio.PDB calculations. The uncertainty lives entirely in step 6, which is why that step is the one with the hard rules.

## Alternatives considered

- **[Predict a protein–protein complex to map the binding interface](predict-protein-protein-complex-interface.html) (rung 2).** Reach for that when you do *not* have a structure and need to generate one by co-folding. It is the upstream sibling: its output is exactly this recipe's input, and running this recipe on a co-folded model is the natural next step — with the caveat that a predicted interface's contacts inherit the prediction's error, so the consensus-across-models discipline there matters more than the cutoff discipline here.
- **[Vet a PDB structure before reusing it](vet-a-pdb-structure-before-reusing-it.html) (rung 2).** Run that first if you have not established that your chosen entry is fit for purpose at all — resolution, construct mutations, missing loops at the interface. A gap in the density exactly at the contact surface will silently shorten your contact list.
- **Contact analysis by hand in [PyMOL](../../catalog/tools/pymol.html) or [ChimeraX](../../catalog/tools/chimerax-mcp.html).** Faster for a one-off look and better for the figure. Use it to *see* the interface. It is the wrong tool when you need the numbers in a table with the cutoff recorded next to them, which is the reproducibility requirement this recipe exists to satisfy.
- **Experimental interface mapping (alanine scan, crosslinking-MS, HDX-MS, SEC-MALS).** The ground truth, and the resolution of every `ambiguous` verdict. This recipe tells you which five residues to mutate first instead of twenty; escalate as soon as the cost of being wrong exceeds the cost of the experiment.

## See also

- [Interface Analysis (bioSkills)](../../catalog/tools/interface-analysis.html)
- [PDB MCP Server](../../catalog/tools/pdb.html) · [PDBe](../../catalog/tools/pdbe.html) — fetch the biological assembly.
- [Complex Portal](../../catalog/tools/complex-portal.html) · [IntAct](../../catalog/tools/intact.html) — curated orthogonal interaction evidence for the packing call.
- [Look up the curated composition and stoichiometry of a protein complex](look-up-curated-complex-composition.html) — a followable path for that orthogonal-evidence check.
- [Predict a protein–protein complex to map the binding interface](predict-protein-protein-complex-interface.html) — generates the input when you have no structure.
- [Vet a PDB structure before reusing it](vet-a-pdb-structure-before-reusing-it.html) — run upstream.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [Luo et al., "Effective discrimination between biologically relevant contacts and crystal packing contacts using new determinants" (*Proteins* 2014)](https://pubmed.ncbi.nlm.nih.gov/25142782/) — ROC 0.923, 91.4%/91.7% test accuracy, outperforms DiMoVo/Pita/PISA/EPPIC; published 2014; verified 2026-08-08 (this run).
- [Block et al., "Physicochemical descriptors to discriminate protein-protein interactions in permanent and transient complexes" (*Proteins* 2006)](https://pubmed.ncbi.nlm.nih.gov/16955490/) — up to 94.8% on 172 packing-vs-functional complexes; published 2006; verified 2026-08-08 (this run).
- [Tsuchiya, Nakamura & Kinoshita, "Discrimination between biological interfaces and crystal-packing contacts" (2008)](https://pubmed.ncbi.nlm.nih.gov/21918609/) — ~88.8%, discriminator explicitly uncorrelated with contact area; published 2008; verified 2026-08-08 (this run).
- [Kundrotas et al., "Modeling CAPRI targets 110-120 by template-based and free docking" (*Proteins* 2018)](https://pubmed.ncbi.nlm.nih.gov/28905425/) — CAPRI assessment: scoring still does not distinguish biological from crystal-packing interfaces; published 2018; verified 2026-08-08 (this run).
- [`GPTomics/bioSkills` — `structural-biology/interface-analysis`](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/interface-analysis/SKILL.md) — skill workflow, cutoff guidance, SASA/BSA procedure; catalog page last verified 2026-08-01.
- [Biopython `Bio.PDB.SASA` (ShrakeRupley)](https://biopython.org/docs/latest/api/Bio.PDB.SASA.html) — SASA implementation the skill drives.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=characterize-a-protein-protein-interface&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fcharacterize-a-protein-protein-interface.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
