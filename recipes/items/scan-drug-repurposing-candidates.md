---
title: Scan approved drugs for repurposing candidates against a disease
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Knowledge synthesis
subject_areas: [Drug Repurposing and Discovery, Translational Medicine]
evidence_level: Proposed
complexity: Multi-tool harness
availability: Subscription required
compute_requirements: Laptop
last_verified: 2026-05-24
summary: Given a disease, use Open Targets to rank associated targets, ChEMBL and PubChem for approved-drug bioactivity, and DrugBank for mechanism / indication / interaction context to produce a ranked shortlist of repurposing candidates.
---

# Scan approved drugs for repurposing candidates against a disease

Given a disease name or EFO/MONDO ID, produce a ranked shortlist of approved or late-clinical drugs whose targets are genetically or mechanistically tied to the disease, with potency, indication, and interaction context attached to each candidate.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Drug Repurposing and Discovery, Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | Multi-tool harness |
| **Availability** | Subscription required |
| **Compute** | Laptop |

## Problem

The opening move of a repurposing project is to compress thousands of approved compounds into a handful worth following up. The data needed is well-known — disease-target evidence (genetics, expression, mouse KO, literature), known bioactivity of approved drugs against those targets, off-target and interaction liabilities, and the legal indication landscape — and lives across at least three databases (Open Targets, ChEMBL or PubChem, DrugBank). The cost is not the lookups; it is reconciling identifiers (ENSG vs UniProt vs ChEMBL target ID; DrugBank vs ChEMBL compound ID), filtering for clinical-stage molecules, and writing it up. Solved looks like: one prompt, a 10–20 candidate table with cited evidence per row, in under ten minutes of wall-clock.

## Recommended approach

1. **Install the three components.** Open Targets and ChEMBL come from the same marketplace; DrugBank is a community MCP that needs the user-supplied DrugBank XML (a separate license).

   ```
   /plugin marketplace add anthropics/life-sciences
   /plugin install open-targets@life-sciences
   /plugin install chembl@life-sciences
   ```

   Then install [DrugBank MCP](../../catalog/tools/drugbank.html) per its catalog page (clone, `npm run download:db` with your DrugBank XML, register the stdio server). If your institution does not have a DrugBank licence, substitute the [PubChem MCP](../../catalog/tools/pubchem.html) — you lose mechanism and interaction queries but keep bioactivity and structure.

2. **Drive the scan with a single multi-step prompt.** A minimal version:

   ```
   Find drug-repurposing candidates for idiopathic pulmonary fibrosis (EFO_0000768).

   Use:
   - open-targets: query target-disease associations for EFO_0000768
     ordered by overall association score; return the top 25 targets
     with their ENSG IDs, UniProt accessions, and tractability flags
     (small_molecule, antibody, clinical_compounds).
   - chembl: for each of those 25 targets, call compound_search /
     get_bioactivity to find approved or late-clinical compounds
     (max_phase >= 3) with reported activity (IC50/Ki/Kd < 10 uM).
     Skip endogenous ligands and chemical probes.
   - drugbank: for each surviving compound, pull indication,
     mechanism_of_action, and known drug-drug interactions.

   Render as a Markdown table with one row per (target, compound) pair:
   gene | drug | mechanism | approved indication | pChEMBL | OT
   association score | OT tractability | DDI flags | source IDs.
   Sort by (OT association score desc, pChEMBL desc).
   Cite each row with the Open Targets target ID, ChEMBL ID, and
   DrugBank ID.
   ```

3. **Read the table critically.** A high Open-Targets score + an approved drug whose label is in a totally unrelated indication is the repurposing signal. Same-indication hits are not repurposing (they are confirmation). Filter out endogenous ligands (insulin, EGF, etc.) before showing the table to a clinician — they pass the bioactivity filter but are not deployable drugs.

4. **Spot-check the top three.** For each candidate, paste the (target, drug) pair into a fresh Claude session and ask for the supporting literature (PubMed via the [PubMed MCP](../../catalog/tools/pubmed.html) if installed). If no human-evidence paper exists in the last 10 years, demote.

5. **Save the prompt as a slash command.** Once the scan is right, parameterize on the EFO/MONDO ID — `/repurpose-scan <efo_id>` — and reuse for every new indication.

## Why this assembly

Rung 3 of the simplicity ladder. The scan needs three heterogeneous evidence axes: disease-target ranking (Open Targets), quantitative bioactivity tied to approved compounds (ChEMBL), and indication / mechanism / interaction context for those compounds (DrugBank). No single MCP covers all three end-to-end at the granularity repurposing needs. Open Targets does include a `knownDrugs` block per target, but it surfaces clinical compounds without bioactivity values and without interaction data — that is why ChEMBL and DrugBank earn their seats. Rung 2 (Open Targets alone) under-resolves the candidate shortlist; rung 4 (a full autonomous system like Biomni) is overkill for what is fundamentally a ranked-join across three databases.

## Availability

Subscription required, driven by DrugBank. The DrugBank XML is license-gated — academic licences are typically free but require institutional sign-off; commercial licences are paid. Open Targets and ChEMBL are CC0 / CC-BY-SA-3.0 with no auth. If you cannot get a DrugBank licence, swap in PubChem (`Fully open` substitution but you lose the curated mechanism-of-action and DDI fields). The Anthropic life-sciences marketplace itself is free.

## Compute requirements

Laptop-sufficient. All three components are read-only API or local-SQLite lookups; the DrugBank stdio server uses ~50–100 MB RAM. The orchestration time is dominated by Claude's tool-calling latency — expect 3–10 minutes for a 25-target × 5-compound scan. No GPU.

## Evidence

Proposed. No published end-to-end benchmark of this exact three-MCP composition is known. The closest documented analogue is **DeepDrug** ([Li et al., *Scientific Reports* 2025](https://www.nature.com/articles/s41598-025-85947-7)), which integrates DrugBank (v5.1.10), DrugCentral, ChEMBL (v31), and BindingDB into a signed directed heterogeneous biomedical graph for Alzheimer's drug repurposing — confirming that the database combination *and* the join pattern (target evidence + bioactivity + approved-drug metadata) are the right primitives. DeepDrug returned a five-drug combination (tofacitinib, niraparib, baricitinib, empagliflozin, doxercalciferol) operating across 7,379 drug-target edges. **Robin** ([Ghareeb et al., *Nature* 2026](https://doi.org/10.1038/s41586-026-10652-y)) shows that an LLM-agent system can identify a viable repurposing candidate end-to-end — ripasudil for dry age-related macular degeneration, validated in vitro with a 1.89-fold increase in RPE phagocytosis — though Robin's component stack is FutureHouse-internal (PaperQA2 + Finch), not the open MCPs used here. On the LLM-validation side, **Zunzunegui Sanz et al.** ([bioRxiv 2025-06-13](https://www.biorxiv.org/content/10.1101/2025.06.13.659527v1)) benchmarked four LLMs (GPT-4o, Claude-3, Gemini-2, DeepSeek) on a DREBIOP dataset of pathway-based drug-repurposing cases and reported significantly higher accuracy with structured prompts (p < 0.001) — supporting the structured-prompt approach in step 2. The exact Open-Targets + ChEMBL + DrugBank MCP composition has not been independently benchmarked.

## Alternatives considered

- **Open Targets alone (rung 2).** The Open Targets `knownDrugs` field on each target returns clinical compounds and trial phase already. Reach for this when you only need a candidate list — no potency comparison, no interaction screen. It is the first thing to try if you want to skip DrugBank licensing.
- **DrugBank-only by indication search.** Useful when you already have a candidate drug and want to ask "what else does this hit". Inverts the target-first flow; appropriate when polypharmacology is the question, not target-driven repurposing.
- **Biomni (rung 4).** The Biomni paper ([Huang et al. 2025](https://doi.org/10.1101/2025.05.30.656746)) wires Open Targets, ChEMBL-class bioactivity, and a DrugBank-class drug-knowledge graph into one autonomous agent. Reach for Biomni when the scan is one step inside a larger autonomous loop (e.g., scan → hypothesis → bench experiment → re-scan). For a one-shot repurposing scan against a defined disease, the rung-3 toolbelt is more transparent and easier to audit per row.
- **Robin (rung 4).** Reach for Robin specifically when wet-lab validation and an iterative dry-AMD-style closed loop are part of the scope. Robin is open source but heavier to set up than the three MCPs above.

## See also

- [Open Targets Plugin](../../catalog/tools/open-targets.html)
- [ChEMBL Connector](../../catalog/tools/chembl.html)
- [DrugBank MCP Server](../../catalog/tools/drugbank.html)
- [PubChem MCP Server](../../catalog/tools/pubchem.html) — open substitute when DrugBank is not licensed.
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — drill-down on a single target after the scan narrows it.
- [Biomni](../../autonomous-science/systems/biomni.html) — autonomous-system option one rung up.
- [Robin](../../autonomous-science/systems/robin.html) — autonomous-system with documented repurposing validation (dAMD).

## Sources

- [Li et al., "DeepDrug as an expert guided and AI driven drug repurposing methodology…," *Scientific Reports* 15:2093](https://www.nature.com/articles/s41598-025-85947-7) — published 2025-01-16; verified 2026-05-24 (this run).
- [Ghareeb et al., "A multi-agent system for automating scientific discovery," *Nature*](https://doi.org/10.1038/s41586-026-10652-y) — published 2026-05; verified 2026-05-24 (this run).
- [Zunzunegui Sanz et al., "Accelerating Drug Repurposing with AI…," *bioRxiv*](https://www.biorxiv.org/content/10.1101/2025.06.13.659527v1) — published 2025-06-13; verified 2026-05-24 (this run).
- [Open Targets Platform MCP (official blog post)](https://blog.opentargets.org/official-open-targets-mcp/) — published 2026-04; verified 2026-05-24 (this run).
- [Anthropic — Using the ChEMBL Connector in Claude](https://claude.com/resources/tutorials/using-the-chembl-connector-in-claude) — verified 2026-05-24 (this run).
- [`openpharma-org/drugbank-mcp-server`](https://github.com/openpharma-org/drugbank-mcp-server) — verified 2026-05-24 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=scan-drug-repurposing-candidates&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fscan-drug-repurposing-candidates.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
