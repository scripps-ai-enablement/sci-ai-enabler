# Verifier changelog

Rolling, reverse-chronological log of catalog verification + security passes. Each scheduled or
on-demand run that produces changes prepends a dated block; the top block is mirrored to the pinned
"Verification updates" issue.

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
