---
title: Somatic Signatures (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine, Molecular and Cellular Biology]
last_verified: 2026-08-16
summary: "Extracts and assigns COSMIC v3.4 mutational signatures from somatic VCFs with SigProfiler, MutationalPatterns, MuSiCal or HRDetect to read DNA-damage etiology"
---

# Somatic Signatures (bioSkills)

A Claude Code skill that turns a somatic VCF into mutational-signature assignments — which DNA-damage or repair-defect process generated the mutations, and whether that implies a therapy decision.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT). SigProfilerSuite, MutationalPatterns, MuSiCal, SigNet and HRDetect install separately under their own licences; COSMIC signature data is subject to COSMIC's terms (free for academic use, commercial licence required otherwise) |
| **Capabilities** | Read/Write — Claude runs the Python and R workflows locally on your VCFs; it is not an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "clinical-databases"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/clinical-databases/somatic-signatures ~/.claude/skills/
  ```
  (run from the directory holding your clone — if you are still in `bioSkills/` from the previous step, use `cp -r clinical-databases/somatic-signatures ~/.claude/skills/`, or replace `bioSkills/` with the absolute path of your clone). Install the primary toolchain:
  ```
  pip install SigProfilerMatrixGenerator SigProfilerAssignment SigProfilerExtractor
  ```
  The R-based alternative is `BiocManager::install("MutationalPatterns")`. A matching reference genome must be installed for SigProfiler (`SigProfilerMatrixGenerator install GRCh38`).

## What it does

- **Matrix generation** — builds the 96-context SBS matrix (or DBS / ID / CN / SV matrices) from somatic VCFs.
- **Extraction vs refit** — chooses de novo NMF extraction (cohorts of ≥ 50) or refit-to-COSMIC assignment (single samples or N < 50), which is the decision most signature analyses get wrong.
- **Signature catalogues** — COSMIC v3.4: 86 SBS, 11 DBS, 18 ID, 21 CN, 16 SV signatures.
- **Method choice** — SigProfilerSuite (default), MutationalPatterns (R, strict refit + NMF), MuSiCal (minimum-volume NMF, addresses non-uniqueness), SigNet (neural, tuned for low mutation counts), HRDetect (six-feature BRCA-deficiency classifier), plus YAPSA, MutSignatures and Helmsman.
- **Stability gating** — 100 NMF replicates, minimum stability ≥ 0.2 and average ≥ 0.8 before a de novo signature is believed.
- **Etiology and actionability** — maps dominant signatures to causes (BRCA1/2 homologous-recombination deficiency, MMR deficiency, POLE, APOBEC3A, UV, tobacco, aflatoxin, 5-FU/SBS17b, platinum, colibactin/SBS88) and flags where that routes a PARP-inhibitor or checkpoint-inhibitor decision, or indicates therapy-induced damage.

**Primary use cases**: HRD assessment for PARP-inhibitor decisions, identifying mutational processes in a tumour cohort, distinguishing MMR-deficient from POLE hypermutators, auditing a published signature analysis for extraction/refit and stability choices.

## Notes

**Research use, not a diagnostic result.** An HRD or signature-based therapy decision needs a validated clinical assay; the skill's contribution is method selection and the stability criteria that determine whether an extracted signature is real.

The judgement call it forces is de novo extraction versus refitting: extracting signatures from a small cohort produces unstable, uninterpretable components, while refitting a single sample to the full COSMIC catalogue over-explains noise unless the candidate set is constrained. Signature non-uniqueness (different decompositions fitting equally well) is the reason MuSiCal's minimum-volume approach is offered.

Read alongside [MSI Detection](msi-detection.html) and [Tumor Mutational Burden](tumor-mutational-burden.html) — the three answer complementary questions about the same somatic call set (process, instability, burden). [CNV Inference](cnv-inference.html) covers the copy-number layer that CN signatures and HRDetect draw on.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection. Upstream skill front-matter name is `bio-clinical-databases-somatic-signatures`; upstream directory `clinical-databases/somatic-signatures`. The skill is description-activated — there is no bare `/somatic-signatures` slash command.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-databases/somatic-signatures/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-databases/somatic-signatures/SKILL.md)
- [COSMIC Mutational Signatures v3.4](https://cancer.sanger.ac.uk/signatures/)
- [`AlexandrovLab/SigProfilerAssignment`](https://github.com/AlexandrovLab/SigProfilerAssignment)
- [Davies et al. 2017, HRDetect](https://doi.org/10.1038/nm.4292)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=somatic-signatures&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fsomatic-signatures.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
