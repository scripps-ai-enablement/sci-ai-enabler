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

## 2026-07-27 (worklist maintenance — 12 unstamped stamped, 13 rechecked, novomcp drift)

Worked the injected worklist top-to-bottom: stamped the 12 unstamped pages, then rechecked the 13
already-stamped pages (all 2026-07-20, within cadence). One real drift found on recheck: `novomcp`.

### Verified (newly stamped)
- `cdxml-toolkit` works/caution — PyPI `cdxml-toolkit` 0.5.17 MIT resolves; both the `cdxml-mcp`
  entry point and the `cdxml_toolkit.mcp_server` module launch are confirmed in PyPI metadata (the
  smoke `boot_error` was only because the dep resolver backtracked to 0.5.1, which lacks the entry
  point). Windows+ChemDraw-only so not smoke-testable. Provenance matches leehiufung911; single-
  maintainer Beta.
- `chimerax-mcp` works/caution — PyPI `chimerax-mcp` 0.1.1 MIT resolves; `chimerax-mcp` entry point
  confirmed. Needs GUI + separate ChimeraX install so not smoke-tested. Provenance matches mahynotch;
  early v0.1.1 single-maintainer (3★) + runs arbitrary scripts.
- `openfda-mcp-server` works/cleared — **smoke test passed this run** (`npx -y
  @cyanheads/openfda-mcp-server@latest` installed + booted v0.11.0 over stdio). `cyanheads` Apache-2.0,
  pushed 2026-07-27.
- `protein-mcp-server` works/cleared — npm `@cyanheads/protein-mcp-server` 0.4.0 Apache-2.0; bin
  `protein-mcp-server`→dist/index.js confirms the npx launch. Pushed 2026-07-03.
- `cms-datagov-mcp` works/caution — `clarifyhealth/cms-datagov-mcp-server` MIT; package.json bin
  `cms-datagov-mcp-server`→build/index.js confirms the npm-link launch. Clone-and-build so not
  smoke-tested; single-maintainer (1★) + stale (pushed 2025-12-02).
- `admetlab-mcp` degraded/caution — `ToxMCP/admetlab-mcp` Apache-2.0 resolves; uvicorn HTTP launch
  documented but not smoke-tested, and depends on the upstream ADMETlab 3.0 API the project notes is
  unstable. Not on PyPI, 2★ Beta.
- `amplicon-processing`, `repertoire-visualization`, `specificity-annotation`, `taxonomy-assignment`,
  `vdjtools-analysis` works/cleared — all anchor `GPTomics/bioSkills` MIT/not-archived/pushed
  2026-07-25/1084★; clone + copy install path current. Wrapped tools (DADA2/QIIME2/VDJtools/etc.) are
  separately-installed OSS.

### Fixed
- (none — `drug-pipeline-mcp` flagged rather than fixed; see below)

### Flagged
- `drug-pipeline-mcp` degraded/caution + `flagged:` — `DasClown/drug-pipeline-mcp` MIT repo resolves
  (pushed 2026-07-07) and the `git+https` source install works, but PyPI `drug-pipeline-mcp` returned
  404 on all three endpoints (JSON, simple index, project page) this run, so the documented `pip
  install drug-pipeline-mcp` / `uvx drug-pipeline-mcp` launch does NOT resolve despite the page's
  GA/PyPI claim. Curator: confirm the real PyPI package name or drop the pip/uvx blocks in favor of
  the git-source install.

### Security / drift
- `novomcp` still degraded/unknown but **note refreshed for a real change**: novomcp.com now points
  to a self-host repo `NovoMCP/novomcp` (pushed 2026-07-26, 2★) exposing a local `localhost:8018/mcp`
  endpoint — a shift from the prior closed-source-SaaS assessment. GitHub reports its license as
  NOASSERTION (site claims Apache-2.0). Launch command not yet confirmed against the README and the
  hosted FAVES tier stays application-gated, so kept degraded/unknown this run. Next run: fetch the
  repo README, confirm the self-host launch, and reconcile the LICENSE — likely flips toward
  works/caution if the self-host path checks out.

### Verified (rechecked, unchanged — within cadence, 2026-07-20 stamps left in place)
- `CUHK-AIM-Group/NeuroClaw` MIT/not-archived/pushed 2026-07-26/76★ → `nii2dcm`, `nibabel-skill`,
  `nilearn-tool`, `nifd-skill`, `neurostorm` works.
- `K-Dense-AI/scientific-agent-skills` MIT/not-archived/pushed 2026-07-27/31.9k★ → `neurokit2`,
  `neuropixels-analysis` works.
- `jaechang-hits/SciAgent-Skills` NOASSERTION-classifier-but-CC-BY-4.0-root/pushed 2026-07-24/284★ →
  `nnunet-segmentation` works/cleared.
- `stanislavjiricek/neuroflow` MIT/pushed 2026-06-04/6★ → `neuroflow` works/caution (unchanged).
- `magland/neurosift-mcps` no-LICENSE/pushed 2025-11-03/1★ → `neurosift` works/caution (unchanged).
- Anthropic first-party: `nextflow-development` (life-sciences), `npi-registry` (healthcare) works —
  unchanged.

## 2026-07-22 (worklist maintenance — selector loop broken, new window served, zero drift)

The selector finally **advanced past the stuck 25-page window**: this run's worklist was a fresh,
different slice (`ketcher` → `medical-terminologies-mcp`, 25 pages) — the same-date rotation the
maintainer added to `select_verify_targets.py`/the workflow is working. All 25 were already stamped
2026-07-20; rechecked top-to-bottom against fresh source fetches this run. **All 25 confirmed
unchanged, no fixes.** Left the existing 2026-07-20 stamps in place (within cadence, clean recheck).

### Verified (rechecked, unchanged)
- `epam/ketcher` Apache-2.0/not-archived/pushed 2026-07-22/845-star + Anthropic Claude Science
  connectors-and-skills doc → ketcher works/cleared.
- `CUHK-AIM-Group/NeuroClaw` MIT/not-archived/pushed 2026-07-14/76-star → kmeans + lggnn works/cleared.
- `GPTomics/bioSkills` MIT/not-archived/pushed 2026-07-18/1053-star → kraken-classification works/cleared.
- `K-Dense-AI/scientific-agent-skills` MIT/not-archived/pushed 2026-07-21/31.5k-star → lamindb,
  liteparse, literature-review, markdown-mermaid-writing, markitdown, matchms, matlab, matplotlib,
  medchem works/cleared; labarchive-integration + latchbio-integration + latex-posters works/caution
  (skill license unstated on page / external ELN-cloud credentials).
- `jaechang-hits/SciAgent-Skills` NOASSERTION-classifier-but-CC-BY-4.0-root/not-archived/pushed
  2026-06-15/279-star → libsbml-network-modeling, macs3-peak-calling, maxquant-proteomics,
  mdanalysis-trajectory, mdtraj-trajectory-analysis works/cleared.
- `dauparas/LigandMPNN` MIT/not-archived/pushed 2025-02-06/606-star + Claude Science skill → ligandmpnn works/cleared.
- `JonasRackl/labmate-mcp` MIT/2-star + PyPI `labmate-mcp` 7.3.1 MIT (launch `labmate-mcp` binary,
  no subcommand) → labmate-mcp works/caution (single-maintainer + optional third-party API keys).
- `scmcphub/liana-mcp` no-LICENSE/pushed 2025-06-27/1-star + PyPI `liana-mcp` 0.4.0 (launch
  `liana-mcp run` confirmed correct per scmcphub) → liana-mcp works/caution (unmaintained since 2025-06).
- `SidneyBissoli/medical-terminologies-mcp` MIT/pushed 2026-07-20/7-star + npm `medical-terminologies-mcp`
  1.5.7 MIT (bin → dist/index.js; launch `npx -y medical-terminologies-mcp`) → works/cleared.

Sources: GitHub repos API, PyPI JSON, npm registry, Anthropic Claude Science doc.

## 2026-07-20 (worklist maintenance batch #5 — same 25 pages rechecked, zero drift)

The selector re-served the identical worklist (`10x-genomics-cloud` → `autodock-vina-docking`, 25
pages) a **fifth** consecutive time. The catalog is uniformly dated 2026-07-20, so the
verified_on-oldest tie-break in `select_verify_targets.py` returns the same 25 slugs every run and
the pointer never advances. Rechecked top-to-bottom against fresh source fetches this run:
**all 25 confirmed unchanged, no fixes.**

### Verified (rechecked, unchanged)
- NeuroClaw `CUHK-AIM-Group/NeuroClaw` MIT/not-archived/pushed 2026-07-14/75-star → abcd/abide/
  adhd200/adni/aibl/aomic/asl works/cleared.
- K-Dense `K-Dense-AI/scientific-agent-skills` MIT/not-archived/pushed 2026-07-20/31.3k-star +
  this-run smoke pass (aeon/anndata/arboreto/astropy) → adaptyv works/caution; aeon/anndata/arboreto/
  astropy works/cleared.
- DeepMind `google-deepmind/science-skills` Apache-2.0/pushed 2026-07-07/2469-star → alphagenome
  degraded/cleared (signup-gated preview).
- `google-deepmind/alphafold` Apache-2.0/pushed 2026-04-22/14.7k-star → alphafold2 works/cleared.
- `GPTomics/bioSkills` MIT/pushed 2026-07-18/1042-star → amr-detection works/cleared.
- `Augmented-Nature/AlphaFold-MCP-Server` + `BioStudies-MCP-Server` both NOASSERTION/pushed
  2025-12-21 → alphafold + arrayexpress works/caution.
- SciAgent `jaechang-hits/SciAgent-Skills` NOASSERTION-classifier-but-CC-BY-4.0-root/pushed
  2026-06-15/278-star → archs4-database + autodock-vina-docking works/cleared.
- PyPI `arxiv-mcp-server` 0.5.1 Apache-2.0 + `aind-data-mcp` 0.4.5 MIT → arxiv/aind-data works/cleared.
- `MCPmed/allenbrain-mcp` no-LICENSE/pushed 2026-04-01/3-star → allenbrain degraded/caution.
- `anthropics/life-sciences` marketplace.json still lists `adisinsight` (Springer Nature) +
  `10x-genomics` → both degraded (subscription/paid gated); antibody-registry connector works/cleared.

### Fixed
- None (zero drift).

### Flagged
- Selector loop persists (fifth identical batch). Maintainer action needed: add a secondary
  tie-break to `select_verify_targets.py` or a rotating cursor in the workflow so runs serve
  different windows — otherwise ~420 pages never get rechecked while the count shows "complete."

### Security
- No provenance/license/advisory changes across the 25 anchors this run.

## 2026-07-20 (worklist maintenance batch #4 — same 25 pages rechecked, zero drift)

The selector re-served the identical worklist (`10x-genomics-cloud` → `autodock-vina-docking`, 25
pages) a **fourth** consecutive time. The catalog is uniformly dated 2026-07-20, so the
verified_on-oldest tie-break in `select_verify_targets.py` returns the same 25 slugs every run and
the pointer never advances. Rechecked top-to-bottom against fresh source fetches this run:
**all 25 confirmed unchanged, no fixes.**

### Verified (rechecked, unchanged)
- NeuroClaw `CUHK-AIM-Group/NeuroClaw` MIT/not-archived/pushed 2026-07-14/75-star → abcd/abide/
  adhd200/adni/aibl/aomic/asl works/cleared.
- K-Dense `K-Dense-AI/scientific-agent-skills` MIT/not-archived/pushed 2026-07-20/31.3k-star +
  this-run smoke pass (aeon/anndata/arboreto/astropy) → adaptyv works/caution; aeon/anndata/arboreto/
  astropy works/cleared.
- DeepMind `google-deepmind/science-skills` Apache-2.0/pushed 2026-07-07/2469-star → alphagenome
  degraded/cleared (not in life-sciences marketplace; signup-gated preview).
- `google-deepmind/alphafold` Apache-2.0/pushed 2026-04-22/14.7k-star → alphafold2 works/cleared.
- `GPTomics/bioSkills` MIT/pushed 2026-07-18/1042-star → amr-detection works/cleared.
- `Augmented-Nature/AlphaFold-MCP-Server` + `BioStudies-MCP-Server` both NOASSERTION/pushed
  2025-12-21 → alphafold + arrayexpress works/caution.
- SciAgent `jaechang-hits/SciAgent-Skills` NOASSERTION-classifier-but-CC-BY-4.0-root/pushed
  2026-06-15/278-star → archs4-database + autodock-vina-docking works/cleared.
- PyPI `arxiv-mcp-server` 0.5.1 Apache-2.0 + `aind-data-mcp` 0.4.5 MIT → arxiv/aind-data works/cleared.
- `MCPmed/allenbrain-mcp` no-LICENSE/pushed 2026-04-01/3-star → allenbrain degraded/caution.
- `anthropics/life-sciences` marketplace.json still lists `adisinsight` (Springer Nature) +
  `10x-genomics` → both degraded (subscription/paid gated). antibody-registry Anthropic connector
  unchanged (works/cleared).

### Flagged (maintainer)
- Selector loop confirmed a fourth time: the workflow keeps serving only these 25 pages while
  reporting a "complete" count, so ~420 catalog pages go unrechecked. The verifier cannot break the
  loop itself (must not bump `verified_on` past the run date; all pages already carry it). Needs a
  secondary tie-break in `select_verify_targets.py` (e.g. round-robin hash of slug against run
  date/commit) or a rotating cursor in the workflow.

