---
title: Build a target dossier from gene name to structure to cancer dependency
parent: All recipes
grand_parent: Recipes
nav_order: 1
problem_class: Knowledge synthesis
subject_areas: [Molecular and Cellular Biology, Drug Repurposing and Discovery, Translational Medicine]
evidence_level: Proposed
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-21
summary: Combine the Open Targets plugin, UniProt MCP, AlphaFold MCP, and the DepMap skill to produce a one-page dossier on a candidate gene — disease evidence, protein annotation, predicted structure, and cancer-cell-line essentiality.
---

# Build a target dossier from gene name to structure to cancer dependency

For a candidate gene, return one page of evidence: disease associations and tractability from Open Targets, protein annotation and PTMs from UniProt, an AlphaFold predicted structure with confidence regions flagged, and CRISPR essentiality plus drug-sensitivity context from DepMap.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Molecular and Cellular Biology, Drug Repurposing and Discovery, Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Target dossiers are the bread-and-butter of early discovery and translational research. A wet-lab biologist hears a gene name in a seminar, or a computational biologist's pipeline surfaces a new hit, and the next question is always the same: *what do we already know?* That means stitching together Open Targets (disease evidence, tractability, mechanism), UniProt (sequence, domains, PTMs, subcellular localization), AlphaFold (predicted structure, low-confidence loops to avoid in modelling), and DepMap (CRISPR essentiality across cancer cell lines, optional drug-sensitivity context). Each lookup is fast on its own; the cost is context-switching across four portals and copy-pasting evidence into a doc. Solved looks like: one prompt, one page of cited evidence, in under five minutes.

## Recommended approach

1. **Install the four components.**

   ```
   /plugin marketplace add anthropics/life-sciences
   /plugin install open-targets@life-sciences
   /plugin marketplace add K-Dense-AI/claude-scientific-skills
   /plugin install gget@claude-scientific-skills
   /plugin install depmap@claude-scientific-skills
   ```

   Add the UniProt and AlphaFold MCP servers per their catalog pages — both are stdio Node servers, no auth needed.

2. **Drive the dossier with a single multi-step prompt.** A minimal version:

   ```
   Build a one-page target dossier for STK11. Use:
   - open-targets: top 5 disease associations by association score,
     plus tractability evidence (clinical compounds, antibodies, small
     molecules).
   - uniprot: canonical isoform, domain architecture, PTMs,
     subcellular localization, key paralogs.
   - alphafold: predicted full-length structure; flag any region with
     pLDDT < 70 as low-confidence.
   - depmap: CRISPR essentiality (Chronos) summary across all
     lineages and any lineage where the gene is selectively essential.
   Cite each fact with the source database and an accession or query.
   Render as a single Markdown page under dossiers/STK11.md.
   ```

3. **Sanity-check the cross-references.** UniProt's accession should match the gene symbol Open Targets used; AlphaFold's structure should be keyed on that same UniProt accession; DepMap should use the HUGO gene symbol or Entrez ID. Mismatches usually mean the gene has paralogs (e.g., the GAPDH / GAPDHS family) — re-prompt with the explicit accession.

4. **Iterate.** Once the first dossier is right, save the prompt as a slash command (e.g., `/dossier`) and parameterize on the gene symbol. The same prompt will work for any future gene without re-explaining the structure.

## Why this assembly

Rung 3 of the simplicity ladder. The problem genuinely requires four heterogeneous data sources — disease evidence, protein annotation, structure, and dependency. No single MCP covers all four. A toolbelt of four read-only components is still well within the rung-3 budget (≤ 3 tightly-coupled components is the soft target; here Open Targets + UniProt + AlphaFold + DepMap is four loosely-coupled lookups orchestrated by a single prompt, which the agent loop handles cleanly). Escalating to an autonomous-science system (Biomni) would work but adds loop overhead with no extra capability — the dossier is a knowledge-synthesis problem, not a hypothesis-generation problem.

## Availability

Fully open. Open Targets data is CC0; UniProt, AlphaFold, and DepMap are free for academic use. All four MCP/skill components are OSS. No subscription or institutional account is required for the public data shown here. (DepMap downloads can be hundreds of MB on first run; cache locally.)

## Compute requirements

Laptop-sufficient. All four components are read-only API or file lookups; the only heavy step is the initial DepMap data download (~200 MB for the standard files), cached after first use. No GPU needed.

## Evidence

Proposed. No published end-to-end benchmark of this exact four-component assembly is known. The closest documented analogue is the Biomni paper's case studies, where the same agent integrates dozens of biomedical databases (including Open Targets, UniProt-class annotation, and AlphaFold) to answer multi-step biomedical questions and matches expert performance on LAB-Bench DbQA (74.4% vs 74.7% human experts, [Huang et al., 2025](https://doi.org/10.1101/2025.05.30.656746)). Each component in this recipe has independent evidence (Open Targets is the consortium-maintained reference for target-disease associations; UniProt is the canonical protein annotation; AlphaFold confidence-based filtering is standard practice; DepMap essentiality scoring follows [Behan et al. 2019](https://pubmed.ncbi.nlm.nih.gov/30971826/) and [Dempster et al. 2021](https://pubmed.ncbi.nlm.nih.gov/34349281/)). The composition has not been benchmarked.

## Alternatives considered

- **gget alone.** The [gget skill](../../catalog/tools/gget.html) covers Ensembl, UniProt, and PDB lookups in one interface. Reach for gget when the dossier is gene-and-protein-centric only and you don't need DepMap dependencies or Open Targets disease evidence. Cheaper but less complete.
- **Open Targets alone.** Open Targets exposes a lot through GraphQL, including some of the cross-reference data UniProt provides. Reach for Open-Targets-only when target-disease evidence is the primary question and structure/dependency are nice-to-have.
- **Biomni.** An autonomous-science system that already has Open Targets, UniProt-class annotation, AlphaFold, and DepMap-style data wired in. Reach for Biomni when the dossier is one step of a larger autonomous pipeline (e.g., generate target list → build dossiers → propose experiments). For a one-shot dossier, the rung-3 toolbelt is simpler and more transparent.

## See also

- [Open Targets Plugin](../../catalog/tools/open-targets.html)
- [UniProt MCP Server](../../catalog/tools/uniprot.html)
- [AlphaFold MCP Server](../../catalog/tools/alphafold.html)
- [DepMap (Claude Skill)](../../catalog/tools/depmap.html)
- [gget (Claude Skill)](../../catalog/tools/gget.html) — lower-rung alternative when DepMap and Open Targets are not needed.
- [Biomni](../../autonomous-science/systems/biomni.html) — the autonomous-science option one rung up.

## Sources

- [Open Targets Platform MCP (official blog post)](https://blog.opentargets.org/official-open-targets-mcp/) — published 2026-04 release 2026.03.1; verified 2026-05-21 (this run).
- [`Augmented-Nature/UniProt-MCP-Server`](https://github.com/Augmented-Nature/UniProt-MCP-Server) — verified 2026-05-21 (this run).
- [`Augmented-Nature/AlphaFold-MCP-Server`](https://github.com/Augmented-Nature/AlphaFold-MCP-Server) — verified 2026-05-21 (this run).
- [DepMap skill (`SKILL.md`)](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/depmap/SKILL.md) — last updated 2025–2026; verified 2026-05-21 (this run).
- [Huang et al., "Biomni: A General-Purpose Biomedical AI Agent," *bioRxiv*](https://doi.org/10.1101/2025.05.30.656746) — published 2025-05; closest analogous benchmark.

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=build-target-dossier&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fbuild-target-dossier.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
