# Changelog

A reverse-chronological log of catalog updates produced by the curator agent. The newest entry is at the top.

<!-- Curator appends new dated entries directly below this line. -->

## 2026-05-20

### Surface knowledge-work-plugins bio-research umbrella plugin

Cleared the top Deferred item — `bio-research@anthropics/knowledge-work-plugins` — using the plugin's GitHub README, the parent `knowledge-work-plugins` repo, and the DeepWiki marketplace breakdown as primary sources. It is a pan-life-sciences plugin (literature, single-cell, sequencing, drug discovery, strategy), so tagged `Categories: All` and added to every category index. Also dropped `benchling@life-sciences` from the Deferred list: it was removed from the `anthropics/life-sciences` marketplace because the plugin system does not support tenant-specific URLs (per the [Benchling DeepWiki page](https://deepwiki.com/anthropics/life-sciences/3.6-benchling)); Benchling remains reachable indirectly via the new bio-research umbrella.

### Added
- **bio-research (Claude Code Plugin)** (Categories: All) — Anthropic open-source umbrella plugin in `anthropics/knowledge-work-plugins` bundling 5 analysis skills (Literature Review, Single-Cell Analysis, Sequencing Pipeline, Drug Discovery, Research Strategy) and ~10 MCP connectors (PubMed, BioRender, bioRxiv, ClinicalTrials.gov, ChEMBL, Synapse, Wiley Scholar Gateway, Owkin, Open Targets, Benchling); install via `/plugin marketplace add anthropics/knowledge-work-plugins` then `/plugin install bio-research@knowledge-work-plugins`, then `/start` ([plugin README](https://github.com/anthropics/knowledge-work-plugins/tree/main/bio-research), [DeepWiki](https://deepwiki.com/anthropics/knowledge-work-plugins)).

### Updated
- **[catalog/entries.md]** — New bio-research entry inserted alphabetically between Anthropic PubMed Connector and BioMCP; Recently surfaced refreshed (5-item rolling window: dropped nextflow-development, added bio-research at top); Deferred reshaped to flag individual `knowledge-work-plugins` connectors (bioRxiv, ChEMBL, ClinicalTrials.gov, Owkin, Open Targets) and the K-Dense-AI scientific-skills collection as next-run targets.
- **[catalog/README.md]** — Distinct-tool count 11 → 12; per-category counts incremented by 1 across all seven indices (Chemistry 7 → 8; Structural/Computational and Neuroscience 10 → 11; Immunology, Molecular & Cellular, Drug Discovery, Translational 11 → 12). All-tagged-tool list updated to include bio-research.
- **[All seven category indices]** — One new `bio-research (Claude Code Plugin)` card added per index in the alphabetical slot between Anthropic PubMed Connector and BioMCP.
- **[Deferred list]** — Removed `bio-research@anthropics/knowledge-work-plugins` (surfaced this run); recorded `benchling@life-sciences` as dropped with rationale and DeepWiki citation; added individual bundled connectors and `K-Dense-AI/scientific-agent-skills` as next-run priorities.

### Flagged
- _None._

### Verified (no changes)
- 11 existing entries spot-checked (all carry `Last verified` between 2026-05-19 and 2026-05-20 from recent runs); no field drift on supplier links, availability, or install paths. The bio-research plugin's bundled PubMed/BioRender/Synapse/Wiley connectors corroborate the existing standalone entries for those tools.

## 2026-05-20

### Surface anthropics/life-sciences marketplace entries (batch 4)

Cleared all three remaining `*@life-sciences` candidates from the Deferred list — Synapse, Wiley Scholar Gateway, and scientific-problem-selection — using web search results that cite the `anthropics/life-sciences` marketplace, the Anthropic tutorials, and the DeepWiki marketplace breakdown as primary sources. All three are pan-life-sciences tools and tagged `Categories: All`, so each was added to every category index. Held at three new entries this run (within the soft cap of 5) since each `All`-tagged entry costs 1 entry-block write + 7 card edits = 8 file touches.

### Added
- **Scholar Gateway Connector (Wiley)** (Categories: All) — Wiley remote MCP server / Claude.ai connector providing peer-reviewed scholarly content across 3M+ articles (including 300+ Life Sciences journals covering 900,000+ research articles); hosted at `connector.scholargateway.ai/mcp`, Beta, free Scholar Gateway account required ([Anthropic tutorial](https://claude.com/resources/tutorials/using-the-scholar-gateway-connector-in-claude), [DeepWiki](https://deepwiki.com/anthropics/life-sciences/3.5-wiley-scholar-gateway), [Wiley press release](https://newsroom.wiley.com/press-releases/press-release-details/2025/Wiley-Launches-Interoperable-Platform-to-Power-Scientific-Discovery-in-Worlds-Leading-AI-Technologies/default.aspx)).
- **scientific-problem-selection (Claude Skill)** (Categories: All) — Anthropic skill encoding Fischbach & Walsh's *Cell* (2024) framework for project ideation, risk assessment, troubleshooting stuck projects, and strategic scientific planning ([marketplace](https://github.com/anthropics/life-sciences), [Claude for Life Sciences](https://www.anthropic.com/news/claude-for-life-sciences)).
- **Synapse.org Connector** (Categories: All) — Sage Bionetworks remote MCP server / Claude.ai connector at `mcp.synapse.org/mcp` for discovery, project structure, and metadata retrieval across Synapse-hosted biomedical data; OAuth2 default, free Synapse account required, per-project access controls apply ([Anthropic tutorial](https://claude.com/resources/tutorials/using-the-synapse-org-connector-in-claude), [marketplace](https://github.com/anthropics/life-sciences), [server source](https://github.com/susheel/synapse-mcp)).

### Updated
- **[catalog/entries.md]** — Three new entry blocks inserted alphabetically; Recently surfaced refreshed (5-item rolling window: dropped instrument-data-to-allotrope, BioRender Connector, 10x Genomics Cloud MCP; added Synapse, scientific-problem-selection, Scholar Gateway at top).
- **[catalog/README.md]** — Distinct-tool count 8 → 11; per-category counts incremented by 3 across all seven indices (Chemistry 4 → 7; Structural/Computational and Neuroscience 7 → 10; Immunology, Molecular & Cellular, Drug Discovery, Translational 8 → 11). All-tagged-tool list updated to include Scholar Gateway, Synapse, and scientific-problem-selection.
- **[All seven category indices]** — Three new cards added per index in their alphabetical slots, freshness timestamps bumped.
- **[Deferred list]** — Removed all three surfaced items; `bio-research@anthropics/knowledge-work-plugins` carries forward; added `benchling@life-sciences` (named in Anthropic launch coverage alongside 10x Genomics) as a new next-run priority.

### Flagged
- _None._

### Verified (no changes)
- 8 existing entries spot-checked (all `Last verified: 2026-05-19` from prior runs); no field drift on supplier links, availability, or install paths.

## 2026-05-19

### Surface anthropics/life-sciences marketplace entries (batch 3)

Cleared one more item from the Deferred list — `scvi-tools@life-sciences` — using the `anthropics/life-sciences` marketplace plus the Anthropic tutorial as primary sources. Held to one new entry this run because the tag list expands to six category-card edits (Chemistry excluded — scvi-tools is single-cell omics, not chemistry).

### Added
- **scvi-tools (Claude Skill)** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine) — Anthropic skill bundling deep-learning workflows for scVI, scANVI, totalVI, MultiVI, PeakVI, DestVI, contrastiveVI, sysVI, and veloVI; covers batch correction, semi-supervised cell-type annotation, multi-modal CITE-seq / multiome integration, spatial deconvolution, perturbation analysis, and RNA velocity ([Anthropic tutorial](https://claude.com/resources/tutorials/how-to-use-the-scvi-tools-bioinformatics-skill-bundle-with-claude), [marketplace](https://github.com/anthropics/life-sciences)).

### Updated
- **[catalog/entries.md]** — Promoted scvi-tools from the Deferred list; refreshed Recently surfaced (5-item rolling window: dropped single-cell-rna-qc, added scvi-tools at top).
- **[catalog/README.md]** — Distinct-tool count 7 → 8; per-category counts incremented for the six tagged categories (Immunology, Molecular & Cellular, Drug Discovery, Translational 7 → 8; Structural/Computational and Neuroscience 6 → 7). Chemistry unchanged at 4.
- **[Deferred list]** — Removed `scvi-tools@life-sciences`; remaining items (synapse, wiley-scholar-gateway, scientific-problem-selection, bio-research umbrella) carry forward.

### Flagged
- _None._

### Verified (no changes)
- 7 existing entries spot-checked (all `Last verified: 2026-05-19` from prior runs today); no field drift on supplier links or install paths.

## 2026-05-19

### Surface anthropics/life-sciences marketplace entries (batch 2)

Cleared two items from the previous run's Deferred list using the `anthropics/life-sciences` marketplace as the manifest-driven source. Stayed under the per-run surfacing cap (2 entries this run vs. soft cap of 5) because each new entry's tag list expands into 5–6 category-card edits.

### Added
- **instrument-data-to-allotrope (Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery, Immunology and Microbiology, Molecular and Cellular Biology, Translational Medicine) — Anthropic skill that converts 40+ lab-instrument output formats (PDF, CSV, Excel, TXT) to Allotrope Simple Model JSON / flattened CSV via the `allotropy` library, with PDF-table fallback and ASM validation ([skill listing](https://playbooks.com/skills/anthropics/life-sciences/instrument-data-to-allotrope), [marketplace](https://github.com/anthropics/life-sciences)).
- **nextflow-development (Claude Skill)** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine) — Anthropic prototype skill that runs nf-core `rnaseq` 3.22.2, `sarek` 3.7.1, and `atacseq` 2.1.2 on local FASTQ or GEO/SRA inputs ([skill listing](https://agent-skills.md/skills/anthropics/life-sciences/nextflow-development), [marketplace](https://github.com/anthropics/life-sciences)).

### Updated
- **[catalog/entries.md]** — Promoted both skills from the Deferred list; refreshed Recently surfaced to include them.
- **[catalog/README.md]** — Distinct-tool count 5 → 7; per-category counts incremented (Chemistry 3 → 4; Structural/Computational and Neuroscience 5 → 6; Immunology, Molecular & Cellular, Drug Discovery, and Translational 5 → 7).
- **[Deferred list]** — Removed the two surfaced items; added `bio-research@anthropics/knowledge-work-plugins` (umbrella plugin bundling 10 MCP servers + 6 skills) as a new next-run priority after it was named by both search results.

### Flagged
- _None._

### Verified (no changes)
- 5 existing entries spot-checked (all `Last verified: 2026-05-19` from yesterday's run); no field drift on supplier links or install paths.

## 2026-05-19

### Refactor: entries.md is canonical; category files become tag-filtered indices

Multi-category entries were previously duplicated as full blocks into every named category file. That hit the action's 600-second wall on expansion runs (each pan-life-sciences entry cost ~7 file writes plus drift detection) and forced an artificial "primary category" choice for genuinely cross-cutting tools like PubMed.

Refactored to a single source of truth:

- `catalog/entries.md` now holds every entry's full content block, alphabetically.
- Each `catalog/<area>.md` is a card-based index: brief summary per entry tagged with that category, linking back to `entries.md`.
- The `Categories` field is a tag list (comma-separated), with the literal value `All` allowed for tools applicable across every life-science domain. No notion of a "primary" category.
- Drift detection at run-start is no longer needed — single source of truth, no drift possible.
- Updates to a tool's pricing/availability/etc. are one write to `entries.md`. Card edits in indices are only needed when the card's surface text (name, type, supplier, availability, one-line summary) changes.

This refactor was performed locally rather than by the agent because it's a substantial content migration and the agent's per-run timeouts made it unsafe to run there. AGENT.md was rewritten in the same change to match the new storage model.

#### Removed
- Per-category duplicated copies of the 5 cross-cutting entries (Anthropic PubMed Connector, BioMCP, BioRender Connector, 10x Genomics Cloud MCP, single-cell-rna-qc) — superseded by `entries.md` as canonical store.

#### Added
- **catalog/entries.md** — canonical file with all 5 entries; PubMed / BioMCP / BioRender tagged `All`, 10x Genomics Cloud / single-cell-rna-qc tagged with their explicit 6-category subset.
- Card-based index in each category file linking back to canonical entries.

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
