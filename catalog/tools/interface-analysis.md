---
title: Interface Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology, Integrative Structural and Computational Biology]
last_verified: 2026-08-01
summary: "Map protein-protein and protein-ligand interfaces with Bio.PDB — contact residues, buried surface area, and telling a real interface from crystal packing"
verification: works
verified_on: 2026-08-03
reviewed_on: 2026-08-03
security: cleared
security_on: 2026-08-03
security_note: "GPTomics/bioSkills root LICENSE confirmed MIT this run, not archived, 1.1k stars, skill dir current"
---

# Interface Analysis (bioSkills)

A Claude Code skill that maps protein–protein and protein–ligand interfaces: which residues are in contact, how much surface each partner buries, and whether the interface is biological or a crystallization artifact.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — Biopython, NumPy and the optional FreeSASA are separately installed OSS; PDBePISA is a free EBI web service |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |
| **Verified** | works · 2026-08-03 |
| **Security** | cleared · 2026-08-03 — GPTomics/bioSkills MIT confirmed, provenance matches, no advisories |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "structural-biology"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/structural-biology/interface-analysis ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone).

## What it does

Walks the interface calculation while forcing the two decisions people usually skip — which cutoff, and which assembly:

- **Cutoff choice, stated explicitly** — heavy-atom 4–5 Å for van der Waals contact, Cα–Cα 8 Å for a topological definition, 3.5–4.0 Å for hydrogen bonds and salt bridges. The skill requires the rationale to be recorded, because the residue list changes with the cutoff.
- **Contacts** — `NeighborSearch` over non-hydrogen atoms, collecting cross-chain pairs.
- **Buried surface area** — a contact list is not an interface: SASA is computed with `ShrakeRupley` on the complex and on each isolated chain at an identical probe radius (1.4 Å default), then BSA = SASA(A) + SASA(B) − SASA(complex), halved for per-partner area. FreeSASA 2.2+ is an optional Lee–Richards alternative.
- **Biology vs crystal packing** — cross-checks BSA magnitude, hydrogen bonding, interface conservation and the PDBePISA complexation-significance score, and pushes for corroboration from solution data before calling an interface real.
- **Assembly discipline** — computes on the biological assembly, not the asymmetric unit, which is the single most common source of spurious interfaces.
- **Applications** — ligand-contact residues and antibody/antigen epitope residues fall out of the same contact machinery.
- **Components** — Bio.PDB (primary), Biopython 1.83+, NumPy 1.26+, FreeSASA 2.2+ (optional), PDBePISA (external web service, no local binding).

**Primary use cases**: protein–protein interface mapping, epitope residue identification, ligand contact footprints, screening out crystal-packing contacts.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-structural-biology-interface-analysis`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/interface-analysis`. PDBePISA has no local Python binding — its complexation-significance score is read from the web service, so that step is manual or scripted against the EBI endpoint. Complements the catalogued [PDBe](pdbe.html) and [RCSB PDB](pdb.html) entries for fetching biological assemblies, [Complex Portal](complex-portal.html) and [IntAct](intact.html) for orthogonal interaction evidence, and the [Epitope Prediction](epitope-prediction.html) skill for the immunology case. Upstream directory: `structural-biology/interface-analysis`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`structural-biology/interface-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/interface-analysis/SKILL.md)
- [PDBePISA](https://www.ebi.ac.uk/pdbe/pisa/)
- [Biopython `Bio.PDB.SASA` (ShrakeRupley)](https://biopython.org/docs/latest/api/Bio.PDB.SASA.html)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=interface-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Finterface-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
