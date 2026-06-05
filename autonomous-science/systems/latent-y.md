---
title: Latent-Y
parent: Systems
grand_parent: AI scientists
nav_order: 29
affiliation: Latent Labs (London, UK; San Francisco, USA)
lifecycle_stages: [Multi-stage]
autonomy: Fully autonomous
domain: Biology / drug discovery (biologics)
availability: Closed / platform access
last_verified: 2026-05-29
---

# Latent-Y

Lab-validated autonomous agent that executes complete de novo antibody design campaigns from text prompts, covering literature review, target analysis, epitope identification, candidate design, computational validation, and selection of lab-ready sequences.

| | |
|---|---|
| **Affiliation** | Latent Labs Team, London & San Francisco ([Latent Labs Platform](https://platform.latentlabs.com)) |
| **First introduced** | 2026-03 (arXiv:2603.29727, dated 23 March 2026) |
| **Lifecycle stages** | Multi-stage (literature review → target/epitope analysis → candidate design → computational validation → lab-ready selection) |
| **Autonomy level** | Fully autonomous end-to-end campaigns; collaborative mode also supported |
| **Domain focus** | De novo biologics design (antibodies, VHHs / nanobodies, peptides, mini-binders) |
| **Availability** | Closed; available to selected partners on the Latent Labs Platform |

## Approach

Latent-Y is an agentic system layered on the Latent Labs Platform that orchestrates the Latent-X2 generative model alongside bioinformatics tools, biological databases, and scientific literature. From a natural-language objective, it consults the literature, identifies target structures, characterizes candidate epitopes against functional criteria, and spawns targeted computational experiments using Latent-X2. The agent reasons about iPTM, DockQ, and other quality metrics, adjusts generation parameters or epitope constraints, and triages designs across cycles. Where standard capabilities are insufficient, it can generate custom computational approaches from natural-language descriptions, extending its own toolkit. Final quality assurance includes clustering for diversity, sequence-similarity searches, and liability analyses before producing a lab-ready set.

## Validation

Wet-lab validation across nine therapeutic targets via three campaign types: epitope discovery (IL-6, PRL, IL-33, TNFα, SC2RBD, IL-6R); cross-species reactivity (human and cynomolgus TNFL9, requiring autonomous generation of a custom cross-species design method); and literature-inferred design from a scientific publication targeting human transferrin receptor (hTfR1) for blood–brain barrier crossing. Binders were measured by one-point high-throughput SPR primary screening and five-point SPR kinetic fitting.

## Notable results

- 67% target-level success rate (lab-confirmed nanobody binders against 6 of 9 targets); per-target hit rates 1–28% of tested sequences.
- Single-digit nanomolar binding affinities: 5.44 nM (PRL), 12.5 nM (IL-6), 517 nM (IL-6R); reported as the first experimentally validated fully de novo designed antibody binder against IL-6.
- Expert user study (n = 10 expert baseline estimates vs. n = 5 agent-assisted runs) reports a 56× acceleration of full computational design campaigns, with literature/PDB review (~4,300×) and structural analysis/epitope selection (~350×) as the largest individual speedups.
- Cross-species TNFL9 campaign validates Latent-Y-generated custom generative code as a working capability extension under human biological steering.

## Primary paper

[Latent Labs Team, "Latent-Y: A Lab-Validated Autonomous Agent for De Novo Drug Design," arXiv:2603.29727 (2026)](https://arxiv.org/abs/2603.29727).

## Other references

_None yet._

## Code

Not released. Latent-Y is available to selected partners at [platform.latentlabs.com](https://platform.latentlabs.com); designed structures from the reported campaigns are published on the platform and accessible without sign-in.
