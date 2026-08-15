---
title: Get balanced reactions and cross-references for a metabolite or EC number
parent: All recipes
grand_parent: Recipes
nav_order: 34
problem_class: Knowledge synthesis
subject_areas: [Chemistry, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: Claude Code alone
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-15
summary: Have Claude Code script the Rhea release files so a metabolite name or EC number returns mass- and charge-balanced reactions with direction and cross-references.
---

# Get balanced reactions and cross-references for a metabolite or EC number

Turn a metabolite name or an EC number into a table of mass- and charge-balanced reactions with an explicit direction, ChEBI participants, and KEGG/MetaCyc/GO cross-references you can paste into a model.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Chemistry, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | Claude Code alone |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You are extending a metabolic model, annotating a metabolomics hit, or writing the pathway paragraph of a paper, and you need the reactions a compound actually participates in — balanced, directional, and cross-referenced to whatever identifier space your pipeline already speaks. The obvious moves both fail quietly. Asking a model from memory returns fluent equations that are frequently unbalanced by a proton or a water. Copying an equation off a pathway map gives you a cartoon with no charge state and no committed direction.

Rhea is the resource that fixes this — it is the enzyme-annotation vocabulary of UniProtKB and an ELIXIR Core Data Resource, and its reactions are chemically balanced for mass and charge at pH 7.3. But three of its modelling conventions bite anyone who queries it casually: reaction participants are the **major microspecies at pH 7.3** (so the ChEBI ID you looked up by name usually is not the one in the reaction), every reaction exists as a **quartet of four IDs** with different directions, and **the left side is not the substrate side**. Solved looks like: a committed script that takes an identifier, applies those three conventions explicitly, and emits reaction, participant, and cross-reference tables stamped with the Rhea release they came from.

## Recommended approach

Rhea and ChEBI are catalogued as [Claude Science connectors](../../catalog/tools/rhea.html) for interactive lookup, but a connector cannot leave a re-runnable artifact behind. For anything that feeds a model, have Claude Code build the artifact against the CC BY 4.0 release files instead.

1. **Pull one release into `data/` and record it.** All files carry the release date; download them once and treat them as a frozen snapshot, not a live service:

   ```
   Download these from https://ftp.expasy.org/databases/rhea/tsv/ into data/,
   then write the sha256 of each file plus the FTP Last-Modified date into
   provenance.json:
     chebi_pH7_3_mapping.tsv  chebiId_name.tsv  rhea-directions.tsv
     rhea-obsoletes.tsv  rhea-chebi-smiles.tsv  rhea-reaction-smiles.tsv
     rhea2ec.tsv  rhea2kegg_reaction.tsv  rhea2metacyc.tsv  rhea2go.tsv
   ```

2. **Resolve the query identifier, then map it to the pH 7.3 form.** This is the step that decides whether you get hits at all. Have the script look the name up in `chebiId_name.tsv`, then pass the ChEBI ID through `chebi_pH7_3_mapping.tsv` and **carry that file's third column (`computation` or `curation`) into the output as a confidence field** — a computed microspecies assignment is a weaker claim than a curated one. Searching Rhea for the neutral form of a polyanion returns nothing, which reads identically to "this compound has no known reactions".

3. **Enumerate the quartet and commit to one direction.** Look the master (undefined-direction) ID up in `rhea-directions.tsv` to get its left-to-right, right-to-left, and bidirectional siblings. Write all four IDs to the output row, and require the script to **fail loudly rather than emit a master ID as a modelling result** — the master's direction is undefined (`<?>`) and is not a stoichiometric statement. `rhea-reaction-smiles.tsv` covers only the LR and RL members, which is a useful forcing function: if you want a machine-readable equation, you must have chosen a direction.

4. **Derive participants and stoichiometry, and label the sides neutrally.** Split each directed reaction SMILES on `>>`, count repeated molecules to recover coefficients, and join each SMILES back to a ChEBI ID via `rhea-chebi-smiles.tsv`. Name the output columns `side_left` / `side_right`, never `substrates` / `products`: Rhea attaches no semantic meaning to the two sides, and the direction ID is the only thing that licenses reading left → right. Note in the provenance that the SMILES files are a beta RDKit derivation of the RXN files.

5. **Join cross-references on `MASTER_ID`, not on your chosen ID.** The `rhea2*.tsv` files carry `RHEA_ID`, `DIRECTION`, `MASTER_ID`, and the external ID, and an external database may have mapped to any member of the quartet. Grouping by `MASTER_ID` and keeping the `DIRECTION` column visible is the difference between a complete cross-reference set and a half-empty one. Expect **many rows per EC number and per compound** — an EC number routinely covers several Rhea reactions — so never reduce to the first hit.

6. **Screen for retirement, then emit.** Check every ID against `rhea-obsoletes.tsv` and mark rather than drop obsolete rows, since old model files and papers cite retired IDs and you want the collision to be visible. Commit `rhea_lookup.py`, `data/` (or its checksums), `reactions.csv`, `participants.csv`, `xrefs.csv`, and `provenance.json`. Any prose you write must cite only what appears in those tables.

The script is stdlib-only — `urllib` and `csv` are enough — so there is no environment to pin beyond the Python version, which belongs in `provenance.json` alongside the release date and the model identity that authored the script. Rhea releases track UniProtKB at roughly eight-week intervals, so a re-run months later against a fresh download will differ; the recorded date and checksums are what make that visible instead of silent.

## Why this assembly

Rung 1. The whole problem is "apply four documented conventions to ten tab-separated files", which is exactly what Claude Code does natively — no Skill, no MCP server, no dependency. Rung 2 would mean the Claude Science Chemistry connector, and that is the right tool for a single question you will not re-run, but it cannot produce the committed script a model build needs, and it puts the pH 7.3 and direction conventions back inside a conversation where they are easy to skip. Escalating further buys nothing: there is no search, no optimization, and no judgment call in this workflow — the hard part is refusing the defaults, and a script is a better place to encode a refusal than a prompt.

## Availability

Fully open. All Rhea data is CC BY 4.0 and downloadable from [`ftp.expasy.org/databases/rhea/`](https://ftp.expasy.org/databases/rhea/) with no account; ChEBI is CC BY 4.0 from EMBL-EBI. Attribution is required if you redistribute. Nothing about your query leaves your machine once the release files are downloaded, so a confidential target list is safe here — in deliberate contrast to the connector path, which sends the compound name to a hosted service. If you use the interactive connector route instead, that needs a Claude.ai plan with Claude Science access.

## Compute requirements

Laptop. The full TSV set is roughly 18 MB compressed, dominated by `rhea-reaction-smiles.tsv` at 11 MB; the download is the slow step. Every join in this recipe is a dictionary lookup over at most ~18,600 reactions and ~15,200 compounds, so the whole script runs in a couple of seconds and well under 1 GB of RAM. No GPU, no network access after step 1.

## Evidence

Proposed. No documented attempt at an LLM-scripted Rhea lookup is known. The grounding is entirely resource-level and strong: Rhea is expert-curated, is the reference vocabulary for enzyme annotation in UniProtKB, and is an ELIXIR Core Data Resource ([Bansal et al., *NAR* 2022](https://doi.org/10.1093/nar/gkab1016)). The four gates above are not invented — each traces to a stated Rhea convention verified this run. The quartet structure (LR/RL/BI/UN, each with its own identifier, mapped in `rhea-directions.tsv`) and the mass-and-charge balance at pH 7.3 are documented Rhea behaviour; so is the statement that neither side carries substrate/product semantics. The cross-reference caveat has a published instance: the UniProt REST service returns more than one Rhea identifier per entry, including undefined-direction and directional IDs together ([Morgat et al., *Bioinformatics* 2020](https://doi.org/10.1093/bioinformatics/btz817)), which is the same many-to-many shape step 5 handles. The closest documented analogous workflow is Rhea's own federated-SPARQL demonstration, which links metabolite annotation through the proteome to the genome ([Lombardot et al., *NAR* 2019](https://doi.org/10.1093/nar/gky876)) — the same joins, driven by hand rather than by an agent.

## Alternatives considered

- **The Claude Science Chemistry connector, interactively.** Reach for [Rhea](../../catalog/tools/rhea.html) and [ChEBI](../../catalog/tools/chebi.html) as connectors when you have one question, want a conversational answer, and will not re-run it. You lose the artifact, and you must apply the pH 7.3 and direction conventions yourself in the prompt.
- **The Rhea SPARQL endpoint** at `sparql.rhea-db.org`. The better choice when your question is a graph query rather than a lookup — "every reaction whose participants include any member of this ChEBI class, federated against UniProt for the enzymes". It is a live service, so pin nothing and record the query date instead.
- **KEGG instead of Rhea.** [KEGG](../../catalog/tools/kegg-database.html) has broader pathway-map coverage and is often what a reviewer recognises, but its equations are not curated to Rhea's mass-and-charge standard and its licensing is more restrictive than CC BY 4.0. Use `rhea2kegg_reaction.tsv` to move between them rather than picking one.
- **Skip the lookup and let a metabolic model supply the stoichiometry.** If you already have a genome-scale model, [predict-gene-knockout-phenotypes-with-fba](predict-gene-knockout-phenotypes-with-fba.html) consumes reactions you never had to source. This recipe is for the case where the reaction you need is missing from that model.

## See also

- [Rhea (Claude Science Connector)](../../catalog/tools/rhea.html)
- [ChEBI (Claude Science Connector)](../../catalog/tools/chebi.html)
- [Predict gene-knockout phenotypes with flux balance analysis](predict-gene-knockout-phenotypes-with-fba.html) — the downstream consumer of this recipe's stoichiometry.
- [Identify an unknown compound from an MS/MS spectrum](identify-unknown-compound-from-msms-spectrum.html) — upstream, when you do not yet know which metabolite you have.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) — the artifact pattern this recipe follows.

## Sources

- [Rhea TSV release directory, `ftp.expasy.org/databases/rhea/tsv/`](https://ftp.expasy.org/databases/rhea/tsv/) — files dated 2026-06-10; fetched 2026-08-15 (this run).
- [Rhea TSV `README.txt`](https://ftp.expasy.org/databases/rhea/tsv/README.txt) — per-file column definitions; fetched 2026-08-15 (this run).
- [Bansal et al., "Rhea, the reaction knowledgebase in 2022," *NAR* 50:D693](https://doi.org/10.1093/nar/gkab1016) — published 2022-01-01; resource reference, UniProtKB adoption, ELIXIR Core Data Resource status.
- [Morgat et al., "Enzyme annotation in UniProtKB using Rhea," *Bioinformatics* 36:1896](https://doi.org/10.1093/bioinformatics/btz817) — published 2020-01-01; multiple Rhea IDs per UniProt entry.
- [Lombardot et al., "Updates in Rhea: SPARQLing biochemical reaction data," *NAR* 47:D596](https://doi.org/10.1093/nar/gky876) — published 2019-01-01; SPARQL endpoint and federated metabolite annotation.
- [Rhea (Claude Science Connector) catalog entry](../../catalog/tools/rhea.html) — catalog `last_verified` 2026-07-17.
- [ChEBI (Claude Science Connector) catalog entry](../../catalog/tools/chebi.html) — catalog `last_verified` 2026-07-17.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=get-balanced-reactions-for-a-metabolite&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fget-balanced-reactions-for-a-metabolite.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
