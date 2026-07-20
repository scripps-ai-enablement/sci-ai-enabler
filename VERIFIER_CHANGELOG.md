# Verifier changelog

Rolling, reverse-chronological log of catalog verification + security passes. Each scheduled or
on-demand run that produces changes prepends a dated block; the top block is mirrored to the pinned
"Verification updates" issue.

## 2026-07-20 (bootstrap pass 16)

Sixteenth bootstrap pass — the final 12 unstamped `supplier: NeuroClaw` neuroimaging skills,
completing the entire NeuroClaw batch (37 pages across passes 15+16). All judgments grounded in
sources fetched this run.

### Verified
- 12 NeuroClaw `-skill` pages — works / cleared. Anchor `CUHK-AIM-Group/NeuroClaw` re-confirmed via
  the GitHub API (not archived, `disabled:false`, MIT, default branch `main`, pushed 2026-07-14,
  updated 2026-07-19, 75 stars, 0 open issues). All 12 skill dirs confirmed present via the
  `contents/skills` listing. Non-executable Skill-docs (Claude runs the skill's Python locally via
  Bash, not an MCP server) — graded `works` on the confirmed-current `git clone` +
  `cp -r NeuroClaw/skills/<slug>` install path. Slugs: `nsd-skill`, `oasis-skill`, `pet-skill`,
  `pnc-skill`, `ppmi-skill`, `rest-mneta-mdd-skill`, `seed-iv-skill`, `seed-vig-skill`, `smri-skill`,
  `tcp-skill`, `ucla-cnp-skill`, `ukb-skill`.

### Fixed
- None — no broken install targets or metadata in this batch.

### Flagged
- None.

### Security
- All 12 — cleared. Provenance matches the pages' `supplier: NeuroClaw` (all link to
  `CUHK-AIM-Group/NeuroClaw`); MIT license matches the pages' claim; repo actively maintained
  (pushed 2026-07-14); no OSV advisories for the skill collection. No smoke run for these
  (clone/copy Skill-docs).

## 2026-07-20 (bootstrap pass 15)

Fifteenth bootstrap pass — first batch of unstamped `supplier: NeuroClaw` neuroimaging skills.
All judgments grounded in sources fetched this run.

### Verified
- 25 NeuroClaw `-skill` pages — works / cleared. Anchor `CUHK-AIM-Group/NeuroClaw` (GitHub API:
  not archived, `disabled:false`, MIT, default branch `main`, pushed 2026-07-14, updated 2026-07-19,
  75 stars, 0 open issues). Every skill dir confirmed present via the `contents/skills` listing.
  These are non-executable Skill-docs (Claude runs the skill's Python locally via Bash, not an MCP
  server) — graded `works` on the confirmed-current `git clone` + `cp -r NeuroClaw/skills/<slug>`
  install path. Slugs: `abcd-skill`, `adni-skill`, `abide-skill`, `adhd200-skill`, `aibl-skill`,
  `aomic-skill`, `asl-skill`, `bold5000-skill`, `camcan-skill`, `cobre-skill`, `dmt-har-med-skill`,
  `dwi-skill`, `eeg-skill`, `fmri-skill`, `hbn-skill`, `nibabel-skill`, `nifd-skill`, `hcpd-skill`,
  `hcpep-skill`, `hcpa-skill`, `hcpya-skill`, `ixi-skill`, `meg-skill`, `mnd-skill`,
  `mschallenge-skill`.

### Fixed
- None — no broken install targets or metadata in this batch.

### Security
- All 25 — cleared. Provenance matches the pages' `supplier: NeuroClaw` (all link to
  `CUHK-AIM-Group/NeuroClaw`); committed root `LICENSE` is verbatim MIT ("Copyright (c) 2026
  zxcvb6958") matching the pages' MIT claim; repo is actively maintained (pushed 2026-07-14); no OSV
  advisories for a doc-only skill clone. No external-credential or non-commercial-data restrictions in
  this batch.

Caps respected (25 static verifications = 25 cap, 0 smoke verdicts consumed). 12 more unstamped
NeuroClaw `-skill` pages (`nsd`, `oasis`, `pet`, `pnc`, `ppmi`, `rest-mneta-mdd`, `seed-iv`,
`seed-vig`, `smri`, `tcp`, `ucla-cnp`, `ukb`) deferred to next run — all confirmed present in the
`contents/skills` listing, same anchor, ready to stamp with the same pattern.

## 2026-07-20 (bootstrap pass 14)

Fourteenth bootstrap pass — the 5 remaining unstamped `supplier: Google DeepMind` catalog pages.
All judgments grounded in sources fetched this run.

### Verified
- `alphafold2` — works / cleared. Anchor `google-deepmind/alphafold` (GitHub API: not archived,
  `disabled:false`, Apache-2.0, pushed 2026-04-22, 14,736 stars). The OSS `git clone` install path
  is confirmed-current; the Claude Science built-in path is Anthropic-hosted. Graded `works` on the
  confirmed-current clone path.
- `unibind-database`, `gtex-database`, `embl-ebi-ols`, `alphagenome` — degraded / cleared. Anchor
  `google-deepmind/science-skills` (GitHub API: not archived, Apache-2.0, pushed 2026-07-07, 2458
  stars). Each skill dir confirmed present via `contents/skills` (`unibind_database`, `gtex_database`,
  `embl_ebi_ols`, `alphagenome_single_variant_analysis`).

### Fixed
- `unibind-database`, `gtex-database`, `embl-ebi-ols`, `alphagenome` — each install block copied a
  now-nonexistent `skills/scienceskillscommon` dir (absent from the repo's `skills/` contents listing
  fetched this run). Each SKILL.md fetched from `raw.githubusercontent.com` shows no
  `scienceskillscommon` import — instead they instruct "Read the `uv` skill". Replaced the stale
  `cp -r science-skills/skills/scienceskillscommon` line with `cp -r science-skills/skills/uv` and
  corrected the parenthetical. Graded `degraded` (path auto-fixed this run), same pattern as the
  prior `pymol`/`foldseek-structural-search` fixes.

### Security
- `alphagenome` — cleared, but noted it ships `ALPHAGENOME_API_KEY` to the first-party Google
  DeepMind AlphaGenome API (same provenance as supplier; signup-gated non-commercial research
  preview). No provenance mismatch, so cleared rather than caution.

Caps respected (5 static verifications ≤25, 0 smoke verdicts consumed). Note: all 8 slugs in this
run's `.verify/smoke-results.json` (bci-mcp, instrument-data-to-allotrope, flowio,
foldseek-structural-search, nextflow-development, pymol, rdkit-skill, scikit-bio) were already
stamped and dated 2026-07-20; their smoke `pass` verdicts corroborate the existing stamps.

## 2026-07-20 (bootstrap pass 13)

Thirteenth bootstrap pass — SciAgent `-database` batch 2: 18 more unstamped `supplier: SciAgent`
database skill entries stamped. All judgments grounded in sources fetched this run: anchor repo
`jaechang-hits/SciAgent-Skills` (GitHub API — not archived, `disabled:false`, pushed 2026-06-15,
275 stars; classifier NOASSERTION but the committed root `LICENSE` fetched from
`raw.githubusercontent.com` is verbatim CC BY 4.0, commercial use + redistribution permitted). These
skills do **not** live under `skills/genomics-bioinformatics/databases/`; each was confirmed by
fetching its declared *parent* contents endpoint: `structural-biology-drug-discovery` (dailymed,
ddinter, emdb, fda, gtopdb, opentargets, unichem, zinc), `proteomics-protein-engineering` (hmdb,
interpro, metabolomics-workbench, pride), `systems-biology-multiomics` (brenda, reactome,
string-database-ppi), `scientific-writing` (biorxiv, openalex), `scientific-computing` (uspto). All
graded `works` on the confirmed-current install path (non-executable Skill-doc type). Caps respected
(18 static verifications ≤25, 0 smoke verdicts consumed).

### Verified
- works/cleared (17): `biorxiv-database`, `interpro-database`, `hmdb-database`, `gtopdb-database`, `emdb-database`, `brenda-database`, `unichem-database`, `uspto-database`, `zinc-database`, `reactome-database`, `pride-database`, `openalex-database`, `opentargets-database`, `metabolomics-workbench-database`, `dailymed-database`, `fda-database`, `string-database-ppi` — anchor repo live, each skill dir resolves via its parent contents fetch, skill code CC BY 4.0, public REST queries, no OSV advisories.
- works/caution (1): `ddinter-database` — resolves and install path current; DDInter data is CC BY-NC 4.0 (non-commercial per the NAR 2022/2025 papers), not the page's CC-BY-4.0.

### Fixed
- None this run.

### Flagged
- `ddinter-database` — security `caution`: skill code is CC BY 4.0 and provenance clears, but DDInter data is CC BY-NC 4.0 (non-commercial); the page's `Pricing` line claims CC-BY-4.0 (curator handoff to reconcile).

### Security
- 17 cleared (provenance matches `jaechang-hits/SciAgent-Skills`, skill code CC BY 4.0, open/public data licenses — CC0, CC BY 4.0, Apache-2.0, ODbL, public domain — no OSV advisories).
- 1 caution (`ddinter-database`, non-commercial data-source license).

## 2026-07-20 (bootstrap pass 12)

Twelfth bootstrap pass — first non-K-Dense batch: 19 unstamped `supplier: SciAgent` database skill
entries stamped. All judgments grounded in sources fetched this run: anchor repo
`jaechang-hits/SciAgent-Skills` (GitHub API — not archived, `disabled:false`, pushed 2026-06-15,
275 stars; GitHub's classifier reports NOASSERTION but the committed root `LICENSE` is verbatim
CC BY 4.0, permitting commercial use + redistribution), the `skills/genomics-bioinformatics/databases/`
contents listing (24 subdirs), each stamped `skills/genomics-bioinformatics/databases/<slug>` dir
confirmed via a direct contents-API fetch, and `.claude-plugin/marketplace.json` (plugin name
`sciagent-skills` matches the pages' `/plugin install sciagent-skills`). The `geo` page's second
install path (`geo-mcp`) was confirmed on PyPI (0.1.2, BSD-3-Clause, homepage `MCPmed/geomcp`).
Caps respected (19 static verifications ≤25, 0 smoke verdicts consumed — all smoke slugs already
stamped). `ensembl-database.md` has no catalog page (repo listing only) and was dropped.

### Verified
- works/cleared (17): `clinvar-database`, `dbsnp-database`, `archs4-database`, `gene-database`, `gnomad-database`, `gwas-database`, `jaspar-database`, `monarch-database`, `mouse-phenome-database`, `quickgo-database`, `regulomedb-database`, `remap-database`, `cbioportal-database`, `clinpgx-database`, `encode-database`, `ena-database`, `geo-database` — anchor repo live, each `skills/…/<slug>` resolves via a direct contents fetch, skill code CC BY 4.0, public no-auth REST queries, no OSV advisories. `geo-database` is dual-path (SciAgent skill + `geo-mcp` MCP, BSD-3-Clause).
- works/caution (2): `cosmic-database`, `kegg-database` — resolve and install paths current; underlying data-source license concern noted under Security.

### Fixed
- None this run.

### Flagged
- `cosmic-database` — security `caution`: skill code is CC BY 4.0 but COSMIC data is CC-BY-NC-SA-4.0 (non-commercial, registration required).
- `kegg-database` — security `caution`: skill code is CC BY 4.0 but KEGG data requires a paid commercial license for non-academic use.

### Security
- 17 cleared: SciAgent provenance matches supplier, real stated license (CC BY 4.0 root LICENSE), collection maintained (pushed 2026-06-15), public EBI/NCBI/portal REST queries with no install-time arbitrary-code or credential-exfiltration signals, no OSV advisories.
- Correction logged in verifier-state: the prior "SciAgent-Skills = NOASSERTION → caution" note is superseded — the committed root LICENSE is CC BY 4.0, so SciAgent skills clear on provenance/license by default; flag only where a page's underlying data source carries its own restriction. The two cautions above are data-use restrictions, not skill-code problems. Note also: the pages' `Pricing` lines describe the underlying *data-source* license, not the skill code.

## 2026-07-20 (bootstrap pass 11)

Eleventh bootstrap pass — 7 more unstamped K-Dense skill entries stamped. All judgments grounded in
sources fetched this run: anchor repo `K-Dense-AI/scientific-agent-skills` (GitHub API — MIT, not
archived, `disabled:false`, pushed 2026-07-15, updated 2026-07-20, 31,248 stars) and per-slug
`contents/skills/<slug>` fetches. These six slugs (`statistical-analysis`, `scikit-survival`,
`treatment-plans`, `usfiscaldata`, `venue-templates`, `what-if-oracle`) plus `iso-13485-certification`
had been deferred in a prior run as "not in the skills/ tree" — that was an artifact of a truncated,
summarized alphabetical listing. Each dir was confirmed to exist via an individual contents fetch
this run. Caps respected (7 static verifications, 0 smoke verdicts consumed).

### Verified
- works/cleared: `iso-13485-certification` (MIT), `statistical-analysis` (MIT), `treatment-plans` (MIT), `usfiscaldata` (MIT, keyless public U.S. Treasury Fiscal Data API), `venue-templates` (MIT), `scikit-survival` (MIT collection wrapping GPL-3.0 scikit-survival) — anchor repo live + each `skills/<slug>` resolves via a direct contents fetch; self-contained local execution, license stated, no OSV advisories.
- works/caution: `what-if-oracle` — resolves and install path current; license concern noted under Security.

### Fixed
- None this run.

### Flagged
- `what-if-oracle` — security `caution`: provenance/anchor clear, but the page states CC BY-NC-SA 4.0 (non-commercial, share-alike) while the collection root is MIT. The non-commercial clause limits reuse; recheck if K-Dense relicenses.

### Security
- Six of seven cleared: K-Dense-AI provenance matches supplier, real stated licenses (MIT; scikit-survival wraps GPL-3.0), collection maintained (pushed 2026-07-15), no OSV advisories, no install-time arbitrary-code or credential-exfiltration signals (`usfiscaldata` uses a keyless public government API).
- Correction logged in verifier-state: earlier "absent from skills/ tree" notes for these slugs (and for `scipy`/`seurat`/`squidpy`/etc.) were unreliable summarized-listing artifacts; future passes should confirm presence/absence with direct per-slug contents fetches.

## 2026-07-20 (bootstrap pass 10)

Tenth bootstrap pass — 16 more unstamped K-Dense skill entries stamped (the integration/utility
slugs deferred from pass 9). All judgments grounded in sources fetched this run: anchor repo
`K-Dense-AI/scientific-agent-skills` (GitHub API — MIT, not archived, `disabled:false`, pushed
2026-07-15, updated 2026-07-20, 31,247 stars) and the `skills/` contents API listing, which
confirmed each stamped subdir resolves (two fetches covering the alphabetical range). Caps
respected (16 static verifications, 0 smoke verdicts consumed — the 8/8-pass smoke batch was
already captured in pass 8). Honesty note: the second `skills/` contents fetch returned a
garbled/repeated tail past `scholar-evaluation`; those names were discarded and flagged in
verifier-state for a clean re-fetch. `benchling-integration` was already stamped works/cleared in a
prior run and was skipped.

### Verified
- works/cleared: `liteparse` (Apache-2.0), `markdown-mermaid-writing` (Apache-2.0), `polars-bio` (Apache-2.0), `pptx-posters` (MIT), `scholar-evaluation` (MIT), `pacsomatic` (MIT), `research-grants` (MIT) — anchor repo + each `skills/<slug>` resolves via contents API; self-contained local execution, license stated, no OSV advisories.
- works/caution: `research-lookup`, `open-notebook`, `modal`, `latex-posters`, `paper-lookup`, `parallel-web`, `infographics`, `ginkgo-cloud-lab`, `omero-integration`, `opentrons-integration`, `protocolsio-integration`, `labarchive-integration`, `latchbio-integration` — resolve and install path current; concerns noted under Security.

### Fixed
- None this run.

### Flagged
- `research-lookup` — security `caution`: MIT/provenance clear, but ships a user `PARALLEL_API_KEY` to api.parallel.ai and `OPENROUTER_API_KEY` to openrouter.ai (query text leaves the machine to external paid services).
- `open-notebook`, `modal` — security `caution`: MIT/Apache-2.0 clear, but `open-notebook` wires content to user-configured external AI providers and `modal` deploys user code/data to the external paid Modal cloud.
- `latex-posters`, `paper-lookup` — security `caution`: provenance clears and no external credentials, but the skill license is unstated on the page (collection root is MIT). Lift to cleared once a per-skill license is confirmed.
- `parallel-web`, `infographics` — security `caution`: skill license unstated on the page and each ships prompts/queries to an external service (parallel-cli web API; Google Gemini image services respectively).
- `ginkgo-cloud-lab`, `omero-integration`, `opentrons-integration`, `protocolsio-integration`, `labarchive-integration`, `latchbio-integration` — security `caution`: skill license unstated on the page and each authenticates to an external cloud/ELN service with user credentials. `opentrons-integration` wraps the local open Opentrons Protocol API; lift to cleared if a license is confirmed.

### Security
- No OSV/GitHub advisories surfaced for the anchor collection this run; all serious concerns are the credential/external-service and unstated-license cautions listed above. No provenance mismatches or typosquat-shaped names in this batch (all under `K-Dense-AI`).

## 2026-07-20 (bootstrap pass 9)

Ninth bootstrap pass — 16 more unstamped K-Dense skill entries stamped. All judgments grounded in
sources fetched this run: anchor repo `K-Dense-AI/scientific-agent-skills` (GitHub API — MIT, not
archived, `disabled:false`, pushed 2026-07-15, updated 2026-07-20, 31,246 stars) and the `skills/`
contents API listing, which confirmed each stamped subdir (`depmap`, `dnanexus-integration`,
`exa-search`, `fluidsim`, `generate-image`, `get-available-resources`, `imaging-data-commons`,
`matlab`, `molecular-dynamics`, `neuropixels-analysis`, `optimize-for-gpu`, `hugging-science`,
`pathway-enrichment`, `primekg`, `pufferlib`) resolves. Caps respected (16 static verifications, 0
smoke verdicts consumed — the 8/8-pass smoke batch was already captured in pass 8). Honesty note: a
second `skills/` contents fetch returned a garbled/repeated tail past `scholar-evaluation`; those
names were discarded and flagged in verifier-state for a clean re-fetch.

### Verified
- works/cleared: `depmap`, `get-available-resources`, `exploratory-data-analysis`, `fluidsim`, `pathway-enrichment`, `molecular-dynamics`, `imaging-data-commons`, `pufferlib`, `matlab`, `neuropixels-analysis` — anchor repo + each `skills/<slug>` resolves via contents API; MIT collection, local execution, no OSV advisories.
- works/caution: `primekg`, `optimize-for-gpu`, `hugging-science`, `dnanexus-integration`, `exa-search`, `generate-image` — resolve and install path current; concerns noted under Security.

### Fixed
- None this run.

### Flagged
- `generate-image`, `exa-search` — security `caution`: MIT/provenance clear, but each ships a user API key to an external service (FLUX/Nano Banana image services; the Exa web API respectively). Same external-credential pattern as `scientific-schematics`.
- `dnanexus-integration` — security `caution`: license unstated on the page and the skill uses DNAnexus cloud credentials via `dxpy`.
- `primekg`, `optimize-for-gpu`, `hugging-science` — security `caution`: each page states the skill/data license as unstated; `hugging-science` can also call the external HF Inference API. Lift to cleared once a license is confirmed.

### Security
- No OSV/GitHub advisories surfaced for the anchor collection this run; all serious concerns are the credential/external-service and unstated-license cautions listed above. No provenance mismatches or typosquat-shaped names in this batch (all under `K-Dense-AI`).

## 2026-07-20 (bootstrap pass 8)

Eighth bootstrap pass — 12 more unstamped K-Dense skill entries stamped, plus verification-note
refreshes on two already-stamped entries (`flowio`, `nextflow-development`) whose notes referenced
the prior run's sandbox `git ENOENT` failure. This cycle the smoke image resolved that: the safe
smoke batch shows `npx skills add K-Dense-AI/scientific-agent-skills` and
`npx skills add google-deepmind/science-skills/` both `pass` (8/8 pass in
`.verify/smoke-results.json`). All judgments grounded in sources fetched this run: anchor repo
`K-Dense-AI/scientific-agent-skills` (GitHub API — MIT, not archived, pushed 2026-07-15, updated
2026-07-20); the `skills/` contents API listing confirming each stamped subdir resolves; raw
`skills/pdf/LICENSE.txt`, `skills/docx/LICENSE.txt`, `skills/pptx/LICENSE.txt` (all "© 2025
Anthropic, PBC. All rights reserved"); `skills/pdf` / `skills/docx` / `skills/pptx` / `skills/markitdown`
contents listings; and `gcorso/DiffDock` (GitHub API — MIT, not archived) for the DiffDock model
provenance. Caps respected (12 static, 0 net-new smoke verdicts consumed beyond note refresh).

### Verified
- `esm`, `diffdock`, `geomaster`, `glycoengineering`, `hypogenic`, `hypothesis-generation`, `literature-review`, `peer-review`, `markitdown` → works — anchor repo + each `skills/<slug>` resolves via contents API; `diffdock` also resolves its upstream `gcorso/DiffDock` (MIT).
- `pdf`, `docx`, `pptx` → works — `skills/<slug>` resolves and install path current; license concern noted under Security.
- Note refresh (already works): `flowio`, `nextflow-development` — replaced the stale "smoke clone failed on sandbox missing git" caveat with this cycle's `npx skills add` smoke pass.

### Fixed
- None this run. (Note: `diffdock.md` Sources line still points to the old `K-Dense-AI/claude-skills` repo name in prose — left to the curator; the install block uses the current `scientific-agent-skills` path.)

### Flagged
- None broken. License-claim concerns captured under Security.

### Security
- cleared (9): `esm`, `diffdock`, `geomaster`, `glycoengineering`, `hypogenic`, `hypothesis-generation`, `literature-review`, `peer-review`, `markitdown` — K-Dense provenance matches supplier, MIT collection wrapping OSI-licensed upstream (or prompt-only), maintained (pushed 2026-07-15), no OSV advisories. `glycoengineering` note records it orchestrates external academic-licensed NetNGlyc/NetOGlyc (not redistributed, no keys). `markitdown` note records the skill dir ships no own LICENSE but the MIT repo umbrella covers it.
- caution (3): `pdf`, `docx`, `pptx` — each `skills/<slug>/LICENSE.txt` is Anthropic PBC proprietary ("© 2025 Anthropic, PBC. All rights reserved", no redistribution/derivatives) redistributed inside the MIT collection while the page claims Free/OSS (curator to fix the Pricing line, same pattern as `xlsx`). Provenance genuine (Anthropic document skills), no risky patterns.

## 2026-07-20 (bootstrap pass 7)

Seventh bootstrap pass — 13 more unstamped entries: 12 K-Dense skill wrappers plus the
Anthropic-supplied `scientific-problem-selection` skill. All judgments grounded in sources fetched
this run: the anchor repo `K-Dense-AI/scientific-agent-skills` (GitHub API — MIT, not archived,
pushed 2026-07-15, updated 2026-07-20) with per-slug `skills/<slug>` contents-API resolution;
`anthropics/life-sciences` (GitHub API — not archived, pushed 2026-05-08) and its documented plugin
listing for `scientific-problem-selection`; and the raw `skills/xlsx/LICENSE.txt` for the xlsx
license check. `.verify/smoke-results.json` for this run held only slugs already stamped in prior
passes (`bci-mcp`, `flowio`, `instrument-data-to-allotrope`, `nextflow-development`, `rdkit-skill`,
`scikit-bio`, plus already-fixed `pymol`/`foldseek-structural-search`), so no new smoke verdicts were
consumed; skill verification rests on the resolving subdir. Caps respected (13 static, 0
smoke-consuming).

### Verified
- `stable-baselines3`, `torchdrug`, `tiledbvcf`, `timesfm-forecasting` → works — anchor repo + each `skills/<slug>/SKILL.md` resolves via contents API.
- `scientific-writing`, `scientific-brainstorming`, `scientific-critical-thinking`, `scientific-schematics`, `scientific-slides`, `scientific-visualization` → works — anchor repo + each `skills/<slug>/SKILL.md` resolves.
- `xlsx` → works — `skills/xlsx/` resolves (install path current); license concern noted under Security.
- `scientific-problem-selection` → works — `anthropics/life-sciences` resolves and plugin `scientific-problem-selection@life-sciences` is documented with the page's exact install command.

### Fixed
- None this run.

### Flagged
- None broken. Provenance/license concerns captured under Security.

### Security
- cleared (9): `stable-baselines3`, `torchdrug`, `tiledbvcf`, `timesfm-forecasting`, `scientific-writing`, `scientific-brainstorming`, `scientific-critical-thinking`, `scientific-slides`, `scientific-visualization` — K-Dense provenance matches supplier, MIT collection wrapping OSI-licensed upstream (MIT/Apache-2.0 per entry) or prompt-only, maintained (pushed 2026-07-15), no OSV advisories via reachable sources.
- caution (4): `xlsx` — `skills/xlsx/LICENSE.txt` is Anthropic PBC proprietary ("© 2025 Anthropic, PBC. All rights reserved", no redistribution/derivatives) redistributed inside the MIT collection while the page claims Free/OSS (curator to fix Pricing). `scientific-schematics` — sends prompts plus a user API key to external Google Gemini ("Nano Banana 2" / Gemini 3.1 Pro) image services. `scientific-problem-selection` — official Anthropic provenance but repo carries no top-level LICENSE.

## 2026-07-20 (bootstrap pass 6)

Sixth bootstrap pass — 20 more unstamped entries: 15 K-Dense skill wrappers, the dual
Skill+MCP `rowan` entry, the Anthropic-supplied `scvi-tools` skill (with K-Dense alt), and three
K-Dense skills whose upstream license is unstated. All judgments grounded in sources fetched this
run: the anchor repo `K-Dense-AI/scientific-agent-skills` (GitHub API — MIT, not archived, pushed
2026-07-15) with per-slug `skills/<slug>` dir resolution; `anthropics/life-sciences` (GitHub API —
not archived, pushed 2026-05-08) for `scvi-tools`; and PyPI `rowan-mcp` (v2.3.2, MIT) plus the
`k-yenko/rowan-mcp` repo (no committed LICENSE) for `rowan`. Smoke clones still depend on `git`,
absent from the sandbox image, so skill verification rests on the resolving subdir rather than a
boot; noted per entry.

### Verified
- `pymoo`, `pydeseq2`, `pydicom`, `pyzotero`, `etetoolkit`, `histolab` → works — anchor repo + each `skills/<slug>` dir resolve.
- `pathml`, `geniml`, `matchms`, `molfeat`, `pytorch-lightning`, `pytdc`, `pylabrobot`, `lamindb`, `medchem` → works — anchor repo + each `skills/<slug>` dir resolve.
- `phylogenetics`, `gtars`, `pyhealth` → works — anchor repo + each `skills/<slug>` dir resolve (upstream license unstated; see Security).
- `scvi-tools` → works — `anthropics/life-sciences` repo resolves (not archived, pushed 2026-05-08) and the K-Dense alt `skills/scvi-tools` dir resolves.
- `rowan` → works — K-Dense `skills/rowan` dir resolves and `rowan-mcp` is on PyPI; both submit to the paid Rowan cloud platform and require `ROWAN_API_KEY` (free tier).

### Fixed
- None this run.

### Security
- cleared (16): `pymoo`, `pydeseq2`, `pydicom`, `pyzotero`, `etetoolkit`, `histolab`, `pathml`, `geniml`, `matchms`, `molfeat`, `pytorch-lightning`, `pytdc`, `pylabrobot`, `lamindb`, `medchem`, `scvi-tools` — provenance matches supplier, MIT/Anthropic collection wrapping OSI-licensed upstream (noted per entry), maintained, no OSV advisories via reachable sources.
- caution (4): `phylogenetics`, `gtars`, `pyhealth` — K-Dense provenance clears but each skill's own upstream library license is unstated; `rowan` — K-Dense skill clears but the `k-yenko/rowan-mcp` repo publishes no LICENSE and the tool ships a user API key to an external cloud service.

### Flagged
- None broken.

## 2026-07-20 (bootstrap pass 5)

Fifth bootstrap pass — 8 more unstamped K-Dense skill entries plus the `uniprot` MCP server. All
judgments grounded in sources fetched this run: the anchor repo `K-Dense-AI/scientific-agent-skills`
(GitHub API — MIT, not archived, pushed 2026-07-15, open_issues 38), a fresh GitHub tree listing of
its `skills/` directory (confirming each stamped skill's subdir, and confirming several assumed dirs
are absent — see below), and for `uniprot` the `Augmented-Nature-UniProt-MCP-Server` repo (GitHub
API), its `package.json`, and its committed `LICENSE`. The `npx skills add K-Dense-AI/...` CLI is
shown installing successfully in this run's `smoke-results.json`. OSV was not queryable (POST-only,
405 via WebFetch); advisories assessed as none-found via reachable sources.

### Verified
- `shap`, `umap-learn`, `zarr-python`, `transformers` → works — anchor repo + each `skills/<slug>` dir resolve; `npx skills add` CLI confirmed in smoke batch.
- `simpy`, `scvelo`, `torch-geometric`, `vaex` → works — anchor repo + each `skills/<slug>` dir resolve; `npx skills add` CLI confirmed in smoke batch.
- `uniprot` → works — `Augmented-Nature-UniProt-MCP-Server` repo resolves (page URL redirects to it); wraps public UniProt REST API, no auth.

### Fixed
- None this run (page install paths still resolve; `uniprot` license discrepancy is a supplier issue, flagged for the curator rather than edited in-page).

### Security
- cleared (8): `shap`, `umap-learn`, `zarr-python`, `transformers`, `simpy`, `scvelo`, `torch-geometric`, `vaex` — provenance matches supplier K-Dense-AI, MIT collection (wraps MIT/BSD-3/Apache-2.0 upstream, noted per entry), maintained (pushed 2026-07-15), no advisories via reachable sources.
- caution (1): `uniprot` — committed LICENSE is restrictive non-commercial ("personal, non-commercial use only", no redistribution/modification) while `package.json` and the catalog page both claim MIT; last push 2025-12-21 (~7mo stale).

### Flagged
- `uniprot` license discrepancy (see above) — recorded in `catalog/verifier-state.md` for the curator to reconcile the `Pricing` line.

### Notes
- Corrected a stale assumption in the deferred queue: dirs `scipy`, `seurat`, `squidpy`, `spatialdata`, `sqlalchemy`, `survival-analysis`, `structural-biology`, `systems-biology`, `tensorflow`, `torch` are NOT present in the K-Dense `skills/` tree; future runs must resolve any such catalog entry against its own supplier, not this anchor.

## 2026-07-20 (bootstrap pass 4)

Fourth bootstrap pass — 16 more unstamped K-Dense skill entries stamped (all static). All judgments
grounded in sources fetched this run: the anchor repo `K-Dense-AI/scientific-agent-skills` (GitHub
API — MIT, not archived, pushed 2026-07-15, open_issues 38) and a fresh GitHub contents listing of
its `skills/` directory, which lists each stamped skill's subdirectory. Smoke clones for these
depend on `git`, still missing from the sandbox image, so verification rests on the resolving
subdir rather than a boot; noted per entry.

### Verified
- `matplotlib`, `networkx`, `statsmodels`, `sympy`, `polars`, `seaborn` → works — anchor repo + each `skills/<slug>` dir resolve.
- `scikit-learn`, `pysam`, `qiskit`, `pennylane`, `qutip` → works — anchor repo + each `skills/<slug>` dir resolve.
- `pymc`, `pymatgen`, `geopandas`, `neurokit2`, `pyopenms` → works — anchor repo + each `skills/<slug>` dir resolve.

### Fixed
- None this run.

### Security
- cleared (16): `matplotlib`, `networkx`, `statsmodels`, `sympy`, `polars`, `seaborn`, `scikit-learn`, `pysam`, `qiskit`, `pennylane`, `qutip`, `pymc`, `pymatgen`, `geopandas`, `neurokit2`, `pyopenms` — provenance matches supplier K-Dense-AI, MIT collection (wrap BSD-3/MIT/Apache-2.0 upstream libs, noted per entry), maintained (pushed 2026-07-15), no OSV advisories.

### Flagged
- None broken.

## 2026-07-20 (bootstrap pass 3)

Third bootstrap pass — 21 K-Dense skill entries stamped (all static). All judgments grounded in
sources fetched this run: the anchor repo `K-Dense-AI/scientific-agent-skills` (GitHub API — MIT,
not archived, pushed 2026-07-15, LICENSE.md + SECURITY.md present) and its `skills/` git tree, which
lists each stamped skill's directory. Per-entry differentiator is the skill subdir resolving.

### Verified
- `astropy`, `cobrapy`, `deeptools`, `deepchem`, `aeon`, `arboreto`, `cirq`, `bioservices` → works — anchor repo + each `skills/<slug>` dir resolve.
- `bgpt-paper-search`, `bids`, `bulk-rnaseq`, `cellxgene-census`, `dask`, `database-lookup` → works — anchor repo + each `skills/<slug>` dir resolve.
- `benchling-integration`, `citation-management`, `clinical-decision-support`, `clinical-reports`, `consciousness-council` → works — anchor repo + each `skills/<slug>` dir resolve.
- `adaptyv`, `autoskill` → works — anchor repo + each `skills/<slug>` dir resolve (see Security).

### Fixed
- None this run.

### Security
- cleared (19): `astropy`, `cobrapy`, `deeptools`, `deepchem`, `aeon`, `arboreto`, `cirq`, `bioservices`, `bgpt-paper-search`, `bids`, `bulk-rnaseq`, `cellxgene-census`, `dask`, `database-lookup`, `benchling-integration`, `citation-management`, `clinical-decision-support`, `clinical-reports`, `consciousness-council` — provenance matches supplier K-Dense-AI, MIT collection (some wrap BSD-3/Apache-2.0/GPL upstream libs, noted per entry), maintained, no OSV advisories.
- caution (2): `adaptyv` (skill writes to a paid external Adaptyv wet-lab platform and handles an ADAPTYV_API_KEY; in-silico half runs unauthenticated); `autoskill` (skill observes the user's screen via a local screenpipe daemon — detection is local and only redacted summaries reach the LLM).

### Flagged
- None broken.

## 2026-07-20 (bootstrap pass 2)

Second bootstrap pass — 8 more entries stamped (all static). All judgments grounded in sources
fetched this run (GitHub/PyPI/npm APIs and GitHub Advisory/OSV search).

### Verified
- `arxiv` → works — `blazickjp/arxiv-mcp-server` (Apache-2.0, pushed 2026-05) and PyPI `arxiv-mcp-server` v0.5.0 resolve.
- `chembl` → works — `anthropics/life-sciences` marketplace repo resolves and is active (non-executable plugin/connector; path current).
- `clinicaltrials-gov-mcp` → works — `cyanheads/clinicaltrialsgov-mcp-server` (Apache-2.0, pushed 2026-07) and npm `clinicaltrialsgov-mcp-server` v2.8.2 resolve.
- `datamol` → works — `K-Dense-AI/scientific-agent-skills` (MIT) and PyPI `datamol` v0.12.5 resolve.
- `blast` → works — `bio-mcp/bio-mcp-blast` repo resolves (clone-and-install path current).
- `bcftools-variant-manipulation`, `autodock-vina-docking` → works — `jaechang-hits/SciAgent-Skills` (pushed 2026-06) and each skill dir resolve.
- `chemcp` → works — `scottmreed/ChemCP` repo resolves and npm `chemcp` v1.1.0 present.

### Security
- cleared: `arxiv` (Apache-2.0, provenance blazickjp), `chembl` (Anthropic-packaged), `clinicaltrials-gov-mcp` (Apache-2.0, provenance cyanheads), `datamol` (K-Dense-AI MIT + Datamol Apache-2.0) — provenance matches, real license, no OSV advisories.
- caution: `blast` (no LICENSE upstream despite MIT claim, unmaintained since 2025-06); `bcftools-variant-manipulation`, `autodock-vina-docking` (GitHub license NOASSERTION); `chemcp` (no LICENSE file in repo, npm metadata says ISC).

### Flagged
- None broken. Deferred for LICENSE recheck: `blast`, SciAgent-Skills NOASSERTION entries, `chemcp`.

## 2026-07-20

First bootstrap pass — 17 entries stamped (8 consuming smoke results, 9 static). All judgments
grounded in sources fetched this run (GitHub/PyPI/npm APIs, OSV list pages, `.verify/smoke-results.json`).

### Verified
- `bci-mcp` → works — smoke `pass`; PyPI+npm `bci-mcp` v0.1.3 and `enkhbold470/bci-mcp` (MIT) all resolve.
- `instrument-data-to-allotrope` → works — smoke `pass`; `anthropics/life-sciences` plugin dir resolves; `allotropy` v0.1.141 on PyPI.
- `flowio`, `rdkit-skill`, `scikit-bio`, `gget`, `biopython`, `anndata` → works — `K-Dense-AI/scientific-agent-skills` (MIT, pushed 2026-07-15) and each skill dir resolve. Smoke clone failed only on sandbox missing `git` (environmental, not tool) — noted in each `verification_note`.
- `nextflow-development` → works — `anthropics/life-sciences/nextflow-development` dir resolves.
- `biomcp` → works — PyPI `biomcp-cli` v0.8.25 and `biomcp-python` v0.7.3 (MIT, GenomOncology) resolve.
- `scanpy`, `cellrank-mcp`, `decoupler-mcp`, `liana-mcp` → works — scmcphub PyPI packages (v0.5.0/v0.4.0) and repos resolve.

### Fixed
- `pymol`, `foldseek-structural-search` → degraded — removed a stale `cp -r science-skills/skills/scienceskillscommon` install line (path 404s in `google-deepmind/science-skills`; SKILL.md does not import it). Skill dirs themselves resolve.

### Security
- cleared: `instrument-data-to-allotrope`, `flowio`, `rdkit-skill`, `scikit-bio`, `gget`, `biopython`, `anndata`, `nextflow-development`, `pymol`, `foldseek-structural-search`, `biomcp` — provenance matches supplier, real license, no OSV advisories, maintained.
- caution: `bci-mcp` (single-maintainer alpha); `scanpy`, `cellrank-mcp`, `decoupler-mcp`, `liana-mcp` (scmcphub repos unmaintained since 2025-06, several with no LICENSE file); `gromacs-mcp` (no repo LICENSE, alpha).

### Flagged
- None broken. Deferred for maintenance recheck: scmcphub ecosystem staleness; `gromacs-mcp` missing LICENSE.
- Infra note: smoke image lacks `git`, so all clone-based skill jobs returned `install_error` spuriously — add `git` to the smoke image before re-queuing them.

## 2026-07-18

### Added
- Bootstrapped the Verifier agent: `VERIFIER_AGENT.md`, the two-job `verify.yml` workflow
  (quarantined smoke-test job + sandboxed agent job), `scripts/select_smoke_targets.py` +
  `scripts/run_smoke_tests.py`, `catalog/verifier-state.md`, and the `verification` / `security`
  stamp schema (front-matter fields + metadata-table rows + area-card badges). No catalog entries
  stamped yet — the first bootstrap pass populates them.
