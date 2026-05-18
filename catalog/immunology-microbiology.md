# Immunology and Microbiology

> AI ecosystem components for immune repertoire analysis, epitope prediction, antibody design, microbial genomics, metagenomics, host-pathogen interaction modeling, and related areas.

_Last updated: 2026-05-18_

## Entries

### IgFold (with AntiBERTy)

- **Type**: Library
- **Supplier**: Gray Lab, Johns Hopkins University ([repo](https://github.com/Graylab/IgFold))
- **Availability**: GA (v0.4.0 current)
- **Pricing**: Free for non-commercial use (including at commercial entities) under the JHU Academic Software License Agreement; commercial use requires contacting JHU Tech Ventures
- **Capabilities**: Read-only — antibody Fv structure prediction and AntiBERTy sequence embeddings
- **Primary use cases**: High-throughput antibody structure prediction, antibody-specific embedding features for downstream ML
- **Benchmarks**: Ruffolo et al., _Nature Communications_ 14:2389 (2023) — similar or better quality than AlphaFold for antibodies in <25 s per structure
- **Installation**: `pip install igfold` (optional PyRosetta or OpenMM for refinement; AbNumber for renumbering)
- **Integration notes**: Pretrained weights downloaded on first run; AntiBERTy trained on 558M sequences from Observed Antibody Space
- **Sources**: [GitHub](https://github.com/Graylab/IgFold), [Paper](https://www.nature.com/articles/s41467-023-38063-x), [PyPI](https://pypi.org/project/igfold/)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

## Flagged for review

_None._

## Recently surfaced

- **IgFold** (added 2026-05-18) — Antibody structure prediction with AntiBERTy embeddings.

## See also

- [Integrative Structural and Computational Biology](structural-computational-biology.md) — RFdiffusion, ESM-2/ESMFold, AlphaFold 3, Chai-1 and Boltz are also used for antibody and pathogen-protein modeling.
