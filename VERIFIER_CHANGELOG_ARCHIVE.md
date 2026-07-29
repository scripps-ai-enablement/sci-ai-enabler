
# Verifier changelog archive

Older entries rotated out of [VERIFIER_CHANGELOG.md](VERIFIER_CHANGELOG.md). Newest first, same format.
## 2026-07-20 (worklist maintenance batch #2 — same 25 pages rechecked)

The selector re-served the identical worklist (`10x-genomics-cloud` → `autodock-vina-docking`, 25
pages) because these remain the 25 oldest `verified_on` (the whole catalog is now uniformly dated
2026-07-20). Rechecked top-to-bottom against fresh source fetches: 24 unchanged, 1 micro-fixed.

### Fixed
- arxiv — security_note version string 0.5.0→0.5.1. PyPI `arxiv-mcp-server` published 0.5.1 (still
  Apache-2.0; the `uvx arxiv-mcp-server` launch command is unchanged). Grade stays works/cleared.

### Verified (rechecked, unchanged)
- NeuroClaw `CUHK-AIM-Group/NeuroClaw` MIT/pushed 2026-07-14/75-star → abcd/abide/adhd200/adni/aibl/
  aomic/asl works/cleared.
- K-Dense `K-Dense-AI/scientific-agent-skills` MIT/pushed 2026-07-20/31.3k-star + this-run smoke pass
  → adaptyv works/caution; aeon/anndata/arboreto/astropy works/cleared.
- SciAgent `jaechang-hits/SciAgent-Skills` CC-BY-4.0-root/pushed 2026-06-15/278-star → archs4-database
  + autodock-vina-docking works/cleared.
- `google-deepmind/alphafold` Apache-2.0/14.7k-star → alphafold2 works/cleared;
  `google-deepmind/science-skills` Apache-2.0/pushed 2026-07-07 → alphagenome degraded/cleared.
- `GPTomics/bioSkills` MIT/pushed 2026-07-18 → amr-detection works/cleared.
- `Augmented-Nature/AlphaFold-MCP-Server` + `BioStudies-MCP-Server` (both NOASSERTION/no-real-LICENSE,
  pushed 2025-12-21) → alphafold + arrayexpress works/caution.
- PyPI `aind-data-mcp` 0.4.5 MIT → aind-data works/cleared.
- `MCPmed/allenbrain-mcp` no-LICENSE/Alpha → allenbrain degraded/caution.
- `anthropics/life-sciences` marketplace still lists adisinsight + 10x-genomics → both degraded
  (subscription/paid-account gated); antibody-registry Anthropic connector works/cleared.

## 2026-07-20 (worklist maintenance batch — 25 pages rechecked)

Worked the injected worklist (`10x-genomics-cloud` → `autodock-vina-docking`, 25 pages) top-to-bottom.
Every entry was already stamped 2026-07-20, so this was a recheck grounded on fresh source fetches:
24 confirmed unchanged, 1 fixed.

### Fixed
- autodock-vina-docking — security caution→cleared. The note still cited GitHub's NOASSERTION
  license classifier, but the committed SciAgent-Skills root LICENSE is verbatim CC BY 4.0
  (supersedes the NOASSERTION caution, same basis as the already-cleared sibling `archs4-database`).

### Verified (rechecked, unchanged)
- NeuroClaw `CUHK-AIM-Group/NeuroClaw` MIT/pushed 2026-07-14/75-star → abcd/abide/adhd200/adni/aibl/
  aomic/asl skills works/cleared.
- K-Dense `K-Dense-AI/scientific-agent-skills` MIT/pushed 2026-07-20/31.3k-star + smoke pass →
  adaptyv works/caution; aeon/anndata/arboreto/astropy works/cleared.
- SciAgent `jaechang-hits/SciAgent-Skills` CC-BY-4.0-root/pushed 2026-06-15/278-star → archs4-database
  + autodock works/cleared.
- PyPI `arxiv-mcp-server` 0.5.0 Apache-2.0 → arxiv works/cleared; `aind-data-mcp` 0.4.5 MIT →
  aind-data works/cleared.
- `GPTomics/bioSkills` MIT/pushed 2026-07-18 → amr-detection works/cleared.
- `google-deepmind/alphafold` Apache-2.0/14.7k-star → alphafold2 works/cleared;
  `google-deepmind/science-skills` Apache-2.0/pushed 2026-07-07 → alphagenome degraded/cleared.
- `Augmented-Nature/AlphaFold-MCP-Server` (restrictive, NOASSERTION) → alphafold works/caution;
  `BioStudies-MCP-Server` (no LICENSE) → arrayexpress works/caution.
- `MCPmed/allenbrain-mcp` (transfer confirmed, no LICENSE) → allenbrain degraded/caution.
- `anthropics/life-sciences` marketplace still lists `adisinsight` + `10x-genomics` → both degraded
  (subscription/paid-account gated). antibody-registry Research Resources connector works/cleared.

## 2026-07-20 (launch-command sweep — verifier check hardened)

New static check in `VERIFIER_AGENT.md`: resolving the install target is no longer sufficient for
`works` — the launch invocation the user actually runs (the subcommand/args after
`claude mcp add <name> ... --`, and the `command`/`args` in a `mcpServers` block) must be confirmed
against a primary source (README / CLI `--help` / MCP-server reference), not the PyPI/npm page. This
closes the blind spot that stamped BioMCP `works` with a dead `biomcp run` command: the package
resolved, and BioMCP was smoke-excluded (its page mentions optional API keys, which the smoke gate
denylist treats as auth-gated), so nothing ever exercised the invocation.

### Fixed
- biomcp — `biomcp run` is not a real subcommand. PyPI `biomcp-cli`/`biomcp-python` resolve, but the
  CLI exposes `serve` (canonical) with `mcp` as a legacy alias (biomcp.org MCP-server reference).
  Corrected all four occurrences (Claude Code `claude mcp add` line + the uv variant + both
  `claude_desktop_config.json` `args`) from `run` to `serve`.

### Verified
- biomcp — works→degraded/cleared. Launch command auto-fixed this run (⇒ degraded per rubric);
  flips back to works on the next clean recheck. Security unchanged (cleared).
- Launch-command sweep, confirmed CORRECT (no change): scmcphub `scanpy-mcp`/`liana-mcp`/
  `decoupler-mcp`/`cellrank-mcp` all genuinely document `run`; `bci-mcp serve`; `rdkit-agent mcp`;
  `chatspatial ... -m chatspatial server`; `scitex mcp start`. `run` is a legitimate verb for
  scmcphub — the check validates the actual token against upstream docs, it does not pattern-match
  the verb, so these produced no false positives.

## 2026-07-20 (worklist batch — 7 unstamped stamped)

Stamped the 7 UNSTAMPED worklist pages, each grounded on a source fetched this run; rechecked the
8 already-stamped worklist items against fresh source fetches and left them at their existing
2026-07-20 grades. Two in-page license fixes on the Augmented-Nature MCP-server family.

### Verified
- mygene — works/cleared. `longevity-genie/biothings-mcp` MIT + PyPI `biothings-mcp` 0.1.6; read-only public MyGene.info API.
- alphafold — works/caution. `Augmented-Nature/AlphaFold-MCP-Server` resolves (35-star, not archived); EBI AlphaFold API public read-only.
- gene-ontology — works/caution. `Augmented-Nature/GeneOntology-MCP-Server` resolves (8-star, not archived); GO API public read-only.
- brian2 — works/caution. `HughYau/neuroforge-skills` + `skills/brian2/SKILL.md` confirmed; GitHub license null vs page MIT claim, single-maintainer/4-star, stale (2026-02-24).
- clinical-trial-protocol — works/caution. First-party Anthropic; `healthcare` + `clinical-trial-protocol` plugins confirmed in `anthropics/healthcare` marketplace.json; repo has no top-level LICENSE.
- cms-coverage — works/caution. First-party Anthropic; `healthcare` + `cms-coverage` plugins confirmed in marketplace.json; hosted read-only CMS endpoint; repo has no top-level LICENSE.
- biorender — degraded/cleared. `biorender` plugin confirmed in `anthropics/life-sciences` marketplace.json; vendor-hosted remote MCP requires BioRender OAuth login so boot unverifiable without an account.
- Rechecked unchanged: NeuroClaw source `CUHK-AIM-Group/NeuroClaw` MIT/maintained (pushed 2026-07-14, 75-star) backs abcd/abide/adhd200/adni-skill (works/cleared); K-Dense `K-Dense-AI/scientific-agent-skills` MIT/maintained (pushed 2026-07-20, 31k-star, smoke-installable) backs adaptyv (works/caution) + aeon (works/cleared); adisinsight + 10x-genomics-cloud stay degraded (subscription/paid-account gated).

### Fixed
- alphafold — `Pricing` row corrected: the wrapper repo LICENSE is a restrictive personal non-commercial grant (GitHub NOASSERTION), NOT the MIT the page claimed.
- gene-ontology — `Pricing` row corrected to distinguish CC-BY GO *data* from the restrictive non-commercial wrapper *code* (page previously implied OSS for the wrapper).

### Security
- alphafold, gene-ontology — caution. Same restrictive non-commercial LICENSE pattern as `uniprot`/`human-protein-atlas` across the Augmented-Nature MCP-server family; treat any `Augmented-Nature/*-MCP-Server` MIT/OSS claim as suspect and fetch its raw LICENSE.
- brian2 — caution. GitHub license null vs page MIT claim; single-maintainer, stale.
- clinical-trial-protocol, cms-coverage — caution. `anthropics/healthcare` repo has no top-level LICENSE despite Free/OSS claim (same pattern as prior-auth-review/icd-10-codes).

### Flagged
- alphafold, gene-ontology — added to Flagged as Augmented-Nature license-mismatch entries; Pricing fixed in-page, curator owns any further wording.

## 2026-07-20 (maintenance recheck pass 3 — bootstrap complete)

Third post-enumeration cadence recheck of the open degraded/broken/flagged tail, plus two
staleness-cadence caution items. Re-fetched every priority item live this run; none changed grade.
Only edit is an evidence refresh on `openneuro` (now a fourth consecutive 404 run). All 440 pages
carry `^verification:`.

### Verified
- openneuro — broken/caution/flagged (unchanged grade; note refreshed). `api.github.com/repos/QuentinCody/open-neuro-mcp-server`
  and the hosted `open-neuro-mcp-server.quentincody.workers.dev/sse` endpoint both 404 again — fourth
  consecutive 404 run. Bumped verification_note + flagged field + Verified table row from "third" to
  "fourth consecutive run". Curator: strong signal to remove or replace the entry.
- glygen — degraded/caution (unchanged). Hosted `mcp.glygen.org/mcp` still 503 this run.
- open-targets — degraded/caution (unchanged). Official source repo `opentargets/platform-mcp` still
  Apache-2.0, not archived, pushed 2026-07-01; official endpoint still untestable via GET WebFetch.
- covasyn — degraded/caution (unchanged). npm `@covasyn/mcp-client` still 0 results on the registry search.
- morning — degraded/unknown (unchanged). Still no `morning` dir in `anthropics/skills/skills/` (17 dirs listed, none named morning).
- scanpy — works/caution (unchanged). `scmcphub/scanpy-mcp` BSD-3, pushed 2025-06-27 (~13mo stale); note already accurate.
- blast — works/caution (unchanged). `bio-mcp/bio-mcp-blast` license null, pushed 2025-06-29; note already accurate.

### Flagged
- openneuro — flagged field refreshed to cite four consecutive 404 runs (repo + hosted endpoint); strong hand-off signal to curator for removal/replacement.

## 2026-07-20 (maintenance recheck pass 2 — bootstrap complete)

Second post-enumeration cadence recheck of the open degraded/broken/flagged tail. Re-fetched the
five priority items live this run; none changed grade. Only edit is an evidence refresh on
`openneuro` (now a third consecutive 404 run). All 440 pages carry `^verification:`.

### Verified
- openneuro — broken/caution/flagged (unchanged grade; note refreshed). `api.github.com/repos/QuentinCody/open-neuro-mcp-server`
  and the hosted `open-neuro-mcp-server.quentincody.workers.dev/sse` endpoint both 404 again — third
  consecutive 404 run. Bumped verification_note + flagged field + Verified table row from "second" to
  "third consecutive run". Curator: remove or replace the entry.
- glygen — degraded/caution (unchanged). Hosted `mcp.glygen.org/mcp` still 503 this run.
- open-targets — degraded/caution (unchanged). Official source repo `opentargets/platform-mcp` still
  Apache-2.0, not archived, pushed 2026-07-01; official endpoint still untestable via GET WebFetch.
- covasyn — degraded/caution (unchanged). npm `@covasyn/mcp-client` still 0 results on the registry search.
- morning — degraded/unknown (unchanged). Still no `morning` dir in `anthropics/skills/skills/` (17 dirs listed, none named morning).

### Flagged
- openneuro — flagged field refreshed to cite three consecutive 404 runs (repo + hosted endpoint); hand off to curator for removal/replacement.

## 2026-07-20 (maintenance recheck — bootstrap complete)

First post-enumeration maintenance recheck of the degraded/flagged tail (all 440 pages already carry
`^verification:`). One regrade, several confirmed-unchanged rechecks, and two smoke-note refreshes.
Every judgment grounded in a live fetch this run (GitHub repos API, npm registry search, and direct
endpoint fetches) plus the handed-in `.verify/smoke-results.json` (8/8 pass). No new smoke run
initiated by the verifier.

### Verified
- rdkit-skill — works/cleared (note refreshed). This run's smoke batch installed the K-Dense
  collection via `npx skills add K-Dense-AI/scientific-agent-skills` (pass); replaced the stale
  "smoke clone failed on sandbox missing git" note.
- scikit-bio — works/cleared (note refreshed). Same K-Dense `npx skills add` smoke pass; replaced the
  stale git-ENOENT note.
- glygen — degraded/caution (unchanged). Hosted `mcp.glygen.org/mcp` still returns 503 this run; the
  self-host repo `glygener/glygen-mcp-server` remains current, so boot stays unverified.
- open-targets — degraded/caution (unchanged). Official source repo `opentargets/open-targets-platform-mcp`
  redirects to `opentargets/platform-mcp` (Apache-2.0, pushed 2026-07-01, not archived); the community
  fallback `Augmented-Nature/OpenTargets-MCP-Server` is unchanged (NOASSERTION, 11 stars, pushed
  2025-12-21). Official endpoint `initialize` still untestable via GET WebFetch.
- covasyn — degraded/caution (unchanged). Hosted `mcp.covasyn.com/mcp` reachable (406, API-key gated);
  npm `@covasyn/mcp-client` still returns 0 results on the registry search — stdio client package name
  still unconfirmable.

### Flagged
- openneuro — **regraded degraded → broken**, `flagged:` field set. `api.github.com/repos/QuentinCody/open-neuro-mcp-server`,
  the repo web page, AND the hosted `open-neuro-mcp-server.quentincody.workers.dev/sse` endpoint all
  returned 404 again this run — the second consecutive 404 run — so there is no working install path.
  Unofficial community wrapper (not endorsed by OpenNeuro). Handed to the curator for removal/replacement.

### Security
- No security-grade changes this run. openneuro stays `caution` (unofficial wrapper, unreachable so
  license/maintenance unconfirmable against a live source).

## 2026-07-20 (bootstrap pass 30)

Thirtieth bootstrap pass — **16 pages stamped**, clearing the final unstamped remainder of the catalog
(Anthropic first-party healthcare/connector entries, standalone MCP servers, and a couple of
lab/first-party skills + plugins). Each judgment grounded in a source fetched this run (GitHub repo +
contents APIs, PyPI + npm registry JSON, and the `anthropics/healthcare` / `anthropics/life-sciences` /
`anthropics/knowledge-work-plugins` marketplace manifests). 8 works/cleared, 6 works/caution, 2
degraded. No smoke run consumed. Enumeration lesson: Grep `count` output_mode gives false "Found 0"
for line-1 matches — used LS for the full untruncated `catalog/tools/` listing then read candidate
headers directly (Task/subagent 404'd on the sonnet model). Stamped strictly sequentially
(read-then-two-single-Edits per file).

### Verified
- npi-registry — works/cleared. First-party Anthropic hosted connector; `npi-registry` confirmed in
  the `anthropics/healthcare` marketplace.json; read-only over the public CMS NPPES API.
- pubmed — works/cleared. First-party Anthropic hosted connector; `pubmed` confirmed in the
  `anthropics/life-sciences` marketplace.json; read-only over the public NCBI E-utilities.
- fhir-wso2 — works/cleared. `wso2/fhir-mcp-server` Apache-2.0 (pushed 2026-07-14) + PyPI
  `fhir-mcp-server` 0.10.0 Apache-2.0; WSO2 org provenance.
- proto-okn — works/cleared. `sbl-sdsc/mcp-proto-okn` BSD-3-Clause, maintained; read-only SPARQL over
  public knowledge graphs; SDSC provenance.
- aind-data — works/cleared. Allen Institute `AllenNeuralDynamics/aind-data-mcp` MIT (maintained) +
  PyPI `aind-data-mcp` 0.4.5 MIT; read-only over the AIND DocDB.
- mhc-binding-prediction — works/cleared. `GPTomics/bioSkills` MIT (pushed 2026-07-18); local skill
  running user-installed predictors; no OSV advisories.
- drug-repurposing — works/cleared. `mims-harvard/ToolUniverse` Apache-2.0 (pushed 2026-07-20);
  read-only over public APIs; Zitnik Lab provenance.
- hypothesis-crucible — works/cleared. First-party this repo; `crucible/.claude-plugin` + `skills`
  dirs confirmed via contents API; actively maintained.
- fraud-detection — works/caution. First-party `anthropics/healthcare`, skill dir confirmed via
  contents API, but repo has no top-level LICENSE despite Free/OSS claim and it handles claims data.
- procedure-coding — works/caution. First-party `anthropics/healthcare`, skill dir confirmed, but repo
  has no top-level LICENSE.
- clinical-note-extract — works/caution. First-party `anthropics/healthcare`, skill dir confirmed, but
  repo has no top-level LICENSE and it processes clinical notes.
- openfda — works/caution. `ythalorossy/openfda` + npm `@ythalorossy/openfda` 1.0.19 MIT; provenance
  matches but single-maintainer community package (4 stars) and reads an API key from env.
- cbioportal — works/caution. `cBioPortal/cbioportal-mcp` official + maintained (pushed 2026-07-17),
  read-only, no OSV advisories, but no SPDX LICENSE file despite the Free/OSS claim.
- arrayexpress — works/caution. `Augmented-Nature/BioStudies-MCP-Server` resolves, read-only, no OSV
  advisories, but no LICENSE file and the repo is unmaintained since 2025-12 (community, 2 stars).
- bio-research — degraded. Plugin resolves in `anthropics/knowledge-work-plugins` (Apache-2.0,
  maintained), but open bug anthropics/claude-code#40106 breaks bundled MCP tools in Claude Code.
- 10x-genomics-cloud — degraded. `10x-genomics` plugin confirmed in the `anthropics/life-sciences`
  manifest, but a paid 10x Cloud account + token gate functional use, and it is a closed-source vendor
  binary that cannot be statically assessed.

### Fixed
- None this run.

### Flagged
- arrayexpress, cbioportal, openfda, fraud-detection, procedure-coding, clinical-note-extract →
  security caution (license/maintenance/data-handling signals — see state file). bio-research and
  10x-genomics-cloud → degraded verification (upstream bug / paid-account gate).

### Security
- No OSV advisories surfaced for any repo checked this run. Recurring caution driver: first-party
  `anthropics/healthcare` skills ship without a top-level LICENSE despite Free/OSS claims — lift to
  cleared when a LICENSE lands.

## 2026-07-20 (bootstrap pass 29)

Twenty-ninth bootstrap pass — **12 pages stamped**, clearing the previously-deferred tail of
unstamped pages (MCP servers + Claude Skills + Claude Code plugins). Each judgment grounded in a
source fetched this run (GitHub repo + contents APIs, PyPI + npm registry JSON, the
`anthropics/life-sciences` and `anthropics/healthcare` marketplace manifests, the Claude Science
connectors-and-skills doc, and the live `hcls.mcp.claude.com/icd10_codes/mcp` + OpenNeuro endpoints).
5 works/cleared, 4 works/caution, 3 degraded. No smoke run consumed for these (the 8/8-pass smoke
batch maps to already-stamped or interactive-picker targets). Stamped strictly sequentially
(read-then-two-single-Edits per file; the Read cache invalidates across files as expected).

### Verified
- tcr-epitope-binding — works/cleared. `GPTomics/bioSkills` MIT (GitHub API); `immunoinformatics/tcr-epitope-binding`
  dir + SKILL.md confirmed via contents API; read-only local clustering/lookup workflow.
- single-cell-rna-qc — works/cleared. First-party Anthropic; `single-cell-rna-qc` confirmed in the
  `anthropics/life-sciences` marketplace.json this run; read-into-local QC skill.
- pdbe — works/cleared. `PDBeurope/pdbe-mcp-servers` Apache-2.0 (pushed 2026-07-16) + PyPI
  `pdbe-mcp-server` 1.1.5 Apache-2.0; PDBe/EMBL-EBI provenance; keyless read-only API/Search servers.
- medical-terminologies-mcp — works/cleared. `SidneyBissoli/medical-terminologies-mcp` MIT (pushed
  2026-07-06) + npm `medical-terminologies-mcp` 1.5.7 MIT; provenance matches; read-only.
- indication-dossier — works/cleared. First-party Anthropic; listed by name in the claude.com Claude
  Science connectors-and-skills doc; orchestrates existing connectors, no extra credentials.
- pynibs — works/caution. `HughYau/neuroforge-skills` resolves and `skills/pynibs` dir confirmed, but
  GitHub license null vs page MIT claim; single-maintainer/4-star; stale (pushed 2026-02-24).
- ontology-lookup-service — works/caution. `seandavi/ols-mcp-server` resolves (26 stars) but GitHub
  license null (page claims Free/OSS) and stale (pushed 2025-07-16).
- prior-auth-review — works/caution. First-party Anthropic, confirmed in `anthropics/healthcare`
  manifest (consolidated `healthcare` plugin + `prior-auth` skill dir), but repo has no top-level
  LICENSE; reads/drafts clinical PA documents.
- icd-10-codes — works/caution. First-party Anthropic, `icd10-codes` in the healthcare manifest and
  hosted endpoint reachable (405-to-GET as expected), but repo has no top-level LICENSE.
- open-targets — degraded. Plugin resolves in the life-sciences manifest but official MCP endpoint
  still fails `initialize` (existing flag); documented `Augmented-Nature/OpenTargets-MCP-Server`
  fallback builds/handshakes.
- openneuro — degraded. `QuentinCody/open-neuro-mcp-server` GitHub repo AND the hosted
  `*.workers.dev/sse` endpoint both returned 404 on live fetch this run; install path unconfirmed.
- morning — degraded. Neither `anthropics/skills/skills/` (no `morning` dir) nor the Claude Science
  doc lists the skill this run; install path unresolvable.

### Fixed
- None this run (no in-page fixes; the pdbe PyPI version drift 1.1.4→1.1.5 is cosmetic — the `uvx
  pdbe-mcp-server` install path is unpinned and resolves regardless, so left to the curator).

### Flagged
- open-targets, openneuro, morning → verification `degraded` (see Security/Verified above). openneuro
  flagged for recheck: if repo + endpoint remain 404 next run, grade broken and set `flagged:`.
  morning flagged for the curator to reconcile its install path or Claude Science claim.

### Security
- caution: pynibs (no LICENSE + stale), ontology-lookup-service (no LICENSE + stale),
  prior-auth-review + icd-10-codes (no repo LICENSE; prior-auth handles clinical docs), open-targets
  (working fallback is NOASSERTION Augmented-Nature wrapper), openneuro (unofficial wrapper,
  unreachable this run). unknown: morning (skill not locatable to assess). cleared: tcr-epitope-binding,
  single-cell-rna-qc, pdbe, medical-terminologies-mcp, indication-dossier.

## 2026-07-20 (bootstrap pass 28)

Twenty-eighth bootstrap pass — **12 pages stamped**, a mixed MCP server / Claude Skill / plugin /
connector batch of unstamped pages. Each judgment grounded in a source fetched this run (GitHub repo
+ contents + security-advisories APIs, PyPI JSON, the Anthropic `anthropics/healthcare` marketplace
manifest, the Claude Science connectors doc, and the live `mcp.glygen.org/mcp` endpoint). 5
works/cleared, 6 works/caution, 1 degraded/caution. No smoke run consumed (the smoke batch maps to
already-stamped pages). Stamped strictly sequentially (read-then-two-single-Edits per file).

### Verified
- ligandmpnn — works/cleared. Baker Lab `dauparas/LigandMPNN` MIT (GitHub API); featured Claude
  Science skill; local inference, no credentials.
- ensembl — works/cleared. `effieklimi/ensembl-mcp-server` MIT; read-only public Ensembl REST API;
  featured Claude Science Genomes connector.
- fhir-developer — works/cleared. First-party Anthropic; `anthropics/healthcare` marketplace
  manifest confirms the consolidated `healthcare` plugin this run; local authoring, no credentials.
- kraken-classification — works/cleared. `GPTomics/bioSkills` MIT; `metagenomics/kraken-classification`
  SKILL.md confirmed via contents API; local Bash workflow wrapping bioconda tools.
- immcantation-analysis — works/cleared. `GPTomics/bioSkills` MIT; `tcr-bcr-analysis/immcantation-analysis`
  SKILL.md confirmed; local R/Python workflow over the open-source Immcantation suite.
- esmfold — works/caution. `facebookresearch/esm` MIT but repo ARCHIVED/unmaintained (Meta moved ESM
  to EvolutionaryScale); featured Claude Science skill.
- gwas-mcp — works/caution. PyPI `gwas-mcp` 1.0.2 MIT resolves but GitHub canonical owner is
  `muslus/gwas-mcp` (page cites zaeyasa); single-maintainer/1-star, stale 2026-02-09.
- encode-toolkit — works/caution. `ammawla/encode-toolkit` + PyPI 0.3.0 AGPL-3.0-only copyleft;
  maintained (pushed 2026-07-19); unaffiliated community project.
- human-protein-atlas — works/caution. `Augmented-Nature/ProteinAtlas-MCP-Server` LICENSE is a
  restrictive personal non-commercial grant (NOASSERTION), NOT the MIT the page claimed.
- fhir-momentum — works/caution. `the-momentum/fhir-mcp-server` MIT/maintained but write-capable over
  PHI and document/search tools ship clinical data to a third-party Pinecone account.
- mixcr-analysis — works/caution. `GPTomics/bioSkills` MIT, dir confirmed, but the required MiXCR
  binary is separately licensed (free academic/non-commercial only).
- glygen — degraded/caution. Self-host `glygener/glygen-mcp-server` current (pushed 2026-07-15) but
  hosted `mcp.glygen.org/mcp` returned 503 this run so boot unverified; wrapper repo has no LICENSE.

### Fixed
- human-protein-atlas — corrected the false MIT claim in both the `Pricing` table row and the `Notes`
  paragraph to state the repo's actual restrictive personal, non-commercial LICENSE.

### Security
- cleared: ligandmpnn, ensembl, fhir-developer, kraken-classification, immcantation-analysis.
- caution: esmfold (archived), gwas-mcp (owner mismatch + stale), encode-toolkit (AGPL copyleft +
  unaffiliated), human-protein-atlas (restrictive LICENSE vs MIT claim), fhir-momentum (PHI write +
  Pinecone), mixcr-analysis (MiXCR separate license), glygen (no LICENSE + hosted 503).

### Flagged
- human-protein-atlas, esmfold, gwas-mcp, encode-toolkit, fhir-momentum, mixcr-analysis, glygen —
  see verifier-state Flagged. Curator handoff: reconcile the gwas-mcp `supplier`/link to the
  canonical `muslus/gwas-mcp` owner.

## 2026-07-20 (bootstrap pass 27)

Twenty-seventh bootstrap pass — **7 pages stamped**, a mixed standalone MCP / plugin / skill batch
of unstamped pages. Each judgment grounded in a source fetched this run (GitHub repo + contents +
security-advisories APIs, PyPI JSON, and this repo's own `.claude-plugin/marketplace.json`). 4
works/cleared, 3 works/caution. No smoke run consumed for these (the smoke batch's `flowio`/`pymol`
etc. map to already-stamped pages). Stamped strictly sequentially (read-then-two-single-Edits per
file; state-file Read cache invalidated between edits as usual).

### Verified
- pdb — works/cleared. Official `rcsb/rcsb-mcp` MIT (GitHub API) + PyPI `rcsb-mcp` 0.9.0; RCSB PDB
  provenance, read-only public APIs, no GitHub advisories.
- chemlint — works/cleared. `molML/ChemLint` MIT, maintained (pushed 2026-06-29), advisories empty.
- composer — works/cleared. First-party Scripps plugin confirmed as `composer` at `./composer` in
  this repo's `.claude-plugin/marketplace.json`; install path `composer@sci-ai-enabler` current.
- amr-detection — works/cleared. `GPTomics/bioSkills` MIT (pushed 2026-07-18);
  `metagenomics/amr-detection/SKILL.md` confirmed via contents API; read-only local workflow.
- pubchem — works/caution. `JackKuo666/PubChem-MCP-Server` resolves + PyPI `pubchem-mcp-server`
  0.1.7; works via multiple paths but repo has no LICENSE (page claims MIT) and is stale 2025-04-07.
- certus — works/caution. `Certus_server` MIT resolves (canonical owner now
  `aditya-damerla128/Certus_server`; old path redirects); stale 2025-09-03, single-maintainer.
- clair-variant-caller — works/caution. `HKU-BAL/Clair-skills` resolves but no SPDX LICENSE
  (page already notes), single-maintainer.

### Security
- caution: pubchem (no LICENSE vs MIT claim + stale), certus (owner-renamed + stale +
  single-maintainer), clair-variant-caller (no SPDX LICENSE). All provenance-matched, no advisories.
- cleared: pdb, chemlint, composer, amr-detection.

### Flagged
- pubchem / certus / clair-variant-caller — security caution (see verifier-state Flagged); curator
  handoff to reconcile pubchem `Pricing` MIT claim and certus `supplier`/link to the current owner.

## 2026-07-20 (bootstrap pass 26)

Twenty-sixth bootstrap pass — **15 pages stamped**, a mixed standalone MCP / plugin / connector
batch of unstamped non-K-Dense / non-SciAgent pages. Each judgment grounded in a source fetched this
run (GitHub repo API, npm registry, PyPI JSON, official docs, or the `anthropics/life-sciences`
marketplace); advisory checks via GitHub `security-advisories` (GET, all empty) since OSV is
POST-only. 6 works/cleared, 7 works/caution, 2 degraded. No smoke run for these. Stamped strictly
sequentially (read-then-two-single-Edits per file).

### Verified
- rdkit-mcp — works. `tandemai-inc/rdkit-mcp-server` MIT, pushed 2026-05-04, advisories empty.
- spikelab — works. PyPI `spikelab` 0.1.2 MIT + `braingeneers/SpikeLab` MIT pushed 2026-07-02.
- seqera — works. Official docs.seqera.io confirm hosted endpoint `mcp.seqera.io/mcp` (OAuth-gated).
- healthlake-mcp — works. PyPI `awslabs.healthlake-mcp-server` 0.0.16 Apache-2.0 (AWS Labs), 2026-05-09.
- scholar-gateway — works. `wiley-scholar-gateway` dir confirmed in `anthropics/life-sciences`
  marketplace (OAuth-gated).
- synapse — works. `synapse` dir confirmed in same marketplace; endpoint on Sage's mcp.synapse.org.
- molecule-mcp — works. `ChatMol/molecule-mcp` MIT (stale, last push 2025-04-20).
- openmm-mcp — works. `PhelanShao/openmm-mcp-server` resolves (stale 2025-05-31).
- rdkit-agent — works. npm `rdkit-agent` 0.1.1 MIT + GitHub resolve (Alpha, 9 stars).
- labmate-mcp — works. PyPI `labmate-mcp` 7.3.1 MIT + `JonasRackl/labmate-mcp` MIT (2 stars).
- scitex — works. PyPI `scitex` 2.30.8 AGPL-3.0-only.
- drugbank — works. `openpharma-org/drugbank-mcp-server` resolves (unofficial wrapper).
- neuroflow — works. `stanislavjiricek/neuroflow` MIT, pushed 2026-06-04 (early Beta, 6 stars).
- novomcp — degraded. Site loads but MCP endpoints API-key/application-gated (research preview).
- cortellis — degraded. Plugin dir confirmed in `anthropics/life-sciences` but Clarivate-subscription-gated.

### Fixed
- None this run.

### Flagged
- novomcp — verification degraded + security unknown: closed-source hosted SaaS (Quant NexusAI), no
  published client source or license, endpoints application-gated.
- cortellis — verification degraded + security caution: closed-source commercial connector,
  subscription-gated data, and Clarivate exploring a sale of its Life Sciences & Healthcare segment.
- drugbank — security caution: unofficial community wrapper (not affiliated with DrugBank), GitHub
  license classifier null, requires user-supplied license-gated DrugBank data.
- molecule-mcp, openmm-mcp, rdkit-agent, labmate-mcp, scitex, neuroflow — security caution: each a
  single-maintainer and/or stale and/or license-signal risk (see verifier-state Flagged for detail).
  All verification works.

### Security
- 6 cleared: rdkit-mcp, spikelab, seqera, healthlake-mcp, scholar-gateway, synapse — provenance
  matches supplier, permissive/Apache licenses, maintained, no advisories. seqera/healthlake are
  write-capable (healthlake handles PHI — use --readonly + a signed BAA); no provenance concern.
- 7 caution + 2 degraded — see Flagged.

### Deferred
- ~55 catalog pages remain unstamped after this run. Remaining standalone MCP servers (`blast`,
  scmcphub `scanpy`/`decoupler-mcp`/`liana-mcp`/`cellrank-mcp`) and any other non-K-Dense/non-SciAgent
  pages surfaced by an LS sweep of `catalog/tools/` are the next priority.

## 2026-07-20 (bootstrap pass 25)

Twenty-fifth bootstrap pass — **28 pages stamped**. Two groups. First, the **NeuroClaw remainder +
bedtools** (7 pages): the final 6 unstamped `supplier: NeuroClaw` non-`-skill` pages
(`qsiprep-tool`, `run_models`, `spacenet`, `wmh-segmentation`, `nii2dcm`, `nilearn-tool`) plus
`bedtools-genomic-intervals` — all `works`/`cleared`. Second, the **Anthropic `tool_type: Claude.ai
Connector` batch** (21 pages): 16 Anthropic-hosted Claude Science featured-connector data sources +
`ketcher` + `medidata` graded `works`/`cleared`; `owkin` + `revvity-signals` + `inductive-bio`
graded `degraded`/`cleared` (provenance confirmed but no publicly resolvable MCP endpoint). All
judgments grounded in sources fetched this run (Anthropic Claude Science connectors-and-skills doc,
`anthropics/life-sciences` marketplace.json, `epam/ketcher` GitHub API, and cited vendor press for
revvity/inductive-bio; no smoke run for these).

### Verified
- NeuroClaw remainder (6) — all works, on the confirmed clone + `cp -r NeuroClaw/skills/<slug>`
  install path against `CUHK-AIM-Group/NeuroClaw`: qsiprep-tool, run_models, spacenet,
  wmh-segmentation, nii2dcm, nilearn-tool. No NeuroClaw pages remain unstamped.
- bedtools-genomic-intervals — works.
- 16 Anthropic-hosted Claude Science featured connectors — all works/cleared, presence confirmed in
  the Anthropic connectors-and-skills doc: metabolights, mgnify (Omics Archives); complex-portal,
  intact (Structures & Interactions); rfam (RNA); rhea, chebi, bindingdb (Chemistry); finngen,
  eqtl-catalogue, biobank-japan (Human Genetics); biomart; antibody-registry; cellguide; civic,
  clingen (Clinical Genomics). Anthropic-hosted, read-only, no per-connector MCP URL.
- ketcher — works. Anthropic connector confirmed in the doc; underlying `epam/ketcher` repo live and
  Apache-2.0 (GitHub API, pushed 2026-07-20, 841 stars); client-side 2D editor, no credentials.
- medidata — works. Listed as `medidata` in `anthropics/life-sciences` marketplace.json; install path
  resolves to the published hosted endpoint `mcp.imedidata.com/mcp` (tool responses need iMedidata login).
- owkin — degraded. Listed in the marketplace.json; MCP endpoint URL and tool list vendor-gated
  behind an Owkin account, so not functionally resolvable from public sources.
- revvity-signals — degraded. Directory listing confirmed via cited press (CLP, 2026-07-01); no
  public MCP endpoint or self-serve sign-up.
- inductive-bio — degraded. MCP-connector launch confirmed via cited PR Newswire (2026-06-30); no
  public MCP endpoint or self-serve sign-up.

### Fixed
- None this run.

### Flagged
- None broken this run.

### Security
- All 28 cleared. NeuroClaw remainder + bedtools: read-only local analysis, provenance matches
  supplier repo, no advisories (`nii2dcm` note reflects MIT skill code wrapping BSD-3-Clause upstream).
- 16 featured connectors + ketcher: Anthropic-hosted, read-only public data (EMBL-EBI / CC-licensed /
  client-side), no credentials. medidata/owkin: official marketplace entries, vendor-hosted remote
  MCP, read-only, access gated by a vendor account. revvity-signals/inductive-bio: vendor connectors
  in Anthropic's directory (press-confirmed), read-only, enterprise-gated, no public endpoint
  (inductive-bio: per vendor, submitted structures not retained or used for training).

### Deferred
- ~70 catalog pages remain unstamped (448 total, ~378 stamped after this run). NeuroClaw, SciAgent,
  GPTomics, and the Claude.ai Connector families are now fully stamped; next runs should target the
  remaining oldest/unstamped pages across other suppliers.

## 2026-07-20 (bootstrap pass 24)

Twenty-fourth bootstrap pass — one supplier batch, **25 pages stamped, all `works`/`cleared`**. The
**NeuroClaw non-`-skill` tool/model pages**: 25 unstamped `supplier: NeuroClaw` catalog entries
against the anchor `CUHK-AIM-Group/NeuroClaw`. These are Skill-doc type — Claude runs the skill's
Python locally via Bash (clone + `cp -r`), not an MCP server — so each is graded `works` on the
confirmed-current clone/copy install path. Every target slug was confirmed present under the repo's
`skills/` tree via two direct GitHub contents-API fetches this run. All judgments grounded in sources
fetched this run (1 GitHub repo check + contents-API listings + one representative SKILL.md read +
the GitHub security-advisories endpoint; no smoke run for these).

### Verified
- Anchor `CUHK-AIM-Group/NeuroClaw` confirmed via GitHub API (MIT spdx_id, not archived, not
  disabled, pushed 2026-07-14, updated 2026-07-19, 75 stars, 0 open issues, default branch main).
- 25 NeuroClaw Claude Skills — all works. Each skill dir confirmed present via the contents API:
  svm, freesurfer-tool, bnt, brain-visualization, brain_gnn, combraintf, conn-tool, dcm2nii,
  detrending, dictlearning, dipy-tool, filtering, fm_app, fmriprep-tool, fsl-tool, glm,
  harmonization-tool, hcppipeline-tool, hierarchical, ibgnn, ica, kmeans, lggnn, mne-eeg-tool,
  neurostorm. Clone + `cp -r NeuroClaw/skills/<slug>` install paths resolve.

### Fixed
- None this run.

### Security
- All 25 cleared. Provenance matches supplier `CUHK-AIM-Group/NeuroClaw`; repo MIT, not archived,
  no OSV/GitHub advisories (security-advisories endpoint empty). Read `skills/run_models/SKILL.md`
  (representative) — read-only local orchestration under `./run_models_output/`, no API-key/credential
  requests, no install-time arbitrary code, no exfiltration.
- Note (`dcm2nii`): its Pricing line cites BSD-3-Clause for the wrapped rordenlab/dcm2niix binary;
  the stamp note reflects skill code MIT wrapping BSD-3-Clause dcm2niix (not a provenance mismatch).

### Deferred
- ~6 NeuroClaw non-`-skill` pages remain unstamped for next run: qsiprep-tool, run_models, spacenet,
  wmh-segmentation, nii2dcm, nilearn-tool (all present in `skills/`; same grading expected).

## 2026-07-20 (bootstrap pass 23)

Twenty-third bootstrap pass — two supplier batches, 19 pages stamped, all `works`/`cleared`. First,
the **SciAgent non-`-database` skills, batch 4**: 15 more unstamped `supplier: SciAgent` Claude Skill
pages against the re-confirmed anchor `jaechang-hits/SciAgent-Skills`. Second, the **GPTomics
bioSkills** batch: 4 unstamped `supplier: GPTomics bioSkills` pages against the newly-confirmed anchor
`GPTomics/bioSkills`. Both are Skill-doc type — Claude runs the skill's Python/CLI locally via Bash,
not an MCP server — so each is graded `works` on the confirmed-current clone/copy install path. Each
skill's directory was confirmed present with its `SKILL.md` via direct GitHub contents-API fetches
this run. All judgments grounded in sources fetched this run (2 GitHub repo checks + per-skill
contents API listings; no smoke run for these).

### Verified
- Anchor `jaechang-hits/SciAgent-Skills` re-confirmed via GitHub API (root LICENSE verbatim CC BY
  4.0, GitHub NOASSERTION, not archived, not disabled, pushed 2026-06-15, updated 2026-07-20, 276
  stars, 7 open issues, default branch main). New parent dir `data-visualization/` confirmed.
- Anchor `GPTomics/bioSkills` confirmed via GitHub API (MIT spdx_id, not archived, not disabled,
  pushed 2026-07-18, updated 2026-07-20, 1037 stars, 0 open issues, default branch main).
- 15 SciAgent Claude Skills — all works. Each skill dir confirmed present with SKILL.md via the
  contents API: mdanalysis-trajectory, sar-analysis, smina-molecular-docking
  (structural-biology-drug-discovery); multiqc-qc-reports (genomics-bioinformatics/qc);
  plannotate-plasmid-annotation, sgrna-design-guide (molecular-biology); libsbml-network-modeling
  (systems-biology-multiomics); plotly-interactive-plots (data-visualization); napari-image-viewer,
  opencv-bioimage-analysis, cellpose-cell-segmentation, scikit-image-processing (cell-biology);
  celltypist-cell-annotation, harmony-batch-correction (genomics-bioinformatics/single-cell);
  simpleitk-image-registration (medical-imaging). Clone/copy install paths resolve.
- 4 GPTomics bioSkills — all works. Each skill dir confirmed present with SKILL.md via the contents
  API: neoantigen-prediction, epitope-prediction, mhc-class-ii-prediction (immunoinformatics);
  scirpy-analysis (tcr-bcr-analysis). Clone + `./install-claude.sh` / `cp -r` install paths resolve.

### Fixed
- None this run.

### Flagged
- None broken this run.

### Security
- All 19 cleared. SciAgent: provenance matches jaechang-hits, root LICENSE CC BY 4.0, no GitHub
  security-advisories, read-only local analysis with no credential/API-key requests (the pages'
  `Pricing` lines cite each wrapped library's own OSS license, not a skill-code provenance issue).
- GPTomics: provenance matches GPTomics/bioSkills, MIT, no GitHub security-advisories, read-only
  local pVACtools/scirpy workflow with no credential requests (optional public IEDB API with a
  preferred local install).

## 2026-07-20 (bootstrap pass 22)

Twenty-second bootstrap pass — the **SciAgent non-`-database` skills, batch 3**: 10 more unstamped
`supplier: SciAgent` Claude Skill pages, all sharing the anchor `jaechang-hits/SciAgent-Skills`.
Each skill's parent directory was confirmed present via a direct GitHub contents-API fetch this run
(8 distinct parent dirs). Skill-doc type — Claude runs the skill's Python/CLI locally via Bash, not
an MCP server — so each is graded `works` on the confirmed-current clone/copy install path. All
judgments grounded in sources fetched this run (GitHub repo + 8 contents API listings).

### Verified
- Anchor `jaechang-hits/SciAgent-Skills` re-confirmed via GitHub API (root LICENSE verbatim CC BY
  4.0, GitHub NOASSERTION, not archived, not disabled, pushed 2026-06-15, updated 2026-07-20, 275
  stars, 7 open issues, default branch main).
- 10 SciAgent Claude Skills — all works. Each parent dir confirmed present via the contents API:
  viennarna-structure-prediction (molecular-biology); mdtraj-trajectory-analysis
  (structural-biology-drug-discovery); fastp-fastq-preprocessing (genomics-bioinformatics/qc);
  western-blot-quantification (lab-automation); ucsc-genome-browser
  (genomics-bioinformatics/databases); nnunet-segmentation (medical-imaging); maxquant-proteomics
  (proteomics-protein-engineering); omics-analysis-guide, mofaplus-multi-omics,
  cellchat-cell-communication (systems-biology-multiomics). Clone/copy install paths resolve.

### Fixed
- None this run.

### Flagged
- None broken this run.

### Security
- 9 of 10 cleared — provenance matches jaechang-hits, root LICENSE CC BY 4.0, no GitHub
  security-advisories, read-only local analysis with no credential/API-key requests.
- `kegg-pathway-analysis` — caution. Skill code is CC BY 4.0 and provenance matches, but the
  underlying KEGG data needs a paid commercial license for non-academic use (data-use restriction
  only; verification `works`).

## 2026-07-20 (bootstrap pass 21)

Twenty-first bootstrap pass — the **SciAgent non-`-database` skills, batch 2**: 10 more unstamped
`supplier: SciAgent` Claude Skill pages, all sharing the anchor `jaechang-hits/SciAgent-Skills`.
Each skill's parent directory was confirmed present via the GitHub contents API; one representative
`SKILL.md` (Prokka) was read to confirm read-only local analysis with no credential/API-key
requests and no runtime network calls. All judgments grounded in sources fetched this run (GitHub
repo + contents + security-advisories APIs, one SKILL.md).

### Verified
- Anchor `jaechang-hits/SciAgent-Skills` re-confirmed via GitHub API (root LICENSE verbatim CC BY
  4.0, not archived, not disabled, pushed 2026-06-15, 275 stars, 7 open issues, default branch main).
- 10 SciAgent Claude Skills — all works. Each parent dir confirmed present via the contents API:
  snakemake-workflow-engine, spikeinterface-electrophysiology (scientific-computing);
  prokka-genome-annotation, bakta-genome-annotation, roary-pangenome (annotation);
  trackpy-particle-tracking, pyimagej-fiji-bridge (cell-biology); popv-cell-annotation,
  single-cell-annotation-guide (single-cell); muon-multiomics-singlecell (systems-biology-multiomics).
  Clone/copy install paths resolve.

### Fixed
- None this run.

### Flagged
- None broken this run.

### Security
- All 10 cleared — provenance matches jaechang-hits, CC BY 4.0 root LICENSE, no GitHub
  security-advisories, read-only local skills with no credential requests.

## 2026-07-20 (bootstrap pass 20)

Twentieth bootstrap pass — the **SciAgent genomics-bioinformatics skills** (non-`-database` batch 1):
13 unstamped `supplier: SciAgent` Claude Skill pages, all sharing the anchor
`jaechang-hits/SciAgent-Skills`. Each skill directory was individually confirmed present via the
GitHub contents API; one representative `SKILL.md` (DESeq2) was read raw to confirm read-only local
analysis with no credential/API-key requests. All judgments grounded in sources fetched this run
(GitHub repo + contents + security-advisories APIs, one raw SKILL.md).

### Verified
- Anchor `jaechang-hits/SciAgent-Skills` via GitHub API (root LICENSE verbatim CC BY 4.0, not
  archived, not disabled, pushed 2026-06-15, 275 stars, default branch main).
- 13 SciAgent Claude Skills — all works. Each skill directory confirmed present via the contents
  API: deseq2-differential-expression, featurecounts-rna-counting, salmon-rna-quantification,
  gseapy-gene-enrichment (rnaseq); star-rna-seq-aligner, samtools-bam-processing,
  bwa-mem2-dna-aligner (alignment); gatk-variant-calling, snpeff-variant-annotation,
  cnvkit-copy-number, plink2-gwas-analysis (variant); macs3-peak-calling, homer-motif-analysis
  (top-level genomics-bioinformatics). Clone/copy install paths resolve.

### Fixed
- None this run.

### Flagged
- None broken this run.

### Security
- 13 pages cleared — provenance matches `jaechang-hits/SciAgent-Skills`, CC BY 4.0 root LICENSE,
  read-only local skills, no GitHub security advisories.
- `gseapy-gene-enrichment` note records that it calls the public Enrichr API (no key required).

## 2026-07-20 (bootstrap pass 19)

Nineteenth bootstrap pass — the **ToolUniverse family**: 19 unstamped `supplier: Zitnik Lab
(Harvard Medical School)` pages (1 MCP server + 18 Claude Skills), all sharing the single anchor
`mims-harvard/ToolUniverse`. Each skill directory was individually confirmed present via the GitHub
contents API; the MCP server was corroborated against PyPI. All judgments grounded in sources
fetched this run (GitHub repo + contents + security-advisories APIs, PyPI JSON).

### Verified
- `tooluniverse` — works / cleared. Anchor `mims-harvard/ToolUniverse` via GitHub API (Apache-2.0,
  not archived, pushed 2026-07-20, 1578 stars, default branch main) + PyPI `tooluniverse` 1.0.22.
  `uvx tooluniverse` install path resolves.
- 18 `tooluniverse-*` Claude Skills — all works. Each `skills/tooluniverse-<slug>/SKILL.md`
  confirmed present via the contents API: target-research, drug-research, drug-target-validation,
  precision-oncology, rare-disease-diagnosis, pharmacovigilance, immunotherapy-response-prediction,
  gwas-drug-discovery, small-molecule-discovery, rare-disease-genomics, drug-synergy,
  adverse-event-detection, adverse-outcome-pathway, cancer-genomics-tcga,
  cancer-variant-interpretation, chemical-safety, binder-discovery, drug-drug-interaction.

### Fixed
- None this run.

### Flagged
- None broken this run.

### Security
- 17 pages cleared — provenance matches Zitnik Lab (`mims-harvard/ToolUniverse`), Apache-2.0, each
  skill dir confirmed present, no GitHub security advisories.
- `tooluniverse-binder-discovery` — caution. Provenance/Apache-2.0 clear and skill dir confirmed,
  but docking/generation calls external NVIDIA NIM endpoints requiring a user `NVIDIA_API_KEY`.
- `tooluniverse-drug-drug-interaction` — caution. Provenance/Apache-2.0 clear and skill dir
  confirmed, but ships a `.env.template` requesting user API keys for external DBs
  (BioGRID DisGeNET OMIM USPTO NVIDIA BRENDA).

## 2026-07-20 (bootstrap pass 18)

Eighteenth bootstrap pass — a second batch of **non-K-Dense standalone** entries: five Claude Science
model skills anchored to their own OSS GitHub repos, two self-hosted MCP servers (each also on PyPI),
and three entries with issues (an unlicensed MCP, a transferred repo, and a hosted API whose
documented npm client is a dead package). All judgments grounded in sources fetched this run
(GitHub / PyPI / npm registry APIs and endpoint probes).

### Verified
- `evo2` — works / cleared. Anchor `ArcInstitute/evo2` via GitHub API (Apache-2.0, not archived,
  pushed 2026-06-19, 3993 stars). OSS `git clone` path current.
- `scgpt` — works / cleared. Anchor `bowang-lab/scGPT` (MIT, not archived, pushed 2026-04-29,
  1605 stars). OSS clone path current.
- `proteinmpnn` — works / cleared. Anchor `dauparas/ProteinMPNN` (MIT, not archived, 1796 stars;
  stable research model). OSS clone path current.
- `solublempnn` — works / cleared. Anchor `dauparas/LigandMPNN` (MIT, not archived, active, 605
  stars) where the soluble-optimized weights ship. OSS clone path current.
- `openfold3` — works / cleared. Anchor `aqlaboratory/openfold` (Apache-2.0, not archived, pushed
  2025-12-16, 3397 stars). OSS clone path current.
- `chatspatial` — works / cleared. Anchor `cafferychen777/ChatSpatial` (MIT, not archived, pushed
  2026-07-16) + PyPI `chatspatial` 1.2.10 (MIT). pip/Docker install paths resolve.
- `biocontextai` — works / cleared. Anchor `biocontext-ai/knowledgebase-mcp` (Apache-2.0, not
  archived) + PyPI `biocontext_kb` 0.2.1 (Apache-2.0). `uvx` install path resolves.
- `neurosift` — works / caution. Anchor `magland/neurosift-mcps` resolves (not archived, not
  disabled) and the clone/build install path is current, but the repo has **no LICENSE**,
  single-maintainer, last push 2025-11-03.

### Fixed
- `allenbrain` — the GitHub API for `maflot/allenbrain-mcp` reports `full_name: MCPmed/allenbrain-mcp`;
  the repo was transferred to the MCPmed org. Updated the `git clone` command and the Sources link
  to the canonical `MCPmed/allenbrain-mcp`. Graded verification `degraded` (owner drift, page's
  Supplier still says `maflot` — curator to reconcile).

### Flagged
- `covasyn` — verification `degraded` + security `caution`. Hosted endpoint `mcp.covasyn.com/mcp`
  responds (HTTP 406, API-key gated — a live endpoint, not dead), but the page's documented npm
  `@covasyn/mcp-client` stdio proxy is a **confirmed 404** (`registry.npmjs.org/-/v1/search?text=covasyn`
  returns 0 packages). The real connection method is behind covasyn.com account login, so no
  primary-source fix was possible; left for the curator to reconcile the two stdio-proxy blocks.
- `allenbrain` — security `caution`: repo transferred to MCPmed org, no LICENSE, Alpha,
  single-maintainer.

### Security
- OSV `api.osv.dev/v1/query` is POST-only and WebFetch is GET-only (405), so advisory checks used the
  GitHub `repos/<org>/<repo>/security-advisories` endpoint (empty for evo2, openfold, ChatSpatial).
- Provenance matched supplier for all seven cleared entries. `neurosift` and `covasyn` carry
  license/provenance cautions (unlicensed repo; personal-account examples repo for a commercial
  hosted service); `allenbrain` carries an ownership-drift caution.

## 2026-07-20 (bootstrap pass 17)

Seventeenth bootstrap pass — first batch of **non-K-Dense standalone** entries: two Claude Science
model skills anchored to their own OSS repos, two API/agent skills, and two subscription-gated
`anthropics/life-sciences` MCP connectors. All judgments grounded in sources fetched this run.

### Verified
- `borzoi` — works / cleared. Anchor `calico/borzoi` via GitHub API (Apache-2.0, not archived,
  `disabled:false`, 254 stars, pushed 2025-08-28 — stable research model, default branch `main`).
  OSS `git clone` path confirmed current.
- `chai-1` — works / cleared. Anchor `chaidiscovery/chai-lab` (Apache-2.0, not archived, active,
  1970 stars). OSS clone path confirmed current.
- `boltz` — works / caution. Anchor `boltz-bio/boltz-api-skills` (MIT, active); confirmed listed in
  `anthropics/claude-plugins-official` marketplace.json pointing at that repo `plugins/boltz`.
  Supplier boltz.bio loads.
- `biomni` — works / caution. Anchor `snap-stanford/Biomni` (Apache-2.0, active, 3517 stars) + PyPI
  `biomni` 0.0.8 (Apache-2.0) + wrapper `davila7/claude-code-templates` (MIT, active). All three
  install targets resolve.
- `consensus` — degraded / cleared. Plugin present in `anthropics/life-sciences` marketplace.json;
  MCP server needs a Consensus.app account, so functionally unverifiable without a subscription.
- `adisinsight` — degraded / cleared. Plugin `adisinsight` v1.0.0 present in `anthropics/life-sciences`;
  `plugin.json` MCP endpoint `adisinsight-mcp.springer.com/mcp` resolves to the supplier host; needs
  an AdisInsight subscription, so functionally unverifiable.

### Fixed
- None — no broken install targets or metadata in this batch.

### Flagged
- `boltz`, `biomni` — security caution (informational): `boltz` ships a `BOLTZ_API_KEY` to the
  hosted paid Boltz API; `biomni`'s A1 agent executes LLM-generated code with full system
  privileges. Provenance/license are clean — no mismatch.
- `consensus`, `adisinsight` — verification degraded (subscription/account-gated remote MCP servers,
  not testable without credentials).

### Security
- `borzoi`, `chai-1` — cleared. Provenance matches the page supplier; Apache-2.0; GitHub
  `security-advisories` endpoint empty for both.
- `boltz` — caution. Provenance matches boltz-bio (MIT, official marketplace) but external paid-API
  key dependency.
- `biomni` — caution. Apache-2.0 and provenance match, but full-privilege code execution — sandbox.
- `consensus`, `adisinsight` — cleared. Anthropic-packaged in the official life-sciences marketplace;
  endpoints/provenance match the stated supplier; read-only.
- Tooling note: OSV `api.osv.dev/v1/query` is POST-only and WebFetch is GET-only (405); advisory
  checks used the GitHub `repos/<org>/<repo>/security-advisories` endpoint (all empty this run).

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
