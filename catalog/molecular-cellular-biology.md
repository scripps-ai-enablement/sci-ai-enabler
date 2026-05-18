# Molecular and Cellular Biology

> AI ecosystem components for genomics, transcriptomics, single-cell analysis, gene regulation, CRISPR design, cell imaging, and other molecular- and cell-scale biology applications.

_Last updated: 2026-05-18_

## Entries

### Scanpy

- **Type**: Library
- **Supplier**: scverse consortium (fiscally sponsored by NumFOCUS) ([scverse.org](https://scverse.org/))
- **Availability**: GA (1.12.1, April 2026)
- **Pricing**: Free / OSS (BSD-3-Clause)
- **Capabilities**: Read/Write — single-cell preprocessing, dimensionality reduction, clustering, trajectory inference, differential expression
- **Primary use cases**: Single-cell RNA-seq analysis at scale (>100M cells), AnnData-based pipelines
- **Benchmarks**: Wolf et al., _Genome Biology_ (2018) — original benchmarking; widely adopted as community reference
- **Installation**: `pip install scanpy` or `conda install -c conda-forge scanpy`
- **Integration notes**: Python ≥3.12 from 1.12.x; Dask backend supports out-of-core datasets; optional extras (leiden, harmony, scrublet, scanorama, rapids)
- **Sources**: [GitHub](https://github.com/scverse/scanpy), [Docs](https://scanpy.readthedocs.io/), [PyPI](https://pypi.org/project/scanpy/)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

### CZ CELLxGENE Discover Census

- **Type**: Hosted service + Library
- **Supplier**: Chan Zuckerberg Initiative ([cziscience.com](https://cellxgene.cziscience.com/))
- **Availability**: GA; long-term-support releases every 6 months since May 2023
- **Pricing**: Free / OSS (MIT for client libraries); data hosted gratis on AWS Open Data
- **Capabilities**: Read-only — query standardized single-cell corpus (>65M cells, 900+ datasets) via Python or R
- **Primary use cases**: Cross-dataset single-cell exploration, atlas building, ML data loaders for foundation-model training
- **Benchmarks**: CZ CELLxGENE Discover, _Nucleic Acids Research_ 53(D1):D886 (2025)
- **Installation**: `pip install cellxgene-census` (Python) or `install.packages("cellxgene.census")` (R, via R-universe)
- **Integration notes**: TileDB-SOMA backend, streamable to AnnData / Seurat / SingleCellExperiment / PyTorch DataLoader
- **Sources**: [Docs](https://chanzuckerberg.github.io/cellxgene-census/), [GitHub](https://github.com/chanzuckerberg/cellxgene-census), [AWS Open Data](https://registry.opendata.aws/czi-cellxgene-census/)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

## Flagged for review

_None._

## Recently surfaced

- **Scanpy** (added 2026-05-18) — scverse single-cell analysis toolkit.
- **CZ CELLxGENE Discover Census** (added 2026-05-18) — standardized cross-dataset single-cell API.
