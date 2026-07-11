---
title: Scan a therapeutic antibody for glycosylation sites
parent: All recipes
grand_parent: Recipes
nav_order: 23
problem_class: Experimental design
subject_areas: [Immunology and Microbiology, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-11
summary: Use the Glycoengineering skill to scan an antibody sequence for N-glycosylation sequons and O-glycosylation hotspots before committing to a cell-line or developability campaign.
---

# Scan a therapeutic antibody for glycosylation sites

Hand Claude an antibody (or any glycoprotein) sequence and get back an annotated map of every N-glycosylation sequon and O-glycosylation hotspot — including the conserved Fc Asn-297 site that governs effector function — as a sequence-level developability pre-flight.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Immunology and Microbiology, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You are designing or assessing a therapeutic antibody (or an immunogen, or a fusion protein) and need to know where it will be glycosylated before you commit to a cell line, an affinity-maturation campaign, or a manufacturing run. Glycosylation is a critical quality attribute: the conserved N-glycan at Fc Asn-297 modulates FcγRIIIa binding and antibody-dependent cellular cytotoxicity (ADCC), and *unintended* N-glycosylation sequons introduced into the variable domains during humanization or affinity maturation are a recurring developability liability — they create heterogeneity, can block the paratope, and complicate comparability. You want a fast, reproducible answer to "where are the sequons, and did my last round of mutations add or remove any?" — before the wet lab, not after. Solved looks like: paste a heavy- and light-chain sequence, get an annotated table of every N-X-S/T sequon (X ≠ P), flagged Fc vs variable-domain location, plus predicted O-glycosylation hotspots, with a note on which sites are expected vs introduced.

## Recommended approach

1. **Install the [Glycoengineering skill](../../catalog/tools/glycoengineering.html)** (K-Dense `scientific-agent-skills`):

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   ```

   Enable the `glycoengineering` skill when prompted. It installs its Python dependencies via `uv` on first invocation, so have `uv` available.

2. **Provide the chain sequences.** Paste the heavy and light chains as FASTA. If you only have a UniProt accession or a parent-antibody name, fetch the canonical sequence first with the [gget skill](../../catalog/tools/gget.html) and confirm the numbering scheme you care about (EU vs Kabat vs linear) — the skill scans on the linear sequence, so tell Claude which residue is your reference Asn-297.

3. **Prompt for a full sequon scan.** A minimal version:

   ```
   Use the glycoengineering skill to scan the antibody chains below.

   For each chain:
   1. Find every N-glycosylation sequon (N-X-S/T, X != P) and report
      its position, the +1 and +2 residues, and whether it sits in a
      constant domain (especially Fc Asn-297) or a variable domain.
   2. Predict O-glycosylation hotspots (Ser/Thr-rich regions) and
      report their spans.
   3. Flag any variable-domain N-sequon as a candidate UNINTENDED site
      (potential developability liability).

   Heavy chain (FASTA):
   >HC
   <paste>
   Light chain (FASTA):
   >LC
   <paste>

   Return one CSV per chain with columns:
   chain, position, motif, type (N|O), domain (Fc|CH|CL|VH|VL),
   status (expected|introduced), note
   ```

4. **Compare against the parent, not in isolation.** The signal that matters for affinity maturation is the *delta*: ask Claude to diff the sequon map of your engineered variant against the parent antibody, so introduced or lost sites surface explicitly rather than being buried in the full list.

5. **(Optional) Propose edits to add or remove a site.** If the scan flags an unwanted variable-domain sequon, ask the skill to suggest the minimal conservative substitution (typically S/T → A at the +2 position, or N → Q) that removes the motif without disrupting the paratope, and carry the candidate into a structure check.

## Why this assembly

Rung 2. One skill does the whole scan: sequon detection is a deterministic motif search, and the O-glycosylation/edit-suggestion steps are what the skill adds on top. Claude Code alone (rung 1) *can* regex N-X-S/T, but it cannot reliably run the O-glycosylation predictors (NetOGlyc) or orchestrate the glycan-analysis tooling, and it will confabulate domain assignments without a structured scan — so the skill earns rung 2. No toolbelt (rung 3) or autonomous system (rung 4) is warranted for a sequence-level annotation: the escalation that *would* justify rung 3 is closing the loop into structure (does the glycan shield the paratope?) or into a wet-lab assay — pair the [AlphaFold skill](../../catalog/tools/alphafold.html) for the former or the [Adaptyv skill](../../catalog/tools/adaptyv.html) for the latter only when you actually need it.

## Availability

Fully open. The Glycoengineering and gget skills are free/OSS. The core N-sequon scan is pure-Python and needs no API keys. Some external predictors the skill can call (NetNGlyc / NetOGlyc, DTU Health Tech) are free for academic use but require separate registration for commercial use — the skill orchestrates them but does not redistribute them, so plan for that registration if you need the NetOGlyc-backed O-glycosylation calls in a commercial setting.

## Compute requirements

Laptop-sufficient. Sequon scanning over a pair of ~450-residue chains is instantaneous; O-glycosylation prediction and glycan-tool orchestration are light. No GPU. The only latency is network round-trips if the skill calls a hosted predictor (NetOGlyc) rather than a local one.

## Evidence

Proposed. No documented attempt of this exact Claude/Glycoengineering-skill assembly is known. The underlying biology and the value of sequon mapping are well established. The Fc Asn-297 N-glycan's control of effector function is a validated therapeutic lever: **Shuang et al. (*mAbs* 2026)** show that two anti-CD20 antibodies with *identical amino-acid sequences* but divergent Asn-297 glycoforms (complete afucosylation vs bisecting GlcNAc) produce disparate FcγRIIIA binding, ADCC potency, and thermal stability ([doi:10.1080/19420862.2026.2657099](https://doi.org/10.1080/19420862.2026.2657099)). **Illés (2026)** reviews how Fc-glycan state and FcγRIIIa polymorphism modulate ADCC across approved anti-CD20 mAbs and how Fc engineering compensates ([doi:10.18071/isz.79.0131](https://doi.org/10.18071/isz.79.0131)). Terminal galactosylation as a CQA affecting ADCC/CDC and half-life is documented by **Klingler et al. (*Biotechnol. Bioeng.* 2024)** ([doi:10.1002/bit.28616](https://doi.org/10.1002/bit.28616)). What is not independently benchmarked is the convenience layer — Claude driving the K-Dense skill to assemble the annotated sequon map and parent-vs-variant diff.

## Alternatives considered

- **Claude Code alone (rung 1).** Fine if all you want is a raw N-X-S/T regex over a single chain and you already know the domain boundaries. It cannot run the O-glycosylation predictors or suggest glycan-tool-backed edits, and it will guess at domain assignment — so for anything beyond the trivial sequon list, the skill is worth the install.
- **[Score point mutations with a protein language model](score-protein-variants-with-esm.html) (ESM, rung 2).** Reach for that when the question is *fitness/tolerance* of a substitution, not *glycosylation*. The two are complementary: scan for sequons here, then score the conservative knock-out substitution (e.g. S→A) for tolerability there before ordering it.
- **[Adaptyv wet-lab loop](../../catalog/tools/adaptyv.html) (rung 3+).** Escalate only when you need experimental ground truth — expression, binding, thermostability — on the glyco-variant. The sequence scan is the cheap pre-flight that decides which variants are worth that spend.

## See also

- [Glycoengineering (Claude Skill)](../../catalog/tools/glycoengineering.html)
- [gget (Claude Skill)](../../catalog/tools/gget.html) — fetches the canonical antibody/UniProt sequence for the input step.
- [Adaptyv (Claude Skill)](../../catalog/tools/adaptyv.html) — wet-lab validation loop for the down-selected glyco-variants.
- [Score point mutations for functional impact with a protein language model](score-protein-variants-with-esm.html) — tolerability scoring for any sequon knock-out substitution.

## Sources

- [Shuang et al., "Impact of afucosylation strategy on antibody function: a comparative study of glycoengineered anti-CD20 antibodies" (*mAbs* 2026)](https://doi.org/10.1080/19420862.2026.2657099) — published 2026-01-01; verified 2026-06-13 (this run).
- [Illés, "Developing anti-CD20 molecules and B cell depletion in multiple sclerosis" (2026)](https://doi.org/10.18071/isz.79.0131) — Fc-glycan / FcγRIIIa / ADCC review; published 2026-01-01; verified 2026-06-13 (this run).
- [Klingler et al., "Developing microRNAs as engineering tools to modulate monoclonal antibody galactosylation" (*Biotechnol. Bioeng.* 2024)](https://doi.org/10.1002/bit.28616) — galactosylation as a CQA; published 2024.
- [`K-Dense-AI/scientific-agent-skills` — `glycoengineering` SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/glycoengineering/SKILL.md) — N-/O-sequon scanning and NetNGlyc/NetOGlyc orchestration; verified 2026-06-13 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=scan-antibody-glycosylation-sites&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fscan-antibody-glycosylation-sites.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
