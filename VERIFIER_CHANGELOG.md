---
title: Verification updates
parent: Updates
nav_order: 5
permalink: /updates/verification.html
---

# Verification updates

Rolling, reverse-chronological log of catalog verification + security passes. Each scheduled or
on-demand run that produces changes prepends a dated block; the top block is mirrored to the pinned
"Verification updates" issue.

Older entries live in [VERIFIER_CHANGELOG_ARCHIVE.md](VERIFIER_CHANGELOG_ARCHIVE.md).

## 2026-08-17

### Verified
- Adjudicated the injected 15-page digest: `acmg-classification`, `alignment-trimming`, `alkyl`, `blatant-why`, `can-immune`, `mcptools`, `medicare-mcp`, `msa-statistics`, `msi-detection`, `multiple-alignment`, `neuro-mcp`, `nwb-mcp-server`, `pbmcpedia`, `somatic-signatures`, `structural-alignment`. All 15 graded `works`; 13 `caution`, 2 `cleared` (`mcptools`, `medicare-mcp`). 9 further digest pages were over this run's 15-page review budget and were intentionally left untouched.
- Confirmed install/launch commands against primary sources for every non-smoke-tested page in the batch: `mcptools` (package vignette), `medicare-mcp` (`package.json` + README), `pbmcpedia` (`server.ts` + README) all match the catalog pages verbatim.

### Fixed
- No install-path or launch-command defects found this run; no page-content fixes were required beyond the stamp fields and table rows.

### Flagged
- **Discrepancy vs. prior runs:** `GPTomics/bioSkills` is now confirmed `archived: true` on GitHub (1187★, pushed 2026-08-15). This reverses the not-archived status this same repo has carried across 5+ prior verifier runs (most recently 2026-08-13). All 7 affected catalog pages (`acmg-classification`, `alignment-trimming`, `msa-statistics`, `msi-detection`, `multiple-alignment`, `somatic-signatures`, `structural-alignment`) are graded `works`/`caution` this run — MIT root license and skill directories are still intact and resolve, but no further upstream maintenance should be expected. Flagged in `catalog/verifier-state.md` for next-run recheck.
- 9 digest pages remain over this run's review budget and stay due for the next run.

### Security
- Resolved 3 digest flags as non-issues on primary-source evidence: `osv-advisory` on `requests` (`acmg-classification`) and on `uv` (`nwb-mcp-server`) both trace to GHSA fixes that shipped before each page's pinned version; `license-unrecognized` (`mcptools`) resolved via a raw `LICENSE.md` fetch confirming standard MIT (GitHub's classifier had simply failed to auto-detect it) — regraded `cleared`.
- `endpoint-non-2xx` on `can-immune` confirmed as expected live-server behavior (406 to a browser-shaped GET, consistent with the digest's own 405 finding).
- New `caution` grades (first review, provenance/license clean but carrying an independent risk signal): `alkyl` (single-maintainer Beta, no CI-passing tests), `blatant-why` (optional external compute/wet-lab API keys), `can-immune` (new/low-traffic repo over COSMIC/DepMap-derived data), `neuro-mcp` (Alpha/0-star single-org project persisting subject and EHR records locally), `nwb-mcp-server` (single-maintainer, pins a pre-release dependency), `pbmcpedia` (stale, low-traffic repo).
- New `cleared` grades: `mcptools` (MIT confirmed), `medicare-mcp` (MIT confirmed, provenance and launch command verified against package.json/README).

## 2026-08-13

### Verified
- Stamped 15 previously-unreviewed catalog pages with full verification/security badges: `loop-calling`, `metabolite-communication`, `multiplicity-graphical`, `ncrna-search`, `netneurotools-guide`, `neural-population-analysis-guide`, `parameter-recovery-checker`, `power-and-sample-size`, `pycortex-guide`, `structure-probing`, `subgroup-analysis`, `tad-detection`, `tooluniverse-clinical-trial-design`, `tooluniverse-clinical-trial-matching`, `tooluniverse-drug-mechanism-research` — all graded `works`/`cleared`.
- 8 `GPTomics/bioSkills` pages confirmed against a fresh root LICENSE fetch this run (MIT verbatim, 1.2k★, not archived): `loop-calling`, `metabolite-communication`, `multiplicity-graphical`, `ncrna-search`, `power-and-sample-size`, `structure-probing`, `subgroup-analysis`, `tad-detection`. None depend on external credentials.
- 4 `HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills` pages (`netneurotools-guide`, `neural-population-analysis-guide`, `parameter-recovery-checker`, `pycortex-guide`) carried a `repo-renamed` flag; confirmed this run as the same genuine GitHub org transfer to `NeuroAIHub` already established for sibling skills in this collection (old owner URL still resolves and redirects to the new owner) — no page fix needed.
- 3 ToolUniverse skill pages (`tooluniverse-clinical-trial-design`, `tooluniverse-clinical-trial-matching`, `tooluniverse-drug-mechanism-research`) confirmed against a fresh `mims-harvard/ToolUniverse` fetch this run (Apache-2.0, active, 1,624★); each is read-only over public sources (Open Targets, ClinicalTrials.gov, ChEMBL, KEGG, Reactome, STRING, DailyMed, PharmGKB, EU CTIS, ISRCTN, CIViC, MyGene, FDA/openFDA/FAERS, PubMed/Europe PMC) with no API-key/credential dependency, matching the pattern of the ~22 already-stamped ToolUniverse pages.

### Fixed
- None — all 15 pages resolved cleanly with no install-path, launch-command, or licence discrepancies.

### Flagged
- None new. Two additional pages in this run's digest were over the 15-page review budget and were intentionally left unstamped; they lead the next worklist.

### Security
- All 15 pages graded `cleared`: provenance matches supplier for every page, real permissive licenses (MIT ×12, Apache-2.0 ×3) confirmed by fresh fetch, no OSV/GHSA advisories surfaced, and no external-service credential requirements found in any of the three ToolUniverse skills reviewed.

## 2026-08-10

### Verified
- Worked the injected 15-page adjudication digest at this run's 15-page review budget: `bayesian-trials`, `cdisc-data-handling`, `chemgraph`, `clustering-phenotyping`, `compartment-analysis`, `compensation-transformation`, `covariation-analysis`, `cytometry-differential-analysis`, `cytometry-qc`, `effect-measures`, `fda-mcp`, `gating-analysis`, `geometric-analysis`, `hashing-demultiplexing`, `lesion-symptom-mapping-guide`. All first-time full stamps (never previously reviewed); all graded `works`.
- 9 `GPTomics/bioSkills` pages confirmed against a fresh root LICENSE fetch (MIT verbatim) → works/cleared.
- `chemgraph` (argonne-lcf) — Apache-2.0 confirmed via raw LICENSE fetch, provenance matches ALCF, `python -m chemgraph.mcp.mcp_tools` launch command confirmed verbatim in upstream README, no OSV/GHSA advisories.
- `fda-mcp` (openpharma-org) — MIT confirmed via raw LICENSE fetch, provenance matches (OpenPharma confirmed as a real 50+-repo coordinated org), `node build/index.js` stdio launch already correctly documented on the page.
- `lesion-symptom-mapping-guide` — `repo-renamed` flag confirmed a genuine GitHub org transfer `HaoxuanLiTHUAI` → `NeuroAIHub`, same pattern already established for sibling skills in this collection.
- `covariation-analysis` — R-scape dependency confirmed GPLv3 (EddyRivasLab) this run.
- `geometric-analysis` — DSSP dependency confirmed migrated to Boost Software License / BSD-2-Clause (no longer restrictive) this run.

### Fixed
- No page-content fixes were needed this run — all evidence gathered (GPTomics MIT root, chemgraph Apache-2.0, fda-mcp MIT, lesion-symptom-mapping-guide repo-renamed) confirmed the pages were already accurate.

### Flagged
- `cdisc-data-handling` added to the Flagged list: security `caution` — skill code MIT/clean and provenance confirmed, but CDISC standards require membership/licence for some deliverables and Pinnacle 21 Enterprise is commercial (free Community validator is more limited). Data/tool-license restriction only, same pattern as `kegg-pathway-analysis`. Verification `works`.
- 17 further flagged pages were over this run's review budget and were intentionally left untouched — they should lead the next worklist.

### Security
- 14 of 15 pages graded `cleared`; 1 graded `caution` (`cdisc-data-handling`, data-use restriction only — see Flagged).
- No new advisories found via WebSearch/GitHub security-advisories for `GPTomics/bioSkills`, `argonne-lcf/ChemGraph`, or `openpharma-org/fda-mcp`.

## 2026-08-06

### Verified
- Worked the injected 15-page adjudication digest: `omophub-mcp`, `optogenetics-protocol-designer`, `perturb-seq`, `pyomop`, `rosetta-mcp-server`, `scatac-analysis`, `signal-detection-analysis`, `strain-tracking`, `structure-preparation`, `structure-validation`, `tooluniverse-admet-prediction`, `tooluniverse-cell-line-profiling`, `tooluniverse-chemical-sourcing`, `tooluniverse-dose-response`, `trial-reporting`.
- `perturb-seq`, `scatac-analysis`, `strain-tracking`, `trial-reporting` (GPTomics bioSkills) — works/cleared, fresh root LICENSE fetch confirms MIT.
- `tooluniverse-admet-prediction`, `tooluniverse-cell-line-profiling`, `tooluniverse-chemical-sourcing`, `tooluniverse-dose-response` (ToolUniverse) — works/cleared, confirmed against `mims-harvard/ToolUniverse` Apache-2.0.
- `optogenetics-protocol-designer`, `signal-detection-analysis` (awesome_cognitive_and_neuroscience_skills) — works/cleared; the `repo-renamed` flag on both confirmed as a legitimate GitHub org transfer to NeuroAIHub, not a typosquat.
- `rosetta-mcp-server` — works/caution; install/launch commands confirmed unchanged against the README.

### Fixed
- `pyomop` — the documented `pyomop-mcp-server` console-script entry point boot-errored in this run's smoke test (`No such file or directory`) despite a clean `pip install pyomop`. Replaced the install/registration blocks (Verify-it-starts, Claude Code stdio, Claude Desktop config) with the working `pyomop --mcp-server` subcommand form. Graded degraded pending a clean reboot confirmation next run.

### Flagged
- `structure-preparation`, `structure-validation` (GPTomics bioSkills) — security caution: bundled Phenix/CCTBX tooling (`reduce`, `phenix.molprobity`, `phenix.process_predicted_model`) is free for academic use only, same pattern as `mixcr-analysis`.
- `rosetta-mcp-server` — security caution: `license-absent` flag confirmed accurate, no `LICENSE` file committed upstream, MIT asserted only in README/package.json prose.
- `omophub-mcp` — verification degraded: auth-gated (requires a signed-up `OMOPHUB_API_KEY`), so functionally unverifiable without an account.
- `pyomop` — verification degraded pending a clean-reboot recheck of `pyomop --mcp-server` next run.
- One further flagged page from this run's digest was over the 15-page review budget and was intentionally left untouched; it leads the next worklist.

### Security
- `pyomop` — `license-absent` flag resolved: fetched the repository `LICENSE` directly from the `develop` branch (the actual GitHub default branch) and confirmed GPL-3.0 verbatim, matching the GitHub API license field. Regraded security cleared.
- `signal-detection-analysis` — `osv-advisory` flag traced to three old scipy GHSA IDs, all fixed-by-or-withdrawn before the pinned scipy 1.18.0; no live advisory applies. Regraded security cleared.

## 2026-08-03

### Verified
- First-time full review + stamp of a 15-page bootstrap batch: `adaptive-designs`, `binding-site-detection`, `calcium-imaging-analysis-guide`, `cnv-inference`, `deeplabcut`, `differential-abundance`, `doublet-detection`, `drift-diffusion-model`, `functional-profiling`, `immunogenicity-scoring`, `interface-analysis`, `lineage-tracing`, `materials-project-mcp`, `metaphlan-profiling`, `missing-data-sensitivity`. All graded `works`.
- `GPTomics/bioSkills` (10 pages) reconfirmed MIT via a fresh root LICENSE fetch (1.1k★, not archived).
- `HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills` (3 pages) repo-transfer to `NeuroAIHub` confirmed genuine (old URL redirects live, new README still documents old install path) — no fix needed.
- `materials-project-mcp` launch command `uvx mcp-science materials-project` reconfirmed against PyPI `mcp-science` 0.1.7 metadata and the `mcp.science` root README (MIT, 146★, no advisories).

### Fixed
- None — all three inspection flags this run (`repo-renamed` ×3, `smoke-install-error` ×1) were resolved as non-issues on evidence; no page content required correction.

### Flagged
- `immunogenicity-scoring` (GPTomics bioSkills) — security `caution`: skill code MIT/clean, but bundled MixMHCpred/PRIME predictors are academic/non-commercial-use only (same pattern as `mixcr-analysis`).

### Security
- `lineage-tracing` — smoke job's `install_error` is a false negative: it pip-installed the stale/deprecated PyPI `cassiopeia-lineage` 1.0.4 (2019, incompatible with Python 3.12's removed `numpy.distutils`), a path the catalog page itself already warns against. The page's own recommended `pip install git+https://github.com/YosefLab/Cassiopeia@master` was confirmed live. Graded `works`/`cleared`.
- No new advisories found for any of the 15 pages' upstream repos/packages (GitHub `/security` pages and PyPI metadata checked where applicable).

## 2026-07-29

### Verified
- `arboreto` (K-Dense) — works/cleared, `verified_on`/`reviewed_on` refreshed to 2026-07-29. Liveness flagged `changed-since-verified` (skill dir last committed 2026-07-26): fetched `skills/arboreto/SKILL.md` this run — unchanged install (`uv pip install arboreto` / `conda install -c bioconda arboreto`), no risky patterns, no external creds. Smoke-test `pip install arboreto` passed this run (`.verify/smoke-results.json`), upgrading the evidence to a real install verdict.
- `archs4-database` (SciAgent) — works/cleared, `verified_on`/`reviewed_on` refreshed to 2026-07-29. Liveness flagged `license-missing`: GitHub's API reports NOASSERTION for `jaechang-hits/SciAgent-Skills`, but the raw root `LICENSE` fetched this run is verbatim CC BY 4.0 — consistent with the standing SciAgent finding, reconfirmed independently this run.
- `arxiv` — works/cleared, `verified_on`/`reviewed_on` refreshed to 2026-07-29. Liveness flagged the launch command as unconfirmed by execution (auth-not-applicable but not smoke-run): fetched `blazickjp/arxiv-mcp-server`'s README this run — `claude mcp add --transport stdio --scope user arxiv -- uvx arxiv-mcp-server` and the `claude_desktop_config.json` stdio block both match the page verbatim. No fix needed.

### Fixed
- `arrayexpress` (Augmented Nature) — Pricing row corrected from "Free / OSS" to note the wrapper's restrictive personal/non-commercial LICENSE. Liveness flagged `license-missing`; the GitHub license API actually returns a LICENSE file (SPDX NOASSERTION) whose text, fetched this run, is a restrictive non-commercial grant — same pattern as `uniprot`/`alphafold`/`gene-ontology`/`human-protein-atlas`. This is a license-text discrepancy the prefetch's binary "license present/missing" signal cannot distinguish from a real absence.

### Flagged
- `arrayexpress` — security stays `caution`; added to the Flagged registry with the corrected rationale (restrictive LICENSE vs. the page's former OSS claim, not just "no LICENSE").

### Security
- No new advisories or provenance mismatches found in this batch. `arrayexpress` regrades its existing `caution` rationale (see Fixed/Flagged) but the grade itself is unchanged.

Note: worked the digest's 4-page review-budget list in full; the other 9 flagged pages in this run's 14-page liveness batch were over budget and were not touched — they stay due and lead the next worklist.

## 2026-07-29

### Verified
- Worked the injected 8-page worklist (`allenbrain` → `aomic-skill`) top-to-bottom. 3 pages resolved clean per the workflow's liveness prefetch (`alphafold2`, `amr-detection`, `aomic-skill`) — anchors re-confirmed (`google-deepmind/alphafold`/`science-skills` Apache-2.0/2026-04-22+2026-07-07; `GPTomics/bioSkills` MIT/2026-07-18; `CUHK-AIM-Group/NeuroClaw` MIT/2026-07-14), stamps refreshed 2026-07-20→2026-07-29 with no content changes.
- `allenbrain`: fetched `api.github.com/repos/MCPmed/allenbrain-mcp` — still resolves, no LICENSE, not archived, pushed 2026-04-01, 3 stars. Prior-run transfer fix stands; kept degraded/caution.
- `alphafold`: fetched `api.github.com/repos/Augmented-Nature/AlphaFold-MCP-Server` — LICENSE still NOASSERTION (restrictive non-commercial), not archived, pushed 2025-12-21, 35 stars. Kept works/caution.
- `alphagenome`: `google-deepmind/science-skills` still Apache-2.0/not-archived, pushed 2026-07-07, 2,552 stars; skill dir resolves. AlphaGenome API remains a signup-gated research preview, so kept degraded/cleared per the auth-gate rubric.
- `anndata`: confirmed `K-Dense-AI/scientific-agent-skills` MIT/not-archived, pushed 2026-07-29 (same-day), and PyPI `anndata` 0.13.2 (BSD-3-Clause). The quarantined smoke job additionally reports `pip install anndata` as a `pass` this run — first smoke evidence for this page (install-only, no import/boot script) — noted in the `**Verified**` row. Kept works/cleared.
- `antibody-registry`: refetched `claude.com/docs/claude-science/connectors-and-skills` — the Research Resources featured connector still lists "Grants.gov, Antibody Registry" as sources. Kept works/cleared.

### Discrepancy noted (informational, no page change)
- The injected liveness prefetch resolved `antibody-registry`'s "repo" to `scripps-ai-enablement/sci-ai-enabler` (this catalog repo) rather than an external tool repo — expected, since this is an Anthropic-hosted connector with no installable repo of its own; the page correctly documents no git-based install path. Flagging so the mismatch between prefetch and page content is visible, per this run's instructions.

### Fixed
(none this run — all 8 pages held their existing grades)

### Flagged
(none new this run)

### Security
No security regrades this run. All 5 adjudicated pages' existing `caution`/`cleared` grades were reconfirmed against freshly fetched GitHub/PyPI/doc evidence (see Verified above); no new OSV/GitHub advisories found for any of the 8 repos/packages checked.

## 2026-07-29 (worklist maintenance — 25-page window, umap-learn → aind-data)

Worked the injected 25-page worklist top-to-bottom. All 25 were already stamped 2026-07-20;
rechecked against fresh source fetches. 24 clean rechecks + 1 launch-command fix. Stamps refreshed
2026-07-20→2026-07-29.

### Verified
- 24 pages rechecked works/degraded (unchanged) against fresh anchors: `K-Dense-AI/scientific-agent-
  skills` MIT/pushed 2026-07-29/32073★ (umap-learn, usfiscaldata, vaex, venue-templates,
  what-if-oracle, xlsx, zarr-python, adaptyv, aeon); `google-deepmind/science-skills` Apache-2.0/
  pushed 2026-07-07/2552★ (unibind-database — prior scienceskillscommon fix stands, stays degraded);
  `jaechang-hits/SciAgent-Skills` CC-BY-4.0-root/pushed 2026-07-24/288★ (unichem-database,
  uspto-database, viennarna-structure-prediction, western-blot-quantification, zinc-database);
  `Augmented-Nature/UniProt-MCP-Server` NOASSERTION/pushed 2025-12-21/19★ (uniprot);
  `CUHK-AIM-Group/NeuroClaw` MIT/pushed 2026-07-26/76★ (wmh-segmentation, abcd-skill, abide-skill,
  adhd200-skill, adni-skill, aibl-skill); `anthropics/life-sciences` marketplace 21 plugins
  (10x-genomics-cloud, adisinsight — both stay degraded, subscription/account-gated).
- Added missing `verification_note` + `**Verified**` table row to `unichem-database`, and missing
  `verification_note` to `uspto-database` / `viennarna-structure-prediction` /
  `western-blot-quantification`.

### Fixed
- `aind-data` works→degraded — PyPI `aind-data-mcp` v0.4.5 MIT still resolves but the upstream README
  no longer ships a stdio console-script; it now documents a remote HTTP endpoint
  `https://metadata-portal.allenneuraldynamics.org/mcp/` (live: 406 to a browser Accept header). No
  `aind-data-mcp` entry point in PyPI metadata. Rewrote the install block from the dead
  `uv tool install` + `--transport stdio -- aind-data-mcp` invocation to the current
  `--transport http` registration (plus the HTTP `claude_desktop_config.json` form).

### Flagged
- `aind-data` degraded — launch command auto-fixed to the HTTP transport this run; recheck the HTTP
  endpoint next cycle and flip to works once it proves stable.

### Security
- No security regrades. Kept-caution unchanged: `xlsx` (Anthropic-proprietary LICENSE.txt in an MIT
  collection), `what-if-oracle` (CC BY-NC-SA 4.0 non-commercial), `adaptyv` (writes to a paid wet-lab
  platform, handles ADAPTYV_API_KEY), `uniprot` (restrictive non-commercial LICENSE vs page's MIT
  claim, ~7mo stale), `10x-genomics-cloud` (closed-source vendor binary). `aind-data` security stays
  cleared (Allen Institute provenance, MIT, read-only).

## 2026-07-27 (worklist maintenance — 4-page recheck, latchbio-integration → liana-mcp)

Worked the injected 4-page worklist top-to-bottom. All four were already stamped 2026-07-20 (within
cadence); rechecked against fresh source fetches — zero drift, no fixes. Stamps refreshed to
2026-07-27.

### Verified
- `latchbio-integration` works/caution (unchanged) — `K-Dense-AI/scientific-agent-skills` MIT/not-
  archived/pushed 2026-07-27/31.9k★; `skills/latchbio-integration/SKILL.md` (8527 B) confirmed.
- `latex-posters` works/caution (unchanged) — same anchor; `skills/latex-posters/SKILL.md` (15554 B)
  confirmed.
- `lggnn` works/cleared (unchanged) — `CUHK-AIM-Group/NeuroClaw` MIT/not-archived/pushed 2026-07-26/
  76★; `skills/lggnn/SKILL.md` (5467 B) confirmed.
- `liana-mcp` works/caution (unchanged) — `scmcphub/liana-mcp` no-LICENSE/not-archived/pushed
  2025-06-27/1★; PyPI `liana-mcp` 0.4.0; launch `liana-mcp run` re-confirmed against the repo README.

### Security
- `latchbio-integration` caution: provenance matches K-Dense-AI, but the per-skill license is unstated
  on the page and it deploys workflows/data to the external LatchBio cloud with user credentials.
- `latex-posters` caution: provenance matches K-Dense-AI, no external calls, but the per-skill license
  is unstated on the page (collection root is MIT).
- `lggnn` cleared: provenance matches CUHK-AIM-Group/NeuroClaw, MIT, no OSV advisories.
- `liana-mcp` caution: provenance matches scmcphub, no OSV advisories, but no repo LICENSE file and the
  scmcphub ecosystem is unmaintained since 2025-06.

## 2026-07-27 (worklist maintenance — 4-page recheck, kegg-database → kmeans)

Worked the injected 4-page worklist top-to-bottom. All four were already stamped 2026-07-20 (within
cadence); rechecked against fresh source fetches — zero drift, no fixes. Stamps refreshed to
2026-07-27.

### Verified
- `kegg-database` works/caution (unchanged) — `jaechang-hits/SciAgent-Skills` NOASSERTION-classifier-
  but-CC-BY-4.0-root/not-archived/pushed 2026-07-24/284★; `skills/genomics-bioinformatics/databases/
  kegg-database/SKILL.md` (18418 B) confirmed.
- `kegg-pathway-analysis` works/caution (unchanged) — same anchor; `skills/systems-biology-multiomics/
  kegg-pathway-analysis/SKILL.md` (17508 B) confirmed.
- `ketcher` works/cleared (unchanged) — `epam/ketcher` Apache-2.0/not-archived/pushed 2026-07-27/847★;
  npm `ketcher-react` 3.17.1 Apache-2.0; Anthropic Claude Science connector, client-side editor, no creds.
- `kmeans` works/cleared (unchanged) — `CUHK-AIM-Group/NeuroClaw` MIT/not-archived/pushed 2026-07-26/
  76★; `skills/kmeans/SKILL.md` (4082 B) confirmed.

### Security
- `kegg-database` + `kegg-pathway-analysis` caution: skill code CC BY 4.0 and provenance clear, but the
  underlying KEGG data needs a paid commercial license for non-academic use (data-use restriction only).
- `ketcher` + `kmeans` cleared: provenance matches supplier, real Apache-2.0/MIT licenses, no OSV
  advisories, no credentials.

## 2026-07-27 (worklist maintenance — 4-page recheck, inductive-bio → intact)

Worked the injected 4-page worklist top-to-bottom. All four were already stamped 2026-07-20 (within
cadence); rechecked against fresh source fetches — zero drift, no fixes. Stamps refreshed to
2026-07-27.

### Verified
- `inductive-bio` degraded/cleared (unchanged) — supplier inductive.bio loads (Beacon-1 ADMET, 3×
  OpenADMET blind-challenge wins) but no public MCP endpoint / self-serve sign-up, and the Claude
  Science connectors-and-skills doc does not list Inductive Bio; the vendor connector is confirmed
  only via the cited PR Newswire release, so the install path stays functionally unverifiable.
- `infographics` works/caution (unchanged) — `K-Dense-AI/scientific-agent-skills` MIT/not-archived/
  pushed 2026-07-27/31.9k★; `skills/infographics/SKILL.md` (10949 B) + references/scripts confirmed.
- `instrument-data-to-allotrope` works/cleared (unchanged) — plugin registered in `anthropics/
  life-sciences` `.claude-plugin/marketplace.json` (source `./`); `allotropy` dep on PyPI is Benchling
  MIT (latest 0.1.142).
- `intact` works/cleared (unchanged) — Claude Science connectors-and-skills doc confirms "Structures
  & Interactions | PDB, AlphaFold, EMDB, Complex Portal, IntAct"; read-only EMBL-EBI CC BY 4.0.

### Security
- `infographics` caution: unstated skill license + prompts sent to external Google Gemini / Nano
  Banana image services. The other three unchanged (inductive-bio cleared vendor connector;
  allotrope/intact cleared Anthropic-provenance, real MIT/CC-BY licenses, no OSV advisories).

## 2026-07-27 (worklist maintenance — 4-page recheck, hypothesis-crucible → ica)

Worked the injected 4-page worklist top-to-bottom. All four were already `works/cleared` (stamped
2026-07-20, within cadence); rechecked against fresh source fetches — zero drift, no fixes. Stamps
refreshed to 2026-07-27. Catalog is now at full `verification:` coverage (459 total · 0 unstamped).

### Verified
- `hypothesis-crucible` works/cleared — first-party this repo; confirmed `crucible/.claude-plugin/
  plugin.json` (name `crucible`), `crucible/skills/forge/SKILL.md`, and the `crucible` entry in root
  `.claude-plugin/marketplace.json` so `/plugin install crucible` matches.
- `hypothesis-generation` works/cleared — `K-Dense-AI/scientific-agent-skills` MIT/not-archived/
  pushed 2026-07-27/31.9k★; `skills/hypothesis-generation/` holds SKILL.md (14767 B) + assets/
  references/scripts.
- `ibgnn` works/cleared — `CUHK-AIM-Group/NeuroClaw` MIT/not-archived/pushed 2026-07-26/76★;
  `skills/ibgnn/SKILL.md` (5587 B) resolves.
- `ica` works/cleared — same NeuroClaw anchor; `skills/ica/SKILL.md` (4275 B) resolves.

### Security
- All four cleared: provenance matches supplier, real licenses (MIT / first-party OSS), no OSV
  advisories, maintained. Skills execute locally via Bash/Python (no smoke target).

