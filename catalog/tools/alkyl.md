---
title: ALKYL
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Kyllian de Vos (community)
availability: Beta
tool_categories: [Chemistry, Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-08-15
summary: Claude Code plugin bundling 27 computational-chemistry skills — RDKit, docking, MD, quantum chemistry, free energy, generative design — plus four keyless MCP servers.
---

# ALKYL

Community Claude Code plugin that turns a Claude Code session into a computational-chemistry workbench: 27 description-activated skills spanning cheminformatics, docking, molecular dynamics, quantum chemistry, free-energy methods and generative design, backed by 22 standalone RDKit-based Python scripts.

| | |
|---|---|
| **Type** | Claude Code Plugin (skills + bundled MCP servers) |
| **Supplier** | [Kyllian de Vos](https://github.com/Kdevos12/ALKYL) (community project) |
| **Availability** | Beta — `plugin.json` declares v1.0.0; source-only install, 6 stars, last pushed 2026-03-15 |
| **Pricing** | Free / OSS (MIT, confirmed via the GitHub license API). The optional external engines carry their own terms — xTB and GROMACS are free, ORCA is free for academic use after registration, MODELLER requires a licence key. |
| **Capabilities** | Read/Write — the bundled scripts read and write structure, descriptor and report files on your machine |

## How to install

Requires Claude Code and Python 3.9+. The repository's default branch is `master`.

```
git clone https://github.com/Kdevos12/ALKYL
cd ALKYL
bash alkyl.sh install
```

**The upstream README shows the clone URL as `https://github.com/YOUR_USERNAME/alkyl` — that is a placeholder and will fail.** Use the URL above; note the directory it creates is `ALKYL`, capitalised, not `alkyl`.

`bash alkyl.sh install` appends an ALKYL context block to your global `~/.claude/CLAUDE.md`, delimited by `<!-- ALKYL-START -->` / `<!-- ALKYL-END -->` markers. Re-running it replaces the old block cleanly rather than duplicating it.

If you want the 22 standalone scripts (or to run the test suite), create the Python environment as well. This step is optional — the skills themselves load without it:

```
bash alkyl.sh venv
bash alkyl.sh status
```

`bash alkyl.sh venv` creates a `.venv/` inside the clone containing RDKit and pytest. `bash alkyl.sh status` prints what is currently installed and is a one-shot check, not a service to leave running.

To remove the plugin:

```
bash alkyl.sh uninstall
```

Optional Perplexity literature search — only if you hold a Perplexity API key (replace `pplx-YOUR_KEY_HERE` with your own key):

```
bash alkyl.sh setup-key perplexity pplx-YOUR_KEY_HERE
```

**There is no marketplace install path.** The repository ships `.claude-plugin/plugin.json` but **no `marketplace.json`**, so `/plugin marketplace add Kdevos12/ALKYL` will not resolve. The clone-and-run-`alkyl.sh` path above is the only documented install.

**Claude Desktop is not supported.** ALKYL installs by writing to `~/.claude/CLAUDE.md` and shells out to local Python scripts, both of which are Claude Code mechanisms.

## What it does

Twenty-seven skills under `skills/`, grouped by the area they cover:

- **Cheminformatics** — `rdkit`, `openbabel`, `daylight-theory` (SMILES/SMARTS semantics), `chem-brainstorm`, `synkit`
- **Molecular dynamics and structure** — `ase`, `mdanalysis`, `force-fields`, `coarse-grained`, `homology-modeling`
- **Quantum chemistry** — `qm-dft`, `organic-mechanisms`
- **Drug discovery** — `docking`, `fbdd` (fragment-based design), `free-energy`, `binding-kinetics`, `pharmacophore`
- **Molecular design and ML** — `generative-design`, `mmpa` (matched molecular pairs), `uncertainty-qsar`, `active-learning`, `deepchem`, `torchdrug`, `pepflex`
- **Visualisation and utilities** — `py3Dmol`, `lit-rescue`, `nextflow`

Twenty-two standalone Python scripts under `scripts/` cover format conversion, property and pKa calculation, 3D embedding, scaffold and R-group decomposition, tautomer and library enumeration, similarity clustering, diversity selection, substructure filtering, ADMET estimation and lead-likeness scoring.

The plugin also registers four MCP servers that need no API key: bioRxiv, ChEMBL, ClinicalTrials.gov and PubMed.

**Primary use cases**: Exploratory cheminformatics on SMILES sets, setting up docking and MD runs, quantum-chemistry and mechanism reasoning, hit-to-lead triage and generative design.

## Notes

**The clone is the installation.** Skills are *not* copied into `~/.claude/skills/`; they stay in the cloned repository and are referenced from the block written into `~/.claude/CLAUDE.md`. Moving, renaming or deleting the clone after install will break the skills. Clone it somewhere permanent, not a temporary directory.

Skills are description-activated — describe the chemistry task in plain language rather than looking for slash commands.

`plugin.json` advertises "23 domain skills" while `skills/` actually contains 27 directories; the upstream README's grouped list also merges `torchdrug` and `pepflex` into a single entry. The 27 directory names above were read from the repository.

The four bundled MCP servers overlap literature and database tools already in this catalog — see [ChEMBL](chembl.html) and [PubMed](pubmed.html), both also available independently. If you already have those registered, expect duplicate tool surfaces in the same session. **Unverified —** ALKYL's own bioRxiv and ClinicalTrials.gov servers were not exercised for this entry; note that the separate `biorxiv@life-sciences` and `clinical-trials@life-sciences` plugins have an unreachable backing host, so do not assume these four are interchangeable with the Anthropic-marketplace versions.

Skills are prompt-level guidance plus scripts, not solvers. The heavy engines — ORCA, xTB, GROMACS, OpenMM, MODELLER, AutoDock Vina — are **optional and not installed for you**; a skill that needs one will fail until you install it separately and put it on `PATH`. Only RDKit arrives with `bash alkyl.sh venv`.

Small single-maintainer project (42 commits, 6 stars, one open issue) with no releases and no tests documented as passing in CI. Read the skill text before trusting a numerical result — in particular the ADMET and pKa scripts, which are estimators rather than validated models.

Writing to the global `~/.claude/CLAUDE.md` means the chemistry context block is loaded in **every** Claude Code session on the machine, not just chemistry projects. Run `bash alkyl.sh uninstall` if that becomes noisy.

For a server that actually executes simulations rather than guiding them, see [ChemGraph](chemgraph.html); for input-deck preparation alone, see [XTB MCP Server](xtb-mcp-server.html).

## Sources

- [`Kdevos12/ALKYL`](https://github.com/Kdevos12/ALKYL)
- [`.claude-plugin/plugin.json`](https://github.com/Kdevos12/ALKYL/blob/master/.claude-plugin/plugin.json)
- [`skills/` directory listing](https://github.com/Kdevos12/ALKYL/tree/master/skills)
- [GitHub repository metadata API (licence, default branch, last push)](https://api.github.com/repos/Kdevos12/ALKYL)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=alkyl&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Falkyl.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
