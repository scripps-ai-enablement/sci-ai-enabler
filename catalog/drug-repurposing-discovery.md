# Drug Repurposing and Discovery

> AI ecosystem components for target identification, virtual screening, lead optimization, ADMET prediction, drug repurposing knowledge graphs, and end-to-end discovery agents.

_Last updated: 2026-05-18_

## Entries

### TxGNN

- **Type**: Library
- **Supplier**: Zitnik Lab, Harvard Medical School ([zitniklab.hms.harvard.edu](https://zitniklab.hms.harvard.edu/projects/TxGNN/))
- **Availability**: GA; companion TxGNN Explorer web app at [txgnn.org](http://txgnn.org)
- **Pricing**: Free / OSS (MIT per repo)
- **Capabilities**: Read-only — graph neural network for zero-shot indication/contraindication prediction across 17,080 diseases and 7,957 therapeutic candidates
- **Primary use cases**: Drug repurposing for rare or under-studied diseases, hypothesis ranking, explainable prediction paths
- **Benchmarks**: Huang et al., _Nature Medicine_ (2024) — vs. 8 baselines, +49.2% accuracy on indications and +35.1% on contraindications under zero-shot evaluation
- **Installation**: Clone `github.com/mims-harvard/TxGNN`; Python 3.8 with DGL 0.5.2 and PyTorch (PyG optional for disease-area splits)
- **Integration notes**: Knowledge graph dataset on Harvard Dataverse (DOI 10.7910/DVN/IXA7BM); Explainer module provides multi-hop rationales
- **Sources**: [GitHub](https://github.com/mims-harvard/TxGNN), [Nature Medicine paper](https://www.nature.com/articles/s41591-024-03233-x), [Project page](https://zitniklab.hms.harvard.edu/projects/TxGNN/)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

## Flagged for review

_None._

## Recently surfaced

- **TxGNN** (added 2026-05-18) — Harvard graph foundation model for zero-shot drug repurposing.

## See also

- [Chemistry](chemistry.md) — DeepChem and ChemCrow support virtual screening and small-molecule property prediction workflows.
- [Integrative Structural and Computational Biology](structural-computational-biology.md) — Boltz-2 and Chai-1 are used for structure-aware screening; RFdiffusion for de novo binder design.
- [Translational Medicine](translational-medicine.md) — BioMCP surfaces ClinicalTrials.gov / OpenFDA data relevant to repositioning.
