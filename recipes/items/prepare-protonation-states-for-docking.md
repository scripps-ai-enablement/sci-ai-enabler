---
title: Prepare the correct protonation state of a ligand before docking
parent: All recipes
grand_parent: Recipes
nav_order: 19
problem_class: Experimental design
subject_areas: [Chemistry, Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
summary: Use the Rowan skill in Claude Code to predict macro-pKa and the dominant protonation state of ligands at physiological pH before docking or MD, as a reproducible prepared-ligand table.
last_verified: 2026-07-11
---

# Prepare the correct protonation state of a ligand before docking

Hand Claude Code a list of ligand SMILES; get back each compound in its dominant protonation (and, where relevant, tautomeric) state at physiological pH, with the macro-pKa values that justify the assignment — so the structures you feed into docking or MD carry the right formal charges instead of whatever state the drawn SMILES happened to encode.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery, Integrative Structural and Computational Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A SMILES string carries whatever protonation state the chemist happened to draw — a carboxylic acid keyed as neutral `C(=O)O`, a basic amine keyed as neutral `N`, a zwitterion drawn as either extreme. Docking and molecular dynamics do not fix this for you: they place the atoms and charges they are given. Feed an unionized carboxylate into a pose where the biological reality is a −1 anion salt-bridging an active-site lysine, and the score, the pose, and every downstream interpretation are wrong. The effect is not marginal — protonation and tautomeric state are well documented to swing virtual-screening enrichment and pose ranking ([Kim et al., *J. Comput. Aided Mol. Des.* 2013](https://doi.org/10.1007/s10822-013-9643-9)).

The recurring, unglamorous prep step is therefore: for each ligand, decide the *dominant* microspecies at pH ≈ 7.4, assign the right formal charges, and note the pKa that justifies it (so a reviewer can see why a group was protonated). Solved looks like: a list of SMILES in, a table out with each compound's physiological-pH SMILES, net charge, and governing macro-pKa values — reproducibly, on a laptop, before a single docking job is launched.

## Recommended approach

1. **Install the [Rowan skill](../../catalog/tools/rowan.html)** and set an API key. Rowan runs the pKa/macro-pKa models as cloud workflows; the free tier at [labs.rowansci.com](https://labs.rowansci.com) covers this recipe.

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   export ROWAN_API_KEY="your_api_key_here"
   ```

   Enable the `rowan` skill when prompted. Confirm the key is visible to the session before running any workflow.

2. **(Optional, local) canonicalize the input first with the [Datamol skill](../../catalog/tools/datamol.html).** Strip salts, keep the largest fragment, and canonicalize tautomers so the pKa call operates on a clean parent. This step is laptop-local and free; do it when the input SMILES come from a messy vendor export. Skip it for hand-drawn, already-clean leads.

3. **Write the protonation-prep step to a versioned script.** Have Claude Code author `prepare_protonation.py` — do not leave the workflow as an interactive chat. A minimal prompt:

   ```
   Input: ligands.csv with columns id, smiles.

   Write prepare_protonation.py that, for each row:
     1. (if datamol available) standardize the SMILES: largest
        fragment, canonical tautomer, neutralize, canonical SMILES.
     2. Use the Rowan skill: submit rowan.submit_macropka_workflow
        over pH 0-14; wait; retrieve. From the result take the
        dominant microspecies at pH 7.4 and its SMILES, and the
        macro-pKa values (acidic and basic) that bracket it.
     3. Record: id, input_smiles, prepared_smiles_pH7.4, net_charge,
        macro_pka_acidic, macro_pka_basic, dominant_fraction.
   Emit prepared_ligands.csv sorted by id. Print a one-line summary
   per ligand: id -> net_charge (governing pKa).
   ```

   Have Claude submit workflows in a small batch with polite waits; macro-pKa runs take 5–15 minutes each, so cache retrieved results by input InChIKey so a re-run does not re-submit.

4. **Record provenance.** Emit `provenance.json` capturing the Rowan skill version/tag, the macro-pKa workflow/model identifier and its Rowan-side workflow IDs, the `rowan-mcp`/skill package version, the pH used (7.4), the run date, the sha256 of `ligands.csv` and `prepared_ligands.csv`, and the model id driving the session. Cloud workflow results are not byte-reproducible — the recorded workflow IDs and date are what make a later divergence visible.

5. **Hand off the prepared table.** `prepared_ligands.csv` is the durable artifact. Feed `prepared_smiles_pH7.4` straight into the [Dock a ligand library with DiffDock](dock-ligand-library-with-diffdock.html) or [Rank a compound library by predicted binding affinity](rank-compound-library-by-predicted-affinity.html) recipes, or into [Set up a protein MD simulation in GROMACS](set-up-protein-md-simulation-in-gromacs.html). Commit `prepare_protonation.py`, a pinned `requirements.txt`, `prepared_ligands.csv`, and `provenance.json` to version control. Follow the [reproducibility guide](../../guide/advanced/reproducibility.html) for the artifact layout.

## Why this assembly

Rung 2 of the simplicity ladder. Physiological-pH protonation-state assignment needs a real pKa model — the RDKit/Datamol standardization step (rung 1) canonicalizes charges and tautomers but does *not* predict pH-dependent ionization, so it cannot tell you a carboxylate is anionic at 7.4. The [Rowan skill](../../catalog/tools/rowan.html) exposes exactly one primitive that closes the gap: `submit_macropka_workflow`, which returns the pH-resolved microspecies distribution and macro-pKa values. One skill, one workflow — no orchestration across heterogeneous APIs (rung 3) and no autonomous chemist (rung 4) is warranted. The Datamol pre-clean is an optional laptop-local convenience, not a second essential tool.

## Availability

Fully open. The [Rowan skill](../../catalog/tools/rowan.html) ships in the `K-Dense-AI/scientific-agent-skills` collection (community OSS); the optional [Datamol skill](../../catalog/tools/datamol.html) is MIT. Rowan's pKa/macro-pKa models run as cloud workflows and require a free Rowan API key (`ROWAN_API_KEY`; free tier at labs.rowansci.com) — no subscription or institutional licence, but the compute runs on Rowan's servers, so SMILES leave your machine. If ligand structures are confidential, treat this as a data-residency caveat and confirm your project's policy before submitting. The `rowan-mcp` repo does not publish a LICENSE file; confirm licensing before redistributing the wrapper.

## Compute requirements

Laptop. All heavy computation runs cloud-side on Rowan; your machine only submits and polls. Budget wall-clock per ligand: microscopic pKa 2–5 min, macro-pKa 5–15 min, at roughly 5–15 Rowan credits each. For a 100-ligand batch, submit concurrently and cache by InChIKey; the optional Datamol standardization pass is sub-second per molecule on a single CPU core. No GPU, negligible local RAM.

## Evidence

Proposed. No published benchmark of an LLM-driven Rowan protonation-prep workflow is known. The closest documented evidence is component-level and problem-level: Rowan's own platform documents microscopic and macro-pKa prediction workflows ([Rowan Labs](https://labs.rowansci.com)), and the *impact* this step addresses is well established — protonation, tautomeric, and receptor ionization states are repeatedly shown to change virtual-screening enrichment and pose ranking ([Kim et al., *J. Comput. Aided Mol. Des.* 27:235, 2013](https://doi.org/10.1007/s10822-013-9643-9)). Each component (a pKa model; a docking or MD downstream) has independent validation; the agent-orchestrated prep assembly does not. Treat `prepared_ligands.csv` as a defensible starting state to be sanity-checked (does the net charge match chemical intuition for each ionizable group?), not an oracle.

## Alternatives considered

- **Datamol / RDKit standardization alone (rung 1).** Neutralizes charges and canonicalizes tautomers but is pH-blind — it will happily hand a neutral carboxylic acid to docking. Use it as the *pre-clean* here, not as the protonation decision. See [Enumerate analogs around a lead](enumerate-analogs-around-a-lead.html) for that standardization surface.
- **A local pH-aware protonator (e.g. Dimorphite-DL, OpenBabel `-p`).** These enumerate plausible protonation states offline and keep SMILES on your machine — attractive when structures are confidential. None is currently a Claude-installable skill or MCP in [`catalog/tools/`](../../catalog/), so the recipe cannot recommend them yet; a note is filed for the catalog curator. Reach for one manually if data residency forbids cloud submission.
- **Skipping prep and docking the drawn state.** Defensible only for neutral, non-ionizable scaffolds. For anything with a carboxylate, a basic amine, or an ambiguous tautomer, skipping this step silently biases every downstream score.

## See also

- [Rowan (Claude Skill / MCP)](../../catalog/tools/rowan.html)
- [Datamol (Claude Skill)](../../catalog/tools/datamol.html) — the optional local standardization pre-clean.
- [Dock a ligand library with DiffDock](dock-ligand-library-with-diffdock.html) — the downstream docking step this prepares ligands for.
- [Rank a compound library by predicted binding affinity](rank-compound-library-by-predicted-affinity.html) — alternate downstream scoring step.
- [Set up a protein MD simulation in GROMACS](set-up-protein-md-simulation-in-gromacs.html) — MD downstream that also needs correct ligand charges.
- [Rank the conformers and tautomers of a small molecule with semi-empirical QM](rank-conformers-and-tautomers-with-xtb.html) — the local, laptop-side alternative when SMILES cannot leave your machine, and the way to pick a 3D starting geometry once the charge state is fixed.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the artifact + provenance pattern this recipe follows.

## Sources

- [`K-Dense-AI/scientific-agent-skills` — rowan skill (SKILL.md)](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/rowan/SKILL.md) — documents `submit_pka_workflow` / `submit_macropka_workflow`; verified 2026-07-11 (this run).
- [Rowan Labs](https://labs.rowansci.com) — pKa/macro-pKa workflow platform, free tier; verified 2026-07-11 (this run).
- [Kim M.O. et al. — Effects of protonation and rotameric states on virtual screening, *J. Comput. Aided Mol. Des.* 27:235 (2013)](https://doi.org/10.1007/s10822-013-9643-9) — published 2013.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=prepare-protonation-states-for-docking&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fprepare-protonation-states-for-docking.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
