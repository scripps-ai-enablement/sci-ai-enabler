---
title: OpenScientist
parent: Systems
grand_parent: AI scientists
nav_order: 15
affiliation: Washington University in St. Louis, with collaborators at Harvard Medical School, Lawrence Berkeley National Laboratory, Stanford, University of Washington
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Biomedicine (clinical)
availability: Open source
last_verified: 2026-05-20
---

# OpenScientist

Open-source agentic AI co-scientist for biomedical discovery. Built on Claude Code with a public collection of domain-specific Agent Skills; semi-autonomously investigates scientist-defined queries by querying PubMed, examining papers, and writing and executing code.

| | |
|---|---|
| **Affiliation** | Washington University in St. Louis (Department of Pathology & Immunology), with Harvard Medical School, Lawrence Berkeley National Laboratory, Stanford, University of Washington, and additional partners ([openscientist.io](https://openscientist.io/)) |
| **First introduced** | 2026-03 (medRxiv preprint 2026.03.15.26348338) |
| **Lifecycle stages** | Multi-stage (hypothesis generation + experiment design + analysis) |
| **Autonomy level** | Semi-autonomous (default 10 feedback rounds in co-investigator mode; optional human interaction between rounds) |
| **Domain focus** | Biomedicine — Alzheimer's disease biomarkers, plasma proteomics, single-cell neuroscience, oncology |
| **Availability** | Open source (Apache 2.0) — code at [openscientist-io/openscientist](https://github.com/openscientist-io/openscientist); free public web interface at [openscientist.io](https://openscientist.io/) |

## Approach

OpenScientist accepts a scientist-defined query and optional dataset, then autonomously investigates by querying PubMed, examining papers, and writing and executing analysis code. Three architectural elements:

- **Agent Skills** — a public collection of `SKILL.md`-format skills encoding advice in specific biomedical domains, analytical functions, and bioinformatics tools. New skills can be added by contributors.
- **Knowledge State Data Structure (KSDS)** — stores intermediate findings and supports iterative refinement across rounds.
- **Co-investigator mode** — optional human-in-the-loop checkpoints between iterations (default 10 rounds), letting domain experts steer the investigation without breaking the autonomous loop.

OpenScientist is built on Claude Code, with the design intended to support alternative AI agents in the future.

## Validation

Four clinical case studies, evaluated by domain experts:

- **SEABIRD Alzheimer's biomarker cohort** — prespecified ROC analysis to identify the best plasma biomarker discriminating amyloid-PET status. Identified `%ptau217` as the best predictor, matching the human-expert analysis. The agent completed the prespecified analysis in ~40 minutes; human analysts took ~2 hours; the original work had taken several weeks.
- **Plasma proteomic survival prediction** — unsupervised modelling task. Generated a survival model with c-index comparable to published Biomarkers-of-Aging models.
- **Single-cell transcriptomics, neurofibrillary tangles** — hypothesis-investigation task in neurons. Proposed a mechanism linking tau pathology to altered lysosomal acidification, surfacing downregulation of a lysosomal ion channel in affected neurons.
- **Multiple myeloma hypothesis generation** — generated hypotheses across disease-progression stages and validated them in an external cohort (Dataset V, n=162) while correctly rejecting patterns in a randomized control (Dataset R).

## Notable results

- Completed a prespecified Alzheimer's biomarker analysis in 40 minutes that originally took human scientists several weeks.
- Generated multiple-myeloma hypotheses validated in an external cohort while distinguishing true signal from randomized controls.
- Demonstrated end-to-end usability across four heterogeneous clinical case studies, evaluated by domain experts.

## Primary paper

[Roberts et al., "OpenScientist: evaluating an open agentic AI co-scientist to accelerate biomedical discovery," medRxiv 2026.03.15.26348338](https://www.medrxiv.org/content/10.64898/2026.03.15.26348338v1).

## Other references

- [PubMed entry (PMID 41891004)](https://pubmed.ncbi.nlm.nih.gov/41891004/)
- [Supplementary materials on Zenodo](https://doi.org/10.5281/zenodo.18852839)
- [Public web interface](https://openscientist.io/)

## Code

[openscientist-io/openscientist](https://github.com/openscientist-io/openscientist) — Apache 2.0.
