---
title: Detect and rank druggable pockets on a protein structure
parent: All recipes
grand_parent: Recipes
nav_order: 21
problem_class: Data analysis
subject_areas: [Integrative Structural and Computational Biology, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-01
summary: Enumerate surface cavities on an apo structure with fpocket, rank them for ligandability with P2Rank, and emit a docking box — one Claude Skill.
---

# Detect and rank druggable pockets on a protein structure

Point Claude Code at a coordinate file with no bound ligand; get back a ranked pocket table with geometry and learned-ligandability scores kept side by side, the lining residues of each pocket, and a docking box ready for the screening step.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Integrative Structural and Computational Biology, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have a structure for a new target and no co-crystallized ligand to tell you where to aim. Every downstream structure-based step needs a site: docking needs a box, a virtual screen needs a receptor definition, a mutagenesis plan needs lining residues. Guessing from a cartoon render is how projects end up screening against a crystallization-additive cleft for three months.

The tooling exists and is mature — fpocket enumerates cavities geometrically, P2Rank scores surface points for learned ligandability — but the two answer different questions, install differently, and disagree often enough that reconciling them by hand is the actual work. Worse, the failure modes are silent: druggability models were trained on ligand-bound structures, so an apo or cryptic site gets a low score for reasons that have nothing to do with whether a drug can bind there. Solved looks like a committed script that produces one `pockets.csv` per structure — rank, volume, druggability score, lining residues, both tools' verdicts as separate columns — plus a docking box you can hand straight to Vina, and a provenance record naming the tool versions and the input hash.

## Recommended approach

Rung 2 — one Claude Skill, [Binding Site Detection](../../catalog/tools/binding-site-detection.html), which drives fpocket, P2Rank and (optionally) the CASTp / DoGSiteScorer web services and knows how to read their disagreements. Keep the run local unless your data-sharing policy permits sending coordinates to an academic web server.

1. **Install the skill.** Verbatim steps are on the [catalog page](../../catalog/tools/binding-site-detection.html) (clone `GPTomics/bioSkills`, run `./install-claude.sh --categories "structural-biology"` or copy `structural-biology/binding-site-detection` into `~/.claude/skills/`). Install fpocket 4.1+ and P2Rank 2.4+ when prompted on first use — the skill will not silently substitute one for the other.

2. **Vet the receptor before you search it.** Pockets are only as real as the atoms lining them. Run the [Structure Validation skill](../../catalog/tools/structure-validation.html) on an experimental file, or — for an AlphaFold model — [triage the model first](triage-alphafold-model-for-docking.html): pocket-lining side-chain rotamers are among the least reliable atoms in a predicted structure, and a low-pLDDT region will produce cavities that do not exist. Strip waters, ions and crystallization additives with the [Structure Preparation skill](../../catalog/tools/structure-preparation.html) before detection, or fpocket will happily wrap a pocket around a PEG molecule.

3. **Enumerate, then rank — as two separate columns.** Ask for both, and do not let either be collapsed into a single number:

   ```
   Structure: receptor_clean.pdb (apo, chain A only).

   Using the binding-site-detection skill:
     1. Run fpocket. For each pocket report: rank, volume (A^3),
        number of alpha spheres, mean local hydrophobic density,
        fpocket druggability score, and the lining residue list
        (chain + resnum + resname).
     2. Run P2Rank on the same file. For each predicted pocket
        report: rank, P2Rank score, pocket center (x,y,z), and
        lining residues.
     3. Match the two sets by centroid proximity (<= 5 A) and
        by lining-residue Jaccard overlap. Emit ONE table with
        columns: site_id, fpocket_rank, fpocket_volume,
        fpocket_drugscore, p2rank_rank, p2rank_score,
        n_shared_residues, agreement (both | fpocket_only |
        p2rank_only).
     Do not average the two scores into a single ranking.
   ```

   Sites where both tools agree are the safe bets. `fpocket_only` sites are usually shallow grooves or additive clefts; `p2rank_only` sites are worth a look precisely because P2Rank scores surface chemistry rather than enclosure.

4. **Anchor against what is already known.** Before trusting rank 1, check the target's annotated sites — catalytic residues, cofactor sites, a homolog's co-crystal ligand. Pull them with the [UniProt MCP server](../../catalog/tools/uniprot.html) (`Binding site` / `Active site` features) or find a holo structure with the [PDB MCP server](../../catalog/tools/pdb.html) and compare its ligand centroid to your predicted centers. Add a `known_site_overlap` column. If the tools miss a site you know is real, that is the calibration you need before believing the novel ones.

5. **Emit the docking box.** The point of the exercise:

   ```
   For site_id S1, write docking_box.json with:
     center: [x, y, z] (pocket centroid),
     size:   [sx, sy, sz] (pocket bounding box + 4 A padding
             on each axis, rounded to 0.5 A),
     lining_residues: [...],
     source: "fpocket+P2Rank consensus".
   ```

   That file drops straight into [AutoDock Vina](../../catalog/tools/autodock-vina-docking.html) / [smina](../../catalog/tools/smina-molecular-docking.html), or seeds the pocket for [a DiffDock run](dock-ligand-library-with-diffdock.html) and the [affinity-ranking recipe](rank-compound-library-by-predicted-affinity.html).

6. **Escalate to cryptic pockets only if the apo search comes up empty.** If the surface looks flat and the target is nonetheless known to be ligandable, run `mdpocket` over a conformational ensemble — a trajectory from the [GROMACS MCP server](../../catalog/tools/gromacs-mcp.html) or [OpenMM MCP server](../../catalog/tools/openmm-mcp.html), set up via the [MD-simulation recipe](set-up-protein-md-simulation-in-gromacs.html) — and report pocket *occurrence frequency* across frames, not a single-frame score. This is the step that turns a laptop job into a GPU job; do not reach for it first.

7. **Commit the artifact.** Version `detect_pockets.sh` (the fpocket and P2Rank invocations with their exact flags) and `reconcile_pockets.py` (the matching and table emission), alongside `pockets.csv`, `docking_box.json`, the prepared `receptor_clean.pdb`, and a `provenance.json` recording: fpocket and P2Rank versions, the P2Rank model name, the input PDB/AlphaFold accession **and its file sha256**, the preparation steps applied, whether any web service was called, and the model id that authored the script. Pocket rankings shift between tool versions; without the versions recorded you cannot tell a real conformational difference from a scorer update. See [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html).

## Why this assembly

Rung 2, and it stops there. The scientific content is two established command-line tools plus the judgement to read them against each other; the skill supplies the invocation details and the interpretation discipline (geometric cavity ≠ functional site; holo-trained scores under-detect apo pockets). Rung 1 — plain Claude Code — can shell out to fpocket if you have already installed and learned it, but will improvise flag choices and, worse, will confidently rank a crystallization-additive cleft first because nothing in its context says not to. Rung 3 is not warranted: the neighbouring components here (validation, preparation, docking) are separate recipes with their own outputs, not co-resident tools in one harness. Rung 4 is plainly excessive for a single-structure analysis whose output is one table.

## Availability

Fully open. The skill is MIT-licensed; fpocket, P2Rank and mdpocket are open-source and run entirely on your machine. Two optional components are external academic web services — CASTp and DoGSiteScorer (via the ProteinsPlus server) — so an unpublished or confidential structure should stay on the local fpocket/P2Rank path. There is no local substitute in the catalog for DoGSiteScorer's SVM druggability model; if you need a druggability number and cannot upload, use fpocket's own druggability score and treat it as coarser. P2Rank requires a Java runtime.

## Compute requirements

Laptop. P2Rank predicts on a single protein in under a second; fpocket is comparable, so a whole-PDB-entry scan is seconds and a few-hundred-structure batch runs in minutes on one core. Memory is negligible (tens of MB per structure). The one heavy path is step 6: `mdpocket` needs an MD trajectory first, which is a GPU job of hours to days depending on system size and the timescale of the cryptic opening — budget that separately, and note that the pocket analysis itself remains cheap once frames exist.

## Evidence

`Proposed`. No documented attempt at this exact assembly — Claude Code driving the Binding Site Detection skill through an enumerate-then-rank-then-reconcile workflow — is known as of 2026-08-01. The components and the *design* of the workflow are well benchmarked:

- **Rank with a learned scorer, enumerate with geometry.** In the largest binding-site benchmark to date — 13 predictors and 15 variants against the LIGYSIS dataset of ~30,000 protein–ligand complexes — fpocket predictions rescored by PRANK or DeepPocket gave the highest recall (60%), versus 39% for the weakest method tested; stronger scoring schemes alone improved recall by up to 14% and precision by up to 30% ([Utgés & Barton, *J. Cheminform.* 2024](https://doi.org/10.1186/s13321-024-00923-z)). That result is why step 3 separates enumeration from ranking rather than trusting one tool's ordering.
- **P2Rank as the ranking layer.** P2Rank outperformed fpocket, SiteHound, MetaPocket 2.0 and DeepSite in its original evaluation, at under 1 s per protein ([Krivák & Hoksza, *J. Cheminform.* 2018](https://doi.org/10.1186/s13321-018-0285-8)) — the speed is what makes batch use practical.
- **The apo caveat is measured, not folklore.** CryptoBench assembles 1,107 apo–holo pairs with substantial binding-site conformational change and shows that holo-based evaluation "yields unrealistic performance expectations" for cryptic sites, with P2Rank explicitly not tailored to them ([Škrhák et al., *Bioinformatics* 2024](https://doi.org/10.1093/bioinformatics/btae745)). This grounds step 6 and the warning against reading a low score as "not druggable".
- **Membrane targets degrade.** Across GPCR and ion-channel sets, every method tested scored worse on membrane-embedded interfaces than on a soluble PDBBind set (best-case normalized DCC / DVO 0.33–0.72) ([Pliushcheuskaya & Künze, *J. Chem. Inf. Model.* 2025](https://doi.org/10.1021/acs.jcim.5c00336)). If your target is a GPCR or channel, weight the known-site anchor in step 4 more heavily than the scores.

The missing link is a head-to-head of an agent-driven reconciliation against a structural biologist doing the same by hand.

## Alternatives considered

**PrankWeb (hosted).** The same P2Rank engine behind a web server, now with an integrated AutoDock Vina docking module, UniProt-ID input that pulls the AlphaFold model for you, and ChimeraX/PyMOL export ([Polák et al., *Nucleic Acids Res.* 2025](https://doi.org/10.1093/nar/gkaf421); AlphaFold and Docker support landed in [PrankWeb 3](https://doi.org/10.1093/nar/gkac389)). Reach for it for a one-off look at a public target — it is faster than installing anything. Reach for this recipe when you need a batch, an audit trail, or the structure never to leave your machine.

**Skip detection entirely.** If a holo structure of your target or a close homolog exists, superpose it and take the ligand's position as the site — cheaper and more reliable than any prediction. [Superpose two protein structures](superpose-two-protein-structures.html) is that path, and step 4 here is its degenerate case. Detection earns its keep only when no bound-state reference exists.

**Blind docking.** DiffDock and similar can search the whole surface without a box. That trades a defensible, inspectable site hypothesis for a pose that may be anywhere, and it does not give you lining residues to design mutants against. Use it as a cross-check on the sites this recipe ranks, not as a replacement.

## See also

- [Binding Site Detection (Claude Skill)](../../catalog/tools/binding-site-detection.html)
- [Structure Validation (Claude Skill)](../../catalog/tools/structure-validation.html) — vet the receptor before searching it.
- [Structure Preparation (Claude Skill)](../../catalog/tools/structure-preparation.html) — strip waters and additives first.
- [Triage an AlphaFold model for structure-based drug design](triage-alphafold-model-for-docking.html) — the predicted-model pre-flight; it assumes a pocket residue list, which this recipe produces.
- [Prepare protonation states for docking](prepare-protonation-states-for-docking.html) — the ligand-side companion once the box exists.
- [Dock a ligand library with DiffDock](dock-ligand-library-with-diffdock.html) and [Rank a compound library by predicted affinity](rank-compound-library-by-predicted-affinity.html) — the downstream consumers of `docking_box.json`.
- [Set up a protein MD simulation in GROMACS](set-up-protein-md-simulation-in-gromacs.html) — the ensemble the cryptic-pocket path needs.

## Sources

- [Utgés J.S. & Barton G.J., "Comparative evaluation of methods for the prediction of protein-ligand binding sites," *J. Cheminform.* 2024](https://doi.org/10.1186/s13321-024-00923-z) — published 2024; verified 2026-08-01 (this run).
- [Krivák R. & Hoksza D., "P2Rank: machine learning based tool for rapid and accurate prediction of ligand binding sites from protein structure," *J. Cheminform.* 2018](https://doi.org/10.1186/s13321-018-0285-8) — published 2018; verified 2026-08-01 (this run).
- [Škrhák V. et al., "CryptoBench: cryptic protein-ligand binding sites dataset and benchmark," *Bioinformatics* 2024](https://doi.org/10.1093/bioinformatics/btae745) — published 2024; verified 2026-08-01 (this run).
- [Pliushcheuskaya P. & Künze G., "Evaluation of Small-Molecule Binding Site Prediction Methods on Membrane-Embedded Protein Interfaces," *J. Chem. Inf. Model.* 2025](https://doi.org/10.1021/acs.jcim.5c00336) — published 2025; verified 2026-08-01 (this run).
- [Polák L. et al., "PrankWeb 4: a modular web server for protein-ligand binding site prediction and downstream analysis," *Nucleic Acids Res.* 2025](https://doi.org/10.1093/nar/gkaf421) — published 2025; verified 2026-08-01 (this run).
- [Jakubec D. et al., "PrankWeb 3: accelerated ligand-binding site predictions for experimental and modelled protein structures," *Nucleic Acids Res.* 2022](https://doi.org/10.1093/nar/gkac389) — published 2022.
- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills) — install path per the catalog page, last verified 2026-08-01.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=detect-and-rank-druggable-pockets&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdetect-and-rank-druggable-pockets.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
