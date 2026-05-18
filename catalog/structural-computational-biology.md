# Integrative Structural and Computational Biology

> AI ecosystem components for protein and complex structure prediction, molecular dynamics, integrative modeling, cryo-EM analysis, and computational biology workflows that span structure, sequence, and dynamics.

_Last updated: 2026-05-18_

## Entries

### AlphaFold 3

- **Type**: Hosted service + Library (inference)
- **Supplier**: Google DeepMind / Isomorphic Labs ([deepmind.google](https://deepmind.google/technologies/alphafold/alphafold-server/))
- **Availability**: GA (AlphaFold Server); code at v3.0.2 on GitHub (per release notes 2025)
- **Pricing**: Free for non-commercial use; AlphaFold Server is gratis but rate-limited (20 jobs/day/user reported); model weights require gated request and academic affiliation
- **Capabilities**: Read-only — predicts structures of proteins, nucleic acids, ligands, ions, and PTMs from sequence/specification
- **Primary use cases**: Biomolecular complex structure prediction, hypothesis generation, target characterization
- **Benchmarks**: Abramson et al., _Nature_ (2024) — improved accuracy on protein–ligand, protein–DNA/RNA interactions vs. AlphaFold 2 / RoseTTAFold AA
- **Installation**: AlphaFold Server (web); local: clone `github.com/google-deepmind/alphafold3`, request weights via DeepMind form
- **Integration notes**: Source code under CC-BY-NC-SA 4.0; weights under separate non-commercial terms; v3.0.2 supports NVIDIA Blackwell GPUs; server cannot fold proprietary novel drug-like ligands
- **Sources**: [GitHub](https://github.com/google-deepmind/alphafold3), [Server](https://deepmind.google/technologies/alphafold/alphafold-server/), [License](https://github.com/google-deepmind/alphafold3/blob/main/LICENSE)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

### Boltz-1 / Boltz-2

- **Type**: Library
- **Supplier**: MIT Jameel Clinic (Wohlwend, Corso et al.) ([repo](https://github.com/jwohlwend/boltz))
- **Availability**: GA (Boltz-1, Dec 2024); Boltz-2 released as follow-up foundation model
- **Pricing**: Free / OSS (MIT) — code, weights, training pipeline, and benchmarks
- **Capabilities**: Read-only — biomolecular complex structure prediction; Boltz-2 additionally predicts binding affinities
- **Primary use cases**: AlphaFold 3-class structure prediction with commercial-friendly licensing, in-silico screening (Boltz-2)
- **Benchmarks**: Boltz-1 preprint reports LDDT-PLI 65% vs. Chai-1 40% and DockQ>0.23 of 83% on CASP15 protein–ligand set ([bioRxiv 2024.11.19.624167](https://www.biorxiv.org/content/10.1101/2024.11.19.624167v1))
- **Installation**: `pip install boltz` (per README); GPU required
- **Integration notes**: Full training and inference code open; MIT license suitable for commercial drug discovery
- **Sources**: [GitHub](https://github.com/jwohlwend/boltz), [MIT News](https://news.mit.edu/2024/researchers-introduce-boltz-1-open-source-model-predicting-biomolecular-structures-1217), [Preprint](https://www.biorxiv.org/content/10.1101/2024.11.19.624167v1)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

### Chai-1

- **Type**: Library + Hosted service
- **Supplier**: Chai Discovery ([chaidiscovery.com](https://www.chaidiscovery.com/))
- **Availability**: GA
- **Pricing**: Web interface free (including for commercial use); Python package & weights restricted to non-commercial use
- **Capabilities**: Read-only — unified prediction of proteins, small molecules, DNA, RNA, glycans, modifications
- **Primary use cases**: Multimodal structure prediction, hosted exploratory folding
- **Benchmarks**: Chai-1 tech report ([bioRxiv 2024.10.10.615955](https://www.biorxiv.org/content/10.1101/2024.10.10.615955v1.full.pdf)) — AlphaFold 3-comparable performance across PoseBusters and other benchmarks
- **Installation**: `pip install chai_lab`; Linux + Python 3.10+ + CUDA GPU (≥A10/A30; A100/H100 recommended)
- **Integration notes**: Inference-only code; pre-compiled weights; web server permits commercial drug-discovery queries
- **Sources**: [GitHub](https://github.com/chaidiscovery/chai-lab), [Tech report](https://www.biorxiv.org/content/10.1101/2024.10.10.615955v1.full.pdf)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

### OpenFold / OpenFold3

- **Type**: Library
- **Supplier**: OpenFold Consortium / AlQuraishi Lab, Columbia ([openfold.io](https://openfold.io/))
- **Availability**: OpenFold GA; OpenFold3 preview (Oct 2025)
- **Pricing**: Free / OSS (Apache 2.0 code); AlphaFold 2 weights covered by CC BY 4.0 in original OpenFold
- **Capabilities**: Read-only — trainable PyTorch reproductions of AlphaFold 2 (OpenFold) and AlphaFold 3 (OpenFold3)
- **Primary use cases**: Custom training on private structural data, reproducible structure prediction, integration into in-house pipelines
- **Benchmarks**: Ahdritz et al., _Nat. Methods_ (2024) for OpenFold; OpenFold3 preview reports parity-track development vs. AlphaFold 3
- **Installation**: Clone `github.com/aqlaboratory/openfold` or `openfold-3`; Docker images and HuggingFace checkpoints provided
- **Integration notes**: Apache 2.0 permits commercial use of code; OpenFold3 is preview-stage, modalities and parity still being completed
- **Sources**: [OpenFold GitHub](https://github.com/aqlaboratory/openfold), [OpenFold3 GitHub](https://github.com/aqlaboratory/openfold-3), [Consortium announcement](https://www.businesswire.com/news/home/20251028507233/en/OpenFold-Consortium-Releases-Preview-of-OpenFold3-An-Open-Source-Foundation-Model-for-Structure-Prediction-of-Proteins-Nucleic-Acids-and-Drugs)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

### ESM-2 / ESMFold

- **Type**: Library (model weights)
- **Supplier**: Meta AI FAIR ([repo](https://github.com/facebookresearch/esm))
- **Availability**: GA; original `facebookresearch/esm` archived in favor of EvolutionaryScale releases (ESM3, ESM C)
- **Pricing**: Free / OSS (MIT for ESM-2/ESMFold code); ESM3/ESM C use mixed non-commercial and permissive commercial terms
- **Capabilities**: Read-only — protein language model embeddings (ESM-2) and single-sequence structure prediction (ESMFold)
- **Primary use cases**: Sequence representation learning, fast MSA-free structure prediction, function annotation
- **Benchmarks**: Lin et al., _Science_ (2023) — ESMFold ~order-of-magnitude faster than AlphaFold 2 with comparable accuracy on well-represented sequences; underpins ESM Metagenomic Atlas
- **Installation**: `pip install fair-esm`; HuggingFace integration via `transformers` (v4.24.0+)
- **Integration notes**: Successor work (ESM3, ESM C) at `github.com/evolutionaryscale/esm`; ESM Metagenomic Atlas data CC-BY-4.0
- **Sources**: [GitHub](https://github.com/facebookresearch/esm), [EvolutionaryScale](https://github.com/evolutionaryscale/esm), [HF model docs](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/esm.md)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

### RFdiffusion

- **Type**: Library
- **Supplier**: Baker Lab / Institute for Protein Design, University of Washington ([Baker Lab](https://www.bakerlab.org/))
- **Availability**: GA; RFdiffusion2 (Sep 2025) and RFdiffusion3 (Dec 2025) released as separate codebases
- **Pricing**: Free / OSS (BSD) for original RFdiffusion; later versions retain open licensing per IPD announcements
- **Capabilities**: Write — diffusion-based de novo protein backbone generation, motif scaffolding, binder design
- **Primary use cases**: De novo binder and enzyme design, symmetric oligomer design, scaffold generation
- **Benchmarks**: Watson et al., _Nature_ (2023) — outperforms prior hallucination/inpainting methods across multiple design tasks
- **Installation**: Docker image (Rosetta Commons) or local conda env per repo; Colab notebook available
- **Integration notes**: All-atom variant at `baker-laboratory/rf_diffusion_all_atom`; RFdiffusion3 shares no code with predecessors and broadens supported molecule types
- **Sources**: [GitHub](https://github.com/RosettaCommons/RFdiffusion), [Baker Lab post](https://www.bakerlab.org/2023/03/30/rf-diffusion-now-free-and-open-source/), [RFdiffusion3 announcement](https://www.ipd.uw.edu/2025/12/rfdiffusion3-now-available/)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

## Flagged for review

_None._

## Recently surfaced

- **AlphaFold 3** (added 2026-05-18) — DeepMind biomolecular complex prediction (server + non-commercial code).
- **Boltz-1 / Boltz-2** (added 2026-05-18) — MIT-licensed open structure and affinity models.
- **Chai-1** (added 2026-05-18) — Chai Discovery multimodal structure prediction.
- **OpenFold / OpenFold3** (added 2026-05-18) — Apache-2.0 reproductions of AlphaFold 2/3.
- **ESM-2 / ESMFold** (added 2026-05-18) — Meta FAIR protein language model and folding head.
- **RFdiffusion** (added 2026-05-18) — Baker Lab generative protein design diffusion model.
