# Changelog

A reverse-chronological log of catalog updates produced by the curator agent. The newest entry is at the top.

<!-- Curator appends new dated entries directly below this line. -->

## 2026-05-19

### Surface anthropics/life-sciences marketplace entries (batch 1)

Drew from the `anthropics/life-sciences` marketplace manifest — the highest-yield, pre-validated source for Claude-installable life-science components. Added the three most impactful entries not yet catalogued and stopped at the per-run cap of 3.

#### Added
- **[Chemistry, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine, Drug Repurposing and Discovery] BioRender Connector** — Scientific-illustration MCP / Claude.ai connector launched alongside the Oct 23, 2025 Anthropic × BioRender partnership; relevant across every life-science domain because figure-building is universal ([Anthropic tutorial](https://claude.com/resources/tutorials/using-the-biorender-connector-in-claude), [BusinessWire announcement](https://www.businesswire.com/news/home/20251023858531/en/BioRender-and-Anthropic-Partner-To-Bring-Scientific-Illustrations-to-Claude-For-Life-Sciences)).
- **[Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine, Drug Repurposing and Discovery] 10x Genomics Cloud MCP** — Local MCPB extension distributed by 10x Genomics that lets Claude Code and Claude Desktop drive 10x Cloud single-cell / immune-profiling / Visium / Xenium analyses; available from Oct 20, 2025 ([10x docs](https://www.10xgenomics.com/support/software/cloud-analysis/latest/tutorials/cloud-mcp-server-code)).
- **[Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine, Drug Repurposing and Discovery] single-cell-rna-qc (Claude Skill)** — Anthropic's first published scientific skill; performs scverse MAD-based QC on `.h5ad` and 10x `.h5` inputs ([SKILL.md](https://github.com/anthropics/life-sciences/blob/main/single-cell-rna-qc/SKILL.md), [Anthropic tutorial](https://claude.com/resources/tutorials/how-to-use-the-single-cell-rna-qc-skill-with-claude)).

#### Updated
- **[catalog/README.md]** — Refreshed entry counts (Chemistry → 3, all other categories → 5; distinct tools → 5) and updated cross-cutting-tools example list.

#### Flagged
- _None._

#### Verified (no changes)
- _None — new-surfacing run._

### Deferred — next-run priority

The following candidates were observed in `anthropics/life-sciences` and adjacent sources during this run but deferred to remain within the 3-entry surfacing cap. Pick up next run before re-querying any source.

- **synapse@life-sciences** — Remote MCP server for Sage Bionetworks Synapse; needs verification of auth model and supplier-side docs.
- **wiley-scholar-gateway@life-sciences** — Remote MCP server for Wiley scholarly content; verify subscription/auth requirements.
- **instrument-data-to-allotrope@life-sciences** — Skill that converts lab-instrument data to Allotrope Simple Model; useful in Chemistry and Translational Medicine.
- **nextflow-development@life-sciences** — Skill for running nf-core pipelines (rnaseq, sarek, atacseq) on local or GEO/SRA inputs.
- **scvi-tools@life-sciences** — Skill packaging the scvi-tools deep-learning toolkit for single-cell omics.
- **scientific-problem-selection@life-sciences** — Skill encoding Fischbach & Walsh (Cell 2024) scientific-project framework.

## 2026-05-19

### Enable multi-category entries

Backfilled the new `Categories` field on every existing catalog entry and duplicated each entry block byte-identically into every category file it claims. Both currently-catalogued tools are cross-cutting biomedical research infrastructure and were assigned all seven categories.

#### Updated
- **[All categories] Anthropic PubMed Connector** — Added `Categories: Chemistry | Immunology and Microbiology | Integrative Structural and Computational Biology | Molecular and Cellular Biology | Neuroscience | Translational Medicine | Drug Repurposing and Discovery`. Entry block duplicated into the six non-Translational-Medicine category files.
- **[All categories] BioMCP** — Added `Categories: Chemistry | Immunology and Microbiology | Integrative Structural and Computational Biology | Molecular and Cellular Biology | Neuroscience | Translational Medicine | Drug Repurposing and Discovery` (reflecting that it bundles ClinicalTrials.gov, PubMed, MyVariant.info, and OpenFDA — all relevant to every life-science domain). Entry block duplicated into the six non-Translational-Medicine category files.
- **[catalog/README.md]** — Refreshed entry counts (each category now lists 2 entries; 2 distinct tools across the catalog) and clarified that cross-cutting entries are duplicated across files.
- **[AGENT.md]** — Removed the one-time multi-category backfill subsection now that the backfill has been executed.

#### Added
- **[Chemistry] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced` ([Tutorial](https://claude.com/resources/tutorials/using-the-pubmed-connector-in-claude)).
- **[Chemistry] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced` ([biomcp.org](https://biomcp.org/)).
- **[Immunology and Microbiology] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced`.
- **[Immunology and Microbiology] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced`.
- **[Integrative Structural and Computational Biology] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced`.
- **[Integrative Structural and Computational Biology] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced`.
- **[Molecular and Cellular Biology] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced`.
- **[Molecular and Cellular Biology] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced`.
- **[Neuroscience] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced`.
- **[Neuroscience] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced`.
- **[Drug Repurposing and Discovery] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced`.
- **[Drug Repurposing and Discovery] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced`.

#### Flagged
- _None._

#### Verified (no changes)
- _None — backfill only._

## 2026-05-19

### Scope refocus to Claude-installable components

The catalog scope was narrowed to discrete, installable Claude components (Claude Skills, MCP servers, Claude Code Plugins, Claude.ai Connectors). General-purpose libraries, model weights distributed only as research artifacts, hosted SaaS without a Claude-installable wrapper, and bespoke LangChain-style agents are no longer in scope. The entry schema was migrated to add `Available in` (every supported install path) and `Tools / resources exposed`, and to drop the free-form `Benchmarks` and `Installation` fields. Surviving entries were re-keyed to the new schema; out-of-scope entries were removed (git history preserves them).

### Removed
- **[Chemistry] RDKit** — General-purpose cheminformatics library; no Claude Skill/MCP/Plugin/Connector wrapper.
- **[Chemistry] DeepChem** — General-purpose ML toolkit for chemistry; no Claude-installable wrapper.
- **[Chemistry] ChemCrow** — LangChain bespoke agent, not packaged as a Skill or Plugin.
- **[Structural and Computational Biology] AlphaFold 3** — Model weights + hosted server; no Claude-installable wrapper.
- **[Structural and Computational Biology] Boltz-1 / Boltz-2** — Model weights / research code; no Claude-installable wrapper.
- **[Structural and Computational Biology] Chai-1** — Model weights + hosted SaaS; no Claude-installable wrapper.
- **[Structural and Computational Biology] OpenFold / OpenFold3** — Research code reproductions; no Claude-installable wrapper.
- **[Structural and Computational Biology] ESM-2 / ESMFold** — Model weights distributed as research artifacts; no Claude-installable wrapper.
- **[Structural and Computational Biology] RFdiffusion** — Research-artifact model weights; no Claude-installable wrapper.
- **[Immunology and Microbiology] IgFold** — Research-artifact library; no Claude-installable wrapper.
- **[Molecular and Cellular Biology] Scanpy** — General-purpose single-cell library; no Claude-installable wrapper.
- **[Molecular and Cellular Biology] CZ CELLxGENE Discover Census** — Hosted dataset + client library; no Claude-installable wrapper.
- **[Neuroscience] DeepLabCut** — General-purpose pose-estimation library; no Claude-installable wrapper.
- **[Translational Medicine] Claude for Life Sciences** — Umbrella offering, not a discrete installable component.
- **[Drug Repurposing and Discovery] TxGNN** — Research-artifact model and code; no Claude-installable wrapper.

### Updated
- **[Translational Medicine] Anthropic PubMed Connector** — Re-keyed to new schema with explicit `Available in` (Claude Code plugin marketplace, direct `mcp add`, Claude.ai Healthcare connector) and `Tools / resources exposed`.
- **[Translational Medicine] BioMCP** — Re-keyed to new schema with explicit `Available in` (Claude Code via `uv`, Claude Desktop mcp_config.json) and `Tools / resources exposed`.
- **[AGENT.md]** — Removed the one-time scope-migration subsection now that it has been executed.
- **[catalog/README.md]** — Refreshed entry counts and timestamp; updated schema summary.

### Flagged
- _None._

### Verified (no changes)
- _None — scope migration only._

## 2026-05-18

First substantive curator run — seeded each category with established, primary-source-verifiable entries.

### Added
- **[Chemistry] RDKit** — Core BSD-3-Clause cheminformatics toolkit; latest release 2025.09.x ([GitHub](https://github.com/rdkit/rdkit), [Install docs](https://www.rdkit.org/docs/Install.html))
- **[Chemistry] DeepChem** — MIT-licensed deep-learning toolkit for chemistry and materials ([GitHub](https://github.com/deepchem/deepchem))
- **[Chemistry] ChemCrow** — LangChain chemistry agent (Bran et al., _Nature Machine Intelligence_ 2024) ([GitHub](https://github.com/ur-whitelab/chemcrow-public))
- **[Structural and Computational Biology] AlphaFold 3** — DeepMind biomolecular structure prediction; server GA, code under CC-BY-NC-SA 4.0 ([GitHub](https://github.com/google-deepmind/alphafold3))
- **[Structural and Computational Biology] Boltz-1 / Boltz-2** — MIT-licensed open structure + affinity models (MIT Jameel Clinic) ([GitHub](https://github.com/jwohlwend/boltz))
- **[Structural and Computational Biology] Chai-1** — Chai Discovery multimodal predictor with free web interface ([GitHub](https://github.com/chaidiscovery/chai-lab))
- **[Structural and Computational Biology] OpenFold / OpenFold3** — Apache-2.0 reproductions of AlphaFold 2/3 ([GitHub](https://github.com/aqlaboratory/openfold), [OpenFold3](https://github.com/aqlaboratory/openfold-3))
- **[Structural and Computational Biology] ESM-2 / ESMFold** — Meta FAIR protein language model + folding head ([GitHub](https://github.com/facebookresearch/esm))
- **[Structural and Computational Biology] RFdiffusion** — Baker Lab generative protein design; RFdiffusion3 released Dec 2025 ([GitHub](https://github.com/RosettaCommons/RFdiffusion), [IPD announcement](https://www.ipd.uw.edu/2025/12/rfdiffusion3-now-available/))
- **[Immunology and Microbiology] IgFold** — Gray Lab antibody structure prediction with AntiBERTy embeddings ([GitHub](https://github.com/Graylab/IgFold))
- **[Molecular and Cellular Biology] Scanpy** — scverse single-cell analysis toolkit, BSD-3-Clause, v1.12.1 ([GitHub](https://github.com/scverse/scanpy))
- **[Molecular and Cellular Biology] CZ CELLxGENE Discover Census** — CZI hosted single-cell corpus with Python/R APIs ([Docs](https://chanzuckerberg.github.io/cellxgene-census/))
- **[Neuroscience] DeepLabCut** — Mathis Labs markerless pose estimation; v3.0 PyTorch engine ([GitHub](https://github.com/DeepLabCut/DeepLabCut))
- **[Translational Medicine] Anthropic PubMed Connector** — Official MCP server for NCBI literature ([Tutorial](https://claude.com/resources/tutorials/using-the-pubmed-connector-in-claude))
- **[Translational Medicine] BioMCP** — GenomOncology MIT-licensed MCP server bundling ClinicalTrials.gov, PubMed, MyVariant, OpenFDA ([biomcp.org](https://biomcp.org/))
- **[Translational Medicine] Claude for Life Sciences** — Anthropic life-science offering launched Oct 2025 ([CNBC](https://www.cnbc.com/2025/10/20/anthropic-claude-life-sciences-research-ai.html))
- **[Drug Repurposing and Discovery] TxGNN** — Zitnik Lab zero-shot graph foundation model for drug repurposing (Huang et al., _Nature Medicine_ 2024) ([GitHub](https://github.com/mims-harvard/TxGNN))

### Updated
- **[catalog/README.md]** — Refreshed with current entry counts and freshness timestamp.

### Flagged
- _None._

### Verified (no changes)
- _None — first substantive run._
