---
title: Curator state
parent: Catalog
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Molecular Dynamics (Claude Skill)** (added 2026-05-27) — K-Dense skill that runs and analyzes OpenMM-based MD simulations and post-processes trajectories with MDAnalysis (RMSD, RMSF, contact maps, free-energy surfaces) for protein-stability, ligand-binding-pose refinement, and conformational-ensemble work.
- **Glycoengineering (Claude Skill)** (added 2026-05-26) — K-Dense skill for protein-glycosylation analysis: N-glycosylation sequon scanning, O-glycosylation hotspot prediction, and orchestration of NetOGlyc / GlycoShield / GlycoWorkbench for antibody and vaccine design.
- **Datamol (Claude Skill)** (added 2026-05-25) — K-Dense skill wrapping the Datamol RDKit-built library for molecular standardization, transformations, featurization, and parallel processing on large compound libraries.
- **Molfeat (Claude Skill)** (added 2026-05-25) — K-Dense skill wrapping Molfeat — a unified API over 100+ molecular featurizers (classical fingerprints, descriptors, pretrained ChemBERTa / MolBERT / Uni-Mol embeddings).
- **MedChem (Claude Skill)** (added 2026-05-25) — K-Dense skill wrapping MedChem — Lipinski / Veber / Egan / Muegge drug-likeness filters, PAINS / BRENK structural alerts, and synthetic-accessibility scoring on top of RDKit.

## Flagged for review

- **allenbrain-mcp** — upstream license unset; flagged 2026-05-20 before any redistribution.

## Deferred — next-run priority

- **Cortellis Plugin (`anthropics/life-sciences`)** — Clarivate Cortellis drug-pipeline / deals data; standalone marketplace entry beyond `adisinsight`.
- **Medidata Connector (`anthropics/life-sciences`)** — clinical-operations / EDC platform integration; announced Jan 2026 but install path still gated behind Medidata account onboarding.
- **Consensus Plugin (`anthropics/life-sciences`)** — Consensus.app evidence-search connector; verify install path.
- **NPI Registry MCP (Anthropic Healthcare)** — Anthropic-published MCP for NPPES provider lookup; fourth healthcare-marketplace MCP from the 2026-05-23 run, still pending.
- **Cellxgene Census (K-Dense Skill)** — query CZ CELLxGENE Discover census (61M+ cells, 1000+ datasets) via TileDB-SOMA. Strong Molecular & Cellular Biology candidate.
- **scVelo (K-Dense Skill)** — RNA velocity analysis on single-cell data; next Thursday's Molecular & Cellular Biology pass.
- **Arboreto (K-Dense Skill)** — gene regulatory network inference (GRNBoost2, GENIE3) on single-cell expression.
- **DeepChem (K-Dense Skill)** — deep-learning models for ADMET, virtual screening, and molecular property prediction; next Chemistry-focus pass.
- **TorchDrug / PyTDC / DiffDock / PyOpenMS / matchms / cobrapy (K-Dense Skills)** — remaining chemistry-stack siblings, surface incrementally.
- **Retrosynthesis MCP** — no Claude-installable wrapper for AiZynthFinder / ASKCOS / IBM RXN located 2026-05-25; revisit on next Chemistry-focus pass.
- **OpenClaw Medical Skills Library** — 869-skill MIT-licensed collection; treat each individual skill (pharmacovigilance, adverse-event detection, PyHealth) as a separate entry.
- **Ensembl MCP servers** (`munch-group/ensembl-mcp`, `effieklimi/ensembl-mcp-server`) — both early-stage; revisit when one stabilises.
- **UCSC Genome MCP** (`hlydecker/ucsc-genome-mcp`) — 12 tools over the UCSC Genome Browser API.
- **NCBI Datasets MCP** (`Augmented-Nature/NCBI-Datasets-MCP-Server`) — 31 tools over the NCBI Datasets API.
- **OpenFDA MCP** (`Augmented-Nature/OpenFDA-MCP-Server`, `ythalorossy/openfda`) — standalone OpenFDA wrappers.
- **Azure FHIR MCP** (`erikhoward/azure-fhir-mcp-server`) — Azure Health Data Services FHIR adapter.
- **AACT Clinical Trials MCP** (`navisbio/aact_mcp`) — SQL-over-PostgreSQL alternative to the ClinicalTrials.gov v2 API; complementary to the v2-API MCP surfaced 2026-05-23.
- **Augmented-Nature ChEMBL-MCP-Server** — 22-tool community alternative to the official Anthropic ChEMBL connector; useful for users without marketplace access. Deferred because the first-party connector now covers the same surface.
- **IEDB MCP wrapper** — no Claude-installable wrapper for the IEDB Query API located on the 2026-05-26 Immunology pass; the IEDB API exposes ~2.2M epitopes and is a natural MCP candidate. Revisit on next Immunology-focus pass.
- **BCR/TCR repertoire MCP** — no dedicated MCP server for immcantation / VDJdb / McPAS-TCR identified on the 2026-05-26 sweep; awesome-vdj catalogs upstream libraries but no Claude wrapper yet.
- **Adaptyv (K-Dense Skill)** — wraps NetSolP / SoluProt / SolubleMPNN / ESM / ipTM / pSAE for antibody affinity maturation and developability prep; strong Immunology candidate, surface incrementally.
- **MDAnalysis (K-Dense Skill)** — standalone trajectory-analysis sibling to the new `molecular-dynamics` skill; may warrant its own entry once the K-Dense catalog confirms whether `mdanalysis` is a distinct `SKILL.md` directory or only the analysis half of `molecular-dynamics`.
- **Cryo-EM MCP / Skill** — no Claude-installable wrapper for RELION / cryoSPARC / CTFFIND located on the 2026-05-27 Structural pass; revisit on next Integrative Structural and Computational Biology pass.
- **RFdiffusion / ProteinMPNN Claude Skill** — protein-design model wrappers; not yet packaged as a Claude Skill or MCP server on the 2026-05-27 sweep.

## User requests (open)

- [#11 @goodb 2026-05-27] (no trailer emitted; needs curator triage) title="[Tool feedback]" label=claude:tool-feedback

## User requests (closed this run)

_None._
