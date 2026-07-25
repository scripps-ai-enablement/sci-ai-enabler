---
title: Build a protein interaction network and rank hub genes
parent: All recipes
grand_parent: Recipes
nav_order: 3
problem_class: Data analysis
subject_areas: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-25
summary: Feed a gene list to the STRING skill to build a PPI network, then rank hub proteins by degree/centrality and detect modules — the canonical "which of these genes matter most" step.
---

# Build a protein interaction network and rank hub genes

Hand Claude a gene list (usually the significant hits from a DE run or a screen), retrieve the STRING protein–protein interaction network, and rank the hub proteins by network centrality — the step that turns a flat list of dozens of genes into a short, defensible shortlist of candidate drivers.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Integrative Structural and Computational Biology, Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have a list of 30–300 genes — differentially expressed genes, a co-expression module, a screen hit set — and you need to know *which* of them sit at the center of the biology rather than at the periphery. The field-standard move is to build the protein–protein interaction (PPI) network among those genes from STRING, then rank proteins by network centrality (degree, betweenness, closeness) to pull out the "hub" proteins, and optionally decompose the network into densely-connected modules. Hub proteins are the recurring output of thousands of "identification of key genes" papers because a highly-connected node is more likely to be a functional driver and a druggable choke point than a leaf node.

Done by hand this is swivel-chairing: paste symbols into the STRING web form, export the edge list, load it into Cytoscape, run the CytoHubba plugin, screenshot the top-10 table. The interpretation at the end is where naïve LLM use fails — a model asked "which of these are important" will confabulate a ranking. Solved looks like: point at a gene-symbol list and species, get a saved edge table, a centrality-ranked hub table, a module assignment, a rendered network figure, and a written summary anchored only to the tabulated numbers — captured as a re-runnable script, not a chat.

## Recommended approach

Rung 2 — one Claude Skill, the [STRING skill](../../catalog/tools/string-database-ppi.html), which calls the STRING REST API locally to fetch the interaction network. The hub ranking and module detection are deterministic graph operations you pin in a small script (`networkx` / `python-igraph`) so the result is reproducible and independent of any web-plugin version.

1. **Install the skill.** Verbatim steps are on the [catalog page](../../catalog/tools/string-database-ppi.html) (clone `jaechang-hits/SciAgent-Skills`, then `/plugin install sciagent-skills`, or copy `skills/systems-biology-multiomics/string-database-ppi` into `~/.claude/skills/`). The skill runs its own Python locally; no API key.

2. **Fetch the network with the skill.** Hand Claude the gene list, the species, and the confidence cutoff:

   ```
   Use the string-database-ppi skill to retrieve the PPI network for
   these human gene symbols at a minimum combined score of 0.7
   (high confidence). Save the full edge list (protein_a, protein_b,
   combined_score) to results/string_edges.tsv and report how many of
   my input genes mapped to STRING identifiers and how many were dropped.

   Genes: <paste symbols>
   ```

   State the species (`9606` for human) and the score cutoff explicitly — the default 0.4 (medium) inflates the network with speculative edges; 0.7+ is the defensible choice for a hub analysis.

3. **Author a re-runnable hub-ranking script.** Capture the graph analysis as a committed script rather than an ad-hoc chat. Ask Claude to write `rank_hubs.py`:

   ```
   Write rank_hubs.py that reads results/string_edges.tsv into a networkx
   graph and:
     1. Computes per-node degree, betweenness, and closeness centrality.
     2. Ranks nodes by degree (the CytoHubba "Degree" method), writes
        results/hub_genes.csv (gene, degree, betweenness, closeness, rank).
     3. Detects modules with the Louvain method; adds a module column.
     4. Renders results/ppi_network.png (nodes sized by degree, coloured
        by module) and writes the top-15 hubs to results/top_hubs.csv.
   Pin every library in requirements.txt.
   ```

   Run it, then invoke as a project command if you will reuse it across gene lists.

4. **Synthesize from the saved tables only.** Have Claude write the interpretation citing rows in the CSVs:

   ```
   From results/hub_genes.csv and results/top_hubs.csv, summarize the
   network. Name the top hubs by degree, note which module each falls in,
   and flag any hub that is also high in betweenness (a bottleneck).
   Do not claim biological importance for any gene not in the tables, and
   do not infer function beyond what the centrality numbers support.
   ```

5. **Record provenance.** The saved edge list, hub CSVs, and PNG are the audit trail. Have Claude write `results/provenance.json`: the STRING skill commit, the **STRING database version** and query date (STRING is versioned — record it, the network changes between releases), the species and score cutoff, the input gene-list sha256, library versions, and the model/agent identity. See the [reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide.

The durable artifact is the committed `rank_hubs.py`, the pinned `requirements.txt`, and the saved `results/*` (edge list, hub CSVs, network PNG, provenance JSON).

## Why this assembly

Rung 2, and it stops here. One skill fetches the network; the ranking and module detection are deterministic graph math that belongs in a pinned script for auditability. Rung 1 (plain Claude Code) can't reach the STRING API or compute centralities reproducibly. A rung-3 toolbelt buys nothing — a single query plus one graph-analysis script fully covers the problem — and no autonomous system is warranted for a deterministic network operation. The one honest constraint is that STRING edges are *predicted/aggregated* associations, not all physical interactions; the recipe pins the confidence cutoff and database version so that caveat is visible rather than silent.

## Availability

Fully open. The STRING skill is CC-BY-4.0 (code) and queries the public STRING REST API (data CC-BY-4.0) with no key. `networkx`, `python-igraph`, and `matplotlib` are open-source. No subscription, institutional agreement, or data-residency concern for public gene symbols.

## Compute requirements

Laptop. A STRING query for a few hundred genes returns in seconds over the network; centrality and Louvain on a graph of hundreds of nodes and a few thousand edges is instantaneous. Outputs are small (a TSV, two CSVs, a PNG). No GPU, no local database download.

## Evidence

`Reported`. The STRING-PPI → centrality-hub-ranking workflow is one of the most heavily documented analysis patterns in the systems-biology literature — thousands of "identification of key/hub genes" studies run exactly this chain (DE genes → STRING PPI → CytoHubba/centrality → hub shortlist), e.g. hepatocellular-carcinoma key-gene identification ([Hasan et al., *Sci. Rep.* 2023](https://pubmed.ncbi.nlm.nih.gov/36882493/)), diabetic-foot-ulcer immune hub genes ([Jiang et al., *Int. Immunopharmacol.* 2024](https://pubmed.ncbi.nlm.nih.gov/39079197/)), and osteoporosis PRR hub genes ([Mao et al., *Sci. Rep.* 2025](https://pubmed.ncbi.nlm.nih.gov/40854963/)). The STRING skill itself is part of the BixBench-evaluated SciAgent-Skills collection and is a Claude Science featured connector.

The individual steps carry independent validation (STRING is the field-standard PPI resource; degree centrality is the canonical CytoHubba hub method). No documented attempt of *this exact Claude+STRING-skill composition* is known, so the label is `Reported`, not `Validated`; the recipe's design (fixed high-confidence cutoff, deterministic pinned centrality script) mirrors the published manual workflow. A field report would move it toward `Validated`.

## Alternatives considered

- **[Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) (rung 2).** The complementary "what does this list mean" step — term-overlap enrichment, not network topology. Run enrichment to name the pathways; run this to find the central genes *within* those pathways. They pair naturally: enrichment gives the biology, hub ranking gives the shortlist.
- **[Map a disease to its genes and pathways](map-disease-to-genes-and-pathways.html).** Starts from a *disease* (Open Targets → gene set) rather than a gene list you already have; feed its output gene set into this recipe when you want the network structure among disease genes.
- **Cytoscape + CytoHubba (no LLM).** The manual field standard. Choose it when you need the full interactive-exploration GUI or one of CytoHubba's dozen alternative ranking methods (MCC, MNC, EPC). This recipe wins for the common "rank the hubs and give me a reproducible script" case by removing the GUI round-trip and emitting a committed, re-runnable artifact.
- **Rung 3+ (toolbelt or autonomous system).** Overkill for a single-query-plus-graph-analysis problem.

## See also

- [STRING (Claude Skill)](../../catalog/tools/string-database-ppi.html)
- [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) — term-overlap counterpart on the same gene list.
- [Map a disease to its genes and pathways](map-disease-to-genes-and-pathways.html) — disease-first gene-set source that feeds this recipe.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md)

## Sources

- [`jaechang-hits/SciAgent-Skills` — `string-database-ppi/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/systems-biology-multiomics/string-database-ppi/SKILL.md) — STRING REST query, network retrieval, enrichment; verified 2026-07-25 (this run).
- [Hasan et al., "Differentially expressed discriminative genes and significant meta-hub genes based key genes identification for hepatocellular carcinoma…," *Sci. Rep.* 13:4739 (2023)](https://pubmed.ncbi.nlm.nih.gov/36882493/) — STRING PPI + CytoHubba hub-gene workflow; published 2023.
- [Jiang et al., "Comprehensive transcriptomic analysis of immune-related genes in diabetic foot ulcers…," *Int. Immunopharmacol.* (2024)](https://pubmed.ncbi.nlm.nih.gov/39079197/) — DEGs → STRING PPI → cytoHubba hub genes; published 2024.
- [Mao et al., "Study on differentially expressed genes and pattern recognition receptors in osteoporosis based on bioinformatics analysis," *Sci. Rep.* (2025)](https://pubmed.ncbi.nlm.nih.gov/40854963/) — STRING PPI + CytoHubba six-hub-gene identification; published 2025.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=build-ppi-network-and-rank-hub-genes&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fbuild-ppi-network-and-rank-hub-genes.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
