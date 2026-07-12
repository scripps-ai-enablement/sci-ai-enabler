---
title: Find drug-repurposing candidates by walking a biomedical knowledge graph
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Knowledge synthesis
subject_areas: [Drug Repurposing and Discovery, Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-12
summary: Walk PrimeKG offline from a disease through its genes to the drugs that target them, then flag drugs whose current indications are elsewhere as repurposing leads.
---

# Find drug-repurposing candidates by walking a biomedical knowledge graph

For a disease, generate a shortlist of approved drugs mechanistically connected to it through shared genes/proteins — using an offline knowledge-graph walk that surfaces indirect links a target-by-target bioactivity join misses.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Drug Repurposing and Discovery, Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

The classic target-first repurposing scan (rank disease targets, then look up drugs with measured bioactivity against them) is precise but narrow: it only sees drugs whose potency against a *specific* disease gene is already tabulated. A lot of real repurposing signal is one hop further out — a drug hits protein A, protein A physically interacts with protein B, and protein B is the disease gene. That connectivity lives natively in a biomedical knowledge graph (disease→gene→protein-interaction→drug), where it is a graph traversal rather than a database join. A scientist opening a new indication wants a fast, offline first-pass candidate list built from that graph — drugs that are *mechanistically adjacent* to the disease but currently approved for something else. Solved looks like: disease in, a ranked table of graph-connected approved drugs out, each row carrying the path (which gene, which relation) that connects it, produced on a laptop with no network calls and no license gate.

## Recommended approach

1. **Install the PrimeKG skill** ([catalog page](../../catalog/tools/primekg.html)).

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   ```

   Enable the `primekg` skill when prompted. It ships a local CSV knowledge graph (~129k nodes, ~4M edges over 29 relation types) queried with pandas — everything runs offline.

2. **Have Claude author a versioned walk script, not an ad-hoc chat.** The skill exposes three primitives (`search_nodes`, `get_neighbors`, `get_disease_context`); ask Claude to compose them into a committed `kg_repurpose.py`:

   ```
   Using the primekg skill's query functions, write kg_repurpose.py that,
   given a disease name:
     1. search_nodes(name, type="disease") -> resolve to a PrimeKG node id;
        stop and list candidates if the match is ambiguous.
     2. get_neighbors(disease_id) filtered to disease_gene / gwas edges
        -> the disease gene/protein set G.
     3. For each gene in G, get_neighbors(gene) filtered to
        protein_protein edges -> the one-hop-expanded protein set G+
        (keep the hop distance, 0 or 1, per protein).
     4. For each protein in G+, get_neighbors(protein) filtered to
        drug_protein edges -> candidate drugs, recording (drug, via_gene,
        hop_distance, relation).
     5. For each candidate drug, get_neighbors(drug) filtered to
        drug_disease edges -> its current indications.
     6. Drop drugs already indicated for the query disease (those are
        confirmation, not repurposing).
     7. Score each drug = (# distinct disease genes it connects to,
        weighted 1.0 for hop 0 and 0.5 for hop 1); rank descending.
   Write candidates.csv with columns: drug, score, n_direct_genes,
   n_indirect_genes, connecting_genes, current_indications, node_ids.
   ```

   Have Claude pin the environment (`requirements.txt` with the pinned `pandas` version and the skill commit) and keep both `kg_repurpose.py` and `requirements.txt` under version control.

3. **Run it and record provenance.** PrimeKG is a fixed released dataset, but the skill and its CSV snapshot are not byte-pinned by the graph itself. Have the run emit `provenance.json` capturing: the skill commit SHA, the PrimeKG data version/download date, the input disease string and resolved node id, a sha256 of `candidates.csv`, the run date, and the model id. Commit `candidates.csv` and `provenance.json` as the audit trail.

4. **Read the table as leads, not answers.** A high-scoring drug connecting to several disease genes via direct `drug_protein` edges, currently indicated in an unrelated area, is the repurposing signal. Any natural-language write-up must cite only rows in `candidates.csv`. For the top few, confirm with a quantitative bioactivity check (the target-first [repurposing scan](scan-drug-repurposing-candidates.html)) and a literature pass before acting.

5. **Parameterize.** Once correct, wrap the invocation as a slash command — `/kg-repurpose <disease name>` — and reuse across indications.

## Why this assembly

Rung 2 of the simplicity ladder. The entire graph — diseases, genes, protein interactions, drugs, indications — lives inside one skill's local dataset, so a single Skill plus a committed walk script solves it. Rung 1 (Claude Code alone) has no graph to walk and would fabricate connections. Rung 3 (add ChEMBL/DrugBank/Open Targets) buys quantitative bioactivity and licensed indication metadata — that is the separate, `Subscription required` [target-first scan](scan-drug-repurposing-candidates.html); reach for it to *confirm* leads, not to generate them. This recipe deliberately stays at the offline, fully-open, graph-connectivity layer: it is the cheaper, wider-net complement, not a replacement.

## Availability

Fully open. PrimeKG is public research data assembled from 20+ primary sources; the skill is community OSS in the K-Dense `scientific-agent-skills` collection (upstream license not stated — verify before commercial use). No subscription, no institutional account, no network access at run time.

## Compute requirements

Laptop. The graph is a set of CSVs loaded into pandas; a disease→gene→protein→drug walk with one-hop protein expansion for a typical disease (tens of genes, hundreds of expanded proteins) completes in seconds to a couple of minutes and holds the full graph in a few GB of RAM. No GPU. Expect `candidates.csv` to be tens to a few hundred rows before filtering.

## Evidence

Proposed. No documented attempt at *this exact* Claude + PrimeKG-skill graph-walk assembly is known. The closest documented evidence is on the same substrate: **TxGNN**, trained on PrimeKG, is the canonical validated KG repurposing model, and the PrimeKG graph is the field-standard precision-medicine KG. On PrimeKG's ~17,080 diseases and 4M+ relationships, **COMIC** ([Aamer et al., *BMC Bioinformatics* 2026](https://doi.org/10.1186/s12859-025-06337-4)) reported a 9.55% average improvement over prior SOTA and correctly recovered **21 of the 30 most-recent FDA-approved repurposed drug–disease pairs**, demonstrating that PrimeKG's connectivity carries real repurposing signal. **CellAwareGNN** ([Zhang et al., 2026](https://pubmed.ncbi.nlm.nih.gov/42124589/)) reports AUPRC 0.826 for PrimeKG-based drug-indication prediction (TxGNN baseline 0.799) and surfaces interpretable gene-mediated candidates (e.g., ocrelizumab for pemphigus via CD20⁺ B cells). Caveat: those are trained GNN *link-prediction* models; the PrimeKG **skill** only exposes neighbor lookups, so this recipe implements an *interpretable graph-traversal heuristic* over the same edges, not a learned predictor — it will have lower recall than TxGNN-class models and is a lead-generator, not a ranker of record. KG integration also has documented failure modes (disease-node over-merging, sparse cross-ontology coverage; [Hu et al., 2026](https://pubmed.ncbi.nlm.nih.gov/42245041/)), reinforcing step 4's confirm-before-acting discipline.

## Alternatives considered

- **Target-first bioactivity scan** ([Scan approved drugs for repurposing candidates](scan-drug-repurposing-candidates.html), rung 3). Precise, quantitative, and license-gated (DrugBank). Reach for it to confirm the top leads this recipe generates, or when you need measured pChEMBL values and curated interaction data per candidate. This recipe is the wider, offline, no-license first pass.
- **Open Targets prioritization** ([Prioritize targets within a disease](prioritize-targets-within-a-disease.html), rung 2). Answers "which targets" not "which drugs," and needs network access to the Open Targets API. Complementary, not competing.
- **A trained KG model (TxGNN / COMIC / CellAwareGNN).** Higher recall and calibrated ranking, but none is a Claude-installable skill/MCP/plugin today — running them means standing up the GNN yourself outside the cookbook. Reach for them when you need a defensible ranked prediction rather than an interpretable lead list. (Surfaced as a missing component.)
- **Biomni** ([system page](../../autonomous-science/systems/biomni.html), rung 4). Overkill for one-shot candidate generation; reach for it only when the graph walk is one step inside a larger autonomous loop.

## See also

- [PrimeKG (Claude Skill)](../../catalog/tools/primekg.html)
- [Scan approved drugs for repurposing candidates against a disease](scan-drug-repurposing-candidates.html) — the quantitative, target-first confirmation path.
- [Prioritize targets within a disease via Open Targets](prioritize-targets-within-a-disease.html) — target-ranking sibling.
- [Build a target dossier](build-target-dossier.html) — drill-down on a single target once a lead's mechanism is confirmed.
- [Biomni](../../autonomous-science/systems/biomni.html) — autonomous-system option one rung up.

## Sources

- [Aamer et al., "Comic: explainable drug repurposing via contrastive masking for interpretable connections," *BMC Bioinformatics* (2026)](https://doi.org/10.1186/s12859-025-06337-4) — verified 2026-07-12 (this run).
- [Zhang et al., "CellAwareGNN: Single-Cell Enhanced Knowledge Graph Foundation Model for Drug Indication Prediction," PubMed 42124589 (2026)](https://pubmed.ncbi.nlm.nih.gov/42124589/) — verified 2026-07-12 (this run).
- [Hu et al., "Beyond Identifier Matching: … Failure Modes in Biomedical Knowledge Graph Integration," PubMed 42245041 (2026)](https://pubmed.ncbi.nlm.nih.gov/42245041/) — verified 2026-07-12 (this run).
- [`K-Dense-AI/scientific-agent-skills` — `skills/primekg/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/primekg/SKILL.md) — verified 2026-07-12 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=find-repurposing-candidates-in-a-knowledge-graph&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ffind-repurposing-candidates-in-a-knowledge-graph.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
