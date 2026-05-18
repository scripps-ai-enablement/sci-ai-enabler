# Chemistry

> AI ecosystem components focused on cheminformatics, computational chemistry, chemical structure handling, reaction prediction, retrosynthesis, and chemistry-aware language interfaces.

_Last updated: 2026-05-18_

## Entries

### RDKit

- **Type**: Library
- **Supplier**: RDKit open-source project ([rdkit.org](https://www.rdkit.org/))
- **Availability**: GA
- **Pricing**: Free / OSS (BSD-3-Clause)
- **Capabilities**: Read/Write — molecule parsing, descriptors, fingerprints, 2D/3D coordinate generation, substructure search, reaction handling
- **Primary use cases**: Cheminformatics pipelines, descriptor/fingerprint computation, structure standardisation
- **Benchmarks**: None published; widely used as reference toolkit in cheminformatics literature
- **Installation**: `pip install rdkit` or `conda install -c conda-forge rdkit`
- **Integration notes**: Pure-Python API over C++ core; C++20 required to build from source since 2025.03 release; broad downstream ecosystem (DeepChem, ChemCrow, etc.)
- **Sources**: [GitHub](https://github.com/rdkit/rdkit), [Install docs](https://www.rdkit.org/docs/Install.html), [PyPI](https://pypi.org/project/rdkit/)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

### DeepChem

- **Type**: Library
- **Supplier**: DeepChem project ([deepchem.io](https://deepchem.io/)) ([GitHub org](https://github.com/deepchem))
- **Availability**: GA
- **Pricing**: Free / OSS (MIT)
- **Capabilities**: Read/Write — featurization, model training, and evaluation for molecules, materials, and biology
- **Primary use cases**: Property prediction, generative chemistry baselines, MoleculeNet benchmarking
- **Benchmarks**: MoleculeNet (curated by the project) — see repository documentation
- **Installation**: `pip install deepchem`
- **Integration notes**: Optional TensorFlow, PyTorch, or JAX backends installed separately; JAX extras unsupported on Windows
- **Sources**: [GitHub](https://github.com/deepchem/deepchem), [PyPI](https://pypi.org/project/deepchem/), [Docs](https://deepchem.readthedocs.io/en/latest/get_started/installation.html)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

### ChemCrow

- **Type**: Agent
- **Supplier**: White Lab, University of Rochester / EPFL ([repo](https://github.com/ur-whitelab/chemcrow-public))
- **Availability**: GA (public subset)
- **Pricing**: Free / OSS (MIT); requires user-supplied OpenAI and optional RXN4Chem / SerpAPI keys
- **Capabilities**: Read/Write — LangChain agent orchestrating RDKit, paper-qa, PubChem, RXN4Chem and other chemistry tools
- **Primary use cases**: Organic synthesis planning, retrosynthesis queries, chemistry Q&A
- **Benchmarks**: Bran et al., _Nature Machine Intelligence_ (2024) — agent evaluations on chemistry tasks; public repo notes some tools omitted vs. paper
- **Installation**: `pip install chemcrow`
- **Integration notes**: Python >=3.9, <3.12; default retrosynthesis path calls RXN4Chem API; optional self-hosted Docker route via `local_rxn=True`
- **Sources**: [GitHub](https://github.com/ur-whitelab/chemcrow-public), [Paper](https://www.nature.com/articles/s42256-024-00832-8), [arXiv](https://arxiv.org/abs/2304.05376)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

## Flagged for review

_None._

## Recently surfaced

- **RDKit** (added 2026-05-18) — core cheminformatics library, BSD-3-Clause.
- **DeepChem** (added 2026-05-18) — deep-learning toolkit for chemistry and materials, MIT.
- **ChemCrow** (added 2026-05-18) — LangChain chemistry agent from the White lab.
